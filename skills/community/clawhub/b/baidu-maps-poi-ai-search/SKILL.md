---
name: baidu-maps-poi-ai-search
description: Search and get details for POI (points of interest) using Baidu Maps API. Use for searching places, restaurants, hotels, attractions, and retrieving detailed POI information by UID.
metadata: { "openclaw": { "emoji": "📍", "requires": { "bins": ["python3"], "env": ["BAIDU_AK"], "primaryEnv": "BAIDU_AK" } } }
---

# Baidu Maps POI AI Search Skill

百度地图 POI AI搜索,通过百度地图AI搜接口，可以查找地点的名称、地址、类别、经营范围、属性内容。

> ⚠️ **环境配置**：使用前请设置 `BAIDU_AK` 环境变量（百度地图开放平台申请的 AK）。脚本内不含默认 AK，需自行配置。

## 接口概览

| 接口 | 脚本 | 说明 |
|------|------|------|
| 多维检索 | `search.py` | 搜索 POI，名称(北京大学)、地址(北京市上地十街10号)、类别(火锅)、经营范围(买包子)、复杂属性内容(西二旗附近适合带宠物的餐厅)。|

## 1. 多维检索 (search.py)

```bash
python3 skills/baidu-maps-poi-ai-search/scripts/search.py '<JSON>'
```

### 请求参数

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| query | str | yes | - | 检索关键字，如"美食"、"海底捞"、"看日出的地方"、"能带宠物吃饭的餐厅" |
| region | str | yes | - | 行政区划，如"北京"、"北京市海淀区" |
| scope | int | yes | 2 | 2=详细信息 |
| page_num | int | no | 0 | 分页页码，从0开始 |
| center | str | no | - | 中心点坐标 `lat,lng`，配合 sort_name=distance |
| coord_type | int | no | 3 | 坐标类型：1=wgs84ll, 2=gcj02ll, 3=bd09ll |

### 多维检索 Examples

```bash
# 搜索名称
python3 skills/baidu-maps-poi-ai-search/scripts/search.py '{"query":"北京大学","region":"北京","scope":2,"page_size":5}'

# 搜索类别
python3 skills/baidu-maps-poi-ai-search/scripts/search.py '{"query":"火锅","region":"北京","scope":2,"page_size":5}'

# 口语化搜索
python3 skills/baidu-maps-poi-ai-search/scripts/search.py '{"query":"故宫附近能多人聚会的地方","region":"北京","scope":2,"page_size":5}'
```

## API 文档
- 多维检索：`https://api.map.baidu.com/api_place_pro/v1/region`
