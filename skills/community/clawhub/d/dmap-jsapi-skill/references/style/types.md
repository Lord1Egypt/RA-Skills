

# Types - 数据类型

样式规范中使用的各种数据类型。

## Color - 颜色

### 颜色格式

```javascript
// CSS颜色名称
'fill-color': 'red'

// 十六进制
'fill-color': '#ff0000'
'fill-color': '#f00'

// RGB
'fill-color': 'rgb(255, 0, 0)'

// RGBA
'fill-color': 'rgba(255, 0, 0, 0.5)'

// HSL
'fill-color': 'hsl(0, 100%, 50%)'

// HSLA
'fill-color': 'hsla(0, 100%, 50%, 0.5)'
```

### 颜色表达式

```javascript
'fill-color': [
  'interpolate',
  ['linear'],
  ['get', 'temperature'],
  0, 'blue',
  20, 'green',
  40, 'yellow',
  60, 'red'
]
```

## PromoteId - ID提升

用于从要素属性中指定唯一标识符。

### 配置

```javascript
{
  "type": "vector",
  "url": dmapgl.serviceUrl + "/map/vector/standard/styles/style.json",
  "promoteId": {
    "building": "building_id"
  }
}
```

### 使用场景

```javascript
// GeoJSON源
map.addSource('buildings', {
  type: 'geojson',
  data: buildingData,
  promoteId: 'id'  // 使用'id'属性作为要素ID
});

// 设置要素状态
map.setFeatureState(
  { source: 'buildings', id: 123 },
  { hover: true }
);
```

## Formatted - 格式化文本

支持富文本格式化的字符串。

### 基本用法

```javascript
'text-field': [
  'format',
  'Bold Text', { 'font-scale': 1.2, 'text-font': ['Open Sans Bold'] },
  '\n', {},
  'Normal Text', { 'font-scale': 1.0 }
]
```

### 带颜色的文本

```javascript
'text-field': [
  'format',
  'Red ', { 'text-color': '#ff0000' },
  'Green ', { 'text-color': '#00ff00' },
  'Blue', { 'text-color': '#0000ff' }
]
```

### 动态格式化

```javascript
'text-field': [
  'format',
  ['get', 'name'], { 'font-scale': 1.2 },
  '\n', {},
  ['get', 'population'], { 
    'font-scale': 0.8,
    'text-color': '#666666'
  }
]
```

## ResolvedImage - 解析图片

用于图标图片的引用。

### 基本用法

```javascript
'icon-image': 'restaurant-15'
```

### 条件图片

```javascript
'icon-image': [
  'match',
  ['get', 'type'],
  'restaurant', 'restaurant-15',
  'cafe', 'cafe-15',
  'hotel', 'hotel-15',
  'default-15'  // 默认值
]
```

### 动态添加图片

```javascript
// 从URL加载
const image = new Image();
image.src = 'custom-icon.png';
image.onload = () => {
  map.addImage('custom-icon', image);
};

// 使用
'icon-image': 'custom-icon'
```

## VariableAnchorOffsetCollection - 可变锚点偏移

定义文本标签的可变锚点和偏移。

### 配置

```javascript
'text-variable-anchor-offset': [
  'top', [0, -10],
  'bottom', [0, 10],
  'left', [-10, 0],
  'right', [10, 0]
]
```

### 使用场景

```javascript
map.addLayer({
  id: 'labels',
  type: 'symbol',
  source: 'places',
  layout: {
    'text-field': ['get', 'name'],
    'text-variable-anchor': ['top', 'bottom', 'left', 'right'],
    'text-radial-offset': 1.5
  }
});
```

## 数值类型

### Number

```javascript
'circle-radius': 10
'fill-opacity': 0.7
'line-width': 3
```

### 数组

```javascript
// 坐标数组
'center': [800000, 600000]

// 边界数组
'bounds': [716638.24, 548483.59, 894455.08, 728066.47]

// 颜色数组（RGBA）
'fill-color': [255, 0, 0, 0.5]
```

## 字符串类型

### String

```javascript
'text-field': 'Hello World'
'icon-image': 'marker-15'
```

### Enum（枚举）

```javascript
// visibility
'visibility': 'visible'  // 或 'none'

// line-cap
'line-cap': 'round'  // 'butt', 'round', 'square'

// line-join
'line-join': 'round'  // 'bevel', 'round', 'miter'

// symbol-placement
'symbol-placement': 'point'  // 'point', 'line', 'line-center'
```

## Boolean类型

```javascript
'circle-antialias': true
'icon-allow-overlap': false
```

## Padding - 内边距

```javascript
// 单一值
'icon-padding': 10

// 数组 [上, 右, 下, 左]
'icon-padding': [10, 20, 10, 20]
```

## Offset - 偏移

```javascript
// [x, y] 偏移
'icon-offset': [10, -20]
'text-offset': [0, -1.5]
```

## Anchor - 锚点

```javascript
// 单锚点
'icon-anchor': 'center'  // center, left, right, top, bottom等

// 多锚点
'text-variable-anchor': ['top', 'bottom', 'left', 'right']
```

## 注意事项

1. **类型安全**: 确保属性值类型正确
2. **单位**: 注意不同属性的单位（像素、度、米等）
3. **范围**: 某些属性有有效范围限制
4. **兼容性**: 检查浏览器对颜色格式的支持
5. **性能**: 复杂的格式化文本影响渲染性能
