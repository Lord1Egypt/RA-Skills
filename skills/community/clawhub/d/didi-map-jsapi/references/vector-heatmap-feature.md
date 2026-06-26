---
outline: deep
---
 # HeatmapFeature


## HeatmapFeature

**`热力图要素类`** <br>

> 继承[BaseFeature][1]

### Examples

```javascript
const heatmapFeature = new DiMap.HeatmapFeature({
  geoData: [116.405467, 39.907761],
  heatmapValue: 10
})
const heatmapLayer = new DiMap.HeatmapLayer({ max: 100 })
heatmapFeature.addToLayer(heatmapLayer)
heatmapLayer.addToMap(map)
```

### constructor

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `opts` | 是 | [HeatmapFeatureOptions][2] | 热力图要素属性 |
| `userData` | 否 | Record<[string][3], any> | 用户自定义数据，默认值为 `{}` |

## HeatmapFeatureOptions

**`热力图要素属性`**

### Properties
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `geoData` | 是 | [[number][4], [number][4]] | 空间数据，[经度, 纬度] |
| `heatmapValue` | 是 | [number][4] | 热力值 |

[1]: /jsapi/apis/vector-layer/BaseFeature.html

[2]: #heatmapfeatureoptions

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number
