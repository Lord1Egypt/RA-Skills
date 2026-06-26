---
outline: deep
---
 # PolygonExtrusionLayer


## PolygonExtrusionLayer

**`多边形立体图层类`**<br>

> 继承[BaseLayer][1]

### Examples

```javascript
const polygonExtrusionLayer = new DiMap.PolygonExtrusionLayer()
polygonExtrusionLayer.addFeature(new DiMap.PolygonExtrusionFeature({...}))
polygonExtrusionLayer.addToMap(map)
polygonExtrusionLayer.on("click", () => {
 console.log("click")
})
```

### constructor

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `opts` | 否 | [PolygonExtrusionLayerOptions][2] | 多边形立方体图层配置选项 |
| `sourceId` | 否 | [string][3] | 数据源ID |

## PolygonExtrusionLayerOptions

**`多边形立体图层配置项`**

### Properties
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `layout` | 否 | [FillExtrusionLayout][4] | 多边形立体图层布局 |
| `paint` | 否 | [FillExtrusionPaint][5] | 多边形立体图层样式 |
| `minzoom` | 否 | [number][6] | 多边形立体图层最小缩放层级 |
| `maxzoom` | 否 | [number][6] | 多边形立体图层最大缩放层级 |


[1]: /jsapi/apis/vector-layer/BaseLayer.html

[2]: #polygonextrusionlayeroptions

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[4]: /jsapi/apis/types/Types.html#fillextrusionlayout

[5]: /jsapi/apis/types/Types.html#fillextrusionpaint

[6]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number
