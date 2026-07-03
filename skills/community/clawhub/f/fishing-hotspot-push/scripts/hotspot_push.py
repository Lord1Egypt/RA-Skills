#!/usr/bin/env python3
"""
Fishing Hotspot Push - 钓鱼热点推送
多渠道聚合钓鱼情报 + 天气 + 位置，推送最佳钓点。

Usage:
    python hotspot_push.py --setup
    python hotspot_push.py --run
    python hotspot_push.py --run --city "深圳"
    python hotspot_push.py --run --input "搜索文本..."
    python hotspot_push.py --history
    python hotspot_push.py --view 1
"""

import os
import sys
import json
import argparse
import re
import hashlib
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urlencode
from collections import defaultdict

import requests

# ─── 路径常量 ─────────────────────────────────────────────────
HOTSPOT_HOME = Path.home() / ".fishing-hotspot"
CONFIG_FILE = HOTSPOT_HOME / "config.json"
REPORTS_DIR = HOTSPOT_HOME / "reports"
PUSH_INDEX = HOTSPOT_HOME / "push_index.json"

# 共享 fishing-trip-planner 配置
FISHING_PLANNER_CONFIG = Path.home() / ".fishing-planner" / "config.json"

AMAP_BASE = "https://restapi.amap.com/v3"
QWEATHER_BASE = "https://api.qweather.com/v7"
QWEATHER_GEO = "https://geoapi.qweather.com/v2"

# ─── 钓鱼领域知识库 ──────────────────────────────────────────

# 钓鱼圈黑话 → 评分信号
SENTIMENT_POSITIVE = [
    "爆护", "狂拉", "连杆", "爆箱", "爆桶", "大丰收",
    "口好", "鱼口好", "鱼情好", "狂口", "疯口",
    "大鱼", "巨物", "米级", "大货", "惊喜",
    "推荐", "不错", "很棒", "爽", "过瘾", "满足",
]

SENTIMENT_NEGATIVE = [
    "空军", "打龟", "没口", "停口", "鱼口差",
    "小鱼闹", "杂鱼", "不好钓", "失望", "白跑",
    "水浑", "涨水", "退水", "电鱼", "网鱼",
]

# 常见鱼种
FISH_SPECIES = [
    "鲫鱼", "鲤鱼", "草鱼", "青鱼", "鲢鱼", "鳙鱼", "鲶鱼", "黑鱼",
    "翘嘴", "鳊鱼", "罗非", "鲮鱼", "鳜鱼", "鲈鱼", "黄颡", "黄辣丁",
    "白条", "麦穗", "鳑鲏", "马口", "溪哥", "桃花鱼",
    "黑鲷", "黄鳍鲷", "石斑", "海鲈", "鲻鱼", "泥猛", "乌头",
    "金枪鱼", "马鲛", "带鱼", "黄鱼", "鲅鱼", "八爪鱼",
]

# 常见钓饵
FISH_BAITS = [
    "蚯蚓", "红虫", "玉米", "麦粒", "商品饵", "沙蚕", "虾肉",
    "活虾", "小鱼", "路亚", "亮片", "软虫", "米诺", "VIB",
]

# 水域类型 POI 关键词
WATER_POI_KEYWORDS = [
    "水库", "湖泊", "河流", "海域", "钓场", "鱼塘", "垂钓园",
    "湿地", "港湾", "码头", "海滩", "礁石",
]

WEATHER_EMOJI = {
    "晴": "☀️", "少云": "🌤️", "多云": "⛅", "阴": "☁️",
    "雨": "🌧️", "雪": "❄️", "雾": "🌫️", "霾": "😷",
    "阵雨": "🌦️", "雷阵雨": "⛈️", "小雨": "🌧️", "中雨": "🌧️",
    "大雨": "🌧️", "暴雨": "⛈️",
}


# ─── 工具函数 ─────────────────────────────────────────────────

def log(msg: str, level: str = "INFO"):
    prefix = {"INFO": "📋", "OK": "✅", "WARN": "⚠️", "ERR": "❌", "API": "🌐", "NLP": "🧠"}
    print(f"  {prefix.get(level, '•')} {msg}", file=sys.stderr)


def mask_key(key: str) -> str:
    if not key:
        return "(未设置)"
    if len(key) <= 8:
        return key[:2] + "***"
    return key[:4] + "****" + key[-4:]


def extract_chinese(text: str) -> str:
    """提取中文内容."""
    return "".join(re.findall(r"[\u4e00-\u9fff]+", text))


# ─── 配置管理 ─────────────────────────────────────────────────

def ensure_dirs():
    HOTSPOT_HOME.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict:
    """加载配置: config.json → fishing-planner共享 → 环境变量."""
    config = {
        "amap_key": "",
        "qweather_key": "",
        "home_city": "",
        "home_coordinates": [0.0, 0.0],
        "search_radius_km": 50,
        "fish_type": "不限",
        "user_name": "",
        "setup_at": "",
    }

    # 1. 环境变量
    config["amap_key"] = os.environ.get("AMAP_KEY", "")
    config["qweather_key"] = os.environ.get("QWEATHER_KEY", "")

    # 2. 尝试共享 fishing-trip-planner 配置
    if FISHING_PLANNER_CONFIG.exists():
        try:
            with open(FISHING_PLANNER_CONFIG, "r", encoding="utf-8") as f:
                planner_cfg = json.load(f)
            for k in ("amap_key", "qweather_key", "user_name"):
                if planner_cfg.get(k) and not config.get(k):
                    config[k] = planner_cfg[k]
            log("已自动读取 fishing-trip-planner 配置", "OK")
        except Exception:
            pass

    # 3. 自身配置文件 (最高优先级)
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            for k in ("amap_key", "qweather_key", "home_city", "home_coordinates",
                      "search_radius_km", "fish_type", "user_name"):
                if saved.get(k):
                    config[k] = saved[k]
            config["setup_at"] = saved.get("setup_at", "")
        except Exception as e:
            log(f"配置读取异常: {e}", "WARN")

    return config


