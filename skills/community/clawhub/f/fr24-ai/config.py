"""Skill 配置（Skill 搜索 + NewApi 预订）。"""
from __future__ import annotations

import json
import os
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
CACHE_DIR = SKILL_DIR / ".cache"
CLIENT_KEY_FILE = CACHE_DIR / "skill_client.json"
PENDING_PAYLOAD_FILE = CACHE_DIR / "pending_search.json"
BOOKING_CONTEXT_FILE = CACHE_DIR / "booking_context.json"
PASSENGERS_FILE = CACHE_DIR / "passengers.json"
KEYS_FILE = CACHE_DIR / "keys.json"
ENV_FILE = SKILL_DIR / ".env"

CLIENT_KEY_HEADER = "X-Skill-Client-Key"
DAILY_LIMIT = 10

# 项目与 Skill 标识（对外信封、安装目录名）
PROJECT_NAME = "FR24-AI"
SKILL_ID = "fr24-ai"
SKILL_DISPLAY_NAME = "Flightroutes24航路国际机票"
SKILL_AUTHOR = "FR24"

# --- export 网关（项目内固定；切换环境请直接改此处，勿使用 skill.local.env）---
EXPORT_BASE_URL = "https://flight.flightroutes24.com"
GRAY_HEADER = "ww"

SHOPPING_PATH = "/ai/shopping"
NEWAPI_SHOPPING_PATH = "/api/new/shopping"
PRICING_PATH = "/api/new/pricing"
BOOKING_PATH = "/api/new/booking"


# ---------------------------------------------------------------------------
# 多源配置读取：环境变量 > .env 文件 > .cache/keys.json
# ---------------------------------------------------------------------------

_ENV_TO_JSON_KEYS = {
    "FR_NEWAPI_APPKEY": "appkey",
    "FR_NEWAPI_SIGN_SECRET": "signSecret",
    "FR_NEWAPI_AES_SECRET": "aesSecret",
    "FR_NEWAPI_SKIP_AUTH": "skipAuth",
    "FR_NEWAPI_SKIP_IP_WHITELIST": "skipIpWhitelist",
}

_dotenv_cache: dict[str, str] | None = None
_keys_json_cache: dict[str, str] | None = None


def _load_dotenv() -> dict[str, str]:
    """解析 .env 文件（KEY=VALUE，忽略 # 注释和空行）。"""
    global _dotenv_cache
    if _dotenv_cache is not None:
        return _dotenv_cache
    result: dict[str, str] = {}
    if not ENV_FILE.is_file():
        _dotenv_cache = result
        return result
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        result[key.strip()] = value.strip().strip("\"'")
    _dotenv_cache = result
    return result


def _load_keys_json() -> dict[str, str]:
    """读取 .cache/keys.json。"""
    global _keys_json_cache
    if _keys_json_cache is not None:
        return _keys_json_cache
    result: dict[str, str] = {}
    if KEYS_FILE.is_file():
        try:
            data = json.loads(KEYS_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                result = {str(k): str(v) for k, v in data.items()}
        except (json.JSONDecodeError, OSError):
            pass
    _keys_json_cache = result
    return result


def _read_config(env_name: str, default: str = "") -> str:
    """按优先级读取配置：环境变量 > .env 文件 > .cache/keys.json。"""
    # 1. 环境变量（最高优先级）
    val = os.environ.get(env_name, "").strip()
    if val:
        return val
    # 2. .env 文件
    json_key = _ENV_TO_JSON_KEYS.get(env_name, env_name)
    val = _load_dotenv().get(env_name, "").strip()
    if val:
        return val
    # 3. .cache/keys.json
    val = _load_keys_json().get(json_key, "").strip()
    if val:
        return val
    return default


def _read_config_bool(env_name: str) -> bool:
    """读取布尔配置（字符串 '1'/'true'/'yes' 视为 True）。"""
    return _read_config(env_name).lower() in ("1", "true", "yes")


def reload_config() -> None:
    """清除内部缓存，下次读取时重新加载 .env 和 keys.json。"""
    global _dotenv_cache, _keys_json_cache
    _dotenv_cache = None
    _keys_json_cache = None


# NewApi 采购密钥（支持多源读取，勿写入仓库）
NEWAPI_APP_KEY = _read_config("FR_NEWAPI_APPKEY")
NEWAPI_SIGN_SECRET = _read_config("FR_NEWAPI_SIGN_SECRET")
NEWAPI_AES_SECRET = _read_config("FR_NEWAPI_AES_SECRET")
NEWAPI_SKIP_AUTH = _read_config_bool("FR_NEWAPI_SKIP_AUTH")
NEWAPI_SKIP_IP_WHITELIST = _read_config_bool("FR_NEWAPI_SKIP_IP_WHITELIST")
FR24_API_HEADER = "fr24-api"

REGISTER_PORTAL_URL = "https://www.flightroutes24.com/"

USER_BOOKING_USER_MESSAGE = (
    f"当前为演示查价。若要预订，请打开 {REGISTER_PORTAL_URL} 注册并开通 API 采购，"
    f"由管理员在本机配置采购密钥后，再按预订流程提供乘客信息。"
)

USER_BOOKING_AGENT_HINT = (
    "维护者：配置 FR_NEWAPI_APPKEY、FR_NEWAPI_SIGN_SECRET、FR_NEWAPI_AES_SECRET；"
    "联调见 references/setup-maintainer.md（勿展示给用户）。"
)

BOOKING_CONFIG_HINT = USER_BOOKING_AGENT_HINT

SEARCH_ONLY_HINT = "（仅查价）当前未开通采购预订；注册并配置密钥后可继续预订。"

USER_SKILL_QUOTA_EXCEEDED_MESSAGE = (
    f"今日演示查价次数已用完（每日 {DAILY_LIMIT} 次）。"
    f"若要继续查询，请打开 {REGISTER_PORTAL_URL} 注册并开通 API 采购，"
    f"取得采购 APPKEY 后在本机完成密钥配置并重启 Claude Code，"
    f"之后将使用您的采购账号搜索（不受演示日限额）。"
    f"询问「如何配置 appkey」可查看配置步骤。"
)


def is_newapi_configured() -> bool:
    if not NEWAPI_APP_KEY:
        return False
    if NEWAPI_SKIP_AUTH:
        return True
    return bool(NEWAPI_SIGN_SECRET)


def is_booking_ready() -> bool:
    if not is_newapi_configured():
        return False
    return bool(NEWAPI_AES_SECRET)


def booking_required_payload(step: str = "booking") -> dict:
    return {
        "code": "CONFIG_REQUIRED",
        "success": False,
        "step": step,
        "registerPortalUrl": REGISTER_PORTAL_URL,
        "message": USER_BOOKING_USER_MESSAGE,
        "bookingConfigHint": USER_BOOKING_AGENT_HINT,
    }


def booking_config_required_envelope(action: str, step: str = "booking") -> dict:
    """未配置采购密钥时，统一返回注册/申请引导（含 registerPortalUrl）。"""
    data = booking_required_payload(step=step)
    return {
        "skill": SKILL_ID,
        "status": "failure",
        "action": action,
        "data": data,
        "message": data["message"],
    }
