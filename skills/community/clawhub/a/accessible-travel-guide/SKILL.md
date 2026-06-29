---
name: accessible-travel-guide
display_name: "无障碍旅行助手"
description: "零配置即装即用，提供3项无障碍出行工具，支持景点/酒店/交通无障碍设施查询和出行建议，基于国内30+热门景区及主流酒店品牌实地数据。"
tags: [无障碍旅行, 轮椅出行, 残障旅行, 银发旅游, 无障碍设施, 景点无障碍, 酒店无障碍, 老年出行, 婴儿车出行, 无障碍通道, accessible travel, wheelchair travel]
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

# 无障碍旅行助手

查询国内热门景点和酒店的无障碍设施信息，为轮椅使用者、视障听障人士、老年人和带婴儿车出行者提供出行建议。覆盖30+5A景区和10+主流酒店品牌，基于实地调研数据。

## 能做什么

- **景点无障碍查询**：输入景点名称，返回轮椅通道、无障碍卫生间、轮椅租借点、无障碍游览路线等信息，标注具体位置和开放情况
- **酒店无障碍查询**：输入酒店品牌和城市，返回无障碍客房房型、房门宽度、浴室扶手、电梯规格等设施详情
- **出行建议**：根据需求类型（轮椅/视障/听障/婴儿车/老年）和目的地，提供交通选择、装备清单、预约渠道、优惠政策等实用建议

## 不能做什么

- 不提供实时无障碍设施变更信息（如临时维修关闭），建议出行前电话确认
- 不覆盖所有景点和酒店，目前仅收录30+热门5A景区和10+主流酒店品牌
- 不提供无障碍出租车或特殊交通的在线预约，仅给预约渠道建议
- 不替代医院的出行医疗建议，术后恢复期出行请遵医嘱

## 使用示例

1. "故宫轮椅能进吗？有哪些殿可以看？"
2. "万豪酒店有没有无障碍房？"
3. "坐轮椅去西安旅游有什么建议？"
4. "带老人去杭州西湖方便吗？"
5. "推婴儿车逛外滩有推荐路线吗？"

## 注意事项

- 景点和酒店的无障碍设施可能因装修或政策调整而变化，出行前建议电话确认
- 部分景点提供免费轮椅租借但数量有限，建议提前预约
- 所有数据为本地内置，不发送任何外部请求，不收集用户数据
- 国内部分5A景区对残障人士有免票或半价政策，出行建议中会提示

## 使用提示

- 查询景点时加上城市名更准确，如"北京故宫"而非仅"故宫"
- wheelchair类型涵盖轮椅使用者和推婴儿车出行，两者对通道宽度和坡度的需求高度重合
- 老年出行建议侧重路线平缓度和休息点，不涉及医疗内容
- 视障/听障出行建议侧重景区辅助服务（语音导览/手语服务）和交通衔接
- 景区无障碍路线通常比常规路线长但坡度缓，预留更多游览时间

## 数据流向

所有数据为本地内置，不发送任何外部请求，不收集用户数据。

