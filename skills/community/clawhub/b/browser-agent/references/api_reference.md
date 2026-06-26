# Browser Agent API 参考

## CDP 核心命令

### Page 域（页面操作）

```json
// 导航到 URL
{
  "method": "Page.navigate",
  "params": {"url": "https://example.com"}
}

// 截取截图
{
  "method": "Page.captureScreenshot",
  "params": {"format": "png", "quality": 80}
}

// 刷新页面
{
  "method": "Page.reload",
  "params": {"ignoreCache": true}
}

// 打印为 PDF
{
  "method": "Page.printToPDF",
  "params": {"paperWidth": 8.5, "paperHeight": 11}
}
```

### DOM 域（元素操作）

```json
// 获取文档根节点
{
  "method": "DOM.getDocument",
  "params": {"depth": -1}
}

// 查询选择器
{
  "method": "DOM.querySelector",
  "params": {"nodeId": 1, "selector": "#my-button"}
}

// 获取元素盒模型
{
  "method": "DOM.getBoxModel",
  "params": {"nodeId": 123}
}

// 获取元素属性
{
  "method": "DOM.getAttributes",
  "params": {"nodeId": 123}
}
```

### Input 域（输入事件）

```json
// 鼠标点击
{
  "method": "Input.dispatchMouseEvent",
  "params": {
    "type": "mousePressed",
    "x": 100, "y": 200,
    "button": "left",
    "clickCount": 1
  }
}

// 键盘输入
{
  "method": "Input.dispatchKeyEvent",
  "params": {
    "type": "keyDown",
    "text": "a",
    "unmodifiedText": "a"
  }
}
```

### Runtime 域（JavaScript 执行）

```json
// 执行表达式
{
  "method": "Runtime.evaluate",
  "params": {
    "expression": "document.title",
    "returnByValue": true
  }
}

// 调用函数
{
  "method": "Runtime.callFunctionOn",
  "params": {
    "functionDeclaration": "function() { return this.innerText; }",
    "objectId": "123456789.1"
  }
}
```

### Network 域（网络监控）

```json
// 启用网络事件
{
  "method": "Network.enable",
  "params": {"maxTotalBufferSize": 10000000}
}

// 获取响应体
{
  "method": "Network.getResponseBody",
  "params": {"requestId": "123.456"}
}
```

## 常用 JavaScript 片段

```javascript
// 获取所有链接
document.querySelectorAll('a').map(a => a.href)

// 获取表单数据
Array.from(document.querySelectorAll('input')).map(i => ({
  name: i.name,
  value: i.value,
  type: i.type
}))

// 模拟点击
document.querySelector('#button').click()

// 滚动到底部
window.scrollTo(0, document.body.scrollHeight)

// 获取页面文本
document.body.innerText

// 等待元素出现
await new Promise(r => {
  const el = document.querySelector('#target')
  if (el) r(el)
  else {
    const obs = new MutationObserver(() => {
      const el = document.querySelector('#target')
      if (el) { obs.disconnect(); r(el) }
    })
    obs.observe(document.body, {childList: true, subtree: true})
  }
})
```

## OpenClaw Browser 工具映射

| CDP 命令 | OpenClaw browser 工具 |
|---------|---------------------|
| Page.navigate | `browser(action="navigate", url=...)` |
| Page.captureScreenshot | `browser(action="screenshot")` |
| Input.dispatchMouseEvent | `browser(action="act", kind="click", ref=...)` |
| Input.dispatchKeyEvent | `browser(action="act", kind="type", text=...)` |
| Runtime.evaluate | `browser(action="act", kind="evaluate", fn=...)` |
| DOM.querySelector | `browser(action="snapshot", refs="aria")` + ref |

## 错误处理

```python
try:
    result = connector.send("Page.navigate", {"url": url})
    if result.get("errorText"):
        print(f"导航失败：{result['errorText']}")
except websocket.WebSocketTimeoutException:
    print("连接超时，尝试重连...")
    connector.connect()
except Exception as e:
    print(f"未知错误：{e}")
```

## 性能优化

1. **复用连接** - 使用 SessionManager 保持 WebSocket 连接
2. **批量操作** - 合并多个 DOM 查询为单次 evaluate
3. **懒加载** - 仅在需要时启用 Network/Runtime 域
4. **超时控制** - 设置合理的 WebSocket 超时（默认 10 秒）
