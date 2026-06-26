---
name: dmap-jsapi-skill
description: DMap GL地图 JSAPI (dmapgl) 开发指南。在编写、审查或调试使用DMap地图 API的代码时应运用此技能。适用于涉及地图初始化、覆盖物渲染、图层管理、事件处理、控件交互等任务。当用户提及 dmap、dmapgl、jsapi-gl或相关地图开发需求时自动触发
license: MIT
version: 1.0.0
---

# DMap GL JSAPI开发指南

本指南包含地图初始化、标记、弹窗、控件、图层、数据源等核心模块的 API 说明和代码示例,旨在帮助开发者快速集成DMap GL地图并遵循正确的使用方式。

## 目的

利用此技能,在前端项目中以生产级安全的默认设置实现DMap GL JSAPI功能。

## 何时使用

在以下场景中参考这些指南:

- 创建新的地图页面或组件
- 在地图上添加标记(Marker)、弹窗(Popup)等UI元素
- 配置地图视图(缩放、中心点、旋转、俯仰)
- 管理图层和数据源(GeoJSON、矢量瓦片、栅格瓦片等)
- 处理地图交互事件(点击、拖拽、缩放等)
- 添加地图控件(导航、比例尺、全屏等)
- 调试地图渲染或性能问题

## 快速开始

### 1. 引入 DMap GL JS

通过 CDN 安装:

```html
<!-- CDN -->
<link rel="stylesheet" href="http://172.26.64.84/dmapapi/bj2000/v1.0/dmap-gl.css">
<script type="text/javascript" src="http://172.26.64.84/dmapapi/bj2000/v1.0/dmap-gl.js"></script>
```

### 2. 指定后台服务地址

```javascript
// 注意：此处需改为你的后台服务地址
dmapgl.serviceUrl = 'http://172.26.64.84/api';
```

### 3. 初始化地图

```javascript
var map = new dmapgl.Map({
  container: 'map', // HTML容器ID
  style: dmapgl.serviceUrl + '/map/vector/standard/styles/style.json', // 地图样式URL
  center: [800000, 600000], // 初始中心点 [x, y] 地方平面坐标
  zoom: 11, // 初始缩放级别 (7-19)
  pitch: 0, // 俯仰角(0-85)
  bearing: 0, // 旋转角度
  minZoom: 7, // 最小缩放级别
  maxZoom: 19, // 最大缩放级别
  maxBounds: [
    [716638.2414098255, 548483.5939021005], // 西南角
    [894455.0756895209, 728066.4667000007]  // 东北角
  ],
});

// 等待地图加载完成
map.on('load', () => {
  console.log('地图加载完成');
});
```

## 场景示例

### 地图控制

- **生命周期**: `references/map-init.md` - 掌握 Map 实例创建、配置及 destroy 销毁流程
- **视图交互**: `references/view-control.md` - 控制 zoom(缩放)、center(平移)、pitch(俯仰)、bearing(旋转)

> **注意**: DMap 使用地方平面坐标系，中心点为 [800000, 600000]，地图范围为 [716638.24, 548483.59, 894455.08, 728066.47]，缩放级别范围为 7-19。

### 标记与弹窗

- **标记**: `references/marker.md` - 使用 Marker 标注位置,支持自定义HTML元素
- **弹窗**: `references/popup.md` - 通过 Popup 展示详细信息

### 图层与数据源

- **数据源**: `references/sources.md` - GeoJSON、矢量瓦片、栅格瓦片、图片、Canvas等数据源
- **图层管理**: `references/layers.md` - 添加、移除、排序图层,动态更新样式

### 控件与交互

- **控件**: `references/controls.md` - 缩放和旋转按钮、缩放按钮、比例尺、全屏按钮
- **事件系统**: `references/events.md` - 响应点击、拖拽、缩放、移动等交互事件

### 高级功能

- **动画**: `references/animation.md` - 相机飞行动画、平滑过渡
- **3D地形**: `references/terrain.md` - 启用3D地形渲染

## 最佳实践

1. **资源释放**: 组件卸载时务必调用 `map.remove()` 或 `map.destroy()`,防止 WebGL 上下文内存泄漏
2. **按需加载**: 仅在需要时添加图层和控件,避免不必要的性能开销
3. **事件监听清理**: 移除组件时取消事件监听,使用 `map.off()` 清理
4. **样式优化**: 使用 `setLayoutProperty` 和 `setPaintProperty` 动态更新样式,而非重新添加图层
5. **数据更新**: GeoJSON 数据频繁更新时使用 `setData()` 而非删除重建
6. **性能监控**: 使用 `map.queryRenderedFeatures()` 进行高效的要素查询

## API Reference

### [Map](references/api/map.md)
Map - 地图核心对象，包含所有地图操作方法、交互处理器(handler)属性、相机控制、样式管理、查询等功能。

**主要内容包括:**
- Camera (相机控制): getCenter, setZoom, flyTo, easeTo, fitBounds 等
- Map constraints (地图约束): getMaxBounds, setMaxBounds, setMinZoom, setMaxZoom 等
- Handlers (交互处理器): boxZoom, scrollZoom, dragPan, dragRotate, keyboard, doubleClickZoom, touchZoomRotate 等
- Markers and Controls (标记和控件): addControl, removeControl
- Styling (样式): addLayer, addSource, setPaintProperty, addImage, setLight, setTerrain, setFog 等
- Querying features (查询要素): queryRenderedFeatures, querySourceFeatures, queryTerrainElevation
- I/O (输入输出): getContainer, getCanvas, getCanvasContainer
- Other (其他): loaded, remove, destroy, resize, update, triggerRepaint 等

