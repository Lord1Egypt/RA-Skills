---
name: cruise-ticket-query
display_name: 游轮船票查询
description: 零配置即装即用，支持长江三峡游轮和城市游船船票查询含价格和预订链接、市内交通到码头查询（地铁优先）、景点门票推荐和住宿推荐，多旅游平台数据直连。
tags: [游轮, 游船, 三峡游轮, 黄浦江游船, 船票, 游轮票, cruise, ship, ticket]
tools:
  - name: search_cruise
    description: 查询游轮船票信息，包括游轮名、价格、航线方向和退改政策
    parameters:
      - name: scenic_name
        type: string
        description: 游轮线路名，如"长江三峡游轮"、"黄浦江游船"、"重庆游船"
        required: true
  - name: query_transport
    description: 查询从出发地到游轮码头的交通方式，地铁优先展示，还有公交和打车预估
    parameters:
      - name: origin
        type: string
        description: 出发地名称，如"重庆北站"、"解放碑"
        required: true
      - name: destination
        type: string
        description: 目的地（码头名），如"朝天门码头"、"宜昌游客中心"
        required: true
      - name: city
        type: string
        description: 所在城市，如"重庆"、"宜昌"
        required: true
  - name: recommend_attraction
    description: 推荐游轮出发地或目的地城市的热门景点，含门票价格和预订链接
    parameters:
      - name: city
        type: string
        description: 城市名，如"重庆"、"宜昌"、"上海"
        required: true
      - name: keyword
        type: string
        description: 景点关键词，如"洪崖洞"、"大坝"，不填则推荐城市热门景点
        required: false
  - name: recommend_hotel
    description: 用自然语言描述住宿需求，AI智能匹配高分酒店并返回推荐和预订链接
    parameters:
      - name: query
        type: string
        description: 住宿需求描述，如"重庆朝天门附近酒店，300左右"
        required: true
---

# 游轮船票查询 — 游轮票务 + 市内交通 + 景点推荐 + 住宿推荐

> ⚡ **游轮船票 · 市内交通 · 景点门票 · 住宿推荐 · 零配置即装即用**

---

## 快速入门

**4个开场白示例，复制即用：**
1. "帮我查长江三峡游轮的船票"
2. "从重庆北站怎么去朝天门码头"
3. "推荐重庆的热门景点"
4. "重庆住解放碑附近，300左右的酒店"

---

## 核心能力

1. **游轮船票查询**：查询长江三峡游轮、黄浦江游船等船票，含价格、上下水方向和退改政策
2. **市内交通**：查去码头的地铁/公交/打车方案，地铁优先展示
3. **景点推荐**：推荐游轮出发地或目的地城市热门景点，含门票价格和购票链接
4. **住宿推荐**：用自然语言描述需求，AI智能匹配酒店

## 能做什么

- 查询长江三峡游轮、黄浦江游船、重庆游船等船票
- 查去码头的地铁、公交、打车方案
- 推荐出发地/目的地城市的热门景点和门票
- 推荐附近住宿酒店

## 不能做什么

- 不支持直接购买船票（提供预订链接，用户点击跳转购买）
- 不支持海洋邮轮（如歌诗达、皇家加勒比），仅覆盖国内江河游轮
- 不支持查询已购船票状态或办理退票

## 使用示例

1. "帮我查长江三峡游轮的船票"
2. "黄浦江游船多少钱"
3. "从重庆北站怎么去朝天门码头"
4. "推荐宜昌的景点"
5. "重庆住解放碑附近，300左右的酒店"

## 注意事项

- 游轮搜索需要精确关键词，如"长江三峡游轮"比"三峡"更准确
- 船票价格实时变动，以实际下单页面为准
- 地铁/公交方案来自高德地图，实际运营时间以当地公交地铁公告为准
- 打车费用为预估，实际以网约车平台为准
- 数据来源为多旅游平台直连，查询经代理服务获取，不存储用户数据

## 数据流向

用户输入（线路名/城市/日期等查询参数）→ 本技能脚本 → 代理服务 → 旅游平台API → 返回结果给用户。查询参数会发送到代理服务以获取实时票务和交通数据，代理服务不存储用户数据。
