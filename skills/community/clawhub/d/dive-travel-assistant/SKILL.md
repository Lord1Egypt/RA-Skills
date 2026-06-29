---
name: dive-travel-assistant
display_name: "潜水旅行助手"
description: "零配置即装即用，覆盖潜水全链路服务——潜点搜索、考证指南、安全检查，以及机票酒店交通美食预订，国内走飞猪高德国际走RG自动分流，所有预订链路支持分佣。"
tags: [潜水, 海岛, 考证, PADI, 旅行, 预订, 机票, 酒店, 安全, 美食, dive, scuba]
tools:
  - name: dive_site_search
    description: 搜索国内外潜水点，支持按关键词、级别、区域、类型筛选，返回潜点详情、最佳季节、能见度、水温、所需证书等级等
    parameters:
      - name: keyword
        type: string
        description: 搜索关键词，如三亚、仙本那、沉船、洞穴
        required: false
      - name: level
        type: string
        description: 潜水级别筛选，如初级/中级/高级/OW/AOW
        required: false
      - name: region
        type: string
        description: 区域筛选，如国内/东南亚/太平洋/印度洋
        required: false
      - name: site_type
        type: string
        description: 潜点类型筛选，如珊瑚礁/沉船/洞穴/峭壁
        required: false
      - name: limit
        type: integer
        description: 返回结果数量，默认10
        required: false
  - name: dive_cert_guide
    description: 查询潜水考证信息，覆盖OW到教练及各专长证书，含费用、时长、前置条件、热门考证地推荐
    parameters:
      - name: cert
        type: string
        description: 证书名称，如OW/AOW/Rescue/DM/Nitrox/Deep/Wreck/Cave
        required: false
  - name: dive_safety_check
    description: 查询潜水安全信息，覆盖减压病、气压伤、海洋生物伤害、洋流安全、潜水保险、身体条件等
    parameters:
      - name: topic
        type: string
        description: 安全主题，如减压病/气压伤/海洋生物/洋流/保险/身体条件
        required: false
  - name: search_dive_flights
    description: 搜索潜水目的地机票，国内自动走飞猪，国际自动走RG，返回航班和预订链接
    parameters:
      - name: origin
        type: string
        description: 出发城市
        required: true
      - name: destination
        type: string
        description: 到达城市或潜点
        required: true
      - name: date
        type: string
        description: 出发日期，格式YYYY-MM-DD
        required: true
  - name: search_dive_hotels
    description: 搜索潜水目的地酒店，国内自动走飞猪，国际自动走RG，返回酒店价格和预订链接
    parameters:
      - name: city
        type: string
        description: 城市或目的地名
        required: true
      - name: checkin
        type: string
        description: 入住日期，格式YYYY-MM-DD
        required: true
      - name: checkout
        type: string
        description: 离店日期，格式YYYY-MM-DD
        required: true
      - name: keyword
        type: string
        description: 关键词，如潜水、潜店、度假村
        required: false
  - name: search_dive_transport
    description: 搜索潜水目的地交通，国内火车票(飞猪)+驾车路线(高德)，返回时刻表和路线规划
    parameters:
      - name: origin
        type: string
        description: 出发地
        required: true
      - name: destination
        type: string
        description: 目的地
        required: true
      - name: date
        type: string
        description: 出发日期，格式YYYY-MM-DD
        required: false
      - name: transport_type
        type: string
        description: 交通类型，train/taxi，不传则同时查询
        required: false
  - name: search_dive_food
    description: 搜索潜水目的地附近餐厅，基于高德POI数据，支持菜系筛选，返回评分、价格和距离
    parameters:
      - name: location
        type: string
        description: 地点、景点或潜店名
        required: true
      - name: cuisine
        type: string
        description: 菜系偏好，如海鲜、川菜、西餐
        required: false
      - name: radius
        type: integer
        description: 搜索半径(米)，默认3000
        required: false
      - name: limit
        type: integer
        description: 返回结果数量，默认8
        required: false
---

# 潜水旅行助手

从选潜点到考证到出行到安全，一站式覆盖潜水旅行全链路。国内30+潜点+国际20+顶级潜点数据，机票酒店交通美食自动分流预订。

## 能做什么

- **潜点搜索**：30+国内潜点(三亚/涠洲岛/千岛湖/小琉球/绿岛等)+20+国际顶级潜点(诗巴丹/马尔代夫/帕劳/红海等)，按级别/区域/类型筛选
- **考证指南**：OW→AOW→Rescue→DM→Instructor全链路+8个专长(Nitrox/Deep/Wreck/Cave等)，含费用、时长、热门考证地
- **安全检查**：减压病/气压伤/海洋生物伤害/洋流安全/潜水保险/身体条件6大安全主题
- **机票搜索**：国内自动走飞猪，国际自动走RG，带预订链接
- **酒店搜索**：国内飞猪+国际RG自动分流，含潜店度假村推荐
- **交通查询**：火车票(飞猪)+驾车路线(高德)+机场提示
- **美食搜索**：基于高德POI搜索潜点附近餐厅，支持菜系筛选

## 不能做什么

- 不提供实时水下能见度监测(数据为季节性参考值)
- 不替代专业潜水教练和医生的建议
- 不处理潜水装备购买和租赁
- 不提供潜水课程预约(仅提供考证信息参考)

## 使用示例

1. "我想去三亚潜水，有哪些潜点？"
2. "OW证怎么考？大概多少钱？"
3. "减压病怎么预防和处理？"
4. "帮我查北京到三亚的机票和酒店，下周五出发住3晚"
5. "仙本那潜水怎么样？周边有什么好吃的？"
6. "从广州到涠洲岛怎么去？有火车吗？"

## 注意事项

- 潜点能见度、水温为季节参考值，实际受天气和洋流影响
- 安全信息仅供参考，紧急情况请联系当地救援和DAN热线
- 机票酒店价格为实时查询结果，最终以预订页面为准
- 潜水有风险，请确保持有效证书并在能力范围内潜水
- **数据流向**：脚本通过SCF代理调用飞猪/RG/高德API，不直接暴露凭证

## 使用提示

- 搜索潜点时可组合筛选：如"东南亚 沉船 高级"
- 考证建议先看OW再根据兴趣选专长，AOW+Nitrox是最实用组合
- 预订链路均有分佣：国内走飞猪(RG 5%佣金)，国际走RG
- 潜水保险强烈推荐DAN，年费$35起含减压舱+医疗后送
