---
outline: deep
---
 # BaseFeature


## BaseFeature

**`基础要素类`**<br>

> 注：feature基类，不可直接实例化

### constructor

### featureData

**`元素数据`**

Type: <span>\![GeoJSONFeatureI][1]</span>

### featureId

**`元素ID`**

Type: <span>[string][2]</span>

### getUserData

**`获取用户自定义数据`**

Returns **Record<[string][2], any>**&#x20;

### getOptions

获取属性

Returns **xxFeatureOptions**&#x20;

### addToLayer

**`添加到图层上`**

#### Parameters

*   `layer` **[BaseLayer][3]**&#x20;

Returns **this**&#x20;

### removeFromLayer

**`从图层上移除`**

#### Parameters

*   `layer` **[BaseLayer][3]**&#x20;

Returns **this**&#x20;

### update

**`更新元素`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `options` | 是 | `Partial<O>` | 要素选项的部分属性，其中 `O` 继承自 `CommonFeatureOptT` |
| `immediateRender` | 否 | [boolean][4] | 是否立即渲染，默认值为 `false` |

Returns **this**&#x20;

### isAddedToMap

**`判断是否已经绘制在地图上`**

Returns **[boolean][4]**&#x20;

### scaleWithAnimation

**`以质心点带动画缩放`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `duration` | 是 | [number][5] | 动画持续时间，单位毫秒 |
| `options` | 否 | [Object][6] | 动画属性配置 |
| `options.cubicBezier` | 否 | [Array][7]<[number][5]> | 缓动函数，4个参数：[控制点1x, 控制点1y, 控制点2x, 控制点2y] |
| `options.onFinished` | 否 | [Function][8] | 动画结束回调函数 |
| `options.onProgress` | 否 | [Function][8] | 动画过程回调函数，参数为动画进度(0-1) |

Returns **this**&#x20;

### on

**`监听鼠标/触摸事件`**

#### Parameters

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 是 | [MapLayerEventType][9] | 事件类型 |
| `cb` | 是 | `function (ev: LayerMouseEvent<T>, feature: this): void` | 事件回调函数，接收事件对象和当前要素实例 |

Returns **this**&#x20;

### once

**`监听鼠标/触摸事件，只触发一次`**

#### Parameters

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 是 | [MapLayerEventType][9] | 事件类型 |
| `cb` | 是 | `function (ev: LayerMouseEvent<T>, feature: this): void` | 事件回调函数，接收事件对象和当前要素实例，只触发一次 |

Returns **this**&#x20;

### off

**`取消监听鼠标/触摸事件`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 是 | [MapLayerEventType][9] | 事件类型 |
| `cb` | 否 | `function (ev: LayerMouseEvent<T>): void` | 要取消的事件回调函数 |

Returns **this**&#x20;

[1]: /jsapi/apis/types/Types.html#geojsonfeaturei

[2]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[3]: /jsapi/apis/vector-layer/BaseLayer.html

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[6]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object

[7]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array

[8]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/function

[9]: /jsapi/apis/types/Types.html#maplayereventtype
