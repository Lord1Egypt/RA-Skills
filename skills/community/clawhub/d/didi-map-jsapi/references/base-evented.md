---
outline: deep
---
 # Evented


## Evented

**`发布订阅类`**

### Examples

```javascript
const evented = new DiMap.Evented()
evented.on('test', (e) => {
 console.log(e)
})
evented.fire('test', { test: 'test' })
evented.off('test')
evented.once('test', (e) => {
 console.log(e)
})
```

### on

**`订阅事件`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 是 | [string][1] | 事件类型 |
| `listener` | 是 | [EventedListener][2] | 事件回调函数 |

Returns **this**&#x20;

### off

**`取消订阅事件`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 否 | [string][1] \| any | 事件类型 |
| `listener` | 否 | [EventedListener][2] | 事件回调函数 |

Returns **this**&#x20;

### once

**`订阅事件（仅订阅一次）`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 是 | [string][1] | 事件类型 |
| `listener` | 是 | [EventedListener][2] | 事件回调函数 |

Returns **this**&#x20;

### fire

**`触发事件`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 是 | [string][1] | 事件类型 |
| `properties` | 否 | [Object][3]<[string][1], any> | 事件负载数据 |

Returns **this**&#x20;

[1]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[2]: /jsapi/apis/types/Types.html#eventedlistener

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object
