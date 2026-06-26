---
outline: deep
---

# Circle

## Circle

**`构造圆形覆盖物（需在地图加载完成后），通过CircleOptions设置圆形`**<br>

> 继承[OverlayBase][1]

### Examples

```javascript
const circle = new DiMap.Circle({
  map: map,
  center: [116.405467, 39.907761],
  radius: 1000,
  strokeColor: "#006600",
  strokeOpacity: 1,
  strokeWeight: 2,
  fillColor: "#006600",
  fillOpacity: 1,
  userData: {},
});
circle.show();
```

### constructor

#### Parameters

- `options` **[CircleOptions][2]** 圆形选项

### setCenter

**`设置中心点`**

#### Parameters

- `center` **[LngLatLike][3]** 中心点

Returns **this**&#x20;

### getCenter

**`获取中心点`**

Returns **[LngLatLike][3]** 中心点

### getBounds

**`获取圆形代表的矩形范围`**

Returns **[LngLatBounds][4]** 矩形范围

### setRadius

**`设置半径`**

#### Parameters

- `radius` **[number][5]** 半径

Returns **this**&#x20;

### getRadius

**`获取半径`**

Returns **[number][5]** 半径

### contains

**`判断点是否在圆内`**

#### Parameters

- `point` **[LngLatLike][3]** 点

Returns **[boolean][6]** 是否在圆内

## CircleOptions

**`圆形属性`**

### Properties

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `map` | 是 | [Map][7] | 地图实例 |
| `center` | 是 | [LngLatLike][3] | 中心点 |
| `radius` | 是 | [number][5] | 半径 |
| `strokeColor` | 否 | [string][8] | 边框颜色 |
| `strokeOpacity` | 否 |[number][5]| 边框透明度 |
| `strokeWeight` | 否 | [number][5] | 边框宽度 |
| `fillColor` | 否 | [string][8] | 填充颜色 |
| `fillOpacity` | 否 | [number][5] | 填充透明度 |
| `userData` | 否 | Record<[string][8], any> | 用户自定义数据对象 |

[1]: /jsapi/apis/overlay/OverlayBase.html
[2]: #circleoptions
[3]: /jsapi/apis/types/Types.html#lnglatlike
[4]: /jsapi/apis/coordinate/LngLatBounds.html
[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number
[6]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean
[7]: /jsapi/apis/map/Map.html
[8]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String