def save_config(cfg: Dict):
    ensure_dirs()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    os.chmod(CONFIG_FILE, 0o600)
    log(f"配置已保存: {CONFIG_FILE}", "OK")


def setup_wizard():
    """交互式配置向导."""
    print("\n" + "=" * 56)
    print("  🎣 Fishing Hotspot Push - 首次配置向导")
    print("=" * 56)

    config = load_config()

    def status(val, label):
        return f"✅ {label}" if val else f"⚠️  {label} (未设置)"

    print(f"\n  当前配置状态:")
    print(f"    {status(config['amap_key'], '高德地图 API Key')}")
    print(f"    {status(config['qweather_key'], '和风天气 API Key')}")
    print(f"    {status(config['home_city'], '默认城市') or '⚠️  默认城市 (未设置)'}")
    if config.get("setup_at"):
        print(f"    上次配置: {config['setup_at']}")

    # 尝试共享配置
    if FISHING_PLANNER_CONFIG.exists():
        print(f"\n  📎 检测到 fishing-trip-planner 已配置，将共用 API Key")

    # Step 1: 高德 Key
    print("\n  ── ① 高德地图 API Key ──")
    print("  申请地址: https://lbs.amap.com/ → 创建应用 → Web服务")
    amap_key = input(f"  高德 Key [{mask_key(config['amap_key'])}]: ").strip()
    if amap_key:
        config["amap_key"] = amap_key

    # Step 2: 和风 Key
    print("\n  ── ② 和风天气 API Key ──")
    print("  申请地址: https://dev.qweather.com/ → 控制台 → 创建项目")
    qw_key = input(f"  和风 Key [{mask_key(config['qweather_key'])}]: ").strip()
    if qw_key:
        config["qweather_key"] = qw_key

    # Step 3: 默认城市
    print("\n  ── ③ 默认城市/位置 ──")
    print("  你的常驻地，如: 深圳南山、北京朝阳")
    city = input(f"  默认城市 [{config.get('home_city','') or '未设置'}]: ").strip()
    if city:
        config["home_city"] = city
        # 尝试地理编码
        if config["amap_key"]:
            coords = amap_geocode(config, city)
            if coords:
                config["home_coordinates"] = [coords[0], coords[1]]
                log(f"已定位: {coords[2]} ({coords[0]:.4f}, {coords[1]:.4f})", "OK")

    # Step 4: 搜索半径
    print("\n  ── ④ 搜索半径 ──")
    print("  多大范围内搜索钓点？(10-200km)")
    radius = input(f"  搜索半径(km) [{config.get('search_radius_km', 50)}]: ").strip()
    if radius and radius.isdigit():
        config["search_radius_km"] = int(radius)

    # Step 5: 鱼种偏好
    print("\n  ── ⑤ 偏好鱼种 (可选) ──")
    print("  淡水 / 海水 / 不限")
    fish = input(f"  偏好 [{config.get('fish_type', '不限')}]: ").strip()
    if fish:
        config["fish_type"] = fish

    # Step 6: 称呼
    print("\n  ── ⑥ 你的称呼 (可选) ──")
    name = input(f"  如何称呼你 [{config.get('user_name','') or '钓友'}]: ").strip()
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
                timeout=8
            )
            qw_ok = resp.json().get("code") == "200"
        except:
            pass
    print(f"    和风天气: {'✅ 通过' if qw_ok else '❌ 失败' if config['qweather_key'] else '⏭️ 跳过'}")

    save_config(config)

    print("\n  🎉 配置完成！")
    print('    python hotspot_push.py --run --city "深圳"')
    if not config.get("home_city"):
        print('    或先设置默认城市: python hotspot_push.py --setup')
    print()
    return config


def check_keys(config: Dict) -> bool:
    ok = True
    if not config.get("amap_key"):
        log("未配置高德地图 API Key", "ERR")
        ok = False
    if not config.get("qweather_key"):
        log("未配置和风天气 API Key", "WARN")
    return ok


# ─── 高德地图 API ─────────────────────────────────────────────

def amap_geocode(config: Dict, address: str, city: str = "") -> Optional[Tuple[float, float, str]]:
    """地理编码: 地名→坐标 (lon, lat, name)."""
    log(f"地理编码: {address}", "API")
    params = {"key": config["amap_key"], "address": address}
    if city:
        params["city"] = city
    try:
        resp = requests.get(f"{AMAP_BASE}/geocode/geo", params=params, timeout=10)
        data = resp.json()
        if data.get("status") == "1" and data.get("geocodes"):
            gc = data["geocodes"][0]
            lon, lat = gc["location"].split(",")
            return float(lon), float(lat), gc.get("formatted_address", address)
    except Exception as e:
        log(f"地理编码失败: {e}", "WARN")
    return None


