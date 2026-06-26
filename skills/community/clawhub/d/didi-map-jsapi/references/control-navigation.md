---
outline: deep
---
 # NavigationControl


## NavigationControl

**`导航控件，添加缩放地图按钮`**<br>

> 继承[Control][1]<br>
> 实现[IControl][2]

### Examples

```javascript
const nCtrol = new DiMap.NavigationControl({
 showCompass: true, // 显示罗盘
 showZoom: true, // 显示zoom级别
 visualizePitch: true // 按钮可视化俯仰角
})
map.addControl(nCtrol,"top-left") // 添加到地图左上角（默认右上角）
```

### constructor

构造函数

#### 参数
| 参数名 | 必选 | 类型 | 描述 |
|--------|------|------|------|
| options.showCompass | 否 | [boolean][3] \| [undefined][4] | 是否显示指南针，默认为 true |
| options.showZoom | 否 | [boolean][3] \| [undefined][4] | 是否显示缩放控件，默认为 true |
| options.visualizePitch | 否 | [boolean][3] \| [undefined][4] | 是否可视化地显示倾斜角度，默认为 false |

[1]: /jsapi/apis/types/Types.html#control

[2]: /jsapi/apis/types/Types.html#icontrol

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/undefined
