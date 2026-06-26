

# 标记 (Marker)

在地图上添加点标记,支持自定义HTML内容和样式。

## 基础用法

### 创建简单标记

```javascript
// 基本标记
const marker = new dmapgl.Marker()
  .setLngLat([800000, 600000])
  .addTo(map);

// 带颜色的标记
const redMarker = new dmapgl.Marker({ color: '#FF0000' })
  .setLngLat([810000, 610000])
  .addTo(map);
```

### 自定义HTML标记

```javascript
// 创建自定义DOM元素
const el = document.createElement('div');
el.className = 'custom-marker';
el.innerHTML = '<div class="marker-icon">📍</div>';

const customMarker = new dmapgl.Marker({ element: el })
  .setLngLat([800000, 600000])
  .addTo(map);
```

CSS样式:

```css
.custom-marker {
  width: 40px;
  height: 40px;
  background: #3b82f6;
  border-radius: 50% 50% 50% 0;
  transform: rotate(-45deg);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.marker-icon {
  transform: rotate(45deg);
  font-size: 20px;
}
```

## Marker 配置选项

```javascript
const marker = new dmapgl.Marker({
  // 自定义DOM元素
  element: customElement,
  
  // 颜色 (仅当未提供element时有效): red, blue, green等
  color: '#FF0000',
  
  // 锚点位置
  anchor: 'center', // center, top, bottom, left, right
  
  // 偏移量 [x, y]
  offset: [0, -20],
  
  // 可拖拽
  draggable: true,
  
  // 旋转角度
  rotation: 45,
  
  // 旋转对齐方式
  rotationAlignment: 'map', // map, viewport, auto
  
  // 缩放对齐方式
  scaleAlignment: 'auto', // auto, map, viewport
  
  // 点击提示文本
  clickTolerance: 3
});
```

## 标记操作

### 获取和设置位置

```javascript
// 获取位置
const lngLat = marker.getLngLat();
console.log('经度:', lngLat.lng);
console.log('纬度:', lngLat.lat);

// 设置位置
marker.setLngLat([810000, 610000]);

// 移动到新位置(带动画)
marker.setLngLat([810000, 610000]);
```

### 拖拽功能

```javascript
// 启用拖拽
marker.setDraggable(true);

// 禁用拖拽
marker.setDraggable(false);

// 监听拖拽事件
marker.on('dragstart', () => {
  console.log('开始拖拽');
});

marker.on('drag', () => {
  const pos = marker.getLngLat();
  console.log('拖拽中:', pos);
});

marker.on('dragend', () => {
  const pos = marker.getLngLat();
  console.log('拖拽结束:', pos);
});
```

### 显示和隐藏

```javascript
// 从地图移除
marker.remove();

// 重新添加到地图
marker.addTo(map);

// 检查是否在地图上
if (marker.getMap()) {
  console.log('标记已添加到地图');
}
```

### Popup 关联

```javascript
// 创建弹窗
const popup = new dmapgl.Popup({ offset: 25 })
  .setHTML('<h3>北京</h3><p>中国首都</p>');

// 将弹窗绑定到标记
const marker = new dmapgl.Marker()
  .setLngLat([800000, 600000])
  .setPopup(popup)
  .addTo(map);

// 切换弹窗显示
marker.togglePopup();

// 打开弹窗
marker.getPopup().addTo(map);

// 关闭弹窗
marker.getPopup().remove();

// 更新弹窗内容
marker.getPopup().setHTML('<h3>新标题</h3><p>新内容</p>');
```

## 多个标记管理

### 批量添加标记

```javascript
const locations = [
  { name: '北京', coords: [800000, 600000] },
  { name: '上海', coords: [850000, 580000] },
  { name: '广州', coords: [780000, 550000] }
];

const markers = [];

locations.forEach(location => {
  const marker = new dmapgl.Marker({ color: '#3b82f6' })
    .setLngLat(location.coords)
    .setPopup(new dmapgl.Popup().setHTML(`<h3>${location.name}</h3>`))
    .addTo(map);
  
  markers.push(marker);
});
```

### 清除所有标记

```javascript
markers.forEach(marker => marker.remove());
markers.length = 0;
```

