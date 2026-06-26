

# 动画 (Animation)

DMap GL提供流畅的相机动画和过渡效果。

## 飞行动画 (flyTo)

从一个视图平滑飞行到另一个视图。

### 基础用法

```javascript
map.flyTo({
  center: [810000, 610000],
  zoom: 14,
  duration: 3000  // 毫秒
});
```

### 完整配置

```javascript
map.flyTo({
  // 目标中心点
  center: [810000, 610000],
  
  // 目标缩放级别
  zoom: 15,
  
  // 目标旋转角度
  bearing: 45,
  
  // 目标俯仰角
  pitch: 60,
  
  // 动画时长(毫秒)
  duration: 4000,
  
  // 飞行曲线(越大弧度越大)
  curve: 1.5,
  
  // 飞行速度
  speed: 1.2,
  
  // 屏幕像素/毫秒的最大滚动速度
  screenSpeed: 1,
  
  // 即使减少运动也执行(无障碍)
  essential: true,
  
  // 缓动函数
  easing: (t) => t * t
});
```

### 监听动画状态

```javascript
// 动画开始
map.on('movestart', (e) => {
  if (e.originalEvent && e.originalEvent.flyTo) {
    console.log('飞行动画开始');
  }
});

// 动画结束
map.on('moveend', () => {
  console.log('飞行动画结束');
});

// 中断动画
map.stop();
```

## 平滑过渡 (easeTo)

使用线性插值平滑过渡到新视图。

### 基础用法

```javascript
map.easeTo({
  center: [810000, 610000],
  zoom: 14,
  duration: 2000
});
```

### 自定义缓动

```javascript
// 缓入缓出
map.easeTo({
  center: [810000, 610000],
  duration: 2000,
  easing: (t) => {
    return t < 0.5 
      ? 2 * t * t 
      : -1 + (4 - 2 * t) * t;
  }
});

// 弹性效果
map.easeTo({
  zoom: 15,
  duration: 1500,
  easing: (t) => {
    return Math.pow(2, -10 * t) * Math.sin((t - 0.075) * (2 * Math.PI) / 0.3) + 1;
  }
});
```

### 仅改变单个属性

```javascript
// 仅缩放
map.easeTo({ zoom: 12 });

// 仅旋转
map.easeTo({ bearing: 90 });

// 仅俯仰
map.easeTo({ pitch: 45 });

// 仅平移
map.easeTo({ center: [116.5, 39.9] });
```

## 立即跳转 (jumpTo)

无动画立即跳转到新视图。

```javascript
map.jumpTo({
  center: [810000, 610000],
  zoom: 14,
  bearing: 45,
  pitch: 60
});
```

## 专用动画方法

### zoomTo - 缩放到指定级别

```javascript
map.zoomTo(15, {
  duration: 1000,
  easing: (t) => t
});
```

### panTo - 平移到指定位置

```javascript
map.panTo([810000, 610000], {
  duration: 1500,
  easing: (t) => t
});
```

### rotateTo - 旋转到指定角度

```javascript
map.rotateTo(90, {
  duration: 1000
});

// 重置为北向
map.resetNorth({ duration: 500 });
```

### pitchTo - 俯仰到指定角度

```javascript
map.pitchTo(60, {
  duration: 1000
});
```

## 相机动画序列

### 链式动画

```javascript
function cameraTour() {
  map.flyTo({
    center: [800000, 600000],
    zoom: 12,
    duration: 3000
  });
  
  setTimeout(() => {
    map.flyTo({
      center: [116.407, 39.904],
      zoom: 15,
      bearing: 45,
      duration: 3000
    });
  }, 3000);
  
  setTimeout(() => {
    map.flyTo({
      center: [800000, 600000],
      zoom: 12,
      bearing: 0,
      duration: 3000
    });
  }, 6000);
}

cameraTour();
```

### Promise封装

