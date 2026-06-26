---
outline: deep
---
 # BaseLayer


## BaseLayer

**`基础图层类`** <br>

> 注：不可直接实例化，需继承后使用

### constructor

**`构造函数`**

#### Parameters

*   `sourceId` **[string][1]?**&#x20;

### addToMap

**`添加图层到地图`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `map` | 是 | [Map][2] | 地图实例 |
| `before` | 否 | [string][1] | 图层插入到某个图层之前，before为图层id |

Returns **this**&#x20;

### removeFromMap

**`从地图上移除图层`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `map` | 否 | [Map][2] | 地图实例 |
| `noSource` | 否 | [boolean][3] | 是否移除source |

Returns **this**&#x20;

### getLayerId

**`获取layer id`**

Returns **[string][1]**&#x20;

### getSourceData

**`获取source data`**

Returns **[GeoJSONSourceRaw][4]**&#x20;

### getSourceId

**`获取source id`**

Returns **[string][1]**&#x20;

### addFeature

**`添加元素到图层，如果元素已存在，则不添加`**

#### Parameters

*   `feature` **[BaseFeature][5]**&#x20;

Returns **this**&#x20;

### addFeatures

**`添加多个元素到图层`**

#### Parameters

*   `features` **[Array][6]<[BaseFeature][5]>**&#x20;

Returns **this**&#x20;

### setFeatures

**`重新添加元素列表到图层，会清空原有元素列表`**

#### Parameters

*   `features` **[Array][6]<[BaseFeature][5]>**&#x20;

Returns **this**&#x20;

### getFeatures

**`获取feature，如果不传featureId，则返回所有feature，否则返回指定feature`**

#### Parameters

*   `featureId` **[string][1]?** featureId

Returns **([BaseFeature][5] | [Array][6]<[BaseFeature][5]> | [undefined][7])**&#x20;

### clearFeatures

**`清空元素`**

Returns **this**&#x20;

### updateFeature

**`更新元素`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `featureId` | 是 | [string][1] | 要素ID |
| `options` | 是 |`Partial<O>` | 要素选项的部分属性，其中 O 继承自 CommonFeatureOptT |
| `immediateRender` | 否 | [boolean][3] | 是否立即渲染 |

Returns **this**&#x20;

### removeFeature

**`移除元素`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `featureId` | 是 | [string][1] | 要素ID |
| `dontUnbind` | 否 | [boolean][3] | 是否不解绑Layer |

Returns **this**&#x20;

### removeFeatures

**`移除多个元素`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `featureIds` | 是 | [Array][6]<[string][1]> | 要素ID数组 |
| `dontUnbind` | 否 | [boolean][3] | 是否不解绑Layer |

Returns **this**&#x20;

### hasFeature

**`判断是否包含某个元素`**

#### Parameters

*   `featureId` **[string][1]**&#x20;

Returns **[boolean][3]**&#x20;

### scaleWithAnimation

带动画缩放

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `duration` | 是 | [number][8] | 动画持续时间，单位毫秒 |
| `options` | 否 | [Object][9] | 动画属性配置 |
| `options.cubicBezier` | 否 | [Array][6]<[number][8]> | 缓动函数，4个参数：[控制点1x, 控制点1y, 控制点2x, 控制点2y] |
| `options.onFinished` | 否 | [Function][10] | 动画结束回调函数 |
| `options.onProgress` | 否 | [Function][10] | 动画过程回调函数，参数为动画进度(0-1) |
| `featureIds` | 否 | [Array][6]<[string][1]> | 指定缩放的元素，不传则缩放所有元素 |

Returns **this**&#x20;

### fitToBounds

**`将图层视角调整到最佳显示范围`**

#### Parameters

*   `option` **[FitBoundsOptions][11]?**&#x20;

Returns **this**&#x20;

### getBounds

**`获取图层最佳显示范围`**

Returns **[LngLatBoundsLike][12]**&#x20;

### setPaintProperty

**`设置图层[Paint](/jsapi/apis/types/Types.html#paint)`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `property` | 是 | [string][1] | 图层paint属性名称 |
| `value` | 是 | `any` | 属性值 |

Returns **this**&#x20;

### setLayoutProperty

**`设置图层[Layout](/jsapi/apis/types/Types.html#layout)`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `property` | 是 | [string][1] | 图层layout属性名称 |
| `value` | 是 | `any` | 属性值 |

Returns **this**&#x20;

### getPaintProperty

**`获取图层[Paint](/jsapi/apis/types/Types.html#paint)`**

#### Parameters

*   `property` **[string][1]**&#x20;

Returns **any**&#x20;

### getLayoutProperty

**`获取图层[Layout](/jsapi/apis/types/Types.html#layout)`**

#### Parameters

*   `property` **[string][1]**&#x20;

Returns **any**&#x20;

### show

**`显示图层`**

Returns **this**&#x20;

### hide

**`隐藏图层`**

Returns **this**&#x20;

### on

**`监听鼠标事件`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 是 | `T` | 事件类型 |
| `cb` | 是 | `function (ev: `[LayerMouseEvent][13]`<T>, feature: (`[Array][6]`<F> \| F)): void`| 事件回调函数，接收事件对象和要素（单个或数组） |
| `featureId` | 否 | [string][1] | 指定要素ID |

Returns **this**&#x20;

### once

**`监听鼠标事件，只触发一次`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 是 | `T` | 事件类型 |
| `cb` | 是 | `function (ev: `[LayerMouseEvent][13]`<T>, feature: (`[Array][6]`<F> \| F)): void` | 事件回调函数，接收事件对象和要素（单个或数组），只触发一次 |
| `featureId` | 否 | [string][1] | 指定要素ID |

Returns **this**&#x20;

### off

**`取消监听鼠标事件`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 是 | `T` | 事件类型 |
| `cb` | 否 | `function (ev: `[LayerMouseEvent][13]`<T>): void` | 要取消的事件回调函数 |

Returns **this**&#x20;

## isAddedToMap

**`判断是否已经绘制在地图上`**

Returns **[boolean][3]**&#x20;

## LayerMouseEvent

**`图层事件类型`**

Type: <span>[LayerMouseEvent][13]</span>

### Examples

```javascript
type LayerMouseEvent<T extends keyof MapLayerEventType> = MapLayerEventType[T] & EventData
```

[1]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[2]: /jsapi/apis/map/Map.html

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean

[4]: /jsapi/apis/types/Types.html#geojsonsourceraw

[5]: /jsapi/apis/vector-layer/BaseFeature.html

[6]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array

[7]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/undefined

[8]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[9]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object

[10]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/function

[11]: /jsapi/apis/types/Types.html#fitboundsoptions

[12]: /jsapi/apis/types/Types.html#lnglatboundslike

[13]: #layermouseevent
