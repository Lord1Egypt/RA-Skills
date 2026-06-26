---
outline: deep
---
 # Heatmap


## Heatmap

**`构造热力图，通过HeatmapOptions指定热力图样式`**<br>

> 继承[OverlayBase][1]

### Examples

```javascript
const heatmap = new DiMap.Heatmap({
 map: map,
 data: [
   [116.234,39.1231,12],
   [116.234,39.1231,10],
   [116.234,39.1231,20]
   ...
 ]
})
heatmap.show()
```

### constructor

#### Parameters

*   `options` **[HeatmapOptions][2]** 热力图选项

### getBounds

**`获取热力图最佳视野范围对象`**

#### Examples

```javascript
const bounds = heatmap.getBounds()
map.fitBounds(bounds, {
 padding: 100
})
```

Returns **[LngLatBounds][3]**&#x20;

## HeatmapOptions

**`热力图选项`**

### Properties

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `map` | 是 | [Map][4] | 地图实例 |
| `data` | 是 | <\[[number][6], [number][6], [number][6]]> | 热力数据，[经度, 纬度, 热力值] |
| `max` | 否 | [number][6] | 热力最大值(默认从data中计算得出)，越接近最大值，颜色越深 |
| `radius` | 否 | [number][6] | 热力半径大小，默认为30，单位像素 |
| `opacity` | 否 | [number][6] | 热力透明度，取值范围 [0,1]，0表示完全透明，1表示不透明。默认为0.8 |
| `userData` | 否 | Record<[string][7], any> | 用户自定义数据对象 |


[1]: /jsapi/apis/overlay/OverlayBase.html

[2]: #heatmapoptions

[3]: /jsapi/apis/coordinate/LngLatBounds.html

[4]: /jsapi/apis/map/Map.html

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array

[6]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[7]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String
