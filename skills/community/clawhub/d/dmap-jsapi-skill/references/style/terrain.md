

# Terrain - 地形

Terrain 属性定义全局地形高程数据源。

## 配置

### 基本配置

```javascript
{
  "terrain": {
    "source": "dmap-dem",
    "exaggeration": 1.5
  }
}
```

### 属性说明

- **source** (必需): DEM数据源ID
- **exaggeration** (可选): 地形夸张倍数，默认1.0

## 添加DEM数据源


### 自定义DEM数据

```javascript
map.addSource('custom-dem', {
  type: 'raster-dem',
  tiles: [
    'https://example.com/terrain/{z}/{x}/{y}.png'
  ],
  tileSize: 256,
  encoding: 'terrarium',  // 或 'dmap'
  minzoom: 7,
  maxzoom: 12
});

map.setTerrain({
  source: 'custom-dem',
  exaggeration: 2.0
});
```

## DEM编码格式

### Mapbox编码

- RGB值编码高程
- 公式: `height = -10000 + ((R * 256 * 256 + G * 256 + B) * 0.1)`
- 范围: -10000米到15000米

### Terrarium编码

- PNG格式
- 公式: `height = (R * 256 + G + B / 256) - 32768`
- 范围: -32768米到32767米

## 动态控制地形

### 调整夸张度

```javascript
// 增加地形起伏
map.setTerrain({
  source: 'dmap-dem',
  exaggeration: 2.5
});

// 减少地形起伏
map.setTerrain({
  source: 'dmap-dem',
  exaggeration: 0.5
});

// 移除地形
map.setTerrain(null);
```

### 动画效果

```javascript
let exaggeration = 0;
const targetExaggeration = 2.0;

function animateTerrain() {
  exaggeration += 0.1;
  
  if (exaggeration <= targetExaggeration) {
    map.setTerrain({
      source: 'dmap-dem',
      exaggeration: exaggeration
    });
    
    requestAnimationFrame(animateTerrain);
  }
}

animateTerrain();
```

## 配合3D图层

### 3D建筑物

```javascript
map.addLayer({
  id: '3d-buildings',
  type: 'fill-extrusion',
  source: 'composite',
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

### 天空雾层

```javascript
map.setFog({
  'range': [1, 5],
  'horizon-blend': 0.1,
  'color': 'white',
  'high-color': '#30ccff',
  'space-color': '#ade0fa',
  'star-intensity': 0.0
});
```

## 视角设置

```javascript
// 设置3D视角
map.setPitch(60);
map.setBearing(-20);
map.setZoom(16);
map.setCenter([800000, 600000]);
```

## 注意事项

1. **性能**: 地形渲染需要GPU支持
2. **数据大小**: DEM瓦片较大，注意带宽
3. **缩放级别**: 高缩放级别效果更好
4. **兼容性**: 检查WebGL支持
5. **夸张度**: 过高的夸张度可能失真
6. **内存**: 地形数据占用较多显存
