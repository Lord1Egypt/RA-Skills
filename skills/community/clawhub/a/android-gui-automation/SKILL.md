---
name: android-gui-automation
description: Android GUI automation via MCP — MiniMax calls uiautomator2 tools through MCP protocol to control phone screens like a human. Supports ALL Android apps (Taobao, Pinduoduo, Xiaohongshu, Douyin, JD, WeChat). Use when: user wants phone automation, app control, price monitoring, social media posting, screen scraping, or any human-like phone operation from an AI agent. Works on Termux + MiniMax MCP. Can: click, swipe, type, screenshot, search, post, compare prices, schedule tasks, send alerts.
emoji: "📱"
---

# Android GUI Automation

让 MiniMax（或其他 MCP Client）通过 MCP 协议直接调用 uiautomator2，像真人一样控制 Android 手机屏幕。

## 架构

```
MiniMax API (MCP Client)
    ↓ MCP 调用
uiautomator2-mcp (在 Termux 里跑)
    ↓ uiautomator2
Android 手机屏幕 ← USB/无线 ADB
```

**核心优势：**
- MiniMax 直接理解用户意图
- MCP Tools 自动暴露所有手机操作能力
- 45 个现成工具，包括 `tap_sequence`（复合步骤序列）
- 不需要写死步骤，AI 自己拆解任务

---

## 第一步：Termux 安装

```bash
pkg install python python-pip
pip install uiautomator2 uiautomator2-mcp pillow requests schedule
python -m uiautomator2 init
```

## 第二步：启动 MCP Server

```bash
# 方式A: 直接运行（stdio 模式，AI 通过 stdin/stdout 调用）
uiautomator2-mcp

# 方式B: SSH 远程调用（从其他机器连接手机）
ssh user@phone-ip 'cd /path/to/project && uiautomator2-mcp'
```

## 第三步：MiniMax MCP 配置

在 MiniMax MCP 配置里添加：

```json
{
  "mcpServers": {
    "android": {
      "command": "ssh",
      "args": ["user@phone-ip", "uiautomator2-mcp"]
    }
  }
}
```

---

## 45 个可用 MCP Tools

### 连接 & 设备
| Tool | 说明 |
|------|------|
| `list_devices` | 列出 ADB 可见的所有设备 |
| `connect` | 连接设备（IP:5555 或自动发现） |
| `device_info` | 获取机型/屏幕/系统版本 |
| `current_app` | 获取当前前台 APP |

### 点击 & 滑动
| Tool | 说明 |
|------|------|
| `tap` | 点击坐标 |
| `double_tap` | 双击坐标 |
| `long_tap` | 长按坐标 |
| `multi_tap` | 多次点击 |
| `swipe` | 滑动（两点之间） |
| `drag` | 拖拽 |
| `press_key` | 按键（home/back/enter/power） |

### 输入
| Tool | 说明 |
|------|------|
| `input_text` | 输入文字 |
| `set_element_text` | 设置元素文字 |

### 元素定位
| Tool | 说明 |
|------|------|
| `find_element` | 查找元素（text/resourceID/class/xpath） |
| `tap_element` | 查找并点击元素 |
| `double_tap_element` | 查找并双击元素 |
| `element_exists` | 检查元素是否存在 |
| `wait_element` | 等待元素出现 |

### ⭐ 复合操作（最强大）
| Tool | 说明 |
|------|------|
| `tap_sequence` | **一次执行多步操作序列** |

```json
// tap_sequence 示例：淘宝搜索 iPhone
{
  "action": "tap_sequence",
  "steps": [
    {"action": "tap_element", "text": "搜索"},
    {"action": "wait", "timeout": 2},
    {"action": "input_text", "text": "iPhone 16 256GB"},
    {"action": "press_key", "key": "enter"},
    {"action": "wait", "timeout": 3},
    {"action": "screenshot", "save_path": "/sdcard/result.png"}
  ]
}
```

### 截图 & UI 分析
| Tool | 说明 |
|------|------|
| `screenshot` | 截图（可返回 base64 给 AI 分析） |
| `dump_hierarchy` | 获取 XML 界面结构 |
| `get_ui_tree` | 获取 JSON 格式完整 UI 树 |

