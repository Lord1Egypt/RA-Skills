---
outline: deep
---
 # CircleMarker


## CircleMarker

**`圆点标记，属性和方法与Circle一致，区别为CircleMarker不随着地图级别变化发生大小改变，radius的单位为px`**<br>

> 继承[Circle][1]

### Examples

```javascript
const circleMarker = new DiMap.CircleMarker({
 map: map,
 center: [116.405467, 39.907761],
 radius: 10,
 strokeColor: "#006600",
 strokeOpacity: 1,
 strokeWeight: 2,
 fillColor: "#006600",
 fillOpacity: 1,
 userData: {}
})
circleMarker.show()
```

### constructor

#### Parameters

*   `options` **CircleOptions** 圆形选项

[1]: /jsapi/apis/overlay/Circle.html
