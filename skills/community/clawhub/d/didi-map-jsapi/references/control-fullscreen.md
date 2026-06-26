---
outline: deep
---
 # FullscreenControl


## FullscreenControl

**`全屏控件，可设置地图全屏显示`**<br>

> 继承[Control][1]<br>
> 实现[IControl][2]

### Examples

```javascript
map.on('load', () => {
    const fCtrol = new DiMap.FullscreenControl()
    map.addControl(fCtrol, 'top-left')  // 显示在左上角
});
```

### constructor

构造函数

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
|--------|------|------|------|
| options | 否 | [FullscreenControlOptions][3] \| null | 全屏控件配置选项 |

[1]: /jsapi/apis/types/Types.html#control

[2]: /jsapi/apis/types/Types.html#icontrol

[3]: /jsapi/apis/types/Types.html#fullscreencontroloptions
