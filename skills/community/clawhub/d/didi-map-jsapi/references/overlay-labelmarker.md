---
outline: deep
---
 # LabelMarker


## LabelMarker

**`标注类，支持大量点标注和文本标注的绘制，基于LabelLayer图层绘制`**<br>

> 继承[SymbolFeature][1]

### Examples

```javascript
const labelMarker = new DiMap.LabelMarker({
  position: [116.405467, 39.907761],
  zooms: [0, 22],
  opacity: 1,
  zIndex: 1,
  icon: {
    image: "https://xxx.com/marker.png",
    size: [46 * 0.6, 66 * 0.6],
    anchor: "bottom",
    offset: [0, 4]
  },
  text: {
    content: "文字内容",
    direction: "top",
    offset: 0,
    style: {
      fontSize: 12,
      fillColor: "#000"
    }
  }
})
const labelLayer = new LabelLayer({
 visible: true,
 opacity: 1,
 collision: true,
 zooms: [0, 22]
})
labelLayer.add(labelMarker)
labelLayer.addToMap(map)
```

### constructor

#### Parameters

*   `options` **[LabelMarkerOptions][2]** 标注属性

### setLabelMarkerOptions

**`设置标注属性`**

#### Parameters

*   `options` **Partial<[LabelMarkerOptions][2]>** 标注属性

Returns **this**&#x20;

### getLabelMarkerOptions

**`获取标注属性`**

Returns **[LabelMarkerOptions][2]** 标注属性

### getPosition

**`获取标注位置`**

Returns **[LngLatLike][3]** 标注位置

### show

**`显示标注`**

Returns **this**&#x20;

### hide

**`隐藏标注`**

Returns **this**&#x20;

## TextDirection

**`文字方向`**

Type: <span>[string][4]</span>

### Properties

*   `left` **`"left"`** 左
*   `right` **`"right"`** 右
*   `top` **`"top"`** 上
*   `bottom` **`"bottom"`** 下

## LabelMarkerOptions

**`标注属性`**

### Properties

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `position` | 是 | [LngLatLike][3] | 标注位置 |
| `zooms` | 否 | [[number][5], [number][5]] | 标注显示级别，默认[0-22] |
| `opacity` | 否 | [number][5] | 透明度，默认1 |
| `zIndex` | 否 | [number][5] | 层级，默认1 |
| `icon` | 否 | [Object][6] | 图标配置 |
| `icon.image` | 否 | [string][4] | 图标地址，禁用图标时设置为空字符串 |
| `icon.size` | 否 | [number][5] \| [[number][5], [number][5]] | 图标大小，倍数或指定宽高，默认[27.6, 39.6] |
| `icon.anchor` | 否 | [Anchor][8] | 图标锚点，默认bottom |
| `icon.offset` | 否 | [[number][5], [number][5]] | 图标偏移，默认[0, -4] |
| `text` | 否 | [Object][6] | 文字配置 |
| `text.content` | 否 | [string][4] | 文字内容，禁用文字时设置为空字符串 |
| `text.direction` | 否 | [TextDirection][9] | 文字方向，默认top |
| `text.offset` | 否 | [number][5] | 相对方向的偏移 |
| `text.style` | 否 | [Object][6] | 文字样式 |
| `text.style.fontSize` | 否 | [number][5] | 字体大小，默认12 |
| `text.style.fillColor` | 否 | [string][4] | 填充颜色，默认#000 |


[1]: /jsapi/apis/vector-layer/SymbolFeature.html

[2]: #labelmarkeroptions

[3]: /jsapi/apis/types/Types.html#lnglatlike

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[6]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object

[7]: https://xxx.com/marker.png

[8]: /jsapi/apis/types/Types.html#anchor

[9]: #textdirection
