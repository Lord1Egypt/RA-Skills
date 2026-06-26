---
name: baidu-nearby
description_en: |
  Baidu capability suite - provides Baidu web search and Baidu Map route planning.
  Includes: Baidu web search (baidu_search), route planning (baidu_direction), nearby place recommendation (baidu_nearby).
  Use when: Need to search the web, plan travel routes, or find nearby restaurants/attractions/hotels and other location services.
description_zh: |
  百度能力集合 - 提供百度搜索和百度地图路线规划功能。
  包含：百度网页搜索(baidu_search)、路线规划(baidu_direction)、附近场所推荐(baidu_nearby)。
  Use when: 需要搜索网页、规划出行路线、查找附近餐饮/景点/酒店等位置服务时。
version: 1.0.4
credentials:
  env:
    BAIDU_API_KEY:
      description: Baidu LBS Platform API Key (AK), used for map route planning and nearby place search / 百度 LBS 开放平台 API Key（AK），用于地图路线规划和附近场所搜索功能
      required: true
      sensitive: true
      sources:
        - env: BAIDU_API_KEY
        - env: BAIDU_AK
      docs: https://lbsyun.baidu.com/apiconsole/key
---

# Baidu Nearby / 百度能力集合

Baidu capability suite providing search and location services. / 百度能力集合，提供搜索和位置服务。

## Features / 功能

| Command / 命令 | Description / 说明 |
|------|------|
| `baidu_search` | Baidu web search / 百度网页搜索 |
| `baidu_direction` | Baidu Map route planning / 百度地图路线规划 |
| `baidu_nearby` | Nearby place recommendation / 附近场所推荐 |

## Configuration / 配置

Set Baidu API Key (required for LBS location services) / 设置百度 API Key（LBS 位置服务需要）：

```bash
export BAIDU_API_KEY="your_baidu_ak"
```

How to get AK / 获取 AK：
1. Visit https://lbsyun.baidu.com/
2. Register a developer account / 注册开发者账号
3. Create an application to get AK / 创建应用获取 AK

## Usage / 使用方法

### Baidu Search / 百度搜索

```bash
python scripts/baidu_search.py "search_keywords" [result_count]
```

### Route Planning / 路线规划

```bash
python scripts/baidu_direction.py "origin_address" "destination_address" [driving|riding|walking|transit]
```

### Nearby Place Recommendation / 附近场所推荐

```bash
python scripts/baidu_nearby.py "location" [category] [radius_meters] [count]
```

**Supported Categories / 支持的类别：**
- 餐饮/美食/餐厅 — Food & Dining
- 娱乐/休闲 — Entertainment & Leisure
- 景点/旅游/景区 — Attractions & Tourism
- 酒店/住宿 — Hotels & Accommodation
- 购物/商场/超市 — Shopping & Malls
- 交通/地铁/公交 — Transportation

**Examples / 示例：**
```bash
# Search for food near Sanlitun / 搜索三里屯附近美食
python scripts/baidu_nearby.py "Sanlitun, Chaoyang District, Beijing" 餐饮 1000 5

# Search for attractions near Tiananmen / 搜索天安门附近景点
python scripts/baidu_nearby.py "Tiananmen" 景点 5000 10

# Search using coordinates / 使用坐标搜索
python scripts/baidu_nearby.py "39.9,116.4" 娱乐
```

## Dependencies / 依赖

Pure Python standard library, no additional dependencies. / 纯 Python 标准库实现，无需额外依赖。

## Security Notes / 安全说明

- Uses system default SSL certificate verification / 使用系统默认 SSL 证书验证
- Input parameters are validated and sanitized / 输入参数已做验证和清理
- Only HTTP/HTTPS protocols supported / 仅支持 HTTP/HTTPS 协议
