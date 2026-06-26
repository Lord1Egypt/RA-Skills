---
outline: deep
---

# MarkerCluster

**`用于需要展示大量 marker 点的场景，将 marker 点按照距离进行聚合，仅展示聚合后的图标和数量，以提高绘制性能。支持用户自定义聚合图标和基础 marker 的样式。`**

## 调用方式

```javascript
new DiMap.MarkerCluster(map: Map, dataOptions: Array, MarkerClusterOptions: Object)
```

## 参数说明

### map
| 类型 | 描述 |
|------|------|
| [Map][1] | 要添加点聚合的地图对象 |

### dataOptions
需要进行聚合显示的点数据

| 属性 | 类型 | 描述 |
|------|------|------|
| lnglat | [Array][3] | 点标记的经纬度信息 |

### MarkerClusterOptions
点聚合属性设置

| 属性 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `gridSize` | [Number][5] | `60` | 最小的聚合距离，点之间的距离小于该值时，点会聚合至一起，以像素为单位 |
| `maxZoom` | [Number][5]  | `18` | 最大的聚合级别，大于该级别就不进行相应的聚合。即小于 18 级的级别均进行聚合，18 及以上级别不进行聚合 |
| `styles` | [Array][3]<[Object][7]> | - | 指定聚合后的点标记的图标样式，可缺省，缺省时为默认样式，自定义样式[style][2] |
| `renderClusterMarker` | [function][4] | - | 实现聚合点的自定义绘制，由开发者自己实现，API 将在绘制每个聚合点的时候调用这个方法，可以实现聚合点样式的灵活设定，指定了 renderClusterMarker 后 styles 无效，[参数][6] |
| `renderMarker` | [function][4] | - | 实现非聚合点的自定义绘制，由开发者自己实现，API 将在绘制每个非聚合点的时候调用这个方法，[参数][9] |

#### styles
数据元素分别对应聚合量在1-10,11-100,101-1000…的聚合点的样式；

当用户设置聚合样式少于实际叠加的点数，未设置部分按照系统默认样式显示。

单个图标样式包括以下属性：

| 属性 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `url` | [string][8] | - | **必选**，图标显示图片的url地址 |
| `size` | [Number][5] | - | **必选**，图标显示图片的大小 |
| `offset` | [Array][3] | `(0,0)` | 可选，图标定位在地图上的位置相对于图标左上角的偏移值 |
| `imageOffset` | [Array][3] | `(0,0)` | 可选，图片相对于可视区域的偏移值，此功能的作用等同CSS中的background-position属性 |
| `textColor` | [string][8] | `"#000000"` | 可选，文字的颜色 |
| `textSize` | [Number][5]  | `10` | 可选，文字的大小 |

#### renderClusterMarker 函数参数
| 参数 | 类型 | 描述 |
|------|------|------|
| `count` | [Number][5]  | 当前聚合点下聚合的 Marker 的数量 |
| `marker` | [Object][7] | 当前聚合点显示的 Marker |

#### renderMarker 函数参数
| 参数 | 类型 | 描述 |
|------|------|------|
| `marker` | [Object][7] | 非聚合点 Marker 对象 |

## 成员函数

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `addData(dataOptions)` | [Array][3] | - | 在原数据基础上添加数据 |
| `setData(dataOptions)` | [Array][3] | - | 设置数据 |
| `getClustersCount()` | - | [Number][5]  | 获取整个聚合图层中，聚合簇的数量 |
| `getGridSize()` | - | [Number][5]  | 获取聚合网格的像素大小 |
| `setGridSize(size)` | [Number][5] | - | 设置聚合网格的像素大小 |
| `getMaxZoom()` | - | [Number][5]  | 获取地图中点标记的最大聚合级别 |
| `setMaxZoom(zoom)` | [Number][5] | - | 设置地图中点标记的最大聚合级别 |
| `setStyles(styles)` | [Array][3] | - | 设置样式聚合点，格式同 opts.styles |
| `getStyles()` | - | `array[style]` | 获取样式 |
| `getMap()` | - | [Map][1] | 获取地图对象 |
| `setMap(map)` | [Map][1] | - | 设置地图对象 |

## 事件

### click 点击事件

#### 返回参数
```javascript
{
    cluster: Object,      // 点击的聚合点图层对象
    clusterData: Object,  // 聚合簇的clusterData数组
    lnglat: LngLat,       // 点击的位置点坐标
    marker: Marker        // 点击的聚合点所包含的 marker 对象
}
```

#### 调用说明
```javascript
cluster.on('click', function (data) {
    console.log(data)
});
```

[1]: /jsapi/apis/map/Map.html
[2]: #styles
[3]: https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array
[4]:https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Functions
[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number
[6]: #renderclustermarker-函数参数
[7]: https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object
[8]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String
[9]: #rendermarker-函数参数
