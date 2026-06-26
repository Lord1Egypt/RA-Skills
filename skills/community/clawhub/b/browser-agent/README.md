# Browser Agent 技能

> 🤖 让 AI 直接控制浏览器，实现真正的自动化操作

## 快速开始

### 1. 安装依赖

```bash
cd skills/browser-agent/scripts
pip install -r requirements.txt
```

### 2. 启动 Chrome（远程调试模式）

**Windows:**
```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\chrome-profile"
```

**macOS:**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-profile"
```

**或使用 OpenClaw 内置浏览器（推荐）:**
```python
browser(action="start")  # 自动配置 CDP
```

### 3. 测试连接

```bash
python browser_agent.py --check
```

输出示例:
```
✅ Chrome CDP 连接正常
   活跃标签页：3
   - Google
   - GitHub
   - X (Twitter)
```

### 4. 执行自动化任务

**截图:**
```bash
python browser_agent.py --url "https://example.com" --action screenshot --output page.png
```

**点击元素:**
```bash
python browser_agent.py --url "https://example.com" --action click --selector "#login-button"
```

**输入文本:**
```bash
python browser_agent.py --url "https://example.com" --action type --selector "#username" --text "myuser"
```

## 在 OpenClaw 中使用

```python
# 启动浏览器
browser(action="start")

# 导航到页面
browser(action="navigate", url="https://x.com")

# 获取页面快照（获取元素 ref）
browser(action="snapshot", refs="aria")

# 点击元素
browser(action="act", kind="click", ref="e123")

# 输入文本
browser(action="act", kind="type", text="Hello World")

# 执行 JavaScript
browser(action="act", kind="evaluate", fn="() => document.title")

# 截图
browser(action="screenshot", fullPage=True)
```

## 应用场景

### 1. 社交媒体管理
- 批量发布/删除推文
- 自动点赞、转发
- 监控提及和回复

### 2. 数据采集
- 抓取产品价格
- 监控竞品信息
- 收集用户评价

### 3. 跨平台同步
- Notion ↔ 飞书数据同步
- GitHub star 整理
- Analytics 数据导出

### 4. 自动化测试
- UI 回归测试
- 表单提交测试
- 登录流程验证

## 高级用法

### 会话保持

```python
from session_manager import CDPWithSession

client = CDPWithSession(ws_url)
client.enable_keep_alive(interval=60)  # 60 秒心跳

# 长时间运行任务
client.navigate("https://example.com")
time.sleep(300)  # 5 分钟后连接仍然有效
client.screenshot("final.png")
```

### 自定义脚本

创建 `my_automation.py`:

```python
from browser_agent import CDPConnector

cdp = CDPConnector()
cdp.connect()

# 登录
cdp.navigate("https://example.com/login")
cdp.type_text("#email", "user@example.com")
cdp.type_text("#password", "secret123")
cdp.click("#submit")

# 抓取数据
title = cdp.evaluate("document.title")
print(f"页面标题：{title}")

cdp.close()
```

运行:
```bash
python browser_agent.py --script my_automation.py
```

## 故障排查

### 问题：无法连接 Chrome

**检查 Chrome 是否运行:**
```bash
# Windows
tasklist | findstr chrome

# macOS
ps aux | grep Chrome
```

**重启 Chrome:**
```bash
# Windows
taskkill /F /IM chrome.exe
chrome.exe --remote-debugging-port=9222

# macOS
killall "Google Chrome"
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

### 问题：连接超时

- 确保端口 9222 未被防火墙阻止
- 检查 Chrome 是否使用相同的 `--user-data-dir`
- 尝试增加超时时间：`websocket.create_connection(url, timeout=30)`

### 问题：安全提示弹窗

使用 WebSocket 直连方案（`session_manager.py`），或在 Chrome 弹窗中手动点击"允许"。

## 参考资料

- [Chrome DevTools Protocol 官方文档](https://chromedevtools.github.io/devtools-protocol/)
- [websocket-client 文档](https://websocket-client.readthedocs.io/)
- [OpenClaw Browser 工具文档](../../../docs/browser.md)

## 许可证

MIT License
