"""
全局配置

APIKey 仅从 ~/.ghdata/ghdataapikey 读取（不读 settings.json 或环境变量）
删除该文件 → 自动生成随机GUID → 服务端验证失败 → 降级为免费预览

URL/超时 支持 3 种来源（优先级从高到低）：
  1. init() 传参
  2. settings.json（ghdataskill/ 目录下）
  3. 环境变量 GHDATA_API_URL / GHDATA_TIMEOUT
  4. 默认值 http://api.topeasychina.com:15099/api / 30秒
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

# ===== 分析参数 =====
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
    初始化配置 — APIKey仅从 ~/.ghdata/ghdataapikey 读取
    删除该文件后自动生成随机GUID（服务端验证失败→降级为免费预览）

    参数:
        webapi_url: WebAPI 基地址
        timeout: 请求超时秒数
        api_key: APIKey（传入则覆盖文件内容）

    示例:
        >>> config.init()                                          # 从 ~/.ghdata/ghdataapikey 读取
        >>> config.init("http://192.168.1.100:5099/api")          # 代码覆盖URL
        >>> config.init(api_key="<在此填入你的APIKey>")  # 指定APIKey（示例，用真实Key替换）
    """
    global WEBAPI_BASE_URL, TIMEOUT, DOC_DIR, DATA_DIR, API_KEY, _initialized

    # URL/超时来源：settings.json > 环境变量 > 默认
    settings = _load_settings()
    file_url = settings.get("webapi_url", "")
    file_timeout = settings.get("webapi_timeout", 0)
    env_url = os.environ.get("GHDATA_API_URL", "")
    env_timeout = os.environ.get("GHDATA_TIMEOUT", "")

    final_url = webapi_url or file_url or env_url or "http://api.topeasychina.com:15099/api"
    final_timeout = (timeout or 
                     (int(file_timeout) if file_timeout else 0) or 
                     (int(env_timeout) if env_timeout else 30))

    WEBAPI_BASE_URL = final_url.rstrip("/")
    TIMEOUT = final_timeout

    # 输出目录
    global DOC_DIR, DATA_DIR
    DOC_DIR = os.path.join(BASE_DIR, "doc")
    DATA_DIR = os.path.join(BASE_DIR, "data")
    os.makedirs(DOC_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    # APIKey：仅从 ~/.ghdata/ghdataapikey 读取
    local_file_api_key = _read_apikey_file()
    if api_key:
        # 传参指定Key → 保存到文件并覆盖
        _write_apikey_file(api_key)
        API_KEY = api_key
    elif local_file_api_key:
        API_KEY = local_file_api_key
    else:
        # 文件不存在 → 自动生成随机GUID → 服务端验证失败 → 降级免费预览
        API_KEY = _ensure_api_key()

    _initialized = True

    # 打印配置
    masked_key = API_KEY[:8] + "****" + API_KEY[-4:] if len(API_KEY) > 20 else "（未设置）"
    key_source = "ghdataapikey文件"
    if api_key:
        key_source = "init传参"
    elif not os.path.exists(_APIKEY_FILE):
        key_source = "自动生成（文件不存在）"
    print(f"[config] WebAPI: {WEBAPI_BASE_URL}  timeout={TIMEOUT}s  APIKey: {masked_key} ({key_source})")
    # 购买链接由 db.get_payment_url() 生成（v2.2.50 token化，URL不含完整Key）
    print(f"[config] 购买链接: 由 analyze() 返回的 _payment_url 提供（token化，不再打印完整Key）")
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
    print(f"  配置来源:      settings.json(URL/超时) + ghdataapikey(API密钥)")


# ===== 模块加载时自动初始化 =====
# 确保 config.API_KEY / WEBAPI_BASE_URL / TIMEOUT 在使用前已设置
if not _initialized:
    init()

    print(f"\n  📋 APIKey来源（仅从文件读取）：")
    print(f"  ① init() 传参  → 覆盖文件内容")
    print(f"  ② ~/.ghdata/ghdataapikey → 默认读取位置 ✅")
    print(f"  ③ 自动生成    → 文件不存在时生成随机GUID（无效Key→降级免费预览）")
    print("=" * 50)
