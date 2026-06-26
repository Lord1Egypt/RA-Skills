---
outline: deep
---
 # Polyline


## Polyline

**`构造折线对象，通过PolylineOptions指定折线样式`**<br>

> 继承[OverlayBase][1]

### Examples

```javascript
const polyline = new DiMap.Polyline({
 map: map,
 path: [
  [116.397411, 39.909186],
  [116.410886, 39.909186],
  [116.410886, 39.924397],
  [116.397411, 39.924397]
 ],
 strokeColor: "#FF33FF",
 strokeOpacity: 0.2,
 strokeWeight: 10,
 strokeStyle: "dashed",
 lineJoin: "round",
 lineCap: "round",
 showDir: true,
 userData: {
  id: "polyline1"
 }
})
polyline.show()
```

### constructor

#### Parameters

*   `options` **[PolylineOptions][2]** 折线选项

### setPath

**`设置path`**

#### Parameters

*   `path` **[Array][3]<[LngLatLike][4]>**&#x20;

Returns **this**&#x20;

### getPath

**`获取path`**

Returns **[Array][3]<[LngLatLike][4]>**&#x20;

### getLength

**`获取折线物理长度`**

Returns **[number][5]** 单位：米

### getBounds

**`获取折线的矩形范围对象`**

#### Examples

```javascript
const bounds = polyline.getBounds()
map.fitBounds(bounds, {
 padding: 100
})
```

Returns **[LngLatBounds][6]**&#x20;

## PolylineOptions

**`折线属性`**

### Properties
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `map` | 是 | [Map][7] | 地图实例 |
| `path` | 是 | [Array][3]<[LngLatLike][4]> | 折线路径 |
| `isOutline` | 否 | [boolean][8] | 是否带描边，默认false |
| `borderWeight` | 否 | [number][5] | 描边宽度，默认1 |
| `outlineColor` | 否 | [string][9] | 描边颜色，默认#000000 |
| `strokeColor` | 否 | [string][9] | 线条颜色，默认#006600 |
| `strokeOpacity` | 否 | [number][5] | 线条透明度，默认1 |
| `strokeWeight` | 否 | [number][5] | 线条宽度，默认2，单位像素 |
| `strokeStyle` | 否 | `"solid" \| "dashed"` | 线条样式，实线或虚线 |
| `strokeDasharray` | 否 | [Array][3]<[number][5]> | 自定义虚线样式。实线：[0,0,0]；虚线：[10,10]（默认）；点画线：[10,2,10] |
| `lineJoin` | 否 | `"bevel" \| "round" \| "miter"` | 折线拐点连接处的样式，默认尖角（miter），可选：圆角（round）,斜角（bevel） |
| `lineCap` | 否 | `"round" \| "butt" \| "square"` | 折线两端线帽的样式，默认butt，可选：圆头（round）,方头（square） |
| `userData` | 否 | Record<[string][9], any> | 用户自定义数据对象 |
| `showDir` | 否 | [boolean][8] | 是否显示方向箭头，默认false |

[1]: /jsapi/apis/overlay/OverlayBase.html

[2]: #polylineoptions

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array

[4]: /jsapi/apis/types/Types.html#lnglatlike

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[6]: /jsapi/apis/coordinate/LngLatBounds.html

[7]: /jsapi/apis/map/Map.html

[8]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean

[9]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String
