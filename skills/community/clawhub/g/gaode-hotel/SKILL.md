---
name: gaode-hotel
display_name: "高德×飞猪·一句话订酒店"
description: 用高德 POI 数据解析任意地名（商圈、地铁站、网红餐厅、小区……），再调飞猪实时房价和预订链接。突破飞猪 --poi-name 只认头部景区的限制，任意地点均可锚定。
homepage: https://open.fly.ai/
metadata:
  version: 1.0.3
  agent:
    type: tool
    runtime: python
    context_isolation: execution
    parent_context_access: read-only
  openclaw:
    emoji: "🏨"
    priority: 85
    requires:
      bins:
        - python3
        - flyai
    intents:
      - hotel_search
      - travel_booking
      - poi_anchored_hotel_search
    patterns:
      - "(附近|旁边|周边|近).*(酒店|民宿|住宿|客栈)"
      - "(酒店|民宿|住宿).*(附近|推荐|预订|查一下)"
      - "我要去.*(住|订酒店|找酒店)"
      - "(hotel|stay).*(near|around|next to)"
---

# 高德×飞猪·一句话订酒店

**核心差异化**：飞猪 `--poi-name` 只能锚定西湖、故宫等头部景区；普通商圈（798艺术区）、地铁站（酒仙桥）、餐厅附近等会漂到错误位置。本 skill 先用高德 POI 数据做地名解析，拿到规范名称和坐标，再把规范名喂给飞猪，实现任意地点锚定。

## 用法

```bash
# 环境变量（必须，不能写入任何文件）
export GAODE_POI_KEY="xl_xxx"
export GAODE_POI_BASE="<高德 POI 服务地址>"

# 自然语言整句（v1.0.2 新增，agent 直接调用推荐方式）
python3 travel_agent.py --query "我下周去成都宽窄巷子住两晚"
python3 travel_agent.py --query "明天去杭州西湖住一晚"
python3 travel_agent.py --query "10月25日去北京798艺术区住3晚"

# 参数拆分方式（仍支持，与 --query 可混用）
python3 travel_agent.py --city 北京 --place 798艺术区 \
  --check-in 2026-10-25 --check-out 2026-10-26

# 带星级和价格上限
python3 travel_agent.py --city 上海 --place 外滩 \
  --check-in 2026-11-01 --check-out 2026-11-02 \
  --stars 4,5 --max-price 800 --sort rate_desc --top 5

# 附上周边餐饮（高德富化，1km 内）
python3 travel_agent.py --query "后天去成都宽窄巷子出差住一晚" --enrich-nearby
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--city` | 是 | 城市，如 北京、杭州 |
| `--place` | 是 | 目的地/景点/商圈/地铁站/任意地名 |
| `--check-in` | 是 | 入住日期 YYYY-MM-DD |
| `--check-out` | 是 | 退房日期 YYYY-MM-DD |
| `--stars` | 否 | 星级，逗号分隔，如 4,5 |
| `--max-price` | 否 | 每晚最高价（元） |
| `--sort` | 否 | 排序：`distance_asc`/`rate_desc`/`price_asc`/`price_desc`（默认 distance_asc） |
| `--top` | 否 | 展示酒店数量（默认 5） |
| `--enrich-nearby` | 否 | 附上目的地周边 1km 内餐饮（高德富化数据） |

## 工作流程

```
用户一句话
  ↓
高德 POI /search 解析地名
  → 得到规范名称 + 坐标 + 类目
  → 若类目非住宿：用规范名 + --key-words（通用锚定）
  → 若类目是住宿（说明地名是泛词如"西湖"）：用原始输入 + --poi-name（飞猪对著名景区更准）
  ↓
flyai search-hotel
  → 实时房价 + 真实库存 + feizhu.com 预订链接
  ↓
（可选）高德 POI /nearby 周边餐饮富化
  ↓
Markdown 输出：图片 + 价格 + 预订链接 + 周边吃饭
```

## 输出示例

```markdown
# 北京 · 798艺术区 附近酒店

基于高德 POI 定位：798艺术区（风景名胜）坐标 116.496,39.986，酒仙桥路4号

## 飞猪实时库存（2026-10-25 → 2026-10-26）

![](https://img.alicdn.com/...)

### 秋果酒店(北京望京798艺术区店)

舒适型 · 4.0分 · ¥358 · 近798艺术区

[点击预订](https://router.feizhu.com/...)
```

## 数据来源

- **高德 POI**：REST API，服务地址通过环境变量 `GAODE_POI_BASE` 配置，Header `X-API-Key`
- **飞猪**：`flyai search-hotel`，OpenClaw/FlyAI 协议，实时房价房态

## 安全规则

`GAODE_POI_KEY` 必须通过环境变量传入，禁止写入任何文件（含 memory、config、脚本硬编码）。
