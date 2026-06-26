---
name: browser-use-init
description: 初始化并启动 Chrome DevTools Protocol（CDP）模式，支持用 Playwright 和 browser-use Agent 远程控制真实 Chrome 浏览器。解决 Chrome 145+ App-Bound Encryption 限制，自动复制 Profile 到非默认路径以启用 CDP。适合自动化网页操作、数据提取、Form 填表、爬虫等场景。
---

# browser-use-init Skill

## 概述

此 Skill 提供完整的 Chrome DevTools Protocol（CDP）初始化和连接方案，用于在 Chrome 145+ 版本下远程控制浏览器。

### 为什么需要这个 Skill

Chrome 130+ 引入了安全限制，`--remote-debugging-port` 强制要求使用非默认的 user-data-dir 路径。直接用默认 Profile 启动 CDP 调试会失败，导致无法用 Playwright 或 browser-use 连接浏览器。

此 Skill 通过**自动复制 Profile 到自定义目录**的方式绕过此限制，同时保留登录态。

---

## 快速开始

### 1. 首次初始化（一次性）

```bash
cd <skill 目录>/scripts
python start_chrome.py
```

输出示例：
```
[1] 关闭现有 Chrome...
[2] 准备 profile...
[profile] 首次复制 profile...
  复制 Default (~可能需要几分钟)...
[profile] 复制完成: <CHROME_PROFILE_DIR>
[3] 启动 Chrome (CDP 模式)...
[4] 等待 CDP 就绪...
[OK] Chrome 已启动: Chrome/145.0.7632.160
[OK] CDP 端口 9222 就绪
[OK] WS URL: ws://localhost:9222/devtools/browser/...
```

此时 Chrome 窗口已打开，可用浏览器操作。

### 2. 处理首次登录态丢失

如果登录状态丢失（DPAPI 绑定限制），需要**手动登录一次**：

- 在弹出的 Chrome 窗口中打开：你的登录网址
- 使用你的登录方式（App 扫码、验证码、账号密码等）完成登录
- 登录成功后关闭 Chrome

重新运行 `start_chrome.py`，登录态现已保存，以后启动无需重新登录。

### 3. 查询 CDP 连接信息

```bash
python query_cdp.py
```

输出：
```
Browser: Chrome/145.0.7632.160
WS URL: ws://localhost:9222/devtools/browser/8c3e...
Version: 12.7

标签页 (1):
  - 京东首页 | https://www.jd.com/
```

---

## 工作流场景

### 场景 A：用 Playwright 直接操作（确定性任务）

适用于：数据提取、页面截图、表单填充等明确的操作

```python
import asyncio
from scripts.playwright_connect import get_page

async def extract_data():
    pw, browser, page = await get_page()
    try:
        await page.goto("https://example.com/data-page")
        await page.wait_for_load_state("networkidle")
        
        # 用 JS 提取页面信息
        items = await page.evaluate("""
        () => {
            return Array.from(document.querySelectorAll('.item-name'))
                .map(el => el.textContent.trim());
        }
        """)
        print("提取的数据:", items)
    finally:
        await pw.stop()

asyncio.run(extract_data())
```

**优点**：
- 快速、可靠、确定性强
- 直接控制 DOM，支持 JS 注入
- 无需 LLM

---

### 场景 B：用 browser-use Agent（自然语言任务）

适用于：开放式任务、需要 AI 判断的操作

```bash
python run_agent.py --task "打开网站，找出最新发布的产品名称" --model qwen3.5:9b
```

或在代码中：

```python
import asyncio
from scripts.run_agent import run_task

asyncio.run(run_task(
    task="打开网站列表页，提取所有商品的名称和价格",
    model="qwen3.5:9b"
))
```

**优点**：
- 支持自然语言描述任务
- AI 自动判断操作流程
- 适合复杂的人机交互

**注意**：
- 需要本地 Ollama 运行且模型可用
- LLM 输出质量直接影响效果

---

## 技术详解

### 核心脚本说明

| 脚本 | 用途 | 何时使用 |
|------|------|--------|
| `start_chrome.py` | 启动 Chrome CDP 模式，复制 Profile | 首次初始化、每次重启浏览器 |
| `query_cdp.py` | 查询 CDP 连接状态和已打开标签页 | 诊断、获取 WebSocket URL |
| `playwright_connect.py` | 用 Playwright 直连 CDP Chrome | 需要确定性自动化操作 |
| `run_agent.py` | 用 browser-use Agent + LLM | 需要 AI 驱动的自然语言任务 |

