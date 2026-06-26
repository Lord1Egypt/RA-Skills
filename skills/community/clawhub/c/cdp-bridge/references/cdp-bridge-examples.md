# CDP Bridge 操作示例

## 示例 1：获取所有标签页

```powershell
# 使用脚本
.\scripts\cdp-call.ps1 -Tool "browser_get_tabs"

# 直接调用
$sessionId = InitializeSession
CallTool $sessionId "browser_get_tabs" "{}"
```

**输出：**
```
Session initialized: cb34dcb93ebb4a02a96960a53755c56d
{
  "tabs": [
    {"id": "702640649", "url": "https://example.com", "title": "Example"},
    {"id": "702640591", "url": "https://google.com", "title": "Google"}
  ],
  "active_tab": "702640649"
}
```

---

## 示例 2：切换标签页并扫描内容

```powershell
# 切换到标签页 702640640
.\scripts\cdp-call.ps1 -Tool "browser_switch_tab" -ArgsJson '{"tab_id":"702640640"}'

# 扫描页面内容（纯文本）
.\scripts\cdp-call.ps1 -Tool "browser_scan" -ArgsJson '{"text_only":true}'
```

---

## 示例 3：执行 JavaScript 点击按钮

```powershell
$jsScript = 'document.querySelector("#submit-button").click()'
$jsonArgs = @{script = $jsScript} | ConvertTo-Json -Compress
.\scripts\cdp-call.ps1 -Tool "browser_execute_js" -ArgsJson $jsonArgs
```

---

## 示例 4：获取页面标题

```powershell
$jsonArgs = @{script = 'document.title'} | ConvertTo-Json -Compress
.\scripts\cdp-call.ps1 -Tool "browser_execute_js" -ArgsJson $jsonArgs
```

---

## 示例 5：导航到新页面

```powershell
.\scripts\cdp-call.ps1 -Tool "browser_navigate" -ArgsJson '{"url":"https://github.com"}'
```

---

## 示例 6：截图并保存

```powershell
# 截图
$response = .\scripts\cdp-call.ps1 -Tool "browser_screenshot" -ArgsJson '{}'

# 解析 base64 并保存
$result = $response | ConvertFrom-Json
$base64 = $result.result  # 假设返回 base64 数据
[IO.File]::WriteAllBytes("screenshot.png", [Convert]::FromBase64String($base64))
```

---

## 示例 7：读取 Cookie

```powershell
# 当前页面 Cookie
.\scripts\cdp-call.ps1 -Tool "browser_cookies" -ArgsJson '{}'

# 指定 URL Cookie
.\scripts\cdp-call.ps1 -Tool "browser_cookies" -ArgsJson '{"url":"https://example.com"}'
```

---

## 示例 8：等待元素出现

```powershell
$condition = 'document.querySelector(".loading") === null'
$jsonArgs = @{
    condition_js = $condition
    timeout = 30
} | ConvertTo-Json -Compress
.\scripts\cdp-call.ps1 -Tool "browser_wait" -ArgsJson $jsonArgs
```

---

## 示例 9：批量操作

```powershell
$commands = @(
    @{cmd = "cdp"; method = "DOM.getDocument"; params = @{depth = 1}},
    @{cmd = "cdp"; method = "Runtime.evaluate"; params = @{expression = "window.location.href"}}
)
$jsonArgs = @{commands = $commands; timeout = 20} | ConvertTo-Json -Depth 3 -Compress
.\scripts\cdp-call.ps1 -Tool "browser_batch" -ArgsJson $jsonArgs
```

---

## 完整 PowerShell 函数封装

```powershell
function CdpGetTabs {
    $headers = @{
        "Accept" = "application/json, text/event-stream"
        "Content-Type" = "application/json"
    }
    $initBody = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}'
    $init = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/mcp' -Method POST -Headers $headers -Body $initBody -TimeoutSec 10
    $sessionId = $init.Headers["mcp-session-id"]
    
    $headers["mcp-session-id"] = $sessionId
    $toolBody = '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"browser_get_tabs","arguments":{}}}'
    $result = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/mcp' -Method POST -Headers $headers -Body $toolBody -TimeoutSec 30
    $json = ($result.Content -split "\n" | Where-Object { $_ -match "^data: " })[0].Substring(6) | ConvertFrom-Json
    return $json.result.content[0].text | ConvertFrom-Json
}

# 使用
$tabs = CdpGetTabs
$tabs.tabs | Format-Table
```

---

## 在 Skill 中使用的推荐写法

当调用本 skill 时，Agent 应：

1. **检查服务状态**
```powershell
try {
    Invoke-WebRequest -Uri 'http://127.0.0.1:8000/mcp' -Method POST -TimeoutSec 5 -ErrorAction Stop
} catch {
    Write-Host "CDP Bridge MCP 服务未启动"
}
```

2. **封装调用逻辑**
```powershell
$ProgressPreference = 'SilentlyContinue'
$headers = @{
    "Accept" = "application/json, text/event-stream"
    "Content-Type" = "application/json"
}
# 初始化...
```

3. **解析 SSE 响应**
```powershell
$content = $response.Content
$jsonLine = ($content -split "\n" | Where-Object { $_ -match "^data: " })[0].Substring(6)
$result = $jsonLine | ConvertFrom-Json
```