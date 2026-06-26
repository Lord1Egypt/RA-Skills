"""
scrape_profile.py
Scrapes Douyin creator homepage videos via MediaCrawler (NanmiCoder/MediaCrawler).
MediaCrawler uses CDP mode + stealth, providing much better anti-detection than raw Playwright.

Usage:
    python scripts/scrape_profile.py
    python scripts/scrape_profile.py --url https://www.douyin.com/user/xxx
    python scripts/scrape_profile.py --limit 5
"""

import argparse
import asyncio
import csv
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from storage import DATA_DIR
from utils_platform import platform_defaults

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── 路径配置 ──────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

OUTPUT_DIR = DATA_DIR
COOKIE_FILE = BASE_DIR / ".douyin_cookies.json"
MEDIACRAWLER_DIR = Path(os.getenv("MEDIACRAWLER_DIR", platform_defaults()))
MEDIACRAWLER_CFG = MEDIACRAWLER_DIR / "config" / "base_config.py"

OUTPUT_DIR.mkdir(exist_ok=True)

# ── 默认目标博主 ───────────────────────────────────────────────
DEFAULT_URL = (
    "https://www.douyin.com/user/"
    "MS4wLjABAAAAQZR8MKh0fcPVUQMTgxJll5B5iy-10GR8spJPo-KUrxU"
)


def check_cookie_age() -> int:
    """返回 Cookie 文件存活天数，-1 表示文件不存在"""
    if not COOKIE_FILE.exists():
        return -1
    return int((time.time() - COOKIE_FILE.stat().st_mtime) / 86400)


def load_cookie_string() -> str:
    """将 .douyin_cookies.json 转为 key=val; key2=val2 格式字符串"""
    if not COOKIE_FILE.exists():
        return ""
    cookies = json.loads(COOKIE_FILE.read_text(encoding="utf-8"))
    return "; ".join(f"{c['name']}={c['value']}" for c in cookies if c.get("name"))


def set_mediacrawler_max_count(n: int) -> str:
    """临时修改 MediaCrawler 的 CRAWLER_MAX_NOTES_COUNT，返回原始内容供恢复"""
    text = MEDIACRAWLER_CFG.read_text(encoding="utf-8")
    new_text = re.sub(
        r"^(CRAWLER_MAX_NOTES_COUNT\s*=\s*)\d+",
        rf"\g<1>{n}",
        text,
        flags=re.MULTILINE,
    )
    MEDIACRAWLER_CFG.write_text(new_text, encoding="utf-8")
    return text


def ensure_mediacrawler_ready() -> None:
    required = [
        MEDIACRAWLER_DIR,
        MEDIACRAWLER_DIR / "main.py",
        MEDIACRAWLER_DIR / "config" / "base_config.py",
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "MediaCrawler 路径无效，请在 .env 中配置 MEDIACRAWLER_DIR。\n"
            + "缺失路径：\n- "
            + "\n- ".join(missing)
        )


def find_latest_jsonl(save_path: Path) -> Path | None:
    """找到 MediaCrawler 最新写入的 creator_contents JSONL 文件"""
    jsonl_dir = save_path / "douyin" / "jsonl"
    if not jsonl_dir.exists():
        return None
    files = list(jsonl_dir.glob("creator_contents_*.jsonl"))
    return max(files, key=lambda f: f.stat().st_mtime, default=None)


