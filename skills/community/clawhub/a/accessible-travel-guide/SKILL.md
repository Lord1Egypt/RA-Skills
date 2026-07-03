---
name: accessible-travel-guide
display_name: 无障碍旅行助手
description: 无障碍出行助手，查询景点/酒店/交通无障碍设施，覆盖轮椅/视障/听障/婴儿车/老年5类需求，30+热门景区和主流酒店品牌实地数据，零配置即装即用。
tags: [无障碍旅行, 轮椅出行, 银发旅游, 婴儿车出行, 无障碍设施]
tools:
  - name: spot_accessibility
    description: 查询景点的无障碍设施信息，包括轮椅通道、无障碍卫生间、轮椅租借、无障碍路线等
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: spot_name
        type: string
        description: 景点名称，如"故宫""西湖""兵马俑"
        required: true
      - name: need_type
        type: string
        description: 无障碍需求类型，可选：wheelchair(轮椅)、visual(视障)、hearing(听障)、stroller(婴儿车)、elderly(老年人)
        required: false
  - name: hotel_accessibility
    description: 查询酒店品牌的无障碍房型和设施信息，包括无障碍客房、扶手、宽门、电梯等
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: hotel_brand
        type: string
        description: 酒店品牌或名称，如"万豪""如家""全季"
        required: true
      - name: city
        type: string
        description: 城市名称，如"北京""上海"
        required: false
  - name: travel_tips
    description: 根据出行类型和目的地提供无障碍旅行实用建议，包括交通、装备、预约等
    parameters:
      - name: destination
        type: string
        description: 目的地，如"北京""西安""成都"
        required: true
      - name: accessibility_need
        type: string
        description: 无障碍需求类型，可选：wheelchair(轮椅)、visual(视障)、hearing(听障)、stroller(婴儿车)、elderly(老年人)
        required: true
      - name: travel_mode
        type: string
        description: 出行方式，可选：plane(飞机)、train(火车)、self_drive(自驾)
        required: false
---

# 无障碍旅行助手 — 轮椅/视障/听障/婴儿车/老年，5类需求全覆盖

> 覆盖30+热门5A景区和10+主流酒店品牌实地数据，为无障碍出行提供设施查询和实用建议。

🔥 **核心亮点：**
- **5类需求覆盖** — 轮椅/视障/听障/婴儿车/老年，一个技能全搞定
- **30+景区数据** — 故宫/西湖/兵马俑等热门5A景区实地调研数据
- **酒店无障碍** — 万豪/如家/全季等品牌无障碍客房和设施查询
- **实用建议** — 交通选择、装备清单、预约渠道、优惠政策
- **零配置** — 装上就能用

## 快速入门

**3个开场白示例，复制即用：**

1. "故宫轮椅能进吗"
2. "带老人去杭州西湖方便吗"
3. "万豪酒店有没有无障碍房"

## 核心能力

1. **景点无障碍查询** — 轮椅通道、无障碍卫生间、轮椅租借点、无障碍路线
2. **酒店无障碍查询** — 无障碍客房房型、房门宽度、浴室扶手、电梯规格
3. **出行建议** — 根据需求类型和目的地，提供交通/装备/预约/优惠建议
4. **5类需求** — 轮椅使用者、视障、听障、婴儿车、老年人各有专属建议
5. **优惠政策** — 国内5A景区残障人士免票或半价政策提示
6. **预约渠道** — 免费轮椅租借提前预约渠道和方法

## 能做什么

- 查询景点的无障碍设施信息（轮椅通道/卫生间/租借/路线）
- 查询酒店品牌的无障碍房型和设施详情
- 根据需求类型和目的地提供出行建议
- 标注景区对残障人士的优惠政策

## 不能做什么

- 不提供实时无障碍设施变更信息（如临时维修关闭）
- 不覆盖所有景点和酒店，目前仅收录30+热门5A景区和10+主流品牌
- 不提供无障碍出租车在线预约
- 不替代医院的出行医疗建议

## 使用提示

- 查询景点时加上城市名更准确，如"北京故宫"而非仅"故宫"
- wheelchair类型涵盖轮椅和婴儿车，两者对通道宽度需求高度重合
- 部分景点提供免费轮椅租借但数量有限，建议提前预约
- 景区无障碍路线通常比常规路线长但坡度缓，预留更多时间
- 老年出行建议侧重路线平缓度和休息点

## 🔗 搭配使用

- **亲子出行助手** — 带娃出行的全面规划
- **高德地图全能版** — 导航到景点，查周边无障碍设施
- **景点智能推荐** — 适合无障碍游览的景点推荐

## 数据流向

所有数据为本地内置，不发送任何外部请求，不收集用户数据。
