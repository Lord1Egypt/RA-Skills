#!/usr/bin/env python3
"""
Fishing Trip Planner - 钓鱼行程规划工具
整合高德地图(路线) + 和风天气(天气/潮汐) API，生成钓鱼行程HTML报告。

Usage:
    python fishing_planner.py --origin "深圳南山" --destination "惠州巽寮湾" --date "2026-06-15" --mode driving
"""

import os
import sys
import json
import argparse
import time
import math
import hashlib
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urlencode

import requests

# ─── 路径常量 ─────────────────────────────────────────────────
FISHING_HOME = Path.home() / ".fishing-planner"
CONFIG_FILE = FISHING_HOME / "config.json"
TRIPS_DIR = FISHING_HOME / "trips"
TRIPS_INDEX = FISHING_HOME / "trips_index.json"

AMAP_BASE = "https://restapi.amap.com/v3"
QWEATHER_BASE = "https://api.qweather.com/v7"
QWEATHER_GEO = "https://geoapi.qweather.com/v2"

MOODS = {
    "driving": {"emoji": "🚗", "label": "驾车"},
    "walking": {"emoji": "🚶", "label": "步行"},
    "transit": {"emoji": "🚌", "label": "公交"},
    "bicycling": {"emoji": "🚴", "label": "骑行"},
}

WEATHER_EMOJI = {
    "晴": "☀️", "少云": "🌤️", "多云": "⛅", "阴": "☁️",
    "雨": "🌧️", "雪": "❄️", "雾": "🌫️", "霾": "😷",
    "阵雨": "🌦️", "雷阵雨": "⛈️", "小雨": "🌧️", "中雨": "🌧️",
    "大雨": "🌧️", "暴雨": "⛈️",
}

WIND_DIR_MAP = {"北": "N", "东北": "NE", "东": "E", "东南": "SE",
                "南": "S", "西南": "SW", "西": "W", "西北": "NW"}


def log(msg: str, level: str = "INFO"):
    prefix = {"INFO": "📋", "OK": "✅", "WARN": "⚠️", "ERR": "❌", "API": "🌐"}
    print(f"  {prefix.get(level, '•')} {msg}", file=sys.stderr)


# ─── 配置管理 ─────────────────────────────────────────────────

