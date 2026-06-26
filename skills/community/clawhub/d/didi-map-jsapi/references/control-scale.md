---
outline: deep
---
 # ScaleControl


## ScaleControl

**`比例尺控件`**<br>

> 继承[Control][1]<br>
> 实现[IControl][2]

### Examples

```javascript
const sCtrol = new DiMap.ScaleControl({
  maxWidth: 100, // 最大宽度（px）
  unit: "metric" // 单位，有效的度量单位字符串
})
map.addControl(sCtrol, "top-left") // 添加到地图左上角
```

### constructor

构造函数

#### 参数
| 参数名 | 必选 | 类型 | 描述 |
|--------|------|------|------|
| options.maxWidth | 否 | [number][3] \| [undefined][4] | 指定最大宽度（像素） |
| options.unit | 否 | [string][5] \| [undefined][4] | 指定单位，默认为"metric"，可选值："imperial"、"metric"、"nautical" |

### setUnit

设置单位

#### 参数

| 参数名 | 必选 | 类型 | 描述 |
|--------|------|------|------|
| unit | 是 | "imperial" \| "metric" \| "nautical" | 设置比例尺的单位 |

Returns **void**&#x20;

[1]: /jsapi/apis/types/Types.html#control

[2]: /jsapi/apis/types/Types.html#icontrol

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/undefined

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String
