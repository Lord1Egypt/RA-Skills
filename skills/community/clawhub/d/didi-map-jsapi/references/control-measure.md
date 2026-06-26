---
outline: deep
---
 # Measure


## Measure

**`距离测量控件`** <br>

### Examples

```javascript
window.DiMapLoader.load({
    key: "您申请的服务端key",
    plugins: ["Measure"],
}).then(({ DiMap, DiMapPlugin }) => {
    // 创建 测距工具
    const measure = new DiMapPlugin.Measure(map)
    console.log("measure", measure)

    // 添加 触发测距的按钮
    const mapContainer = map.getContainer()
    const anchor = document.createElement("div")
    anchor.className = "control"
    anchor.style.zIndex = "9999"
    anchor.innerHTML = "开始测距"
    anchor.style.position = "absolute"
    anchor.style.right = "10px"
    anchor.style.top = "10px"
    mapContainer.appendChild(anchor)

    // 监听 测距按钮的点击事件
    let measureActive = false
    anchor.onclick = () => {
        measureActive = !measureActive
        if (measureActive) {
            measure.startMeasure()
            anchor.innerHTML = "结束测距"
        } else {
            measure.finishMeasure()
            anchor.innerHTML = "开始测距"
        }
    }
});
```

### startMeasure

**`开始测量`**

Returns **void**&#x20;

### finishMeasure

**`结束测量`**

Returns **void**&#x20;

[1]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[2]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String