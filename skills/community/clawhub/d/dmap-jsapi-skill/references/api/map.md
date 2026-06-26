

# Map - 地图核心对象

Map是DMap GL的核心类,代表页面上的地图实例。

## 构造函数

```javascript
new dmapgl.Map(options)
```

详见 [地图初始化](../map-init.md)

## 实例属性 (Handlers)

Map实例提供以下交互处理器属性,用于控制用户交互:

- `boxZoom` - BoxZoomHandler 框选缩放处理器
- `scrollZoom` - ScrollZoomHandler 滚轮缩放处理器
- `dragPan` - DragPanHandler 拖拽平移处理器
- `dragRotate` - DragRotateHandler 拖拽旋转处理器
- `keyboard` - KeyboardHandler 键盘交互处理器
- `doubleClickZoom` - DoubleClickZoomHandler 双击缩放处理器
- `touchZoomRotate` - TouchZoomRotateHandler 触摸缩放旋转处理器
- `twoFingersTouchPitch` - TwoFingersTouchPitchHandler 双指倾斜处理器
- `twoFingersTouchZoomRotate` - TwoFingersTouchZoomRotateHandler 双指缩放旋转处理器

每个handler都有以下方法:
- `enable()` - 启用该交互
- `disable()` - 禁用该交互
- `isEnabled()` - 检查是否启用
- `isActive()` - 检查是否正在活动(仅部分handler)

```javascript
// 禁用滚轮缩放
map.scrollZoom.disable();

// 禁用框选缩放
map.boxZoom.disable();

// 禁用拖拽旋转
map.dragRotate.disable();

// 检查状态
if (map.keyboard.isEnabled()) {
  console.log('键盘交互已启用');
}
```

## 实例方法

### Camera - 相机控制

#### 获取当前视图状态

- `getCenter()` - 获取中心点坐标
- `getZoom()` - 获取缩放级别
- `getBearing()` - 获取旋转角度(方位角)
- `getPitch()` - 获取俯仰角
- `getPadding()` - 获取填充
- `getBounds()` - 获取可视区域边界
- `project(lnglat)` - 地理坐标转屏幕像素坐标
- `unproject(point)` - 屏幕像素坐标转地理坐标

#### 设置视图状态

- `setCenter(center)` - 设置中心点
- `setZoom(zoom)` - 设置缩放级别
- `setBearing(bearing)` - 设置旋转角度
- `setPitch(pitch)` - 设置俯仰角
- `setPadding(padding)` - 设置填充

#### 动画过渡

- `jumpTo(options)` - 立即跳转到指定视图(无动画)
- `easeTo(options)` - 平滑过渡到指定视图
- `flyTo(options)` - 飞行动画到指定视图
- `zoomTo(zoom, options)` - 缩放到指定级别
- `panTo(lnglat, options)` - 平移到指定位置
- `rotateTo(bearing, options)` - 旋转到指定角度
- `pitchTo(pitch, options)` - 倾斜到指定角度
- `fitBounds(bounds, options)` - 适配到指定边界
- `fitScreenCoordinates(p0, p1, bearing, options)` - 适配屏幕坐标
- `stop()` - 停止所有正在进行的动画和过渡

#### 查询动画状态

- `isMoving()` - 检查地图是否正在移动
- `isZooming()` - 检查地图是否正在缩放
- `isRotating()` - 检查地图是否正在旋转

### Map constraints - 地图约束

#### 地图约束

- `setMaxBounds(bounds)` - 设置最大边界限制
- `getMaxBounds()` - 获取最大边界
- `setMinZoom(minZoom)` - 设置最小缩放级别
- `getMinZoom()` - 获取最小缩放级别
- `setMaxZoom(maxZoom)` - 设置最大缩放级别
- `getMaxZoom()` - 获取最大缩放级别
- `setMinPitch(minPitch)` - 设置最小俯仰角
- `getMinPitch()` - 获取最小俯仰角
- `setMaxPitch(maxPitch)` - 设置最大俯仰角
- `getMaxPitch()` - 获取最大俯仰角
- `setRenderWorldCopies(boolean)` - 设置是否渲染世界副本
- `getRenderWorldCopies()` - 获取是否渲染世界副本

### Markers and controls - 标记和控件

- `addControl(control, position)` - 添加控件到地图
- `removeControl(control)` - 从地图移除控件

### Styling - 样式管理

#### 图层管理

- `addLayer(layer, beforeId)` - 添加图层
- `removeLayer(id)` - 移除图层
- `moveLayer(id, beforeId)` - 移动图层到指定位置
- `getLayer(id)` - 获取图层配置

#### 图层属性