def amap_poi_search(config: Dict, keywords: str, city: str,
                    location: str = "", radius: int = 50000,
                    page: int = 1, types: str = "") -> List[Dict]:
    """高德POI搜索."""
    log(f"POI搜索: {keywords} @ {city}", "API")
    params = {
        "key": config["amap_key"],
        "keywords": keywords,
        "city": city,
        "offset": 20,
        "page": page,
        "extensions": "all",
    }
    if location:
        params["location"] = location
    if radius:
        params["radius"] = radius
    if types:
        params["types"] = types

    try:
        resp = requests.get(f"{AMAP_BASE}/place/text", params=params, timeout=10)
        data = resp.json()
        if data.get("status") == "1":
            return data.get("pois", [])
    except Exception as e:
        log(f"POI搜索失败: {e}", "WARN")
    return []


def amap_around_search(config: Dict, location: str, keywords: str,
                       radius: int = 50000) -> List[Dict]:
    """高德周边搜索."""
    log(f"周边搜索: {keywords} (半径{radius}m)", "API")
    params = {
        "key": config["amap_key"],
        "location": location,
        "keywords": keywords,
        "radius": radius,
        "offset": 25,
        "extensions": "all",
    }
    try:
        resp = requests.get(f"{AMAP_BASE}/place/around", params=params, timeout=10)
        data = resp.json()
        if data.get("status") == "1":
            return data.get("pois", [])
    except Exception as e:
        log(f"周边搜索失败: {e}", "WARN")
    return []


# ─── 和风天气 API ─────────────────────────────────────────────

def qweather_city_lookup(config: Dict, location: str) -> Optional[Tuple[str, float, float]]:
    """城市搜索, 返回 (location_id, lon, lat)."""
    log(f"城市搜索: {location}", "API")
    key = config.get("qweather_key", "")
    params = {"location": location}
    if key:
        params["key"] = key
    try:
        resp = requests.get(f"{QWEATHER_GEO}/city/lookup", params=params, timeout=10)
        data = resp.json()
        if data.get("code") == "200" and data.get("location"):
            loc = data["location"][0]
            return loc["id"], float(loc.get("lon", 0)), float(loc.get("lat", 0))
    except Exception as e:
        log(f"城市搜索失败: {e}", "WARN")
    return None


def qweather_fishing_index(config: Dict, location_id: str) -> Optional[Dict]:
    """钓鱼指数."""
    log("获取钓鱼指数", "API")
    try:
        resp = requests.get(f"{QWEATHER_BASE}/indices/1d",
                           params={"location": location_id, "type": "1"},
                           headers={"Authorization": f"Bearer {config.get('qweather_key', '')}"},
                           timeout=10)
        data = resp.json()
        if data.get("code") == "200" and data.get("daily"):
            return data["daily"][0]
    except Exception as e:
        log(f"钓鱼指数查询失败: {e}", "WARN")
    return None


def qweather_7d(config: Dict, location_id: str) -> Optional[List[Dict]]:
    """7天天气预报."""
    log("获取7天预报", "API")
    try:
        resp = requests.get(f"{QWEATHER_BASE}/weather/7d",
                           params={"location": location_id},
                           headers={"Authorization": f"Bearer {config.get('qweather_key', '')}"},
                           timeout=10)
        data = resp.json()
        if data.get("code") == "200":
            return data.get("daily", [])
    except Exception as e:
        log(f"天气查询失败: {e}", "WARN")
    return None


# ─── NLP 信息提取 ─────────────────────────────────────────────

def nlp_extract_hotspots(text: str, known_city: str = "") -> List[Dict]:
    """
    从非结构化文本中提取钓鱼热点情报。
    返回: [{"location": "钓点名", "coordinates": None, "fish_species": [...],
            "sentiment": "positive/negative/neutral", "catch_quality": 0-10,
            "bait": [], "summary": "...", "source": "text"}]
    """
    if not text or len(text) < 10:
        return []

    hotspots = []
    log(f"NLP分析文本: {len(text)}字符", "NLP")

    # 按句子/段落分割
    segments = re.split(r"[。！？\n；;]+", text)
    segments = [s.strip() for s in segments if len(s.strip()) > 8]

    for seg in segments:
        info = _analyze_segment(seg, known_city)
        if info and info.get("location"):
            hotspots.append(info)

    # 去重（相同钓点合并）
    merged = _merge_hotspots(hotspots)
    log(f"提取到 {len(merged)} 个钓点情报", "NLP")
    return merged


def _analyze_segment(text: str, fallback_city: str) -> Optional[Dict]:
    """分析单个文本段."""
    # 情感分析
    pos_count = sum(1 for w in SENTIMENT_POSITIVE if w in text)
    neg_count = sum(1 for w in SENTIMENT_NEGATIVE if w in text)

    if pos_count > neg_count:
        sentiment = "positive"
        catch_quality = min(10, 5 + pos_count * 2)
    elif neg_count > pos_count:
        sentiment = "negative"
        catch_quality = max(1, 5 - neg_count * 2)
    else:
        sentiment = "neutral"
        catch_quality = 5

    # 鱼种提取
    species = [s for s in FISH_SPECIES if s in text]

    # 饵料提取
    baits = [b for b in FISH_BAITS if b in text]

    # 钓点提取 - 尝试匹配地名模式
    location = _extract_location(text, fallback_city)

    if not location and not species:
        return None

    return {
        "location": location or fallback_city,
        "coordinates": None,
        "fish_species": list(set(species)),
        "sentiment": sentiment,
        "catch_quality": catch_quality,
        "bait": list(set(baits)),
        "summary": text[:120],
        "source": "social",
    }


