"""
全局配置 — 支持 ClawHub 设置 + 4种配置方式（优先级从高到低）

  1. ClawHub skills.entries.ghdata_analyze.config  ← 技能设置面板
  2. settings.json 文件（技能根目录）
  3. 环境变量               ← GHDATA_API_URL / GHDATA_TIMEOUT
  4. 默认值                 ← http://api.topeasychina.com:15099/api / 30秒

APIKey存放位置：~/.ghdata/ghdataapikey
  - 首次使用自动生成随机GUID并保存到此文件
  - 付费后替换文件内容为购买到的密钥
  - ~ 为用户主目录（Windows下为 C:\\Users\\<用户名>）
"""
import os
import json
import uuid

# ===== 默认参数（兜底）=====
WEBAPI_BASE_URL: str = "http://api.topeasychina.com:15099/api"
TIMEOUT: int = 30
API_KEY: str = ""
DOC_DIR: str = ""
DATA_DIR: str = ""
_initialized = False
_CONFIG_FILE = ""  # settings.json 的路径

# ===== 路径计算 =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ===== APIKey文件路径 =====
_GH_DATA_DIR = os.path.join(os.path.expanduser("~"), ".ghdata")
_APIKEY_FILE = os.path.join(_GH_DATA_DIR, "ghdataapikey")

# ===== 预测参数 =====
BASE_SCORE = 5.0
RANGE_MAP = {
    "偏多": "+1.5%~+3.0%",
    "震荡偏多": "0%~+2.0%",
    "震荡": "-1.0%~+1.0%",
    "震荡偏空": "-2.0%~0%",
    "偏空": "-3.0%~-1.0%",
}
START_DATE = "2025-01-01"
FETCH_DAYS = 700


