---
outline: deep
---
 # CircleLayer


## CircleLayer

**`圆图层类`**<br>

> 继承[BaseLayer][1]

### Examples

```javascript
const circleLayer = new DiMap.CircleLayer()
circleLayer.addFeature(new DiMap.CircleFeature({...}))
circleLayer.addToMap(map)
circleLayer.on("click", () => {
 console.log("click")
})
```

### constructor

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `opts` | 否 | [CircleLayerOptions][2] | 圆图层配置选项 |
| `sourceId` | 否 | [string][3] | 数据源ID |

## CircleLayerOptions

**`圆图层配置项`**

### Properties
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `layout` | 否 | [CircleLayout][4] | 圆图层布局 |
| `paint` | 否 | [CirclePaint][5] | 圆图层样式 |
| `minzoom` | 否 | [number][6] | 圆图层最小缩放层级 |
| `maxzoom` | 否 | [number][6] | 圆图层最大缩放层级 |

[1]: /jsapi/apis/vector-layer/BaseLayer.html

[2]: #circlelayeroptions

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[4]: /jsapi/apis/types/Types.html#circlelayout

[5]: /jsapi/apis/types/Types.html#circlepaint

[6]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number
