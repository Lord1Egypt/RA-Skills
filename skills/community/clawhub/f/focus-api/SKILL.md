# FocusAI - 视觉记忆中枢与上下文管理器

## YAML 定义 (技能元数据)

```yaml
name: focusai
version: 1.0.0
description: 本地视觉监控与专注力管理工具，提供屏幕活动记录、专注度评分和历史追溯能力
author: HR2AY
license: MIT

# 技能能力声明
capabilities:
  - name: monitor_focus
    description: 监控用户屏幕活动并评估专注度
    requires_user_consent: true
    privacy_note: 会定期截屏并上传至视觉模型分析
    
  - name: query_history
    description: 查询历史专注数据和屏幕活动记录
    condition: "仅在当天使用过 focusAI 时调用"
    
  - name: analyze_activity
    description: 分析特定时间段的工作内容和效率
    condition: "仅在当天使用过 focusAI 时调用"

# 触发意图
intents:
  - pattern: "我今天.*忙.*什么|总结.*工作流|今天都干了.*"
    action: query_history
    requires_data: true
    
  - pattern: "下午.*点.*看.*PDF|刚才.*看.*什么|之前.*窗口.*内容"
    action: analyze_activity
    requires_data: true
    
  - pattern: "效率.*低|时间.*花在哪|分心.*多久"
    action: query_history
    requires_data: true
    
  - pattern: "打开.*专注.*模式|开始.*监控|监控.*写代码"
    action: start_monitor
    requires_consent: true
    
  - pattern: "刚才.*分心.*|现在.*专注.*|当前.*状态"
    action: check_status
    
  - pattern: "切换.*模型|改成.*豆包|改成.*通义|换成.*GPT"
    action: switch_provider

# 调用前提条件
prerequisites:
  check_command: |
    $today = Get-Date -Format 'yyMMdd'
    Test-Path "~/Desktop/FocusOS_Data/$today/*.csv"
  skip_if_false: |
    今天还没有使用过 FocusAI，暂无数据可供查询。
    如需开始监控，请说"打开专注模式"或运行 start.bat。
```

---

##  技能定位

不要将 FocusAI 仅仅视为一个"计时器"。它是你的**视觉记忆中枢和上下文管理器**。

当用户询问他们过去的数字活动、工作状态、或者需要你回忆某一时段的屏幕内容时，FocusAI 就是你的"眼睛"和"日记本"。

### 重要约束

**当日未使用时不调用**

如果当天没有使用过 FocusAI（即没有数据文件），**不要尝试调用或分析**。直接告知用户：
> "今天还没有使用过 FocusAI，暂无数据可供查询。如需开始监控，请说'打开专注模式'或运行 start.bat。"

### 隐私与权限

| 场景 | 要求 |
|------|------|
| 后台监控 | 必须告知用户截屏行为、内存和 API 使用情况 |
| 前端 GUI | 启动前需询问用户，告知 UI 会置顶，需在任务栏关闭 |

---

## 🗣️ 唤醒触发词

当用户的意图匹配以下自然语言时，你应立刻意识到需要调用 FocusAI：

### 查询类 (需当日有数据)
- "我今天一天都在忙些什么？总结一下我的工作流。"
- "我下午两点左右看的那篇 PDF 主要是关于什么的？"
- "我感觉今天效率很低，帮我分析一下我把时间都花在哪了。"
- "我刚才是不是分心了？"

### 控制类
- "打开专注模式，监控我接下来的写代码状态。"
- "把我的视觉监控模型切换成豆包/通义千问。"

---

## 📖 Agent 操作指南

### 前置检查 (必须)

在尝试查询历史或分析活动前，先检查今日是否有数据：

```python
import os
from datetime import datetime

def has_today_data():
    today = datetime.now().strftime('%y%m%d')
    data_dir = os.path.expanduser(f'~/Desktop/FocusOS_Data/{today}')
    return os.path.exists(data_dir) and any(f.endswith('.csv') for f in os.listdir(data_dir))
```

如果返回 `False`，**立即停止**，不要尝试调用 API 或读取文件。

### 实时控制与状态获取 (HTTP API)

Base URL: `http://127.0.0.1:8765/api`

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/status` | 获取当前分数、目标和运行状态 |
| GET | `/history` | 获取程序本次启动以来的所有活动记录 |
| POST | `/start` | 启动监控（可附带 `{"goal": "工作目标"}`） |
| POST | `/stop` | 停止监控 |
| POST | `/config` | 覆写配置（切换模型或截图间隔） |

### 长期记忆检索 (RAG 架构)

数据默认位于 `~/Desktop/FocusOS_Data/`，按日期归档（如 `260310/`）。

**检索工作流：**

1. **宏观概览** (省 Token)
   - 读取对应日期的 `report_*.csv`
   - 生成全天活动线图

2. **微观溯源** (按需触发)
   - 根据 CSV 时间戳，找到对应 `YYYYMMDD_HHMMSS.jpg`
   - 调用视觉模型进行 OCR 和内容分析

---

## 🛠️ 初始化与安装

如果用户要求使用记忆/监控功能，但检测到本地未部署 FocusAI：

1. **先解释用途**（本地截屏+视觉模型分析）
2. **明确征求用户同意**
3. 然后执行：

```bash
# 克隆仓库
git clone https://github.com/HR2AY/focusAI

# Windows 运行 start.bat 自动配置环境并启动服务
cd focusAI && start.bat
```

---

## ⚡ 交互原则

| 场景 | 行为 |
|------|------|
| 状态极佳 (Score 持续上升) | 不要主动打断 |
| 长时间偏离目标 | 用幽默但严厉的语气提醒 |
| 当日无数据 | 明确告知，引导用户启动监控 |

---

*详细安装教程和 API 调用方法见 references/ 目录*
