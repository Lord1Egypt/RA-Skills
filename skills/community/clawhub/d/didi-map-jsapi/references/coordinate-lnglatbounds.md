---
outline: deep
---
 # LngLatBounds


## LngLatBounds

**`表示经纬度范围`**

### Examples

```javascript
const bounds = new DiMap.LngLatBounds([
 [116.282852, 39.881762],
 [116.414083, 39.987994]
])
```

### sw

**`矩形区域的西南角坐标。`**

Type: <span>[LngLatLike][1]</span>

### ne

**`矩形区域的东北角坐标。`**

Type: <span>[LngLatLike][1]</span>

### convert

**`将传入的范围转换为 LngLatBounds 对象。`**

#### Parameters

*   `input` **[LngLatBoundsLike][2]** 需要转换的范围对象。

Returns **[LngLatBounds][3]** 转换后的 LngLatBounds 对象。

### constructor

**`创建一个新的 `LngLatBounds` 对象。`**

#### Parameters

*   `boundsLike` **([LngLatLike][1] | \[[LngLatLike][1], [LngLatLike][1]] | \[[number][4], [number][4], [number][4], [number][4]])** **`  要创建的矩形区域的西南角和东北角坐标，或表示它们的数组。`**

### constructor

**`创建一个新的 `LngLatBounds` 对象。`**

#### Parameters

*   `sw` **[LngLatLike][1]** 矩形区域的西南角坐标。
*   `ne` **[LngLatLike][1]** 矩形区域的东北角坐标。

### setNorthEast

**`设置矩形区域的东北角坐标。`**

#### Parameters

*   `ne` **[LngLatLike][1]** 矩形区域的东北角坐标。

Returns **[LngLatBounds][3]** 此对象本身。

### setSouthWest

**`设置矩形区域的西南角坐标。`**

#### Parameters

*   `sw` **[LngLatLike][1]** 矩形区域的西南角坐标。

Returns **[LngLatBounds][3]** 此对象本身。

### contains

**`判断一个经纬度坐标是否在矩形区域内。`**

#### Parameters

*   `lnglat` **[LngLatLike][1]** 要判断的经纬度坐标。

Returns **[boolean][5]** 如果该点在矩形区域内，则为 `true`；否则为 `false`。

### extend

**`将矩形区域扩展以包含指定的经纬度坐标或另一个矩形区域。`**

#### Parameters

*   `obj` **([LngLatLike][1] | [LngLatBoundsLike][2])** 要包含的经纬度坐标或矩形区域。

Returns **[LngLatBounds][3]** 此对象本身。

### getCenter

**`返回当前范围的中心坐标。`**

Returns **[LngLat][6]** 当前范围的中心坐标。

### getSouthWest

**`返回当前范围的西南角坐标。`**

Returns **[LngLat][6]** 当前范围的西南角坐标。

### getNorthEast

**`返回当前范围的东北角坐标。`**

Returns **[LngLat][6]** 当前范围的东北角坐标。

### getNorthWest

**`返回当前范围的西北角坐标。`**

Returns **[LngLat][6]** 当前范围的西北角坐标。

### getSouthEast

**`返回当前范围的东南角坐标。`**

Returns **[LngLat][6]** 当前范围的东南角坐标。

### getWest

**`返回当前范围的最小经度值。`**

Returns **[number][4]** 当前范围的最小经度值。

### getSouth

**`返回当前范围的最小纬度值。`**

Returns **[number][4]** 当前范围的最小纬度值。

### getEast

**`返回当前范围的最大经度值。`**

Returns **[number][4]** 当前范围的最大经度值。

### getNorth

**`返回当前范围的最大纬度值。`**

Returns **[number][4]** 当前范围的最大纬度值。

### toArray

**`将当前范围转换成二维数组。`**

Returns **[Array][7]<[Array][7]<[number][4]>>**&#x20;

### toString

**`将当前范围转换成字符串。`**

Returns **[string][8]** 当前范围的字符串表示。

### isEmpty

**`判断当前范围是否为空。`**

Returns **[boolean][5]** 如果当前范围为空则返回 true，否则返回 false。

[1]: /jsapi/apis/types/Types.html#lnglatlike

[2]: /jsapi/apis/types/Types.html#lnglatboundslike

[3]: #lnglatbounds

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean

[6]: /jsapi/apis/coordinate/LngLat.html

[7]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array

[8]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String
