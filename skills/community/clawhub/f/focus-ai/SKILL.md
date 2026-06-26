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
    requires_user_setup: true
    privacy_note: |
      会定期截屏并发送至用户配置的视觉模型API（如通义千问、豆包等）进行分析。
      视觉模型运行在云端，非本地运行。
      
  - name: query_history
    description: 查询历史专注数据和屏幕活动记录
    condition: "仅在当天使用过 focusAI 时调用"
    
  - name: analyze_activity
    description: 分析特定时间段的工作内容和效率
    condition: "仅在当天使用过 focusAI 时调用"

# 所需凭证（由用户自行配置，Bot 不存储）
credentials:
  - name: cloud_vision_api_key
    description: 云端视觉模型 API 密钥（如通义千问、豆包等）
    provided_by: user
    storage_location: "~/.openclaw/workspace/focusAI/config.json（用户本地文件，Bot 仅检查是否存在，不读取内容）"

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
    
  - pattern: "停止.*监控|结束.*专注|关闭.*focus|不.*监控.*了"
    action: stop_monitor
    
  - pattern: "换.*目标|目标.*改|开始.*做.*|我要.*写|接下来.*做"
    action: update_goal
    
  - pattern: "昨天.*做.*什么|前天.*忙.*啥|上周.*工作|之前.*数据"
    action: query_past_history
    requires_data: true

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

### 启动流程（标准交互）

当用户表达"开始记录今日工作"、"开始专注"等意图时：

**前置检查 - FocusAI 已安装配置？**
```python
def check_focusai_ready():
    """仅检查程序目录是否存在，不读取配置文件内容"""
    program_path = os.path.expanduser("~/.openclaw/workspace/focusAI/start.bat")
    return os.path.exists(program_path)
```
- 如果未安装 → 引导用户先完成安装步骤（包括自行配置 API 凭证）
- **注意**：API 密钥由用户在本地 `config.json` 中配置，Bot 不读取、不传输该文件内容

**Step 1 - Bot 主动询问**
> "可以使用 FocusAI 来辅助监控你的工作状态。需要启动吗？
> - **后台静默** - 只在后台记录，无界面干扰
> - **唤起 UI** - 打开可视化监控面板（窗口置顶）"
> 
> ⚠️ 注意：FocusAI 会将截图发送至你配置的云端视觉模型（消耗API额度）

**Step 2 - 用户选择后，Bot协助启动**
- 用户选择「后台静默」→ Bot 询问用户"是否现在启动 FocusAI？"，获得明确确认后执行启动命令
- 用户选择「唤起 UI」→ Bot 询问用户"是否现在启动 FocusAI？"，获得明确确认后执行启动命令

**Step 3 - 启动命令（用户明确确认后，Bot执行）**
```powershell
# Bot 仅在用户明确说"启动"或"好的"后执行：

# 后台静默启动（最小化）
Start-Process -FilePath "~/.openclaw/workspace/focusAI/start.bat" -WindowStyle Minimized

# 或唤起 UI（正常窗口）
Start-Process -FilePath "~/.openclaw/workspace/focusAI/start.bat"
```

> **操作边界说明**：
> - Bot **不会**自动执行启动命令，必须获得用户明确口头/文字确认
> - Bot **不会**读取用户的 `config.json` 文件内容
> - Bot **不会**传输用户的 API 凭证到任何外部服务器

> ⚠️ 启动前必须确认：
> - 用户已同意隐私条款（截屏、API 调用）
> - 用户已配置 API 凭证

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
- "帮我保持工作时的注意力"
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
| GET | `/focus/score` | 获取当前分数、目标和运行状态 |
| GET | `/history` | 获取程序本次启动以来的所有活动记录 |
| POST | `/start` | 启动监控（可附带 `{"goal": "工作目标"}`） |
| POST | `/stop` | 停止监控 |
| POST | `/config` | 覆写配置（切换模型或截图间隔） |

### 中途修改目标

用户想切换工作内容时，**无需重启**，直接 POST 新目标即可覆盖：

```python
requests.post("http://127.0.0.1:8765/api/start", 
              json={"goal": "写论文 - 文献综述部分"})
```

**Bot 回复示例**：
> "已更新目标为「写论文 - 文献综述部分」。专注分数会基于新目标重新评估。"

### 查询历史日期

支持自然语言解析：

```python
def resolve_date(query):
    """把自然语言解析成 yyMMdd 格式"""
    today = datetime.now()
    if "昨天" in query: 
        return (today - timedelta(1)).strftime('%y%m%d')
    if "前天" in query: 
        return (today - timedelta(2)).strftime('%y%m%d')
    # 支持「上周三」「3月5号」等扩展...
```

**Bot 回复示例（无数据时）**：
> "昨天没有使用 FocusAI，暂无数据。需要我帮你启动今天的监控吗？"

