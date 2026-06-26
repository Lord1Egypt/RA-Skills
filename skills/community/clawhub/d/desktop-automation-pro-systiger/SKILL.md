---
name: desktop-automation-pro
description: |
  Desktop GUI automation toolkit for browser, mobile devices, and native applications.
  桌面 GUI 自动化工具包，支持浏览器、移动设备和原生应用。
  
  Use this skill when:
  使用此技能的场景：
  - Automating web browsers (Chromium-based)
  - 控制 Chromium 浏览器
  - Controlling paired mobile devices (Android/iOS/macOS)
  - 控制配对的移动设备
  - Taking screenshots of desktop/windows/regions
  - 桌面/窗口/区域截图
  - Automating Windows native applications via Python
  - 通过 Python 自动化 Windows 原生应用
  - Mouse/keyboard simulation
  - 鼠标键盘模拟
  
  Triggers: 桌面自动化, GUI自动化, 浏览器自动化, 手机控制, 截图, desktop automation, GUI automation, browser automation, mobile control, screenshot, pyautogui, pywinauto
---

# Desktop GUI Automation / 桌面 GUI 自动化

Cross-platform GUI automation toolkit with browser control, mobile device management, and native app automation capabilities.

跨平台 GUI 自动化工具包，支持浏览器控制、移动设备管理和原生应用自动化。

## Capabilities Overview / 能力概览

| Platform 平台 | Tool 工具 | Use Case 使用场景 |
|---------------|-----------|-------------------|
| Browser 浏览器 | `browser` | Web automation, screenshots, form filling |
| Mobile 移动设备 | `nodes` | Device control, screen recording, camera |
| Desktop 桌面 | `screenshot` skill | Window/region capture |
| Native 原生应用 | Python scripts | Windows app automation, mouse/keyboard simulation |

---

## 1. Browser Automation / 浏览器自动化

Use the `browser` tool for Chromium-based browser control.

使用 `browser` 工具控制 Chromium 浏览器。

### Common Actions / 常用操作

```markdown
# Open URL / 打开网址
browser action=open url="https://example.com"

# Take screenshot / 截图
browser action=screenshot

# Click element / 点击元素
browser action=act kind=click ref="e12"

# Type text / 输入文本
browser action=act kind=type text="Hello" ref="e15"

# Get page snapshot / 获取页面快照
browser action=snapshot
```

### Workflow Example / 工作流示例

1. Start browser: `browser action=start`
2. Navigate: `browser action=open url="..."`
3. Snapshot to find elements: `browser action=snapshot`
4. Interact: `browser action=act kind=click ref="..."`
5. Capture result: `browser action=screenshot`

---

## 2. Mobile Device Control / 移动设备控制

Use the `nodes` tool for paired devices (Android/iOS/macOS).

使用 `nodes` 工具控制配对设备。

### Available Actions / 可用操作

| Action 操作 | Description 描述 |
|-------------|------------------|
| `camera_snap` | Take photo / 拍照 |
| `screen_record` | Record screen / 录屏 |
| `location_get` | Get GPS location / 获取位置 |
| `device_info` | Device status / 设备状态 |
| `run` | Execute command (iOS/macOS) / 执行命令 |

### Example Usage / 使用示例

```markdown
# List paired devices / 列出配对设备
nodes action=status

# Take screenshot / 截图
nodes action=camera_snap node="my-iphone" facing="back"

# Record screen / 录屏
nodes action=screen_record node="my-android" durationMs=10000
```

---

## 3. Native App Automation / 原生应用自动化

For Windows native applications, use Python scripts via `exec`.

Windows 原生应用通过 Python 脚本执行。

### Option A: Mouse/Keyboard Simulation / 鼠标键盘模拟

Use `pyautogui` for global input simulation.

使用 `pyautogui` 进行全局输入模拟。

```python
# scripts/pyautogui_demo.py
import pyautogui
import time

# Safety: move mouse to corner to abort / 安全：移到角落中止
pyautogui.FAILSAFE = True

# Get screen size / 获取屏幕尺寸
width, height = pyautogui.size()

# Move mouse / 移动鼠标
pyautogui.moveTo(100, 200, duration=0.5)

# Click / 点击
pyautogui.click(x=100, y=200)

# Type text / 输入文本
pyautogui.write('Hello World', interval=0.1)

# Hotkey / 快捷键
pyautogui.hotkey('ctrl', 'c')

# Screenshot / 截图
screenshot = pyautogui.screenshot()
screenshot.save('screenshot.png')

# Locate image on screen / 在屏幕上定位图片
position = pyautogui.locateOnScreen('button.png')
if position:
    pyautogui.click(position)
```

### Option B: Windows App Control / Windows 应用控制

Use `pywinauto` for native Windows application control.

使用 `pywinauto` 控制 Windows 原生应用。

```python
# scripts/pywinauto_demo.py
from pywinauto import Application
import time

# Method 1: Start new app / 方式1：启动新应用
app = Application().start('notepad.exe')

# Method 2: Connect to existing app / 方式2：连接已有应用
# app = Application().connect(title='Untitled - Notepad')

# Get main window / 获取主窗口
win = app.window(title='Untitled - Notepad')

# Type text / 输入文本
win.Edit.type_keys('Hello World{ENTER}', with_spaces=True)

# Menu operations / 菜单操作
win.menu_select('File->Save')

# Click button / 点击按钮
# win.Button1.click()

# Close window / 关闭窗口
win.close()
```

### Installation / 安装依赖

```bash
pip install pyautogui pywinauto pillow
```

---

## 4. Screenshot Capture / 截图捕获

Use the `screenshot` skill for desktop capture.

使用 `screenshot` 技能进行桌面截图。

```markdown
# Full screen / 全屏
Use screenshot skill

# Specific window / 特定窗口
Use browser or nodes tool

# Region / 区域
Use pyautogui.screenshot(region=(x, y, w, h))
```

---

## Quick Reference / 快速参考

| Task 任务 | Recommended Tool 推荐工具 |
|-----------|---------------------------|
| Web form filling 网页表单填充 | `browser` |
| Web scraping 网页抓取 | `browser` + snapshot |
| Mobile screen record 手机录屏 | `nodes` |
| Windows app control Windows应用控制 | `pywinauto` script |
| Global mouse/keyboard 全局鼠标键盘 | `pyautogui` script |
| Desktop screenshot 桌面截图 | `screenshot` skill |

---

## Best Practices / 最佳实践

1. **Browser**: Always use `snapshot` before interacting to get fresh element refs.
   浏览器：交互前先 `snapshot` 获取最新元素引用。

2. **Mobile**: Check device status with `nodes action=status` first.
   移动设备：先检查设备状态。

3. **Native Apps**: Enable FAILSAFE for pyautogui; add delays between actions.
   原生应用：启用 FAILSAFE 安全机制；操作间添加延迟。

4. **Error Handling**: Use try-except and validate element presence before clicking.
   错误处理：使用 try-except，点击前验证元素存在。

---

## Troubleshooting / 故障排查

| Issue 问题 | Solution 解决方案 |
|------------|-------------------|
| Browser won't start 浏览器无法启动 | Check if Chrome/Edge is installed |
| Device not found 设备未找到 | Run `nodes action=status` to check pairing |
| pyautogui click misses 点击偏移 | Check DPI scaling; use `pyautogui.position()` to verify |
| pywinauto connection failed 连接失败 | Run as admin; check app window title |
