---
outline: deep
---
 # AttributionControl


## AttributionControl

**`属性控件，可自定义地图copyright`** <br>

> 继承[Control][1]<br>
> 实现[IControl][2]

### Examples

```javascript
const aCtrol = new DiMap.AttributionControl({
  customAttribution: "Power by MapFE"
})
map.addControl(aCtrol, "bottom-right")
```

### constructor

构造函数


#### 参数
| 参数名 | 必选 | 类型 | 描述 |
|--------|------|------|------|
| options.compact | 否 | [boolean][3] \| [undefined][4] | 是否启用压缩模式，默认为 false |
| options.customAttribution | 否 | [string][5] \| [Array][6]\<[string][5]\> \| [undefined][4] | 自定义归属信息，可以是字符串或字符串数组 |

[1]: /jsapi/apis/types/Types.html#control

[2]: /jsapi/apis/types/Types.html#icontrol

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/undefined

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[6]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array