def _extract_location(text: str, fallback: str) -> Optional[str]:
    """从文本中提取地名."""
    # 常见地名模式
    patterns = [
        # "在XX钓的"
        r"在([\u4e00-\u9fff]{2,6}(?:水库|湖|河|湾|塘|坑|江|海|岛|码头|港|钓场|垂钓园|湿地|潭|溪|浜|荡|浦))",
        # "去了XX"
        r"(?:去了|到达|来到)([\u4e00-\u9fff]{2,10})",
        # "XX钓点"
        r"([\u4e00-\u9fff]{2,6})钓点",
        # "XX附近"
        r"([\u4e00-\u9fff]{2,6})附近",
        # 纯地名 + 水域后缀
        r"([\u4e00-\u9fff]{2,4}(?:水库|湖|河|湾|塘|坑|江|海|钓场))",
    ]

    for pat in patterns:
        m = re.search(pat, text)
        if m:
            return m.group(1)

    return None


def _merge_hotspots(hotspots: List[Dict]) -> List[Dict]:
    """合并相同钓点的情报."""
    groups = defaultdict(list)
    for h in hotspots:
        key = h.get("location", "未知")
        groups[key].append(h)

    merged = []
    for loc, items in groups.items():
        all_species = list(set(s for item in items for s in item.get("fish_species", [])))
        all_baits = list(set(b for item in items for b in item.get("bait", [])))
        avg_quality = sum(i.get("catch_quality", 5) for i in items) / len(items)
        sentiment_counts = defaultdict(int)
        for i in items:
            sentiment_counts[i.get("sentiment", "neutral")] += 1
        dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)

        merged.append({
            "location": loc,
            "coordinates": items[0].get("coordinates"),
            "fish_species": all_species,
            "sentiment": dominant_sentiment,
            "catch_quality": round(avg_quality, 1),
            "bait": all_baits,
            "summary": items[0].get("summary", ""),
            "source": "social",
            "mention_count": len(items),
        })

    return merged


# ─── 距离计算 ─────────────────────────────────────────────────

def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """计算两点间距离 (km)."""
    from math import radians, cos, sin, asin, sqrt
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * asin(sqrt(a)) * 6371


# ─── 评分与排序 ───────────────────────────────────────────────

def score_hotspot(hotspot: Dict, user_lon: float, user_lat: float,
                  weather_daily: List[Dict], user_radius: int) -> Dict:
    """
    综合评分:
    - 距离分: 越近越高 (0-30)
    - 鱼获分: 基于NLP提取 (0-35)
    - 天气分: 基于和风天气 (0-25)
    - 时效分: 基于提及频率 (0-10)
    """
    score = 0
    details = {}

    # 1. 距离评分 (0-30)
    h_lon = hotspot.get("lon")
    h_lat = hotspot.get("lat")
    if h_lon and h_lat and user_lon and user_lat:
        dist = haversine(user_lon, user_lat, h_lon, h_lat)
        hotspot["distance_km"] = round(dist, 1)
        if dist <= 10:
            dist_score = 30
        elif dist <= 30:
            dist_score = 25
        elif dist <= 50:
            dist_score = 18
        elif dist <= 100:
            dist_score = 10
        elif dist <= 200:
            dist_score = 5
        else:
            dist_score = 2
    else:
        dist_score = 0
        hotspot["distance_km"] = None
    score += dist_score
    details["距离"] = dist_score

    # 2. 鱼获质量评分 (0-35)
    catch_q = hotspot.get("catch_quality", 5)
    mention_bonus = min(5, hotspot.get("mention_count", 1) * 2)
    catch_score = int(catch_q * 3 + mention_bonus)
    catch_score = min(35, catch_score)
    score += catch_score
    details["鱼获情报"] = catch_score

    # 3. 天气评分 (0-25)
    weather_score = 10  # 基础分
    if weather_daily:
        today = weather_daily[0]
        # 温度
        temp = int(today.get("tempMax", 25) or 25)
        if 15 <= temp <= 28:
            weather_score += 5
        elif 5 <= temp <= 35:
            weather_score += 2
        else:
            weather_score -= 3
        # 风力
        wind = int(today.get("windScaleDay", 3) or 3)
        if wind <= 2:
            weather_score += 5
        elif wind <= 4:
            weather_score += 3
        elif wind <= 6:
            weather_score += 0
        else:
            weather_score -= 5
        # 降水
        precip = float(today.get("precip", 0) or 0)
        if precip <= 0.5:
            weather_score += 5
        elif precip <= 5:
            weather_score += 0
        else:
            weather_score -= 5
    weather_score = max(0, min(25, weather_score))
    score += weather_score
    details["天气条件"] = weather_score

    # 4. 时效/热度评分 (0-10)
    freshness = min(10, hotspot.get("mention_count", 1) * 3)
    score += freshness
    details["情报热度"] = freshness

    # 综合评定
    total = min(100, score)
    if total >= 80:
        level, color, emoji = "强烈推荐", "#22c55e", "🔥"
    elif total >= 60:
        level, color, emoji = "推荐", "#3b82f6", "👍"
    elif total >= 40:
        level, color, emoji = "一般", "#f59e0b", "🤔"
    else:
        level, color, emoji = "暂不推荐", "#ef4444", "⚠️"

    hotspot["score"] = total
    hotspot["level"] = level
    hotspot["level_color"] = color
    hotspot["level_emoji"] = emoji
    hotspot["score_details"] = details

    return hotspot


