---
outline: deep
---
 # PolylineFeature


## PolylineFeature

**`折线要素类`**<br>

> 继承[BaseFeature][1]

### Examples

```javascript
const polylineFeature = new DiMap.PolylineFeature({
  geoData: [
    [116.405467, 39.907761],
    [116.415467, 39.917761],
    [116.425467, 39.927761],
    [116.435467, 39.937761]
  ],
  lineWidth: 2,
  lineColor: "#000",
  lineOpacity: 1,
  lineJoin: "miter",
  lineBlur: 0,
  lineGapWidth: 0,
  lineOffset: 0
})
const polylineLayer = new DiMap.PolylineLayer()
polylineFeature.addToLayer(polylineLayer)
polylineLayer.addToMap(map)
```

### constructor

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `opts` | 是 | [PolylineFeatureOptions][2] | 折线要素属性 |
| `userData` | 否 | Record<[string][3], any> | 用户自定义数据，默认值为 `{}` |

## PolylineFeatureOptions

**`折线要素属性`**

### Properties
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `geoData` | 是 | [Array][4]<\[[number][5], [number][5]]> | 空间数据，[[经度, 纬度]] |
| `lineWidth` | 是 | [number][5] | 折线宽度 |
| `lineColor` | 否 | [string][3] | 折线颜色 |
| `lineOpacity` | 否 | [number][5] | 折线透明度 |
| `lineBlur` | 否 | [number][5] | 折线模糊度 |
| `lineGapWidth` | 否 | [number][5] | 线套两边相距距离(pixels)，lineWidth表示线套两边宽度 |
| `lineOffset` | 否 | [number][5] | 线偏移量，正值偏右，负值偏左 |


[1]: /jsapi/apis/vector-layer/BaseFeature.html

[2]: #polylinefeatureoptions

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number
