---
outline: deep
---
 # OverlayBase


## OverlayEvent

**`覆盖物虚类事件虚类`**<br>

> 不可直接实例化

### on

**`绑定事件`**

#### Parameters

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 是 | [MapLayerEventType][1] | 事件类型 |
| `cb` | 是 | `function (ev: LayerMouseEvent<T>): void` | 事件回调函数 |

Returns **this**&#x20;

### once

**`单次绑定事件`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 是 | [MapLayerEventType][1] | 事件类型 |
| `cb` | 是 | `function (ev: LayerMouseEvent<T>): void` | 事件回调函数 |

Returns **this**&#x20;

### off

**`解绑事件`**

#### Parameters

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 是 | [MapLayerEventType][1] | 事件类型 |
| `cb` | 否 | `function (ev: LayerMouseEvent<T>): void` | 事件回调函数 |

Returns **this**&#x20;

## OverlayBase

**`覆盖物虚类`**<br>

> 继承[OverlayEvent][2]
> 不可直接实例化

### scaleWithAnimation

**`带动画缩放`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `duration` | 是 | [number][3] | 动画持续时间，单位毫秒 |
| `options` | 否 | [Object][4] | 动画属性配置 |
| `options.cubicBezier` | 否 | [Array][5]<[number][3]> | 缓动函数，4个参数，分别为控制点1x, 控制点1y, 控制点2x, 控制点2y |
| `options.onFinished` | 否 | [Function][6] | 动画结束回调 |
| `options.onProgress` | 否 | [Function][6] | 动画过程回调，参数为动画进度，0-1 |

Returns **this**&#x20;

### hide

隐藏覆盖物

Returns **this**&#x20;

### show

显示覆盖物

#### Parameters

*   `beforeId` **[string][7]?**&#x20;

Returns **this**&#x20;

### setMap

设置(新)地图实例，传 null 则从原有地图上移除，同`destroy`方法

#### Parameters

*   `map` **([Map][8] | null)**&#x20;

Returns **any** this

### setOptions

设置覆盖物配置项

#### Parameters

*   `options` **[Object][4]** 覆盖物配置项
*   `immediate`   (optional, default `false`)

Returns **this**&#x20;

### getOptions

获取覆盖物配置项

Returns **this**&#x20;

### setUserData

设置用户自定义数据

#### Parameters

*   `userData` **[Object][4]** 用户自定义数据

Returns **this**&#x20;

### getUserData

获取用户自定义数据

Returns **[Object][4]**&#x20;

### destroy

销毁覆盖物

Returns **this**&#x20;

[1]: /jsapi/apis/types/Types.html#maplayereventtype

[2]: #overlayevent

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array

[6]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/function

[7]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[8]: /jsapi/apis/map/Map.html