# ─── HTML 报告生成 ─────────────────────────────────────────────

def generate_html(city: str, hotspots: List[Dict], weather_daily: List[Dict],
                  fishing_index: Optional[Dict], user_coords: Tuple[float, float],
                  user_name: str, search_radius: int, text_input: str = "") -> str:
    """生成HTML热点推送报告."""

    # ── 天气卡片 ──
    weather_cards = ""
    for i, day in enumerate(weather_daily[:5] or []):
        date = day.get("fxDate", "")
        text_day = day.get("textDay", "?")
        temp_high = day.get("tempMax", "?")
        temp_low = day.get("tempMin", "?")
        wind = day.get("windScaleDay", "?")
        emoji = WEATHER_EMOJI.get(text_day, "🌤️")
        active = "active" if i == 0 else ""
        weather_cards += f"""
        <div class="weather-card {active}">
          <div class="wc-date">{date[-5:] if len(date)>=10 else date}</div>
          <div class="wc-icon">{emoji}</div>
          <div class="wc-text">{text_day}</div>
          <div class="wc-temp">{temp_low}° / <b>{temp_high}°</b></div>
          <div class="wc-detail">🌬️ {wind}级</div>
        </div>"""

    # ── 钓鱼指数 ──
    fi_html = ""
    if fishing_index:
        fi_cat = fishing_index.get("category", "?")
        fi_text = fishing_index.get("text", "")
        fi_level = fishing_index.get("level", "2")
        fi_colors = {"1": "#22c55e", "2": "#3b82f6", "3": "#f59e0b", "4": "#ef4444"}
        fi_color = fi_colors.get(fi_level, "#94a3b8")
        fi_html = f"""
        <div class="fishing-index" style="border-color:{fi_color};">
          <span class="fi-badge" style="background:{fi_color};">{fi_cat}</span>
          <span class="fi-text">{fi_text}</span>
        </div>"""

    # ── 热点卡片 ──
    hotspot_cards = ""
    if hotspots:
        for i, h in enumerate(hotspots[:10]):
            rank_emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"][i]

            # 鱼种标签
            species_tags = ""
            for s in h.get("fish_species", [])[:4]:
                species_tags += f'<span class="species-tag">🐟 {s}</span>'

            # 饵料标签
            bait_tags = ""
            for b in h.get("bait", [])[:3]:
                bait_tags += f'<span class="bait-tag">🪱 {b}</span>'

            # 距离显示
            dist_km = h.get("distance_km")
            dist_str = f"{dist_km}km" if dist_km else "距离未知"

            # 情感标识
            sent_map = {"positive": "🟢", "negative": "🔴", "neutral": "🟡"}
            sent_emoji = sent_map.get(h.get("sentiment", "neutral"), "🟡")

            # 评分条
            score = h.get("score", 50)
            score_color = h.get("level_color", "#3b82f6")

            # 社交来源摘要
            social_badge = ""
            if h.get("source") == "social":
                mention = h.get("mention_count", 1)
                social_badge = f'<span class="social-badge">📱 {mention}条情报</span>'

            hotspot_cards += f"""
            <div class="hotspot-card">
              <div class="hc-rank">{rank_emoji}</div>
              <div class="hc-body">
                <div class="hc-header">
                  <h3>{h.get('location', '未知钓点')}</h3>
                  <div class="hc-level" style="color:{score_color};">{h.get('level_emoji','')} {h.get('level','')}</div>
                </div>
                <div class="hc-meta">
                  <span>📍 {dist_str}</span>
                  <span>{sent_emoji} 鱼情: {h.get('sentiment','neutral')}</span>
                  {social_badge}
                </div>
                <div class="hc-score-bar">
                  <div class="score-fill" style="width:{score}%; background:{score_color};"></div>
                </div>
                <div class="hc-score-text">综合评分: <b style="color:{score_color};">{score}/100</b></div>
                <div class="hc-tags">
                  {species_tags}
                  {bait_tags}
                </div>
                <div class="hc-actions">
                  <a class="btn-plan" href="#">🗺️ 生成行程规划</a>
                  <a class="btn-nav" href="https://uri.amap.com/navigation?to={h.get('lon','')},{h.get('lat','')},{h.get('location','')}" target="_blank">🧭 导航前往</a>
                </div>
              </div>
            </div>"""

    if not hotspot_cards:
        hotspot_cards = """
        <div class="empty-state">
          <div class="empty-icon">🎣</div>
          <h3>暂无热点数据</h3>
          <p>可能是以下原因：</p>
          <ul>
            <li>搜索范围内暂无钓点情报</li>
            <li>可尝试扩大搜索半径</li>
            <li>或手动指定城市: --city "城市名"</li>
          </ul>
        </div>"""

    # ── 数据来源信息 ──
    text_badge = "✅ 已分析社交媒体情报" if text_input else "⚠️ 仅API数据，建议补充社交媒体搜索"
    text_len = f"({len(text_input)}字符)" if text_input else ""

    display_name = user_name or "钓友"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>钓鱼热点推送 - {city}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
  background: linear-gradient(135deg, #0a1628 0%, #1a2744 40%, #0d2137 100%);
  color: #e2e8f0;
  min-height: 100vh;
  padding: 20px;
}}
.container {{ max-width: 800px; margin: 0 auto; }}