```javascript
function flyToPromise(options) {
  return new Promise((resolve) => {
    map.flyTo({
      ...options,
      essential: true
    });
    
    map.once('moveend', resolve);
  });
}

async function cameraSequence() {
  await flyToPromise({
    center: [800000, 600000],
    zoom: 12,
    duration: 2000
  });
  
  await flyToPromise({
    center: [116.407, 39.904],
    zoom: 15,
    bearing: 45,
    duration: 2000
  });
  
  await flyToPromise({
    center: [800000, 600000],
    zoom: 12,
    duration: 2000
  });
  
  console.log('动画序列完成');
}

cameraSequence();
```

## 标记动画

### 移动标记

```javascript
const marker = new dmapgl.Marker()
  .setLngLat([800000, 600000])
  .addTo(map);

// 平滑移动标记
function moveMarker(targetLngLat, duration = 1000) {
  const startLngLat = marker.getLngLat();
  const startTime = performance.now();
  
  function animate(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // 线性插值
    const lng = startLngLat.lng + (targetLngLat[0] - startLngLat.lng) * progress;
    const lat = startLngLat.lat + (targetLngLat[1] - startLngLat.lat) * progress;
    
    marker.setLngLat([lng, lat]);
    
    if (progress < 1) {
      requestAnimationFrame(animate);
    }
  }
  
  requestAnimationFrame(animate);
}

moveMarker([116.407, 39.904], 2000);
```

### 脉冲动画

```javascript
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

.pulse-marker::before,
.pulse-marker::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background: inherit;
  border-radius: 50%;
  animation: pulse 2s ease-out infinite;
}

.pulse-marker::after {
  animation-delay: 1s;
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

const marker = new dmapgl.Marker({ element: bounceEl })
  .setLngLat([800000, 600000])
  .addTo(map);
```

CSS:

```css
.bounce-marker {
  width: 30px;
  height: 30px;
  background: #ef4444;
  border-radius: 50% 50% 50% 0;
  transform: rotate(-45deg);
  animation: bounce 1s ease infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: rotate(-45deg) translateY(0);
  }
  50% {
    transform: rotate(-45deg) translateY(-10px);
  }
}
```

## 图层动画

### 淡入淡出

```javascript
// 添加图层时设置初始透明度
map.addLayer({
  id: 'fade-layer',
  type: 'fill',
  source: 'my-source',
  paint: {
    'fill-opacity': 0
  }
});

// 淡入
function fadeIn(layerId, duration = 1000) {
  const start = performance.now();
  const targetOpacity = 1;
  
  function animate(currentTime) {
    const elapsed = currentTime - start;
    const progress = Math.min(elapsed / duration, 1);
    
    map.setPaintProperty(layerId, 'fill-opacity', progress * targetOpacity);
    
    if (progress < 1) {
      requestAnimationFrame(animate);
    }
  }
  
  requestAnimationFrame(animate);
}

fadeIn('fade-layer', 1500);

// 淡出
function fadeOut(layerId, duration = 1000) {
  const start = performance.now();
  const startOpacity = map.getPaintProperty(layerId, 'fill-opacity');
  
  function animate(currentTime) {
    const elapsed = currentTime - start;
    const progress = Math.min(elapsed / duration, 1);
    
    map.setPaintProperty(
      layerId, 
      'fill-opacity', 
      startOpacity * (1 - progress)
    );
    
    if (progress < 1) {
      requestAnimationFrame(animate);
    }
  }
  
  requestAnimationFrame(animate);
}
```

### 渐变显示路径

```javascript
// 添加线图层
map.addLayer({
  id: 'animated-line',
  type: 'line',
  source: 'path-source',
  paint: {
    'line-color': '#3b82f6',
    'line-width': 4,
    'line-dasharray': [0, 1000]
  }
});

// 动画显示
function drawLine(duration = 2000) {
  const start = performance.now();
  
  function animate(currentTime) {
    const elapsed = currentTime - start;
    const progress = Math.min(elapsed / duration, 1);
    
    map.setPaintProperty('animated-line', 'line-dasharray', [
      progress * 1000,
      1000
    ]);
    
    if (progress < 1) {
      requestAnimationFrame(animate);
    }
  }
  
  requestAnimationFrame(animate);
}

drawLine(3000);
```

