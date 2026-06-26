

# 事件系统 (Events)

DMap GL使用事件系统响应地图交互和状态变化。

## 事件绑定

### 基础用法

```javascript
// 绑定事件
map.on('click', (e) => {
  console.log('地图被点击', e);
});

// 绑定到特定图层
map.on('click', 'my-layer', (e) => {
  console.log('图层被点击', e.features[0]);
});

// 解绑事件
map.off('click', handler);

// 只触发一次
map.once('load', () => {
  console.log('地图加载完成');
});
```

## 鼠标事件

### click - 点击

```javascript
map.on('click', (e) => {
  console.log('点击位置:', e.lngLat);
  console.log('像素坐标:', e.point);
  console.log('原始事件:', e.originalEvent);
  
  // 查询点击位置的要素
  const features = map.queryRenderedFeatures(e.point);
  console.log('要素数量:', features.length);
});

// 图层点击
map.on('click', 'buildings', (e) => {
  const building = e.features[0].properties;
  console.log('建筑物信息:', building);
});
```

### dblclick - 双击

```javascript
map.on('dblclick', (e) => {
  console.log('双击位置:', e.lngLat);
});
```

### mousedown / mouseup - 鼠标按下/释放

```javascript
map.on('mousedown', (e) => {
  console.log('鼠标按下');
});

map.on('mouseup', (e) => {
  console.log('鼠标释放');
});
```

### mousemove - 鼠标移动

```javascript
map.on('mousemove', (e) => {
  const coords = `${e.lngLat.lng.toFixed(4)}, ${e.lngLat.lat.toFixed(4)}`;
  document.getElementById('coords').textContent = coords;
});

// 图层悬停
map.on('mousemove', 'cities', (e) => {
  map.getCanvas().style.cursor = 'pointer';
  
  // 高亮显示
  if (e.features.length > 0) {
    showTooltip(e.point, e.features[0].properties.name);
  }
});

map.on('mouseleave', 'cities', () => {
  map.getCanvas().style.cursor = '';
  hideTooltip();
});
```

### mouseover / mouseout - 鼠标进入/离开

```javascript
map.on('mouseover', 'my-layer', (e) => {
  console.log('鼠标进入图层');
});

map.on('mouseout', 'my-layer', (e) => {
  console.log('鼠标离开图层');
});
```

### contextmenu - 右键菜单

```javascript
map.on('contextmenu', (e) => {
  e.preventDefault();
  
  showContextMenu(e.originalEvent.clientX, e.originalEvent.clientY, {
    lng: e.lngLat.lng,
    lat: e.lngLat.lat
  });
});
```

## 触摸事件

### touchstart / touchmove / touchend

```javascript
map.on('touchstart', (e) => {
  console.log('触摸开始', e.points);
});

map.on('touchmove', (e) => {
  console.log('触摸移动');
});

map.on('touchend', (e) => {
  console.log('触摸结束');
});
```

## 地图状态事件

### load - 地图加载完成

```javascript
map.on('load', () => {
  console.log('地图样式加载完成');
  
  // 安全地添加图层和数据源
  addCustomLayers();
});
```

### render - 渲染帧

```javascript
let frameCount = 0;

map.on('render', () => {
  frameCount++;
  console.log(`已渲染 ${frameCount} 帧`);
});
```

### idle - 空闲状态

```javascript
map.on('idle', () => {
  console.log('地图处于空闲状态(无动画、无加载)');
});
```

### error - 错误

```javascript
map.on('error', (e) => {
  console.error('地图错误:', e.error);
  
  // 记录错误日志
  logError({
    message: e.error.message,
    stack: e.error.stack,
    timestamp: new Date().toISOString()
  });
});
```

## 视图变化事件

### movestart / move / moveend - 移动

