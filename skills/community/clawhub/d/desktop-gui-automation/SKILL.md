---
name: desktop-gui-automation
description: 用 Python 在 Windows 交互桌面上模拟鼠标键盘，自动化操作任意桌面 GUI 软件（客户端、微信、办公软件等）完成签到、领奖、批量点击、填表等重复任务。This skill should be used when the user asks to automate clicks or repetitive actions in a desktop application, set up a daily GUI task, claim points/check-in automatically, or control a Windows program that has no API. Covers environment setup, template-based element location, idempotency, screenshot evidence, and running scripts in the logged-in session via Windows Task Scheduler to avoid session isolation.
agent_created: true
---

# Desktop GUI Automation（Windows 桌面自动化）

## Overview

在没有 API 的桌面软件里，用截图识别界面 + 模拟鼠标键盘完成重复操作（签到、领积分、批量点击、定时填报）。核心不是"能点"，而是**稳定定位、幂等防重复、全程留证、在能截屏的会话里运行**。

这套方法的真实来源：为 WorkBuddy 客户端搭建每日自动领积分时踩过一整轮坑后沉淀——包括后台会话截屏失败、模板误匹配、按钮三态判断、入口漂移等。

## Critical constraint（必读，决定成败）

**WorkBuddy 的后台自动化会话拿不到交互桌面**：截屏报 `screen grab failed`、激活窗口报 `Error 5 拒绝访问`。所以定时任务**不能**只靠 WorkBuddy automation 自己跑 GUI。

正确架构（二选一，随时间稳定优先选 A）：

- **方案 A（推荐）**：Windows 任务计划程序，触发器设"每天 HH:MM"，主体设"仅在用户登录时运行 + 最高权限"，直接执行 `gui_auto.py` 或业务脚本。登录会话能正常截屏点击。
- **方案 B**：WorkBuddy automation 只做"读日志 + 汇报"，绝不碰 GUI。操作仍由方案 A 的计划任务完成。

判断当前会话能否截屏：运行 `python scripts/gui_auto.py shot`，若生成 PNG 则可用；若抛 OSError 则是隔离会话，必须走方案 A。详见 `references/session-isolation.md`。

## Workflow（做任何 GUI 自动化都按此顺序）

### Step 1 · 只读勘察，绝不先点
先截屏看界面，用 `shot` + `crop` 放大局部，确认目标按钮的**原始像素坐标**。

**关键坑**：读图工具常把截图缩放显示，照预览图估算坐标会整体偏移、全部点空。必须按"裁剪框原始坐标 + 放大倍数"反算：原始 x = crop_x0 + 图上x/倍数。详见 `references/workflow.md`。

### Step 2 · 制作模板，用图像定位而非固定坐标
界面会因窗口状态、对话列表重排而漂移，固定坐标不可靠。用 `locate` 做模板匹配：

```python
python scripts/gui_auto.py locate <模板.png> [--conf 0.82] [--region x,y,w,h]
```

- 模板从**原始像素截图**裁剪，只含按钮本身，去掉圆角和边距。
- confidence 一般 0.8；低于 0.75 时不同按钮会互相误匹配。
- 每次改动后用 `locate` 验证是否稳定命中同一个点。

### Step 3 · 设计幂等，避免重复操作
先判断"今天是否已做过"再决定是否点击。常见信号：
- 按钮变灰 / 文字变"已领取/已兑换/今日已领" → 跳过。
- 计数型（本月已兑 N 次、连续签到天数）→ 达到即跳过。

**坑**：同一"已领"状态可能有多种形态（灰按钮、黑按钮不同文案）。用颜色（灰 vs 黑）+ 多个模板联合判断，别只认一种。

### Step 4 · 编排脚本并留证
基于 `scripts/gui_auto.py` 的工具函数写业务脚本：激活窗口 → 关残留弹窗 → 定位 → 点击 → 等待 → 再截图确认 → 写结构化日志到 `logs/` 与 `checkin-log.md`。只做低风险动作，绝不读/打印账号令牌。

### Step 5 · 挂定时任务
用 `references/task-scheduler.md` 里的 PowerShell 模板创建 Windows 计划任务，**先手动触发一次**验证 `LastTaskResult=0` 且生成了新截图，再交给它每天自动跑。

### Step 6 · 汇报层只读
若需要"每天告诉我结果"，让 WorkBuddy automation 读日志和截图汇报，不碰 GUI，与操作任务错开时间（如操作 9:00、汇报 9:20）。

## Quick start

```bash
# 依赖（装进脚本实际使用的 Python）
python -m pip install pyautogui pillow opencv-python-headless

# 探查
python scripts/gui_auto.py shot
python scripts/gui_auto.py crop <截图.png> x0 y0 x1 y1 <放大倍数>
python scripts/gui_auto.py windows          # 列出窗口标题与位置
python scripts/gui_auto.py locate <模板> --conf 0.82

# 操作
python scripts/gui_auto.py activate "窗口标题"
python scripts/gui_auto.py click X Y
python scripts/gui_auto.py drag X Y1 Y2     # 拖动滚动条

# 完整业务示例见 references/workbuddy-case.md 与 scripts/example_flow.py
```

## Resources

### scripts/
- `gui_auto.py` — 通用工具库/CLI：截屏、局部放大、窗口激活、模板定位、点击、拖动、日志。业务脚本 `import` 它即可复用全部能力。
- `example_flow.py` — 完整业务脚本骨架（打开入口→定位→幂等判断→点击→留证→写日志），按实际软件改写常量与步骤。

### references/
- `workflow.md` — 完整方法论：坐标换算、模板制作、幂等设计、留证与验证清单、常见坑。
- `session-isolation.md` — 为什么后台会话不能操作 GUI，如何诊断与规避。
- `task-scheduler.md` — Windows 任务计划程序的 PowerShell 创建/触发/排查模板（可直接复制）。
- `workbuddy-case.md` — 真实案例：WorkBuddy 每日领 100 积分 + 成长计划兑换，含三态按钮判断和完整踩坑复盘。

### assets/
预留给业务模板图片（按钮截图等），通用场景可为空。
