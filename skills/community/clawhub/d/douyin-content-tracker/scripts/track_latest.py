"""
track_latest.py — 全自动追踪博主最新 N 条视频流程

流程：
  1. 读取账号列表
  2. 采集每位博主最新 N 条视频（自动模式，无需手动干预，需 Cookie 有效）
  3. 清洗数据
  4. 提取音频（ffmpeg 只取音频流，保存为 .m4a）
  5. Whisper 语音识别

用法：
    python scripts/track_latest.py                 # 默认追踪最新 3 条（首次运行会自动提升到 10 条）
    python scripts/track_latest.py --limit 5       # 追踪最新 5 条
    python scripts/track_latest.py --no-audio      # 跳过音频提取和语音识别
    python scripts/track_latest.py --accounts-file /path/to/accounts.txt

账号列表文件格式：
    博主名 | https://www.douyin.com/user/xxx
    （每行一个，# 开头为注释，空行忽略）
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
load_dotenv(ROOT_DIR / ".env")
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from clean_data import clean_csv
from download_video import download_all
from extract_subtitle import load_title_map, process_video, write_blogger_summaries
from run_state import current_run_id, write_current_run
from scrape_profile import DEFAULT_URL, scrape
from storage import AUDIO_DIR, DATA_DIR, SUBTITLE_DIR
from utils import compute_engagement_rate

DEFAULT_ACCOUNT_FILE = ROOT_DIR / "accounts.txt"
ENV_ACCOUNT_FILE = os.getenv("TRACKER_ACCOUNTS_FILE") or os.getenv("ACCOUNTS_FILE")


# ── 账号列表 ──────────────────────────────────────────────────
def resolve_accounts_file(cli_path: Path | None) -> tuple[Path, bool]:
    if cli_path is not None:
        return cli_path.expanduser(), True
    if ENV_ACCOUNT_FILE:
        return Path(ENV_ACCOUNT_FILE).expanduser(), True
    return DEFAULT_ACCOUNT_FILE, False


def load_accounts(accounts_file: Path | None) -> tuple[list[tuple[str, str]], Path]:
    path, is_override = resolve_accounts_file(accounts_file)

    if not path.exists() and is_override:
        print(f"指定账号文件 {path} 不存在，自动回退到默认 accounts.txt")
        path = DEFAULT_ACCOUNT_FILE
        is_override = False

    if not path.exists():
        print("账号列表文件不存在，使用内置默认博主")
        return [("默认博主", DEFAULT_URL)], path

    accounts: list[tuple[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            name, url = line.split("|", 1)
            accounts.append((name.strip(), url.strip()))
        elif line.startswith("http"):
            accounts.append(("博主", line))

    if not accounts:
        print(f"{path} 为空，使用内置默认博主")
        return [("默认博主", DEFAULT_URL)], path

    return accounts, path


# ── 步骤执行封装 ──────────────────────────────────────────────
def section(title: str):
    print("\n" + "=" * 55)
    print(f"  {title}")
    print("=" * 55)


def run_pipeline(limit: int, skip_audio: bool, accounts_file: Path | None = None):
    run_id = current_run_id() or datetime.now().strftime("%Y%m%d_%H%M%S")
    os.environ["RUN_ID"] = run_id
    print(f"RUN_ID: {run_id}")

    has_history = any(DATA_DIR.glob("cleaned_*.csv"))
    effective_limit = limit if has_history else 10
    if not has_history:
        print("检测到首次运行，默认采集最近 10 条")
    else:
        print(f"历史已存在，按最新 {effective_limit} 条采集")

    accounts, accounts_path = load_accounts(accounts_file)
    print(
        f"\n账号文件：{accounts_path}\n共 {len(accounts)} 个账号，每个追踪最新 {effective_limit} 条视频\n"
    )

    all_csv_paths = []

    # ── Step 1: 采集 + 清洗 ──────────────────────────────────
    for name, url in accounts:
        section(f"采集：{name}")
        csv_path = asyncio.run(
            scrape(url, scroll_count=2, headless=True, auto=True, limit=effective_limit)
        )
        if not csv_path:
            print(f"  采集失败，跳过 {name}")
            continue

        print(f"  原始 CSV → {Path(csv_path).name}")
        try:
            cleaned = clean_csv(Path(csv_path))
        except ValueError as e:
            print(f"  清洗失败，跳过 {name}：{e}")
            continue
        if cleaned is not None and not cleaned.empty:
            cleaned_path = Path(csv_path).parent / f"cleaned_{Path(csv_path).stem}.csv"
            all_csv_paths.append(cleaned_path)
            print(f"  清洗完成：{len(cleaned)} 条")

    if not all_csv_paths:
        print("\n未采集到任何数据，流程终止")
        return

    write_current_run(run_id, all_csv_paths)

    # ── Step 2: 提取音频 + 语音识别 ─────────────────────────
    if not skip_audio:
        import pandas as pd

        section("提取音频")
        dfs = [pd.read_csv(p, encoding="utf-8-sig") for p in all_csv_paths if p.exists()]
        if dfs:
            df_all = pd.concat(dfs, ignore_index=True)
            records = df_all.to_dict("records")
            print(f"共 {len(records)} 条视频待处理")
            enriched = asyncio.run(download_all(records))

            if enriched:
                df_new = pd.DataFrame(enriched)
                for col in ["点赞", "评论", "转发", "收藏", "播放"]:
                    if col in df_new.columns:
                        df_new[col] = pd.to_numeric(df_new[col], errors="coerce").fillna(0).astype(int)
                if all(c in df_new.columns for c in ["点赞", "评论", "转发", "播放"]):
                    df_new["互动率"] = compute_engagement_rate(df_new)

                combined_path = DATA_DIR / f"cleaned_combined_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df_new.to_csv(combined_path, index=False, encoding="utf-8-sig")
                for p in all_csv_paths:
                    if p.exists():
                        p.unlink()
                write_current_run(run_id, [combined_path])
                print(f"CSV 已更新（补充详情数据）→ {combined_path.name}")

        section("Whisper 语音识别")
        SUBTITLE_DIR.mkdir(exist_ok=True)
        audio_files = list(AUDIO_DIR.rglob("*.m4a"))
        if audio_files:
            from collections import defaultdict
            print(f"共 {len(audio_files)} 个音频")
            title_map = load_title_map()
            summary_index = defaultdict(list)
            for af in audio_files:
                process_video(af, title_map, summary_index)
            write_blogger_summaries(summary_index)
        else:
            print("音频库为空，跳过语音识别")
    else:
        print("\n已跳过音频提取和语音识别（--no-audio）")

    print("\n" + "=" * 55)
    print("全部完成！请查看 字幕文本/ 与 采集数据/ 目录")
    print("=" * 55)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="自动追踪博主最新视频流程")
    parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="每位博主追踪最新 N 条（默认 3；首次自动提升到 10 条）",
    )
    parser.add_argument(
        "--no-audio",
        action="store_true",
        help="跳过音频提取和语音识别",
    )
    parser.add_argument(
        "--accounts-file",
        type=Path,
        help="自定义账号列表路径（亦可设置 TRACKER_ACCOUNTS_FILE 环境变量）",
    )
    return parser


def parse_args(argv: list[str] | None = None):
    return build_arg_parser().parse_args(argv)


# ── 入口 ─────────────────────────────────────────────────────
if __name__ == "__main__":
    args = parse_args()
    run_pipeline(limit=args.limit, skip_audio=args.no_audio, accounts_file=args.accounts_file)
