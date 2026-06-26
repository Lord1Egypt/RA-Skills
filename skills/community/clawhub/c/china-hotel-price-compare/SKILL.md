---
name: china-hotel-price-compare
description: 零配置即装即用｜先浏览选定再比价｜5源实时比价含预订链接｜评分距离早餐窗户等详细信息
tags: [酒店比价, 酒店预订, 酒店搜索, 酒店查询, 订酒店, 酒店对比, 特价酒店, 途牛酒店, 住宿比价, hotel, travel]
tools:
  - name: hotel_compare
    description: 多平台酒店比价，先浏览选定酒店再启动飞猪/途牛/同程/美团/RG 5源并发比价
    primaryEnv: HOTEL_COMPARE_PROXY_URL
    env:
      - name: HOTEL_COMPARE_PROXY_URL
        description: 比价代理URL（自动配置，无需手动设置）
        required: false
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: city
        type: string
        description: 目标城市，如"上海""北京""成都"
        required: true
      - name: check_in
        type: string
        description: 入住日期，格式YYYY-MM-DD
        required: false
      - name: check_out
        type: string
        description: 退房日期，格式YYYY-MM-DD
        required: false
      - name: keyword
        type: string
        description: 搜索关键词，支持区域（如"外滩""三里屯"）、地标（如"迪士尼"）、品牌（如"全季""亚朵"），不填则搜索全城
        required: false
      - name: hotel_name
        type: string
        description: 选定的酒店名称。不填→第一步浏览模式，展示酒店列表；填写→第二步比价模式，在多个旅游平台查找该酒店最低价
        required: false
      - name: max_price
        type: number
        description: 价格上限（元），如1000表示只看1000元以内的酒店，不填则不限价格
        required: false
      - name: poi_name
        type: string
        description: 兴趣点或景点名称，如"东方明珠""西湖"，会搜索该景点附近的酒店
        required: false
      - name: min_score
        type: number
        description: 最低评分要求，如4.5表示只看4.5分及以上的酒店，不填则不限评分
        required: false
---

# 酒店比价 — 先浏览选定再比价

> ⚡ **两步式交互 · 途牛浏览5源并发比价 · 含评分距离早餐等详细信息 · 零配置即装即用**

---

## 快速入门

**3个开场白示例，复制即用：**
1. "帮我查6月15号上海外滩附近的酒店"
2. "北京1000以内的酒店有哪些"
3. "上海外滩华尔道夫酒店哪个平台最便宜"

---

## 核心能力

1. **两步式交互**：先浏览酒店列表（含评分、距离、早餐、窗户等），选定后启动多平台比价
2. **5源并发比价**：选定酒店后同时查询飞猪、RollingGo、途牛、同程、美团，找全网最低价
3. **丰富酒店信息**：展示评分、距地标距离、早餐、窗户、取消政策、住客点评摘要
4. **佣金优先推荐**：同价时优先推荐有佣金的平台（RollingGo>飞猪），最低价带预订链接
5. **智能换条件提示**：结果不理想时，提示限价、限评分、或换个区域
6. **价格异常提醒**：当平台间价差过大时自动提醒

---

## 能做什么

- 按城市+日期+区域浏览酒店，信息丰富（评分/距离/早餐/窗户/取消政策/点评）
- 选定酒店后一键启动5源并发比价，找到全网最低价
- 支持按区域、地标、品牌关键词精准查找
- 支持按价格上限和最低评分筛选

## 不能做什么

- 不支持直接预订酒店（仅比价并附最低价平台链接，用户点击跳转预订）
- 不支持查询已预订酒店状态
- 不支持按星级筛选（途牛信息中已包含星级标识）

## 使用示例

1. "帮我查6月15号上海外滩附近的酒店"（第一步浏览）
2. "第3家酒店帮我比价"（第二步比价）
3. "北京1000以内4.5分以上的酒店"

## 注意事项

- 价格实时变动，以实际预订页面为准
- 第一步浏览模式展示途牛价格，尚未比价；选定酒店后才启动5源并发比价
- 查询通过云端代理并发转发到飞猪、途牛、同程、美团、RollingGo等OTA平台，代理不存储用户数据
- 部分平台偶发超时无数据，比价结果可能少于5个平台
- 美团为起步价（不含具体入住日期），其他平台为指定日期价格

## 数据流向

用户输入 → 本技能 → 腾讯云SCF代理（密钥安全存储）→ 飞猪/途牛/同程/美团/RollingGo → 代理返回数据 → 本技能解析比价 → 返回结果给用户

## 使用提示

- 用户未提供日期时，默认查明天住一晚
- 不传hotel_name时为浏览模式，传hotel_name时为比价模式
- 同一酒店不同平台价格差大时，可能是房型差异，结果会自动提醒
- 想继续筛选可补充：限价（如"1000以内"）、限评分（如"4.5分以上"）、换区域
