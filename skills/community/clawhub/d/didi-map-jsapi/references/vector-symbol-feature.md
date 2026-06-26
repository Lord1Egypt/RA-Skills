---
outline: deep
---
 # SymbolFeature


## SymbolFeature

**`符号要素类`**<br>

> 继承[BaseFeature][1]

### Examples

```javascript
const symbolFeature = new DiMap.SymbolFeature({
  geoData: [116.405467, 39.907761],
  symbolTextContent: "北京",
  symbolTextAnchor: "top",
  symbolTextSize: 12,
  symbolTextRadialOffset: 0,
  symbolTextColor: "#000000",
  symbolTextBackgroundColor: "rgba(0,0,0,0)",
  symbolTextOpacity: 1,
  symbolIconImage: "",
  symbolIconImageSize: 1,
  symbolIconImageOffset: [0, 0],
  symbolIconImageRotate: 0,
  symbolIconImageAnchor: "center",
  symbolIconImageColor: "#000000",
  symbolIconImageOpacity: 1,
  symbolZIndex: 1
})
const symbolLayer = new DiMap.SymbolLayer()
symbolFeature.addToLayer(symbolLayer)
symbolLayer.addToMap(map)
```

### constructor

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `opts` | 是 | [SymbolFeatureOptions][2] | 符号要素属性 |
| `userData` | 否 | Record<[string][3], any> | 用户自定义数据，默认值为 `{}` |

## SymbolFeatureOptions

**`符号要素属性`**

### Properties
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `geoData` | 是 | [[number][4], [number][4]] | 空间数据，[经度, 纬度] |
| `symbolTextContent` | 是 | [string][3] | 文字内容 |
| `symbolTextAnchor` | 否 | [Anchor][5] | 文字角标位置 |
| `symbolTextSize` | 否 | [number][4] | 文字大小（pixels） |
| `symbolTextRadialOffset` | 否 | [number][4] | 文本偏移量（pixels），此值作用方向跟随 symbolTextAnchor |
| `symbolTextColor` | 否 | [string][3] | 文本颜色 |
| `symbolTextBackgroundColor` | 否 | [string][3] | 文本背景颜色 |
| `symbolTextOpacity` | 否 | [number][4] | 文本透明度 |
| `symbolIconImage` | 否 | [string][3] | 图标名称或 URL，如果是名称需要预先 addImage，URL 则内部处理 |
| `symbolIconImageSize` | 否 | [number][4] \| [[number][4], [number][4]] | 图标缩放比或 [width, height] |
| `symbolIconImageRotate` | 否 | [number][4] | 图标旋转角度，范围 -360 到 360 |
| `symbolIconImageAnchor` | 否 | [Anchor][5] | 图标角标位置 |
| `symbolIconImageColor` | 否 | [string][3] | 图标颜色，仅当image在addImage(name, img, { sdf: true })时生效 |
| `symbolIconImageOpacity` | 否 | [number][4] | 图标透明度 |
| `symbolZIndex` | 否 | [number][4] | 优先级 |

[1]: /jsapi/apis/vector-layer/BaseFeature.html

[2]: #symbolfeatureoptions

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[5]: /jsapi/apis/types/Types.html#anchor
