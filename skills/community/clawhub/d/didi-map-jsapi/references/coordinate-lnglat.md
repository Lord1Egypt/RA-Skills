---
outline: deep
---
 # LngLat


## LngLat

**`表示经纬度坐标。`**

### Examples

```javascript
const lngLat = new DiMap.LngLat(116.397428, 39.90923)
```

### convert

**`将指定经纬度对象或坐标数组转换为经纬度对象。`**

#### Parameters

*   `input` **[LngLatLike][1]** 要转换的经纬度对象或坐标数组。

Returns **[LngLat][2]** 转换后的经纬度对象。

### lng

**`经度值，取值范围为 -180 至 180 度。`**

Type: <span>[number][3]</span>

### lat

**`纬度值，取值范围为 -90 至 90 度。`**

Type: <span>[number][3]</span>

### constructor

**`创建一个新的经纬度对象。`**

#### Parameters

*   `lng` **[number][3]** 经度值，取值范围为 -180 至 180 度。
*   `lat` **[number][3]** 纬度值，取值范围为 -90 至 90 度。

### wrap

**`将经度值限制在 -180 至 180 度之间，并返回一个新的经纬度对象。`**

Returns **[LngLat][2]** 新的经纬度对象。

### toArray

**`将经纬度对象转换为数组，数组中的第一个元素为经度值，第二个元素为纬度值。`**

Returns **[Array][4]<[number][3]>** 数组形式的经纬度值。

### toString

**`返回经纬度对象的字符串表示形式，格式为 "经度,纬度"。`**

Returns **[string][5]** 经纬度字符串。

### distanceTo

**`返回当前经纬度对象与指定经纬度对象之间的距离，单位为米。`**

#### Parameters

*   `lngLat` **[LngLat][2]** 要计算距离的经纬度对象。

Returns **[number][3]** 距离，单位为米。

### toBounds

**`返回一个包含当前经纬度对象和指定半径的正方形区域的边界矩形。`**

#### Parameters

*   `radius` **[number][3]** 正方形区域的半径，单位为米。

Returns **[LngLatBounds][6]** 正方形区域的边界矩形。

[1]: /jsapi/apis/types/Types.html#lnglatlike

[2]: #lnglat

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[6]: /jsapi/apis/coordinate/LngLatBounds.html
