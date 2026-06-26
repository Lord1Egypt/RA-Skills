---
outline: deep
---
 # HeatmapLayer


## HeatmapLayer

**`热力图层类`**<br>

> 继承[BaseLayer][1]

### Examples

```javascript
const heatmapLayer = new DiMap.HeatmapLayer({
 max: 100,
 radius: 25,
 opacity: 0.7
})
heatmapLayer.addFeature(new DiMap.HeatmapFeature({...}))
heatmapLayer.addToMap(map)
heatmapLayer.on("click", () => {
 console.log("click")
})
```

### constructor

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `opts` | 否 | [HeatmapLayerOptions][2] | 热力图图层配置选项 |
| `sourceId` | 否 | [string][3] | 数据源ID |

## HeatmapLayerOptions

**`热力图图层配置项`**

### Properties
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `layout` | 否 | [HeatmapLayout][4] | 热力图图层布局 |
| `paint` | 否 | [HeatmapPaint][5] | 热力图图层样式 |
| `minzoom` | 否 | [number][6] | 热力图层最小缩放层级 |
| `maxzoom` | 否 | [number][6] | 热力图层最大缩放层级 |
| `max` | 否 | [number][6] | 热力值权重最大值，默认自动计算 |
| `radius` | 否 | [number][6] | 热力图半径，单位像素，默认30 |
| `opacity` | 否 | [number][6] | 热力图透明度，范围0-1，默认0.8 |

[1]: /jsapi/apis/vector-layer/BaseLayer.html

[2]: #heatmaplayeroptions

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[4]: /jsapi/apis/types/Types.html#heatmaplayout

[5]: /jsapi/apis/types/Types.html#heatmappaint

[6]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number
