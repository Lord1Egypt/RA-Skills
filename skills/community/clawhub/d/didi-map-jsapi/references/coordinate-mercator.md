---
outline: deep
---
 # MercatorCoordinate


## MercatorCoordinate

**`此类表示基于 WebMercator 投影的坐标。`**

### Examples

```javascript
const mercatorCoordinate = new DiMap.MercatorCoordinate(0.5, 0.5)
```

### x

**`x 坐标值`**

Type: <span>[number][1]</span>

### y

**`y 坐标值`**

Type: <span>[number][1]</span>

### z

**`z 坐标值`**

Type: <span>([number][1] | [undefined][2])?</span>

### fromLngLat

**`根据经纬度坐标和海拔高度创建MercatorCoordinate对象的新实例。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `lngLatLike` | 是 | [LngLatLike][3] | 经纬度坐标 |
| `altitude` | 否 | [number][1] | 海拔高度 |

Returns **[MercatorCoordinate][4]** 新实例

### constructor

**`创建新实例。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `x` | 是 | [number][1] | x 坐标值 |
| `y` | 是 | [number][1] | y 坐标值 |
| `z` | 否 | [number][1] | z 坐标值 |

### toAltitude

**`获取当前 WebMercator 投影坐标的海拔高度（单位：米）。`**

Returns **[number][1]** 海拔高度

### toLngLat

**`将当前 WebMercator 投影坐标转换为经纬度坐标。`**

Returns **[LngLat][5]** 经纬度坐标

### meterInMercatorCoordinateUnits

**`获取当前 WebMercator 投影坐标每米对应的坐标值。`**

Returns **[number][1]** 每米对应的坐标值

[1]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[2]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/undefined

[3]: /jsapi/apis/types/Types.html#lnglatlike

[4]: #mercatorcoordinate

[5]: /jsapi/apis/coordinate/LngLat.html
