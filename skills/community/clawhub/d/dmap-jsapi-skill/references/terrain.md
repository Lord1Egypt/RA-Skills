

# 地形和特效 (Terrain & Effects)

DMap GL支持3D地形渲染和大气效果。

## Terrain - 3D地形

启用基于DEM数据的3D地形。

### 配置地形

```javascript
// 添加DEM数据源
map.addSource('terrain-dem', {
  type: 'raster-dem',
  tiles: [
      dmapgl.serviceUrl + '/map/img?year=&type=DEM&z={z}&x={x}&y={y}'
  ],
  tileSize: 512,
  maxzoom: 14
});

// 启用地形
map.setTerrain({
  source: 'terrain-dem',
  exaggeration: 1.5  // 地形夸张程度
});
```

### 地形选项

- `source` - DEM数据源ID
- `exaggeration` - 地形夸张倍数(0-2)

### 移除地形

```javascript
map.setTerrain(null);
```

### 示例:山地可视化

```javascript
map.on('load', () => {
  // 添加地形
  map.addSource('dmap-dem', {
    type: 'raster-dem',
    tiles: [
      dmapgl.serviceUrl + '/map/img?year=&type=DEM&z={z}&x={x}&y={y}'
    ],
  });
  
  map.setTerrain({
    source: 'dmap-dem',
    exaggeration: 1.5
  });
  
  // 添加天空雾增强效果
  map.setFog({
    'range': [1, 5],
    'horizon-blend': 0.1,
    'color': 'white',
    'high-color': '#30ccff',
    'space-color': '#ade0fa',
    'star-intensity': 0.0
  });
  
  // 设置3D视角
  map.setPitch(60);
  map.setBearing(-20);
});
```

## Fog - 雾效

创建大气雾效,增强深度感。

### 配置雾效

```javascript
map.setFog({
  range: [0.5, 10],        // 雾的范围 [near, far]
  color: '#ffffff',         // 雾的颜色
  'horizon-blend': 0.1      // 地平线混合
});
```

### 雾效属性

- `range` - 雾的可见范围 [近端, 远端]
- `color` - 雾的颜色
- `horizon-blend` - 地平线混合度(0-1)
- `high-color` - 高空颜色
- `space-color` - 太空颜色
- `star-intensity` - 星星强度

### 动态雾效

```javascript
// 根据时间改变雾效
function updateFogByTime() {
  const hour = new Date().getHours();
  
  if (hour >= 6 && hour < 18) {
    // 白天
    map.setFog({
      range: [0.5, 10],
      color: '#ffffff',
      'horizon-blend': 0.1
    });
  } else {
    // 夜晚
    map.setFog({
      range: [0.5, 15],
      color: '#000033',
      'high-color': '#000066',
      'horizon-blend': 0.2,
      'star-intensity': 0.6
    });
  }
}

updateFogByTime();
```

### 移除雾效

```javascript
map.setFog(null);
```

## Light - 光照

控制3D图层的光照效果。

### 配置光照

```javascript
map.setLight({
  anchor: 'viewport',  // viewport 或 map
  position: [1, 90, 80], // [x, y, z]
  intensity: 0.5,       // 强度
  color: '#ffffff'      // 颜色
});
```

### 光照属性

- `anchor` - 锚点(viewport/map)
- `position` - 光源位置 [x, y, z]
- `intensity` - 光照强度(0-1)
- `color` - 光照颜色

### 动态光照

```javascript
// 模拟日照变化
function updateSunPosition() {
  const time = Date.now() / 1000;
  
  map.setLight({
    anchor: 'map',
    position: [
      Math.cos(time * 0.0001) * 100,
      Math.sin(time * 0.0001) * 100,
      50
    ],
    intensity: 0.8
  });
  
  requestAnimationFrame(updateSunPosition);
}

updateSunPosition();
```


## 实用示例

### 昼夜循环

```javascript
class DayNightCycle {
  constructor(map) {
    this.map = map;
    this.time = 0;
    this.duration = 60000; // 1分钟一个周期
  }
  
  start() {
    this.animate();
  }
  
  animate() {
    this.time += 16; // ~60fps
    const progress = (this.time % this.duration) / this.duration;
    const angle = progress * Math.PI * 2;
    
    // 更新光照
    this.map.setLight({
      anchor: 'map',
      position: [
        Math.cos(angle) * 100,
        Math.sin(angle) * 100,
        50
      ],
      intensity: Math.max(0.2, Math.sin(angle))
    });
    
    // 更新雾效
    if (Math.sin(angle) > 0.3) {
      // 白天
      this.map.setFog({
        range: [0.5, 10],
        color: '#ffffff',
        'horizon-blend': 0.1
      });
    } else {
      // 夜晚
      this.map.setFog({
        range: [0.5, 15],
        color: '#000033',
        'high-color': '#000066',
        'star-intensity': 0.8
      });
    }
    
    requestAnimationFrame(() => this.animate());
  }
}

const cycle = new DayNightCycle(map);
cycle.start();
```


### 3D地形剖面

```javascript
// 启用3D地形
map.addSource('terrain', {
  type: 'raster-dem',
  tiles: [
     dmapgl.serviceUrl + '/map/img?year=&type=DEM&z={z}&x={x}&y={y}'
  ],
});

map.setTerrain({
  source: 'terrain',
  exaggeration: 2
});

// 添加3D建筑
map.addLayer({
  id: '3d-buildings',
  type: 'fill-extrusion',
  source: 'composite',
  'source-layer': 'building',
  minzoom: 15,
  paint: {
    'fill-extrusion-color': '#aaa',
    'fill-extrusion-height': ['get', 'height'],
    'fill-extrusion-opacity': 0.7
  }
});

// 设置观察角度
map.setPitch(75);
map.setBearing(45);
map.setZoom(16);
```

### 星空效果

```javascript
// 夜晚星空
map.setFog({
  range: [1, 10],
  color: '#000011',
  'high-color': '#000033',
  'space-color': '#000000',
  'star-intensity': 1,
  'horizon-blend': 0.1
});

// 添加光照
map.setLight({
  anchor: 'map',
  position: [0, 0, 50],
  intensity: 0.3,
  color: '#6666ff'
});
```

## 注意事项

1. **性能**: 地形和特效会影响性能,移动端谨慎使用
2. **数据源**: 地形需要DEM数据源
3. **兼容性**: 检查浏览器WebGL支持
4. **缩放级别**: 地形在高缩放级别效果更好
5. **组合效果**: 多个特效可以组合使用
6. **内存**: 特效会占用额外显存
