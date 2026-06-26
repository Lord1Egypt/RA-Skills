

# 图层类型 (Layers)

样式规范定义的图层类型。

## fill - 填充面

用于渲染多边形区域。

### Paint属性

- `fill-antialias` - 抗锯齿
- `fill-opacity` - 透明度
- `fill-color` - 填充颜色
- `fill-outline-color` - 轮廓颜色
- `fill-translate` - 平移
- `fill-translate-anchor` - 平移锚点(map/viewport)
- `fill-pattern` - 填充图案

### 示例

```javascript
{
  id: 'parks',
  type: 'fill',
  source: 'landuse',
  'source-layer': 'park',
  paint: {
    'fill-color': '#4ade80',
    'fill-opacity': 0.5
  }
}
```

## line - 线

用于渲染线状要素。

### Layout属性

- `line-cap` - 端点样式(butt/round/square)
- `line-join` - 连接样式(bevel/round/miter)
- `line-miter-limit` - 斜接限制
- `line-round-limit` - 圆角限制

### Paint属性

- `line-opacity` - 透明度
- `line-color` - 颜色
- `line-translate` - 平移
- `line-translate-anchor` - 平移锚点
- `line-width` - 宽度
- `line-gap-width` - 间隙宽度
- `line-offset` - 偏移
- `line-blur` - 模糊
- `line-dasharray` - 虚线数组
- `line-pattern` - 线图案
- `line-gradient` - 渐变

### 示例

```javascript
{
  id: 'roads',
  type: 'line',
  source: 'streets',
  layout: {
    'line-cap': 'round',
    'line-join': 'round'
  },
  paint: {
    'line-color': '#3b82f6',
    'line-width': 3,
    'line-dasharray': [2, 2]
  }
}
```

## symbol - 符号/文本

用于渲染图标和文本标签。

### Layout属性

- `symbol-placement` - 符号位置(point/line/line-center)
- `symbol-spacing` - 符号间距
- `symbol-avoid-edges` - 避免边缘
- `symbol-z-order` - Z轴顺序(auto/viewport-y/source)
- `icon-image` - 图标图片
- `icon-rotation-alignment` - 图标旋转对齐
- `icon-size` - 图标大小
- `icon-text-fit` - 图标文本适配
- `icon-padding` - 图标内边距
- `icon-keep-upright` - 保持正立
- `icon-offset` - 图标偏移
- `icon-anchor` - 图标锚点
- `icon-pitch-alignment` - 图标俯仰对齐
- `text-field` - 文本字段
- `text-font` - 字体
- `text-size` - 文本大小
- `text-max-width` - 最大宽度
- `text-line-height` - 行高
- `text-letter-spacing` - 字母间距
- `text-justify` - 对齐方式
- `text-anchor` - 文本锚点
- `text-offset` - 文本偏移
- `text-writing-mode` - 书写模式
- `text-rotation-alignment` - 文本旋转对齐

### Paint属性

- `icon-opacity` - 图标透明度
- `icon-color` - 图标颜色
- `icon-halo-color` - 图标光晕颜色
- `icon-halo-width` - 图标光晕宽度
- `icon-halo-blur` - 图标光晕模糊
- `icon-translate` - 图标平移
- `text-opacity` - 文本透明度
- `text-color` - 文本颜色
- `text-halo-color` - 文本光晕颜色
- `text-halo-width` - 文本光晕宽度
- `text-halo-blur` - 文本光晕模糊
- `text-translate` - 文本平移

### 示例

```javascript
// 图标
{
  id: 'icons',
  type: 'symbol',
  source: 'places',
  layout: {
    'icon-image': 'restaurant-15',
    'icon-size': 1
  }
}

// 文本
{
  id: 'labels',
  type: 'symbol',
  source: 'places',
  layout: {
    'text-field': ['get', 'name'],
    'text-font': ['Open Sans Regular'],
    'text-size': 14
  },
  paint: {
    'text-color': '#333',
    'text-halo-color': '#fff',
    'text-halo-width': 2
  }
}
```

