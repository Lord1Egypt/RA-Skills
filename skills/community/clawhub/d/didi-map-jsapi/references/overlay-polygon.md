---
outline: deep
---
 # Polygon


## Polygon

**`构造多边形对象，通过PolygonOptions指定多边形样式以及属性`**<br>

> 继承[OverlayBase][1]

### Examples

```javascript
const polygon = new DiMap.Polygon({
 map: map,
 path: [
   [116.403322, 39.920255],
   [116.410703, 39.897555],
   [116.402292, 39.892353],
   [116.389846, 39.891365],
   [116.375250, 39.904843],
   [116.384765, 39.916092],
   [116.403322, 39.920255]
 ],
 strokeColor: '#FF33FF',
 strokeOpacity: 1,
 strokeWeight: 3,
 fillColor: '#1791fc',
 fillOpacity: 0.4,
 height: 100,
 extrusionHeight: 100,
 strokeStyle: 'solid',
 strokeDasharray: [10, 10],
 userData: {
  name: 'polygon'
 }
})
polygon.show()
polygon.setOptions({
 strokeColor: '#FF33FF',
 strokeOpacity: 1,
 strokeWeight: 3
})
```

### constructor

#### Parameters

*   `options` **[PolygonOptions][2]** 多边形参数

### setPath

**`设置path`**

#### Parameters

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `path` | 是 | [PolygonOptionsPath][3] | 多边形轮廓线的节点坐标数组。支持单个普通多边形[LngLatLike][4]\[]、单个带孔多边形[LngLatLike][4]\[]\[]、多个带孔多边形[LngLatLike][4]\[]\[]\[] |
| `immediate` | 否 | [boolean][5] | 是否立即更新，默认值为 `false` |

Returns **this**&#x20;

### getPath

**`获取path`**

Returns **[PolygonOptionsPath][3]**&#x20;

### getBounds

**`获取多边形矩形范围对象`**

#### Examples

```javascript
const bounds = polygon.getBounds()
map.fitBounds(bounds, {
 padding: 100
})
```

Returns **[LngLatBounds][6]**&#x20;

### setHeight

**`设置多边形离地高度`**

#### Parameters

*   `height` **[number][7]** 多边形离地高度，单位米

Returns **this**&#x20;

### setExtrusionHeight

**`设置立面体高度值`**

#### Parameters

*   `extrusionHeight` **[number][7]** 立面体高度值，单位米

Returns **this**&#x20;

### getExtrusionHeight

**`返回立体面高度值`**

Returns **[number][7]** 立体面高度值

### contains

**`判断坐标是否在多边形内`**

#### Parameters

*   `originPoint` **[LngLatLike][4]**&#x20;

Returns **[boolean][5]** true 包含，false 不包含

### getArea

**`多边形面积`**

Returns **[number][7]**&#x20;

## PolygonOptions

**`多边形属性`**

### Properties
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `map` | 是 | [Map][8] | 地图实例对象 |
| `path` | 是 | [PolygonOptionsPath][3] | 多边形轮廓线的节点坐标数组。支持单个普通多边形[LngLatLike][4]\[]、单个带孔多边形[LngLatLike][4]\[]\[]、多个带孔多边形[LngLatLike][4]\[]\[]\[]  |
| `zIndex` | 否 | [number][7] | 多边形覆盖物的叠加顺序 |
| `strokeColor` | 否 | [string][9] | 线条颜色，默认值为#00D3FC |
| `strokeOpacity` | 否 | [number][7] | 轮廓线透明度，取值范围[0,1]，默认为0.9 |
| `strokeWeight` | 否 | [number][7] | 轮廓线宽度 |
| `fillColor` | 否 | [string][9] | 多边形填充颜色，使用16进制颜色代码赋值，如：#00B2D5 |
| `fillOpacity` | 否 | [number][7] | 多边形填充透明度，取值范围[0,1]，默认为0.5 |
| `height` | 否 | [number][7] | 设置polygon是否离地绘制，默认值为0（需配合extrusionHeight一起使用，且只能≤extrusionHeight） |
| `extrusionHeight` | 否 | [number][7] | 设置多边形是否拉伸为的立面体高度值，默认值为0 |
| `strokeStyle` | 否 | [string][9] | 轮廓线样式，实线:solid，虚线:dashed |
| `strokeDasharray` | 否 | [Array][10]<[number][7]> | 虚线样式，仅在strokeStyle为dashed时有效（IE9+）。取值示例：[0,0,0]实线、[10,10]虚线、[10,2,10]点画线 |
| `userData` | 否 | Record<[string][9], any> | 用户自定义数据对象 |

## PolygonOptionsPath

**`多边形路径参数`**
| 形式 | 类型 | 描述 |
| :--- | :--- | :--- |
| 单个普通多边形 | [Array][10]<[LngLatLike][4]> | 单个普通多边形的路径，由一系列坐标点组成 |
| 单个带孔多边形 | [Array][10]<[Array][10]<[LngLatLike][4]>> | 单个带孔多边形的路径，第一个元素为外多边形，其余为孔多边形 |
| 多个带孔多边形 | [Array][10]<[Array][10]<[Array][10]<[LngLatLike][4]>>> | 多个带孔多边形的路径，每个元素都是一个带孔多边形 |

[1]: /jsapi/apis/overlay/OverlayBase.html

[2]: #polygonoptions

[3]: #polygonoptionspath

[4]: /jsapi/apis/types/Types.html#lnglatlike

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean

[6]: /jsapi/apis/coordinate/LngLatBounds.html

[7]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[8]: /jsapi/apis/map/Map.html

[9]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[10]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array
