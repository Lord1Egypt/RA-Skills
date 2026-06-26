---
outline: deep
---
 # GetGeoLocation


## getGeoLocation

`获取地理位置工具类，用于获取设备的地理坐标信息`
### Parameters

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `parameters` | 否 | [Object][3] | 参数对象 |
| `parameters.options` | 否 | [PositionOptions][1] | 位置选项 |
| `parameters.success` | 否 | [PositionCallback][4] | 成功回调函数 |
| `parameters.error` | 否 | [PositionErrorCallback][5] | 错误回调函数 |
| `parameters.watch` | 否 | [Object][3] | 监听对象 |
| `parameters.watch.options` | 否 | [PositionOptions][1] | 监听的位置选项 |
| `parameters.watch.success` | 否 | `(data: GeolocationCoordinates) => void` | 监听的成功回调函数 |
| `parameters.watch.error` | 否 | [PositionErrorCallback][5] | 监听的错误回调函数 |

##### PositionCallback

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `position` | 是 | `GeolocationPosition` | 位置信息 |

##### PositionErrorCallback

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `positionError` | 是 | `GeolocationPositionError` | 位置错误信息 |



### Examples

```javascript
const loc = await getGeoLocation({
 success: (data) => {},
 error: (err) => {},
})
```

Returns **[Promise][2]<(any | null)>**&#x20;

[1]: /jsapi/apis/types/Types.html#positionoptions

[2]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise

[3]: https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object

[4]:/jsapi/apis/geolocation/GetGeoLocation.html#positioncallback

[5]:/jsapi/apis/geolocation/GetGeoLocation.html#positionerrorcallback