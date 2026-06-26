---
name: gaode-map-pro
description: 零配置即装即用｜17项地图能力一次调用｜含路线规划和周边搜索｜驾车公交步行骑行全覆盖
tags: [高德地图, 地图查询, 路线规划, 导航, 周边搜索, POI搜索, 天气查询, 地理编码, 逆地理编码, IP定位, gaode, map, amap]
tools:
  - name: tool_geocode
    description: 地理编码，地址转经纬度
    primaryEnv: GAODE_PROXY_URL
    env:
      - name: GAODE_PROXY_URL
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
  - name: tool_schema_take_taxi
    description: 唤端打车
    parameters:
      - name: params
        type: string
        description: 查询参数
        required: true
---

# 高德地图全能版

零配置即装即用的高德地图技能，免申请Key即用，22项地图能力全覆盖。

## 能做什么

- **地理编码**：地址转经纬度、经纬度转地址
- **POI搜索**：关键词搜索、周边搜索、POI详情、输入提示自动补全
- **行政区划**：查询省市区行政区划信息
- **路线规划**：驾车/公交/步行/骑行，支持坐标版和地址版
- **天气查询**：查询城市实时天气
- **IP定位**：根据IP获取位置
- **距离测量**：两点间距离
- **静态地图**：生成静态地图图片
- **坐标转换**：不同坐标系间转换
- **唤端导航**：唤起高德地图APP导航
- **唤端打车**：唤起高德地图APP打车

## 不能做什么

- 唤端导航/打车需要用户手机安装高德地图APP，无法在纯对话环境直接导航或打车
- 坐标格式统一为"经度,纬度"（高德坐标系），不是"纬度,经度"

## 使用示例

1. "帮我查上海外滩的经纬度"
2. "从人民广场到外滩怎么走"
3. "搜一下附近有什么好吃的"
4. "今天上海天气怎么样"
5. "帮我叫个车去浦东机场"

## 注意事项

- 坐标格式为"经度,纬度"
- 查询通过云端代理转发到高德地图API，代理不存储用户数据
- 唤端功能需要用户设备安装高德地图APP

## 使用提示

- 先用IP定位获取当前位置 → 再用周边搜索找附近 → 用唤端打车前往
- 用POI搜索找到目的地 → 用地址版路线规划查路线 → 用唤端导航前往
- 公交路线规划需要指定城市名
