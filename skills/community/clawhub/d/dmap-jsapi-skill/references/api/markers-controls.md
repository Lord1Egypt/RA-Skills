

# Markers and Controls - 标记和控件

用户界面元素,可以在运行时添加到地图上。这些元素存在于地图的 canvas 元素之外。

## IControl - 控件接口

所有控件必须实现的接口规范。

### 必需方法

- `onAdd(map)` - 添加控件时调用,返回 DOM 元素
- `onRemove()` - 移除控件时调用
- `getDefaultPosition()` - 获取默认位置(可选)

### 自定义控件示例

```javascript
class CustomControl {
  onAdd(map) {
    this._map = map;
    this._container = document.createElement('div');
    this._container.className = 'mapboxgl-ctrl';
    this._container.textContent = 'Hello, world';
    return this._container;
  }
  
  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}

map.addControl(new CustomControl(), 'top-right');
```

## Marker - 标记

在地图上添加点标记。

### 构造函数

```javascript
new dmapgl.Marker(options)
```

### 配置选项

- `element` - 自定义DOM元素
- `color` - 标记颜色 (默认 '#3FB1CE')
- `scale` - 缩放比例 (默认 1)
- `anchor` - 锚点位置 ('center', 'top', 'bottom', 'left', 'right'等)
- `offset` - 偏移量 [x, y]
- `draggable` - 是否可拖拽 (默认 false)
- `clickTolerance` - 点击容差 (默认 0)
- `rotation` - 旋转角度 (默认 0)
- `pitchAlignment` - 俯仰对齐方式 ('map', 'viewport', 'auto')
- `rotationAlignment` - 旋转对齐方式 ('map', 'viewport', 'auto')

### 实例方法

#### 基本操作

- `addTo(map)` - 添加到地图
- `remove()` - 从地图移除
- `getMap()` - 获取地图实例
- `getElement()` - 获取DOM元素

#### 位置和外观

- `getLngLat()` - 获取位置坐标
- `setLngLat(lnglat)` - 设置位置坐标
- `getOffset()` - 获取偏移量
- `setOffset(offset)` - 设置偏移量
- `getColor()` - 获取颜色
- `setColor(color)` - 设置颜色
- `getScale()` - 获取缩放比例
- `setScale(scale)` - 设置缩放比例
- `getRotation()` - 获取旋转角度
- `setRotation(rotation)` - 设置旋转角度
- `getRotationAlignment()` - 获取旋转对齐方式
- `setRotationAlignment(alignment)` - 设置旋转对齐方式
- `getPitchAlignment()` - 获取俯仰对齐方式
- `setPitchAlignment(alignment)` - 设置俯仰对齐方式
- `getAnchor()` - 获取锚点
- `setAnchor(anchor)` - 设置锚点

#### 拖拽

- `getDraggable()` - 获取是否可拖拽
- `setDraggable(boolean)` - 设置是否可拖拽
- `getElement()` - 获取DOM元素

#### 弹窗

- `getPopup()` - 获取关联的弹窗
- `setPopup(popup)` - 设置关联的弹窗
- `togglePopup()` - 切换弹窗显示/隐藏
- `getOffset()` - 获取弹窗偏移量

### 事件

- `dragstart` - 开始拖拽
- `drag` - 拖拽中
- `dragend` - 结束拖拽

详见 [标记文档](../marker.md)

## Popup - 弹窗

显示信息弹窗。

### 构造函数

```javascript
new dmapgl.Popup(options)
```

### 配置选项

- `closeButton` - 是否显示关闭按钮 (默认 true)
- `closeOnClick` - 点击地图关闭 (默认 true)
- `closeOnEscape` - ESC键关闭 (默认 true)
- `closeOnMove` - 移动时关闭 (默认 false)
- `focusAfterOpen` - 打开后聚焦 (默认 true)
- `offset` - 偏移量 (默认 Point(0, 0))
- `maxWidth` - 最大宽度 (默认 '240px')
- `className` - CSS类名
- `anchor` - 锚点位置

### 实例方法

#### 基本操作

- `addTo(map)` - 添加到地图
- `remove()` - 从地图移除
- `isOpen()` - 检查是否打开
- `remove()` - 移除弹窗

#### 位置和内容

- `getLngLat()` - 获取位置
- `setLngLat(lnglat)` - 设置位置
- `getHTML()` - 获取HTML内容
- `setHTML(html)` - 设置HTML内容
- `getText()` - 获取文本内容
- `setText(text)` - 设置文本内容
- `getDOMContent()` - 获取DOM内容
- `setDOMContent(element)` - 设置DOM内容

#### 样式和布局

