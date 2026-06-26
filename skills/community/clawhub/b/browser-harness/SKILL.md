---
name: browser-harness
description: 浏览器自动化控制。通过 CDP 连接用户本机 Edge/Chrome，实现网页截图、内容提取、自动化操作。当用户需要：打开网页并截图、提取网页动态内容、看 JS 渲染的页面、自动化操作浏览器时触发。
---

# Browser Harness 技能

通过 `browser-harness` CLI 控制用户本机浏览器（Edge 或 Chrome）。

## 前置条件

1. **本机已安装 browser-harness**：
   ```bash
   git clone https://github.com/browser-use/browser-harness
   cd browser-harness
   uv tool install -e .
   ```

2. **浏览器调试模式启动**：
   ```bash
   # Edge（推荐）：
   "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222
   
   # 或 Chrome：
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
   ```

3. **设置环境变量**（每次使用前）：
   ```bash
   $env:BU_CDP_URL="http://127.0.0.1:9222"
   ```

## 常用命令

### 截图
```bash
browser-harness -c "new_tab('https://example.com'); wait_for_load(); capture_screenshot()"
```
截图保存到 `C:\Users\he\AppData\Local\Temp\shot.png`，用完后复制到工作目录分析。

### 打开网页
```bash
browser-harness -c "new_tab('https://example.com')"           # 新标签页打开
browser-harness -c "goto_url('https://example.com')"        # 在当前标签页打开
```

### 等待页面加载
```bash
browser-harness -c "new_tab('https://example.com'); wait_for_load()"
```

### 获取页面信息
```bash
browser-harness -c "print(page_info())"  # URL、标题、尺寸
browser-harness -c "js('document.body.innerText')"  # 页面文字内容
```

### 提取页面内容
```bash
browser-harness -c "js('document.title')"  # 标题
browser-harness -c "js('document.querySelectorAll(\"a\").length')"  # 链接数量
```

### 关闭标签页
```bash
browser-harness -c "close_tab()"
```

## 注意事项

- **新标签用 `new_tab()`**，不要用 `goto_url()`（会覆盖用户当前页面）
- **截图后** 从 `C:\Users\he\AppData\Local\Temp\shot.png` 复制出来分析
- **等待加载**：`wait_for_load()` 在导航后必须调用
- **JS 渲染页面**：`web_fetch` 抓不到的页面可以用这个
- **视频内容**：只能看到封面和文字，看不到实际视频内容
- **云端浏览器**：设置 `BROWSER_USE_API_KEY` 和 `start_remote_daemon()` 可用远程浏览器

## 故障排除

### 连接失败
```bash
# 检查调试端口是否开启
Invoke-RestMethod "http://localhost:9222/json/version"
# 有返回说明端口正常
```

### 重启浏览器调试
```bash
Stop-Process -Name msedge -Force
Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222
```
