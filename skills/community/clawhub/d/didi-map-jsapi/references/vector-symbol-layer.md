---
outline: deep
---
 # SymbolLayer


## SymbolLayer

**`符号图层类`**<br>

> 继承[BaseLayer][1]

### Examples

```javascript
const symbolLayer = new DiMap.SymbolLayer()
symbolLayer.addFeature(new DiMap.SymbolFeature({...}))
symbolLayer.addToMap(map)
symbolLayer.on("click", () => {
 console.log("click")
})
```

### constructor

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `opts` | 否 | [SymbolLayerOptions][2] | 符号图层配置选项 |
| `sourceId` | 否 | [string][3] | 数据源ID |

## SymbolLayerOptions

**`符号图层配置项`**

### Properties
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `layout` | 否 | [SymbolLayout][4] | 符号图层布局配置项 |
| `paint` | 否 | [SymbolPaint][5] | 符号图层样式配置项 |
| `minzoom` | 否 | [number][6] | 符号图层最小缩放级别 |
| `maxzoom` | 否 | [number][6] | 符号图层最大缩放级别 |

[1]: /jsapi/apis/vector-layer/BaseLayer.html

[2]: #symbollayeroptions

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[4]: /jsapi/apis/types/Types.html#symbollayout

[5]: /jsapi/apis/types/Types.html#symbolpaint

[6]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number
