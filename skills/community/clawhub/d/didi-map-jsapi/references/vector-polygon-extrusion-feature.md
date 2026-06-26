---
outline: deep
---
 # PolygonExtrusionFeature


## PolygonExtrusionFeature

**`多边形立方体要素类`**<br>

> 继承[BaseFeature][1]

### Examples

```javascript
const polygonExtrusionFeature = new DiMap.PolygonExtrusionFeature({
  geoData: [
    [
      [116.405467, 39.907761],
      [116.415467, 39.917761],
      [116.425467, 39.927761],
      [116.435467, 39.937761]
    ]
  ],
  fillExtrusionBase: 0,
  fillExtrusionHeight: 100,
  fillExtrusionColor: "#00B2D5",
  fillExtrusionOpacity: 0.5
})
const polygonExtrusionLayer = new DiMap.PolygonExtrusionLayer()
polygonExtrusionFeature.addToLayer(polygonExtrusionLayer)
polygonExtrusionLayer.addToMap(map)
```

### constructor

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `opts` | 是 | [PolygonExtrusionFeatureOptions][2] | 多边形立方体要素属性 |
| `userData` | 否 | Record<[string][3], any> | 用户自定义数据，默认值为 `{}` |

## PolygonExtrusionFeatureOptions

**`多边形立方体要素属性`**

### Properties
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `fillExtrusionBase` | 否 | [number][4] | 离地高度，单位米 |
| `fillExtrusionHeight` | 否 | [number][4] | 立方体高度，单位米 |
| `fillExtrusionColor` | 否 | [string][3] | 立方体顶部填充颜色 |
| `fillExtrusionOpacity` | 否 | [number][4] | 立方体顶部填充透明度 |

[1]: /jsapi/apis/vector-layer/BaseFeature.html

[2]: #polygonextrusionfeatureoptions

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number