### 标记集群 (MarkerCluster)

对于大量标记点,使用聚类提高性能:

```javascript
// 需要引入 supercluster 库
import Supercluster from 'supercluster';

const cluster = new Supercluster({
  radius: 40,
  maxZoom: 16
});

// 加载数据
cluster.load(points.map(point => ({
  type: 'Feature',
  geometry: {
    type: 'Point',
    coordinates: [point.lng, point.lat]
  },
  properties: point
})));

// 根据视口获取聚类结果
const clusters = cluster.getClusters(
  map.getBounds().toArray(),
  Math.floor(map.getZoom())
);

// 渲染聚类标记
clusters.forEach(cluster => {
  const marker = new dmapgl.Marker({
    element: createClusterElement(cluster.properties.point_count)
  })
    .setLngLat(cluster.geometry.coordinates)
    .addTo(map);
});
```

## 动画效果

### 脉冲动画标记

```javascript
// HTML
const pulseEl = document.createElement('div');
pulseEl.className = 'pulse-marker';

const marker = new dmapgl.Marker({ element: pulseEl })
  .setLngLat([800000, 600000])
  .addTo(map);
```

CSS:

```css
.pulse-marker {
  width: 20px;
  height: 20px;
  background: #3b82f6;
  border-radius: 50%;
  position: relative;
}

.pulse-marker::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background: inherit;
  border-radius: 50%;
  animation: pulse 2s ease-out infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(3);
    opacity: 0;
  }
}
```

### 弹跳动画

```javascript
const bounceEl = document.createElement('div');
bounceEl.className = 'bounce-marker';

function animateBounce() {
  bounceEl.style.transform = 'translateY(0)';
  setTimeout(() => {
    bounceEl.style.transform = 'translateY(-10px)';
  }, 500);
}

setInterval(animateBounce, 1000);
```

## 事件处理

```javascript
const marker = new dmapgl.Marker()
  .setLngLat([800000, 600000])
  .addTo(map);

// 点击事件
marker.getElement().addEventListener('click', (e) => {
  e.stopPropagation(); // 阻止地图点击
  console.log('标记被点击');
});

// 鼠标悬停
marker.getElement().addEventListener('mouseenter', () => {
  marker.getElement().style.cursor = 'pointer';
});

// 右键菜单
marker.getElement().addEventListener('contextmenu', (e) => {
  e.preventDefault();
  showContextMenu(e.clientX, e.clientY);
});
```

## 高级用法

### 自定义图标标记

```javascript
function createIconMarker(iconUrl) {
  const el = document.createElement('div');
  el.className = 'icon-marker';
  el.style.backgroundImage = `url(${iconUrl})`;
  el.style.width = '40px';
  el.style.height = '40px';
  el.style.backgroundSize = 'cover';
  
  return el;
}

const iconMarker = new dmapgl.Marker({ element: createIconMarker('/icons/pin.png') })
  .setLngLat([800000, 600000])
  .addTo(map);
```

### 轨迹回放

```javascript
const path = [
  [800000, 600000],
  [805000, 605000],
  [810000, 610000],
  [815000, 615000]
];

let currentIndex = 0;
const movingMarker = new dmapgl.Marker()
  .setLngLat(path[0])
  .addTo(map);

function moveAlongPath() {
  if (currentIndex < path.length - 1) {
    currentIndex++;
    movingMarker.setLngLat(path[currentIndex]);
    setTimeout(moveAlongPath, 1000);
  }
}

moveAlongPath();
```

### 过滤可见标记

```javascript
// 只显示当前视口内的标记
function updateVisibleMarkers() {
  const bounds = map.getBounds();
  
  allMarkers.forEach(marker => {
    const lngLat = marker.getLngLat();
    if (bounds.contains(lngLat)) {
      marker.addTo(map);
    } else {
      marker.remove();
    }
  });
}

map.on('moveend', updateVisibleMarkers);
```

## 注意事项

1. **性能**: 超过100个标记建议使用 SymbolLayer 或聚类
2. **内存**: 移除标记时调用 `remove()` 释放资源
3. **Z-index**: 标记默认在最上层,可通过CSS调整
4. **响应式**: 标记大小不会随缩放自动调整,需手动处理
