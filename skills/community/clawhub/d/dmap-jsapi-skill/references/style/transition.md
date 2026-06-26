

# Transition - 过渡动画

Transition 属性控制样式属性变化的过渡动画效果。

## 配置

### 全局Transition

```javascript
{
  "transition": {
    "duration": 300,
    "delay": 0
  }
}
```

### 属性说明

- **duration**: 过渡持续时间（毫秒），默认300
- **delay**: 过渡延迟时间（毫秒），默认0

## 图层级Transition

### 在Paint属性中使用

```javascript
map.addLayer({
  id: 'buildings',
  type: 'fill',
  source: 'landuse',
  paint: {
    'fill-color': '#cccccc',
    'fill-opacity': 0.7,
    'fill-opacity-transition': {
      duration: 500,
      delay: 100
    }
  }
});
```

### 禁用Transition

```javascript
map.addLayer({
  id: 'roads',
  type: 'line',
  source: 'streets',
  paint: {
    'line-color': '#3b82f6',
    'line-width': 3,
    'line-width-transition': {
      duration: 0  // 立即变化，无动画
    }
  }
});
```

## 动态设置Transition

### 修改全局Transition

```javascript
map.setTransition({
  duration: 1000,  // 1秒
  delay: 200       // 延迟200毫秒
});
```

### 获取当前Transition

```javascript
const transition = map.getTransition();
console.log('Duration:', transition.duration);
console.log('Delay:', transition.delay);
```

## 可过渡的属性

以下paint属性支持transition:

### Fill图层

- `fill-opacity`
- `fill-color`
- `fill-outline-color`
- `fill-translate`
- `fill-pattern`

### Line图层

- `line-opacity`
- `line-color`
- `line-width`
- `line-gap-width`
- `line-offset`
- `line-blur`
- `line-dasharray`
- `line-translate`
- `line-pattern`

### Symbol图层

- `icon-opacity`
- `icon-color`
- `icon-halo-color`
- `icon-halo-width`
- `icon-halo-blur`
- `icon-translate`
- `text-opacity`
- `text-color`
- `text-halo-color`
- `text-halo-width`
- `text-halo-blur`
- `text-translate`

### Circle图层

- `circle-radius`
- `circle-color`
- `circle-blur`
- `circle-opacity`
- `circle-translate`
- `circle-stroke-width`
- `circle-stroke-color`
- `circle-stroke-opacity`

### 其他图层

- `raster-opacity`
- `raster-hue-rotate`
- `raster-brightness-min`
- `raster-brightness-max`
- `raster-saturation`
- `raster-contrast`
- `fill-extrusion-opacity`
- `fill-extrusion-color`
- `fill-extrusion-height`
- `fill-extrusion-base`

## 实用示例

### 平滑颜色过渡

```javascript
// 设置较长的过渡时间
map.setTransition({
  duration: 2000,
  delay: 0
});

// 改变颜色会平滑过渡
map.setPaintProperty('buildings', 'fill-color', '#ff0000');
```

### 快速响应交互

```javascript
// 悬停时快速高亮
map.on('mouseenter', 'buildings', () => {
  map.setTransition({ duration: 100 });
  map.setPaintProperty('buildings', 'fill-color', '#ffff00');
});

// 离开时缓慢恢复
map.on('mouseleave', 'buildings', () => {
  map.setTransition({ duration: 500 });
  map.setPaintProperty('buildings', 'fill-color', '#cccccc');
});
```

### 渐进式显示

```javascript
// 添加延迟实现渐进效果
map.addLayer({
  id: 'layer1',
  type: 'fill',
  source: 'data1',
  paint: {
    'fill-opacity': 0,
    'fill-opacity-transition': {
      duration: 1000,
      delay: 0
    }
  }
});

map.addLayer({
  id: 'layer2',
  type: 'fill',
  source: 'data2',
  paint: {
    'fill-opacity': 0,
    'fill-opacity-transition': {
      duration: 1000,
      delay: 500  // 延迟500ms
    }
  }
});

// 同时触发，但layer2会延迟显示
map.setPaintProperty('layer1', 'fill-opacity', 1);
map.setPaintProperty('layer2', 'fill-opacity', 1);
```

### 淡入淡出效果

```javascript
function fadeIn(layerId, duration = 1000) {
  map.setTransition({ duration });
  map.setPaintProperty(layerId, 'fill-opacity', 1);
}

function fadeOut(layerId, duration = 1000) {
  map.setTransition({ duration });
  map.setPaintProperty(layerId, 'fill-opacity', 0);
}

// 使用
fadeIn('my-layer', 1500);
setTimeout(() => fadeOut('my-layer', 1500), 3000);
```

## 性能优化

### 禁用不必要的Transition

```javascript
// 对于频繁更新的属性，禁用transition
map.addLayer({
  id: 'realtime-data',
  type: 'circle',
  source: 'live-data',
  paint: {
    'circle-radius': 5,
    'circle-radius-transition': {
      duration: 0  // 禁用过渡
    },
    'circle-color': '#3b82f6',
    'circle-color-transition': {
      duration: 0  // 禁用过渡
    }
  }
});
```

### 批量更新

```javascript
// 先设置transition
map.setTransition({ duration: 500 });

// 批量更新多个属性
map.setPaintProperty('layer1', 'fill-color', '#ff0000');
map.setPaintProperty('layer1', 'fill-opacity', 0.8);
map.setPaintProperty('layer2', 'line-color', '#00ff00');
map.setPaintProperty('layer2', 'line-width', 5);
```

## 注意事项

1. **性能**: 过多的transition会影响性能
2. **时长选择**: 根据场景选择合适的duration
3. **用户体验**: 避免过长的过渡时间
4. **一致性**: 保持相似的过渡时间
5. **实时数据**: 实时数据应禁用transition
6. **浏览器兼容**: 所有现代浏览器都支持
