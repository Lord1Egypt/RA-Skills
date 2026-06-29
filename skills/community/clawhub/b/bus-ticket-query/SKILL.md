---
name: bus-ticket-query
display_name: 汽车票查询与预订
description: 零配置即装即用，支持汽车票班次查询含余票和预订链接、去汽车站交通方式查询（地铁优先）和目的地住宿推荐，多旅游平台数据直连。
tags: [汽车票, 大巴, 客运, 汽车站交通, 地铁去汽车站, 住宿推荐, bus, coach, ticket]
tools:
  - name: search_bus
    description: 查询汽车票班次、价格和余票信息，支持灵活日期输入
    parameters:
      - name: departure
        type: string
        description: 出发城市，如"上海"、"广州"
        required: true
      - name: destination
        type: string
        description: 到达城市，如"苏州"、"深圳"
        required: true
      - name: dep_date
        type: string
        description: 出发日期，支持"6月15日"、"6-15"、"明天"等灵活格式
        required: false
  - name: query_transport
    description: 查询从出发地到汽车站的交通方式，地铁优先展示，还有公交和打车预估
    parameters:
      - name: origin
        type: string
        description: 出发地名称，如"南京路"、"浦东机场"
        required: true
      - name: bus_station
        type: string
        description: 汽车站名，如"上海虹桥客运西站"、"苏州汽车南站"
        required: true
      - name: city
        type: string
        description: 所在城市，如"上海"、"苏州"
        required: true
  - name: recommend_hotel
    description: 用自然语言描述住宿需求，AI智能匹配高分酒店并返回推荐和预订链接
    parameters:
      - name: query
        type: string
        description: 住宿需求描述，如"苏州住观前街附近，200左右"
        required: true
---

# 汽车票查询与预订 — 汽车票查询 + 去站交通 + 住宿推荐

> ⚡ **实时余票 · 灵活日期 · 地铁优先去站 · 住宿推荐 · 零配置即装即用**

---

## 快速入门

**3个开场白示例，复制即用：**
1. "帮我查明天上海到苏州的汽车票"
2. "从南京路怎么去上海虹桥客运西站"
3. "苏州住观前街附近，200左右的酒店"

---

## 核心能力

1. **汽车票查询**：查询客运班次、票价、余票，按出发时间排序
2. **智能日期解析**：支持"6月15日"、"6-15"、"明天"、"后天"等多种日期格式
3. **余票提醒**：5张以下标🔥仅剩，无票标❌，方便抢票决策
4. **去站交通（地铁优先）**：地铁/城轨方案排最前，公交次之，打车预估最后
5. **住宿推荐**：用自然语言描述需求，AI智能匹配酒店

## 能做什么

- 查询国内汽车票实时票价和余票
- 查去汽车站的地铁、公交、打车方案（省钱优先）
- 推荐目的地住宿酒店

## 不能做什么

- 不支持直接购买汽车票（提供预订链接，用户点击跳转购买）
- 不支持查询已购车票状态或办理退票

## 使用示例

1. "帮我查明天上海到苏州的汽车票"
2. "广州到深圳6月20号的汽车票"
3. "从浦东机场怎么去虹桥客运站"
4. "苏州住观前街附近，200左右的酒店"

## 注意事项

- 票价和余票实时变动，以实际下单页面为准
- 地铁/公交方案来自高德地图，实际运营时间以当地公交地铁公告为准
- 打车费用为预估，实际以网约车平台为准
- 数据来源为多旅游平台直连，不存储用户数据

## 数据流向

用户输入（城市、日期、车站名等查询参数）→ 本技能脚本 → 代理服务 → 旅游平台API → 返回结果给用户。查询参数会发送到代理服务以获取实时票务和交通数据，代理服务不存储用户数据。
