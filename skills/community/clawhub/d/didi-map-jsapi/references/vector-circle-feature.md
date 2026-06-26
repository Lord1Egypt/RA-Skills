---
outline: deep
---
 # CircleFeature


## CircleFeature

**`圆要素类`** <br>

> 继承[BaseFeature][1]

### Examples

```javascript
const circleFeature = new DiMap.CircleFeature({
  geoData: [116.405467, 39.907761],
  circleRadius: 5,
  circleRadiusUnits: "meters",
  circleColor: "#f60",
  circleOpacity: 1,
  circleStrokeColor: "#fff",
  circleStrokeWidth: 1,
  circleStrokeOpacity: 1,
  circleBlur: 0,
  circleZIndex: 1
})
const circleLayer = new DiMap.CircleLayer()
circleFeature.addToLayer(circleLayer)
circleLayer.addToMap(map)
```

### constructor

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `opts` | 是 | [CircleFeatureOptions][2] | 圆要素属性 |
| `userData` | 否 | Record<[string][3], any> | 用户自定义数据，默认值为 `{}` |

## CircleFeatureOptions

**`圆要素属性`**

### Properties
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `geoData` | 是 | [[number][4], [number][4]] | 空间数据，[经度, 纬度] |
| `circleRadius` | 是 | [number][4] | 半径 |
| `circleRadiusUnits` | 否 | `"meters"` | 半径单位 |
| `circleColor` | 否 | [string][3] | 填充颜色 |
| `circleOpacity` | 否 | [number][4] | 透明度 |
| `circleStrokeColor` | 否 | [string][3] | 边框颜色 |
| `circleStrokeWidth` | 否 | [number][4] | 边框宽度(pixels) |
| `circleStrokeOpacity` | 否 | [number][4] | 边框透明度 |
| `circleBlur` | 否 | [number][4] | 模糊度 |
| `circleZIndex` | 否 | [number][4] | 优先级 |

[1]: /jsapi/apis/vector-layer/BaseFeature.html

[2]: #circlefeatureoptions

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number
