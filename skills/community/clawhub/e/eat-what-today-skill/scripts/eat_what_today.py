import argparse
import json
import random
import re
from datetime import datetime
from pathlib import Path

PRICE_ORDER = {"low": 1, "mid": 2, "high": 3}

WEATHER_KEYWORDS = {
    "rainy": ["雨", "下雨", "阴", "潮", "潮湿", "回南天"],
    "cold": ["冷", "寒", "降温", "冬"],
    "hot": ["热", "炎热", "高温", "夏"],
    "sunny": ["晴", "太阳", "阳光"],
    "windy": ["风", "刮风", "大风"],
}

MOOD_KEYWORDS = {
    "happy": ["开心", "高兴", "愉快"],
    "tired": ["累", "疲惫", "困", "没精神"],
    "comfort": ["治愈", "安慰", "暖", "想吃点热乎"],
    "focused": ["效率", "专注", "工作", "赶ddl", "学习"],
    "adventurous": ["新鲜", "尝试", "刺激", "重口"],
    "light": ["清淡", "轻食", "少油", "少盐"],
    "party": ["聚会", "朋友", "热闹"],
    "healthy": ["健康", "减脂", "控卡", "养生"],
}

MODE_KEYWORDS = {
    "takeaway": ["外卖", "懒得出门", "送到", "快点"],
    "dine_in": ["堂食", "出去吃", "餐厅", "下馆子"],
    "cook": ["自己做", "下厨", "做饭", "家里做"],
}

SPICY_KEYWORDS = {
    "high": ["辣", "重辣", "爆辣", "无辣不欢"],
    "mid": ["小辣", "中辣", "辣一点", "有点辣"],
    "low": ["不辣", "微辣", "清淡"],
}

BUDGET_KEYWORDS = {
    "low": ["便宜", "省钱", "预算低", "20以内", "30以内"],
    "mid": ["一般预算", "正常预算", "40以内", "50以内"],
    "high": ["预算高", "想吃好点", "贵点没关系", "100以内"],
}

CITY_TAG_KEYWORDS = {
    "north": [
        "北京", "天津", "河北", "山东", "东北", "西安", "郑州", "太原", "沈阳", "大连", "哈尔滨", "长春", "青岛", "济南",
    ],
    "south": [
        "广州", "深圳", "珠海", "厦门", "福州", "长沙", "南方", "重庆", "成都", "昆明", "贵阳", "南宁", "武汉", "杭州", "南京", "苏州", "上海",
    ],
    "guangdong": ["广东", "广州", "深圳", "佛山", "东莞", "珠海", "中山", "惠州"],
    "hainan": ["海南", "海口", "三亚"],
    "hunan": ["湖南", "长沙", "株洲", "湘潭", "岳阳", "常德", "衡阳"],
}

TIME_ALIAS = {
    6: "breakfast",
    7: "breakfast",
    8: "breakfast",
    9: "breakfast",
    10: "lunch",
    11: "lunch",
    12: "lunch",
    13: "lunch",
    14: "lunch",
    15: "dinner",
    16: "dinner",
    17: "dinner",
    18: "dinner",
    19: "dinner",
    20: "late_night",
    21: "late_night",
    22: "late_night",
    23: "late_night",
    0: "late_night",
    1: "late_night",
}

STYLE_KEYWORDS = {
    "noodle": ["面", "粉", "米线", "拉面", "小面", "馄饨"],
    "rice": ["饭", "盖码", "卤肉", "丼"],
    "hotpot": ["火锅", "麻辣烫", "麻辣香锅", "砂锅"],
    "snack": ["饺", "饼", "锅盔", "臭豆腐", "烧烤"],
    "light": ["粥", "蒸", "肠粉", "寿司"],
}

CUISINE_KEYWORDS = {
    "sichuan": ["川", "麻辣", "重庆", "小面", "水煮", "酸菜鱼", "麻婆"],
    "cantonese": ["粤", "广东", "烧腊", "肠粉", "椰子鸡", "猪肚鸡"],
    "hunan": ["湘", "湖南", "浏阳", "辣椒炒肉", "臭豆腐"],
    "jiangzhe": ["江浙", "上海", "南京", "苏州", "葱油拌面"],
    "northern": ["北方", "北京", "天津", "饺", "锅盔", "凉皮"],
    "japanese": ["日式", "寿司", "拉面", "蛋包饭", "丼"],
    "korean": ["韩式", "炸鸡", "部队火锅", "烤肉"],
}

