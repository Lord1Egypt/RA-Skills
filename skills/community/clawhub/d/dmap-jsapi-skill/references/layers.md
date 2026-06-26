

# 图层管理 (Layers)

图层定义数据如何在地图上渲染,包括样式、颜色、大小等视觉属性。

## 添加图层

### 基础用法

```javascript
map.addLayer({
  id: 'my-layer',
  type: 'circle',
  source: 'my-source',
  paint: {
    'circle-radius': 5,
    'circle-color': '#3b82f6'
  }
});
```

### 完整配置

```javascript
map.addLayer({
  // 图层ID(必须唯一)
  id: 'buildings',
  
  // 图层类型
  type: 'fill',
  
  // 数据源
  source: 'building-source',
  
  // 矢量瓦片的图层名(仅矢量瓦片需要)
  'source-layer': 'building',
  
  // 最小缩放级别
  minzoom: 12,
  
  // 最大缩放级别
  maxzoom: 19,
  
  // 过滤器
  filter: ['==', 'type', 'residential'],
  
  // 布局属性
  layout: {
    visibility: 'visible' // visible 或 none
  },
  
  // 绘制属性
  paint: {
    'fill-color': '#cccccc',
    'fill-opacity': 0.7
  },
  
  // 元数据
  metadata: {
    description: '建筑物图层'
  }
});
```

## 图层类型

### Circle - 圆点

```javascript
map.addLayer({
  id: 'points',
  type: 'circle',
  source: 'data',
  paint: {
    'circle-radius': 8,
    'circle-color': '#3b82f6',
    'circle-stroke-width': 2,
    'circle-stroke-color': '#ffffff',
    'circle-opacity': 0.8,
    'circle-blur': 0
  }
});
```

### Symbol - 符号/文本

```javascript
// 图标
map.addLayer({
  id: 'icons',
  type: 'symbol',
  source: 'places',
  layout: {
    'icon-image': 'restaurant-15',
    'icon-size': 1,
    'icon-allow-overlap': false,
    'icon-ignore-placement': false
  }
});

// 文本标签
map.addLayer({
  id: 'labels',
  type: 'symbol',
  source: 'places',
  layout: {
    'text-field': ['get', 'name'],
    'text-font': ['Open Sans Regular'],
    'text-size': 14,
    'text-offset': [0, -1.5],
    'text-anchor': 'top',
    'text-allow-overlap': false
  },
  paint: {
    'text-color': '#333333',
    'text-halo-color': '#ffffff',
    'text-halo-width': 2
  }
});
```

### Line - 线

```javascript
map.addLayer({
  id: 'roads',
  type: 'line',
  source: 'streets',
  'source-layer': 'road',
  layout: {
    'line-cap': 'round',
    'line-join': 'round'
  },
  paint: {
    'line-color': '#3b82f6',
    'line-width': 3,
    'line-opacity': 0.8,
    'line-dasharray': [2, 2] // 虚线
  }
});
```

### Fill - 填充面

```javascript
map.addLayer({
  id: 'parks',
  type: 'fill',
  source: 'landuse',
  'source-layer': 'park',
  paint: {
    'fill-color': '#4ade80',
    'fill-opacity': 0.5,
    'fill-outline-color': '#22c55e'
  }
});
```

### Fill Extrusion - 3D挤出

```javascript
map.addLayer({
  id: '3d-buildings',
  type: 'fill-extrusion',
  source: 'buildings',
  'source-layer': 'building',
  minzoom: 15,
  paint: {
    'fill-extrusion-color': '#aaa',
    'fill-extrusion-height': ['get', 'height'],
    'fill-extrusion-base': ['get', 'min_height'],
    'fill-extrusion-opacity': 0.6
  }
});
```

### Raster - 栅格

```javascript
map.addLayer({
  id: 'satellite',
  type: 'raster',
  source: 'satellite-source',
  paint: {
    'raster-opacity': 0.8,
    'raster-brightness-min': 0,
    'raster-brightness-max': 1,
    'raster-saturation': 0,
    'raster-contrast': 0
  }
});
```

### Heatmap - 热力图