def _load_settings() -> dict:
    """
    读取 settings.json 配置文件
    搜索顺序：ghdataskill根目录 > 当前工作目录
    """
    candidates = [
        os.path.join(BASE_DIR, "settings.json"),
        os.path.join(os.getcwd(), "settings.json"),
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                global _CONFIG_FILE
                _CONFIG_FILE = path
                # 过滤掉中文说明key
                result = {}
                for k, v in data.items():
                    if not k.startswith("说明") and not k.startswith("备注") and not k.startswith("修改"):
                        result[k] = v
                return result
            except Exception as e:
                print(f"[config] 读取配置文件失败 {path}: {e}")
    return {}


def _read_apikey_file() -> str:
    """从 ~/.ghdata/ghdataapikey 读取APIKey"""
    if not os.path.exists(_APIKEY_FILE):
        return ""
    try:
        with open(_APIKEY_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        print(f"[config] 读取APIKey文件失败 {_APIKEY_FILE}: {e}")
        return ""


def _write_apikey_file(key: str) -> bool:
    """保存APIKey到 ~/.ghdata/ghdataapikey"""
    try:
        os.makedirs(_GH_DATA_DIR, exist_ok=True)
        with open(_APIKEY_FILE, "w", encoding="utf-8") as f:
            f.write(key.strip())
        return True
    except Exception as e:
        print(f"[config] 保存APIKey文件失败 {_APIKEY_FILE}: {e}")
        return False


def _ensure_api_key() -> str:
    """
    确保有有效的APIKey
    优先级：~/.ghdata/ghdataapikey > 自动生成
    """
    # 1. 从文件读取
    existing = _read_apikey_file()
    if existing and len(existing) > 20:
        return existing

    # 2. 自动生成GUID并保存
    new_key = str(uuid.uuid4()).upper()
    _write_apikey_file(new_key)
    print(f"[config] 首次使用，自动生成APIKey → {_APIKEY_FILE}")
    return new_key


def init(webapi_url: str = None, timeout: int = None, api_key: str = None):
    """
    初始化配置 — 4层优先级（高→低）：

    1. init() 传参 webapi_url/timeout/api_key
    2. settings.json 文件（ghdataskill/ 目录下）
    3. 环境变量 GHDATA_API_URL / GHDATA_TIMEOUT / GHDATA_API_KEY
    4. 默认值

    参数:
        webapi_url: WebAPI 基地址
        timeout: 请求超时秒数
        api_key: APIKey验证密钥（付费版本必填）

    示例:
        >>> config.init()                                                    # 从settings.json或默认
        >>> config.init("http://192.168.1.100:5099/api")                    # 代码覆盖
        >>> config.init(api_key="00000000-0000-0000-0000-000000000000")     # 指定APIKey
    """
    global WEBAPI_BASE_URL, TIMEOUT, DOC_DIR, DATA_DIR, API_KEY, _initialized

    # 第1层：settings.json 文件
    settings = _load_settings()
    file_url = settings.get("webapi_url", "")
    file_timeout = settings.get("webapi_timeout", 0)

    # 第2层：环境变量
    env_url = os.environ.get("GHDATA_API_URL", "")
    env_timeout = os.environ.get("GHDATA_TIMEOUT", "")
    env_api_key = os.environ.get("GHDATA_API_KEY", "")

    # 第3层：文件（~/.ghdata/ghdataapikey）
    file_api_key = _read_apikey_file()

    # 第4层：传参覆盖前几层
    final_url = webapi_url or file_url or env_url or "http://api.topeasychina.com:15099/api"
    final_timeout = (timeout or 
                     (int(file_timeout) if file_timeout else 0) or 
                     (int(env_timeout) if env_timeout else 30))
    final_api_key = api_key or env_api_key or file_api_key or ""

    WEBAPI_BASE_URL = final_url.rstrip("/")
    TIMEOUT = final_timeout

    # 输出目录
    global DOC_DIR, DATA_DIR
    DOC_DIR = os.path.join(BASE_DIR, "doc")
    DATA_DIR = os.path.join(BASE_DIR, "data")
    os.makedirs(DOC_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    # APIKey：传参 > 环境变量 > 本地文件 > 自动生成
    if not final_api_key:
        final_api_key = _ensure_api_key()
    API_KEY = final_api_key

    # 如果APIKey来自传参/环境变量（非文件），同步保存到文件
    if api_key or env_api_key:
        _write_apikey_file(final_api_key)

    _initialized = True

    # 打印配置来源
    sources = []
    if webapi_url or api_key:
        sources.append("init传参")
    if _CONFIG_FILE:
        sources.append(os.path.basename(_CONFIG_FILE))
    elif os.environ.get("GHDATA_API_URL"):
        sources.append("环境变量")
    source_str = f" ({' + '.join(sources)})" if sources else ""
    masked_key = API_KEY[:8] + "****" + API_KEY[-4:] if len(API_KEY) > 20 else "（未设置）"
    print(f"[config] WebAPI: {WEBAPI_BASE_URL}  timeout={TIMEOUT}s  APIKey: {masked_key}{source_str}")
    print(f"[config] DOC: {DOC_DIR}")


def reload():
    """重新加载配置（重新读取settings.json和环境变量）"""
    init()


def show():
    """打印当前完整配置信息"""
    global API_KEY
    masked = API_KEY[:8] + "****" + API_KEY[-4:] if len(API_KEY) > 20 else "（未设置）"
    print("=" * 50)
    print("  股海罗盘 当前配置")
    print("=" * 50)
    print(f"  WebAPI URL:    {WEBAPI_BASE_URL}")
    print(f"  Timeout:       {TIMEOUT}s")
    print(f"  APIKey:        {masked}")
    print(f"  APIKey文件:    {_APIKEY_FILE}")
    print(f"  输出目录:      {DOC_DIR}")
    print(f"  数据目录:      {DATA_DIR}")
    print(f"  配置来源:      {_CONFIG_FILE or '默认值'}")

    print(f"\n  📋 修改方式（优先级从高到低）：")
    print(f"  ① init() 传参  → 临时覆盖")
    print(f"  ② settings.json → 改url/timeout，永久生效 ✅ 推荐")
    print(f"  ③ 环境变量      → set GHDATA_API_URL=...")
    print(f"  ④ 默认值        → http://api.topeasychina.com:15099/api")
    print("=" * 50)
