---
name: fliggy-travel
display_name: "飞猪旅行"
description: 零配置即装即用｜11项工具酒店机票门票火车票万豪｜含图片和预订链接｜飞猪官方数据直连
tags: [飞猪旅行, 飞猪酒店, 飞猪机票, 飞猪火车票, 飞猪门票, 万豪酒店, 行程规划, 旅行助手, fliggy, travel, booking]
tools:
  - name: travel_plan
    description: 飞猪行程规划，智能推荐行程方案
    primaryEnv: FLIGGY_PROXY_URL
    env:
      - name: FLIGGY_PROXY_URL
        description: 飞猪代理URL（自动配置，无需手动设置）
        required: false
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"3天2晚上海游"
        required: true
  - name: search_train
    description: 搜索飞猪火车票
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"北京到上海明天的火车"
        required: true
  - name: search_flight
    description: 搜索飞猪机票
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"上海到三亚7月1号机票"
        required: true
  - name: search_hotel
    description: 搜索飞猪酒店
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"杭州西湖附近酒店"
        required: true
  - name: search_poi
    description: 搜索飞猪景点门票
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"上海迪士尼门票"
        required: true
  - name: search_food
    description: 搜索附近美食推荐
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"外滩附近美食"
        required: true
  - name: search_transport
    description: 查询市内交通方案
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"从虹桥到浦东怎么走"
        required: true
  - name: search_fast
    description: 极速搜索酒店+景点
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"三亚酒店和景点"
        required: true
  - name: search_marriott_hotel
    description: 搜索万豪集团酒店
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"上海万豪酒店"
        required: true
  - name: get_marriott_hotel_info
    description: 获取万豪酒店详情
    parameters:
      - name: params
        type: string
        description: 酒店名称或关键词
        required: true
  - name: search_marriott_package
    description: 搜索万豪酒店套餐
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"万豪含早套餐"
        required: true
---

# 飞猪旅行

零配置即装即用的飞猪旅行查询技能，9项工具覆盖酒店、机票、门票、火车票、万豪、美食、交通、行程规划，飞猪官方数据直连。

## 能做什么

- **行程规划**：智能推荐行程方案，涵盖景点+酒店+交通
- **火车票搜索**：查车次、票价、余票
- **机票搜索**：查航班价格、时刻、航司
- **酒店搜索**：按城市/区域/品牌查酒店，含价格和退改政策
- **景点门票**：查景点门票价格和预订链接
- **美食推荐**：搜索附近美食，含评分和距离
- **市内交通**：查询公交/地铁/驾车/步行路线
- **万豪酒店**：搜索万豪集团旗下酒店详情和套餐
- **极速搜索**：一次查询同时返回酒店+景点

## 不能做什么

- 不支持在线下单/支付，预订链接跳转飞猪APP或网页完成
- 部分小城市数据覆盖可能不完整，建议用大城市名查询
- 不支持查询已预订订单状态

## 使用示例

1. "帮我规划一个3天2晚的上海游"
2. "查北京到上海明天的火车票"
3. "杭州西湖附近500元以内的酒店"
4. "上海迪士尼门票多少钱"
5. "上海万豪酒店有什么套餐"

## 注意事项

- 价格实时变动，以实际预订页面为准
- 查询通过云端代理转发到飞猪和高德地图API，代理不存储用户数据
- 万豪酒店数据来自飞猪万豪专区

## 使用提示

- 行程规划工具可一次推荐多日行程，无需分天查询
- 美食搜索基于高德地图数据，自动定位周边
- 火车票搜索支持高铁/动车筛选