```javascript
map.addLayer({
  id: 'heatmap',
  type: 'heatmap',
  source: 'earthquakes',
  paint: {
    'heatmap-weight': [
      'interpolate',
      ['linear'],
      ['get', 'magnitude'],
      0, 0,
      6, 1
    ],
    'heatmap-intensity': ['interpolate', ['linear'], ['zoom'], 0, 1, 9, 3],
    'heatmap-color': [
      'interpolate',
      ['linear'],
      ['heatmap-density'],
      0, 'rgba(0, 0, 255, 0)',
      0.2, 'royalblue',
      0.4, 'cyan',
      0.6, 'lime',
      0.8, 'yellow',
      1, 'red'
    ],
    'heatmap-radius': ['interpolate', ['linear'], ['zoom'], 0, 2, 9, 20],
    'heatmap-opacity': 0.8
  }
});
```

### Background - 背景

```javascript
map.addLayer({
  id: 'background',
  type: 'background',
  paint: {
    'background-color': '#f0f0f0',
    'background-opacity': 1
  }
});
```

## 图层操作

### 检查图层是否存在

```javascript
if (map.getLayer('my-layer')) {
  console.log('图层存在');
}
```

### 移除图层

```javascript
map.removeLayer('my-layer');
```

### 移动图层顺序

```javascript
// 移动到最上层
map.moveLayer('my-layer');

// 移动到指定图层之下
map.moveLayer('my-layer', 'below-layer-id');

// 移动到指定索引
const layers = map.getStyle().layers;
map.moveLayer('my-layer', null, 5);
```

### 显示/隐藏图层

```javascript
// 隐藏
map.setLayoutProperty('my-layer', 'visibility', 'none');

// 显示
map.setLayoutProperty('my-layer', 'visibility', 'visible');

// 切换
function toggleLayer(layerId) {
  const visibility = map.getLayoutProperty(layerId, 'visibility');
  map.setLayoutProperty(
    layerId,
    'visibility',
    visibility === 'visible' ? 'none' : 'visible'
  );
}
```

## 动态更新样式

### 更新绘制属性

```javascript
// 更新单个属性
map.setPaintProperty('my-layer', 'circle-radius', 10);
map.setPaintProperty('my-layer', 'circle-color', '#ff0000');

// 获取当前属性值
const radius = map.getPaintProperty('my-layer', 'circle-radius');
console.log('当前半径:', radius);
```

### 更新布局属性

```javascript
map.setLayoutProperty('my-layer', 'text-size', 16);
map.setLayoutProperty('my-layer', 'icon-size', 1.5);
```

### 更新过滤器

```javascript
// 只显示特定类型
map.setFilter('my-layer', ['==', 'type', 'city']);

// 多条件过滤
map.setFilter('my-layer', [
  'all',
  ['==', 'type', 'city'],
  ['>', 'population', 1000000]
]);

// 清除过滤
map.setFilter('my-layer', null);
```

## 数据驱动样式

### 基于属性设置样式

```javascript
map.addLayer({
  id: 'cities',
  type: 'circle',
  source: 'places',
  paint: {
    // 根据人口设置半径
    'circle-radius': [
      'interpolate',
      ['linear'],
      ['get', 'population'],
      0, 5,
      1000000, 10,
      10000000, 20
    ],
    
    // 根据类型设置颜色
    'circle-color': [
      'match',
      ['get', 'type'],
      'city', '#3b82f6',
      'town', '#10b981',
      'village', '#f59e0b',
      '#999999' // 默认值
    ]
  }
});
```

### 缩放级别驱动样式

```javascript
map.addLayer({
  id: 'roads',
  type: 'line',
  source: 'streets',
  paint: {
    // 根据缩放级别调整线宽
    'line-width': [
      'interpolate',
      ['exponential', 1.5],
      ['zoom'],
      5, 1,
      10, 2,
      15, 5,
      20, 10
    ]
  }
});
```

### 表达式示例

```javascript
// 数学运算
'circle-radius': ['+', ['get', 'base_radius'], 2]

// 条件判断
'circle-color': [
  'case',
  ['>', ['get', 'value'], 100], '#ff0000',
  ['>', ['get', 'value'], 50], '#ffff00',
  '#00ff00'
]

// 字符串操作
'text-field': ['upcase', ['get', 'name']]

// 数组操作
'circle-color': ['at', 0, ['get', 'colors']]

// 类型转换
'circle-radius': ['to-number', ['get', 'radius'], 5]
```

