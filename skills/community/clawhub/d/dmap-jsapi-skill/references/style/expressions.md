

# 表达式 (Expressions)

表达式用于动态计算样式属性值,支持数据驱动样式。

## 表达式类型

### 查找类

#### get - 获取属性值

```javascript
// 获取属性
'circle-color': ['get', 'color']

// 嵌套属性
'text-field': ['get', 'name.en']
```

#### has - 检查属性是否存在

```javascript
'circle-color': [
  'case',
  ['has', 'color'],
  ['get', 'color'],
  '#3b82f6'  // 默认值
]
```

#### in - 检查值是否在数组/字符串中

```javascript
'circle-color': [
  'case',
  ['in', ['get', 'type'], 'city', 'town'],
  '#ff0000',
  '#00ff00'
]
```

### 条件类

#### case - 条件判断

```javascript
'circle-color': [
  'case',
  ['>', ['get', 'population'], 1000000], '#ff0000',  // 如果人口>100万
  ['>', ['get', 'population'], 500000], '#ffff00',   // 如果人口>50万
  '#00ff00'  // 默认值
]
```

#### match - 匹配

```javascript
'circle-color': [
  'match',
  ['get', 'type'],
  'city', '#ff0000',
  'town', '#ffff00',
  'village', '#00ff00',
  '#999999'  // 默认值
]
```

#### coalesce - 返回第一个非null值

```javascript
'text-field': ['coalesce', ['get', 'name_en'], ['get', 'name']]
```


#### within - 检查要素是否在几何范围内

返回 true 如果要素完全包含在输入几何的边界内,否则返回 false。
输入值可以是有效的 GeoJSON,类型为 Polygon、MultiPolygon、Feature 或 FeatureCollection。

**支持的要素类型:**
- **Point**: 如果点在边界上或边界外,返回 false
- **LineString**: 如果线的任何部分在边界外、线与边界相交、或线的端点在边界上,返回 false

```javascript
// 定义一个多边形边界
const boundary = {
  type: 'Polygon',
  coordinates: [[
    [800000, 600000],
    [810000, 600000],
    [810000, 610000],
    [800000, 610000],
    [800000, 600000]
  ]]
};

// 在过滤器中使用
'filter': ['within', boundary]

// 只在指定区域内的要素显示
map.addLayer({
  id: 'points-in-area',
  type: 'circle',
  source: 'points',
  filter: ['within', boundary],
  paint: {
    'circle-radius': 5,
    'circle-color': '#3b82f6'
  }
});
```

**使用 Feature:**

```javascript
const feature = {
  type: 'Feature',
  geometry: {
    type: 'Polygon',
    coordinates: [[
      [800000, 600000],
      [810000, 600000],
      [810000, 610000],
      [800000, 610000],
      [800000, 600000]
    ]]
  }
};

'filter': ['within', feature]
```

**动态更新范围:**

```javascript
// 更新过滤器的范围
function updateWithinFilter(newBoundary) {
  map.setFilter('points-in-area', ['within', newBoundary]);
}
```


### 数学运算类

#### interpolate - 插值

```javascript
// 线性插值
'circle-radius': [
  'interpolate',
  ['linear'],
  ['zoom'],
  5, 5,    // zoom=5时半径=5
  10, 10,  // zoom=10时半径=10
  15, 20   // zoom=15时半径=20
]

// 指数插值
'line-width': [
  'interpolate',
  ['exponential', 1.5],
  ['zoom'],
  5, 1,
  10, 2,
  15, 5
]
```

#### step - 阶梯函数

```javascript
'circle-radius': [
  'step',
  ['get', 'population'],
  5,           // 默认值
  100000, 10,  // population >= 100000 时半径=10
  1000000, 20  // population >= 1000000 时半径=20
]
```

#### +, -, *, /, % - 算术运算

```javascript
'circle-radius': ['+', ['get', 'base_radius'], 2]
'line-opacity': ['/', ['get', 'value'], 100]
'area-ratio': ['%', ['get', 'area'], 100]
```

#### ^, sqrt, abs, floor, ceil, round - 数学函数

```javascript
'circle-radius': ['sqrt', ['get', 'area']]
'text-size': ['floor', ['get', 'size']]
'rounded-value': ['round', ['get', 'value']]
```