CUISINE_LABELS = {
    "sichuan": "川渝风味",
    "cantonese": "粤式风味",
    "hunan": "湘味",
    "jiangzhe": "江浙风味",
    "northern": "北方风味",
    "japanese": "日式",
    "korean": "韩式",
}


def _pick_first_match(text, mapping):
    for label, words in mapping.items():
        if any(word in text for word in words):
            return label
    return None


def _normalize_text(text):
    return text.replace(" ", "").lower()


def detect_spicy(text):
    # Handle negation first so "不辣" is not misread as "辣".
    if any(word in text for word in ("不辣", "别辣", "少辣", "微辣", "清淡")):
        return "low"
    if any(word in text for word in SPICY_KEYWORDS["high"]):
        return "high"
    if any(word in text for word in SPICY_KEYWORDS["mid"]):
        return "mid"
    return None


def detect_budget(text):
    hit = re.search(r"(\d{2,3})\s*(元|块|rmb)?", text)
    if not hit:
        return _pick_first_match(text, BUDGET_KEYWORDS) or "mid"
    amount = int(hit.group(1))
    if amount <= 30:
        return "low"
    if amount <= 60:
        return "mid"
    return "high"


def detect_styles(text):
    prefs = []
    for style, words in STYLE_KEYWORDS.items():
        if any(word in text for word in words):
            prefs.append(style)
    return prefs


def detect_cuisines(text):
    prefs = []
    for cuisine, words in CUISINE_KEYWORDS.items():
        if any(word in text for word in words):
            prefs.append(cuisine)
    return prefs


def infer_item_styles(food_name):
    styles = []
    for style, words in STYLE_KEYWORDS.items():
        if any(word in food_name for word in words):
            styles.append(style)
    return styles or ["rice"]


def infer_item_cuisines(food_name, item):
    hits = []
    explicit = item.get("cuisine")
    if isinstance(explicit, str) and explicit:
        hits.append(explicit)
    elif isinstance(explicit, list):
        for cuisine in explicit:
            if cuisine:
                hits.append(cuisine)

    for cuisine, words in CUISINE_KEYWORDS.items():
        if any(word in food_name for word in words):
            hits.append(cuisine)
    if "guangdong" in item.get("city_tags", []):
        hits.append("cantonese")
    if "hunan" in item.get("city_tags", []):
        hits.append("hunan")
    if "north" in item.get("city_tags", []):
        hits.append("northern")
    return list(dict.fromkeys(hits))


def infer_profile(text):
    text = _normalize_text(text)
    now_slot = TIME_ALIAS.get(datetime.now().hour, "dinner")
    profile = {
        "location": None,
        "city_tag": "all",
        "weather": _pick_first_match(text, WEATHER_KEYWORDS) or "all",
        "mood": _pick_first_match(text, MOOD_KEYWORDS) or "neutral",
        "mode": _pick_first_match(text, MODE_KEYWORDS),
        "budget": detect_budget(text),
        "spicy": detect_spicy(text),
        "time_slot": now_slot,
        "styles": detect_styles(text),
        "cuisines": detect_cuisines(text),
        "need_fast": any(word in text for word in ("快", "赶时间", "来不及", "马上")),
    }

    for tag, words in CITY_TAG_KEYWORDS.items():
        hit = next((word for word in words if word in text), None)
        if hit:
            profile["city_tag"] = tag
            profile["location"] = hit
            break

    for marker, slot in [
        ("早餐", "breakfast"),
        ("早饭", "breakfast"),
        ("午饭", "lunch"),
        ("中饭", "lunch"),
        ("晚饭", "dinner"),
        ("晚餐", "dinner"),
        ("夜宵", "late_night"),
    ]:
        if marker in text:
            profile["time_slot"] = slot
            break

    return profile


def merge_overrides(profile, args):
    fields = ["weather", "mood", "mode", "budget", "spicy", "time_slot", "city_tag", "location"]
    for field in fields:
        value = getattr(args, field)
        if value:
            profile[field] = value


