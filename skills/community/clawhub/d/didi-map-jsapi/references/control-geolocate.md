---
outline: deep
---
 # GeolocateControl


## GeolocateControl

**`定位控件`**<br>

> 继承[Control][1]<br>
> 实现[IControl][2]

### Examples

```javascript
map.on('load', () => {
  const gCtrol = new DiMap.GeolocateControl()
  map.addControl(gCtrol, "top-right") // 显示在右上角
});
```

### constructor

构造函数

#### 参数

| 参数名 | 必选 | 类型 | 描述 |
|--------|------|------|------|
| options.positionOptions | 否 | [PositionOptions][3] \| [undefined][4] | 定位选项对象 |
| options.fitBoundsOptions | 否 | [FitBoundsOptions][5] \| [undefined][4] | 自适应地图视野选项对象 |
| options.trackUserLocation | 否 | [boolean][6] \| [undefined][4]| 是否追踪用户位置，默认为 false |
| options.showAccuracyCircle | 否 | [boolean][6] \| [undefined][4] | 是否显示用户位置精度圈，默认为 true |
| options.showUserLocation | 否 | [boolean][6] \| [undefined][4] | 是否显示用户位置，默认为 false |
| options.showUserHeading | 否 | [boolean][6] \| [undefined][4] | 是否显示用户朝向，默认为 false |
| options.geolocation | 否 | Geolocation \| [undefined][4] | 自定义 Geolocation 对象 |

**Geolocation 方法：**
- `getCurrentPosition()` - 获取当前位置
- `watchPosition()` - 持续监听位置变化
- `clearWatch()` - 停止监听位置变化

这是一个浏览器原生对象，不需要手动创建，除非需要自定义地理位置获取逻辑。

### trigger

触发定位

Returns **[boolean][6]**&#x20;

[1]: /jsapi/apis/types/Types.html#control

[2]: /jsapi/apis/types/Types.html#icontrol

[3]: /jsapi/apis/types/Types.html#positionoptions

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/undefined

[5]: /jsapi/apis/types/Types.html#fitboundsoptions

[6]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean
