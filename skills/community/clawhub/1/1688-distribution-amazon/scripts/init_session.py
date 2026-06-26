"""初始化 Amazon 铺货 session 目录。"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scripts.common import DEFAULT_MARKETPLACE_ID, SESSIONS_BASE, write_session
from scripts.query_user_info import get_user_info


def _slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip().lower()).strip("-")
    return slug or "store"


def create_session(
    offer_id: int | str,
    encrypted_code: str,
    store_name: str,
    marketplace_id: str = DEFAULT_MARKETPLACE_ID,
    base_dir: str = SESSIONS_BASE,
) -> str:
    now = datetime.now()
    ts = now.strftime("%Y%m%d_%H%M%S") + f"{now.microsecond // 1000:03d}"
    name = f"{offer_id}-amazon-{_slug(store_name)}-{marketplace_id}-{ts}"
    session_dir = os.path.join(base_dir, name)
    os.makedirs(session_dir, mode=0o700, exist_ok=True)
    os.chmod(session_dir, 0o700)

    input_data = {
        "session_dir": session_dir,
        "offer_id": int(offer_id),
        "platform": "amazon",
        "marketplace_id": marketplace_id,
        "encrypted_code": encrypted_code,
        "store_name": store_name,
    }
    user_info = {"encryptedCode": encrypted_code, "storeName": store_name}
    write_session(session_dir, "input.json", input_data)
    write_session(session_dir, "query_user_info.json", user_info)

    print(f"[OK] 会话目录已创建: {session_dir}", file=sys.stderr)
    return session_dir


def resolve_encrypted_code(encrypted_code: str | None, store_name: str) -> str:
    if encrypted_code:
        return encrypted_code
    user_info = get_user_info(store_name=store_name)
    resolved = user_info.get("encryptedCode")
    if not resolved:
        raise RuntimeError(f"未能解析 Amazon 店铺 {store_name} 的 encryptedCode")
    return resolved


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="初始化 Amazon 铺货 session 目录")
    parser.add_argument("offer_id", type=int, help="1688 商品 offerId")
    parser.add_argument("--encrypted-code", required=False, help="内部兼容参数；不要在用户可见回复中展示")
    parser.add_argument("--store-name", required=True, help="目标 Amazon 店铺名称")
    parser.add_argument("--marketplace-id", default=DEFAULT_MARKETPLACE_ID, help="Amazon marketplaceId")
    args = parser.parse_args()

    encrypted_code = resolve_encrypted_code(args.encrypted_code, args.store_name)
    print(create_session(args.offer_id, encrypted_code, args.store_name, args.marketplace_id))