## 视口动画

### 适配边界动画

```javascript
map.fitBounds([
  [750000, 560000],
  [850000, 650000]
], {
  padding: 50,
  duration: 2000,
  easing: (t) => t
});
```

### 3D建筑动画

```javascript
// 动态改变建筑高度
let buildingHeight = 0;
const targetHeight = 100;

function animateBuildings() {
  buildingHeight += 2;
  
  if (buildingHeight <= targetHeight) {
    map.setPaintProperty('3d-buildings', 'fill-extrusion-height', buildingHeight);
    requestAnimationFrame(animateBuildings);
  }
}

animateBuildings();
```

## 实用示例

### 轨迹回放

```javascript
class TrackPlayer {
  constructor(trackData) {
    this.track = trackData;
    this.currentIndex = 0;
    this.isPlaying = false;
    this.speed = 1000; // 每点间隔(ms)
    
    this.marker = new dmapgl.Marker()
      .setLngLat(trackData[0])
      .addTo(map);
    
    // 添加轨迹线
    map.addSource('track', {
      type: 'geojson',
      data: {
        type: 'Feature',
        geometry: {
          type: 'LineString',
          coordinates: trackData.slice(0, 1)
        }
      }
    });
    
    map.addLayer({
      id: 'track-line',
      type: 'line',
      source: 'track',
      paint: {
        'line-color': '#3b82f6',
        'line-width': 3
      }
    });
  }
  
  play() {
    if (this.isPlaying) return;
    this.isPlaying = true;
    this.animate();
  }
  
  pause() {
    this.isPlaying = false;
  }
  
  animate() {
    if (!this.isPlaying || this.currentIndex >= this.track.length - 1) {
      this.isPlaying = false;
      return;
    }
    
    this.currentIndex++;
    
    // 更新标记位置
    const pos = this.track[this.currentIndex];
    this.marker.setLngLat(pos);
    
    // 更新轨迹线
    const source = map.getSource('track');
    source.setData({
      type: 'Feature',
      geometry: {
        type: 'LineString',
        coordinates: this.track.slice(0, this.currentIndex + 1)
      }
    });
    
    // 相机跟随
    map.panTo(pos, { duration: this.speed });
    
    setTimeout(() => this.animate(), this.speed);
  }
  
  reset() {
    this.pause();
    this.currentIndex = 0;
    this.marker.setLngLat(this.track[0]);
    
    map.getSource('track').setData({
      type: 'Feature',
      geometry: {
        type: 'LineString',
        coordinates: [this.track[0]]
      }
    });
  }
}

// 使用
const player = new TrackPlayer([
  [800000, 600000],
  [805000, 605000],
  [810000, 610000],
  [815000, 615000]
]);

player.play();
```

### 闪烁效果

```javascript
function blinkLayer(layerId, times = 3, interval = 500) {
  let count = 0;
  
  function toggle() {
    if (count >= times * 2) return;
    
    const visibility = count % 2 === 0 ? 'none' : 'visible';
    map.setLayoutProperty(layerId, 'visibility', visibility);
    
    count++;
    setTimeout(toggle, interval);
  }
  
  toggle();
}

blinkLayer('highlight-layer', 5, 300);
```

## 注意事项

1. **性能**: 避免同时运行过多动画
2. **内存**: 动画完成后清理资源
3. **用户体验**: 尊重用户的"减少运动"偏好
4. **中断处理**: 新动画会中断旧动画
5. **缓动函数**: 选择合适的缓动提升体验
6. **时长控制**: 动画不宜过长或过短
7. **可访问性**: 提供关闭动画的选项
