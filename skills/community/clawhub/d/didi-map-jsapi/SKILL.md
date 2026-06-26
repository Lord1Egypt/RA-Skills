---
name: didi-jsapi
description: 滴滴地图 JSAPI 开发指南。在编写、审查或调试使用滴滴地图 API 的代码时应运用此技能。适用于涉及地图初始化、标记、覆盖物、图层管理、事件处理、控件交互或性能优化的任务。当用户提及 DiMap、滴滴地图、didi-jsapi 或相关地图开发需求时自动触发。
license: MIT
version: 1.0.0
---

# 滴滴地图 JSAPI 开发指南

滴滴地图 JSAPI 开发指南。包含地图初始化、安全密钥配置、标记、覆盖物、事件、图层等核心模块的 API 说明和代码示例，旨在帮助开发者快速集成滴滴地图并遵循正确的使用方式。

## 何时适用

在以下场景中参考这些指南：

- 创建新的地图页面或组件
- 配置安全密钥和代理服务器
- 在地图上添加标记、折线、多边形等覆盖物
- 处理地图交互事件（点击、拖拽、缩放等）
- 配置地图样式或切换图层
- 调试地图渲染或性能问题

## 快速参考

### 0. 安全认证

- `references/jsapi-auth.md` - 安全密钥配置：代理服务器转发、明文方式设置

### 1. 基础类

- `references/coordinate-lnglat.md` - 经纬度类：LngLat 构造、转换
- `references/coordinate-lnglatbounds.md` - 经纬度边界：LngLatBounds 构造、扩展
- `references/coordinate-point.md` - 屏幕坐标点：Point 构造
- `references/coordinate-mercator.md` - 墨卡托坐标：MercatorCoordinate 转换

### 2. 地图核心

- `references/map.md` - 地图类：Map 初始化、视图控制、交互处理
- `references/base-evented.md` - 事件基类：Evented 事件监听、触发
- `references/base-supported.md` - 浏览器支持检测

### 3. 标记与覆盖物

- `references/marker.md` - 点标记：Marker 构造、位置、拖拽
- `references/marker-cluster.md` - 点聚合：MarkerCluster 聚合配置
- `references/overlay-base.md` - 覆盖物基类：OverlayBase 通用方法
- `references/overlay-circle.md` - 圆形覆盖物：Circle 构造、半径
- `references/overlay-circlemarker.md` - 圆形标记：CircleMarker 构造
- `references/overlay-polygon.md` - 多边形：Polygon 构造、坐标
- `references/overlay-polyline.md` - 折线：Polyline 构造、样式
- `references/overlay-rectangle.md` - 矩形：Rectangle 构造、边界
- `references/overlay-heatmap.md` - 热力图：Heatmap 数据、样式
- `references/overlay-labellayer.md` - 标签图层：LabelLayer 管理
- `references/overlay-labelmarker.md` - 标签标记：LabelMarker 文本

### 4. 弹窗

- `references/popup.md` - 弹出窗口：Popup 构造、内容、位置

### 5. 控件

- `references/control-attribution.md` - 版权控件：AttributionControl
- `references/control-fullscreen.md` - 全屏控件：FullscreenControl
- `references/control-geolocate.md` - 定位控件：GeolocateControl
- `references/control-navigation.md` - 导航控件：NavigationControl
- `references/control-scale.md` - 比例尺控件：ScaleControl
- `references/control-measure.md` - 测量控件：Measure 距离、面积

### 6. 矢量图层

- `references/vector-base-layer.md` - 图层基类：BaseLayer 通用方法
- `references/vector-base-feature.md` - 要素基类：BaseFeature 通用方法
- `references/vector-circle-layer.md` - 圆形图层：CircleLayer
- `references/vector-circle-feature.md` - 圆形要素：CircleFeature
- `references/vector-heatmap-layer.md` - 热力图图层：HeatmapLayer
- `references/vector-heatmap-feature.md` - 热力图要素：HeatmapFeature
- `references/vector-polygon-layer.md` - 多边形图层：PolygonLayer
- `references/vector-polygon-feature.md` - 多边形要素：PolygonFeature
- `references/vector-polygon-extrusion-layer.md` - 3D多边形图层：PolygonExtrusionLayer
- `references/vector-polygon-extrusion-feature.md` - 3D多边形要素：PolygonExtrusionFeature
- `references/vector-polyline-layer.md` - 折线图层：PolylineLayer
- `references/vector-polyline-feature.md` - 折线要素：PolylineFeature
- `references/vector-symbol-layer.md` - 符号图层：SymbolLayer
- `references/vector-symbol-feature.md` - 符号要素：SymbolFeature

### 7. 编辑器

- `references/editor-shape.md` - 图形编辑器：ShapeEdit 绘制、编辑

### 8. 服务

- `references/service-geocode.md` - 地理编码服务：GeoCodeService 地址转坐标
- `references/service-poi.md` - POI 搜索服务：PoiService 地点搜索
- `references/service-route.md` - 路径规划服务：RoutePlanService 路线规划

### 9. 工具类

- `references/util-geometry.md` - 几何工具：GeometryUtil 距离、面积计算
- `references/geolocation.md` - 地理定位：GetGeoLocation 获取位置

### 10. 类型定义

- `references/types.md` - 类型定义：TypeScript 类型声明

## 如何使用

请阅读各个参考文件以获取详细说明和代码示例。每个参考文件包含：

- 功能简要说明
- 完整代码示例及解释
- API 参数说明和注意事项

示例：

```
references/map.md
references/marker.md
```