def score_item(item, profile):
    score = 0
    reasons = []
    styles = infer_item_styles(item["name"])
    cuisines = infer_item_cuisines(item["name"], item)

    if item["name"] in profile.get("excluded_names", set()):
        return -999, ["命中排除项"], styles, cuisines

    if profile["time_slot"] in item["time_tags"]:
        score += 3
        reasons.append("适合当前时段")
    else:
        score -= 1

    if "all" in item["weather"] or profile["weather"] in item["weather"]:
        score += 2
        reasons.append("匹配天气")

    if profile["mood"] in item["moods"]:
        score += 2
        reasons.append("符合当前心情")

    if profile["mode"]:
        if profile["mode"] in item["modes"]:
            score += 3
            reasons.append("满足就餐方式")
        else:
            score -= 2

    if profile["city_tag"] == "all":
        score += 1
    elif profile["city_tag"] in item["city_tags"]:
        score += 3
        reasons.append("贴合城市偏好")
    elif "all" in item["city_tags"]:
        score += 1
    else:
        score -= 1

    if profile["spicy"]:
        if profile["spicy"] == item["spicy"]:
            score += 2
            reasons.append("辣度匹配")
        else:
            score -= 2

    if PRICE_ORDER[item["price"]] <= PRICE_ORDER[profile["budget"]]:
        score += 2
        reasons.append("预算友好")
    else:
        score -= 3

    if profile["styles"] and any(style in styles for style in profile["styles"]):
        score += 2
        reasons.append("命中想吃类型")

    if profile["cuisines"] and any(c in cuisines for c in profile["cuisines"]):
        score += 2
        reasons.append("命中偏好菜系")

    if profile["need_fast"] and "takeaway" in item["modes"]:
        score += 1
        reasons.append("适合快速下单")

    return score, reasons, styles, cuisines


def build_image_path(food_name, root):
    foods_dir = root / "assets" / "foods_image"
    for ext in ("jpg", "jpeg", "png", "webp"):
        candidate = foods_dir / f"{food_name}.{ext}"
        if candidate.exists():
            # 返回相对于项目根目录的路径，跨平台兼容
            return str(candidate.relative_to(root))
    return ""


