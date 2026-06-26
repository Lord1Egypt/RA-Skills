---
name: android-auto-controller
description: "控制 Android 手机的终极工具。具备视觉状态感知、自动关闭干扰弹窗、模拟人手操作的能力。内置严格的反幻觉校验机制和防绕过限制，以真实的屏幕视觉反馈为唯一判断标准。"
metadata: {"openclaw":{"emoji":"📱","requires":{"bins":["python3"],"env":["VLM_API_KEY","VLM_BASE_URL","VLM_MODEL_NAME","VLM_COORD_SCALE"]},"primaryEnv":"VLM_API_KEY"}}
---

# 📱 Android Auto Controller (安卓视觉自动化控制)

> **🧑‍💻 以下内容为人类用户阅读的安装与配置指南**

这是一个为 OpenClaw 打造的硬核安卓手机控制技能。它通过连接外部的 **视觉大模型 (VLM)** 作为智能体的“眼睛”，配合 `uiautomator2` 作为“手”，让你的数字员工能够像真人一样感知手机屏幕、自动跳过开屏广告、处理系统弹窗，并完成复杂的跨 App 任务。

## 🛠️ 前置准备 (非常重要！)

在开始使用前，**请确保你的物理环境已准备就绪**，否则脚本将无法控制你的手机。

