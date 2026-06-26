

# Fog - 雾效

Fog 属性定义全局大气雾效，增强深度感和真实感。

## 配置

### 基本配置

```javascript
{
  "fog": {
    "range": [0.5, 10],
    "color": "#ffffff",
    "horizon-blend": 0.1
  }
}
```

### 属性说明

- **range**: 雾的可见范围 `[near, far]`，相对于地平线距离
- **color**: 雾的颜色
- **horizon-blend**: 地平线混合度 (0-1)
- **high-color**: 高空颜色（可选）
- **space-color**: 太空颜色（可选）
- **star-intensity**: 星星强度 (0-1)（可选）

## 动态设置雾效

### 白天雾效

```javascript
map.setFog({
  range: [0.5, 10],
  color: '#ffffff',
  'horizon-blend': 0.1
});
```

### 夜晚雾效

```javascript
map.setFog({
  range: [0.5, 15],
  color: '#000033',
  'high-color': '#000066',
  'horizon-blend': 0.2,
  'star-intensity': 0.6
});
```

### 黄昏雾效

```javascript
map.setFog({
  range: [1, 12],
  color: '#ff9966',
  'high-color': '#ff6633',
  'horizon-blend': 0.15
});
```

## 属性详解

### range - 雾的范围

```javascript
// [近端距离, 远端距离]
// 值越小，雾越浓
map.setFog({
  range: [0.2, 5],  // 浓雾
  color: '#cccccc'
});

map.setFog({
  range: [1, 20],  // 薄雾
  color: '#eeeeee'
});
```

### horizon-blend - 地平线混合

```javascript
// 0 = 无混合，清晰的地平线
// 1 = 完全混合，模糊的地平线
map.setFog({
  range: [0.5, 10],
  color: '#ffffff',
  'horizon-blend': 0.05  // 清晰地平线
});

map.setFog({
  range: [0.5, 10],
  color: '#ffffff',
  'horizon-blend': 0.5  // 模糊的地平线
});
```

### high-color - 高空颜色

```javascript
map.setFog({
  range: [0.5, 10],
  color: '#ffffff',
  'high-color': '#87ceeb',  // 天空蓝
  'horizon-blend': 0.2
});
```

### space-color - 太空颜色

```javascript
map.setFog({
  range: [1, 10],
  color: '#000011',
  'high-color': '#000033',
  'space-color': '#000000',  // 黑色太空
  'star-intensity': 0.8
});
```

### star-intensity - 星星强度

```javascript
// 0 = 无星星
// 1 = 最强星星
map.setFog({
  range: [1, 15],
  color: '#000022',
  'space-color': '#000000',
  'star-intensity': 1.0  // 满天繁星
});
```

## 昼夜循环示例

```javascript
class DayNightFog {
  constructor(map) {
    this.map = map;
    this.time = 0;
    this.duration = 60000; // 1分钟一个周期
  }
  
  start() {
    this.animate();
  }
  
  animate() {
    this.time += 16;
    const progress = (this.time % this.duration) / this.duration;
    const sunAngle = progress * Math.PI * 2;
    const sinValue = Math.sin(sunAngle);
    
    if (sinValue > 0.3) {
      // 白天
      this.map.setFog({
        range: [0.5, 10],
        color: '#ffffff',
        'horizon-blend': 0.1
      });
    } else if (sinValue > -0.3) {
      // 黄昏/黎明
      this.map.setFog({
        range: [0.8, 12],
        color: '#ff9966',
        'high-color': '#ff6633',
        'horizon-blend': 0.15
      });
    } else {
      // 夜晚
      this.map.setFog({
        range: [0.5, 15],
        color: '#000033',
        'high-color': '#000066',
        'space-color': '#000000',
        'star-intensity': 0.7,
        'horizon-blend': 0.2
      });
    }
    
    requestAnimationFrame(() => this.animate());
  }
}

const fogCycle = new DayNightFog(map);
fogCycle.start();
```

## 天气效果

### 雾霾天气

```javascript
map.setFog({
  range: [0.1, 3],
  color: '#dddddd',
  'horizon-blend': 0.4
});
```

### 晴朗天气

```javascript
map.setFog({
  range: [1, 20],
  color: '#f0f8ff',
  'high-color': '#87ceeb',
  'horizon-blend': 0.05
});
```

### 移除雾效

```javascript
map.setFog(null);
```

## 配合地形

```javascript
// 启用地形
map.setTerrain({
  source: 'dmap-dem',
  exaggeration: 1.5
});

// 添加雾效增强深度感
map.setFog({
  range: [0.5, 10],
  color: '#ffffff',
  'horizon-blend': 0.1
});

// 设置观察角度
map.setPitch(60);
map.setZoom(14);
```

## 注意事项

1. **性能**: 雾效会增加渲染开销
2. **范围调整**: 根据缩放级别调整range
3. **颜色选择**: 考虑整体色调协调
4. **星空效果**: 需要深色背景才能看到星星
5. **兼容性**: 旧设备可能不支持
6. **动画**: 避免频繁更新雾效参数
