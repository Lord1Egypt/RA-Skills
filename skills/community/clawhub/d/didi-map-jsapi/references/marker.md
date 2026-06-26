---
outline: deep
---
 # Marker


## Marker

**`一般点标记，它位于地图图层之上，是个DOM UI`** <br>

> 继承[Evented][1]

### Examples

```javascript
const marker = new DiMap.Marker({
 element: document.createElement('div'),
 anchor: 'bottom-left',
 offset: [0, 0],
 draggable: true,
 rotation: 0,
 rotationAlignment: 'auto',
 pitchAlignment: 'auto'
})
marker.setLngLat([116.397411, 39.909186])
marker.addTo(map)
```

### constructor

**`创建一个 Marker 对象。`**

#### Parameters

*   `options` **[MarkerOptions][2]?** 标记选项

### constructor

**`创建一个 Marker 对象，并指定容器元素。`**

#### Parameters

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `element` | 否 | [HTMLElement][3] | 容器元素 |
| `options` | 否 | [MarkerOptions][2] | 标记选项 |

### addTo

**`将标记添加到地图上。`**

#### Parameters

*   `map` **[Map][4]** 要添加到的地图对象

Returns **this** 返回 Marker 对象本身

### remove

**`从地图上删除标记。`**

Returns **this** 返回 Marker 对象本身

### getLngLat

**`获取标记的经纬度。`**

Returns **[LngLat][5]** 返回 LngLat 对象

### setLngLat

**`设置标记的经纬度。`**

#### Parameters

*   `lngLat` **[LngLatLike][6]** 经纬度

Returns **this** 返回 Marker 对象本身

### getElement

**`获取标记的容器元素。`**

Returns **[HTMLElement][3]** 返回容器元素

### setPopup

**`设置标记的弹出窗口。`**

#### Parameters

*   `popup` **[Popup][7]?** 弹出窗口

Returns **this** 返回 Marker 对象本身

### getPopup

**`获取标记的弹出窗口。`**

Returns **[Popup][7]** 返回 Popup 对象

### togglePopup

**`切换标记的弹出窗口的显示状态。`**

Returns **this** 返回 Marker 对象本身

### getOffset

**`获取标记的偏移量。`**

Returns **[PointLike][8]** 返回 PointLike 对象

### getOffset

**`获取标记的偏移量。`**

Returns **[PointLike][8]** 返回 PointLike 对象

### setOffset

**`设置标记的偏移量。`**

#### Parameters

*   `offset` **[PointLike][8]** 偏移量

Returns **this** 返回 Marker 对象本身

### setDraggable

**`设置标记是否可拖拽。`**

#### Parameters

*   `shouldBeDraggable` **[boolean][9]** 是否可拖拽

Returns **this** 返回 Marker 对象本身

### isDraggable

**`判断标记是否可拖拽。`**

Returns **[boolean][9]** 如果可拖拽，返回 true；否则，返回 false

### getRotation

**`获取标记的旋转角度。`**

Returns **[number][10]** 返回旋转角度，单位为度数

### setRotation

**`设置标记的旋转角度。`**

#### Parameters

*   `rotation` **[number][10]** 旋转角度，单位为度数

Returns **this** 返回 Marker 对象本身

### getRotationAlignment

**`获取标记的旋转对齐方式。`**

Returns **[Alignment][11]** 返回旋转对齐方式

### setRotationAlignment

**`设置标记的旋转对齐方式。`**

#### Parameters

*   `alignment` **[Alignment][11]** 旋转对齐方式

Returns **this** 返回 Marker 对象本身

### getPitchAlignment

**`获取标记的俯仰对齐方式。`**

Returns **[Alignment][11]** 返回俯仰对齐方式

### setPitchAlignment

**`设置标记的俯仰对齐方式。`**

#### Parameters

*   `alignment` **[Alignment][11]** 俯仰对齐方式

Returns **this** 返回 Marker 对象本身

[1]: /jsapi/apis/base/Evented.html

[2]: /jsapi/apis/types/Types.html#markeroptions

[3]: https://developer.mozilla.org/docs/Web/HTML/Element

[4]: /jsapi/apis/map/Map.html

[5]: /jsapi/apis/coordinate/LngLat.html

[6]: /jsapi/apis/types/Types.html#lnglatlike

[7]: /jsapi/apis/popup/Popup.html

[8]: /jsapi/apis/types/Types.html#pointlike

[9]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean

[10]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[11]: /jsapi/apis/types/Types.html#alignment
