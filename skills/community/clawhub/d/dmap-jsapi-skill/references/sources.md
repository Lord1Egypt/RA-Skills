

# 数据源 (Sources)

数据源定义地图上显示的数据,包括GeoJSON、矢量瓦片、栅格瓦片等类型。

## GeoJSONSource

用于显示GeoJSON格式的数据。

### 基础用法

```javascript
// 从URL加载
map.addSource('points', {
  type: 'geojson',
  data: 'https://example.com/data.geojson'
});

// 直接传入数据
map.addSource('points', {
  type: 'geojson',
  data: {
    type: 'FeatureCollection',
    features: [
      {
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: [800000, 600000]
        },
        properties: {
          name: '北京'
        }
      }
    ]
  }
});
```

### 配置选项

```javascript
map.addSource('data', {
  type: 'geojson',
  data: geojsonData,
  
  // 最大缩放级别
  maxzoom: 14,
  
  // 瓦片缓冲大小
  buffer: 128,
  
  // 容差(简化几何)
  tolerance: 0.375,
  
  // 启用聚类
  cluster: true,
  clusterMaxZoom: 14,
  clusterRadius: 50,
  
  // 聚类属性
  clusterProperties: {
    sum: ['+', ['get', 'value']]
  },
  
  // 行缓冲
  lineMetrics: false,
  
  // 生成ID
  generateId: false,
  
  // 促进ID
  promoteId: null
});
```

### 动态更新数据

```javascript
// 获取数据源
const source = map.getSource('points');

// 更新数据
source.setData(newGeoJsonData);

// 增量更新
source.updateData({
  type: 'FeatureCollection',
  features: updatedFeatures
});
```

### 聚类功能

```javascript
map.addSource('earthquakes', {
  type: 'geojson',
  data: earthquakeData,
  cluster: true,
  clusterMaxZoom: 14,
  clusterRadius: 50
});

// 添加聚类图层
map.addLayer({
  id: 'clusters',
  type: 'circle',
  source: 'earthquakes',
  filter: ['has', 'point_count'],
  paint: {
    'circle-color': [
      'step',
      ['get', 'point_count'],
      '#51bbd6',
      100,
      '#f1f075',
      750,
      '#f28cb1'
    ],
    'circle-radius': [
      'step',
      ['get', 'point_count'],
      20,
      100,
      30,
      750,
      40
    ]
  }
});

// 点击聚类展开
map.on('click', 'clusters', (e) => {
  const features = map.queryRenderedFeatures(e.point, {
    layers: ['clusters']
  });
  const clusterId = features[0].properties.cluster_id;
  
  const source = map.getSource('earthquakes');
  source.getClusterExpansionZoom(clusterId, (err, zoom) => {
    if (err) return;
    
    map.easeTo({
      center: features[0].geometry.coordinates,
      zoom: zoom
    });
  });
});
```

## VectorTileSource

矢量瓦片数据源。

### 基础用法

```javascript

// 自定义瓦片服务器
map.addSource('custom-vector', {
  type: 'vector',
  tiles: [
    'https://example.com/tiles/{z}/{x}/{y}.pbf'
  ],
  minzoom: 7,
  maxzoom: 14
});
```

### 配置选项

```javascript
map.addSource('vector-data', {
  type: 'vector',
  
  // 瓦片URL模板
  tiles: ['https://example.com/{z}/{x}/{y}.pbf'],
  
  // 或使用TileJSON URL
  url: 'https://example.com/tilejson.json',
  
  // 最小/最大缩放
  minzoom: 7,
  maxzoom: 14,
  
  // 瓦片尺寸
  tileSize: 512,
  
  // 方案(tms或xyz)
  scheme: 'xyz',
  
  // 边界
  bounds: [-180, -85.051129, 180, 85.051129],
  
  //  attribution
  attribution: '© Data Contributors'
});
```

### 使用矢量图层

```javascript
// 添加矢量数据源
map.addSource('buildings', {
  type: 'vector',
  url: 'https://example.com/tiles/{z}/{x}/{y}.pbf'
});

// 引用矢量图层
map.addLayer({
  id: '3d-buildings',
  source: 'buildings',
  'source-layer': 'building',
  type: 'fill-extrusion',
  minzoom: 15,
  paint: {
    'fill-extrusion-color': '#aaa',
    'fill-extrusion-height': ['get', 'height'],
    'fill-extrusion-opacity': 0.6
  }
});
```

## RasterTileSource

栅格瓦片数据源(图片瓦片)。

### 基础用法

```javascript

// 自定义瓦片服务器
map.addSource('custom-raster', {
  type: 'raster',
  tiles: [
    'https://example.com/tiles/{z}/{x}/{y}.png'
  ],
  tileSize: 512
});
```

### WMS服务

```javascript
map.addSource('wms-layer', {
  type: 'raster',
  tiles: [
    'https://img.nj.gov/imagerywms/Natural2015?' +
    'bbox={bbox-epsg-3857}' +
    '&format=image/png' +
    '&service=WMS' +
    '&version=1.1.1' +
    '&request=GetMap' +
    '&srs=EPSG:3857' +
    '&transparent=true' +
    '&width=256' +
    '&height=256' +
    '&layers=Natural2015'
  ],
  tileSize: 256
});
```

### 配置选项

