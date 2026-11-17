---
name: 智能旅行助手
display_name: 智能旅行助手
description: 多源聚合旅行助手——覆盖行程规划、酒店/机票/火车票/景点门票搜索、品牌酒店、美食推荐、市内交通9大功能，数据源整合途牛+TourMind+高德，零配置即装即用
version: "1.4.7"
author: mako2026
license: MIT-0
tags:
  - travel
  - hotel
  - flight
  - train
  - 旅行
  - 门票
  - 途牛
  - 多源聚合
tools:
  - name: travelPlan
    description: 行程规划，用自然语言描述旅行需求，智能推荐含交通住宿景点的行程方案
    parameters:
      - name: query
        type: string
        description: 旅行需求，自然语言，如"三亚5天亲子游"、"周末杭州2日游"
        required: true
  - name: fastSearch
    description: 极速搜索，快速搜索全品类旅行产品（酒店/机票/景点/火车票）
    parameters:
      - name: query
        type: string
        description: 搜索关键词，如"上海迪士尼门票"、"北京到上海机票"
        required: true
  - name: hotelSearch
    description: 搜索酒店，返回酒店列表含价格、评分和预订链接
    parameters:
      - name: destination
        type: string
        description: 目的地城市，如"上海"、"北京"
        required: true
      - name: extra
        type: string
        description: 补充信息，如"外滩附近 明天入住"
        required: false
  - name: flightSearch
    description: 机票查询，查国内航班实时票价、航班号和起降时间
    parameters:
      - name: origin
        type: string
        description: 出发地城市，如"北京"
        required: true
      - name: destination
        type: string
        description: 目的地城市，如"上海"
        required: false
      - name: depDate
        type: string
        description: 出发日期，格式YYYY-MM-DD
        required: false
      - name: backDate
        type: string
        description: 回程日期，格式YYYY-MM-DD
        required: false
      - name: seatClass
        type: string
        description: 舱位等级，如经济舱、公务舱
        required: false
      - name: directOnly
        type: boolean
        description: 是否只看直飞
        required: false
  - name: trainSearch
    description: 火车票查询，查高铁/动车/火车票余票、票价和时刻表
    parameters:
      - name: origin
        type: string
        description: 出发地城市，如"北京"
        required: true
      - name: destination
        type: string
        description: 目的地城市，如"上海"
        required: false
      - name: depDate
        type: string
        description: 出发日期，格式YYYY-MM-DD
        required: false
      - name: seatClass
        type: string
        description: 座位等级，如商务座、一等座、二等座
        required: false
      - name: trainType
        type: string
        description: 车型，如高铁、动车、火车
        required: false
      - name: onlyHasStock
        type: boolean
        description: 是否只看有票
        required: false
  - name: poiSearch
    description: 景点门票搜索，查景点门票价格、评分和预订链接
    parameters:
      - name: destination
        type: string
        description: 目的地城市，如"北京"
        required: true
      - name: keyword
        type: string
        description: 景点关键词，如"迪士尼"
        required: false
  - name: brandHotelSearch
    description: 品牌酒店搜索，搜热门品牌酒店含价格和预订链接
    parameters:
      - name: destination
        type: string
        description: 目的地城市，如"上海"、"北京"
        required: true
      - name: extra
        type: string
        description: 补充信息，如"行政酒廊"
        required: false
  - name: brandHotelDetail
    description: 品牌酒店详情，获取单个酒店的详细信息和房型
    parameters:
      - name: hotelId
        type: string
        description: 酒店ID，从搜索结果获取
        required: true
  - name: brandPackageSearch
    description: 品牌套餐搜索，搜酒店套餐产品
    parameters:
      - name: destination
        type: string
        description: 目的地城市，如"三亚"
        required: true
      - name: extra
        type: string
        description: 补充信息，如"亲子套餐"
        required: false
  - name: foodSearch
    description: 美食推荐，推荐目的地周边美食餐厅含评分和人均
    parameters:
      - name: destination
        type: string
        description: 目的地/地标，如"上海外滩"
        required: true
      - name: keyword
        type: string
        description: 美食类型，如"火锅"
        required: false
  - name: transportSearch
    description: 市内交通，查询城市内两地公交/地铁路线
    parameters:
      - name: origin
        type: string
        description: 出发地，如"上海虹桥站"
        required: true
      - name: destination
        type: string
        description: 目的地，如"外滩"
        required: true
      - name: city
        type: string
        description: 所在城市，如"上海"
        required: false
---

# 智能旅行助手

多源聚合旅行技能，覆盖行程规划、酒店、机票、火车票、景点门票、品牌酒店、美食推荐、市内交通9大品类。数据源整合途牛、TourMind、高德，价格真实、带预订链接。

## ✅ 能做什么

| 功能 | 说明 |
|------|------|
| 🗺 行程规划 | 自然语言描述需求，智能生成含交通住宿景点的完整行程 |
| 🏨 酒店搜索 | 按城市/区域查酒店，返回价格/评分/预订链接（途牛+TourMind双源） |
| ✈️ 机票查询 | 查国内航班价格/时刻/航司，支持单程往返 |
| 🚄 火车票查询 | 查高铁/动车/普速车次余票、票价和坐席 |
| 🎫 景点门票 | 查景点门票价格和预订链接 |
| 🏢 品牌酒店 | 品牌酒店搜索、详情、套餐 |
| 🍜 美食推荐 | 周边美食餐厅推荐，含评分人均地址 |
| 🚇 市内交通 | 公交/地铁路线查询，含打车参考 |
| ⚡ 极速搜索 | 全品类快速智能检索 |

## ⚠️ 不能做什么

- 不支持在线下单/支付，预订链接跳转对应平台完成
- 日期请用自然语言或YYYY-MM-DD格式描述

## 🔒 数据安全

所有查询通过云端代理转发，API密钥仅存储在服务端，客户端零密钥，保障数据安全。代理不存储用户数据。

## 💡 使用提示

- 酒店搜索支持补充区域、星级、日期，如`extra="外滩附近 明天入住"`
- 机票搜索可筛选舱位和直飞，如`seatClass="经济舱", directOnly=true`
- 行程规划支持复杂需求，如`query="三亚5天亲子游 预算1万"`