```javascript
map.on('movestart', () => {
  console.log('开始移动');
  showLoadingIndicator();
});

map.on('move', () => {
  const center = map.getCenter();
  const zoom = map.getZoom();
  console.log(`移动中: ${center.lng.toFixed(4)}, ${center.lat.toFixed(4)}, zoom: ${zoom}`);
});

map.on('moveend', () => {
  console.log('移动结束');
  hideLoadingIndicator();
  
  // 更新URL
  updateUrlHash();
  
  // 加载新数据
  loadDataForViewport();
});
```

### zoomstart / zoom / zoomend - 缩放

```javascript
map.on('zoomstart', () => {
  console.log('开始缩放');
});

map.on('zoom', () => {
  console.log('当前缩放:', map.getZoom());
});

map.on('zoomend', () => {
  console.log('缩放结束');
});
```

### rotatestart / rotate / rotateend - 旋转

```javascript
map.on('rotatestart', () => {
  console.log('开始旋转');
});

map.on('rotate', () => {
  console.log('当前角度:', map.getBearing());
});

map.on('rotateend', () => {
  console.log('旋转结束');
});
```

### pitchstart / pitch / pitchend - 俯仰

```javascript
map.on('pitchstart', () => {
  console.log('开始俯仰');
});

map.on('pitch', () => {
  console.log('当前俯仰角:', map.getPitch());
});

map.on('pitchend', () => {
  console.log('俯仰结束');
});
```

## 数据加载事件

### dataloading - 数据加载中

```javascript
map.on('dataloading', (e) => {
  console.log('数据类型加载中:', e.dataType);
  // dataType: 'source' | 'style'
});
```

### data - 数据加载

```javascript
map.on('data', (e) => {
  console.log('数据已加载:', e.dataType);
  
  if (e.isSourceLoaded) {
    console.log('所有源数据已加载');
  }
});
```

### sourcedataloading / sourcedata - 源数据

```javascript
map.on('sourcedataloading', (e) => {
  console.log('源数据加载中:', e.sourceId);
});

map.on('sourcedata', (e) => {
  console.log('源数据已加载:', e.sourceId);
  
  if (e.isSourceLoaded && e.sourceId === 'my-source') {
    console.log('我的数据源加载完成');
  }
});
```

### styledataloading / styledata - 样式数据

```javascript
map.on('styledataloading', () => {
  console.log('样式数据加载中');
});

map.on('styledata', () => {
  console.log('样式数据已加载');
});
```

## 图层事件

### layer.add / layer.remove - 图层添加/移除

```javascript
map.on('layer.add', (e) => {
  console.log('图层已添加:', e.layer.id);
});

map.on('layer.remove', (e) => {
  console.log('图层已移除:', e.layer.id);
});
```

## 实用示例

### 坐标显示

```javascript
const coordDisplay = document.getElementById('coordinates');

map.on('mousemove', (e) => {
  coordDisplay.textContent = 
    `经度: ${e.lngLat.lng.toFixed(6)}\n纬度: ${e.lngLat.lat.toFixed(6)}`;
});
```

### 要素信息查询

```javascript
map.on('click', (e) => {
  const features = map.queryRenderedFeatures(e.point);
  
  if (features.length > 0) {
    const properties = features[0].properties;
    
    new dmapgl.Popup()
      .setLngLat(e.lngLat)
      .setHTML(createInfoPopup(properties))
      .addTo(map);
  }
});

function createInfoPopup(properties) {
  let html = '<div class="info-popup">';
  for (const [key, value] of Object.entries(properties)) {
    html += `<p><strong>${key}:</strong> ${value}</p>`;
  }
  html += '</div>';
  return html;
}
```

### 绘制工具

