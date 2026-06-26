# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""MBTI NFT 文件管理器 — 管理 ~/.mbti/ 目录下的所有文件状态。"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# 对话量门槛（与 conversation_manager.py 保持一致）
_MIN_TOTAL_TURNS = 50
_MIN_OPEN_TURNS = 10


def get_mbti_dir(mbti_dir: str | None = None) -> Path:
    """获取 .mbti 目录路径，默认为 ~/.mbti/"""
    if mbti_dir:
        return Path(mbti_dir).expanduser().resolve()
    return Path.home() / ".mbti"


def ensure_dirs(mbti_dir: Path) -> None:
    """确保必要的目录结构存在。"""
    mbti_dir.mkdir(parents=True, exist_ok=True)
    (mbti_dir / "wallet").mkdir(exist_ok=True)


def _get_conversation_stats(mbti_dir: Path) -> dict[str, Any]:
    """统计会话摘要数据。"""
    conversations_dir = mbti_dir / "conversations"
    if not conversations_dir.exists():
        return {
            "session_count": 0,
            "total_turns": 0,
            "open_turns": 0,
            "ready_for_analysis": False,
        }

    total_turns = 0
    open_turns = 0
    session_count = 0

    for f in conversations_dir.glob("session-*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            turns = data.get("turns", {})
            total_turns += turns.get("total", 0)
            open_turns += turns.get("open", 0)
            session_count += 1
        except (json.JSONDecodeError, OSError):
            continue

    return {
        "session_count": session_count,
        "total_turns": total_turns,
        "open_turns": open_turns,
        "ready_for_analysis": total_turns >= _MIN_TOTAL_TURNS and open_turns >= _MIN_OPEN_TURNS,
    }


def cmd_check(args: argparse.Namespace) -> None:
    """检查 ~/.mbti/ 目录状态，返回 JSON。"""
    mbti_dir = get_mbti_dir(args.mbti_dir)

    has_mbti = (mbti_dir / "mbti-latest.json").exists()
    has_wallet = (mbti_dir / "wallet" / "address").exists()

    nft_status = "none"
    nft_status_file = mbti_dir / "nft-status.json"
    if nft_status_file.exists():
        data = json.loads(nft_status_file.read_text(encoding="utf-8"))
        nft_status = data.get("status", "none")

    result: dict[str, Any] = {
        "mbti_dir": str(mbti_dir),
        "has_mbti": has_mbti,
        "has_wallet": has_wallet,
        "nft_status": nft_status,
        "conversation_stats": _get_conversation_stats(mbti_dir),
    }
    print(json.dumps(result, indent=2))


def cmd_read_mbti(args: argparse.Namespace) -> None:
    """读取 mbti-latest.json。"""
    mbti_dir = get_mbti_dir(args.mbti_dir)
    latest = mbti_dir / "mbti-latest.json"

    if not latest.exists():
        print(json.dumps({"error": "mbti-latest.json not found"}), file=sys.stderr)
        sys.exit(1)

    data = json.loads(latest.read_text(encoding="utf-8"))
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_write_mbti(args: argparse.Namespace) -> None:
    """写入新的 MBTI 结果，自动归档旧文件。"""
    mbti_dir = get_mbti_dir(args.mbti_dir)
    ensure_dirs(mbti_dir)

    latest = mbti_dir / "mbti-latest.json"

    # 归档旧文件
    if latest.exists():
        old_data = json.loads(latest.read_text(encoding="utf-8"))
        detected_at = old_data.get("detected_at", "")
        if detected_at:
            try:
                dt = datetime.fromisoformat(detected_at.replace("Z", "+00:00"))
                archive_name = f"mbti-{dt.strftime('%Y%m%d-%H%M')}.json"
            except ValueError:
                archive_name = f"mbti-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M')}.json"
        else:
            archive_name = f"mbti-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M')}.json"

        archive_path = mbti_dir / archive_name
        shutil.copy2(latest, archive_path)

    # 写入新结果
    mbti_data: dict[str, Any] = json.loads(args.data)
    if "detected_at" not in mbti_data:
        mbti_data["detected_at"] = datetime.now(timezone.utc).isoformat()

    latest.write_text(json.dumps(mbti_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"status": "ok", "path": str(latest)}, indent=2))


def cmd_read_nft_status(args: argparse.Namespace) -> None:
    """读取 nft-status.json。"""
    mbti_dir = get_mbti_dir(args.mbti_dir)
    nft_file = mbti_dir / "nft-status.json"

    if not nft_file.exists():
        print(json.dumps({"status": "none"}))
        return

    data = json.loads(nft_file.read_text(encoding="utf-8"))
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_write_nft_status(args: argparse.Namespace) -> None:
    """更新 nft-status.json。"""
    mbti_dir = get_mbti_dir(args.mbti_dir)
    ensure_dirs(mbti_dir)

    nft_file = mbti_dir / "nft-status.json"
    nft_data: dict[str, Any] = json.loads(args.data)
    nft_file.write_text(json.dumps(nft_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"status": "ok", "path": str(nft_file)}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="MBTI NFT 文件管理器")
    parser.add_argument("--mbti-dir", type=str, default=None, help="~/.mbti/ 目录路径，默认为 ~/.mbti")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("check", help="检查目录状态")
    subparsers.add_parser("read-mbti", help="读取最新 MBTI 结果")

    write_mbti = subparsers.add_parser("write-mbti", help="写入 MBTI 结果")
    write_mbti.add_argument("--data", required=True, help="MBTI 结果 JSON 字符串")

    subparsers.add_parser("read-nft-status", help="读取 NFT Mint 状态")

    write_nft = subparsers.add_parser("write-nft-status", help="更新 NFT Mint 状态")
    write_nft.add_argument("--data", required=True, help="NFT 状态 JSON 字符串")

    args = parser.parse_args()

    commands: dict[str, Any] = {
        "check": cmd_check,
        "read-mbti": cmd_read_mbti,
        "write-mbti": cmd_write_mbti,
        "read-nft-status": cmd_read_nft_status,
        "write-nft-status": cmd_write_nft_status,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
