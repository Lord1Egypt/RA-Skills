

# Light - 光照

Light 属性定义全局光源，影响fill-extrusion等3D图层的照明效果。

## 配置

### 基本配置

```javascript
{
  "light": {
    "anchor": "viewport",
    "position": [1, 90, 80],
    "intensity": 0.5,
    "color": "#ffffff"
  }
}
```

### 属性说明

- **anchor**: 光源锚点 (`viewport` 或 `map`)
  - `viewport`: 光源位置相对于视口固定
  - `map`: 光源位置随地图旋转
- **position**: 光源位置 `[x, y, z]`
  - `x`: 东西方向（经度方向）
  - `y`: 南北方向（纬度方向）
  - `z`: 高度（仰角）
- **intensity**: 光照强度 (0-1)
- **color**: 光照颜色

## 动态设置光照

### 基础光照

```javascript
map.setLight({
  anchor: 'viewport',
  position: [1, 90, 80],
  intensity: 0.5,
  color: '#ffffff'
});
```

### 强光照

```javascript
map.setLight({
  anchor: 'viewport',
  position: [1, 90, 80],
  intensity: 1.0,
  color: '#ffffff'
});
```

### 柔和光照

```javascript
map.setLight({
  anchor: 'viewport',
  position: [1, 90, 60],
  intensity: 0.3,
  color: '#ffeecc'
});
```

## 位置参数详解

### Position数组

```javascript
// [方位角, 仰角, 高度]
position: [
  1,    // 方位角（逆时针从北开始）
  90,   // 仰角（0-90度）
  80    // 高度
]
```

### 不同时间段的光照

#### 早晨

```javascript
map.setLight({
  anchor: 'map',
  position: [120, 45, 50],  // 东南方向
  intensity: 0.6,
  color: '#ffeedd'  // 暖色
});
```

#### 中午

```javascript
map.setLight({
  anchor: 'map',
  position: [180, 80, 100],  // 正上方
  intensity: 1.0,
  color: '#ffffff'  // 白光
});
```

#### 傍晚

```javascript
map.setLight({
  anchor: 'map',
  position: [240, 30, 50],  // 西南方向
  intensity: 0.5,
  color: '#ffddaa'  // 金黄色
});
```

## Anchor模式对比

### Viewport模式

```javascript
// 光源位置相对于屏幕固定
map.setLight({
  anchor: 'viewport',
  position: [1, 90, 80],
  intensity: 0.5
});

// 旋转地图时，光照方向不变
map.setBearing(45);
```

### Map模式

```javascript
// 光源位置相对于地图固定
map.setLight({
  anchor: 'map',
  position: [180, 80, 100],
  intensity: 0.5
});

// 旋转地图时，光照方向随之改变
map.setBearing(45);
```

## 日照动画

### 模拟太阳运动

```javascript
class SunLight {
  constructor(map) {
    this.map = map;
    this.time = 0;
    this.duration = 60000; // 1分钟一圈
  }
  
  start() {
    this.animate();
  }
  
  animate() {
    this.time += 16;
    const progress = (this.time % this.duration) / this.duration;
    
    // 计算太阳位置
    const azimuth = progress * 360;  // 方位角 0-360度
    const altitude = Math.max(10, Math.sin(progress * Math.PI) * 80);  // 仰角
    
    // 计算颜色（早晨/傍晚偏暖，中午偏白）
    const warmth = Math.sin(progress * Math.PI);
    const color = `rgb(255, ${200 + warmth * 55}, ${150 + warmth * 105})`;
    
    // 计算强度
    const intensity = 0.3 + warmth * 0.7;
    
    this.map.setLight({
      anchor: 'map',
      position: [azimuth, altitude, 100],
      intensity: intensity,
      color: color
    });
    
    requestAnimationFrame(() => this.animate());
  }
}

const sun = new SunLight(map);
sun.start();
```

## 配合3D建筑物

```javascript
// 添加3D建筑物
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
    'fill-extrusion-opacity': 0.8
  }
});

// 设置光照
map.setLight({
  anchor: 'viewport',
  position: [1, 60, 70],
  intensity: 0.7,
  color: '#ffffff'
});
```

## 特殊效果

### 月光效果

```javascript
map.setLight({
  anchor: 'viewport',
  position: [1, 45, 50],
  intensity: 0.2,
  color: '#ccccff'  // 冷蓝色
});
```

### 霓虹灯效果

```javascript
map.setLight({
  anchor: 'viewport',
  position: [1, 90, 80],
  intensity: 0.8,
  color: '#ff00ff'  // 紫色
});
```

### 戏剧性光照

```javascript
map.setLight({
  anchor: 'map',
  position: [45, 30, 50],  // 低角度
  intensity: 1.0,
  color: '#ff6600'  // 橙色
});
```

## 注意事项

1. **3D图层**: 光照主要影响fill-extrusion图层
2. **性能**: 动态光照会影响性能
3. **Anchor选择**: 根据需求选择viewport或map
4. **颜色搭配**: 光照颜色与建筑物颜色协调
5. **强度控制**: 过强的光照会过曝
6. **动画频率**: 避免过快更新光照
