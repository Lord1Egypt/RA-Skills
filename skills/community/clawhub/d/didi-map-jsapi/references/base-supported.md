---
outline: deep
---
 # Supported


## supported

**`判断当前环境是否支持地图渲染`**

### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `options` | 否 | [Object][2] | 配置选项 |
| `options.failIfMajorPerformanceCaveat` | 否 | [boolean][1] | 当存在可能严重影响性能的因素时，是否判定为不支持 |

Returns **[boolean][1]**&#x20;

### Examples

```javascript
const supported = DiMap.supported()
```

[1]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean
[2]: https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object