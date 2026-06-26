

# Handlers - 交互处理器

Handler控制地图的用户交互行为，如缩放、平移、旋转等。

## BoxZoomHandler - 框选缩放

通过拖拽矩形框进行缩放。

### 启用/禁用

```javascript
// 禁用框选缩放
map.boxZoom.disable();

// 启用框选缩放
map.boxZoom.enable();

// 检查是否启用
if (map.boxZoom.isEnabled()) {
  console.log('框选缩放已启用');
}
```

### 使用方法

按住Shift键并拖拽鼠标绘制矩形框来缩放。

## ScrollZoomHandler - 滚轮缩放

通过鼠标滚轮进行缩放。

### 启用/禁用

```javascript
// 禁用滚轮缩放
map.scrollZoom.disable();

// 启用滚轮缩放
map.scrollZoom.enable();

// 检查状态
if (map.scrollZoom.isEnabled()) {
  console.log('滚轮缩放已启用');
}
```

### 配置选项

```javascript
// 启用并配置
map.scrollZoom.enable({
  around: 'center'  // 'center' 或 null
});

// 设置缩放速度
map.scrollZoom.setWheelZoomRate(1);  // 默认值
```

### 协作手势

```javascript
var map = new dmapgl.Map({
  container: 'map',
  style: style,
  cooperativeGestures: true  // 需要Ctrl+滚轮才能缩放
});
```

## DragPanHandler - 拖拽平移

通过拖拽移动地图。

### 启用/禁用

```javascript
// 禁用拖拽平移
map.dragPan.disable();

// 启用拖拽平移
map.dragPan.enable();

// 检查状态
if (map.dragPan.isEnabled()) {
  console.log('拖拽平移已启用');
}
```

### 配置选项

```javascript
// 启用并配置
map.dragPan.enable({
  linearity: 0.3,      // 线性度(0-1)
  easing: (t) => t,    // 缓动函数
  deceleration: 0.8,   // 减速度
  maxSpeed: 1400       // 最大速度
});
```

## DragRotateHandler - 拖拽旋转

通过右键拖拽旋转地图。

### 启用/禁用

```javascript
// 禁用拖拽旋转
map.dragRotate.disable();

// 启用拖拽旋转
map.dragRotate.enable();

// 检查状态
if (map.dragRotate.isEnabled()) {
  console.log('拖拽旋转已启用');
}
```

### 配合倾斜

```javascript
// 右键拖拽同时旋转和倾斜
map.dragRotate.enable();

// 仅旋转，不倾斜
map.touchZoomRotate.disableRotation();
```

## KeyboardHandler - 键盘交互

通过键盘控制地图。

### 启用/禁用

```javascript
// 禁用键盘交互
map.keyboard.disable();

// 启用键盘交互
map.keyboard.enable();

// 检查状态
if (map.keyboard.isEnabled()) {
  console.log('键盘交互已启用');
}
```

### 快捷键

- **+**: 放大
- **-**: 缩小
- **←↑→↓**: 平移
- **Shift + ←↑→↓**: 快速平移
- **Shift + ←→**: 旋转
- **Shift + ↑↓**: 倾斜

## DoubleClickZoomHandler - 双击缩放

双击放大，Shift+双击缩小。

### 启用/禁用

```javascript
// 禁用双击缩放
map.doubleClickZoom.disable();

// 启用双击缩放
map.doubleClickZoom.enable();

// 检查状态
if (map.doubleClickZoom.isEnabled()) {
  console.log('双击缩放已启用');
}
```

## TouchZoomRotateHandler - 触摸缩放旋转

通过双指触摸进行缩放和旋转。

### 启用/禁用

```javascript
// 禁用触摸缩放旋转
map.touchZoomRotate.disable();

// 启用
map.touchZoomRotate.enable();

// 仅禁用旋转
map.touchZoomRotate.disableRotation();

// 检查状态
if (map.touchZoomRotate.isEnabled()) {
  console.log('触摸缩放旋转已启用');
}
```

## TwoFingersTouchPitchHandler - 双指倾斜

通过双指触摸进行倾斜。

### 启用/禁用

```javascript
// 禁用双指倾斜
map.twoFingersTouchPitch.disable();

// 启用
map.twoFingersTouchPitch.enable();
```

## TwoFingersTouchZoomRotateHandler - 双指缩放旋转

通过双指触摸进行缩放和旋转（移动端）。

### 启用/禁用

```javascript
// 禁用
map.twoFingersTouchZoomRotate.disable();

// 启用
map.twoFingersTouchZoomRotate.enable();

// 仅禁用旋转
map.twoFingersTouchZoomRotate.disableRotation();
```

## 批量控制交互

### 禁用所有交互

```javascript
map.dragPan.disable();
map.dragRotate.disable();
map.scrollZoom.disable();
map.touchZoomRotate.disable();
map.keyboard.disable();
map.doubleClickZoom.disable();
map.boxZoom.disable();
```

### 启用所有交互

```javascript
map.dragPan.enable();
map.dragRotate.enable();
map.scrollZoom.enable();
map.touchZoomRotate.enable();
map.keyboard.enable();
map.doubleClickZoom.enable();
map.boxZoom.enable();
```

### 初始化时配置

```javascript
// 注意：此处需改为你的后台服务地址
dmapgl.serviceUrl = 'http://172.26.64.84/api';
var map = new dmapgl.Map({
  container: 'map',
  style: style,
  center: [800000, 600000],
  zoom: 11,
  
  // 禁用特定交互
  dragRotate: false,      // 禁用旋转
  touchZoomRotate: false, // 禁用触摸旋转
  doubleClickZoom: false, // 禁用双击缩放
  boxZoom: false,         // 禁用框选缩放
  
  // 或全部禁用
  interactive: false      // 禁用所有交互
});
```

## 实用示例

### 只读模式

```javascript
function setReadOnlyMode(map) {
  map.dragPan.disable();
  map.dragRotate.disable();
  map.scrollZoom.disable();
  map.touchZoomRotate.disable();
  map.keyboard.disable();
  map.doubleClickZoom.disable();
  map.boxZoom.disable();
}

setReadOnlyMode(map);
```

### 移动端优化

```javascript
const isMobile = window.innerWidth < 768;
// 注意：此处需改为你的后台服务地址
dmapgl.serviceUrl = 'http://172.26.64.84/api';
var map = new dmapgl.Map({
  container: 'map',
  style: style,
  center: [800000, 600000],
  zoom: 11,
  
  // 移动端禁用某些交互
  dragRotate: !isMobile,
  keyboard: !isMobile,
  boxZoom: !isMobile,
  
  // 协作手势防止误触
  cooperativeGestures: isMobile
});
```

### 条件启用交互

```javascript
let editMode = false;

function toggleEditMode() {
  editMode = !editMode;
  
  if (editMode) {
    // 编辑模式：启用所有交互
    map.dragPan.enable();
    map.dragRotate.enable();
    map.scrollZoom.enable();
  } else {
    // 查看模式：禁用部分交互
    map.dragRotate.disable();
    map.scrollZoom.disable();
  }
}

document.getElementById('edit-toggle').onclick = toggleEditMode;
```

## 注意事项

1. **性能**: 禁用的handler不会监听事件，提升性能
2. **用户体验**: 根据场景选择合适的交互
3. **移动端**: 考虑触摸设备的特殊性
4. **无障碍**: 保留键盘交互支持无障碍访问
5. **冲突**: 多个handler可能产生冲突
6. **状态管理**: 跟踪handler的启用状态