```javascript
map.addSource('raster-data', {
  type: 'raster',
  tiles: ['https://example.com/{z}/{x}/{y}.png'],
  
  // 瓦片尺寸
  tileSize: 512,
  
  // 最小/最大缩放
  minzoom: 7,
  maxzoom: 19,
  
  // 边界
  bounds: [-180, -85.051129, 180, 85.051129],
  
  // 方案
  scheme: 'xyz',
  
  //  attribution
  attribution: '© Tile Provider'
});
```

## ImageSource

单张图片数据源。

### 基础用法

```javascript
map.addSource('image-source', {
  type: 'image',
  url: 'https://example.com/map-overlay.png',
  coordinates: [
    [-76.54, 39.18],  // 左上
    [-76.52, 39.18],  // 右上
    [-76.52, 39.17],  // 右下
    [-76.54, 39.17]   // 左下
  ]
});

// 添加图层
map.addLayer({
  id: 'image-layer',
  type: 'raster',
  source: 'image-source',
  paint: {
    'raster-opacity': 0.85
  }
});
```

### 动态更新

```javascript
const source = map.getSource('image-source');

// 更新坐标
source.setCoordinates([
  [-76.543, 39.185],
  [-76.528, 39.183],
  [-76.529, 39.176],
  [-76.545, 39.178]
]);

// 更新图片和坐标
source.updateImage({
  url: 'https://example.com/new-image.png',
  coordinates: [
    [-76.543, 39.185],
    [-76.528, 39.183],
    [-76.529, 39.176],
    [-76.545, 39.178]
  ]
});
```

## VideoSource

视频数据源。

### 基础用法

```javascript
map.addSource('video-source', {
  type: 'video',
  urls: [
    'https://example.com/video.mp4',
    'https://example.com/video.webm'
  ],
  coordinates: [
    [-76.54, 39.18],
    [-76.52, 39.18],
    [-76.52, 39.17],
    [-76.54, 39.17]
  ]
});

map.addLayer({
  id: 'video-layer',
  type: 'raster',
  source: 'video-source'
});
```

### 控制播放

```javascript
const videoSource = map.getSource('video-source');

// 获取视频元素
const video = videoSource.getVideo();

// 播放
video.play();

// 暂停
video.pause();

// 监听事件
video.addEventListener('ended', () => {
  console.log('视频播放结束');
});
```

## CanvasSource

Canvas数据源。

### 基础用法

```javascript
map.addSource('canvas-source', {
  type: 'canvas',
  canvas: 'my-canvas-id', // Canvas元素ID
  animate: true,
  coordinates: [
    [-76.54, 39.18],
    [-76.52, 39.18],
    [-76.52, 39.17],
    [-76.54, 39.17]
  ]
});

map.addLayer({
  id: 'canvas-layer',
  type: 'raster',
  source: 'canvas-source'
});
```

### 动态绘制

```javascript
const canvas = document.getElementById('my-canvas');
const ctx = canvas.getContext('2d');

function drawOnCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // 绘制内容
  ctx.fillStyle = 'rgba(255, 0, 0, 0.5)';
  ctx.fillRect(50, 50, 100, 100);
  
  requestAnimationFrame(drawOnCanvas);
}

drawOnCanvas();

// 控制动画
const source = map.getSource('canvas-source');
source.play();   // 开始动画
source.pause();  // 暂停动画
```

## 数据源管理

### 检查数据源是否存在

```javascript
if (map.getSource('my-source')) {
  console.log('数据源存在');
}
```

### 移除数据源

```javascript
// 先移除依赖该数据源的图层
if (map.getLayer('my-layer')) {
  map.removeLayer('my-layer');
}

// 再移除数据源
map.removeSource('my-source');
```

### 获取数据源信息

```javascript
const source = map.getSource('my-source');

// 获取元数据
source.on('dataloading', () => {
  console.log('正在加载数据');
});

source.on('data', (e) => {
  console.log('数据已加载', e);
});

source.on('error', (e) => {
  console.error('数据加载错误', e.error);
});
```

## 实用示例

### 实时轨迹追踪

```javascript
// 初始化GeoJSON
const trackGeoJson = {
  type: 'FeatureCollection',
  features: [{
    type: 'Feature',
    geometry: {
      type: 'LineString',
      coordinates: []
    }
  }]
};

map.addSource('track', {
  type: 'geojson',
  data: trackGeoJson
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

// 实时更新
function updateTrack(position) {
  const source = map.getSource('track');
  const coords = source.getData().features[0].geometry.coordinates;
  
  coords.push([position.lng, position.lat]);
  
  // 保持最近100个点
  if (coords.length > 100) {
    coords.shift();
  }
  
  source.setData({
    type: 'FeatureCollection',
    features: [{
      type: 'Feature',
      geometry: {
        type: 'LineString',
        coordinates: coords
      }
    }]
  });
}
```

### 热力图数据源

```javascript
map.addSource('heatmap-data', {
  type: 'geojson',
  data: pointData
});

map.addLayer({
  id: 'heatmap',
  type: 'heatmap',
  source: 'heatmap-data',
  paint: {
    'heatmap-weight': ['interpolate', ['linear'], ['get', 'magnitude'], 0, 0, 6, 1],
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

## 注意事项

1. **性能**: 大数据集使用矢量瓦片而非GeoJSON
2. **内存**: 及时移除不需要的数据源
3. **CORS**: 确保外部资源支持跨域访问
4. **缓存**: 瓦片数据会自动缓存,可通过maxTileCacheSize控制
5. **更新频率**: 频繁更新时使用setData而非删除重建
6. **聚类**: 大量点数据时启用聚类提高性能
