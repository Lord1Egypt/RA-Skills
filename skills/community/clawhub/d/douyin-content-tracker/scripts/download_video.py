"""
下载音频.py
用 Playwright 打开视频页，拦截抖音 aweme API 响应拿到真实视频 URL，
再用 ffmpeg 只提取音频流（.m4a），不保存完整视频。
"""

import asyncio
import json
import random
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from run_state import (
    current_run_id,
    read_current_run,
    resolve_cleaned_files,
    write_current_run,
)
from storage import AUDIO_DIR, DATA_DIR
from utils import compute_engagement_rate, video_id_from_url

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv(Path(__file__).parent.parent / ".env")

BASE_DIR       = Path(__file__).parent.parent
COOKIE_FILE    = BASE_DIR / ".douyin_cookies.json"
DOWNLOADED_LOG = AUDIO_DIR / "downloaded.txt"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)


# ── ffmpeg 路径：优先 PATH，其次 imageio-ffmpeg 内置 ──────────────
def _get_ffmpeg() -> str:
    import shutil
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        # Windows：imageio-ffmpeg 的 exe 带版本号，复制为纯 ffmpeg.exe 供调用
        if sys.platform.startswith("win"):
            no_ext = Path(exe).parent / "ffmpeg.exe"
            if not no_ext.exists():
                shutil.copy(exe, no_ext)
            return str(no_ext)
        return exe
    except ImportError:
        return "ffmpeg"


FFMPEG_EXE = _get_ffmpeg()


def load_downloaded() -> set[str]:
    if DOWNLOADED_LOG.exists():
        return set(DOWNLOADED_LOG.read_text(encoding="utf-8").splitlines())
    return set()


def save_downloaded(video_id: str, downloaded: set[str] | None = None):
    if downloaded is not None and video_id in downloaded:
        return
    with open(DOWNLOADED_LOG, "a", encoding="utf-8") as f:
        f.write(video_id + "\n")
    if downloaded is not None:
        downloaded.add(video_id)


def audio_file_exists(save_path: Path) -> bool:
    return save_path.exists() and save_path.stat().st_size > 1_000


def ytdlp_download_audio(url: str, save_path: Path, retries: int = 2) -> bool:
    """yt-dlp 备用下载：Playwright 拿不到 URL 时使用"""
    import shutil
    if not shutil.which("yt-dlp"):
        print("    yt-dlp 未安装，请运行：pip install yt-dlp")
        return False
    save_path.parent.mkdir(parents=True, exist_ok=True)
    # yt-dlp 会自动追加真实扩展名，模板去掉 .m4a 后缀
    out_template = str(save_path.with_suffix("")) + ".%(ext)s"
    cmd = [
        "yt-dlp",
        "-x", "--audio-format", "m4a",
        "--no-playlist",
        "-o", out_template,
        "--quiet", "--no-warnings",
        url,
    ]
    for attempt in range(1, retries + 1):
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=180)
            if result.returncode == 0 and audio_file_exists(save_path):
                return True
            stderr = result.stderr.decode(errors="replace")[:300]
            print(f"    yt-dlp 退出码 {result.returncode}：{stderr}")
        except subprocess.TimeoutExpired:
            print(f"    yt-dlp 超时（第 {attempt} 次）")
        except Exception as e:
            print(f"    yt-dlp 失败（第 {attempt} 次）：{e}")
        if save_path.exists():
            save_path.unlink()
        if attempt < retries:
            time.sleep(3 * attempt)
    return False