1. **手机端准备**：准备一台安卓手机，通过 USB 数据线连接到运行 OpenClaw 的电脑上。在“开发者选项”中开启 **[USB 调试]**（部分品牌如小米/vivo还需开启 **[USB 调试 (安全设置)]** 允许模拟点击）。
2. **环境初始化**：确保电脑上已安装 `python3`，并执行 `pip install uiautomator2 openai` 安装依赖。
3. **注入灵魂**：在手机保持亮屏连接的状态下，在电脑终端执行以下命令（这会在你的手机上安装 ATX 守护程序）：
   ```bash
   python -m uiautomator2 init

## ⚙️ 安装与配置

在 OpenClaw 中安装此技能后，请在你的 `~/.openclaw/config.json` 中配置你的视觉模型参数：

~~~shell
{
  "skills": {
    "entries": {
      "android-auto-controller": {
        "enabled": true,
        "apiKey": "你的_VLM_API_KEY", 
        "env": {
          "VLM_BASE_URL": "http://你的模型API地址:端口/v1",
          "VLM_MODEL_NAME": "qwen3-vl-8b", 
          "VLM_COORD_SCALE": "1000"
        }
      }
    }
  }
}
~~~



> **🤖 以下内容为 AI Agent 核心指令区 (AI Instructions Below)**

## When to Use (何时使用)

当用户要求操作手机（如打开App、发送消息、寻找联系人、点击特定元素）时使用。你必须充当一个极其严谨的自动化机器人，**绝对禁止脑补或虚构任何操作结果**。任务的推进和完结必须 100% 依赖真实的屏幕反馈。

## Usage (如何使用)
请通过 Bash 工具运行以下命令来执行 Python 脚本。务必将 `<action_name>` 和 `<parameter_value>` 替换为实际需要的参数。

```bash
python3 {baseDir}/scripts/android_agent.py --action <action_name> --param "<parameter_value>"
```

*(注意：如果是不需要参数的 action，可以省略 `--param`)*

## Arguments (核心动作清单与参数说明)

### 1. 核心感知与规划动作 (每次行动前后的必备动作)

- `analyze_plan`: **大模型的眼睛与大脑。** 截图并调用视觉大模型，分析当前屏幕真实状态。
  - `--param`: 传入用户的最终任务目标描述（例如 "给张三发送你好"）。
  - **输出**: 必须严格读取返回的 JSON (observation, thought, recommended_action)。

### 2. 原子执行动作 (由 analyze_plan 决策后单步调用)

- `get_info`: 获取设备基础状态及当前所在页面的包名。
  - `--param`: 无需参数（可留空）。
- `vision_find`: 调用 VLM 视觉大模型定位画面中特定目标的物理坐标（配合 `click_xy` 使用）。
  - `--param`: 目标的文字或外观描述（例如 "微信右上角的+号" 或 "发送按钮"）。
- `click_xy`: 点击屏幕上的特定物理像素坐标。
  - `--param`: 坐标值，严格遵循 "x,y" 格式（例如 "500,1200"）。
- `click_text`: 直接点击屏幕上的特定文字（常用于快速点击"跳过"、"确定"、"取消"等标准按钮）。
  - `--param`: 需要点击的精确文本内容（例如 "跳过"）。
- `input`: 在当前已经聚焦的输入框中注入文字内容。
  - `--param`: 要输入的具体文本内容。**【警告】执行前必须先用 click_xy 或 click_text 点击一下输入框，确保光标闪烁！**
- `swipe`: 在屏幕上模拟手指滑动。
  - `--param`: 滑动方向，仅支持 "left", "right", "up", "down"。
- `open_app`: 通过 Android 底层包名强制拉起应用。
  - `--param`: 应用的完整包名（例如 "com.tencent.mm"）。
- `smart_open_app`: 通过中文名称智能打开常用应用，自带回桌面寻找的兜底策略。
  - `--param`: 应用的日常中文名称（例如 "微信"、"美团" 或 "淘宝"）。
- `press_key`: 模拟按下 Android 系统的全局导航按键。
  - `--param`: 按键名称，仅支持 "home" (桌面), "back" (返回), "enter" (回车)。
- `wait`: 主动暂停挂机等待若干秒，专门用于避让顶部横幅通知、等广告倒计时或等待页面加载。
  - `--param`: 需要等待的秒数，必须是整数（例如 "3" 或 "5"）。

### 3. 任务状态信号 (终止 ReAct 循环)

- `task_complete`: 汇报任务成功。
  - `--param`: 成功的原因说明。
- `task_failed`: 汇报任务遭遇无法克服的障碍并终止。
  - `--param`: 失败的原因说明。

## Output & Notes (反幻觉铁律与操作 SOP)

**🚨 核心架构与禁令 (CRITICAL BANS):**

1. **禁止手搓代码 (NO INLINE SCRIPTING)**：**绝对不允许**使用 `python -c` 或编写任何自定义的 Python 脚本/内联代码来操作手机！你没有任何权限直接调用 `uiautomator2`。
2. **唯一合法途径**：你**必须且只能**通过 Bash 运行 `python3 {baseDir}/scripts/android_agent.py --action <action_name> --param "<param>"` 这一条命令来控制设备。任何绕过此脚本的行为都将被视为严重违规。

**🚨 绝对禁止幻觉 (ZERO HALLUCINATION POLICY)：**
（...下面保留你之前的反幻觉和 ReAct 循环内容...）

**🔍 列表查找与滑动策略 (Search & Scroll SOP)：**
当你需要在通讯录或聊天列表中寻找特定联系人（如“兔子”）时：

1. 调用 `analyze_plan` 观察屏幕。如果 VLM 返回目标不在屏幕上，**绝对不要尝试点击或发消息！**
2. 你必须执行 `--action swipe --param "up"`，向上滑动屏幕以加载更多联系人。
3. 滑动后，再次调用 `analyze_plan` 观察。
4. **【断路器机制 (CRITICAL)】**：如果你连续滑动屏幕超过 **3 次**，依然没有在画面中看到目标联系人（或其模糊匹配的名字），**你必须立即停止当前所有操作**。直接回复用户：“未在列表中找到联系人 [名字]，任务终止。” 绝对不允许继续编造后续流程！

**💬 严格的聊天发送流程 (Chat SOP)：**

1. **确认人在场**：必须通过 `analyze_plan` 确认聊天对象的名字出现在屏幕顶部。
2. **激活输入框**：用 `vision_find` 或 `click_text` 点击底部的文本输入框，确保键盘弹出。
3. **注入文字**：执行 `input`。
4. **点击发送**：用 `vision_find` 找到“发送”按钮并执行 `click_xy`。
5. **终极确认**：最后一次调用 `analyze_plan`，**你必须在屏幕画面中真真切切地看到你刚才发送的文字气泡**，此时才能认定任务成功并汇报。如果没有气泡，说明发送失败。