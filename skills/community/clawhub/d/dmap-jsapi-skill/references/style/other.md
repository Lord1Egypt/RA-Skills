

# Other - 其他样式属性

其他未在专门章节中描述的样式属性和概念。

## Functions - 函数

属性值可以是函数，根据缩放级别或数据属性动态计算。

### Zoom Functions（已废弃，使用表达式）

旧版语法（不推荐）:

```javascript
// 已废弃，使用interpolate表达式替代
'line-width': {
  "base": 1.5,
  "stops": [
    [5, 1],
    [10, 2],
    [15, 5]
  ]
}
```

新版语法（推荐）:

```javascript
'line-width': [
  'interpolate',
  ['exponential', 1.5],
  ['zoom'],
  5, 1,
  10, 2,
  15, 5
]
```

## Data-driven Styling - 数据驱动样式

基于要素属性动态设置样式。

### 基础示例

```javascript
'circle-color': ['get', 'color']
'circle-radius': ['get', 'size']
```

### 条件样式

```javascript
'fill-color': [
  'case',
  ['==', ['get', 'type'], 'residential'], '#ff0000',
  ['==', ['get', 'type'], 'commercial'], '#00ff00',
  '#0000ff'  // 默认值
]
```

详见 [Expressions](expressions.md)

## Filters - 过滤器

过滤要显示的要素。

### 基础过滤

```javascript
// 只显示特定类型
'filter': ['==', 'type', 'city']

// 数值比较
'filter': ['>', 'population', 1000000]
```

### 复合过滤

```javascript
// AND
'filter': [
  'all',
  ['==', 'type', 'city'],
  ['>', 'population', 1000000]
]

// OR
'filter': [
  'any',
  ['==', 'type', 'city'],
  ['==', 'type', 'town']
]

// NOT
'filter': [
  '!',
  ['==', 'type', 'village']
]
```

### 动态更新过滤器

```javascript
// 设置过滤器
map.setFilter('cities', ['>', 'population', 500000]);

// 清除过滤器
map.setFilter('cities', null);
```

## Visibility - 可见性

控制图层的显示/隐藏。

### 设置可见性

```javascript
// 隐藏图层
map.setLayoutProperty('my-layer', 'visibility', 'none');

// 显示图层
map.setLayoutProperty('my-layer', 'visibility', 'visible');
```

### 切换可见性

```javascript
function toggleLayer(layerId) {
  const visibility = map.getLayoutProperty(layerId, 'visibility');
  map.setLayoutProperty(
    layerId,
    'visibility',
    visibility === 'visible' ? 'none' : 'visible'
  );
}
```

## MinZoom / MaxZoom - 缩放范围

控制图层在特定缩放级别范围内显示。

### 配置

```javascript
{
  "id": "detailed-roads",
  "type": "line",
  "source": "streets",
  "minzoom": 12,  // 仅在zoom >= 12时显示
  "maxzoom": 20,  // 仅在zoom < 20时显示
  "paint": {
    "line-color": "#3b82f6"
  }
}
```

### 动态修改

```javascript
// 注意：minzoom/maxzoom不能在运行时修改
// 需要在添加图层时指定
```

## Source Layer - 矢量瓦片图层

指定矢量瓦片中的子图层。

### 配置

```javascript
{
  "id": "buildings",
  "type": "fill",
  "source": "composite",
  "source-layer": "building",  // 矢量瓦片中的图层名
  "paint": {
    "fill-color": "#cccccc"
  }
}
```


## Paint Properties - 绘制属性

控制图层的视觉表现。

### 通用属性

- `*-opacity`: 透明度
- `*-color`: 颜色
- `*-translate`: 平移
- `*-translate-anchor`: 平移锚点

### 过渡属性

每个可动画的paint属性都有对应的transition:

```javascript
'fill-opacity-transition': {
  duration: 300,
  delay: 0
}
```

## Layout Properties - 布局属性

控制图层的布局和渲染方式。

### 通用属性

- `visibility`: 可见性
- 各图层类型特有的布局属性


## 注意事项

1. **向后兼容**: 避免使用已废弃的特性
2. **性能**: 复杂的过滤器影响性能
3. **表达式优先**: 使用表达式替代旧版functions
4. **文档**: 参考各专题文档获取详细信息
5. **验证**: 使用样式验证工具
6. **测试**: 在不同缩放级别测试样式