### APP 管理
| Tool | 说明 |
|------|------|
| `app_start` | 启动 APP |
| `app_stop` | 停止 APP |
| `app_install` | 安装 APK |
| `app_clear` | 清空 APP 数据 |
| `app_info` | 获取 APP 信息 |

### 设备控制
| Tool | 说明 |
|------|------|
| `screen_on` | 亮屏 |
| `screen_off` | 灭屏 |
| `unlock` | 解锁 |
| `open_notification` | 打开通知栏 |
| `get_clipboard` | 读剪贴板 |
| `set_clipboard` | 写剪贴板 |

### 文件 & Shell
| Tool | 说明 |
|------|------|
| `push_file` | 推文件到手机 |
| `pull_file` | 从手机拉文件 |
| `shell` | 在手机上执行 shell |

### 日志
| Tool | 说明 |
|------|------|
| `get_logs` | 读取 logcat 日志 |
| `clear_logs` | 清空日志 |

---

## 使用示例

### 示例1：淘宝搜索商品

```
用户: "帮我去淘宝搜 iPhone 16 多少钱"

MiniMax MCP 调用:
1. tap_sequence([
     {action:"tap_element", text:"搜索"},
     {action:"input_text", text:"iPhone 16 256GB"},
     {action:"press_key", key:"enter"},
     {action:"wait", timeout:3}
   ])
2. screenshot(inline=true)  →  AI 视觉读价格
```

### 示例2：小红书发笔记

```
用户: "帮我发一条小红书，内容是今天发现超好用的AI工具"

MiniMax MCP 调用:
tap_sequence([
  {action:"tap_element", text:"发布"},
  {action:"wait", timeout:2},
  {action:"tap_element", text:"选择照片"},
  {action:"wait", timeout:1},
  {action:"tap", x:540, y:960},  // 选第一张
  {action:"tap_element", text:"完成"},
  {action:"wait", timeout:1},
  {action:"input_text", text:"今天发现一个超好用的AI工具！#AI工具"},
  {action:"tap_element", text:"发布"},
  {action:"wait", timeout:3}
])
```

### 示例3：多平台比价

```
用户: "帮我对比 iPhone 16 在淘宝、拼多多、京东的价格"

MiniMax 循环调用3次:
for platform in [taobao, pinduoduo, jd]:
  1. app_start(package=platform)
  2. tap_sequence([搜索 → 输入iPhone16 → 等待结果])
  3. screenshot(inline=true) → AI 读价格
汇总 → 生成对比 → 发 Telegram
```

---

## APP 包名速查

| APP | 包名 | 搜索 | 比价 | 发帖 |
|-----|------|:----:|:----:|:----:|
| 淘宝 | `com.taobao.taobao` | ✅ | ✅ | ✅ |
| 拼多多 | `com.xunmeng.pinduoduo` | ✅ | ✅ | ❌ |
| 小红书 | `com.xingin.xhs` | ✅ | ✅ | ✅ |
| 抖音 | `com.ss.android.ugc.aweme` | ✅ | ⚠️ | ✅ |
| 京东 | `com.jingdong.app.mall` | ✅ | ✅ | ❌ |
| 微信 | `com.tencent.mm` | ✅ | ❌ | ✅ |

---

## 定时任务 & 通知

```bash
# crontab 定时执行（Termux 里）
0 9,20 * * * python3 price_monitor.py >> ~/logs/price.log 2>&1
```

```python
# price_monitor.py — 用 MCP call 包装
import subprocess, json

def mcp_call(tool, **kwargs):
    req = {"jsonrpc":"2.0","method":"tools/call",
           "params":{"name":tool,"arguments":kwargs},"id":1}
    proc = subprocess.Popen(
        ["ssh", "phone-ip", "uiautomator2-mcp"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
    )
    out, _ = proc.communicate(input=json.dumps(req)+"\n")
    return json.loads(out)
```

---

## 已知限制

| 场景 | 支持 |
|------|------|
| 标准 UI APP | ✅ |
| 游戏/Unity APP | ❌ |
| 银行加固 APP | ⚠️ |
| 滑动验证码 | ⚠️ 需打码平台 |
| 人脸验证 | ❌ |

---

## 参考

- **uiautomator2-mcp**: https://pypi.org/project/uiautomator2-mcp/
- **uiautomator2**: https://github.com/openatx/uiautomator2
- 本地脚本: `scripts/android_automation.py`（独立 Python 版，无需 MCP）
