---
outline: deep
---
 # PolylineLayer


## PolylineLayer

**`折线图层类`**<br>

> 继承[BaseLayer][1]

### Examples

```javascript
const polylineLayer = new DiMap.PolylineLayer()
polylineLayer.addFeature(new DiMap.PolylineFeature({...}))
polylineLayer.addToMap(map)
polylineLayer.on("click", () => {
 console.log("click")
})
```

### constructor

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `opts` | 否 | [PolylineLayerOptions][2] | 折线图层配置选项 |
| `sourceId` | 否 | [string][3] | 数据源ID |

## PolylineLayerOptions

**`折线图层配置项`**

### Properties
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `layout` | 否 | [LineLayout][4] | 折线图层布局 |
| `paint` | 否 | [LinePaint][5] | 折线图层样式 |
| `minzoom` | 否 | [number][6] | 折线图层最小缩放级别 |
| `maxzoom` | 否 | [number][6] | 折线图层最大缩放级别 |

[1]: /jsapi/apis/vector-layer/BaseLayer.html

[2]: #polylinelayeroptions

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[4]: /jsapi/apis/types/Types.html#linelayout

[5]: /jsapi/apis/types/Types.html#linepaint

[6]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number