### [Properties and Options](references/api/properties.md)
全局属性和工具函数，包括 serviceUrl、version、supported、clearData、setRTLTextPlugin、AnimationOptions、CameraOptions、CustomLayerInterface 等。

### [Markers and Controls](references/api/markers-controls.md)
用户界面元素，可以在运行时添加到地图上。

**包括:**
- IControl - 控件接口规范
- Marker - 标记，支持自定义HTML元素、拖拽、弹窗关联
- Popup - 弹窗，支持HTML内容、动态定位
- NavigationControl - 导航控件(缩放、旋转、俯仰)
- GeolocateControl - 地理定位控件
- ScaleControl - 比例尺控件
- FullscreenControl - 全屏控件
- AttributionControl - 版权控件

### [User Interaction Handlers](references/api/handlers.md)
控制地图的用户交互行为。

**包括:**
- BoxZoomHandler - 框选缩放 (Shift+拖拽)
- ScrollZoomHandler - 滚轮缩放
- DragPanHandler - 拖拽平移
- DragRotateHandler - 拖拽旋转 (右键拖拽)
- KeyboardHandler - 键盘交互
- DoubleClickZoomHandler - 双击缩放
- TouchZoomRotateHandler - 触摸缩放旋转
- TwoFingersTouchPitchHandler - 双指倾斜
- TwoFingersTouchZoomRotateHandler - 双指缩放旋转

每个handler都提供 enable(), disable(), isEnabled() 方法。

### [Sources](references/api/sources.md)
数据源定义地图上要显示的地理数据。

**包括:**
- GeoJSONSource - GeoJSON格式数据源，支持聚类
- VectorTileSource - 矢量瓦片数据源
- RasterTileSource - 栅格瓦片数据源
- RasterArrayTileSource - 栅格数组瓦片数据源
- ImageSource - 单张图片数据源
- VideoSource - 视频数据源
- CanvasSource - Canvas数据源
- ModelSource - 3D模型数据源

### [Events and Event Types](references/api/events.md)
事件系统和事件类型。

**Evented基类:**
- on(type, handler) - 绑定事件
- off(type, handler) - 解绑事件
- once(type, handler) - 一次性事件
- fire(type, data) - 触发事件

**事件对象类型:**
- MapMouseEvent - 鼠标事件对象
- MapTouchEvent - 触摸事件对象
- MapWheelEvent - 滚轮事件对象
- MapBoxZoomEvent - 框选缩放事件对象
- MapDataEvent - 数据加载事件对象

**地图事件分类:**
- 鼠标事件: click, dblclick, mousedown, mouseup, mousemove, mouseover, mouseout, contextmenu
- 触摸事件: touchstart, touchend, touchmove, touchcancel
- 视图事件: movestart, move, moveend, zoomstart, zoom, zoomend, rotatestart, rotate, rotateend, pitchstart, pitch, pitchend
- 加载事件: load, render, idle, error
- 数据事件: dataloading, data, sourcedataloading, sourcedata, styledataloading, styledata
- 图层事件: layer.add, layer.remove
- 框选缩放事件: boxzoomstart, boxzoomend, boxzoomcancel

### [Geography and Geometry](references/api/geography.md)
用于处理地理坐标、边界框和屏幕位置的类。

**包括:**
- LngLat - 地理坐标(经度,纬度)
- LngLatBounds - 地理边界框
- Point - 二维点(x, y)
- MercatorCoordinate - 墨卡托坐标(3D投影)
- Pixel - 像素坐标类型
- PointLike - Point或数字数组的灵活类型
- LngLatLike - LngLat或数组的灵活类型
- LngLatBoundsLike - LngLatBounds或数组的灵活类型

## Style Specification


### [Layers](references/style/layers.md)
fill / line / symbol / circle / heatmap / fill-extrusion / raster / hillshade / background

### [Sources](references/style/sources.md)
vector / raster / raster-dem / geojson / image / video / canvas / model

### [Expressions](references/style/expressions.md)
数学运算 / 条件判断 / 字符串操作 / 颜色转换 / 数据驱动样式

### [Types](references/style/types.md)
Color / PromoteId / Formatted / ResolvedImage / VariableAnchorOffsetCollection

### [Root](references/style/root.md)
version / name / metadata / center / zoom / bearing / pitch / sources / layers

### [Sprite](references/style/sprite.md)
Sprite 图标集配置

### [Glyphs](references/style/glyphs.md)
Glyphs 字体配置

### [Terrain](references/style/terrain.md)
Terrain 地形配置

### [Fog](references/style/fog.md)
Fog 雾效配置

### [Light](references/style/light.md)
Light 光照配置

### [Transition](references/style/transition.md)
Transition 过渡动画配置

### [Other](references/style/other.md)
其他样式属性

## 使用 skills 必须遵循的铁律

1. **校验生成代码可用性**: 自我验证校验代码生成的可用性,一定是可以正常运行的
2. **命名空间一致性**: 所有 API 调用使用 `dmapgl` 命名空间

## 如何使用

1. 如果有相近的"场景示例"那么去阅读场景示例,再阅读场景示例中的涉及的类的api文档。再结合描述/场景示例/api 去完成任务。
2. 在最终的完成任务前,检查用的api用法是否符合文档。
