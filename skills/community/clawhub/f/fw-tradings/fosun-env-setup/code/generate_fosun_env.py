#!/usr/bin/env python3
"""Generate a ready-to-use fosun.env from configurable variables only.

使用方式（不走 args 参数）：
1) 直接修改下方“用户可编辑配置区”的变量值。
2) 运行：
   python3 fw-trade-skill/fosun-env-setup/code/generate_fosun_env.py

注意：
- PRIVATE_KEY_PEM / PRIVATE_KEY_FILE 二选一（必须且只能选一个）。
- PUBLIC_KEY_PEM / PUBLIC_KEY_FILE 二选一（必须且只能选一个）。
- FSOPENAPI_API_KEY_VERIFIED_AT 为空字符串时，会自动写入当前创建时间戳。
"""

from __future__ import annotations

import base64
from datetime import datetime
from pathlib import Path

# ========================= 用户可编辑配置区（按需修改） =========================
# 必填：API Key（必须以 ak_ 开头）
API_KEY = "ak_replace_me"

# 私钥输入：二选一
PRIVATE_KEY_FILE = ""  # 例如: "/absolute/path/client_private.pem"
PRIVATE_KEY_PEM = ""   # 直接粘贴 PEM 全文（BEGIN/END PRIVATE KEY）

# 公钥输入：二选一
PUBLIC_KEY_FILE = ""   # 例如: "/absolute/path/server_public.pem"
PUBLIC_KEY_PEM = ""    # 直接粘贴 PEM 全文（BEGIN/END PUBLIC KEY）

# 输出文件配置
OUTPUT_FILE = "fw-trade-skill/fosun.env"
OVERWRITE = True

# fosun.env 固定字段配置
FSOPENAPI_BASE_URL = "https://openapi.fosunxcz.com"
FSOPENAPI_API_KEY_STATUS = "valid"
# 为空则自动使用当前创建时间戳（推荐）
FSOPENAPI_API_KEY_VERIFIED_AT = ""
# ==========================================================================


def _read_text(path: str) -> str:
    return Path(path).expanduser().read_text(encoding="utf-8").strip()


def _pick_material(inline_value: str, file_value: str, field_name: str) -> str:
    """Read value from inline arg or file arg (exactly one source required)."""
    has_inline = bool((inline_value or "").strip())
    has_file = bool((file_value or "").strip())
    if has_inline == has_file:
        raise ValueError(f"{field_name} 需要且只能提供一种输入方式：inline 或 file。")
    if has_inline:
        return str(inline_value).strip()
    return _read_text(str(file_value).strip())


def _normalize_pem(pem_text: str, begin_tag: str, end_tag: str, field_name: str) -> str:
    """Normalize PEM line endings and verify wrapper lines."""
    normalized = pem_text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if begin_tag not in normalized or end_tag not in normalized:
        raise ValueError(f"{field_name} 不是合法 PEM 文本，缺少 {begin_tag}/{end_tag}。")
    return normalized


def _to_base64_single_line(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def _build_env_content(
    api_key: str,
    private_key_pem: str,
    public_key_pem: str,
    base_url: str,
    status: str,
    verified_at: str,
) -> str:
    private_key_b64 = _to_base64_single_line(private_key_pem)
    public_key_b64 = _to_base64_single_line(public_key_pem)
    lines = [
        f"FSOPENAPI_API_KEY={api_key}",
        f"FSOPENAPI_API_KEY_STATUS={status}",
        f"FSOPENAPI_API_KEY_VERIFIED_AT={verified_at}",
        f"FSOPENAPI_BASE_URL={base_url}",
        f"FSOPENAPI_CLIENT_PRIVATE_KEY={private_key_b64}",
        f"FSOPENAPI_SERVER_PUBLIC_KEY={public_key_b64}",
    ]
    return "\n".join(lines) + "\n"


def _resolved_verified_at(raw_verified_at: str) -> str:
    """Return user value, or auto-fill with current timestamp."""
    value = str(raw_verified_at or "").strip()
    if value:
        return value
    return str(int(datetime.now().timestamp()))


def main() -> None:
    api_key = str(API_KEY).strip()
    if not api_key.startswith("ak_"):
        raise ValueError("api-key 格式不正确，必须以 'ak_' 开头。")

    private_key_raw = _pick_material(PRIVATE_KEY_PEM, PRIVATE_KEY_FILE, "private key")
    public_key_raw = _pick_material(PUBLIC_KEY_PEM, PUBLIC_KEY_FILE, "public key")

    private_key_pem = _normalize_pem(
        private_key_raw,
        "-----BEGIN PRIVATE KEY-----",
        "-----END PRIVATE KEY-----",
        "private key",
    )
    public_key_pem = _normalize_pem(
        public_key_raw,
        "-----BEGIN PUBLIC KEY-----",
        "-----END PUBLIC KEY-----",
        "public key",
    )

    output_path = Path(str(OUTPUT_FILE).strip()).expanduser()
    if output_path.exists() and not OVERWRITE:
        raise FileExistsError(f"输出文件已存在：{output_path}。如需覆盖请将 OVERWRITE=True。")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = _build_env_content(
        api_key=api_key,
        private_key_pem=private_key_pem,
        public_key_pem=public_key_pem,
        base_url=str(FSOPENAPI_BASE_URL).strip(),
        status=str(FSOPENAPI_API_KEY_STATUS).strip(),
        verified_at=_resolved_verified_at(FSOPENAPI_API_KEY_VERIFIED_AT),
    )
    output_path.write_text(content, encoding="utf-8")
    print(f"已生成: {output_path.resolve()}")
    print("该文件已包含 FSOPENAPI_API_KEY_STATUS / FSOPENAPI_API_KEY_VERIFIED_AT / FSOPENAPI_BASE_URL。")
    print("后续只需替换脚本顶部变量中的 PRIVATE KEY / PUBLIC KEY / api-key，再次执行即可。")


if __name__ == "__main__":
    main()