## 图层查询

### 查询渲染的要素

```javascript
// 点击位置查询
map.on('click', (e) => {
  const features = map.queryRenderedFeatures(e.point, {
    layers: ['my-layer']
  });
  
  if (features.length > 0) {
    console.log('点击的要素:', features[0].properties);
  }
});

// 矩形区域查询
const features = map.queryRenderedFeatures([
  [x1, y1], // 左上角
  [x2, y2]  // 右下角
], {
  layers: ['layer1', 'layer2']
});
```

### 查询源数据

```javascript
const features = map.querySourceFeatures('my-source', {
  sourceLayer: 'my-source-layer',
  filter: ['==', 'type', 'city']
});

console.log(`找到 ${features.length} 个要素`);
```

## 图层交互

### 点击事件

```javascript
map.on('click', 'my-layer', (e) => {
  const feature = e.features[0];
  
  new dmapgl.Popup()
    .setLngLat(e.lngLat)
    .setHTML(`<h3>${feature.properties.name}</h3>`)
    .addTo(map);
});
```

### 鼠标悬停

```javascript
// 悬停高亮
let hoveredStateId = null;

map.on('mousemove', 'my-layer', (e) => {
  if (e.features.length > 0) {
    if (hoveredStateId !== null) {
      map.setFeatureState(
        { source: 'my-source', id: hoveredStateId },
        { hover: false }
      );
    }
    
    hoveredStateId = e.features[0].id;
    map.setFeatureState(
      { source: 'my-source', id: hoveredStateId },
      { hover: true }
    );
  }
});

map.on('mouseleave', 'my-layer', () => {
  if (hoveredStateId !== null) {
    map.setFeatureState(
      { source: 'my-source', id: hoveredStateId },
      { hover: false }
    );
  }
  hoveredStateId = null;
});

// 使用状态驱动样式
map.addLayer({
  id: 'my-layer',
  type: 'fill',
  source: 'my-source',
  paint: {
    'fill-color': [
      'case',
      ['boolean', ['feature-state', 'hover'], false],
      '#ff0000',
      '#3b82f6'
    ]
  }
});
```

### 光标变化

```javascript
map.on('mouseenter', 'my-layer', () => {
  map.getCanvas().style.cursor = 'pointer';
});

map.on('mouseleave', 'my-layer', () => {
  map.getCanvas().style.cursor = '';
});
```

## 实用示例

### 图层切换器

```javascript
const layers = [
  { id: 'satellite', name: '卫星图' },
  { id: 'streets', name: '街道图' },
  { id: 'dark', name: '深色图' }
];

layers.forEach(layer => {
  const button = document.createElement('button');
  button.textContent = layer.name;
  button.onclick = () => {
    // 隐藏所有图层
    layers.forEach(l => {
      map.setLayoutProperty(l.id, 'visibility', 'none');
    });
    
    // 显示选中图层
    map.setLayoutProperty(layer.id, 'visibility', 'visible');
  };
  
  document.getElementById('layer-switcher').appendChild(button);
});
```

### 动态过滤

```javascript
// 搜索框过滤
document.getElementById('search').addEventListener('input', (e) => {
  const query = e.target.value.toLowerCase();
  
  if (query === '') {
    map.setFilter('cities', null);
  } else {
    map.setFilter('cities', [
      '>=',
      ['length', ['downcase', ['get', 'name']]],
      0
    ]);
  }
});
```

### 图层透明度控制

```javascript
document.getElementById('opacity-slider').addEventListener('input', (e) => {
  const opacity = parseFloat(e.target.value);
  map.setPaintProperty('my-layer', 'fill-opacity', opacity);
});
```

## 注意事项

1. **图层顺序**: 后添加的图层在上层
2. **性能**: 避免过多图层,合并相似样式
3. **内存**: 移除不需要的图层
4. **ID唯一性**: 每个图层ID必须唯一
5. **数据源依赖**: 移除数据源前先移除相关图层
6. **表达式性能**: 复杂表达式影响渲染性能
7. **可见性**: 隐藏图层仍会占用资源,考虑移除
