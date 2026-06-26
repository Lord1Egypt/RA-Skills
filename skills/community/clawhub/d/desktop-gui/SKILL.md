---
name: desktop-gui
description: "全桌面 GUI 自动化 — 使用 Python 库 (pyautogui, opencv) + xdotool + scrot，支持鼠标/键盘模拟、截图、视觉识别。"
metadata: {"openclaw":{"emoji":"🖥️","requires":{"bins":["python3","xdotool","scrot","tesseract"]}}}
---

# desktop-gui - 全桌面 GUI 自动化

## 概述

使用 Python 库实现全桌面 GUI 自动化，包括鼠标/键盘模拟、截图、视觉识别等。

### 🌟 两种模式

1. **传统模式**：xdotool + scrot + OCR（适合简单场景）
2. **视觉模式**：xdotool + scrot + **Qwen3.5-27b 视觉模型**（推荐，更智能）

## 依赖安装

```bash
# 核心库
pip3 install pyautogui pygetwindow pymsgbox opencv-python-headless pillow pytesseract

# 系统工具
sudo apt-get install -y xdotool scrot tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-chi-tra
```

## 核心功能

### 1. 鼠标控制
- 移动、点击、双击、右键
- 拖动、滑动
- 悬停

### 2. 键盘控制
- 输入文本
- 快捷键（Ctrl+C, Alt+Tab 等）
- 特殊键（Enter, Escape, Arrow 等）

### 3. 屏幕识别
- 截图（全屏/区域）
- 图像搜索（找按钮/图标位置）
- OCR 文字识别

### 4. 窗口管理
- 查找窗口
- 激活/最小化/关闭
- 获取窗口位置/大小

## 使用示例

```python
import pyautogui
import pygetwindow as gw
from PIL import Image
import time

# 暂停保护（误操作时按 Ctrl+C 停止）
pyautogui.PAUSE = 1

# 鼠标操作
pyautogui.moveTo(100, 200)  # 移动到坐标
pyautogui.click()           # 左键点击
pyautogui.doubleClick()     # 双击
pyautogui.rightClick()      # 右键
pyautogui.scroll(5)         # 滚动

# 键盘操作
pyautogui.typewrite('Hello World')
pyautogui.hotkey('ctrl', 'c')  # Ctrl+C
pyautogui.press('enter')

# 截图
screenshot = pyautogui.screenshot()
screenshot.save('/tmp/screen.png')

# 图像搜索（找按钮位置）
button_pos = pyautogui.locateOnScreen('button.png')
if button_pos:
    pyautogui.click(button_pos)

# 窗口管理
windows = gw.getAllWindows()
for w in windows:
    print(w.title, w.left, w.top, w.width, w.height)

# 激活窗口
for w in gw.getWindowsAt(100, 100):
    w.activate()
    break
```

## OpenClaw 集成

通过 `exec` 工具运行 Python 脚本：

```bash
python3 << 'EOF'
import pyautogui
pyautogui.press('f5')  # 刷新页面
EOF
```

## 安全注意事项

⚠️ **高危操作！**
- 误操作可能影响真实桌面
- 建议先在虚拟机测试
- 使用 `pyautogui.FAILSAFE = True`（鼠标移到屏幕角落停止）
- 添加 `PAUSE` 延迟观察效果

## 适用场景

✅ 适合：
- 桌面软件自动化（Office、专业软件）
- 游戏自动化
- 无 API 的老旧系统
- 跨应用工作流

❌ 不适合：
- 网页自动化（用 Playwright 更好）
- 需要视觉识别的复杂场景
- 高并发/生产环境

## 替代方案对比

| 方案 | 优点 | 缺点 |
|------|------|------|
| **pyautogui** | 简单易用、跨平台 | 慢、不精确、依赖屏幕分辨率 |
| **xdotool** | 快速、精确、Linux 原生 | 只能模拟输入、不能截图 |
| **Playwright** | 快速、可靠、支持 JS | 仅限浏览器 |
| **rdp + 远程** | 真实人类操作 | 成本高、需要真机 |

## 🎯 视觉模型驱动方案（推荐）

### 核心思想

用 Qwen3.5-27b 的**原生视觉能力**分析截图，直接返回操作建议：

```
截图 (scrot) → Qwen3.5-27b 分析 → 返回坐标/操作 → xdotool 执行
```

### 优势

✅ **不需要 OCR** - 直接理解界面布局和图标
✅ **上下文感知** - 能理解"这个按钮是干什么的"
✅ **更准确** - 视觉模型比规则匹配更可靠
✅ **更灵活** - 可以问复杂问题（"找到提交按钮"vs"点击坐标 300,200"）

### 示例代码

```python
import subprocess
import base64
import requests

# 1. 截图
subprocess.run(['scrot', '/tmp/screen.png'])

# 2. 转 Base64
with open('/tmp/screen.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

# 3. 问视觉模型
prompt = """
分析屏幕截图，找到打卡按钮，返回坐标。
用 JSON 格式：{"action": "click", "x": 450, "y": 320, "description": "打卡按钮"}
"""

response = requests.post(
    "http://10.6.207.56:8000/v1/chat/completions",
    headers={"Authorization": "Bearer VLLM_API_KEY"},
    json={
        "model": "qwen3.5-27b",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                {"type": "text", "text": prompt}
            ]
        }]
    }
)

result = response.json()['choices'][0]['message']['content']
print(result)  # 输出：{"action": "click", "x": 450, "y": 320}

# 4. 执行操作
import json
data = json.loads(result)
if data['action'] == 'click':
    subprocess.run(['xdotool', 'mousemove', str(data['x']), str(data['y'])])
    subprocess.run(['xdotool', 'click', '1'])
```

### 实际场景

**考勤系统打卡：**
```
1. 截图当前屏幕
2. 问模型："找到打卡/签到按钮，返回坐标"
3. 模型返回：{"x": 512, "y": 400, "confidence": 0.95}
4. xdotool 点击该坐标
5. 截图验证是否成功
```

**比传统方案强在哪里：**
- 传统：需要预先知道按钮坐标，或 OCR 识别文字
- 视觉：直接"看"屏幕理解，自适应界面变化
