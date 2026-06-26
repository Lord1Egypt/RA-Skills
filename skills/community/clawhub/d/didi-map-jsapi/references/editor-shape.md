---
outline: deep
---
 # ShapeEdit


## ShapeEdit

**`图形编辑器`**  
<span style="font-size: 0.9em;">注：目前仅测试版本（1.0.1）支持</span>

### Examples

```javascript
// 以编辑多边形Polygon为例
window.DiMapLoader.load({
    key: "您申请的服务端key",
    plugins: ["ShapeEdit"],
}).then(({ DiMap, DiMapPlugin }) => {
    // 添加 控制按钮
    const anchor = document.createElement("div")
    anchor.className = "control"
    anchor.style.zIndex = "9999"
    anchor.innerHTML = "多边形"
    anchor.style.position = "absolute"
    anchor.style.top = "10px"
    anchor.style.left = "10px"        
    const mapContainer = map.getContainer()
    mapContainer.appendChild(anchor)

    // 创建图形编辑器
    const shapeEdit = new DiMapPlugin.ShapeEdit(map)

    anchor.onclick = () => {
      // 多边形编辑+吸附
      // 可编辑图形：多边形 Polygon、圆 Circle、线段 Line、矩形 Rectangle
      shapeEdit.edit("Polygon") 
    }
})
```

### constructor

#### Parameters

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `map` | 是 | [Map][1] | 地图实例 |
| `options` | 否 | [ShapeEditOptions][6] | 编辑选项 |

##### ShapeEditOptions
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `middlePointState` | 是 | `"showing" \| "default"` | 中间点显示状态 |

### edit

**`启动或结束编辑`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 是 | [string][2] | 编辑类型 `"Polygon" \| "Line" \| "Circle" \| "Rectangle"` |
| `options` | 否 | [EditOptions][7] | 可选参数对象，默认值为 `{}` |

##### EditOptions

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `editColor` | 否 | `string` | 编辑颜色 |
| `doneColor` | 否 | `string` | 完成颜色 |
| `shouldAdsor` | 否 | `boolean` | 是否吸附 |
| `initCoords` | 否 | `[number, number][]` | 初始坐标数组 |

Returns **void**&#x20;

### remove

**`删除选中的图形`**

Returns **void**&#x20;

### clearAll

**`删除地图上所有图形`**

Returns **void**&#x20;

### getSelectedPoints

**`获得当前编辑图形的点串`**

Returns **([Array][3]<\[[number][4], [number][4]]> | [undefined][5])**&#x20;

[1]: /jsapi/apis/map/Map.html

[2]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/undefined

[6]:/jsapi/apis/editors/ShapeEdit.html#shapeeditoptions

[7]:/jsapi/apis/editors/ShapeEdit.html#editoptions