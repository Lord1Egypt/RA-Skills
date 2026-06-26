

# Events - 事件系统

DMap GL的事件系统用于响应地图交互和状态变化。

## Evented

事件基础类,提供事件绑定和解绑功能。

### 实例方法

- `on(type, handler)` - 绑定事件监听器
- `off(type, handler)` - 解绑事件监听器
- `once(type, handler)` - 绑定一次性事件监听器
- `fire(type, data)` - 触发事件

## MapMouseEvent

鼠标事件对象。

### 属性

- `type` - 事件类型
- `target` - 目标对象(Map)
- `originalEvent` - 原始DOM事件
- `point` - 像素坐标 Point {x, y}
- `lngLat` - 地理坐标 LngLat {lng, lat}
- `features` - 要素数组(仅图层事件)

### 实例方法

- `preventDefault()` - 阻止默认行为

## MapTouchEvent

触摸事件对象。

### 属性

- `type` - 事件类型
- `target` - 目标对象
- `originalEvent` - 原始触摸事件
- `point` - 主要触摸点像素坐标
- `points` - 触摸点数组
- `lngLat` - 主要触摸点地理坐标
- `lngLats` - 地理坐标数组
- `features` - 要素数组

### 实例方法

- `preventDefault()` - 阻止默认行为

## MapWheelEvent

滚轮事件对象。

### 属性

- `type` - 事件类型 ("wheel")
- `target` - 目标对象(Map)
- `originalEvent` - 原始 WheelEvent

### 实例方法

- `preventDefault()` - 阻止默认行为

## MapBoxZoomEvent

框选缩放事件对象。

### 属性

- `type` - 事件类型 ("boxzoomstart" | "boxzoomend" | "boxzoomcancel")
- `target` - 目标对象(Map)
- `originalEvent` - 原始 DOM 事件

### 示例

```javascript
map.on('boxzoomend', (e) => {
  console.log('框选边界:', e.boxZoomBounds);
});
```

## DataEvent

数据加载事件对象。

### 属性

- `type` - 事件类型
- `target` - 目标对象
- `dataType` - 数据类型 ('source' | 'style')
- `isSourceLoaded` - 源是否加载完成
- `sourceId` - 源ID(仅source类型)
- `source` - 源配置对象(仅source类型)
- `sourceDataType` - 源数据类型 ('metadata' | 'content' | 'visibility' | 'error')
- `coord` - 瓦片坐标(仅瓦片加载事件)
- `tile` - 瓦片对象(仅瓦片加载事件)

## 地图事件类型

### 鼠标事件

- `click` - 点击
- `dblclick` - 双击
- `mousedown` - 鼠标按下
- `mouseup` - 鼠标释放
- `mousemove` - 鼠标移动
- `mouseover` - 鼠标进入
- `mouseout` - 鼠标离开
- `contextmenu` - 右键菜单

### 触摸事件

- `touchstart` - 触摸开始
- `touchend` - 触摸结束
- `touchmove` - 触摸移动
- `touchcancel` - 触摸取消

### 视图事件

- `movestart` - 移动开始
- `move` - 移动中
- `moveend` - 移动结束
- `zoomstart` - 缩放开始
- `zoom` - 缩放中
- `zoomend` - 缩放结束
- `rotatestart` - 旋转开始
- `rotate` - 旋转中
- `rotateend` - 旋转结束
- `pitchstart` - 俯仰开始
- `pitch` - 俯仰中
- `pitchend` - 俯仰结束

### 加载事件

- `load` - 地图加载完成
- `render` - 渲染帧
- `idle` - 空闲状态
- `error` - 错误

### 数据事件

- `dataloading` - 数据加载中
- `data` - 数据加载
- `sourcedataloading` - 源数据加载中
- `sourcedata` - 源数据加载
- `styledataloading` - 样式数据加载中
- `styledata` - 样式数据加载

### 图层事件

- `layer.add` - 图层添加
- `layer.remove` - 图层移除

## 使用示例

```javascript
// 绑定事件
map.on('click', (e) => {
  console.log('点击位置:', e.lngLat);
});

// 图层事件
map.on('click', 'my-layer', (e) => {
  console.log('要素:', e.features[0]);
});

// 一次性事件
map.once('load', () => {
  console.log('地图已加载');
});

// 解绑事件
const handler = (e) => console.log(e);
map.on('move', handler);
map.off('move', handler);

```

详见 [事件文档](../events.md)
