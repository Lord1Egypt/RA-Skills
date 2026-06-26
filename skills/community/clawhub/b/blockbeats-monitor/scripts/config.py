# 本文件集中管理 TOML 配置、默认路径、律动 API 地址和端点配置。

from pathlib import Path
try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None
from zoneinfo import ZoneInfo


BASE_URL = "https://api-pro.theblockbeats.info"

# 律动 API 端点集中定义，方便后续替换或扩展。
ENDPOINTS = {
    "newsflash_24h": "/v1/newsflash/24h",
    "article_24h": "/v1/article/24h",
    "newsflash_important": "/v1/newsflash/important",
    "article_important": "/v1/article/important",
}

DEFAULT_LANG = "cn"
DEFAULT_TIMEZONE = "Asia/Shanghai"
DEFAULT_DB_PATH = Path("data") / "blockbeats_monitor.sqlite"
DEFAULT_CONFIG_PATH = Path("config.toml")


CONFIG = {}


def _parse_scalar(value):
    """在 Python 3.9 无 tomllib 时，解析本项目需要的简单字符串配置。"""
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value


def _fallback_load_toml(path):
    """轻量 TOML 解析器，仅支持本配置文件使用的 section 和 key=value 字符串。"""
    result = {}
    section = None
    for raw_line in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            result.setdefault(section, {})
            continue
        if "=" in line and section:
            key, value = line.split("=", 1)
            result[section][key.strip()] = _parse_scalar(value)
    return result


def load_config(config_path=None):
    """加载 TOML 配置；默认读取 ./config.toml。"""
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    if not path.exists():
        return {}
    if tomllib:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    return _fallback_load_toml(path)


def set_config(config):
    """CLI 启动时设置全局配置，供各命令统一读取。"""
    global CONFIG
    CONFIG = config or {}


def get_config_value(section, key, default=None):
    section_data = CONFIG.get(section, {})
    if not isinstance(section_data, dict):
        return default
    return section_data.get(key, default)


def get_required_config(section, key):
    """读取必需 TOML 配置，缺失时抛出清晰错误。"""
    value = get_config_value(section, key)
    if not value:
        raise RuntimeError("缺少必需配置：config.toml [%s].%s" % (section, key))
    return value


def get_blockbeats_api_key():
    return get_required_config("blockbeats", "api_key")


def get_telegram_config():
    return (
        get_required_config("telegram", "bot_token"),
        get_required_config("telegram", "chat_id"),
    )


def get_db_path(cli_path=None):
    """按 CLI 参数、TOML、默认值的优先级确定 SQLite 路径。"""
    if cli_path:
        return Path(cli_path)
    return Path(get_config_value("storage", "db_path", str(DEFAULT_DB_PATH)))


def get_lang():
    return get_config_value("blockbeats", "lang", DEFAULT_LANG)


def get_timezone():
    return ZoneInfo(get_config_value("report", "timezone", DEFAULT_TIMEZONE))
