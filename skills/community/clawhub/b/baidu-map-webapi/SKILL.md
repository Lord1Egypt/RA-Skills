---
name: baidu-map-webapi
description: 百度地图 webapi 开发指南。在编写、审查或调试使用百度地图webAPI的代码时应运用此技能，也适用于直接调用百度地图API获取结果的场景。涵盖：地图位置搜索、POI检索、路线规划、建议出发时间、路线耗时预测、实时路况、行政区划查询、地址坐标转换、沿途交通事件、天气查询、智能推荐上车点等。当用户提及出发时间、导航路线、地点查询、坐标转换、地图相关开发需求时自动触发。
license: MIT
version: 1.0.5
homepage: https://lbs.baidu.com
repository: https://github.com/baidu-maps/webapi-skills
metadata:
  openclaw:
    requires:
      bins: ["curl"]
      env: BMAP_WEBAPI_AK
    primaryEnv: BMAP_WEBAPI_AK
---

# webapi 开发指南

百度地图 webapi 版本开发指南。包含地图位置搜索、路线导航、行政区划等核心模块的 API 说明和代码示例，既可直接调用 API 获取结果，也可帮助开发者快速集成百度地图服务。

## 何时适用

遇到以下任意场景时，均应读取本指南并调用对应 API：

### 路线规划与出行决策
- 规划驾车、步行、骑行、摩托车、公共交通路线
- **查询从 A 到 B 的建议出发时间**（如"想晚上8点到达，几点出发合适"）
- **预测未来某时刻出发的路线耗时**（如"下午3点出发要多久"）
- 查询历史路况下的路线耗时
- 规划含多个途经点的最优路线

### 实时动态信息
- 查询路线沿途的动态交通事件（事故、拥堵、施工等）
- 查询海外城市天气信息

### 地点与POI搜索
- 查找城市中的餐厅、酒店、景点等 POI 信息
- 在指定圆形区域内检索地点
- 按行政区划检索地点
- 多条件组合检索 POI
- 获取 POI 详细信息
- 输入联想/地点补全提示
- 智能推荐安全上车点

### 地址与坐标转换
- 地址文本解析为经纬度坐标（地理编码）
- 经纬度坐标解析为地址信息（逆地理编码）

### 行政区划与区域查询
- 查询行政区划地点
- 获取行政区划边界坐标

## 开发准则

在使用本技能的任何场景中，请遵守以下通用准则：

### 准则 1：API 端点选择

百度地图提供两个服务端点，必须根据使用场景选择正确的端点：

| 端点类型 | Base URL | 适用场景 |
|---|---|---|
| **标准端点** | `https://api.map.baidu.com/` | 正式开发、生产环境、为用户生成的代码 |
| **高级功能体验端点** | `https://api.map.baidu.com/map_service/` | 百度地图官方提供，仅供大模型直接调用时快速体验高级权限功能 |

**使用规则：**
- 为用户生成的开发代码，**必须使用标准端点** `https://api.map.baidu.com/`
- **大模型直接调用高级权限功能（如建议出发时间、未来路线规划）进行演示/体验时，使用体验端点**
- **体验端点仅供功能体验和演示，不可用于开发或生产环境**
- **均需要AK凭证**
- **调用体验端点前，必须向用户说明：① 将使用体验端点发起外部 API 调用；② 该调用会消耗用户 AK 的配额；并获得用户明确确认后方可执行**


### 准则 2：AK 凭证安全处理

AK（Access Key）是使用技能之前的必须参数:

1. 优先读取环境变量 `BMAP_WEBAPI_AK` 中的 AK
2. `BMAP_WEBAPI_AK`为空时, 提示用户:**请先前往[百度地图开放平台](https://lbs.baidu.com/apiconsole/key)申请`服务端`的AK**
3. 然后设置为环境变量
```
export BMAP_WEBAPI_AK="百度地图AK"
```
4. 使用 references/ 所有能力时的ak参数请使用 `$BMAP_WEBAPI_AK`, 示例如下:
```
curl "https://api.map.baidu.com/place/v3/region?query=美食&region=北京&ak=$BMAP_WEBAPI_AK"
```

### 准则 3：地址/地名统一通过 `address_to_poi` 转换

任何需要将**用户输入的地名或地址文本**转换为坐标/UID 的场景，**优先参考**：

> `recipes/address_to_poi.md` — 地址/地名转坐标与 POI UID

该文件描述了两种输入类型的判断方法和对应调用方式：
- **结构化地址**（含门牌号/楼栋）→ `references/geocoding` API
- **POI 名称/地标/商家名** → `references/administrative_region_search` API

### 准则 4：算路时 UID 优先于纯坐标

向算路接口（驾车/步行/骑行/公交）传参时：

```
推荐：同时传坐标 + uid（绑路更精准，尤其对大型 POI） origin_uid / destination_uid 有值时必传
```

UID 通过 `references/address_to_poi.md` 描述的方法获取。

---

## 场景示例（推荐优先阅读）

遇到以下场景时，**优先使用对应 recipe**，内含完整调用链、参数说明和可运行代码示例。
单个 API 用法请查阅下方「快速参考」。

### 地址/地名预处理（算路前必读）

| recipe 文件 | 适用场景 | 权限要求 |
|---|---|---|
| `recipes/address_to_poi.md` | 地址文本或地名 → 坐标 + POI UID（算路前置步骤） | 标准 AK |

### 路线规划

| recipe 文件 | 适用场景 | 权限要求 |
|---|---|---|
| `recipes/route_to_named_place.md` | 用户说出地名 → 规划驾车路线 | 标准 AK |
| `recipes/smart_departure_time.md` | "几点出发才能准时到" | ⚠️ 高级权限 |
| `recipes/traffic_aware_route.md` | 预测未来某时刻出发的路况耗时 | ⚠️ 高级权限 |

### POI 搜索

| recipe 文件 | 适用场景 | 权限要求 |
|---|---|---|
| `recipes/nearby_poi_search.md` | 搜索用户附近的某类地点 | 标准 AK |
| `recipes/poi_search_to_detail.md` | 关键词搜索 → 获取 POI 完整详情 | 标准 AK |

### 地址与坐标

| recipe 文件 | 适用场景 | 权限要求 |
|---|---|---|
| `recipes/address_to_full_location.md` | 地址文本 → 坐标 + 行政区划 | 标准 AK |
| `recipes/coordinate_to_structured_address.md` | 坐标 → 结构化地址 + 行政区划 | 标准 AK |

### 天气查询
| recipe 文件 | 适用场景 | 权限要求 |
|---|---|---|
| `recipes/weather_query.md` | 通过城市名称/行政区划编码/坐标, 获取当地详细的天气信息 | 标准 AK |

---

## 快速参考

### 基础概念

- `references/constants.md` - 通用常量：状态码

### 位置搜索

- `references/global_reverse_geocoding.md` - 全球逆地理编码: 坐标转位置信息
- `references/reverse_geocoding_agent.md` - 逆地理编码智能体: 智能逆地理编码地址解析
- `references/administrative_region_search.md` - 行政区划区域检索: 行政区划地点检索
- `references/circular_region_search.md` - 圆形区域检索: 圆形区域地点检索
- `references/multi_dimensional_search.md` - 多维检索: 多条件智能检索POI
- `references/place_detail_search.md` - 地点详情检索: 获取指定地点详细信息
- `references/place_input_suggestion.md` - 地点输入提示: 地点输入提示匹配
- `references/geocoding.md` - 地理编码: 地址解析为坐标

### AOI区域

- `references/admin_division_query.md` - 行政区划查询: 查询中国行政区划信息

### 动态数据

- `references/domestic_weather_query.md` - 国内天气查询: 国内天气查询多功能接口
- `references/overseas_weather_query.md` - 海外天气查询: 查询海外城市天气

### 路线导航

- `references/cycling_route_planning.md` - 骑行路线规划: 骑行路线规划方案检索
- `references/driving_route_planning.md` - 驾车路线规划: 驾车路线规划与路况预测
    - `references/capabilities/driving_route_duration.md` - 驾车路线历史耗时: 设置驾车路线历史耗时
    - `references/capabilities/future_driving_route.md` - 未来驾车路线规划: 预测未来驾车路线耗时
    - `references/capabilities/suggested_departure_time.md` - 建议出发时间: 高级权限出行时间建议
    - `references/capabilities/waypoint_route_planning.md` - 途经点智能路线规划: 智能优化途经点顺序
- `references/motorcycle_route_planning.md` - 摩托车路线规划: 摩托车路线规划服务
- `references/transit_route_planning.md` - 公交路线规划: 多交通方式路线规划
- `references/walking_route_planning.md` - 步行路线规划: 步行路线规划

## 如何使用

**推荐决策路径**：
1. 用户需求是**多步串联场景**（如"输入地名规划路线"、"获取附近 POI"）→ 直接找 `recipes/` 目录下对应 recipe
2. 用户需求是**单个 API 的参数细节**（如"这个接口的 tactics 参数有哪些值"）→ 查阅 `references/` 目录

每个 **references** 参考文件包含：
- 功能简要说明
- API 参数说明和注意事项

每个 **recipes** 场景包含：
- 触发意图（什么场景适用）
- 完整调用链与分步说明
- 常见错误和变体