def parse_jsonl_to_records(jsonl_path: Path, blogger_name: str) -> list[dict]:
    """将 MediaCrawler JSONL 转为我们的 CSV 字段格式"""
    records = []
    for line in jsonl_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        item = json.loads(line)

        # 发布时间：Unix 秒 → 可读字符串
        create_time = item.get("create_time", 0)
        pub_time = ""
        if create_time:
            try:
                pub_time = datetime.fromtimestamp(int(create_time)).strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                pass

        nickname = item.get("nickname") or blogger_name

        records.append({
            "博主昵称": nickname,
            "视频标题": item.get("title") or item.get("desc", ""),
            "视频链接": item.get("aweme_url", ""),
            "播放量": "",  # MediaCrawler creator API 不返回播放量
            "点赞数": item.get("liked_count", ""),
            "评论数": item.get("comment_count", ""),
            "转发数": item.get("share_count", ""),
            "收藏数": item.get("collected_count", ""),
            "发布时间": pub_time,
            "采集时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
    return records


def run_mediacrawler(creator_url: str, save_path: Path, limit: int) -> bool:
    """调用 MediaCrawler subprocess 采集博主主页"""
    ensure_mediacrawler_ready()
    cookie_str = load_cookie_string()

    # 设置 MediaCrawler 最多抓取条数（多取一些，后续按 limit 裁剪）
    fetch_count = max(limit * 2, 20) if limit > 0 else 50
    original_cfg = set_mediacrawler_max_count(fetch_count)

    cmd = [
        sys.executable,
        str(MEDIACRAWLER_DIR / "main.py"),
        "--platform", "dy",
        "--lt", "cookie" if cookie_str else "qrcode",
        "--type", "creator",
        "--creator_id", creator_url,
        "--get_comment", "no",
        "--get_sub_comment", "no",
        "--save_data_option", "jsonl",
        "--save_data_path", str(save_path),
    ]
    if cookie_str:
        cmd += ["--cookies", cookie_str]

    print(f"  启动 MediaCrawler（CDP 模式）... 路径：{MEDIACRAWLER_DIR}")
    try:
        result = subprocess.run(
            cmd,
            cwd=str(MEDIACRAWLER_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
        )
    except subprocess.TimeoutExpired:
        print("  MediaCrawler 超时，尝试使用已采集的部分数据")
        return True
    finally:
        MEDIACRAWLER_CFG.write_text(original_cfg, encoding="utf-8")

    if result.returncode != 0:
        print("  MediaCrawler 失败，最后输出：")
        for line in (result.stdout + result.stderr).splitlines()[-15:]:
            print(f"    {line}")
    return result.returncode == 0


async def scrape(url: str, scroll_count: int = 50, headless: bool = False,
                 auto: bool = False, limit: int = 0) -> str | None:
    """主采集入口，兼容 track_latest.py 调用接口"""
    # Cookie 有效期预警
    age = check_cookie_age()
    if age == -1:
        print("  ⚠️  未找到 Cookie 文件，将使用扫码登录")
    elif age > 20:
        print(f"  ⚠️  Cookie 已 {age} 天未更新（有效期约 7~30 天），建议重新登录")
        print("     运行：python scripts/scrape_profile.py")

    save_path = OUTPUT_DIR / "_mc_temp"
    save_path.mkdir(parents=True, exist_ok=True)

    # 记录运行前已有的文件（用于识别新产生的文件）
    jsonl_dir = save_path / "douyin" / "jsonl"
    before = set(jsonl_dir.glob("creator_contents_*.jsonl")) if jsonl_dir.exists() else set()

    ok = run_mediacrawler(url, save_path, limit)

    if not ok:
        return None

    # 找到本次新生成的 JSONL：优先用差集，回退到 mtime 最新
    after = set(jsonl_dir.glob("creator_contents_*.jsonl")) if jsonl_dir.exists() else set()
    new_files = after - before
    jsonl_file = max(new_files or after, key=lambda f: f.stat().st_mtime, default=None)
    if not jsonl_file:
        print("  MediaCrawler 未生成输出文件，采集失败")
        return None

    # 从文件名或内容中获取博主昵称
    blogger_name = "未知博主"

    records = parse_jsonl_to_records(jsonl_file, blogger_name)
    if not records:
        print("  未解析到任何视频数据")
        print("  可能原因：Cookie 失效 / 账号被限流 / 博主主页为空")
        print("  建议：重新运行 python scripts/scrape_profile.py 扫码登录")
        return None

    # 从第一条记录取博主昵称
    blogger_name = records[0].get("博主昵称", "未知博主")

    # 按 limit 裁剪
    if limit > 0 and len(records) > limit:
        print(f"  仅保留最新 {limit} 条（共采集到 {len(records)} 条）")
        records = records[:limit]

    print(f"  博主：{blogger_name}，共 {len(records)} 条视频")

    # 保存 CSV
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = re.sub(r'[\\/:*?"<>|]', "_", blogger_name)
    out_path = OUTPUT_DIR / f"{safe_name}_{ts}.csv"

    fieldnames = ["博主昵称", "视频标题", "视频链接", "播放量", "点赞数", "评论数", "转发数", "收藏数", "发布时间", "采集时间"]
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"  已保存 → {out_path}")
    return str(out_path)


def run(url: str = DEFAULT_URL, scroll_count: int = 50, auto: bool = False, limit: int = 0):
    """供 main.py / track_latest.py 调用的同步入口"""
    return asyncio.run(scrape(url, scroll_count, auto=auto, limit=limit))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="抖音博主主页视频采集（MediaCrawler 版）")
    parser.add_argument("--url", default=DEFAULT_URL, help="博主主页链接")
    parser.add_argument("--limit", type=int, default=0, help="仅保留最新 N 条（0=全部）")
    parser.add_argument("--auto", action="store_true", help="兼容参数：保留给自动模式调用")
    args = parser.parse_args()

    asyncio.run(scrape(args.url, auto=args.auto, limit=args.limit))





