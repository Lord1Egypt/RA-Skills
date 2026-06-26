---
outline: deep
---
 # GeometryUtil

## GeometryUtil

**`地理计算库`**

## distance

**`计算两点之间的地面距离`**

### Parameters

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `p1` | 是 | [LngLatLike][1] \| [LngLat][2] | 点1经纬度对象 |
| `p2` | 是 | [LngLatLike][1] \| [LngLat][2] | 点2经纬度对象 |

Returns **[number][3]** 两点之间的实际地面距离，单位为米

## distanceOfLine

**`计算多个点依次连成的线的总长度`**

### Parameters

*   `points` **([Array][4]<[LngLatLike][1]> | [Array][4]<[LngLat][2]>)** 多个点的经纬度对象数组，支持 LngLatLike 或 LngLat 类型

Returns **[number][3]** 多个点依次连成的线的总长度，单位为米

## ringArea

**`计算多个点连接形成区域的面积`**

### Parameters

*   `points` **([Array][4]<[LngLatLike][1]> | [Array][4]<[LngLat][2]>)** 多个点的经纬度对象数组，支持 LngLatLike 或 LngLat 类型

Returns **[number][3]** 区域面积，单位为平方米（如果首尾坐标不一致，自动闭合）

## isPointInRing

**`判断点是否在面内`**

### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `point` | 是 | [LngLatLike][1] \| [LngLat][2]| 点经纬度对象 |
| `ring` | 是 |[Array][4]<([LngLatLike][1] \| [LngLat][2])> | 多边形边界点数组 |

Returns **[boolean][5]** 点在面内返回 true，否则返回 false（如果首尾坐标不一致，自动闭合）

[1]: /jsapi/apis/types/Types.html#lnglatlike

[2]: /jsapi/apis/coordinate/LngLat.html

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean