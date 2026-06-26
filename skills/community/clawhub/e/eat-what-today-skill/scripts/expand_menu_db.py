import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
MENU_FILE = BASE / "assets" / "menu_db.json"
FOODS_DIR = BASE / "assets" / "foods_image"

existing = json.loads(MENU_FILE.read_text(encoding="utf-8"))
existing_map = {item["name"]: item for item in existing}

# Curated metadata for dishes not present in the initial seed menu.
overrides = {
    "卤粉": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["busy", "comfort", "neutral"],
        "weather": ["all"],
        "price": "low",
        "spicy": "mid",
        "city_tags": ["south", "hunan", "all"],
        "time_tags": ["breakfast", "lunch", "dinner"],
    },
    "嫩牛五方": {
        "modes": ["takeaway", "dine_in"],
        "moods": ["busy", "happy", "focused"],
        "weather": ["all"],
        "price": "mid",
        "spicy": "low",
        "city_tags": ["all"],
        "time_tags": ["lunch", "dinner"],
    },
    "新疆炒米粉": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["adventurous", "focused", "busy"],
        "weather": ["cold", "all"],
        "price": "mid",
        "spicy": "high",
        "city_tags": ["north", "all"],
        "time_tags": ["lunch", "dinner", "late_night"],
    },
    "日式烧肉饭": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["happy", "focused", "neutral"],
        "weather": ["all"],
        "price": "mid",
        "spicy": "low",
        "city_tags": ["all"],
        "time_tags": ["lunch", "dinner"],
    },
    "杀猪粉": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["comfort", "neutral", "busy"],
        "weather": ["cold", "rainy", "all"],
        "price": "low",
        "spicy": "mid",
        "city_tags": ["south", "hunan", "all"],
        "time_tags": ["breakfast", "lunch", "dinner"],
    },
    "桥头排骨": {
        "modes": ["takeaway", "dine_in"],
        "moods": ["happy", "party", "busy"],
        "weather": ["all"],
        "price": "mid",
        "spicy": "mid",
        "city_tags": ["all"],
        "time_tags": ["lunch", "dinner", "late_night"],
    },
    "水煮肉片": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["adventurous", "party", "happy"],
        "weather": ["cold", "rainy"],
        "price": "mid",
        "spicy": "high",
        "city_tags": ["south", "hunan", "all"],
        "time_tags": ["lunch", "dinner"],
    },
    "油炸烧烤": {
        "modes": ["takeaway", "dine_in"],
        "moods": ["party", "happy", "late_night"],
        "weather": ["all"],
        "price": "mid",
        "spicy": "mid",
        "city_tags": ["all"],
        "time_tags": ["dinner", "late_night"],
    },
    "煎饺": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["busy", "comfort", "neutral"],
        "weather": ["all"],
        "price": "low",
        "spicy": "low",
        "city_tags": ["north", "all"],
        "time_tags": ["breakfast", "lunch", "dinner"],
    },
    "牛丼饭": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["focused", "neutral", "busy"],
        "weather": ["all"],
        "price": "mid",
        "spicy": "low",
        "city_tags": ["all"],
        "time_tags": ["lunch", "dinner"],
    },
    "猪肚鸡": {
        "modes": ["dine_in", "cook"],
        "moods": ["comfort", "family", "tired"],
        "weather": ["cold", "rainy", "humid"],
        "price": "high",
        "spicy": "low",
        "city_tags": ["south", "guangdong", "all"],
        "time_tags": ["dinner", "late_night"],
    },
    "盖码饭": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["focused", "busy", "neutral"],
        "weather": ["all"],
        "price": "mid",
        "spicy": "mid",
        "city_tags": ["south", "hunan", "all"],
        "time_tags": ["lunch", "dinner"],
    },
    "肉汁拌饭": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["comfort", "focused", "neutral"],
        "weather": ["all"],
        "price": "mid",
        "spicy": "low",
        "city_tags": ["all"],
        "time_tags": ["lunch", "dinner"],
    },
    "臭豆腐": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["adventurous", "happy", "late_night"],
        "weather": ["all"],
        "price": "low",
        "spicy": "mid",
        "city_tags": ["south", "hunan", "all"],
        "time_tags": ["lunch", "dinner", "late_night"],
    },
    "葱油拌面": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["light", "busy", "focused"],
        "weather": ["hot", "all"],
        "price": "low",
        "spicy": "low",
        "city_tags": ["south", "all"],
        "time_tags": ["breakfast", "lunch", "dinner"],
    },
    "螺蛳粉": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["adventurous", "tired", "late_night"],
        "weather": ["rainy", "cold", "all"],
        "price": "low",
        "spicy": "high",
        "city_tags": ["south", "all"],
        "time_tags": ["lunch", "dinner", "late_night"],
    },
    "辣椒炒肉": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["adventurous", "focused", "happy"],
        "weather": ["cold", "all"],
        "price": "mid",
        "spicy": "high",
        "city_tags": ["south", "hunan", "all"],
        "time_tags": ["lunch", "dinner"],
    },
    "过桥米线": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["comfort", "focused", "tired"],
        "weather": ["cold", "rainy", "all"],
        "price": "mid",
        "spicy": "mid",
        "city_tags": ["south", "all"],
        "time_tags": ["lunch", "dinner"],
    },
    "酸菜鱼": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["party", "happy", "adventurous"],
        "weather": ["all"],
        "price": "high",
        "spicy": "high",
        "city_tags": ["all"],
        "time_tags": ["lunch", "dinner"]
    },
    "重庆小面": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["adventurous", "focused", "busy"],
        "weather": ["cold", "rainy", "all"],
        "price": "low",
        "spicy": "high",
        "city_tags": ["south", "all"],
        "time_tags": ["breakfast", "lunch", "dinner", "late_night"]
    },
    "锅盔": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["busy", "focused", "neutral"],
        "weather": ["all"],
        "price": "low",
        "spicy": "mid",
        "city_tags": ["north", "all"],
        "time_tags": ["breakfast", "lunch", "dinner"]
    },
    "韩式炸鸡": {
        "modes": ["takeaway", "dine_in"],
        "moods": ["party", "happy", "late_night"],
        "weather": ["all"],
        "price": "mid",
        "spicy": "mid",
        "city_tags": ["all"],
        "time_tags": ["lunch", "dinner", "late_night"]
    },
    "韩式烤肉": {
        "modes": ["dine_in", "cook"],
        "moods": ["party", "happy", "adventurous"],
        "weather": ["cold", "all"],
        "price": "high",
        "spicy": "mid",
        "city_tags": ["all"],
        "time_tags": ["dinner", "late_night"]
    },
    "韩式部队火锅": {
        "modes": ["dine_in", "cook"],
        "moods": ["party", "comfort", "happy"],
        "weather": ["cold", "rainy"],
        "price": "high",
        "spicy": "mid",
        "city_tags": ["all"],
        "time_tags": ["dinner", "late_night"]
    },
    "馄饨": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["comfort", "busy", "neutral"],
        "weather": ["cold", "rainy", "all"],
        "price": "low",
        "spicy": "low",
        "city_tags": ["all"],
        "time_tags": ["breakfast", "lunch", "dinner", "late_night"]
    },
    "鸭血粉丝": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["comfort", "focused", "neutral"],
        "weather": ["cold", "all"],
        "price": "low",
        "spicy": "mid",
        "city_tags": ["south", "all"],
        "time_tags": ["breakfast", "lunch", "dinner"]
    },
    "麻婆豆腐": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["adventurous", "focused", "happy"],
        "weather": ["all"],
        "price": "mid",
        "spicy": "high",
        "city_tags": ["all"],
        "time_tags": ["lunch", "dinner"]
    },
    "麻辣烫": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["adventurous", "tired", "busy"],
        "weather": ["cold", "rainy", "all"],
        "price": "low",
        "spicy": "high",
        "city_tags": ["all"],
        "time_tags": ["lunch", "dinner", "late_night"]
    },
    "麻辣香锅": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["party", "adventurous", "happy"],
        "weather": ["cold", "all"],
        "price": "high",
        "spicy": "high",
        "city_tags": ["all"],
        "time_tags": ["lunch", "dinner", "late_night"]
    },
    "黄焖鸡": {
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["focused", "busy", "neutral"],
        "weather": ["all"],
        "price": "mid",
        "spicy": "low",
        "city_tags": ["all"],
        "time_tags": ["lunch", "dinner"]
    },
}

def default_item(name: str):
    return {
        "name": name,
        "modes": ["takeaway", "dine_in", "cook"],
        "moods": ["neutral", "focused", "busy"],
        "weather": ["all"],
        "price": "mid",
        "spicy": "mid",
        "city_tags": ["all"],
        "time_tags": ["lunch", "dinner"],
    }

image_names = sorted(p.stem for p in FOODS_DIR.glob("*.*") if p.is_file())
updated = []
for name in image_names:
    if name in existing_map:
        item = existing_map[name]
    else:
        item = default_item(name)
    if name in overrides:
        merged = {**item, **overrides[name]}
        merged["name"] = name
        item = merged
    updated.append(item)

updated.sort(key=lambda x: x["name"])
MENU_FILE.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Updated menu items: {len(updated)}")
