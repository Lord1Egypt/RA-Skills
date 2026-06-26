---
outline: deep
---
 # PolygonLayer


## PolygonLayer

**`多边形图层类`**<br>

> 继承[BaseLayer][1]

### Examples

```javascript
const polygonLayer = new DiMap.PolygonLayer()
polygonLayer.addFeature(new DiMap.PolygonFeature({...}))
polygonLayer.addToMap(map)
polygonLayer.on("click", () => {
 console.log("click")
})
```

### constructor

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `opts` | 否 | [PolygonLayerOptions][2] | 多边形图层配置选项 |
| `sourceId` | 否 | [string][3] | 数据源ID |

## PolygonLayerOptions

**`多边形图层配置项`**

### Properties
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `layout` | 否 | [FillLayout][4] | 多边形图层布局 |
| `paint` | 否 | [FillPaint][5] | 多边形图层样式 |
| `minzoom` | 否 | [number][6] | 多边形图层最小缩放级别 |
| `maxzoom` | 否 | [number][6] | 多边形图层最大缩放级别 |

[1]: /jsapi/apis/vector-layer/BaseLayer.html

[2]: #polygonlayeroptions

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[4]: /jsapi/apis/types/Types.html#filllayout

[5]: /jsapi/apis/types/Types.html#fillpaint

[6]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number
