"""客户端默认配置与路径常量。"""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_BASE_URL = os.environ.get("EQXIU_AIGC_API_BASE", "https://ai-api.eqxiu.com").rstrip("/")
CONFIG_DIR = Path.home() / ".eqxiu"
CONFIG_PATH = CONFIG_DIR / "config.json"
CONFIG_TOKEN_KEY = "X-Openclaw-Token"
PASSPORT_PROFILE_URL = "https://passport.eqxiu.com/user/profile"

# COS 临时凭证与素材登记（与投票鸭 upload 流程一致，域名对齐易企秀）
EQXIU_COS_TOKEN_API_BASE = str(
    os.environ.get("EQXIU_COS_TOKEN_API_BASE", "https://emw-api.eqxiu.com")
).rstrip("/")
EQXIU_MATERIAL_API_BASE = str(
    os.environ.get("EQXIU_MATERIAL_API_BASE", "https://material-api.eqxiu.com")
).rstrip("/")
EQXIU_UPLOAD_PAGE_ORIGIN = str(
    os.environ.get("EQXIU_UPLOAD_PAGE_ORIGIN", "https://www.eqxiu.com")
).rstrip("/")

ASSET_PUBLIC_BASE = "https://asset.eqh5.com/"
DEFAULT_COS_BUCKET = "eqxiu"
DEFAULT_COS_PREFIX = "/material/"
DEFAULT_MATERIAL_SOURCE = os.environ.get("EQXIU_MATERIAL_SOURCE", "P010245")
DEFAULT_UPLOAD_TIMEOUT = int(os.environ.get("EQXIU_UPLOAD_TIMEOUT", "120"))

BROWSER_CHROME_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
)

# 一键流式生成 H5（/aigc/draw/ai/create/stream）
DEFAULT_PRODUCT_CODE_SUB = os.environ.get("EQXIU_PRODUCT_CODE_SUB", "P010245")
AI_PORTAL_ORIGIN = os.environ.get("EQXIU_AI_PORTAL_ORIGIN", "https://ai.eqxiu.com").rstrip("/")
