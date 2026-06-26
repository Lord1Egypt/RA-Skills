

# 视图控制

> **坐标系说明**: DMap 使用地方平面坐标系，中心点为 `[800000, 600000]`，地图范围为 `[716638.24, 548483.59, 894455.08, 728066.47]`，缩放级别范围为 `7-19`。

控制地图的相机视图,包括缩放、平移、旋转和俯仰。

## 缩放 (Zoom)

### 获取当前缩放级别

```javascript
const zoom = map.getZoom();
console.log('当前缩放:', zoom);
```

### 设置缩放级别

```javascript
// 立即设置
map.setZoom(15);

// 动画过渡
map.easeTo({ zoom: 15, duration: 2000 });
map.flyTo({ zoom: 15, duration: 3000 });

// 缩放到特定级别
map.zoomTo(12, { duration: 1000 });
```

### 缩放限制

```javascript
// 初始化时设置
var map = new dmapgl.Map({
  minZoom: 7,
  maxZoom: 18
});

// 动态修改
map.setMinZoom(3);
map.setMaxZoom(20);
```

## 中心点 (Center)

### 获取当前中心点

```javascript
const center = map.getCenter();
console.log('经度:', center.lng);
console.log('纬度:', center.lat);
```

### 设置中心点

```javascript
// 立即设置 [lng, lat]
map.setCenter([810000, 610000]);

// 动画过渡
map.easeTo({ 
  center: [810000, 610000],
  duration: 2000 
});

map.flyTo({ 
  center: [810000, 610000],
  duration: 3000,
  zoom: 14
});

// 平移到新位置
map.panTo([810000, 610000], { duration: 1000 });
```

## 旋转 (Bearing)

地图逆时针旋转角度(单位:度)。

### 获取当前旋转角度

```javascript
const bearing = map.getBearing();
console.log('旋转角度:', bearing);
```

### 设置旋转角度

```javascript
// 立即设置
map.setBearing(45);

// 动画过渡
map.easeTo({ bearing: 90, duration: 2000 });
map.rotateTo(180, { duration: 1000 });

// 重置为北向
map.resetNorth();
```

## 俯仰 (Pitch)

地图倾斜角度(0-85度)。

### 获取当前俯仰角

```javascript
const pitch = map.getPitch();
console.log('俯仰角:', pitch);
```

### 设置俯仰角

```javascript
// 立即设置
map.setPitch(60);

// 动画过渡
map.easeTo({ pitch: 45, duration: 2000 });

// 俯仰到特定角度
map.pitchTo(30, { duration: 1000 });
```

## 边界 (Bounds)

### 获取当前可视区域

```javascript
const bounds = map.getBounds();
console.log('西南角:', bounds.getSouthWest());
console.log('东北角:', bounds.getNorthEast());
```

### 适配到边界

```javascript
// 适配到指定边界
map.fitBounds([
  [750000, 560000], // 西南角 [x, y]
  [850000, 650000]  // 东北角 [x, y]
], {
  padding: 50,    // 内边距(像素)
  duration: 2000, // 动画时长
  maxZoom: 19     // 最大缩放
});

// 适配单个点
map.fitBounds([[800000, 600000]], {
  padding: 100,
  zoom: 14
});
```

### 设置边界约束

```javascript
// 初始化时设置
var map = new dmapgl.Map({
  maxBounds: [
    [716638.2414098255, 548483.5939021005], // 西南角
    [894455.0756895209, 728066.4667000007]  // 东北角
  ]
});

// 动态设置
map.setMaxBounds([
  [716638.2414098255, 548483.5939021005],
  [894455.0756895209, 728066.4667000007]
]);

// 移除约束
map.setMaxBounds(null);
```

## 综合动画

### easeTo - 平滑过渡

```javascript
map.easeTo({
  center: [810000, 610000],
  zoom: 14,
  bearing: 45,
  pitch: 60,
  duration: 3000,
  easing: (t) => t * t // 自定义缓动函数
});
```

### flyTo - 飞行动画

```javascript
map.flyTo({
  center: [820000, 620000],
  zoom: 15,
  bearing: 90,
  pitch: 45,
  duration: 4000,
  essential: true, // 即使减少运动也执行
  curve: 1.5,      // 飞行曲线
  speed: 1.2       // 飞行速度
});
```

### jumpTo - 立即跳转

```javascript
map.jumpTo({
  center: [800000, 600000],
  zoom: 12,
  bearing: 0,
  pitch: 0
});
```

## 相机控制

### 获取相机状态

```javascript
const camera = map.getCameraOptions();
console.log(camera);
// { center: LngLat, zoom: number, bearing: number, pitch: number }
```

### 禁用/启用交互

```javascript
// 禁用所有交互
map.dragPan.disable();
map.scrollZoom.disable();
map.boxZoom.disable();
map.keyboard.disable();

// 禁用特定方向
map.touchZoomRotate.disableRotation();

// 重新启用
map.dragPan.enable();
```

## 监听视图变化

```javascript
// 移动开始
map.on('movestart', () => {
  console.log('开始移动');
});

// 移动中
map.on('move', () => {
  const center = map.getCenter();
  const zoom = map.getZoom();
  console.log(`当前位置: ${center.lng.toFixed(4)}, ${center.lat.toFixed(4)}, 缩放: ${zoom}`);
});

// 移动结束
map.on('moveend', () => {
  console.log('移动结束');
});

// 缩放变化
map.on('zoomstart', () => {});
map.on('zoom', () => {});
map.on('zoomend', () => {});

// 旋转变化
map.on('rotatestart', () => {});
map.on('rotate', () => {});
map.on('rotateend', () => {});
```

## 实用示例

### 回到初始视图

```javascript
const initialView = {
  center: [800000, 600000],
  zoom: 11,
  bearing: 0,
  pitch: 0
};

function resetView() {
  map.flyTo({
    ...initialView,
    duration: 2000
  });
}
```

### 跟踪用户位置

```javascript
const geolocate = new dmapgl.GeolocateControl({
  positionOptions: { enableHighAccuracy: true },
  trackUserLocation: true,
  showUserHeading: true
});

map.addControl(geolocate);

geolocate.on('geolocate', (e) => {
  const lng = e.coords.longitude;
  const lat = e.coords.latitude;
  
  map.flyTo({
    center: [lng, lat],
    zoom: 16,
    duration: 1500
  });
});
```

### 视口查询要素

```javascript
// 获取当前可视区域内的要素
const features = map.queryRenderedFeatures({
  layers: ['buildings']
});

console.log(`可视区域内有 ${features.length} 个建筑物`);
```

## 注意事项

1. **性能**: 频繁调用 `flyTo` 或 `easeTo` 会影响性能
2. **动画队列**: 新的动画会取消正在进行的动画
3. **边界检查**: 确保坐标在有效范围内
4. **交互冲突**: 程序化控制时注意与用户交互的冲突
5. **内存**: 大量动画时注意清理定时器