/* 头部 */
.header {{
  text-align: center;
  padding: 40px 20px 30px;
  position: relative;
}}
.header::after {{
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #60a5fa, #34d399);
  border-radius: 2px;
}}
.header h1 {{
  font-size: 2em;
  background: linear-gradient(135deg, #60a5fa 0%, #34d399 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 8px;
}}
.header .location {{
  font-size: 1.3em;
  color: #94a3b8;
  margin: 8px 0;
}}
.header .location span {{ color: #60a5fa; font-weight: 700; }}
.header .meta {{
  color: #64748b;
  font-size: 0.9em;
  margin-top: 8px;
}}

/* 钓鱼指数 */
.fishing-index {{
  background: rgba(30, 41, 59, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid;
  border-radius: 12px;
  padding: 14px 20px;
  margin: 16px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}}
.fi-badge {{
  padding: 3px 12px;
  border-radius: 12px;
  color: #fff;
  font-weight: 700;
  font-size: 0.9em;
}}
.fi-text {{ color: #94a3b8; font-size: 0.9em; }}

/* 天气卡片 */
.weather-strip {{
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding: 8px 0 16px;
  scrollbar-width: thin;
}}
.weather-card {{
  min-width: 95px;
  text-align: center;
  padding: 12px 8px;
  background: rgba(15, 23, 42, 0.6);
  border-radius: 12px;
  border: 2px solid transparent;
  flex-shrink: 0;
}}
.weather-card.active {{
  border-color: #60a5fa;
  background: rgba(96, 165, 250, 0.08);
}}
.wc-date {{ font-size: 0.8em; color: #64748b; }}
.wc-icon {{ font-size: 1.5em; margin: 4px 0; }}
.wc-text {{ font-size: 0.85em; font-weight: 600; }}
.wc-temp {{ font-size: 0.85em; margin: 2px 0; color: #94a3b8; }}
.wc-detail {{ font-size: 0.75em; color: #475569; }}

/* 区域标题 */
.section-title {{
  font-size: 1.1em;
  color: #93c5fd;
  margin: 24px 0 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}}
.section-title .count {{
  font-size: 0.8em;
  color: #64748b;
  background: rgba(100, 116, 139, 0.15);
  padding: 2px 10px;
  border-radius: 10px;
}}

/* 热点卡片 */
.hotspot-card {{
  background: rgba(30, 41, 59, 0.75);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 20px;
  margin: 12px 0;
  border: 1px solid rgba(100, 116, 139, 0.2);
  display: flex;
  gap: 16px;
  transition: transform 0.2s, border-color 0.2s;
}}
.hotspot-card:hover {{
  border-color: rgba(96, 165, 250, 0.4);
  transform: translateY(-2px);
}}
.hc-rank {{
  font-size: 1.8em;
  flex-shrink: 0;
  width: 48px;
  text-align: center;
  line-height: 1.4;
}}
.hc-body {{ flex: 1; min-width: 0; }}
.hc-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}}
.hc-header h3 {{
  font-size: 1.15em;
  color: #e2e8f0;
}}
.hc-level {{
  font-size: 0.85em;
  font-weight: 700;
}}
.hc-meta {{
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin: 6px 0;
  font-size: 0.85em;
  color: #94a3b8;
}}
.hc-score-bar {{
  height: 6px;
  background: rgba(100, 116, 139, 0.2);
  border-radius: 3px;
  margin: 10px 0 4px;
  overflow: hidden;
}}
.score-fill {{
  height: 100%;
  border-radius: 3px;
  transition: width 0.8s ease;
}}
.hc-score-text {{
  font-size: 0.85em;
  color: #64748b;
  margin-bottom: 8px;
}}
.hc-tags {{
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
}}
.species-tag {{
  font-size: 0.8em;
  padding: 2px 10px;
  background: rgba(34, 197, 94, 0.12);
  color: #4ade80;
  border-radius: 10px;
}}
.bait-tag {{
  font-size: 0.8em;
  padding: 2px 10px;
  background: rgba(245, 158, 11, 0.12);
  color: #fbbf24;
  border-radius: 10px;
}}
.social-badge {{
  font-size: 0.8em;
  padding: 2px 8px;
  background: rgba(139, 92, 246, 0.12);
  color: #a78bfa;
  border-radius: 8px;
}}
.hc-actions {{
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}}
.btn-plan, .btn-nav {{
  font-size: 0.85em;
  padding: 6px 16px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: opacity 0.2s;
}}
.btn-plan {{
  background: rgba(96, 165, 250, 0.15);
  color: #60a5fa;
  border: 1px solid rgba(96, 165, 250, 0.3);
}}
.btn-nav {{
  background: rgba(34, 197, 94, 0.1);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.25);
}}
.btn-plan:hover, .btn-nav:hover {{ opacity: 0.8; }}

/* 空状态 */
.empty-state {{
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
}}
.empty-icon {{ font-size: 4em; margin-bottom: 16px; }}
.empty-state h3 {{ color: #94a3b8; margin-bottom: 12px; }}
.empty-state ul {{
  list-style: none;
  padding: 0;
  font-size: 0.9em;
  line-height: 2;
}}

/* 信息栏 */
.info-bar {{
  background: rgba(30, 41, 59, 0.6);
  border-radius: 10px;
  padding: 10px 16px;
  margin: 16px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 0.8em;
  color: #64748b;
}}
.info-bar .status {{ color: #4ade80; }}

/* 底部 */
.footer {{
  text-align: center;
  padding: 30px 20px;
  color: #475569;
  font-size: 0.8em;
}}
.footer p {{ margin: 4px 0; }}

@media (max-width: 600px) {{
  .hotspot-card {{ flex-direction: column; }}
  .hc-rank {{ width: 100%; text-align: left; font-size: 1.2em; }}
  .header h1 {{ font-size: 1.5em; }}
}}
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <h1>🎣 钓鱼热点情报</h1>
    <div class="location">📍 <span>{city}</span> · 半径 {search_radius}km</div>
    <div class="meta">{datetime.now().strftime("%Y-%m-%d %H:%M")} 更新 · 你好，{display_name}！</div>
  </div>

  {fi_html}

  <div class="weather-strip">
    {weather_cards}
  </div>

  <div class="section-title">
    🔥 热点钓点 <span class="count">Top {min(len(hotspots or []), 10)}</span>
  </div>

  {hotspot_cards}

  <div class="info-bar">
    <span>🌐 数据源: 和风天气 + 高德地图</span>
    <span class="status">{text_badge} {text_len}</span>
  </div>

  <div class="footer">
    <p>数据来源: 和风天气 · 高德地图 | 情报仅供参考</p>
    <p>与 <strong>fishing-trip-planner</strong> 联动: 点击「生成行程规划」获得完整出行方案</p>
    <p>Fish On! 🎣 | powered by Fishing Hotspot Push v1.0</p>
  </div>

</div>
</body>
</html>"""

    return html


# ─── 历史记录管理 ─────────────────────────────────────────────

def load_push_index() -> List[Dict]:
    if PUSH_INDEX.exists():
        try:
            with open(PUSH_INDEX, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return []


def save_push_index(pushes: List[Dict]):
    ensure_dirs()
    with open(PUSH_INDEX, "w", encoding="utf-8") as f:
        json.dump(pushes, f, indent=2, ensure_ascii=False)


def save_report(push_id: str, html_content: str, metadata: Dict) -> str:
    ensure_dirs()
    report_path = REPORTS_DIR / f"{push_id}.html"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    pushes = load_push_index()
    pushes.append(metadata)
    save_push_index(pushes)
    log(f"报告已存档: {push_id}", "OK")
    return str(report_path)


def show_history(limit: int = 20):
    pushes = load_push_index()
    if not pushes:
        print("\n📭 暂无推送历史记录")
        return

    pushes.sort(key=lambda t: t.get("created_at", ""), reverse=True)
    pushes = pushes[:limit]

    print(f"\n{'='*68}")
    print(f"  📋 钓鱼热点推送历史 (共 {len(load_push_index())} 条)")
    print(f"{'='*68}")

    for i, p in enumerate(pushes, 1):
        pid = p.get("id", "?")
        created = p.get("created_at", "")[:16]
        city = p.get("city", "?")
        count = p.get("hotspot_count", 0)

        print(f"\n  [{i}] {pid[:12]}")
        print(f"      {created}  📍 {city}  🔥 {count}个热点")

    print(f"\n{'─'*68}")
    print(f"  查看报告: python hotspot_push.py --view <序号或ID>")
    print()


def view_report(ref: str):
    pushes = load_push_index()
    match = None
    try:
        idx = int(ref) - 1
        pushes.sort(key=lambda t: t.get("created_at", ""), reverse=True)
        if 0 <= idx < len(pushes):
            match = pushes[idx]
    except ValueError:
        for p in pushes:
            if p.get("id", "").startswith(ref):
                match = p
                break

    if not match:
        log(f"未找到报告: {ref}", "ERR")
        show_history()
        return

    report_path = REPORTS_DIR / f"{match['id']}.html"
    if not report_path.exists():
        log(f"报告文件不存在: {report_path}", "ERR")
        return

    print(f"\n✅ 打开报告: {match['id']}")
    print(f"   {match.get('city', '?')} | {match.get('created_at', '')}")
    print(f"   {report_path}")


# ─── 主流程 ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="🎣 钓鱼热点推送 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python hotspot_push.py --setup                      # 首次配置
  python hotspot_push.py --run --city "深圳"           # 指定城市
  python hotspot_push.py --run --input "搜索文本..."    # 传入外部情报
  python hotspot_push.py --history                     # 查看历史
  python hotspot_push.py --view 1                      # 查看历史报告
        """
    )

    action = parser.add_mutually_exclusive_group()
    action.add_argument("--setup", "-S", action="store_true", help="运行配置向导")
    action.add_argument("--history", "-H", action="store_true", help="查看推送历史")
    action.add_argument("--view", "-V", type=str, metavar="ID", help="查看历史报告")

    parser.add_argument("--run", "-R", action="store_true", help="执行热点分析")
    parser.add_argument("--city", "-c", help="目标城市 (如: 深圳)")
    parser.add_argument("--input", "-i", help="外部文本情报 (社交媒体搜索结果)")
    parser.add_argument("--input-file", "-f", help="从文件读取文本情报")
    parser.add_argument("--radius", "-r", type=int, help="搜索半径(km)，覆盖配置")
    parser.add_argument("--output", "-O", help="输出HTML文件路径")

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
        view_report(args.view)
        return

    # ── 模式: 热点分析 ──
    if args.run:
        print("\n🎣 钓鱼热点推送 v1.0\n", file=sys.stderr)

        if not check_keys(config):
            print("\n💡 请先配置: python hotspot_push.py --setup", file=sys.stderr)
            sys.exit(1)

        # 确定目标城市
        city = args.city or config.get("home_city", "")
        if not city:
            city = input("请输入目标城市 (如: 深圳): ").strip()
            if not city:
                log("未指定城市", "ERR")
                sys.exit(1)

        radius = args.radius or config.get("search_radius_km", 50)

        print(f"  📍 目标城市: {city} | 搜索半径: {radius}km\n", file=sys.stderr)

        # 1. 城市坐标定位
        city_coords = amap_geocode(config, city)
        if not city_coords:
            log(f"无法定位城市: {city}", "ERR")
            sys.exit(1)
        user_lon, user_lat, city_name = city_coords
        log(f"城市坐标: {city_name} ({user_lon:.4f}, {user_lat:.4f})", "OK")

        # 2. 和风天气 (钓鱼指数 + 天气预报)
        qw_info = qweather_city_lookup(config, city)
        fishing_index = None
        weather_daily = []
        if qw_info:
            qw_id = qw_info[0]
            fishing_index = qweather_fishing_index(config, qw_id)
            weather_daily = qweather_7d(config, qw_id) or []

        # 3. 高德周边水域/钓场搜索
        user_loc_str = f"{user_lon},{user_lat}"
        radius_m = radius * 1000

        all_pois = []
        for kw in ["钓鱼", "水库", "湖泊", "钓场", "垂钓"]:
            pois = amap_around_search(config, user_loc_str, kw, radius_m)
            all_pois.extend(pois)

        # 去重
        seen = set()
        unique_pois = []
        for p in all_pois:
            pid = p.get("id") or p.get("name")
            if pid not in seen:
                seen.add(pid)
                unique_pois.append(p)

        log(f"周边搜索: {len(unique_pois)}个水域/钓场", "OK")

        # 4. NLP 提取社交媒体情报
        text_input = ""
        if args.input_file:
            try:
                with open(args.input_file, "r", encoding="utf-8") as f:
                    text_input = f.read()
                log(f"读取输入文件: {len(text_input)}字符", "OK")
            except Exception as e:
                log(f"读取文件失败: {e}", "WARN")
        elif args.input:
            text_input = args.input
            log(f"接收文本输入: {len(text_input)}字符", "OK")

        social_hotspots = nlp_extract_hotspots(text_input, city) if text_input else []
        log(f"社交情报: {len(social_hotspots)}个钓点", "NLP")

        # 5. 整合POI + 社交情报
        hotspots = []

        # POI 数据转换为热点格式
        for p in unique_pois:
            pname = p.get("name", "")
            ploc = p.get("location", "")
            if ploc:
                plon, plat = ploc.split(",")
                dist = haversine(user_lon, user_lat, float(plon), float(plat))
                if dist <= radius:
                    hotspots.append({
                        "location": pname,
                        "lon": float(plon),
                        "lat": float(plat),
                        "address": p.get("address", ""),
                        "type": p.get("type", ""),
                        "fish_species": [],
                        "sentiment": "neutral",
                        "catch_quality": 5,
                        "bait": [],
                        "summary": p.get("address", ""),
                        "source": "poi",
                        "mention_count": 1,
                    })

        # 社交情报匹配坐标
        for sh in social_hotspots:
            sloc = sh.get("location", "")
            if sloc:
                coord = amap_geocode(config, sloc, city)
                if coord:
                    sh["lon"], sh["lat"], _ = coord
                else:
                    sh["lat"], sh["lon"] = None, None
            hotspots.append(sh)

        # 6. 评分排序
        for h in hotspots:
            score_hotspot(h, user_lon, user_lat, weather_daily, radius)

        hotspots.sort(key=lambda x: x.get("score", 0), reverse=True)
        log(f"最终热点: {len(hotspots)}个", "OK")

        # 打印排名
        for i, h in enumerate(hotspots[:5]):
            s = h.get("score", 0)
            print(f"  {['🥇','🥈','🥉','4','5'][i]} {h['location']} - {s}/100 {h.get('level','')} "
                  f"({h.get('distance_km','?')}km)", file=sys.stderr)

        # 7. 生成HTML报告
        html = generate_html(
            city=city_name,
            hotspots=hotspots,
            weather_daily=weather_daily,
            fishing_index=fishing_index,
            user_coords=(user_lon, user_lat),
            user_name=config.get("user_name", ""),
            search_radius=radius,
            text_input=text_input,
        )

        # 8. 保存
        push_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        if args.output:
            output_path = os.path.abspath(args.output)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html)
            log(f"报告已保存: {output_path}", "OK")
        else:
            output_path = save_report(
                push_id=push_id,
                html_content=html,
                metadata={
                    "id": push_id,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "city": city_name,
                    "hotspot_count": len(hotspots),
                    "social_sources": len(social_hotspots),
                    "poi_sources": len(unique_pois),
                    "radius_km": radius,
                }
            )

        print(f"\n✅ 报告已生成: {output_path}", file=sys.stderr)
        print(f"🔥 发现 {len(hotspots)} 个钓点", file=sys.stderr)
        print(f"\n💡 查看历史: python hotspot_push.py --history", file=sys.stderr)
        print(output_path)
        return

    # ── 无参数 ──
    parser.print_help()
    print("\n💡 快速开始:")
    print("  python hotspot_push.py --setup")
    print('  python hotspot_push.py --run --city "深圳"')


if __name__ == "__main__":
    main()
