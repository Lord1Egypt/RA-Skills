---
name: android-remote-browser-debug
description: >
  远程调试安卓手机浏览器（Edge/Chrome）。通过 ADB + Chrome DevTools Protocol
  直接连接手机浏览器，查看 Console 日志、网络请求、DOM 快照、执行 JS、截图。
  当用户提到手机调试、安卓浏览器、手机 Console、手机网页调试时使用。
metadata:
  version: 0.1.0
  author: kiro
  display_name: "安卓浏览器远程调试"
  tags:
    - android
    - browser
    - debug
    - console
    - edge
    - chrome
    - devtools
    - mobile
---

# 安卓浏览器远程调试 Skill

通过 USB + ADB 端口转发，将安卓手机上 Chromium 系浏览器（Edge、Chrome）的
DevTools Protocol 映射到本地，实现远程调试。

## 前置条件

1. **手机开启 USB 调试**（开发者选项 → USB 调试）
2. **USB 数据线连接 Mac 和手机**
3. **ADB 已安装**（Android SDK platform-tools）

本机 ADB 路径：
```
/Users/song/Library/Android/sdk/platform-tools/adb
```







## 建立连接

### 1. 确认设备连接

```bash
/Users/song/Library/Android/sdk/platform-tools/adb devices
# 应显示设备 ID + "device" 状态
```

### 2. 查找浏览器 DevTools Socket

```bash
/Users/song/Library/Android/sdk/platform-tools/adb shell "cat /proc/net/unix" | grep -i devtools
```

常见 socket 名：
- `@chrome_devtools_remote` — Chrome / Edge 浏览器
- `@webview_devtools_remote_<pid>` — WebView 调试
- `@huawei_webview_devtools_remote_<pid>` — 华为 WebView

### 3. ADB 端口转发

```bash
# Edge / Chrome 浏览器
/Users/song/Library/Android/sdk/platform-tools/adb forward tcp:9222 localabstract:chrome_devtools_remote

# 如果要调试 WebView（替换 <pid>）
/Users/song/Library/Android/sdk/platform-tools/adb forward tcp:9223 localabstract:webview_devtools_remote_<pid>
```

### 4. 验证连接

```bash
# 列出可调试的页面
curl -s http://localhost:9222/json/list | python3 -m json.tool

# 查看浏览器版本信息
curl -s http://localhost:9222/json/version | python3 -m json.tool
```

## 调试操作

所有操作通过 Node.js 脚本 + WebSocket 连接 CDP（Chrome DevTools Protocol）完成。

### 通用脚本模板

```javascript
// tmp_phone_debug.js
const WebSocket = require('ws');
const http = require('http');

http.get('http://localhost:9222/json/list', (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const pages = JSON.parse(data);
    // 选择目标页面（默认第一个）
    const wsUrl = pages[0].webSocketDebuggerUrl;

    const ws = new WebSocket(wsUrl);
    ws.on('open', () => {
      // 发送 CDP 命令
      ws.send(JSON.stringify({
        id: 1,
        method: 'Runtime.evaluate',
        params: { expression: 'YOUR_JS_HERE', returnByValue: true }
      }));
    });
    ws.on('message', (msg) => {
      const r = JSON.parse(msg.toString());
      if (r.id === 1) {
        console.log(JSON.stringify(r.result.result.value, null, 2));
        ws.close();
        process.exit(0);
      }
    });
    ws.on('error', e => { console.error('Error:', e.message); process.exit(1); });
    setTimeout(() => { console.error('Timeout'); process.exit(1); }, 10000);
  });
}).on('error', e => { console.error(e.message); process.exit(1); });
```

### 查看 Console 日志

需要先启用 `Runtime` domain 来接收 console 事件：

```javascript
// 启用后监听 consoleAPICalled 事件
ws.send(JSON.stringify({id: 1, method: 'Runtime.enable'}));
ws.send(JSON.stringify({id: 2, method: 'Log.enable'}));
```

或者用 HTTP 接口快速查看已有日志（不需要 WebSocket）：

```bash
# 通过 evaluate 获取 console 错误
node -e "..." # 用上面模板，expression 设为检查逻辑
```

### 查看网络请求

```javascript
// 启用 Network domain
ws.send(JSON.stringify({id: 1, method: 'Network.enable'}));
// 之后会收到 Network.requestWillBeSent / Network.responseReceived 事件
```

### 执行 JS 并获取结果

```javascript
ws.send(JSON.stringify({
  id: 1,
  method: 'Runtime.evaluate',
  params: {
    expression: 'document.title',
    returnByValue: true
  }
}));
```

### 截图

