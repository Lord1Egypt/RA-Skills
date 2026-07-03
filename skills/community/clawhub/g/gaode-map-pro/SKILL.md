---
name: gaode-map-pro
display_name: "高德地图全能版"
description: 免申请Key即用，17项地图能力全覆盖：地理编码、POI搜索、周边搜索、驾车/公交/步行/骑行路线规划、天气查询、IP定位，出行必备地图工具。
tags: [高德地图, 路线规划, 周边搜索, 导航, 天气查询, 地理编码]
tools:
  - name: geocode
    description: 地址转经纬度坐标
  - name: regeocode
    description: 经纬度转详细地址
  - name: poi_search
    description: 关键词搜索兴趣点
  - name: poi_around
    description: 周边搜索兴趣点
  - name: poi_detail
    description: POI详情查询
  - name: input_tips
    description: 输入提示自动补全
  - name: district
    description: 行政区划查询
  - name: driving_route
    description: 驾车路线规划（坐标版）
  - name: transit_route
    description: 公交路线规划（坐标版）
  - name: walking_route
    description: 步行路线规划（坐标版）
  - name: cycling_route
    description: 骑行路线规划（坐标版）
  - name: driving_route_by_address
    description: 驾车路线规划（地址版）
  - name: transit_route_by_address
    description: 公交路线规划（地址版）
  - name: walking_route_by_address
    description: 步行路线规划（地址版）
  - name: cycling_route_by_address
    description: 骑行路线规划（地址版）
  - name: weather
    description: 天气查询
  - name: ip_location
    description: IP定位

---

# 高德地图全能版 — 17项地图能力，免Key即用，出行必备

> 一个技能覆盖地理编码、POI搜索、4种路线规划、天气查询、IP定位等全部地图需求，零配置装上就能用。

🔥 **核心亮点：**
- **17项能力** — 地理编码/逆编码/POI搜索/周边搜索/路线规划/天气/IP定位全覆盖
- **免Key即用** — 零配置，装上就能用，无需申请任何高德Key
- **双模式路线** — 每种出行方式都有坐标版和地址版，地址版自动转坐标更方便
- **4种出行方式** — 驾车/公交/步行/骑行路线规划，覆盖全场景
- **智能联动** — 工具间可串联使用，如IP定位→周边搜索→路线规划→打车

## 快速入门

**3个开场白示例，复制即用：**

1. "搜一下我附近有什么好吃的餐厅"
2. "从广州塔到珠江新城开车怎么走"
3. "广州今天天气怎么样"

## 核心能力

1. **地点搜索** — 关键词搜索POI、周边搜索、输入提示自动补全，快速定位目标
2. **路线规划** — 驾车/公交/步行/骑行四种方式，支持坐标和文字地址两种输入
3. **地理编码** — 地址转经纬度、经纬度转详细地址，双向转换
4. **天气查询** — 查询城市实时天气信息
5. **IP定位** — 根据IP地址自动获取当前位置
6. **行政区划** — 查询省市区行政边界和区划信息

## 工具参数说明

### 搜索类
- **poi_search**: keywords(必填), city(选填), types(选填), offset/page(分页)
- **poi_around**: location(必填,"lng,lat"), keywords(必填), radius(默认3000米), offset/page(分页)
- **poi_detail**: id(必填，POI的ID)
- **input_tips**: keywords(必填), city(选填), datatype(选填)

### 路线规划（坐标版）
- **driving_route/transit_route/walking_route/cycling_route**: origin(必填,"lng,lat"), destination(必填,"lng,lat")
- 公交额外需要city(必填), cityd(跨城必填)

### 路线规划（地址版，自动转坐标，更方便）
- **driving_route_by_address/transit_route_by_address/walking_route_by_address/cycling_route_by_address**: origin_address(必填), destination_address(必填), origin_city/destination_city(选填)

### 其他
- **geocode**: address(必填), city(选填)
- **regeocode**: location(必填,"lng,lat")
- **district**: keywords(选填), subdistrict(选填)
- **weather**: city(必填)
- **ip_location**: ip(选填，不填定位当前IP)

## 工具联动建议

- 模糊搜索地点：input_tips → poi_search → poi_detail
- 地址到路线：geocode → driving_route，或直接用 driving_route_by_address
- 定位到周边：ip_location → poi_around → 路线规划
- 区划到POI：district → poi_search

## 能做什么

- 搜索附近餐厅、酒店、景点、停车场等POI
- 规划驾车/公交/步行/骑行路线，支持文字地址输入
- 地址与经纬度双向转换
- 查询城市实时天气
- 根据IP自动定位
- 查询行政区划信息

## 不能做什么

- 不提供实时交通路况信息
- 不提供导航语音指引
- 步行路线最大100km，骑行最大500km，超出范围会报错
- 不支持地图瓦片渲染（纯数据接口）

## 使用提示

- 地址版路线工具（_by_address后缀）内置地址转坐标，用起来更方便
- POI搜索和周边搜索默认返回20条，可用offset和page翻页
- 地址解析失败时建议补充完整地址或填写city参数
- 公交路线规划需要填写城市名

## 🔗 搭配使用

- **高德打车** — 查完路线后一键叫车出发
- **天气查询** — 出行前查目的地天气做好准备
- **全能旅行助手** — 行程规划+酒店机票一站式服务

## 数据流向

用户输入（查询参数）→ 本技能脚本 → 高德地图代理 → 数据源API → 返回结果给用户。查询参数会发送到高德地图代理以获取实时数据，代理服务不存储用户数据。
