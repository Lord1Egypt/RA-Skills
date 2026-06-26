---
outline: deep
---
 # LabelLayer


## LabelLayer

**`LabelLayer 类是用于承载 LabelMarker 对象的图层`**

### Examples

```javascript
const labelMarker = new DiMap.LabelMarker({...}) // 见 LabelMarker
const labelLayer = new DiMap.LabelLayer({
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

*   `options` **[LabelLayerOptions][1]?** 图层选项

### addToMap

**`添加到地图`**

#### Parameters

*   `map` **[Map][2]** 地图实例

Returns **this**&#x20;

### removeFromMap

**`从地图移除`**

#### Parameters

*   `map` **[Map][2]?** 地图实例

Returns **this**&#x20;

### fitBounds

**`调整到最佳视野`**

#### Parameters

*   `options` **[FitBoundsOptions][3]?** 视野调整选项

Returns **this**&#x20;

### setOptions

**`设置属性`**

#### Parameters

*   `option` **[LabelLayerOptions][1]** 属性

Returns **this**&#x20;

### show

**`显示`**

Returns **this**&#x20;

### hide

**`隐藏`**

Returns **this**&#x20;

### add

**`添加标注`**

#### Parameters

*   `labelMarker` **([LabelMarker][4] | [Array][5]<[LabelMarker][4]>)** 标注

Returns **this**&#x20;

### remove

**`移除标注`**

#### Parameters

*   `labelMarker` **([LabelMarker][4] | [Array][5]<[LabelMarker][4]>)** 标注

Returns **this**&#x20;

### clear

**`清空标注`**

Returns **this**&#x20;

## LabelLayerOptions

**`LabelLayerOptions`**

### Properties
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `visible` | 否 | [boolean][6] | 是否可见 |
| `opacity` | 否 | [number][7] | 透明度 |
| `collision` | 否 | [boolean][6] | 是否避让 |
| `zooms` | 否 | [[number][7], [number][7]] | 显示层级范围 |


[1]: #labellayeroptions

[2]: /jsapi/apis/map/Map.html

[3]: /jsapi/apis/types/Types.html#fitboundsoptions

[4]: /jsapi/apis/overlay/LabelMarker.html

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array

[6]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean

[7]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number
