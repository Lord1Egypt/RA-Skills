

# Sources - 数据源

数据源定义地图上要显示的地理数据。

## GeoJSONSource

GeoJSON格式数据源。

### 配置选项

- `type: 'geojson'` - 类型
- `data` - GeoJSON数据或URL
- `maxzoom` - 最大缩放
- `buffer` - 瓦片缓冲
- `tolerance` - 容差
- `cluster` - 启用聚类
- `clusterMaxZoom` - 聚类最大缩放
- `clusterRadius` - 聚类半径
- `lineMetrics` - 行度量
- `generateId` - 生成ID
- `promoteId` - 提升ID

### 实例方法

- `setData(data)` - 更新数据
- `updateData(data)` - 增量更新
- `getClusterExpansionZoom(clusterId, callback)` - 获取聚类展开缩放
- `getClusterChildren(clusterId, callback)` - 获取聚类子要素
- `getClusterLeaves(clusterId, limit, offset, callback)` - 获取聚类叶子节点

详见 [数据源文档](../sources.md)

## VectorTileSource

矢量瓦片数据源。

### 配置选项

- `type: 'vector'` - 类型
- `url` - TileJSON URL
- `tiles` - 瓦片URL模板
- `minzoom` - 最小缩放
- `maxzoom` - 最大缩放
- `tileSize` - 瓦片尺寸
- `scheme` - 方案(xyz/tms)
- `bounds` - 边界
- `attribution` - 版权信息

### 实例方法

- `reload()` - 重新加载瓦片
- `setTiles(tiles)` - 设置瓦片URL数组
- `setUrl(url)` - 设置TileJSON URL

详见 [数据源文档](../sources.md)

## RasterTileSource

栅格瓦片数据源。

### 配置选项

- `type: 'raster'` - 类型
- `url` - TileJSON URL
- `tiles` - 瓦片URL模板
- `minzoom` - 最小缩放
- `maxzoom` - 最大缩放
- `tileSize` - 瓦片尺寸(256/512)
- `scheme` - 方案
- `bounds` - 边界
- `attribution` - 版权信息

### 实例方法

- `reload()` - 重新加载瓦片
- `setTiles(tiles)` - 设置瓦片URL数组
- `setUrl(url)` - 设置TileJSON URL

详见 [数据源文档](../sources.md)

## RasterArrayTileSource

栅格数组瓦片数据源(Mapbox Tiling Service创建)。

### 配置选项

- `type: 'raster-array'` - 类型
- `url` - TileJSON URL
- `tileSize` - 瓦片尺寸

### 实例方法

- `reload()` - 重新加载瓦片
- `setTiles(tiles)` - 设置瓦片URL数组
- `setUrl(url)` - 设置TileJSON URL

详见 [数据源文档](../sources.md)

## ImageSource

单张图片数据源。

### 配置选项

- `type: 'image'` - 类型
- `url` - 图片URL
- `coordinates` - 四角坐标 [[左上], [右上], [右下], [左下]]

### 实例方法

- `updateImage(options)` - 更新图片和坐标
- `setCoordinates(coordinates)` - 更新坐标

详见 [数据源文档](../sources.md)

## VideoSource

视频数据源。

### 配置选项

- `type: 'video'` - 类型
- `urls` - 视频URL数组
- `coordinates` - 四角坐标

### 实例方法

- `getVideo()` - 获取视频元素
- `play()` - 播放
- `pause()` - 暂停
- `setCoordinates(coordinates)` - 更新坐标

详见 [数据源文档](../sources.md)

## CanvasSource

Canvas数据源。

### 配置选项

- `type: 'canvas'` - 类型
- `canvas` - Canvas元素或ID
- `animate` - 是否动画
- `coordinates` - 四角坐标

### 实例方法

- `play()` - 开始动画
- `pause()` - 暂停动画
- `getCanvas()` - 获取Canvas元素
- `setCoordinates(coordinates)` - 更新坐标

详见 [数据源文档](../sources.md)


## 使用示例

```javascript
// GeoJSON源
map.addSource('points', {
  type: 'geojson',
  data: geoJsonData,
  cluster: true
});

// 矢量瓦片源
map.addSource('custom-vector', {
    type: 'vector',
    tiles: [
        'https://example.com/tiles/{z}/{x}/{y}.pbf'
    ],
    minzoom: 7,
    maxzoom: 14
});

// 栅格瓦片源
map.addSource('custom-raster', {
    type: 'raster',
    tiles: [
        'https://example.com/tiles/{z}/{x}/{y}.png'
    ],
    tileSize: 512
});

// 图片源
map.addSource('overlay', {
  type: 'image',
  url: 'image.png',
  coordinates: [
    [-76.54, 39.18],
    [-76.52, 39.18],
    [-76.52, 39.17],
    [-76.54, 39.17]
  ]
});

// 动态更新
const source = map.getSource('points');
source.setData(newData);
```
