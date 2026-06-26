---
outline: deep
---
 # PolygonFeature


## PolygonFeature

**`多边形要素类`**<br>

> 继承[BaseFeature][1]

### Examples

```javascript
const polygonFeature = new DiMap.PolygonFeature({
  geoData: [
    [
      [116.405467, 39.907761],
      [116.415467, 39.917761],
      [116.425467, 39.927761],
      [116.435467, 39.937761]
    ]
  ],
  fillColor: "#f60",
  fillOpacity: 1,
  fillOutlineColor: "#000",
  fillZIndex: 1
})
const polygonLayer = new DiMap.PolygonLayer()
polygonFeature.addToLayer(polygonLayer)
polygonLayer.addToMap(map)
```

### constructor

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `opts` | 是 | [PolygonFeatureOptions][2] | 多边形要素属性 |
| `userData` | 否 | Record<[string][3], any> | 用户自定义数据，默认值为 `{}` |

## PolygonFeatureOptions

**`多边形要素属性`**

### Properties
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `fillColor` | 否 | [string][3] | 多边形填充颜色 |
| `fillOpacity` | 否 | [number][4] | 多边形填充透明度 |
| `fillOutlineColor` | 否 | [string][3] | 多边形边框颜色 |
| `fillZIndex` | 否 | [number][4] | 优先级 |

[1]: /jsapi/apis/vector-layer/BaseFeature.html

[2]: #polygonfeatureoptions

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number