#### min, max - 最小最大值

```javascript
'circle-radius': ['min', ['get', 'radius'], 20]  // 最大20
'line-width': ['max', ['get', 'width'], 1]       // 最小1
```

#### clamp - 限制范围

```javascript
// 将值限制在[min, max]范围内
'circle-opacity': ['clamp', ['get', 'opacity'], 0.2, 0.8]
```

### 逻辑运算类

#### all, any, ! - 逻辑与或非

```javascript
// AND
['all', 
  ['==', ['get', 'type'], 'city'],
  ['>', ['get', 'population'], 1000000]
]

// OR
['any',
  ['==', ['get', 'type'], 'city'],
  ['==', ['get', 'type'], 'town']
]

// NOT
['!', ['has', 'hidden']]
```

#### ==, !=, >, >=, <, <= - 比较运算

```javascript
'circle-color': [
  'case',
  ['>=', ['get', 'rating'], 4], '#00ff00',
  ['>=', ['get', 'rating'], 3], '#ffff00',
  '#ff0000'
]
```

### 字符串类

#### concat - 拼接

```javascript
'text-field': ['concat', ['get', 'name'], ' (', ['get', 'type'], ')']
```

#### format - 格式化文本

用于在 symbol 层的 text-field 中创建富文本格式。

```javascript
'text-field': [
  'format',
  ['get', 'name'], { 'font-scale': 1.2, 'text-font': ['Open Sans Bold'] },
  '\n', {},
  ['get', 'population'], { 'font-scale': 0.8, 'text-color': '#666' }
]
```

**format 选项:**
- `font-scale`: 字体缩放比例
- `text-font`: 字体数组
- `text-color`: 文本颜色
- `font-stretch`: 字体拉伸
- `font-weight`: 字体粗细

#### downcase, upcase - 大小写转换

```javascript
'text-field': ['upcase', ['get', 'name']]
```

#### length - 长度

```javascript
'label-density': ['length', ['get', 'name']]
```

#### substring - 子字符串

```javascript
'text-field': ['substring', ['get', 'code'], 0, 3]
```

#### match - 正则匹配

```javascript
// 检查字符串是否匹配正则表达式
'filter': ['match', ['get', 'name'], '^[A-Z].*', true, false]

// 提取匹配部分
['match', ['get', 'phone'], '(\d{3})-(\d{3})-(\d{4})', '$1$2$3', 'invalid']
```


### 颜色类

#### rgb, rgba - RGB颜色

```javascript
'circle-color': ['rgb', 255, 0, 0]
'fill-opacity': ['rgba', 255, 0, 0, 0.5]
```

#### to-rgba - 转换为RGBA数组

```javascript
['to-rgba', ['get', 'color']]
// 返回 [r, g, b, a] 数组
```

#### hsl, hsla - HSL颜色

```javascript
'circle-color': ['hsl', 120, 100, 50]  // 绿色
'fill-color': ['hsla', 240, 100, 50, 0.5]  // 半透明蓝色
```

### 类型转换类

#### to-string, to-number, to-boolean, to-color

```javascript
'text-field': ['to-string', ['get', 'id']]
'circle-radius': ['to-number', ['get', 'radius'], 5]
```

#### literal - 字面量数组

```javascript
// 当需要传递数组字面量时使用
'filter': ['in', 1, ['literal', [1, 2, 3]]]

// 不需要literal的情况(子表达式返回的数组)
'filter': ['in', 1, ['get', 'myArrayProp']]
```

#### collator - 排序规则

```javascript
// 不区分大小写排序
['sort-key', ['collator', {'case-sensitive': false}], ['get', 'name']]

// 区分重音符号
['sort-key', ['collator', {'diacritic-sensitive': true}], ['get', 'name']]
```

### 数组类

#### array, at, slice, index-of, in

```javascript
// 创建数组
['array', 1, 2, 3]

// 获取元素
['at', 0, ['get', 'colors']]

// 切片
['slice', ['get', 'tags'], 0, 3]

// 索引
['index-of', 'red', ['get', 'colors']]
```

#### length - 数组长度

```javascript
'text-field': ['concat', '共有', ['length', ['get', 'tags']], '个标签']
```