def ensure_dirs():
    """确保数据目录存在."""
    FISHING_HOME.mkdir(parents=True, exist_ok=True)
    TRIPS_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict:
    """
    加载配置: config.json → 环境变量 → 默认值.
    config.json 优先级最高.
    """
    config = {
        "amap_key": os.environ.get("AMAP_KEY", ""),
        "qweather_key": os.environ.get("QWEATHER_KEY", ""),
        "default_tide_station": os.environ.get("TIDE_STATION", ""),
        "user_name": "",
        "setup_at": "",
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            # config.json 覆盖环境变量
            for k in ("amap_key", "qweather_key", "default_tide_station", "user_name"):
                if saved.get(k):
                    config[k] = saved[k]
            config["setup_at"] = saved.get("setup_at", "")
        except Exception as e:
            log(f"配置读取异常: {e}", "WARN")
    return config


def save_config(cfg: Dict):
    """保存配置到 config.json."""
    ensure_dirs()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    os.chmod(CONFIG_FILE, 0o600)  # 仅所有者可读写
    log(f"配置已保存: {CONFIG_FILE}", "OK")


def setup_wizard():
    """交互式配置向导."""
    print("\n" + "=" * 56)
    print("  🎣 Fishing Trip Planner - 首次配置向导")
    print("=" * 56)

    config = load_config()

    # 显示当前状态
    def status(val, label):
        return f"✅ {label}" if val else f"⚠️  {label} (未设置)"

    print(f"\n  当前配置状态:")
    print(f"    {status(config['amap_key'], '高德地图 API Key')}")
    print(f"    {status(config['qweather_key'], '和风天气 API Key')}")
    print(f"    {status(config.get('default_tide_station',''), '默认潮汐站点ID')}")
    if config.get("setup_at"):
        print(f"    上次配置: {config['setup_at']}")

    print(f"\n  配置文件位置: {CONFIG_FILE}")

    # Step 1: 高德地图 Key
    print("\n  ── ① 高德地图 API Key ──")
    print("  申请地址: https://lbs.amap.com/ → 创建应用 → Web服务")
    amap_key = input(f"  高德 Key [{mask_key(config['amap_key'])}]: ").strip()
    if amap_key:
        config["amap_key"] = amap_key

    # Step 2: 和风天气 Key
    print("\n  ── ② 和风天气 API Key ──")
    print("  申请地址: https://dev.qweather.com/ → 控制台 → 创建项目")
    print("  选择「免费订阅」(1000次/天)")
    qw_key = input(f"  和风 Key [{mask_key(config['qweather_key'])}]: ").strip()
    if qw_key:
        config["qweather_key"] = qw_key

    # Step 3: 默认潮汐站点
    print("\n  ── ③ 默认潮汐站点ID (可选) ──")
    print("  海钓必配，内陆钓点可跳过")
    print("  获取方式: 和风天气POI搜索 → 找到最近潮汐站 → 格式如 P2951")
    tide = input(f"  潮汐站点ID [{config.get('default_tide_station','') or '跳过'}]: ").strip()
    if tide:
        config["default_tide_station"] = tide

    # Step 4: 用户名
    print("\n  ── ④ 你的称呼 (可选) ──")
    name = input(f"  如何称呼你 [{config.get('user_name','') or '钓鱼人'}]: ").strip()
    if name:
        config["user_name"] = name

    config["setup_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 验证
    print("\n  ⏳ 验证 API 密钥...")
    amap_ok = False
    qw_ok = False

    if config["amap_key"]:
        try:
            resp = requests.get(
                f"{AMAP_BASE}/geocode/geo",
                params={"key": config["amap_key"], "address": "北京"},
                timeout=8
            )
            amap_ok = resp.json().get("status") == "1"
        except:
            pass
    print(f"    高德地图: {'✅ 通过' if amap_ok else '❌ 失败' if config['amap_key'] else '⏭️ 跳过'}")

    if config["qweather_key"]:
        try:
            resp = requests.get(
                f"{QWEATHER_GEO}/city/lookup",
                params={"location": "北京", "key": config["qweather_key"]},
                headers={"Authorization": f"Bearer {config['qweather_key']}"},
                timeout=8
            )
            qw_ok = resp.json().get("code") == "200"
        except:
            pass
    print(f"    和风天气: {'✅ 通过' if qw_ok else '❌ 失败' if config['qweather_key'] else '⏭️ 跳过'}")

    if not amap_ok and config["amap_key"]:
        log("高德 Key 验证失败，请检查是否正确", "WARN")
    if not qw_ok and config["qweather_key"]:
        log("和风 Key 验证失败，请检查是否正确", "WARN")

    save_config(config)

    print("\n  🎉 配置完成！现在可以运行:")
    print('    python fishing_planner.py -o "深圳南山" -d "惠州巽寮湾" -t "2026-06-15"')
    print()
    return config


def mask_key(key: str) -> str:
    """隐藏 Key 中间部分."""
    if not key:
        return "(未设置)"
    if len(key) <= 8:
        return key[:2] + "***"
    return key[:4] + "****" + key[-4:]


def check_keys(config: Dict) -> bool:
    """检查必要的 API Key."""
    ok = True
    if not config.get("amap_key"):
        log("未配置高德地图 API Key", "ERR")
        ok = False
    if not config.get("qweather_key"):
        log("未配置和风天气 API Key", "WARN")
    if not ok:
        log("运行 --setup 进行配置", "INFO")
    return ok


# ─── 行程历史记录 ─────────────────────────────────────────────

def load_trips_index() -> List[Dict]:
    """加载行程索引."""
    if TRIPS_INDEX.exists():
        try:
            with open(TRIPS_INDEX, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return []


def save_trips_index(trips: List[Dict]):
    """保存行程索引."""
    ensure_dirs()
    with open(TRIPS_INDEX, "w", encoding="utf-8") as f:
        json.dump(trips, f, indent=2, ensure_ascii=False)


def save_trip(trip_id: str, html_content: str, metadata: Dict):
    """
    保存一次行程: HTML报告 + 元数据索引.
    trip_id: 唯一标识 (timestamp-based)
    """
    ensure_dirs()
    report_path = TRIPS_DIR / f"{trip_id}.html"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    trips = load_trips_index()
    trips.append(metadata)
    save_trips_index(trips)

    log(f"行程已存档: {trip_id}", "OK")
    return report_path


def show_history(limit: int = 20):
    """展示历史行程列表."""
    trips = load_trips_index()
    if not trips:
        print("\n📭 暂无历史行程记录")
        print(f"  数据目录: {TRIPS_DIR}")
        return

    trips.sort(key=lambda t: t.get("created_at", ""), reverse=True)
    trips = trips[:limit]

    print(f"\n{'='*72}")
    print(f"  📋 钓鱼行程历史记录 (共 {len(load_trips_index())} 条)")
    print(f"{'='*72}")

    for i, t in enumerate(trips, 1):
        trip_id = t.get("id", "?")
        created = t.get("created_at", "")[:16]
        origin = t.get("origin", "?")
        dest = t.get("destination", "?")
        date = t.get("fishing_date", "?")
        score = t.get("score", "?")
        level = t.get("level", "?")
        dist = t.get("distance_km", "?")
        mode = MOODS.get(t.get("mode", ""), {}).get("emoji", "?")

        level_icons = {"优秀": "🎯", "良好": "👍", "一般": "🤔", "不佳": "⚠️"}
        icon = level_icons.get(level, "❓")

        print(f"\n  [{i}] {icon} {trip_id[:12]}")
        print(f"      {created}  {origin} {mode} {dest}")
        print(f"      📅 {date}  |  🚗 {dist}km  |  ⭐ {score}/100 {level}")

    print(f"\n{'─'*72}")
    print(f"  查看报告: python fishing_planner.py --view <序号或ID>")
    print(f"  数据目录: {TRIPS_DIR}")
    print()


def view_trip(trip_ref: str):
    """查看历史行程报告."""
    trips = load_trips_index()

    match = None
    # 尝试序号
    try:
        idx = int(trip_ref) - 1
        trips.sort(key=lambda t: t.get("created_at", ""), reverse=True)
        if 0 <= idx < len(trips):
            match = trips[idx]
    except ValueError:
        pass

    # 尝试 ID 匹配
    if not match:
        for t in trips:
            if t.get("id", "").startswith(trip_ref):
                match = t
                break

    if not match:
        log(f"未找到行程: {trip_ref}", "ERR")
        show_history()
        return

    report_path = TRIPS_DIR / f"{match['id']}.html"
    if not report_path.exists():
        log(f"报告文件不存在: {report_path}", "ERR")
        return

    print(f"\n✅ 打开行程报告: {match['id']}")
    print(f"   {match.get('origin')} → {match.get('destination')} | {match.get('fishing_date')}")
    print(f"   {report_path}")
    # 尝试在浏览器打开
    try:
        webbrowser.open(f"file:///{report_path.as_posix()}")
    except:
        pass


# ─── 高德地图 API ─────────────────────────────────────────────

def amap_geocode(config: Dict, address: str, city: str = "") -> Optional[Tuple[float, float, str]]:
    """地理编码: 地名→坐标. Returns (lon, lat, name)."""
    log(f"地理编码: {address}", "API")
    params = {"key": config["amap_key"], "address": address}
    if city:
        params["city"] = city
    resp = requests.get(f"{AMAP_BASE}/geocode/geo", params=params, timeout=10)
    data = resp.json()
    if data.get("status") == "1" and data.get("geocodes"):
        gc = data["geocodes"][0]
        lon, lat = gc["location"].split(",")
        return float(lon), float(lat), gc.get("formatted_address", address)
    log(f"地理编码失败: {data.get('info')}", "ERR")
    return None


def amap_route(config: Dict, origin: str, destination: str, mode: str) -> Optional[Dict]:
    """路线规划."""
    log(f"路线规划: {mode} ({origin} → {destination})", "API")

    if mode == "driving":
        url = f"{AMAP_BASE}/direction/driving"
        params = {"key": config["amap_key"], "origin": origin, "destination": destination,
                  "extensions": "all", "strategy": "10"}
    elif mode == "walking":
        url = f"{AMAP_BASE}/direction/walking"
        params = {"key": config["amap_key"], "origin": origin, "destination": destination}
    elif mode == "transit":
        url = f"{AMAP_BASE}/direction/transit/integrated"
        params = {"key": config["amap_key"], "origin": origin, "destination": destination, "city": "0755"}
    elif mode == "bicycling":
        url = f"{AMAP_BASE}/v4/direction/bicycling"
        params = {"key": config["amap_key"], "origin": origin, "destination": destination}
    else:
        log(f"不支持的出行方式: {mode}", "ERR")
        return None

    resp = requests.get(url, params=params, timeout=15)
    data = resp.json()
    if data.get("status") == "1" and data.get("route"):
        return data["route"]
    log(f"路线规划失败: {data.get('info')}", "ERR")
    return None


def parse_route(route: Dict, mode: str) -> Dict:
    """解析路线规划结果."""
    paths = route.get("paths", [])
    if not paths:
        return {"error": "无路线方案"}

    path = paths[0]
    distance_km = round(path.get("distance", 0) / 1000, 1)
    duration_min = round(path.get("duration", 0) / 60)
    tolls = path.get("tolls", 0)
    taxi_cost = route.get("taxi_cost", 0)
    traffic_lights = path.get("traffic_lights", 0)

    steps = []
    for s in path.get("steps", [])[:8]:  # 最多8步
        steps.append({
            "instruction": s.get("instruction", ""),
            "road": s.get("road", ""),
            "distance": round(s.get("distance", 0) / 1000, 2),
        })

    # 路况统计 (仅驾车)
    traffic_status = {}
    for s in path.get("steps", []):
        for t in s.get("tmcs", []):
            status = t.get("status", "未知")
            traffic_status[status] = traffic_status.get(status, 0) + t.get("distance", 0)

    total_traffic = sum(traffic_status.values()) or 1
    traffic_pct = {k: round(v / total_traffic * 100, 1) for k, v in traffic_status.items()}

    return {
        "distance_km": distance_km,
        "duration_min": duration_min,
        "duration_str": f"{duration_min // 60}小时{duration_min % 60}分钟" if duration_min >= 60 else f"{duration_min}分钟",
        "tolls": tolls,
        "taxi_cost": taxi_cost,
        "traffic_lights": traffic_lights,
        "steps": steps,
        "traffic_pct": traffic_pct,
        "strategy": path.get("strategy", ""),
    }


# ─── 和风天气 API ─────────────────────────────────────────────

def _qw_headers(config: Dict) -> Dict:
    """和风天气请求头."""
    key = config.get("qweather_key", "")
    return {"Authorization": f"Bearer {key}"} if key else {}


def qweather_city_lookup(config: Dict, location: str) -> Optional[str]:
    """城市搜索, 返回 LocationID."""
    log(f"城市搜索: {location}", "API")
    key = config.get("qweather_key", "")
    params = {"location": location, "key": key} if key else {"location": location}
    try:
        resp = requests.get(f"{QWEATHER_GEO}/city/lookup", params=params, timeout=10)
        data = resp.json()
        if data.get("code") == "200" and data.get("location"):
            loc = data["location"][0]
            return loc["id"]
    except Exception as e:
        log(f"城市搜索失败: {e}", "WARN")
    return None


def qweather_7d(config: Dict, location_id: str) -> Optional[List[Dict]]:
    """7天天气预报."""
    log("获取7天天气预报", "API")
    try:
        resp = requests.get(f"{QWEATHER_BASE}/weather/7d",
                           params={"location": location_id},
                           headers=_qw_headers(config), timeout=10)
        data = resp.json()
        if data.get("code") == "200":
            return data.get("daily", [])
    except Exception as e:
        log(f"天气查询失败: {e}", "WARN")
    return None


def qweather_24h(config: Dict, location_id: str) -> Optional[List[Dict]]:
    """24小时逐小时预报."""
    log("获取逐小时预报", "API")
    try:
        resp = requests.get(f"{QWEATHER_BASE}/weather/24h",
                           params={"location": location_id},
                           headers=_qw_headers(config), timeout=10)
        data = resp.json()
        if data.get("code") == "200":
            return data.get("hourly", [])
    except Exception as e:
        log(f"逐小时查询失败: {e}", "WARN")
    return None


def qweather_tide(config: Dict, tide_station_id: str, date_str: str) -> Optional[Dict]:
    """潮汐数据. date_str: yyyyMMdd"""
    log(f"获取潮汐数据: {tide_station_id} @ {date_str}", "API")
    try:
        resp = requests.get(f"{QWEATHER_BASE}/ocean/tide",
                           params={"location": tide_station_id, "date": date_str},
                           headers=_qw_headers(config), timeout=10)
        data = resp.json()
        if data.get("code") == "200":
            return data
    except Exception as e:
        log(f"潮汐查询失败: {e}", "WARN")
    return None


def qweather_fishing_index(config: Dict, location_id: str) -> Optional[Dict]:
    """钓鱼指数."""
    log("获取钓鱼指数", "API")
    try:
        resp = requests.get(f"{QWEATHER_BASE}/indices/1d",
                           params={"location": location_id, "type": "1"},
                           headers=_qw_headers(config), timeout=10)
        data = resp.json()
        if data.get("code") == "200" and data.get("daily"):
            return data["daily"][0]
    except Exception as e:
        log(f"钓鱼指数查询失败: {e}", "WARN")
    return None


# ─── 钓鱼建议评分 ─────────────────────────────────────────────

def calculate_fishing_score(weather_data: Dict, tide_data: Optional[Dict],
                            wind_scale: int, precip: float, temp: int) -> Dict:
    """综合钓鱼评分系统 (0-100分)."""
    score = 70  # 基础分
    tips = []
    conditions = []

    # 风力评分 (1-3级最佳)
    if wind_scale <= 2:
        score += 10
        conditions.append(("风力", "宜", f"{wind_scale}级 - 微风适宜"))
    elif wind_scale <= 4:
        score += 5
        conditions.append(("风力", "可", f"{wind_scale}级 - 中等风力"))
    elif wind_scale <= 6:
        score -= 10
        conditions.append(("风力", "差", f"{wind_scale}级 - 风力偏大"))
        tips.append("建议使用重铅坠，选择背风钓位")
    else:
        score -= 25
        conditions.append(("风力", "禁", f"{wind_scale}级 - 不建议出钓"))
        tips.append("风力过大，安全风险高，建议改期")

    # 温度评分 (15-28°C最佳)
    if 15 <= temp <= 28:
        score += 10
        conditions.append(("温度", "宜", f"{temp}°C - 鱼类活跃"))
    elif 5 <= temp < 15 or 28 < temp <= 35:
        score += 3
        conditions.append(("温度", "可", f"{temp}°C - 温度适中"))
    else:
        score -= 15
        conditions.append(("温度", "差", f"{temp}°C - 温度不适宜"))
        tips.append("极端温度鱼类活性低，可选择深水区或调整钓层")

    # 降水评分
    if precip <= 0.5:
        score += 5
        conditions.append(("降水", "宜", "无降水或微量"))
    elif precip <= 5:
        score += 0
        conditions.append(("降水", "可", f"{precip}mm - 小雨"))
        tips.append("带好雨具，小雨天鱼口可能更好")
    else:
        score -= 15
        conditions.append(("降水", "差", f"{precip}mm - 雨量较大"))
        tips.append("降雨量大，注意防滑和安全")

    # 潮汐评分 (如果有潮汐数据)
    tide_tip = ""
    tide_events = []
    if tide_data and tide_data.get("tideTable"):
        tide_table = tide_data["tideTable"]
        highs = [t for t in tide_table if t.get("type") == "H"]
        lows = [t for t in tide_table if t.get("type") == "L"]

        # 涨落潮判断：涨潮时钓鱼好
        morning_high = any("06" <= t.get("fxTime", "")[11:13] <= "10" for t in highs)
        evening_high = any("16" <= t.get("fxTime", "")[11:13] <= "19" for t in highs)

        if morning_high or evening_high:
            score += 8
            conditions.append(("潮汐", "宜", "早晚有满潮窗口"))
            tide_tip = "早晨或傍晚满潮前后1小时是最佳钓鱼窗口期"
        else:
            score += 2
            conditions.append(("潮汐", "可", "潮汐窗口一般"))
            tide_tip = "关注涨潮时段，涨潮时鱼群靠岸觅食"

        for t in tide_table:
            fx_time = t.get("fxTime", "")
            hhmm = fx_time[11:16] if len(fx_time) >= 16 else fx_time
            emoji = "🌊" if t.get("type") == "H" else "🏖️"
            label = "满潮" if t.get("type") == "H" else "干潮"
            tide_events.append({
                "time": hhmm,
                "height": t.get("height", "?"),
                "type": label,
                "emoji": emoji,
            })
    else:
        conditions.append(("潮汐", "--", "无潮汐数据(内陆钓点)"))

    # 综合评分等级
    score = max(0, min(100, score))
    if score >= 80:
        level, level_color, level_emoji = "优秀", "#22c55e", "🎯"
    elif score >= 60:
        level, level_color, level_emoji = "良好", "#3b82f6", "👍"
    elif score >= 40:
        level, level_color, level_emoji = "一般", "#f59e0b", "🤔"
    else:
        level, level_color, level_emoji = "不佳", "#ef4444", "⚠️"

    return {
        "score": score,
        "level": level,
        "level_color": level_color,
        "level_emoji": level_emoji,
        "conditions": conditions,
        "tips": tips,
        "tide_tip": tide_tip,
        "tide_events": tide_events,
    }


# ─── HTML 报告生成 ─────────────────────────────────────────────

def generate_html(origin_name: str, dest_name: str, date_str: str, mode: str,
                  route_info: Dict, weather_daily: List[Dict], weather_hourly: List[Dict],
                  tide_data: Optional[Dict], fishing_score: Dict,
                  fishing_index: Optional[Dict]) -> str:
    """生成HTML钓鱼行程报告."""

    mode_info = MOODS.get(mode, MOODS["driving"])

    # ── 天气卡片 ──
    weather_cards = ""
    for i, day in enumerate(weather_daily[:7]):
        date = day.get("fxDate", "")
        text_day = day.get("textDay", "?")
        temp_high = day.get("tempMax", "?")
        temp_low = day.get("tempMin", "?")
        wind_dir = day.get("windDirDay", "?")
        wind_scale = day.get("windScaleDay", "?")
        humidity = day.get("humidity", "?")
        precip = day.get("precip", "0")
        emoji = WEATHER_EMOJI.get(text_day, "🌤️")

        active = "active" if i == 0 else ""

        weather_cards += f"""
        <div class="weather-card {active}">
          <div class="wc-date">{date[-5:] if len(date)>=10 else date}</div>
          <div class="wc-icon">{emoji}</div>
          <div class="wc-text">{text_day}</div>
          <div class="wc-temp">{temp_low}° / <b>{temp_high}°</b></div>
          <div class="wc-detail">🌬️ {wind_dir} {wind_scale}级 | 💧 {humidity}%</div>
          <div class="wc-detail">🌧️ {precip}mm</div>
        </div>"""

    # ── 路线步骤 ──
    route_steps = ""
    for i, step in enumerate(route_info.get("steps", [])[:5]):
        route_steps += f"""
        <div class="route-step">
          <div class="step-num">{i+1}</div>
          <div class="step-content">
            <div class="step-instruction">{step['instruction']}</div>
            <div class="step-meta">{step['road'] or ''} · {step['distance']}km</div>
          </div>
        </div>"""

    # ── 潮汐表格 ──
    tide_rows = ""
    if fishing_score.get("tide_events"):
        for t in fishing_score["tide_events"]:
            tide_rows += f"""
            <tr>
              <td>{t['emoji']}</td>
              <td>{t['type']}</td>
              <td><b>{t['time']}</b></td>
              <td>{t['height']}m</td>
            </tr>"""
    else:
        tide_rows = '<tr><td colspan="4" class="no-data">无潮汐数据 (内陆钓点)</td></tr>'

    # ── 条件评分列表 ──
    condition_rows = ""
    for name, status, desc in fishing_score.get("conditions", []):
        tag_class = {"宜": "tag-green", "可": "tag-yellow", "差": "tag-red", "禁": "tag-red", "--": "tag-gray"}
        tag = tag_class.get(status, "tag-gray")
        condition_rows += f"""
        <tr>
          <td>{name}</td>
          <td><span class="tag {tag}">{status}</span></td>
          <td>{desc}</td>
        </tr>"""

    # ── 建议列表 ──
    tip_items = ""
    for tip in fishing_score.get("tips", []):
        tip_items += f'<li>💡 {tip}</li>'
    if fishing_score.get("tide_tip"):
        tip_items += f'<li>🌊 {fishing_score["tide_tip"]}</li>'
    if fishing_index:
        tip_items += f'<li>🎣 钓鱼指数: {fishing_index.get("category", "?")} - {fishing_index.get("text", "")}</li>'
    if not tip_items:
        tip_items = '<li>无特别建议</li>'

    # ── 逐小时天气行 (截取6:00-20:00) ──
    hourly_rows = ""
    for h in weather_hourly or []:
        fx_time = h.get("fxTime", "")
        hh = fx_time[11:13] if len(fx_time) >= 13 else "?"
        temp = h.get("temp", "?")
        text = h.get("text", "?")
        wind = h.get("windScale", "?")
        pop = h.get("pop", "0")
        emoji = WEATHER_EMOJI.get(text, "🌤️")
        pop_pct = int(pop) if pop and pop != "0" else 0
        pop_str = f"{pop}%" if pop_pct > 0 else "-"

        hourly_rows += f"""
        <tr>
          <td>{hh}:00</td>
          <td>{emoji} {text}</td>
          <td>{temp}°C</td>
          <td>{wind}级</td>
          <td>{pop_str}</td>
        </tr>"""

    # ── 生成完整HTML ──
    score = fishing_score["score"]
    score_color = fishing_score["level_color"]
    score_emoji = fishing_score["level_emoji"]
    score_level = fishing_score["level"]
    score_angle = score / 100 * 360

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>钓鱼行程规划 - {dest_name}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%); color: #e2e8f0; min-height: 100vh; padding: 20px; }}
.container {{ max-width: 900px; margin: 0 auto; }}
.header {{ text-align: center; padding: 30px 20px; }}
.header h1 {{ font-size: 2em; background: linear-gradient(135deg, #60a5fa, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px; }}
.header .subtitle {{ color: #94a3b8; font-size: 1em; }}
.header .route-line {{ font-size: 1.2em; margin-top: 12px; color: #cbd5e1; }}

/* 评分盘 */
.score-section {{ background: rgba(30, 41, 59, 0.8); backdrop-filter: blur(10px); border-radius: 20px; padding: 30px; margin: 20px 0; display: flex; align-items: center; gap: 30px; border: 1px solid rgba(100, 116, 139, 0.3); flex-wrap: wrap; justify-content: center; }}
.score-circle {{ width: 150px; height: 150px; position: relative; }}
.score-circle svg {{ transform: rotate(-90deg); }}
.score-bg {{ fill: none; stroke: rgba(100, 116, 139, 0.2); stroke-width: 12; }}
.score-fill {{ fill: none; stroke: {score_color}; stroke-width: 12; stroke-linecap: round; transition: stroke-dashoffset 1s ease; }}
.score-text {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; }}
.score-text .big {{ font-size: 2.5em; font-weight: 800; color: {score_color}; }}
.score-text .small {{ font-size: 0.9em; color: #94a3b8; }}

.card {{ background: rgba(30, 41, 59, 0.8); backdrop-filter: blur(10px); border-radius: 16px; padding: 24px; margin: 16px 0; border: 1px solid rgba(100, 116, 139, 0.3); }}
.card h2 {{ font-size: 1.2em; margin-bottom: 16px; color: #93c5fd; display: flex; align-items: center; gap: 8px; }}

/* 路线卡片 */
.route-summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 16px; margin-bottom: 20px; }}
.route-metric {{ text-align: center; padding: 12px; background: rgba(15, 23, 42, 0.5); border-radius: 12px; }}
.route-metric .num {{ font-size: 1.8em; font-weight: 700; color: #60a5fa; }}
.route-metric .label {{ font-size: 0.85em; color: #94a3b8; margin-top: 4px; }}
.route-step {{ display: flex; gap: 12px; padding: 10px 0; border-bottom: 1px solid rgba(100, 116, 139, 0.15); }}
.route-step:last-child {{ border-bottom: none; }}
.step-num {{ width: 28px; height: 28px; background: rgba(96, 165, 250, 0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.85em; font-weight: 700; color: #60a5fa; flex-shrink: 0; }}
.step-instruction {{ font-size: 0.95em; }}
.step-meta {{ font-size: 0.8em; color: #64748b; margin-top: 2px; }}

/* 天气卡片 */
.weather-grid {{ display: flex; gap: 12px; overflow-x: auto; padding-bottom: 8px; }}
.weather-card {{ min-width: 110px; text-align: center; padding: 14px 10px; background: rgba(15, 23, 42, 0.5); border-radius: 12px; border: 2px solid transparent; }}
.weather-card.active {{ border-color: {score_color}; background: rgba(96, 165, 250, 0.08); }}
.wc-date {{ font-size: 0.85em; color: #94a3b8; }}
.wc-icon {{ font-size: 2em; margin: 6px 0; }}
.wc-text {{ font-size: 0.9em; font-weight: 600; }}
.wc-temp {{ font-size: 0.95em; margin: 4px 0; }}
.wc-detail {{ font-size: 0.75em; color: #64748b; }}

/* 表格 */
table {{ width: 100%; border-collapse: collapse; font-size: 0.9em; }}
th {{ text-align: left; padding: 10px 8px; color: #94a3b8; font-weight: 600; border-bottom: 1px solid rgba(100, 116, 139, 0.3); }}
td {{ padding: 10px 8px; border-bottom: 1px solid rgba(100, 116, 139, 0.1); }}
.tag {{ padding: 2px 10px; border-radius: 12px; font-size: 0.8em; font-weight: 600; }}
.tag-green {{ background: rgba(34, 197, 94, 0.15); color: #22c55e; }}
.tag-yellow {{ background: rgba(245, 158, 11, 0.15); color: #f59e0b; }}
.tag-red {{ background: rgba(239, 68, 68, 0.15); color: #ef4444; }}
.tag-gray {{ background: rgba(100, 116, 139, 0.15); color: #64748b; }}
.no-data {{ color: #64748b; text-align: center; padding: 20px; }}

/* 建议 */
ul.advice {{ list-style: none; padding: 0; }}
ul.advice li {{ padding: 8px 0; border-bottom: 1px solid rgba(100, 116, 139, 0.1); }}
ul.advice li:last-child {{ border-bottom: none; }}

/* 潮汐曲线可视化 */
.tide-visual {{ display: flex; align-items: flex-end; height: 80px; gap: 2px; margin: 16px 0; padding: 0 8px; }}
.tide-bar {{ flex: 1; border-radius: 2px 2px 0 0; opacity: 0.6; }}
.tide-bar.high {{ background: #60a5fa; opacity: 0.8; }}
.tide-bar.low {{ background: #f59e0b; opacity: 0.6; }}

.footer {{ text-align: center; padding: 20px; color: #475569; font-size: 0.8em; }}
.footer a {{ color: #64748b; }}

@media (max-width: 600px) {{
  .score-section {{ flex-direction: column; }}
  .route-summary {{ grid-template-columns: repeat(2, 1fr); }}
}}
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <h1>🎣 钓鱼行程规划报告</h1>
    <div class="route-line">{origin_name} {mode_info['emoji']} {dest_name}</div>
    <div class="subtitle">{date_str} · {mode_info['label']}出行</div>
  </div>

  <!-- 综合评分 -->
  <div class="score-section">
    <div class="score-circle">
      <svg width="150" height="150" viewBox="0 0 150 150">
        <circle class="score-bg" cx="75" cy="75" r="66"/>
        <circle class="score-fill" cx="75" cy="75" r="66"
          stroke-dasharray="{score / 100 * 414.69} 414.69"/>
      </svg>
      <div class="score-text">
        <div class="big">{score_emoji}</div>
        <div class="small">{score_level}</div>
      </div>
    </div>
    <div>
      <div style="font-size: 3em; font-weight: 800; color: {score_color};">{score}<span style="font-size:0.5em;color:#94a3b8">/100</span></div>
      <div style="color: #94a3b8; margin-top: 4px;">综合钓鱼指数评分</div>
    </div>
  </div>

  <!-- 路线概览 -->
  <div class="card">
    <h2>📍 行程路线</h2>
    <div class="route-summary">
      <div class="route-metric">
        <div class="num">{route_info['distance_km']}<span style="font-size:0.5em">km</span></div>
        <div class="label">总距离</div>
      </div>
      <div class="route-metric">
        <div class="num">{route_info['duration_str']}</div>
        <div class="label">预计耗时</div>
      </div>
      <div class="route-metric">
        <div class="num">¥{route_info['tolls']}</div>
        <div class="label">过路费</div>
      </div>
      <div class="route-metric">
        <div class="num">{route_info['traffic_lights']}</div>
        <div class="label">红绿灯</div>
      </div>
    </div>
    {route_steps}
  </div>

  <!-- 天气预报 -->
  <div class="card">
    <h2>🌤️ 天气预报</h2>
    <div class="weather-grid">
      {weather_cards}
    </div>
  </div>

  <!-- 逐小时天气 -->
  <div class="card">
    <h2>⏰ 逐小时天气 ({date_str})</h2>
    <table>
      <tr><th>时间</th><th>天气</th><th>温度</th><th>风力</th><th>降水概率</th></tr>
      {hourly_rows}
    </table>
  </div>

  <!-- 潮汐数据 -->
  <div class="card">
    <h2>🌊 潮汐预报</h2>
    <table>
      <tr><th>类型</th><th></th><th>时间</th><th>潮高</th></tr>
      {tide_rows}
    </table>
  </div>

  <!-- 钓鱼条件评估 -->
  <div class="card">
    <h2>📊 钓鱼条件评估</h2>
    <table>
      <tr><th>条件</th><th>评级</th><th>详情</th></tr>
      {condition_rows}
    </table>
  </div>

  <!-- 建议 -->
  <div class="card">
    <h2>💡 钓鱼建议 & 注意事项</h2>
    <ul class="advice">
      {tip_items}
      <li>🎒 装备清单: 钓竿、鱼饵、防晒用品、雨具、饮用水、急救包</li>
      <li>🦺 安全提醒: 穿救生衣(海钓)、注意天气变化、告知家人行程</li>
      <li>📱 建议提前下载离线地图，部分海域信号不佳</li>
    </ul>
  </div>

  <div class="footer">
    <p>数据来源: 高德地图 · 和风天气 | 仅供参考，以实际情况为准</p>
    <p>Fish On! 🎣</p>
  </div>

</div>
</body>
</html>"""
    return html


# ─── 主流程 ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="🎣 钓鱼行程规划工具 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python fishing_planner.py --setup                          # 首次配置向导
  python fishing_planner.py -o "深圳" -d "巽寮湾" -t "2026-06-15"  # 生成规划
  python fishing_planner.py --history                        # 查看历史记录
  python fishing_planner.py --view 1                         # 查看第1条历史报告
        """
    )

    # 操作模式 (互斥)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--setup", "-S", action="store_true",
                       help="运行配置向导 (首次使用)")
    action.add_argument("--history", "-H", action="store_true",
                       help="查看历史行程记录")
    action.add_argument("--view", "-V", type=str, metavar="ID",
                       help="查看指定历史报告 (序号或ID)")

    # 规划参数
    parser.add_argument("--origin", "-o", help="出发地 (如: 深圳南山)")
    parser.add_argument("--destination", "-d", help="目的地/钓点 (如: 惠州巽寮湾)")
    parser.add_argument("--date", "-t", help="钓鱼日期 (如: 2026-06-15)")
    parser.add_argument("--mode", "-m", default="driving",
                       choices=["driving", "walking", "transit", "bicycling"],
                       help="出行方式 (默认: driving)")
    parser.add_argument("--tide-station", "-s", default="__auto__",
                       help="和风天气潮汐站点ID (默认读取配置文件)")
    parser.add_argument("--output", "-O", help="输出HTML文件路径 (默认保存到行程库)")

    args = parser.parse_args()
    config = load_config()

    # ── 模式: 配置向导 ──
    if args.setup:
        setup_wizard()
        return

    # ── 模式: 查看历史 ──
    if args.history:
        show_history()
        return

    # ── 模式: 查看历史报告 ──
    if args.view:
        view_trip(args.view)
        return

    # ── 模式: 生成规划 ──
    if not args.origin or not args.destination or not args.date:
        parser.error("规划模式需要 --origin, --destination, --date\n"
                     "  或使用 --setup 运行配置向导\n"
                     "  或使用 --history 查看历史记录")

    print("\n🎣 钓鱼行程规划工具 v2.0\n", file=sys.stderr)
    print(f"  {args.origin} → {args.destination} | {args.date} | {args.mode}\n", file=sys.stderr)

    if not check_keys(config):
        print("\n💡 请运行配置向导:", file=sys.stderr)
        print("  python fishing_planner.py --setup", file=sys.stderr)
        sys.exit(1)

    # 潮汐站点: 命令行 > 配置文件 > 跳过
    tide_station = args.tide_station
    if tide_station == "__auto__":
        tide_station = config.get("default_tide_station", "")

    # 1. 地理编码
    origin_coord = amap_geocode(config, args.origin)
    dest_coord = amap_geocode(config, args.destination)
    if not origin_coord or not dest_coord:
        print("\n❌ 地理编码失败", file=sys.stderr)
        sys.exit(1)

    origin_lonlat = f"{origin_coord[0]},{origin_coord[1]}"
    dest_lonlat = f"{dest_coord[0]},{dest_coord[1]}"
    log(f"起点: {origin_coord[2]} ({origin_lonlat})", "OK")
    log(f"终点: {dest_coord[2]} ({dest_lonlat})", "OK")

    # 2. 路线规划
    route_data = amap_route(config, origin_lonlat, dest_lonlat, args.mode)
    if not route_data:
        print("\n❌ 路线规划失败", file=sys.stderr)
        sys.exit(1)
    route_info = parse_route(route_data, args.mode)
    log(f"路线: {route_info['distance_km']}km, {route_info['duration_str']}", "OK")

    # 3. 天气查询 - 使用目的地
    city_id = qweather_city_lookup(config, args.destination)
    weather_daily = qweather_7d(config, city_id) if city_id else []
    weather_hourly = qweather_24h(config, city_id) if city_id else []
    fishing_index = qweather_fishing_index(config, city_id) if city_id else None

    if city_id:
        log(f"城市ID: {city_id}", "OK")
    if weather_daily:
        log(f"天气: {len(weather_daily)}天预报获取成功", "OK")

    # 4. 潮汐查询
    tide_data = None
    if tide_station:
        date_fmt = args.date.replace("-", "")
        tide_data = qweather_tide(config, tide_station, date_fmt)
        if tide_data:
            log(f"潮汐: {len(tide_data.get('tideTable', []))}条记录", "OK")
    else:
        log("未指定潮汐站点，将跳过潮汐数据 (内陆钓点可选)", "WARN")

    # 5. 综合评分
    today_weather = weather_daily[0] if weather_daily else {}
    wind_scale = int(today_weather.get("windScaleDay", "3") or "3")
    precip = float(today_weather.get("precip", "0") or "0")
    temp = int(today_weather.get("tempMax", "25") or "25")

    fishing_score = calculate_fishing_score(
        weather_data=today_weather,
        tide_data=tide_data,
        wind_scale=wind_scale,
        precip=precip,
        temp=temp,
    )
    log(f"钓鱼评分: {fishing_score['score']}/100 ({fishing_score['level']})", "OK")

    # 6. 生成HTML报告
    html = generate_html(
        origin_name=origin_coord[2],
        dest_name=dest_coord[2],
        date_str=args.date,
        mode=args.mode,
        route_info=route_info,
        weather_daily=weather_daily,
        weather_hourly=weather_hourly,
        tide_data=tide_data,
        fishing_score=fishing_score,
        fishing_index=fishing_index,
    )

    # 7. 保存报告 (输出路径 OR 行程库)
    trip_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    if args.output:
        output_path = os.path.abspath(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        log(f"报告已保存: {output_path}", "OK")
    else:
        # 默认保存到行程库
        output_path = save_trip(
            trip_id=trip_id,
            html_content=html,
            metadata={
                "id": trip_id,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "origin": origin_coord[2],
                "destination": dest_coord[2],
                "fishing_date": args.date,
                "mode": args.mode,
                "distance_km": route_info["distance_km"],
                "duration_str": route_info["duration_str"],
                "score": fishing_score["score"],
                "level": fishing_score["level"],
                "tide_station": tide_station or "",
            }
        )
        output_path = str(output_path)

    print(f"\n✅ 报告已生成: {output_path}", file=sys.stderr)
    print(output_path)
    print(f"\n📊 钓鱼评分: {fishing_score['score']}/100 ({fishing_score['level']})", file=sys.stderr)
    print(f"🚗 {route_info['distance_km']}km | {route_info['duration_str']} | 过路费¥{route_info['tolls']}", file=sys.stderr)
    print(f"\n💡 查看历史: python fishing_planner.py --history", file=sys.stderr)


if __name__ == "__main__":
    main()
