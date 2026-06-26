---
name: gaode-taxi
description: 零配置即装即用｜23项地图能力一键叫车｜含路线规划和周边搜索｜驾车公交步行骑行打车全覆盖
tags: [高德打车, 打车, 叫车, 出租车, 网约车, 路线规划, 导航, 周边搜索, gaode, taxi, ride]
tools:
  - name: tool_schema_take_taxi
    description: 唤端打车，一键叫车含预估费用和多车型对比
    primaryEnv: GAODE_TAXI_PROXY_URL
    env:
      - name: GAODE_TAXI_PROXY_URL
        description: 高德代理URL（自动配置，无需手动设置）
        required: false
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_geocode
    description: 地理编码，地址转经纬度
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_regeocode
    description: 逆地理编码，经纬度转地址
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_poi_search
    description: POI关键词搜索
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_poi_around
    description: 周边POI搜索
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_poi_detail
    description: POI详情查询
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_input_tips
    description: 输入提示，自动补全
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_district
    description: 行政区划查询
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_driving_route
    description: 驾车路线规划（坐标版）
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_transit_route
    description: 公交路线规划（坐标版）
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_walking_route
    description: 步行路线规划（坐标版）
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_cycling_route
    description: 骑行路线规划（坐标版）
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_driving_route_by_address
    description: 驾车路线规划（地址版）
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_transit_route_by_address
    description: 公交路线规划（地址版）
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_walking_route_by_address
    description: 步行路线规划（地址版）
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_cycling_route_by_address
    description: 骑行路线规划（地址版）
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_weather
    description: 天气查询
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_ip_location
    description: IP定位
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_distance
    description: 距离测量
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_staticmap
    description: 静态地图
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_coordinate_convert
    description: 坐标转换
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
  - name: tool_schema_navi
    description: 唤端导航
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
---

# 高德打车

零配置即装即用的高德打车技能，一键叫车含预估费用和多车型对比，另有路线规划、周边搜索等地图能力。

## 能做什么

- **一键叫车**：唤起高德地图APP打车，显示多车型预估费用
- **路线规划**：驾车/公交/步行/骑行，支持坐标版和地址版
- **周边搜索**：搜索附近POI
- **POI搜索**：按关键词搜索地点
- **地理编码**：地址转经纬度、经纬度转地址
- **天气查询**：查询城市实时天气
- **IP定位**：根据IP获取位置

## 不能做什么

- 唤端打车需要用户手机安装高德地图APP，无法在纯对话环境直接打车
- 坐标格式统一为"经度,纬度"（高德坐标系），不是"纬度,经度"

## 使用示例

1. "帮我叫个车去浦东机场"
2. "从这里到外滩打车多少钱"
3. "搜一下附近有什么餐厅"
4. "从人民广场到外滩怎么走"

## 注意事项

- 查询通过云端代理转发到高德地图API，代理不存储用户数据
- 唤端打车需要用户设备安装高德地图APP
- 打车费用为预估值，实际费用以行程结束为准

## 使用提示

- 先用IP定位获取当前位置 → 再用周边搜索找目的地 → 用唤端打车前往
- 用POI搜索找到目的地 → 用地址版路线规划查路线 → 用唤端打车叫车