#### concat (数组) - 数组合并

```javascript
// 合并多个数组
['concat', ['get', 'tags1'], ['get', 'tags2']]
```

### 特性状态

#### feature-state - 获取要素状态

```javascript
'fill-color': [
  'case',
  ['boolean', ['feature-state', 'hover'], false],
  '#ff0000',
  '#3b82f6'
]
```

### 缩放级别

#### zoom - 当前缩放级别

```javascript
'line-width': [
  'interpolate',
  ['linear'],
  ['zoom'],
  5, 1,
  10, 2,
  15, 5
]
```

### 几何信息

#### geometry-type - 几何类型

```javascript
'symbol-placement': [
  'match',
  ['geometry-type'],
  'Point', 'point',
  'LineString', 'line',
  'point'
]
```

#### properties - 要素属性

```javascript
['properties']  // 返回整个properties对象
```

### 变量绑定

#### let - 定义变量

```javascript
'circle-radius': [
  'let',
  'base-size', ['get', 'size'],
  'scale-factor', 2,
  ['*', ['var', 'base-size'], ['var', 'scale-factor']]
]
```

#### var - 引用变量

```javascript
// 必须与let配合使用
['var', 'variable-name']
```

### 累积类(用于聚类)

#### accumulated - 获取累积值

```javascript
// 在聚类中使用
'circle-radius': [
  'case',
  ['has', 'point_count'],
  ['interpolate', ['linear'], ['get', 'point_count'],
    1, 10,
    10, 20,
    100, 30
  ],
  5
]
```

### 热力图专用

#### heatmap-density - 热力图密度

```javascript
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
]
```

### 距离相关

#### distance-from-center - 距中心距离

```javascript
// 仅在symbol层的filter中支持
'filter': ['<', ['distance-from-center'], 1000]
```

### Pitch相关

#### pitch - 当前俯仰角

```javascript
// 仅在symbol层的filter中支持
'filter': ['>', ['pitch'], 45]
```

## 实用示例

### 数据驱动颜色

```javascript
{
  id: 'cities',
  type: 'circle',
  source: 'places',
  paint: {
    'circle-color': [
      'match',
      ['get', 'type'],
      'capital', '#ff0000',
      'city', '#00ff00',
      'town', '#0000ff',
      '#999999'
    ]
  }
}
```

### 缩放驱动样式

```javascript
{
  id: 'roads',
  type: 'line',
  source: 'streets',
  paint: {
    'line-width': [
      'interpolate',
      ['exponential', 1.5],
      ['zoom'],
      5, 0.5,
      10, 2,
      15, 6,
      20, 12
    ],
    'line-color': [
      'interpolate',
      ['linear'],
      ['zoom'],
      10, '#cccccc',
      15, '#666666'
    ]
  }
}
```

### 复合表达式

```javascript
{
  id: 'labels',
  type: 'symbol',
  source: 'places',
  paint: {
    'text-color': [
      'case',
      ['all',
        ['==', ['get', 'type'], 'city'],
        ['>', ['get', 'population'], 1000000]
      ],
      '#ff0000',
      
      ['any',
        ['==', ['get', 'type'], 'town'],
        ['==', ['get', 'type'], 'village']
      ],
      '#00ff00',
      
      '#333333'
    ]
  }
}
```

### 热力图权重

```javascript
{
  id: 'heatmap',
  type: 'heatmap',
  source: 'earthquakes',
  paint: {
    'heatmap-weight': [
      'interpolate',
      ['linear'],
      ['get', 'magnitude'],
      0, 0,
      4, 0.5,
      6, 1
    ]
  }
}
```

### 文本格式化

```javascript
{
  id: 'labels',
  type: 'symbol',
  source: 'places',
  layout: {
    'text-field': [
      'format',
      ['get', 'name'], { 'font-scale': 1.2 },
      '\n', {},
      ['get', 'population'], { 'font-scale': 0.8 }
    ]
  }
}
```

## 注意事项

1. **性能**: 避免过于复杂的嵌套表达式
2. **可读性**: 使用注释和格式化提高可读性
3. **类型安全**: 确保表达式返回正确的类型
4. **默认值**: 提供合理的默认值
5. **测试**: 在不同缩放级别和数据下测试表达式
