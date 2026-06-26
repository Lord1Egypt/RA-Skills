#!/usr/bin/env python3
"""
和风天气工具模块 - 公共函数库

提供所有和风天气脚本共用的工具函数。
"""

import sys
import os
import json
import gzip
import urllib.request
import urllib.error
import urllib.parse
import datetime as dt

# 尝试加载 dotenv（标准方式读取 .env 文件）
try:
    import dotenv
    dotenv.load_dotenv(os.path.expanduser("~/.openclaw/.env"), override=True)
except ImportError:
    pass


# ============ 天气图标 emoji 映射 ============

WEATHER_ICON_EMOJI = {
    "100": "☀️",   "100n": "🌙",
    "101": "⛅",  "102": "⛅",  "103": "🌤️",  "104": "☁️",
    "200": "🌬️",  "201": "🌬️",  "202": "🌬️",  "203": "🌬️",
    "204": "💨",  "205": "💨",  "206": "💨",  "207": "💨",
    "208": "💨",  "209": "💨",  "210": "🌬️",  "211": "🌬️",
    "212": "🌬️",  "213": "💨",
    "300": "🌦️",  "301": "🌧️",  "302": "⛈️",  "303": "⛈️",
    "304": "⛈️",  "305": "🌧️",  "306": "🌧️",  "307": "🌧️",
    "308": "🌧️",  "309": "🌧️",  "310": "🌧️",  "311": "🌧️",
    "312": "🌧️",  "313": "🌧️",  "314": "🌧️",  "315": "🌧️",
    "316": "🌧️",  "317": "🌧️",  "318": "🌧️",  "399": "🌧️",
    "400": "🌨️",  "401": "🌨️",  "402": "❄️",  "403": "❄️",
    "404": "🌨️",  "405": "🌨️",  "406": "🌨️",  "407": "🌨️",
    "408": "🌨️",  "409": "🌨️",  "410": "🌨️",  "499": "🌨️",
    "500": "🌫️",  "501": "🌫️",  "502": "🌫️",  "503": "🌫️",
    "504": "🌫️",  "507": "😷",  "508": "😷",  "509": "😷",
    "510": "🌫️",  "511": "🌫️",  "512": "🌫️",  "513": "🌫️",
    "514": "🌫️",  "515": "🌫️",
    "800": "🌙",  "801": "🌤️",  "802": "⛅",  "803": "⛅",  "804": "☁️",
    "900": "❓",
}

DEFAULT_WEATHER_EMOJI = "🌡️"

# ============ 紫外线指数等级 ============

UV_DESCRIPTION = {
    "0": "很弱",
    "1": "很弱",
    "2": "弱",
    "3": "中等",
    "4": "较强",
    "5": "强",
    "6": "很强",
    "7": "很强",
    "8": "极强",
    "9": "极强",
    "10": "极强",
    "11": "很强",
    "12": "极强",
}


def get_weather_emoji(icon_code: str) -> str:
    """根据天气图标代码获取 emoji。"""
    return WEATHER_ICON_EMOJI.get(icon_code, DEFAULT_WEATHER_EMOJI)


def uv_description(uv_index: str) -> str:
    """获取紫外线指数描述。"""
    return UV_DESCRIPTION.get(str(uv_index), "未知")

def get_token(arg_val: str | None) -> str:
    """获取 JWT Token。优先级：1) 命令行参数 2) ~/.myjwtkey/last-token.dat"""
    if arg_val:
        return arg_val.strip()

    token_file = os.path.expanduser("~/.myjwtkey/last-token.dat")
    if os.path.exists(token_file):
        with open(token_file, "r", encoding="utf-8") as f:
            token = f.read().strip()
        if token:
            return token

    print(f"错误: 缺少 JWT Token", file=sys.stderr)
    print(f"  请通过以下方式提供：1) --token 参数 2) ~/.myjwtkey/last-token.dat", file=sys.stderr)
    sys.exit(1)


# ============ Host / Env 读取 ============