def extract_audio(video_url: str, save_path: Path, retries: int = 3) -> bool:
    """用 ffmpeg 从视频 URL 提取音频流，保存为 .m4a，失败自动重试"""
    save_path.parent.mkdir(parents=True, exist_ok=True)
    headers = (
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36\r\n"
        "Referer: https://www.douyin.com/\r\n"
    )
    for attempt in range(1, retries + 1):
        try:
            result = subprocess.run(
                [
                    FFMPEG_EXE,
                    "-headers", headers,
                    "-i", video_url,
                    "-vn",              # 不要视频流
                    "-acodec", "copy",  # 直接复制音频，不重编码
                    "-y",               # 覆盖已有文件
                    str(save_path),
                ],
                capture_output=True,
                timeout=120,
            )
            if result.returncode != 0:
                print(f"    ffmpeg 退出码 {result.returncode}")
            elif audio_file_exists(save_path):
                return True
        except subprocess.TimeoutExpired:
            print(f"    ffmpeg 超时（第 {attempt} 次）")
        except Exception as e:
            print(f"    ffmpeg 失败（第 {attempt} 次）：{e}")

        if save_path.exists():
            save_path.unlink()
        if attempt < retries:
            time.sleep(2 * attempt)

    return False


def parse_detail(detail: dict) -> dict:
    stats = detail.get("statistics", {})
    ts = detail.get("create_time", 0)
    publish_time = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S") if ts else ""

    return {
        "点赞":     stats.get("digg_count", 0),
        "评论":     stats.get("comment_count", 0),
        "转发":     stats.get("share_count", 0),
        "收藏":     stats.get("collect_count", 0),
        "播放":     stats.get("play_count", 0),
        "发布时间": publish_time,
    }


async def fetch_detail(page, video_page_url: str, expected_video_id: str | None = None) -> tuple[str | None, dict]:
    """打开视频页，从 API 响应中拿真实视频 URL + 完整元数据"""
    captured = {}

    async def on_response(resp):
        if "aweme/v1/web/aweme/detail" not in resp.url:
            return

        try:
            data = await resp.json()
        except Exception:
            return

        if data.get("status_code") != 0:
            return

        detail = data.get("aweme_detail", {})
        aweme_id = str(detail.get("aweme_id", "")).strip()

        # 关键校验：确保拦截到的是当前视频详情，避免数据错绑。
        if expected_video_id and aweme_id and aweme_id != expected_video_id:
            return

        if "data" not in captured:
            captured["data"] = data

    page.on("response", on_response)
    try:
        await page.goto(video_page_url, wait_until="domcontentloaded", timeout=20_000)
        for _ in range(20):
            await asyncio.sleep(0.5)
            if "data" in captured:
                break

        # 首次等待未拿到数据，刷新一次再等
        if "data" not in captured:
            await page.reload(wait_until="domcontentloaded", timeout=15_000)
            for _ in range(20):
                await asyncio.sleep(0.5)
                if "data" in captured:
                    break
    except Exception as e:
        print(f"    页面加载出错：{e}")
    finally:
        page.remove_listener("response", on_response)

    if "data" not in captured:
        return None, {}

    detail = captured["data"].get("aweme_detail", {})
    meta   = parse_detail(detail)

    urls = detail.get("video", {}).get("play_addr", {}).get("url_list", [])
    for u in urls:
        if "nwm=1" in u or "ratio=1080p" in u:
            return u, meta
    return (urls[0] if urls else None), meta