def recommend(query, args):
    base = Path(__file__).resolve().parents[1]
    data_file = base / "assets" / "menu_db.json"
    menu = json.loads(data_file.read_text(encoding="utf-8"))

    profile = infer_profile(query)
    merge_overrides(profile, args)

    text = _normalize_text(query)
    profile["excluded_names"] = {item["name"] for item in menu if item["name"] in text and any(k in text for k in ("不吃", "不要", "别", "排除"))}

    ranked = []
    for item in menu:
        score, reasons, styles, cuisines = score_item(item, profile)
        ranked.append((score, item, reasons, styles, cuisines))

    ranked.sort(key=lambda x: x[0], reverse=True)
    top_candidates = [record for record in ranked if record[0] >= 6][:10]
    if not top_candidates:
        top_candidates = ranked[:10]

    picks = []
    used_styles = set()
    for record in top_candidates:
        score, food, reasons, styles, cuisines = record
        primary_style = styles[0] if styles else "rice"
        if primary_style in used_styles and len(picks) < 2:
            continue
        used_styles.add(primary_style)
        picks.append(record)
        if len(picks) == 3:
            break

    if len(picks) < 3:
        for record in top_candidates:
            if record not in picks:
                picks.append(record)
            if len(picks) == 3:
                break

    lines = []

    # 根据场景生成开场白 - 天气优先于心情
    weather_phrases = {
        "rainy": "🌧️ 下雨天，来点暖和的吧~",
        "cold": "❄️ 天冷了，吃点热乎的暖暖身~",
        "hot": "🔥 大热天，来点清爽的开胃~",
        "sunny": "☀️ 晴天心情好，吃点好的！",
    }
    mood_phrases = {
        "tired": "😴 累了就该好好犒劳自己~",
        "happy": "😊 心情不错，来顿好的庆祝一下！",
        "comfort": "💆 想吃点治愈的~",
        "adventurous": "🌟 来点刺激的！",
        "light": "🥗 清淡点，对胃~",
        "party": "🎉 聚会时间，吃点热闹的！",
        "healthy": "💪 要健康，也要好吃！",
    }

    # 天气优先显示，其次是心情
    if profile["weather"] in weather_phrases:
        mood_phrase = weather_phrases[profile["weather"]]
    elif profile["mood"] in mood_phrases:
        mood_phrase = mood_phrases[profile["mood"]]
    else:
        mood_phrase = "🍽️ 来看看今天吃啥~"

    lines.append(mood_phrase)
    lines.append("")

    # 精简偏好展示
    pref_summary = []
    if profile["location"]:
        pref_summary.append(f"📍 {profile['location']}")
    if profile["mode"]:
        mode_text = {"takeaway": "🚴外卖", "dine_in": "🏪堂食", "cook": "🍳自制"}.get(profile["mode"], "")
        pref_summary.append(mode_text)
    if profile["budget"]:
        budget_text = {"low": "💰¥15-25", "mid": "💰¥25-40", "high": "💰¥40-80"}.get(profile["budget"], "")
        pref_summary.append(budget_text)
    if pref_summary:
        lines.append(" ".join(pref_summary))
        lines.append("")

    lines.append("### ⭐ 推荐给你：")

    for idx, (_, food, reasons, _, cuisines) in enumerate(picks, start=1):
        img_path = build_image_path(food["name"], base)
        reason_text = "、".join(dict.fromkeys(reasons[:4])) if reasons else "综合口味和预算平衡"

        # 更直观的标签
        price_range = {"low": "¥15-25", "mid": "¥25-40", "high": "¥40-80"}.get(food["price"], "")
        price_label = f"💰{price_range}" if price_range else ""
        spicy_emoji = {"low": "🌶️微辣", "mid": "🌶️🌶️中辣", "high": "🌶️🌶️🌶️重辣"}.get(food["spicy"], "")
        # 时段根据当前时段显示推荐适合的时间
        time_emoji = {"breakfast": "🍳", "lunch": "☀️", "dinner": "🌙", "late_night": "🌟"}.get(profile["time_slot"], "")
        time_text = {"breakfast": "早餐", "lunch": "午餐", "dinner": "晚餐", "late_night": "夜宵"}.get(profile["time_slot"], "")
        time_label = f"{time_emoji}{time_text}" if time_emoji else ""
        mode_emoji = "🚴外卖" if "takeaway" in food["modes"] else ("🏪堂食" if "dine_in" in food["modes"] else "🍳自制")

        lines.append(f"**{idx}. {food['name']}**")
        lines.append(f"   💡 {reason_text}")
        tags = [price_label, spicy_emoji, time_label, mode_emoji]
        lines.append(f"   {' '.join([t for t in tags if t])}")
        if img_path:
            normalized_img_path = img_path.replace("\\", "/")
            lines.append(f"   ![{food['name']}]({normalized_img_path})")
        lines.append("")

    lines.append("---")
    lines.append("💬 纠结？回我 **1/2/3**，我给你同类型更多选择~")
    lines.append("💡 想换换口味？告诉我忌口或预算，我重新推荐！")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="根据用户偏好推荐今天吃什么")
    parser.add_argument("query", nargs="*", help="用户原始描述")
    parser.add_argument("--weather", choices=["rainy", "cold", "hot", "sunny", "windy", "humid", "all"])
    parser.add_argument("--mood", choices=["happy", "tired", "comfort", "focused", "adventurous", "light", "party", "healthy", "neutral", "sick", "family", "busy"])
    parser.add_argument("--mode", choices=["takeaway", "dine_in", "cook"])
    parser.add_argument("--budget", choices=["low", "mid", "high"])
    parser.add_argument("--spicy", choices=["low", "mid", "high"])
    parser.add_argument("--time_slot", choices=["breakfast", "lunch", "dinner", "late_night"])
    parser.add_argument("--city_tag", choices=["all", "north", "south", "guangdong", "hainan", "hunan"])
    parser.add_argument("--location")

    args = parser.parse_args()
    query = " ".join(args.query).strip() or "今天吃什么"
    print(recommend(query, args))


if __name__ == "__main__":
    main()
