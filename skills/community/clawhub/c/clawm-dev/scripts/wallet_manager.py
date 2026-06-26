# /// script
# requires-python = ">=3.10"
# dependencies = ["solders>=0.21.0", "base58>=2.1.0"]
# ///
"""Solana 钱包管理器 — 生成和管理 ~/.mbti/wallet/ 下的钱包文件。"""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any


def get_wallet_dir(mbti_dir: str | None = None) -> Path:
    """获取钱包目录路径。"""
    if mbti_dir:
        base = Path(mbti_dir).expanduser().resolve()
    else:
        base = Path.home() / ".mbti"
    return base / "wallet"


def cmd_check(args: argparse.Namespace) -> None:
    """检查钱包是否存在，返回地址（不返回私钥）。"""
    wallet_dir = get_wallet_dir(args.mbti_dir)
    address_file = wallet_dir / "address"

    if not address_file.exists():
        print(json.dumps({"exists": False}))
        return

    address = address_file.read_text(encoding="utf-8").strip()
    print(json.dumps({"exists": True, "address": address}, indent=2))


def cmd_generate(args: argparse.Namespace) -> None:
    """生成新的 Solana 钱包。"""
    wallet_dir = get_wallet_dir(args.mbti_dir)
    address_file = wallet_dir / "address"
    key_file = wallet_dir / "private_key"

    if address_file.exists() and not args.force:
        address = address_file.read_text(encoding="utf-8").strip()
        print(
            json.dumps(
                {"error": "wallet already exists", "address": address},
                indent=2,
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    # 延迟导入，仅在需要时加载
    import base58  # type: ignore[import-untyped]
    from solders.keypair import Keypair  # type: ignore[import-untyped]

    keypair = Keypair()
    address: str = str(keypair.pubkey())
    private_key: str = base58.b58encode(bytes(keypair)).decode("ascii")

    # 确保目录存在
    wallet_dir.mkdir(parents=True, exist_ok=True)

    # 写入私钥（600 权限）
    key_file.write_text(private_key, encoding="utf-8")
    os.chmod(key_file, stat.S_IRUSR | stat.S_IWUSR)  # 600

    # 写入地址（只读）
    address_file.write_text(address, encoding="utf-8")
    os.chmod(address_file, stat.S_IRUSR | stat.S_IWUSR)  # 600

    result: dict[str, Any] = {
        "status": "ok",
        "address": address,
        "key_file": str(key_file),
        "address_file": str(address_file),
        "warning": "请妥善保管，私钥丢失无法恢复！",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_get_address(args: argparse.Namespace) -> None:
    """读取钱包地址。"""
    wallet_dir = get_wallet_dir(args.mbti_dir)
    address_file = wallet_dir / "address"

    if not address_file.exists():
        print(json.dumps({"error": "wallet not found"}), file=sys.stderr)
        sys.exit(1)

    address = address_file.read_text(encoding="utf-8").strip()
    print(json.dumps({"address": address}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Solana 钱包管理器")
    parser.add_argument("--mbti-dir", type=str, default=None, help="~/.mbti/ 目录路径")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("check", help="检查钱包是否存在")

    gen_parser = subparsers.add_parser("generate", help="生成新钱包")
    gen_parser.add_argument("--force", action="store_true", help="强制覆盖已有钱包")

    subparsers.add_parser("get-address", help="获取钱包地址")

    args = parser.parse_args()

    commands: dict[str, Any] = {
        "check": cmd_check,
        "generate": cmd_generate,
        "get-address": cmd_get_address,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
