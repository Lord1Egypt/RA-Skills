---
name: 邮轮游查询预订
display_name: "邮轮游查询预订"
description: 全球邮轮航线实时搜索与智能推荐，接入途牛实时API，覆盖日韩、东南亚、地中海、加勒比海、长江三峡等航线。支持按目的地/出发地/日期/价格智能筛选，提供口碑之选/性价比首选/热门推荐/航线精选多维度推荐。新增产品详情（预订须知/取消条款/促销）、舱位房型查询（价格/面积/楼层/阳台）、船舶信息查询（船舶参数/餐饮设施/娱乐项目），含实时价格、满意度、预订人数和一键预订链接。
version: 3.0.2
tags: [邮轮搜索, 邮轮推荐, 海上邮轮, 长江三峡, 日韩邮轮, 地中海邮轮]
tools:
  - name: search_cruise
    description: 按条件搜索邮轮航线（目的地/出发地/日期/价格）
    primaryEnv: PROXY_URL
    env:
      - name: PROXY_URL
        description: 途牛邮轮API代理地址
        required: true
      - name: PROXY_TOKEN
        description: 代理认证Token
        required: true
    parameters:
      - name: params
        type: string
        description: JSON格式参数，支持字段：destination(目的地,如"日本")、departure(出发城市,如"上海")、days(未来天数,默认90)、price_max(最高价格)、tag(标签筛选,如"亲子")
        required: true
  - name: recommend_cruise
    description: 智能推荐邮轮（按口碑/性价比/热门/航线分组推荐）
    parameters:
      - name: params
        type: string
        description: JSON格式参数，支持字段：days(未来天数,默认90)
        required: true
  - name: cruise_detail
    description: 查询邮轮产品详情（含预订须知、取消条款、当前促销、行程概览）
    parameters:
      - name: params
        type: string
        description: JSON格式参数，必填：product_id(产品ID)；可选：days(搜索天数,默认90)、route(航线关键词辅助定位,如"日本")
        required: true
  - name: cruise_cabin
    description: 查询邮轮舱位房型（舱等类型、价格、面积、楼层、阳台、成人/儿童价）
    parameters:
      - name: params
        type: string
        description: JSON格式参数，必填：product_id(产品ID)、depart_date(出发日期YYYY-MM-DD)
        required: true
  - name: cruise_ship_info
    description: 查询邮轮船舶信息（船舶参数、舱型说明、餐饮设施、娱乐设施）
    parameters:
      - name: params
        type: string
        description: JSON格式参数，必填：product_id(产品ID)
        required: true
primaryEnv: PROXY_URL

---

# 邮轮搜索 — 途牛实时数据，全球航线智能搜索与推荐

> 接入途牛实时API，覆盖全球主要邮轮航线，支持搜索、推荐、产品详情、舱位查询、船舶信息全流程。

🔥 **核心亮点：**
- **实时数据** — 接入途牛API，价格/库存/评价均为实时数据，非静态demo
- **智能推荐** — 4大推荐维度：口碑之选/性价比首选/热门推荐/航线精选
- **产品详情** — 预订须知、取消条款、当前促销优惠、行程概览
- **舱位查询** — 舱等类型（内舱/海景/阳台/套房）、实时价格、面积楼层、阳台信息
- **船舶信息** — 船舶参数（吨位/尺寸/载客）、餐饮设施（免费/收费）、娱乐项目
- **全球覆盖** — 日韩、东南亚、地中海、加勒比海、阿拉斯加、长江三峡等
- **品牌齐全** — 皇家加勒比、MSC、歌诗达、爱达、维京、世纪游轮、黄金游轮等
- **零配置** — 免申请Key，装上就能用

## 快速入门

**5个开场白示例，复制即用：**

1. "暑假有什么邮轮推荐"
2. "上海出发去日本的邮轮"
3. "3000以内的三峡邮轮"
4. "产品320717790的详情和取消条款"
5. "这艘船有什么餐厅和娱乐设施"

## 核心能力

1. **条件搜索** — 按目的地/出发城市/日期范围/价格/标签精准搜索
2. **智能推荐** — 无需明确目的地，自动按4个维度推荐最佳航线
3. **产品详情** — 查看预订须知、取消条款、促销优惠、行程概览
4. **舱位查询** — 各舱等房型价格、面积、楼层、是否阳台、成人/儿童价
5. **船舶信息** — 船舶参数、5种舱型说明、餐饮设施（含免费/收费标注）、娱乐项目
6. **一键预订** — 每条结果附带途牛预订链接，可直接跳转下单

## 能做什么

- 搜索全球各航线邮轮产品，返回实时价格和预订链接
- 按出发城市、目的地、预算范围、出行场景筛选
- 查看产品详情：取消条款、付款规则、签证须知、促销优惠
- 查看舱位价格：内舱房¥3532起、阳台房¥5237起，含面积楼层等
- 查看船舶设施：30家餐厅（4家免费）、15项娱乐设施、船舶参数
- 智能推荐：自动分出口碑/性价比/热门/航线精选4类推荐

## 不能做什么

- 不支持在线下单（提供预订链接跳转途牛完成）
- 不支持邮轮公司官网直连查询
- 不支持历史价格走势图

## 使用提示

- 用户说"邮轮推荐"时，优先用recommend_cruise，分维度展示
- 用户有明确目的地或出发地时，用search_cruise精准搜索
- 用户问某个产品详情/取消条款时，用cruise_detail（需productId）
- 用户问舱位价格/哪种房型好时，用cruise_cabin（需productId+出发日期）
- 用户问船上有什么吃的/玩的/船多大时，用cruise_ship_info（需productId）
- 邮轮价格随舱位浮动，建议尽早预订锁定低价
- 结果最多展示10条，按综合评分排序

## 🔗 搭配使用

- **途牛旅行助手** — 酒店/机票/火车票/门票一站式查询
- **酒店智能搜索** — 邮轮出发港附近酒店预订
- **高德地图全能版** — 导航到邮轮港口
- **全球航班查询** — 查询前往出发港的航班

## 数据流向

用户输入 → 本技能 → 途牛代理API → 途牛邮轮数据库 → 返回实时结果。代理不存储用户数据。