async def download_all(records: list[dict]):
    from playwright.async_api import async_playwright

    downloaded = load_downloaded()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
        )
        ctx = await browser.new_context(
            viewport={"width": 1366, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
            locale="zh-CN",
        )
        await ctx.add_init_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
        )
        if COOKIE_FILE.exists():
            cookies = json.loads(COOKIE_FILE.read_text(encoding="utf-8"))
            await ctx.add_cookies(cookies)
            print(f"已加载 Cookie（{len(cookies)} 条）")

        page = await ctx.new_page()
        success, skip, fail = 0, 0, 0
        total    = len(records)
        enriched = []

        for i, row in enumerate(records, 1):
            url = str(row.get("链接", "")).strip()
            if not url or url == "nan":
                enriched.append(row)
                continue

            video_id   = video_id_from_url(url)
            blogger    = str(row.get("博主", "未知博主")).strip()
            title      = str(row.get("标题", video_id)).strip()[:40]
            safe_title = re.sub(r'[\\/:*?"<>|]', "_", title)
            save_path  = AUDIO_DIR / blogger / f"{video_id}.m4a"

            print(f"[{i}/{total}] {safe_title}")
            video_url, meta = await fetch_detail(page, url, expected_video_id=video_id)

            new_row = dict(row)
            for k, v in meta.items():
                if not new_row.get(k):
                    new_row[k] = v
            enriched.append(new_row)

            if meta:
                print(f"    播放 {meta.get('播放',0):,}  点赞 {meta.get('点赞',0):,}  "
                      f"评论 {meta.get('评论',0):,}  发布 {meta.get('发布时间','')}")

            has_audio = audio_file_exists(save_path)
            if video_id in downloaded and not has_audio:
                print("    已下载日志存在但音频缺失，自动改为重下")
                downloaded.discard(video_id)

            if has_audio:
                save_downloaded(video_id, downloaded)
                print("    音频已存在，跳过")
                skip += 1
            elif video_url:
                ok = extract_audio(video_url, save_path)
                if ok:
                    size_kb = save_path.stat().st_size / 1024
                    print(f"    音频提取完成 {size_kb:.0f} KB")
                    save_downloaded(video_id, downloaded)
                    success += 1
                else:
                    if save_path.exists():
                        save_path.unlink()
                    fail += 1
            else:
                print("    Playwright 未获取到视频 URL，改用 yt-dlp…")
                ok = ytdlp_download_audio(url, save_path)
                if ok:
                    size_kb = save_path.stat().st_size / 1024
                    print(f"    yt-dlp 音频完成 {size_kb:.0f} KB")
                    save_downloaded(video_id, downloaded)
                    success += 1
                else:
                    fail += 1

            await asyncio.sleep(random.uniform(1.5, 3.5))
            # 每 10 条额外停顿，降低触发限流的风险
            if i % 10 == 0:
                extra = random.uniform(8, 15)
                print(f"  已处理 {i} 条，暂停 {extra:.0f}s...")
                await asyncio.sleep(extra)

        await browser.close()

    print(f"\n完成：提取 {success} 条，跳过 {skip} 条（已存在），失败 {fail} 条")
    return enriched


def _csv_belongs_to_current_run(csv_files: list[Path], run_id: str) -> bool:
    state = read_current_run()
    if not state or str(state.get("run_id")) != run_id:
        return False

    state_files = {str(Path(p).resolve()) for p in state.get("cleaned_files", [])}
    if not state_files:
        return False

    csv_set = {str(Path(p).resolve()) for p in csv_files}
    return bool(csv_set) and csv_set.issubset(state_files)


def run():
    csv_files = resolve_cleaned_files()
    if not csv_files:
        print("没有找到清洗后的数据，请先运行 清洗数据.py")
        return

    df = pd.concat((pd.read_csv(f, encoding="utf-8-sig") for f in csv_files), ignore_index=True)

    if "链接" not in df.columns:
        print("CSV 中没有「链接」字段")
        return

    records  = df.to_dict("records")
    print(f"共 {len(records)} 条视频待处理")
    enriched = asyncio.run(download_all(records))

    if enriched:
        df_new = pd.DataFrame(enriched)
        for col in ["点赞", "评论", "转发", "收藏", "播放"]:
            if col in df_new.columns:
                df_new[col] = pd.to_numeric(df_new[col], errors="coerce").fillna(0).astype(int)
        if all(c in df_new.columns for c in ["点赞", "评论", "转发", "播放"]):
            df_new["互动率"] = compute_engagement_rate(df_new)

        run_id = current_run_id()
        stamp = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = DATA_DIR / f"cleaned_combined_{stamp}.csv"
        df_new.to_csv(out_path, index=False, encoding="utf-8-sig")

        if run_id and _csv_belongs_to_current_run(csv_files, run_id):
            for f in csv_files:
                f.unlink(missing_ok=True)

        write_current_run(run_id or stamp, [out_path])
        print(f"CSV 已更新（补充详情数据）→ {out_path.name}")


if __name__ == "__main__":
    run()