### 数据存储位置

| 类型 | 路径 | 说明 |
|------|------|------|
| **数据文件** | `~/Desktop/FocusOS_Data/` | 截图 + CSV 报告，按日期分文件夹（如 `260310/`） |
| **程序本体** | 用户自选克隆路径 | 推荐 `~/.openclaw/workspace/focusAI/` 或 `~/projects/focusAI/` |
| **配置文件** | 程序目录下的 `config.json` | 运行时自动生成，可手动修改 |

> **注意**：除了截图和 CSV，FocusAI 不会在本地生成其他持久化文件。

### 服务异常处理

当 API 无响应时的处理流程：

```python
def check_service():
    try:
        r = requests.get("http://127.0.0.1:8765/api/focus/score", timeout=3)
        return r.ok
    except:
        return False

def handle_exception():
    if not is_process_running("focusAI"):
        return "FocusAI 似乎没有运行。需要我帮你启动吗？"
    else:
        return "服务似乎卡住了，建议重启。要我现在关掉重新启动吗？"
```

### 后台监控的主动提醒

当用户选择**后台静默模式**时，Clawbot 需在对话中通过提醒策略让用户知道运行中的事实：

- **首次启动后 5 分钟**：轻量确认「FocusAI 正在后台记录你的工作状态」
- **运行时间过长（>1.5h）**：用户可能忘了监控还在运行，及时提醒
  > "已经专注 1.5 小时了，还在后台记录着。需要休息一下吗？"

### 提醒策略示例

| 场景 | 语气示例 |
|------|----------|
| 短暂分心 | "嘿，回来一下～" |
| 持续偏离（>10min） | "你已经刷了 10 分钟微博了，那个报告还在等你。" |
| 运行超 1.5h（后台模式） | "专注 1.5 小时了，还在后台记录着。要停了吗？" |
| 目标完成 | "专注 45 分钟，不错。要休息一下还是继续？" |

### 长期记忆检索 (RAG 架构)

**检索工作流：**

1. **宏观概览** (省 Token)
   - 读取对应日期的 `report_*.csv`
   - 生成全天活动线图

2. **微观溯源** (按需触发)
   - 根据 CSV 时间戳，找到对应 `YYYYMMDD_HHMMSS.jpg`
   - 调用视觉模型进行 OCR 和内容分析

---

## 🛠️ 初始化与安装

### 前置要求

FocusAI 需要用户自行配置**云端视觉模型API凭证**（如通义千问、豆包等）。
- 视觉模型运行在**云端**，非本地运行
- API key 由用户在本地配置文件中提供，Bot 不接触、不传输用户凭证

### 安装步骤（用户自行完成）

**Bot 不执行安装，仅提供指引。所有以下步骤由用户手动完成：**

如果用户要求使用记忆/监控功能，但检测到本地未部署 FocusAI：

1. **Bot 先解释用途和风险**
   - 本地截屏 + 云端视觉模型分析
   - 截图和API调用会消耗Token/额度
   - 代码开源在 `https://github.com/HR2AY/focusAI`，建议用户审查后使用

2. **Bot 明确征求用户同意**

3. **Bot 提供安装指引**（用户自行执行）：

```bash
# === 用户自行执行以下步骤 ===

# 1. 克隆仓库到本地（用户自选路径）
git clone https://github.com/HR2AY/focusAI ~/.openclaw/workspace/focusAI

# 2. 编辑配置文件，填入你的API凭证
#    Bot 不会读取此文件内容，仅由 FocusAI 程序本身读取
code ~/.openclaw/workspace/focusAI/config.json
# 配置项示例：
# {
#   "api_key": "YOUR_API_KEY_HERE",
#   "model_provider": "dashscope",
#   "model_name": "qwen-vl-max"
# }

# 3. Windows 运行 start.bat 启动服务
cd ~/.openclaw/workspace/focusAI && start.bat
```

> **安全与隐私声明**：
> | 项目 | 说明 |
> |------|------|
> | **安装** | 由用户手动执行，Bot 不自动运行任何安装命令 |
> | **API 凭证** | 用户自行配置在本地 `config.json`，Bot **不读取、不传输**该文件内容 |
> | **截图数据** | 存储在用户本地 `~/Desktop/FocusOS_Data/`，Bot 仅在用户查询时读取已生成的 CSV/图片 |
> | **程序控制** | Bot 仅在用户明确同意后，通过 HTTP API 或启动命令与本地服务交互 |

---

## ⚡ 交互原则

| 场景 | 行为 |
|------|------|
| 状态极佳 (Score 持续上升) | 不要主动打断 |
| 长时间偏离目标 | 用幽默但严厉的语气提醒 |
| 当日无数据 | 明确告知，引导用户启动监控 |

---