```javascript
let isDrawing = false;
let drawPath = [];

map.on('mousedown', (e) => {
  isDrawing = true;
  drawPath = [[e.lngLat.lng, e.lngLat.lat]];
  
  // 创建临时图层
  map.addSource('draw-source', {
    type: 'geojson',
    data: {
      type: 'Feature',
      geometry: {
        type: 'LineString',
        coordinates: drawPath
      }
    }
  });
  
  map.addLayer({
    id: 'draw-layer',
    type: 'line',
    source: 'draw-source',
    paint: {
      'line-color': '#3b82f6',
      'line-width': 2
    }
  });
});

map.on('mousemove', (e) => {
  if (!isDrawing) return;
  
  drawPath.push([e.lngLat.lng, e.lngLat.lat]);
  
  const source = map.getSource('draw-source');
  source.setData({
    type: 'Feature',
    geometry: {
      type: 'LineString',
      coordinates: drawPath
    }
  });
});

map.on('mouseup', () => {
  isDrawing = false;
  console.log('绘制完成:', drawPath);
});
```

### 视口数据加载

```javascript
let isLoading = false;

async function loadDataForViewport() {
  if (isLoading) return;
  
  isLoading = true;
  const bounds = map.getBounds();
  
  try {
    const response = await fetch(`/api/data?bbox=${bounds.toArray()}`);
    const data = await response.json();
    
    if (map.getSource('viewport-data')) {
      map.getSource('viewport-data').setData(data);
    } else {
      map.addSource('viewport-data', {
        type: 'geojson',
        data: data
      });
      
      map.addLayer({
        id: 'viewport-layer',
        type: 'circle',
        source: 'viewport-data',
        paint: {
          'circle-radius': 5,
          'circle-color': '#3b82f6'
        }
      });
    }
  } catch (error) {
    console.error('加载数据失败:', error);
  } finally {
    isLoading = false;
  }
}

map.on('moveend', loadDataForViewport);
```

### 性能监控

```javascript
const metrics = {
  renders: 0,
  moves: 0,
  errors: 0
};

map.on('render', () => {
  metrics.renders++;
});

map.on('move', () => {
  metrics.moves++;
});

map.on('error', () => {
  metrics.errors++;
});

// 定期上报
setInterval(() => {
  console.log('性能指标:', metrics);
  // sendToAnalytics(metrics);
}, 60000);
```

### 历史记录

```javascript
const viewHistory = [];

map.on('moveend', () => {
  viewHistory.push({
    center: map.getCenter(),
    zoom: map.getZoom(),
    bearing: map.getBearing(),
    pitch: map.getPitch(),
    timestamp: Date.now()
  });
  
  // 保持最近50条记录
  if (viewHistory.length > 50) {
    viewHistory.shift();
  }
});

// 后退功能
function goBack() {
  if (viewHistory.length > 1) {
    viewHistory.pop(); // 移除当前视图
    const previous = viewHistory[viewHistory.length - 1];
    
    map.flyTo({
      center: previous.center,
      zoom: previous.zoom,
      bearing: previous.bearing,
      pitch: previous.pitch,
      duration: 1000
    });
  }
}
```

## 事件对象属性

### MapMouseEvent

```javascript
{
  type: 'click',              // 事件类型
  target: Map,                // 地图实例
  originalEvent: MouseEvent,  // 原始DOM事件
  point: Point,               // 像素坐标 {x, y}
  lngLat: LngLat,             // 地理坐标 {lng, lat}
  features: Array             // 要素数组(仅图层事件)
}
```

### MapTouchEvent

```javascript
{
  type: 'touchstart',
  target: Map,
  originalEvent: TouchEvent,
  points: Array,              // 触摸点数组
  lngLats: Array              // 地理坐标数组
}
```

### DataEvent

```javascript
{
  type: 'data',
  target: Map,
  dataType: 'source',         // 'source' | 'style'
  isSourceLoaded: boolean,
  sourceId: string            // 源ID(仅source类型)
}
```

## 注意事项

1. **性能**: 避免在高频事件(move, render)中执行耗时操作
2. **内存泄漏**: 组件卸载时解绑所有事件监听器
3. **事件冒泡**: 使用 `stopPropagation()` 阻止事件传播
4. **异步处理**: 事件处理器中的异步操作注意错误处理
5. **节流防抖**: 对高频事件使用节流或防抖
6. **图层事件**: 确保图层存在后再绑定事件
7. **错误处理**: 始终监听 error 事件