### Chrome Profile 复制机制

首次运行 `start_chrome.py` 时：

1. **复制 Local State**：包含加密密钥元数据，确保旧 Cookie 能被解密
2. **复制 Default Profile**：包含所有 Cookie、历史记录、书签等
3. **排除大文件**：自动跳过 Cache、Code Cache、日志等不必要的文件（加快速度）

```
原始路径：%LOCALAPPDATA%\Google\Chrome\User Data
    ↓ (复制)
自定义路径：<CHROME_PROFILE_DIR>（可通过环境变量配置）
    ↓ (启动 Chrome)
Chrome 以 --remote-debugging-port 识别为"非默认路径" ✓
    ↓ (DPAPI 解密)
旧 Cookie 被解密并加载 ✓
```

### DPAPI 与登录态

**首次登录态可能丢失的原因**：DPAPI 密钥绑定到原始 user-data-dir 路径。

**解决方案**：手动登录一次后，新 Cookie 使用新路径的 DPAPI 密钥加密，之后自动保持。

详见：`references/chrome-cdp-solution.md` 中的 DPAPI 章节。

---

## 依赖与环境

### 最小依赖

```bash
# 仅启动 Chrome（无需额外包）
python start_chrome.py

# 查询 CDP（仅需标准库）
python query_cdp.py
```

### Playwright 支持

```bash
pip install playwright
playwright install chromium
```

### browser-use Agent 支持

```bash
pip install browser-use langchain-ollama
ollama pull qwen3.5:9b  # 或其他模型
```

---

## 常见问题

### Q: 为什么首次登录态丢失？

A: Chrome 126+ 用 DPAPI 加密 Cookie，密钥绑定到原始 user-data-dir。复制 Profile 后需重新登录一次，之后会自动保持。详见参考文档。

### Q: 我想多开几个 Chrome 实例，怎么做？

A: 修改 `start_chrome.py` 中的 `PORT` 和 `DST_DIR` 变量，为每个实例指定不同端口（如 9222、9223）和独立 Profile 目录。

### Q: CDP 端口 9222 一直不通

A: 检查清单（详见参考文档故障排查章节）：
- `tasklist | grep chrome` 确认 Chrome 进程
- `netstat -ano | grep 9222` 检查端口占用
- 确认 `--user-data-dir` 是非默认路径

### Q: Playwright 连接报 WebSocket 错误

A: 运行 `query_cdp.py` 确认 CDP 在线，再尝试连接。如仍失败，检查防火墙设置。

---

## 进阶用法

### 用法 1: 自定义 Profile 位置和端口

```bash
# 方式 1：修改脚本中的常数（开发模式）
# 编辑 start_chrome.py，修改 DST_DIR 和 PORT

# 方式 2：使用环境变量（推荐，更灵活）
$env:CHROME_PROFILE_DIR = "E:\my-chrome-profile"
$env:CDP_PORT = 9223
python start_chrome.py
```

### 用法 2: Playwright 中的高级操作

```python
async def fill_form():
    pw, browser, page = await get_page()
    try:
        await page.fill("input[name='username']", "user_input")
        await page.fill("input[name='password']", "pass_input")
        await page.click("button[type='submit']")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path="result.png")
    finally:
        await pw.stop()
```

### 用法 3: Agent 中自定义提示词

```python
asyncio.run(run_task(
    task="打开网站，用中文列出首页推荐商品的名称和价格",
    model="qwen3.5:9b"
))
```

---

## 技术参考

详细的技术说明、Chrome 版本历史、DPAPI 机制、故障排查等信息，见：

📄 **`references/chrome-cdp-solution.md`**

---

## 本 Skill 解决的核心问题

1. ✅ Chrome 130+ 强制非默认 user-data-dir 限制
2. ✅ DPAPI App-Bound Encryption 导致的登录态丢失
3. ✅ 简化 CDP 初始化流程（一条命令搞定）
4. ✅ 提供 Playwright 和 browser-use 两种使用方式
5. ✅ 完整的故障诊断和排查工具

---

## 下一步

- 运行 `python start_chrome.py` 启动 Chrome
- 查看 `references/chrome-cdp-solution.md` 深入了解技术细节
- 选择 Playwright（确定性）或 Agent（AI 驱动）的方式操作浏览器