- `getOffset()` - 获取偏移量
- `setOffset(offset)` - 设置偏移量
- `getMaxWidth()` - 获取最大宽度
- `setMaxWidth(width)` - 设置最大宽度
- `getAnchor()` - 获取锚点
- `setAnchor(anchor)` - 设置锚点
- `addClassName(className)` - 添加CSS类名
- `removeClassName(className)` - 移除CSS类名
- `toggleClassName(className)` - 切换CSS类名
- `getClassName()` - 获取CSS类名

#### 其他

- `trackPointer()` - 跟踪鼠标指针
- `getTrackPointer()` - 检查是否跟踪指针
- `getElement()` - 获取弹窗DOM元素

### 事件

- `open` - 弹窗打开
- `close` - 弹窗关闭

详见 [弹窗文档](../popup.md)

## NavigationControl - 导航控件

缩放和旋转控制按钮。

### 构造函数

```javascript
new dmapgl.NavigationControl(options)
```

### 配置选项

- `showZoom` - 显示缩放按钮 (默认 true)
- `showCompass` - 显示指南针 (默认 true)
- `visualizePitch` - 显示俯仰指示器 (默认 false)

### 事件

- `rotate` - 旋转时触发
- `pitch` - 倾斜时触发

详见 [控件文档](../controls.md)


## ScaleControl - 比例尺控件

显示地图比例。

### 构造函数

```javascript
new dmapgl.ScaleControl(options)
```

### 配置选项

- `maxWidth` - 最大宽度 (默认 100)
- `unit` - 单位 ('imperial', 'metric', 'nautical')

### 实例方法

- `setUnit(unit)` - 设置单位

详见 [控件文档](../controls.md)

## FullscreenControl - 全屏控件

切换全屏显示。

### 构造函数

```javascript
new dmapgl.FullscreenControl(options)
```

### 配置选项

- `container` - 全屏容器元素 (默认地图容器)

### 事件

- `fullscreenchange` - 全屏状态变化

详见 [控件文档](../controls.md)

## AttributionControl - 版权控件

显示数据来源版权。

### 构造函数

```javascript
new dmapgl.AttributionControl(options)
```

### 配置选项

- `compact` - 紧凑模式 (默认响应式)
- `customAttribution` - 自定义版权文本 (字符串或数组)

详见 [控件文档](../controls.md)

## 使用示例

### 创建标记和弹窗

```javascript
// 创建标记
const marker = new dmapgl.Marker({ 
  color: '#3b82f6',
  draggable: true,
  rotation: 45
})
  .setLngLat([800000, 600000])
  .addTo(map);

// 创建弹窗
const popup = new dmapgl.Popup({ 
  offset: 25,
  closeButton: true,
  maxWidth: '300px'
})
  .setHTML('<h3>北京</h3><p>这是北京市中心</p>');

// 关联弹窗到标记
marker.setPopup(popup);

// 监听拖拽事件
marker.on('dragend', () => {
  const lngLat = marker.getLngLat();
  console.log('新位置:', lngLat);
});
```

### 添加多个控件

```javascript
// 添加导航控件
map.addControl(
  new dmapgl.NavigationControl({
    showZoom: true,
    showCompass: true,
    visualizePitch: true
  }), 
  'top-right'
);

// 添加比例尺
map.addControl(
  new dmapgl.ScaleControl({
    maxWidth: 80,
    unit: 'metric'
  }), 
  'bottom-left'
);

// 添加地理定位
map.addControl(
  new dmapgl.GeolocateControl({
    positionOptions: { 
      enableHighAccuracy: true,
      timeout: 6000
    },
    trackUserLocation: true,
    showUserHeading: true
  }), 
  'top-right'
);

// 添加全屏控件
map.addControl(
  new dmapgl.FullscreenControl(),
  'top-right'
);

// 添加版权控件
map.addControl(
  new dmapgl.AttributionControl({
    compact: true,
    customAttribution: 'Map design by Me'
  }),
  'bottom-right'
);
```

### 自定义控件

```javascript
class ZoomInfoControl {
  onAdd(map) {
    this._map = map;
    this._container = document.createElement('div');
    this._container.className = 'mapboxgl-ctrl mapboxgl-ctrl-group';
    this._container.innerHTML = '<div id="zoom-info">Zoom: ' + map.getZoom() + '</div>';
    
    // 监听缩放变化
    map.on('zoom', () => {
      this._container.innerHTML = '<div id="zoom-info">Zoom: ' + Math.round(map.getZoom() * 100) / 100 + '</div>';
    });
    
    return this._container;
  }
  
  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}

map.addControl(new ZoomInfoControl(), 'bottom-right');
```