## circle - 圆点

用于渲染圆形标记。

### Paint属性

- `circle-radius` - 半径
- `circle-color` - 颜色
- `circle-blur` - 模糊
- `circle-opacity` - 透明度
- `circle-translate` - 平移
- `circle-translate-anchor` - 平移锚点
- `circle-stroke-width` - 描边宽度
- `circle-stroke-color` - 描边颜色
- `circle-stroke-opacity` - 描边透明度

### 示例

```javascript
{
  id: 'points',
  type: 'circle',
  source: 'data',
  paint: {
    'circle-radius': 8,
    'circle-color': '#3b82f6',
    'circle-stroke-width': 2,
    'circle-stroke-color': '#fff'
  }
}
```

## heatmap - 热力图

用于渲染密度热力图。

### Paint属性

- `heatmap-radius` - 半径
- `heatmap-weight` - 权重
- `heatmap-intensity` - 强度
- `heatmap-color` - 颜色
- `heatmap-opacity` - 透明度

### 示例

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
      6, 1
    ],
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
    ],
    'heatmap-radius': 20,
    'heatmap-opacity': 0.8
  }
}
```

## fill-extrusion - 3D挤出

用于渲染3D建筑物等。

### Paint属性

- `fill-extrusion-opacity` - 透明度
- `fill-extrusion-color` - 颜色
- `fill-extrusion-translate` - 平移
- `fill-extrusion-translate-anchor` - 平移锚点
- `fill-extrusion-pattern` - 图案
- `fill-extrusion-height` - 高度
- `fill-extrusion-base` - 基础高度
- `fill-extrusion-vertical-gradient` - 垂直渐变

### 示例

```javascript
{
  id: '3d-buildings',
  type: 'fill-extrusion',
  source: 'buildings',
  'source-layer': 'building',
  minzoom: 15,
  paint: {
    'fill-extrusion-color': '#aaa',
    'fill-extrusion-height': ['get', 'height'],
    'fill-extrusion-base': ['get', 'min_height'],
    'fill-extrusion-opacity': 0.6
  }
}
```

## raster - 栅格

用于渲染栅格瓦片。

### Paint属性

- `raster-opacity` - 透明度
- `raster-hue-rotate` - 色相旋转
- `raster-brightness-min` - 最小亮度
- `raster-brightness-max` - 最大亮度
- `raster-saturation` - 饱和度
- `raster-contrast` - 对比度
- `raster-resampling` - 重采样(linear/nearest)
- `raster-fade-duration` - 淡入时长

### 示例

```javascript
{
  id: 'satellite',
  type: 'raster',
  source: 'satellite-source',
  paint: {
    'raster-opacity': 0.8
  }
}
```

## hillshade - 山体阴影

用于渲染地形阴影。

### Paint属性

- `hillshade-illumination-direction` - 光照方向
- `hillshade-illumination-anchor` - 光照锚点
- `hillshade-exaggeration` - 夸张程度
- `hillshade-shadow-color` - 阴影颜色
- `hillshade-highlight-color` - 高亮颜色
- `hillshade-accent-color` - 强调颜色

### 示例

```javascript
{
  id: 'hillshade',
  type: 'hillshade',
  source: 'terrain',
  paint: {
    'hillshade-exaggeration': 0.5
  }
}
```

## background - 背景

用于渲染地图背景。

### Paint属性

- `background-color` - 颜色
- `background-pattern` - 图案
- `background-opacity` - 透明度

### 示例

```javascript
{
  id: 'background',
  type: 'background',
  paint: {
    'background-color': '#f0f0f0'
  }
}
```


## 注意事项

1. **图层顺序**: 后添加的图层在上层
2. **性能**: 简化表达式,减少复杂计算
3. **可见性**: 使用 visibility 控制显示/隐藏
4. **缩放级别**: 使用 minzoom/maxzoom 优化性能
5. **数据驱动**: 利用表达式实现动态样式