def get_host(env_var: str, arg_val: str | None, description: str) -> str:
    """获取 API Host，自动补上 https:// 前缀。"""
    val = arg_val or os.environ.get(env_var)
    if not val:
        print(f"错误: 缺少 {description}", file=sys.stderr)
        print(f"  请设置环境变量 {env_var} 或作为命令行参数传入", file=sys.stderr)
        sys.exit(1)
    val = val.strip().rstrip("/")
    if not val.startswith(("http://", "https://")):
        val = "https://" + val
    return val


# ============ 日志 ============

def _mask_token(token: str) -> str:
    """脱敏 JWT token，只显示前8后4位。"""
    if len(token) <= 12:
        return "****"
    return token[:8] + "..." + token[-4:]


def _decompress(body: bytes) -> bytes:
    """尝试解压 gzip，如果失败则返回原始 bytes。"""
    try:
        return gzip.decompress(body)
    except Exception:
        return body


def api_get(url: str, headers: dict, *, log_prefix: str = "api_get") -> dict:
    """
    发送 GET 请求，返回 JSON。支持 gzip 自动解压。
    敏感信息自动脱敏后写入日志。
    """
    log_dir = "/tmp/cslog"
    os.makedirs(log_dir, exist_ok=True)
    today = dt.datetime.now().strftime("%Y%m%d")
    log_path = os.path.join(log_dir, f"{log_prefix}-{today}.log")
    ts = dt.datetime.now().strftime("%H:%M:%S")

    auth_header = headers.get("Authorization", "")
    raw_token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else auth_header
    masked_token = _mask_token(raw_token)

    # 构造可粘贴的 curl 命令（token 已脱敏）
    curl_cmd = (
        f"curl -X GET --compressed \\ \n"
        f" -H 'Authorization: Bearer {masked_token}' \\ \n"
        f" -H 'Accept: application/json' \\ \n"
        f" -H 'Accept-Encoding: gzip' \\ \n"
        f" '{url}'"
    )

    with open(log_path, "a", encoding="utf-8") as log_f:
        log_f.write(f"\n[{ts}] ===== api_get =====\n")
        log_f.write(f"{curl_cmd}\n")
        log_f.write(f"  ────────────────────────────────\n")

    req_headers = dict(headers)
    req_headers["Accept-Encoding"] = "gzip"
    req = urllib.request.Request(url, headers=req_headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            body = _decompress(raw)
            body_str = body.decode("utf-8", errors="replace")
            with open(log_path, "a", encoding="utf-8") as log_f:
                log_f.write(f"  响应 [200 OK]: {body_str[:2000]}\n")
            return json.loads(body_str)
    except urllib.error.HTTPError as e:
        raw = e.read()
        body = _decompress(raw)
        body_str = body.decode("utf-8", errors="replace")
        with open(log_path, "a", encoding="utf-8") as log_f:
            log_f.write(f"  HTTP 错误: {e.code} {e.reason}\n")
            log_f.write(f"  响应内容: {body_str[:2000]}\n")
        print(f"HTTP 错误: {e.code} {e.reason}", file=sys.stderr)
        print(f"响应内容: {body_str[:500]}", file=sys.stderr)
        print(f"已记录到: {log_path}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        with open(log_path, "a", encoding="utf-8") as log_f:
            log_f.write(f"  网络错误: {e.reason}\n")
        print(f"网络错误: {e.reason}", file=sys.stderr)
        sys.exit(1)


# ============ 城市经纬度缓存 ============

# 缓存路径由调用者通过 set_cache_dir() 注入
_cache_dir: str | None = None


def set_cache_dir(script_dir: str) -> None:
    """由调用脚本在入口处注入其所在目录，用于确定缓存文件位置。"""
    global _cache_dir
    _cache_dir = script_dir


def _get_cache_path() -> str:
    """获取城市经纬度缓存文件路径。"""
    if _cache_dir:
        data_dir = os.path.join(_cache_dir, "data")
    else:
        # fallback：使用本模块所在目录
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "location.json")


def _load_cache() -> dict:
    """加载城市缓存。"""
    path = _get_cache_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save_cache(cache: dict) -> None:
    """保存城市缓存到文件。"""
    path = _get_cache_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def lookup_city(host: str, token: str, city_name: str) -> dict | None:
    """
    查询城市经纬度。优先从本地缓存读取，缓存不存在则调用 API 并写入缓存。
    """
    cache = _load_cache()

    if city_name in cache:
        print(f"[缓存命中] {city_name} -> {cache[city_name].get('lat')}, {cache[city_name].get('lon')}", file=sys.stderr)
        return cache[city_name]

    print(f"[缓存未命中] 正在查询 API: {city_name} ...", file=sys.stderr)

    url = f"{host}/geo/v2/city/lookup?location={urllib.parse.quote(city_name)}&number=1"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    result = api_get(url, headers, log_prefix="qweather-geo")
    if result.get("code") != "200":
        print(f"城市查询失败: code={result.get('code')}", file=sys.stderr)
        return None
    locations = result.get("location", [])
    if not locations:
        print(f"未找到城市: {city_name}", file=sys.stderr)
        return None

    city_info = locations[0]

    cache[city_name] = city_info
    _save_cache(cache)
    print(f"[已写入缓存] {city_name}", file=sys.stderr)

    return city_info


# ============ 通用工具函数 ============

def format_timestamp(ts: str) -> str:
    """将 ISO 时间格式化为可读字符串，去掉 T 和时区后缀。"""
    if not ts:
        return ""
    ts = ts.replace("T", " ").replace("+08:00", "").replace("Z", "+00:00")
    return ts.strip()


def _build_display_name(city_info: dict, city_name: str) -> str:
    """
    构建城市显示名。规则：
    - 若 adm2 等于 name，说明是直辖市/省会主城区，显示「X市」或「X省」格式
    - 若不同（如浦东)，显示「X省X市X区」格式（去掉重复后缀）
    """
    adm2 = city_info.get('adm2', '')
    name = city_info.get('name', city_name)
    adm1 = city_info.get('adm1', '')

    # 去掉 adm1 中的「省」「市」等后缀，只留地名部分
    def strip_suffix(region: str, suffix: str) -> str:
        for s in (suffix, suffix[:-1] if suffix else ''):
            if region.endswith(s):
                return region[:-len(s)]
        return region

    # 去掉「市」「省」「自治区」「特别行政区」等后缀
    for suffix in ('市', '省', '自治区', '特别行政区', '壮族自治区', '回族自治区', '维吾尔自治区'):
        adm1 = strip_suffix(adm1, suffix)

    # 若 adm2 和 name 相同（主城区），只显示「X市」
    if adm2 == name:
        # 排除直辖市（adm1 == name 的情况，如「北京市」->「北京」本身）
        if adm1 == name:
            return name  # 直辖市/省会直接用名字
        return f"{adm1}{name}"  # 如「江苏省南京市」->「江苏南京」

    # adm2 和 name 不同，显示「X省X市X区」格式，去掉重复
    # 例如「上海市浦东新区」：adm1=上海，adm2=浦东，name=浦东
    # 去掉 adm1 的「市」后=上海，去掉 adm2 的「区」后=浦东，显示「上海浦东」
    for suffix in ('区', '县', '市'):
        adm2_clean = strip_suffix(adm2, suffix)
    parts = [p for p in (adm1, adm2_clean, name) if p and p not in (adm1,)]
    # 简化：如果 name 已经是 adm2 的一部分，跳过重复
    if adm2_clean and name.startswith(adm2_clean):
        parts = [p for p in parts if p != name]
        result = "".join(parts) + name
    else:
        result = "".join(parts)
    return result if result else name


def resolve_city(city_name: str, host: str, token: str) -> tuple[dict, str, str, str, str] | None:
    """
    查询城市信息，返回 (city_info, lat, lon, full_city_name, location_id)。
    full_city_name 为美化后的城市显示名。
    失败返回 None。
    """
    city_info = lookup_city(host, token, city_name)
    if not city_info:
        return None

    lat = city_info["lat"]
    lon = city_info["lon"]
    location_id = city_info.get("id", "")
    full_city_name = _build_display_name(city_info, city_name)

    print(
        f"找到: {full_city_name}（{city_info.get('adm1', '')}）{lat}, {lon} [{location_id}]",
        file=sys.stderr,
    )
    return city_info, lat, lon, full_city_name, location_id