```javascript
ws.send(JSON.stringify({
  id: 1,
  method: 'Page.captureScreenshot',
  params: { format: 'png' }
}));
// 返回 base64 编码的图片数据
// 解码保存：
// const buf = Buffer.from(r.result.data, 'base64');
// require('fs').writeFileSync('/tmp/phone_screenshot.png', buf);
```

### DOM 快照

```javascript
ws.send(JSON.stringify({
  id: 1,
  method: 'Runtime.evaluate',
  params: {
    expression: 'document.documentElement.outerHTML.substring(0, 5000)',
    returnByValue: true
  }
}));
```

## 输出重定向注意

由于 shell 环境中 venv prompt 可能吞掉 stdout，**始终用文件重定向**：

```bash
node tmp_phone_debug.js > /tmp/phone_out.txt 2>&1
cat /tmp/phone_out.txt
```

或者合并到一行：

```bash
node tmp_phone_debug.js 1>/tmp/dbg.txt 2>/tmp/dbg_err.txt; echo "---stdout---"; cat /tmp/dbg.txt; echo "---stderr---"; cat /tmp/dbg_err.txt
```

## 常用诊断表达式

```javascript
// 页面基本信息
'JSON.stringify({url: location.href, title: document.title, innerW: innerWidth, innerH: innerHeight, screenW: screen.width, screenH: screen.height, dpr: devicePixelRatio})'

// 全屏状态
'JSON.stringify({fullscreenEnabled: document.fullscreenEnabled, isFullscreen: !!document.fullscreenElement, fullscreenEl: document.fullscreenElement ? document.fullscreenElement.tagName : null})'

// 所有按钮列表
'JSON.stringify(Array.from(document.querySelectorAll("button")).map(b => ({text: b.textContent.trim().substring(0,30), aria: b.getAttribute("aria-label"), disabled: b.disabled})))'

// 检查 iframe sandbox
'JSON.stringify(Array.from(document.querySelectorAll("iframe")).map(f => ({src: f.src.substring(0,80), sandbox: f.getAttribute("sandbox"), allowFullscreen: f.hasAttribute("allowfullscreen")})))'

// 检查 Service Worker
'JSON.stringify({swSupported: "serviceWorker" in navigator, swController: !!navigator.serviceWorker.controller})'

// 检查 localStorage 大小
'JSON.stringify({keys: Object.keys(localStorage).length, totalSize: JSON.stringify(localStorage).length})'
```

## 多页面选择

手机上可能打开了多个标签页，`/json/list` 返回所有可调试页面：

```bash
curl -s http://localhost:9222/json/list | python3 -c "
import json, sys
pages = json.load(sys.stdin)
for i, p in enumerate(pages):
    print(f'{i}: [{p[\"type\"]}] {p[\"title\"]} - {p[\"url\"][:80]}')
"
```

连接特定页面时替换 WebSocket URL 中的 page ID。

## 断开与清理

```bash
# 移除端口转发
/Users/song/Library/Android/sdk/platform-tools/adb forward --remove tcp:9222

# 移除所有转发
/Users/song/Library/Android/sdk/platform-tools/adb forward --remove-all

# 删除临时脚本
rm -f tmp_phone_debug.js tmp_debug*.js
```

## 踩坑记录

### ❌ WebSocket 403 Forbidden

错误信息：`Rejected an incoming WebSocket connection from the http://localhost:9222 origin`

**原因**：某些版本的 Chromium 要求 WebSocket 连接的 Origin 匹配白名单。

**解决**：Node.js 的 `ws` 库默认不发 Origin header，直接 `new WebSocket(url)` 即可连接。
如果用 Python 的 `websocket-client`，它会自动加 Origin 导致 403。

### ❌ ADB 设备显示 unauthorized

手机上弹出了 USB 调试授权对话框，需要在手机上点"允许"。

### ❌ 没有 devtools socket

浏览器可能没有打开任何页面，或者 USB 调试模式未正确开启。
确保手机上浏览器有至少一个打开的标签页。

### ❌ stdout 输出被 venv prompt 吞掉

shell 环境中 conda/venv 的 PS1 prompt 可能干扰输出捕获。
始终用 `> /tmp/xxx.txt` 重定向后再 `cat`。

### ❌ 页面 ID 变了

手机上刷新页面或切换标签后，page ID 会变。每次操作前先
`curl http://localhost:9222/json/list` 获取最新 ID。

## 与 Kiro Chrome DevTools MCP 的关系

Kiro 内置的 Chrome DevTools MCP 工具连接的是**本地 Mac 上的 Chrome 浏览器**，
无法直接切换到手机的调试端口。手机调试必须通过本 skill 描述的
ADB + Node.js WebSocket 方式进行。

如果未来 MCP 支持自定义连接端口，可以考虑将手机页面也纳入 MCP 管理。