- `setLayoutProperty(layerId, name, value)` - 设置布局属性
- `getLayoutProperty(layerId, name)` - 获取布局属性
- `setPaintProperty(layerId, name, value)` - 设置绘制属性
- `getPaintProperty(layerId, name)` - 获取绘制属性
- `setFilter(layerId, filter)` - 设置过滤器
- `getFilter(layerId)` - 获取过滤器
- `setFeatureState(source, sourceLayer, featureId, state)` - 设置要素状态
- `getFeatureState(source, sourceLayer, featureId)` - 获取要素状态
- `removeFeatureState(target, key)` - 移除要素状态

#### 数据源管理

- `addSource(id, source)` - 添加数据源
- `removeSource(id)` - 移除数据源
- `getSource(id)` - 获取数据源
- `isSourceLoaded(id)` - 检查数据源是否加载完成

#### 图片管理

- `addImage(name, image, options)` - 添加图片
- `updateImage(name, image)` - 更新图片
- `removeImage(name)` - 移除图片
- `hasImage(name)` - 检查图片是否存在
- `getImage(name)` - 获取图片
- `loadImage(url, callback)` - 加载图片
- `listImages()` - 列出所有图片

#### 样式整体操作

- `setStyle(style, options)` - 设置完整样式
- `getStyle()` - 获取当前样式
- `areTilesLoaded()` - 检查瓦片是否全部加载

#### 光照、地形、雾效、投影

- `setLight(options)` - 设置光照
- `getLight()` - 获取光照配置
- `setTerrain(options)` - 设置地形
- `getTerrain()` - 获取地形配置
- `setFog(options)` - 设置雾效
- `getFog()` - 获取雾效配置
- `setProjection(projection)` - 设置投影方式
- `getProjection()` - 获取投影配置

### Querying features - 查询要素

- `queryRenderedFeatures(geometryOrPoint, options)` - 查询渲染的要素
- `querySourceFeatures(sourceId, parameters)` - 查询数据源要素
- `queryTerrainElevation(lngLat, options)` - 查询地形高程

### I/O - 输入输出

#### 容器和Canvas

- `getContainer()` - 获取地图容器DOM元素
- `getCanvasContainer()` - 获取Canvas容器DOM元素
- `getCanvas()` - 获取Canvas元素

#### 显示选项(属性)

- `showTileBoundaries` - 显示瓦片边界
- `showCollisionBoxes` - 显示碰撞检测框
- `showPadding` - 显示填充区域
- `repaint` - 强制重绘
- `showOverdrawInspector` - 显示过度绘制检查器

#### 数据管理

- `refreshTiles()` - 刷新瓦片
- `clearData(options, callback)` - 清除缓存数据
- `getPixelRatio()` - 获取像素比
- `setPixelRatio(ratio)` - 设置像素比
- `hasControl(control)` - 检查控件是否存在

### Other - 其他方法

#### 生命周期

- `loaded()` - 检查地图是否完全加载
- `remove()` - 移除地图并清理资源
- `destroy()` - 销毁地图实例(同remove)
- `triggerRepaint()` - 触发重绘

#### 尺寸调整

- `resize()` - 调整地图大小以适应容器
- `update()` - 更新地图状态

#### 瓦片管理

- `reloadSource(sourceId)` - 重新加载指定数据源

## 完整示例

```javascript
// 注意：此处需改为你的后台服务地址
dmapgl.serviceUrl = 'http://172.26.64.84/api';
var map = new dmapgl.Map({
  container: 'map',
  style: dmapgl.serviceUrl + '/map/vector/standard/styles/style.json',
  center: [800000, 600000],
  zoom: 11,
  pitch: 0,
  bearing: 0
});

map.on('load', () => {
  // 添加图层
  map.addLayer({
    id: 'points',
    type: 'circle',
    source: {
      type: 'geojson',
      data: { /* ... */ }
    }
  });
  
  // 添加控件
  map.addControl(new dmapgl.NavigationControl(), 'top-right');
  map.addControl(new dmapgl.ScaleControl(), 'bottom-left');
  
  // 禁用某些交互
  map.dragRotate.disable();
  map.touchZoomRotate.disableRotation();
  
  // 绑定事件
  map.on('click', 'points', (e) => {
    console.log('点击了要素:', e.features);
  });
  
  // 飞行动画
  map.flyTo({
    center: [850000, 650000],
    zoom: 14,
    essential: true
  });
});

// 获取地图信息
console.log('中心点:', map.getCenter());
console.log('缩放级别:', map.getZoom());
console.log('Canvas:', map.getCanvas());
console.log('容器:', map.getContainer());

// 设置地图约束
map.setMinZoom(7);
map.setMaxZoom(19);
map.setMaxBounds([
  [716638.24, 548483.59],
  [894455.08, 728066.47]
]);
```
