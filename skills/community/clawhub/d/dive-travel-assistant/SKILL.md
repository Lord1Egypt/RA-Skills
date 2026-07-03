---
name: dive-travel-assistant
display_name: 潜水旅行助手
description: 潜水全链路一站式助手，覆盖潜点搜索、考证指南、安全检查、机票酒店交通美食预订，国内走飞猪高德国际走RG自动分流，零配置即装即用。
tags: [潜水, 海岛游, 潜水考证, PADI, 潜水目的地]
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

# 潜水旅行助手 — 从选潜点到考证到出行，全链路一站式覆盖

> 国内30+潜点+国际20+顶级潜点数据，机票酒店交通美食自动分流预订，国内走飞猪高德，国际走RG。

🔥 **核心亮点：**
- **潜点数据库** — 30+国内潜点(三亚/涠洲岛/千岛湖)+20+国际顶级潜点(诗巴丹/马尔代夫/帕劳)
- **考证全链路** — OW→AOW→Rescue→DM→Instructor+8个专长，含费用和热门考证地
- **安全全覆盖** — 减压病/气压伤/海洋生物/洋流/保险/身体条件6大主题
- **自动分流预订** — 国内走飞猪+高德，国际走RG，机票酒店交通美食一站搞定
- **零配置** — 免申请Key，装上就能用

## 快速入门

**3个开场白示例，复制即用：**

1. "三亚有哪些潜点，新手能去吗"
2. "OW证怎么考，大概多少钱"
3. "帮我查北京到三亚的机票和酒店，下周五出发住3晚"

## 核心能力

1. **潜点搜索** — 按级别/区域/类型筛选，覆盖珊瑚礁/沉船/洞穴/峭壁等类型
2. **考证指南** — 全链路证书信息+费用+时长+热门考证地推荐
3. **安全检查** — 6大安全主题知识库，含减压病预防和应急处理
4. **机票搜索** — 国内飞猪+国际RG，自动分流带预订链接
5. **酒店搜索** — 含潜店度假村推荐，国内外自动分流
6. **美食交通** — 潜点附近餐厅搜索+火车票/驾车路线规划

## 能做什么

- 搜索国内外潜水点，按级别、区域、类型筛选，返回潜点详情和最佳季节
- 查询潜水考证信息，覆盖OW到教练及各专长证书
- 查询潜水安全知识，含减压病、海洋生物伤害等6大主题
- 搜索潜水目的地机票、酒店、交通、美食

## 不能做什么

- 不提供实时水下能见度监测（数据为季节性参考值）
- 不替代专业潜水教练和医生的建议
- 不处理潜水装备购买和租赁
- 不提供潜水课程预约（仅提供考证信息参考）

## 使用提示

- 搜索潜点可组合筛选：如"东南亚 沉船 高级"
- 考证建议先看OW再根据兴趣选专长，AOW+Nitrox是最实用组合
- 潜水保险强烈推荐DAN，年费$35起含减压舱+医疗后送
- 潜水后18小时内不能乘坐飞机，安排行程时注意间隔

## 🔗 搭配使用

- **出行保障助手** — 潜水保险购买和旅行保险对比
- **目的地安全指数** — 查询潜水目的地的安全评级
- **签证聪明办** — 国际潜水目的地的签证要求

## 数据流向

潜点/考证/安全数据为本地内置；机票/酒店/交通通过云端代理转发至飞猪/高德/RG API，代理服务不存储用户数据。
