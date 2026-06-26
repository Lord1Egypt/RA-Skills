---
outline: deep
---
 # Popup


## Popup

**`信息弹窗，它位于地图图层之上，是个DOM UI`**

### Examples

```javascript
new DiMap.Popup()
  .setLngLat([116.3924, 39.94369])
  .setHTML(`<h1>Hello Popup</h1>`)
  .addTo(map)
```

### constructor

**`创建一个 Popup 对象。`**

#### Parameters

*   `options` **[PopupOptions][1]?** 弹出框的选项

### addTo

**`将弹出框添加到地图上。`**

#### Parameters

*   `map` **[Map][2]** 地图对象

Returns **this** 返回 Popup 对象本身

### isOpen

**`检查弹出框是否处于打开状态。`**

Returns **[boolean][3]** 如果弹出框处于打开状态，则返回 true，否则返回 false

### remove

**`从地图中删除弹出框。`**

Returns **this** 返回 Popup 对象本身

### getLngLat

**`获取弹出框的经纬度坐标。`**

Returns **[LngLat][4]** 返回弹出框的经纬度坐标

### setLngLat

**`设置弹出框的经纬度坐标。`**

#### Parameters

*   `lnglat` **[LngLatLike][5]** 要设置的经纬度坐标

Returns **this** 返回 Popup 对象本身

### trackPointer

**`跟踪鼠标指针的位置以将弹出框放置在该位置。`**

Returns **this** 返回 Popup 对象本身

### getElement

**`获取弹出框的 HTML 元素。`**

Returns **[HTMLElement][6]** 返回弹出框的 HTML 元素

### setText

**`设置弹出框的文本内容。`**

#### Parameters

*   `text` **[string][7]** 要设置的文本内容

Returns **this** 返回 Popup 对象本身

### setHTML

**`设置弹出框的 HTML 内容。`**

#### Parameters

*   `html` **[string][7]** 要设置的 HTML 内容

Returns **this** 返回 Popup 对象本身

### setDOMContent

**`设置弹出框的 DOM 元素。`**

#### Parameters

*   `htmlNode` **[Node][8]** 要设置的 DOM 元素

Returns **this** 返回 Popup 对象本身

### getMaxWidth

**`获取弹出框的最大宽度。`**

Returns **[string][7]** 返回弹出框的最大宽度

### setMaxWidth

**`设置弹出框的最大宽度。`**

#### Parameters

*   `maxWidth` **[string][7]** 要设置的最大宽度

Returns **this** 返回 Popup 对象本身

### addClassName

**`给弹出框添加类名`**

#### Parameters

*   `className` **[string][7]** 要添加的类名

Returns **void**&#x20;

### removeClassName

**`移除弹出框的类名`**

#### Parameters

*   `className` **[string][7]** 要移除的类名

Returns **void**&#x20;

### setOffset

**`设置弹出框偏移量`**

#### Parameters

*   `offset` **([Offset][9] | null | [undefined][10])** 元素偏移量

Returns **this**&#x20;

### toggleClassName

**`切换弹出框的类名`**

#### Parameters

*   `className` **[string][7]** 要切换的类名

Returns **void**&#x20;

[1]: /jsapi/apis/types/Types.html#popupoptions

[2]: /jsapi/apis/map/Map.html

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean

[4]: /jsapi/apis/coordinate/LngLat.html

[5]: /jsapi/apis/types/Types.html#lnglatlike

[6]: https://developer.mozilla.org/docs/Web/HTML/Element

[7]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[8]: https://developer.mozilla.org/docs/Web/API/Node/nextSibling

[9]: /jsapi/apis/types/Types.html#offset

[10]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/undefined
