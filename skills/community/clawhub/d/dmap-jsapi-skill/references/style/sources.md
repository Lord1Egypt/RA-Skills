

# 数据源类型 (Sources)

样式规范定义的数据源类型。

## vector - 矢量瓦片

矢量格式的马赛克瓦片数据。

### 配置属性

```javascript
{
  "type": "vector",
  
  // 瓦片URL模板
  "tiles": [
    "https://example.com/{z}/{x}/{y}.pbf"
  ],
  
  // 最小缩放级别
  "minzoom": 0,
  
  // 最大缩放级别
  "maxzoom": 14,
  
  // 瓦片尺寸(512或256)
  "tileSize": 512,
  
  // 方案(xyz或tms)
  "scheme": "xyz",
  
  // 地理边界
  "bounds": [-180, -85.051129, 180, 85.051129],
  
  // 版权信息
  "attribution": "© DmapGL"
}
```

## raster - 栅格瓦片

图片格式的瓦片数据。

### 配置属性

```javascript
{
  "type": "raster",
  
  // 瓦片URL模板
  "tiles": [
    "https://example.com/{z}/{x}/{y}.png"
  ],
  
  // 瓦片尺寸(256或512)
  "tileSize": 256,
  
  // 最小/最大缩放
  "minzoom": 0,
  "maxzoom": 22,
  
  // 方案
  "scheme": "xyz",
  
  // 边界
  "bounds": [-180, -85.051129, 180, 85.051129],
  
  // 版权
  "attribution": "© Satellite Provider"
}
```

### WMS服务示例

```javascript
{
  "type": "raster",
  "tiles": [
    "https://img.nj.gov/imagerywms/Natural2015?" +
    "bbox={bbox-epsg-3857}" +
    "&format=image/png" +
    "&service=WMS" +
    "&version=1.1.1" +
    "&request=GetMap" +
    "&srs=EPSG:3857" +
    "&transparent=true" +
    "&width=256" +
    "&height=256" +
    "&layers=Natural2015"
  ],
  "tileSize": 256
}
```

## raster-dem - 栅格DEM

用于地形渲染的高程数据。

### 配置属性

```javascript
{
  "type": "raster-dem",
  
  // 瓦片URL
  "tiles": [
    "https://example.com/terrain/{z}/{x}/{y}.png"
  ],
  
  // 瓦片尺寸(通常512)
  "tileSize": 512,
  
  // 编码方式(mapbox或terrarium)
  "encoding": "terrarium",
  
  // 最小/最大缩放
  "minzoom": 0,
  "maxzoom": 14
}
```

## geojson - GeoJSON数据

GeoJSON格式的矢量数据。

### 配置属性

```javascript
{
  "type": "geojson",
  
  // GeoJSON数据或URL
  "data": {
    "type": "FeatureCollection",
    "features": []
  },
  
  // 或URL
  // "data": "https://example.com/data.geojson",
  
  // 最大缩放
  "maxzoom": 14,
  
  // 瓦片缓冲
  "buffer": 128,
  
  // 容差(简化几何)
  "tolerance": 0.375,
  
  // 启用聚类
  "cluster": false,
  "clusterMaxZoom": 14,
  "clusterRadius": 50,
  
  // 行度量(用于lineMetrics)
  "lineMetrics": false,
  
  // 生成ID
  "generateId": false,
  
  // 促进ID
  "promoteId": null
}
```

### 聚类配置

```javascript
{
  "type": "geojson",
  "data": pointData,
  "cluster": true,
  "clusterMaxZoom": 14,
  "clusterRadius": 50,
  "clusterProperties": {
    "sum": ["+", ["get", "value"]],
    "max": ["max", ["get", "value"]]
  }
}
```

## image - 单张图片

单张地理参考图片。

### 配置属性

```javascript
{
  "type": "image",
  
  // 图片URL
  "url": "https://example.com/overlay.png",
  
  // 四角坐标 [[左上], [右上], [右下], [左下]]
  "coordinates": [
    [-76.54, 39.18],  // 左上
    [-76.52, 39.18],  // 右上
    [-76.52, 39.17],  // 右下
    [-76.54, 39.17]   // 左下
  ]
}
```

## video - 视频

地理参考视频。

### 配置属性

```javascript
{
  "type": "video",
  
  // 视频URL数组(多种格式)
  "urls": [
    "https://example.com/video.mp4",
    "https://example.com/video.webm"
  ],
  
  // 四角坐标
  "coordinates": [
    [-76.54, 39.18],
    [-76.52, 39.18],
    [-76.52, 39.17],
    [-76.54, 39.17]
  ]
}
```

## canvas - Canvas

HTML Canvas元素作为数据源。

### 配置属性

```javascript
{
  "type": "canvas",
  
  // Canvas元素ID或引用
  "canvas": "my-canvas-id",
  
  // 是否动画
  "animate": true,
  
  // 四角坐标
  "coordinates": [
    [-76.54, 39.18],
    [-76.52, 39.18],
    [-76.52, 39.17],
    [-76.54, 39.17]
  ]
}
```

## 使用示例

### 添加多个数据源

```javascript
// 矢量瓦片
map.addSource('custom-vector', {
    type: 'vector',
    tiles: [
        'https://example.com/tiles/{z}/{x}/{y}.pbf'
    ],
    minzoom: 7,
    maxzoom: 14
});

// 栅格瓦片
map.addSource('custom-raster', {
    type: 'raster',
    tiles: [
        'https://example.com/tiles/{z}/{x}/{y}.png'
    ],
    tileSize: 512
});


// GeoJSON
map.addSource('points', {
  type: 'geojson',
  data: geoJsonData,
  cluster: true
});

// DEM地形
map.addSource('terrain', {
  type: 'raster-dem',
  tiles: [
     dmapgl.serviceUrl + '/map/img?year=&type=DEM&z={z}&x={x}&y={y}'
  ],
  tileSize: 512
});

// 图片叠加
map.addSource('overlay', {
  type: 'image',
  url: 'overlay.png',
  coordinates: [
    [-76.54, 39.18],
    [-76.52, 39.18],
    [-76.52, 39.17],
    [-76.54, 39.17]
  ]
});
```

### 动态更新数据源

```javascript
// 更新GeoJSON
const source = map.getSource('points');
source.setData(newGeoJsonData);

// 更新栅格瓦片URL
const raster = map.getSource('satellite');
raster.setTiles(['https://new-tiles.example.com/{z}/{x}/{y}.png']);

// 更新图片
const image = map.getSource('overlay');
image.updateImage({
  url: 'new-image.png',
  coordinates: [...]
});
```

## 注意事项

1. **CORS**: 外部资源需要支持跨域访问
2. **性能**: 大数据集使用矢量瓦片而非GeoJSON
3. **缓存**: 瓦片会自动缓存
4. **TileJSON**: 优先使用TileJSON简化配置
5. ** attribution**: 始终提供正确的版权信息
6. **瓦片尺寸**: 选择合适的tileSize(256或512)
