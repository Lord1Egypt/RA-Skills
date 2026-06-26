---
outline: deep
---
 # Rectangle


## Rectangle

**`构造矩形对象，通过RectangleOptions指定多边形样式`**<br>

> 继承[Polygon][1]

### Examples

```javascript
const rectangle = new DiMap.Rectangle({
 map: map,
 bounds: new LngLatBounds([116.397428, 39.90923], [116.417428, 39.93923]),
 strokeColor: '#FF0000',
 strokeWeight: 2,
 strokeOpacity: 1,
 fillColor: '#FF0000',
 fillOpacity: 0.5
})
rectangle.show()
```

### constructor

#### Parameters

*   `options` **[RectangleOptions][2]** 矩形选项

### setBounds

**`设置矩形范围`**

#### Parameters

*   `bounds` **[LngLatBounds][3]** 矩形范围

Returns **this**&#x20;

### getCenter

**`获取矩形中心点`**

Returns **[LngLatLike][4]** 矩形中心点

## RectangleOptions

**`矩形选项`**

### Properties
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `map` | 是 | [Map][5] | 地图实例 |
| `bounds` | 是 | [LngLatBounds][3] | 矩形的范围 |
| `zIndex` | 否 | [number][6] | 矩形覆盖物的叠加顺序 |
| `strokeColor` | 否 | [string][7] | 线条颜色，默认值为#00D3FC |
| `strokeOpacity` | 否 | [number][6] | 轮廓线透明度，取值范围[0,1]，默认为0.9 |
| `strokeWeight` | 否 | [number][6] | 轮廓线宽度 |
| `fillColor` | 否 | [string][7] | 填充颜色 |
| `fillOpacity` | 否 | [number][6] | 填充透明度，取值范围[0,1]，默认为0.5 |
| `height` | 否 | [number][6] | 设置polygon是否离地绘制，默认值为0（需配合extrusionHeight一起使用，且只能≤extrusionHeight） |
| `extrusionHeight` | 否 | [number][6] | 设置是否拉伸为的立面体高度值，默认值为0 |
| `strokeStyle` | 否 | `"solid" \| "dashed"` | 轮廓线样式，实线（solid）或虚线(dashed) |
| `strokeDasharray` | 否 | [Array][8]<[number][6]> | 虚线样式，仅在strokeStyle为dashed时有效（IE9+）。取值示例：[0,0,0]实线、[10,10]虚线、[10,2,10]点画线|
| `userData` | 否 | Record<[string][7], any> | 用户自定义数据对象 |

[1]: /jsapi/apis/overlay/Polygon.html

[2]: #rectangleoptions

[3]: /jsapi/apis/coordinate/LngLatBounds.html

[4]: /jsapi/apis/types/Types.html#lnglatlike

[5]: /jsapi/apis/map/Map.html

[6]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[7]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[8]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array
