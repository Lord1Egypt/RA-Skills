---
name: dianping-api
description: "Dianping (大众点评) API skill for searching restaurants and businesses, viewing shop details, deals/coupons, and reading recommended dishes. Use this skill when: (1) the user asks about restaurants, food, or local businesses in Chinese cities, (2) the user wants to search dianping.com, (3) the user needs shop ratings, reviews, prices, deals, or addresses from 大众点评, (4) any query involving Chinese dining recommendations or local business lookup."
---

# Dianping API

Zero-dependency HTTP API for dianping.com (大众点评). No browser engine, no pip install — only `curl` (pre-installed on macOS/Linux).

## Prerequisites

- Python 3.6+
- `curl` (系统自带，无需安装)

### Authentication (only 2 cookies needed)

Only `dper` and `dplet` cookies are required. Stored in `~/.dianping/cookies.json`.

```bash
# Set cookies
python3 dianping-api/scripts/dianping_login.py --set-cookies "dper=xxx; dplet=yyy"

# Check login status
python3 dianping-api/scripts/dianping_login.py --status

# Cookie expired? Guided renewal:
python3 dianping-api/scripts/dianping_login.py --renew
```

## API Reference — `dianping_api.py`

All commands output **JSON to stdout**, ready for AI parsing.

### 1. Search Shops

```bash
python3 dianping-api/scripts/dianping_api.py search <keyword> [--city_id N]
```

- `keyword`: 大众点评搜索框，支持自由组合。示例：
  - **菜系**: `"川菜"`, `"日料"`, `"淮扬菜"`, `"火锅"`, `"西餐"`
  - **地点+菜系**: `"外滩 日料"`, `"陆家嘴 火锅"`, `"世纪大道 淮扬菜"`
  - **景点+场景**: `"迪士尼 亲子餐厅"`, `"故宫 烤鸭"`, `"西湖 本帮菜"`
  - **特殊需求**: `"有包厢"`, `"宝宝餐"`, `"人均100"`, `"深夜食堂"`
  - **综合**: `"陆家嘴 亲子 好评"`, `"南京路 网红甜品"`
- `city_id`: 城市编号（见下方城市表），默认 1=上海

**Response:**
```json
{
  "keyword": "世纪大道淮扬菜",
  "city_id": 1,
  "count": 11,
  "shops": [
    {
      "shop_id": "l7UgWvw6yZ7ytaly",
      "name": "九厨·淮扬(陆家嘴紫金山店)",
      "rating": 4.5,
      "review_count": "455",
      "avg_price": 155
    }
  ]
}
```

### 2. Shop Details

```bash
python3 dianping-api/scripts/dianping_api.py shop <shop_id>
```

**Response:**
```json
{
  "shop_id": "l7UgWvw6yZ7ytaly",
  "name": "九厨·淮扬(陆家嘴紫金山店)",
  "score_text": "口味:4.7 环境:4.8 服务:4.7",
  "avg_price": "155",
  "review_count": "455条",
  "category": "淮扬菜",
  "region": "世纪大道",
  "address": "东方路778号金陵紫金山大酒店2楼",
  "route": "距地铁世纪大道站12口步行400m",
  "phone": "65******",
  "recommended_dishes": ["九厨桂花香酥烤鸭", "淮安特色一品狮子头", "..."],
  "scores": {"taste": 4.7, "environment": 4.8, "service": 4.7}
}
```

### 3. Deals / Coupons

```bash
python3 dianping-api/scripts/dianping_api.py deals <shop_id>
```

**Response:**
```json
{
  "shop_id": "l7UgWvw6yZ7ytaly",
  "name": "九厨·淮扬(陆家嘴紫金山店)",
  "deals": [
    {"title": "【午市专享】100元代金券", "price": 79.0, "original_price": 100.0},
    {"title": "九厨淮扬精选宝宝餐", "price": 0.1, "original_price": 29.9},
    {"title": "招牌烤鸭+醉沼虾+牛肉粒2-3人餐", "price": 279.0, "original_price": 500.0}
  ],
  "services": [],
  "tags": []
}
```

## Python Import Usage

```python
import sys; sys.path.insert(0, "dianping-api/scripts")
from dianping_api import api_search, api_shop, api_deals

# Search
results = api_search("陆家嘴火锅", city_id=1)
for s in results["shops"]:
    print(s["shop_id"], s["name"], s.get("rating"))

# Shop detail
info = api_shop("l7UgWvw6yZ7ytaly")
print(info["scores"], info["recommended_dishes"])

# Deals
deals = api_deals("l7UgWvw6yZ7ytaly")
for d in deals["deals"]:
    print(d["title"], d.get("price"), d.get("original_price"))
```

## Typical AI Workflow

```
1. 根据用户意图组合 keyword（地点+菜系+场景），选对 city_id
   例: 用户说"北京故宫附近吃烤鸭" → search("故宫 烤鸭", city_id=2)
   例: 用户说"上海迪士尼带娃吃饭" → search("迪士尼 亲子餐厅", city_id=1)
   例: 用户说"杭州西湖附近日料"   → search("西湖 日料", city_id=5)

2. api_search(keyword, city_id) → 拿到 shop_id 列表
3. api_shop(shop_id)            → 评分、推荐菜、地址、交通
4. api_deals(shop_id)           → 优惠券、套餐、价格
5. 整理推荐给用户（含评分、人均、推荐菜、优惠信息）
```

## City IDs

| 城市 | ID | 城市 | ID | 城市 | ID | 城市 | ID |
|------|-----|------|-----|------|-----|------|-----|
| 上海 | 1 | 北京 | 2 | 大连 | 3 | 广州 | 4 |
| 杭州 | 5 | 苏州 | 6 | 深圳 | 7 | 成都 | 8 |
| 南京 | 9 | 天津 | 10 | 沈阳 | 11 | 武汉 | 12 |
| 哈尔滨 | 13 | 长沙 | 14 | 厦门 | 15 | 郑州 | 16 |
| 西安 | 17 | 青岛 | 18 | 重庆 | 19 | 昆明 | 20 |

## Error Handling

All errors return `{"error": "..."}`. Common:
- `"请求失败或需要重新登录"` → Run `dianping_login.py --renew`

## Architecture

- **Backend**: Pure HTTP via `curl` subprocess (no Playwright/browser, no pip dependencies)
- **Auth**: `dper` + `dplet` cookies in `~/.dianping/cookies.json`
- **Scripts**: `dianping_login.py` (auth管理) + `dianping_api.py` (数据API)
