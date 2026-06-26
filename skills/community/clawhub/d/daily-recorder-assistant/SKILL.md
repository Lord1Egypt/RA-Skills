---
name: daily-recorder-assistant
description: 每日状态记录与复盘助手。触发词：早反馈/morning query（晨间问询）, 晚复盘/evening review（晚间总结）。支持能量评分、明日规划、当日分析和周期总结。自动识别频道（feishu/telegram/signal/discord），按 User ID 隔离状态数据。
---

# Daily Record Assistant - 每日状态记录与复盘助手

**触发词**:

- **晨间问询**: `早反馈`, `morning query`
- **晚间复盘**: `晚复盘`, `evening review`
- **状态查询**: `状态查询`, `status query`

**v2.0 核心改进 - 混合触发机制**:

### 🎯 **双模式并存**:

#### 1️⃣ **严格模式 (推荐)**: 使用明确指令
- `记录早反馈` / `记录一下早反馈` → 晨间记录
- `记录今日复盘` / `记录一下晚复盘` → 晚间复盘
- `补充记录` / `追加信息` → 附录模式

#### 2️⃣ **智能推断模式**: 基于时间自动识别
**标准时段内**:
- 🌅 **早晨 (6:00-12:00)**: 说"能量 X"或"今日能量 5" → 自动识别为早反馈
- 🌙 **傍晚 (18:00-23:59)**: 说"能量 X"或"完成度 X%" → 自动识别为晚复盘

**非标准时段**: 
⚠️ 系统会提示用户澄清，要求使用明确触发词。

### ⚠️ **错误处理规则**:
- ❌ **无触发词 + 非标准时段**: "今日能量 5" (下午 14:00) → **拒绝执行** + 提示用户澄清
- ✅ **有触发词**: "记录早反馈。今日能量 5" → **执行记录**
- ✅ **智能推断**: "能量 X" (早晨/傍晚时段) → **自动判断早晚并记录**

**自动识别频道**: feishu, telegram, signal, discord 等（状态按 User ID 隔离）

---

## ⚠️ 依赖声明（必需环境）

**本技能运行所需的关键依赖：**

| 类型               | 项目                      | 说明                                                                 |
| ------------------ | ------------------------- | -------------------------------------------------------------------- |
| **Python Runtime** | Python 3.x (≥3.8)         | 所有脚本基于 Python 3 开发，使用标准库 `os`, `subprocess`, `json` 等 |
| **External CLI**   | OpenClaw CLI (`openclaw`) | 用于配置定时任务（`setup_cron.py`调用）                              |
| **Workspace**      | ~/.openclaw/workspace/    | 可写目录，存储脚本、状态文件、笔记                                   |

**依赖检查命令：**

```bash
# 1. Python 版本
python3 --version

# 2. OpenClaw CLI 可用性
openclaw --version && openclaw gateway status

# 3. Workspace 权限
ls -ld ~/.openclaw/workspace
```

**常见错误处理：**

- `command not found: openclaw` → CLI 未安装或未加入 PATH
- `Permission denied` → ~/.openclaw/workspace/ 无写权限，需 `chmod`
- `ModuleNotFoundError` → Python 环境不完整，检查 pip install

---

## 🚀 快速开始

### 🔍 依赖检查（执行前必读）

在运行任何脚本前，请确认 OpenClaw CLI 可用：

```bash
openclaw --version && openclaw gateway status
```

若 `openclaw` 命令不可用：

1. 确保 OpenClaw 已正确安装到系统 PATH
2. 启动 Gateway 服务：`openclaw gateway start`
3. 验证：`openclaw cron list`（应返回空或已有任务列表）

### 1️⃣ 初始化（首次使用）

```bash
python3 scripts/init_cycle.py
```

- ✅ 创建基础目录结构（`notes/daily-recorder/`）
- ✅ 建立状态文件 `state.json`
- ✅ 生成首周 Day 1 初始笔记
- ⚠️ 需要授权当前会话为目标交互窗口

### 2️⃣ 配置定时任务

```bash
python3 scripts/setup_cron.py --mode=openclaw
```

**默认时间表**:

- 晨间问询：每日 **8:00 AM** (`0 8 * * * @ Asia/Shanghai`) → 触发词 `早反馈`
- 晚间复盘：每日 **6 PM** (`0 18 * * * @ Asia/Shanghai`) → 触发词 `晚复盘`

### 3️⃣ 手动触发（对话模式）

在对话中直接发送关键词，AI 会自动调用对应脚本：

| 功能         | 触发词                     | 自动调用脚本                                        |
| ------------ | -------------------------- | --------------------------------------------------- |
| **晨间问询** | `早反馈`, `morning query`  | `scripts/daily_query.py --time-period morning`      |
| **晚间复盘** | `晚复盘`, `evening review` | `scripts/daily_query.py --time-period evening`      |
| **状态查询** | `状态查询`, `status query` | `scripts/daily_query.py --time-period status_query` |
| **反馈记录** | 用户直接回复能量/任务信息  | `scripts/daily_query.py --mode=record_feedback`     |

#### 【优化】自动记录用户反馈流程

当用户在晨间/晚间问询后，**直接给出反馈内容**时，系统会自动：

1. **解析用户输入** → 提取能量评分、精神状态、任务列表等关键字段
2. **生成结构化笔记** → 写入 `notes/daily-recorder/YYYY-MM-DD-day_N.md`
3. **更新状态计数** → `state.json` 中 `total_records` +1

**示例交互**:

```
AI: 早上好！周日晚计划是今天进行 [任务名称]。昨天休息得怎么样呀（评分待评估）？
用户：今日能量 5。精神疲劳。1. 开启自媒体职业计划 2. AI 输出文案
系统：✓ 反馈已成功记录 → 生成笔记文件 ✓ state.json 已更新
```

**自动提取规则**:
| 字段 | 匹配模式 | 默认值 |
|------|---------|--------|
| **能量评分** | `能量 N`, `N/10` | 待评估 |
| **精神状态** | `疲劳`, `累`, `充沛`, `清醒` | 根据关键词推断 readiness |
| **任务列表** | `1. ...`, `2. ...` (最多前 3 项) | 无 |
| **阻碍问题** | `AI`, `耗时`, `卡点` + 关键词组合 | 自动归类 |

> 💡 **优势**: 用户无需手动调用脚本，只需自然回复，系统自动完成记录。

---

## 📚 核心配置文件说明

### ⚙️ `config.py` - 全局配置模块（所有脚本共享）

**功能**:

- **路径计算**: 动态计算 WORKSPACE_BASE, CURRENT_SKILL_PATH, NOTE_BASE_DIR 等关键路径
- **统一配置**: 避免跨脚本重复定义，支持多系统/多用户部署
- **资源映射**: 提供 `get_reference_dir_path()`, `get_assets_dir_path()` 等工具函数
- **模板路径**: `get_template_file_path()` 动态获取特定模板文件路径

**被所有脚本引用**:

```python
from config import (
    WORKSPACE_BASE,           # ~/.openclaw
    SKILL_NAME,               # "daily-recorder-assistant"
    CURRENT_SKILL_PATH,       # 技能目录路径
    NOTE_BASE_DIR,            # notes/基础目录
    DAILY_RECORDER_SUBDIR,    # daily-recorder/
    PLAN_SUBDIR,              # plans/
    REFERENCE_DIR,            # references/目录
    ASSETS_DIR,               # assets/目录
)
```

**关键路径定义**:
| 变量 | 值示例 | 用途 |
|-----|--------|------|
| `WORKSPACE_BASE` | `~/.openclaw` | OpenClaw 工作空间根目录 |
| `CURRENT_SKILL_PATH` | `~/.openclaw/workspace/skills/daily-recorder-assistant` | 技能目录 |
| `NOTE_BASE_DIR` | `~/.openclaw/workspace/notes` | Obsidian notes 基础目录 |
| `DAILY_RECORDER_SUBDIR` | `daily-recorder` | 每日记录子目录 |
| `PLAN_SUBDIR` | `plans` | 计划子目录 |

**使用场景**:

- ✅ **所有脚本启动时**: 自动导入 `config.py` 获取路径配置
- ✅ **跨系统部署**: 通过环境变量动态计算路径，无需硬编码
- ✅ **模板文件访问**: 通过 `get_template_file_path(template_name)` 获取 notes-template.md, plan-template.md 等

---

## 📋 完整脚本使用指南

### 🔧 `init_cycle.py` - 初始化周期结构

**功能**:

- 创建基础目录结构（`notes/daily-recorder/`）
- 生成首周 Day 1 初始笔记
- 建立状态文件与周期计数器
- 支持多频道 UserID 映射

**触发方式**:

```bash
# 手动初始化
python3 scripts/init_cycle.py
```

**输出示例**:

```
✓ 已创建初始笔记：~/.openclaw/workspace/notes/daily-recorder/2026-04-12-day_1.md
✓ 第 1 周期初始化完成
当前频道 feishu: 目标会话 DM（userid: ou_0def59b2...）
```

---

### 📝 `daily_query.py` - 晨间/晚间问询核心脚本

**功能**:

- 读取昨日记录获取关键信息（能量评分、计划内容）
- 根据周 Day + 周期数选择对应模板
- 注入变量生成个性化问询文本

**触发方式**:

```bash
# 晨间问询
python3 scripts/daily_query.py --time-period morning [--mode=manual]

# 晚间复盘
python3 scripts/daily_query.py --time-period evening [--mode=manual]

# 状态查询（特殊模式）
python3 scripts/daily_query.py --time-period status_query
```

**参数说明**:

- `--time-period`: `morning` | `evening` | `status_query`
- `--user-message=...`: 用户消息（用于语言检测）
- `--channel=feishu`: 当前频道（OpenClaw metadata 自动传入）

**模板选择逻辑**:
| 周 Day | 晨间模板 | 晚间模板 |
|-------|---------|---------|
| Monday (1) | `Monday Morning Template` | `Monday Evening Template` |
| Tuesday (2) | `Tuesday Morning Template` | `Tuesday Evening Template` |
| ... | ... | ... |
| Friday (5) | `Friday Morning Template (收尾鼓励式)` | `Friday Evening Template` |

**第 1 周期 vs N+1 周期**:

- **第 1 周期**: 使用标准模板，能量评分显示"待评估"
- **N≥2 周期**: Monday 使用 `Data-Driven Morning Template`,基于历史数据分析

---

### ✍️ `record_feedback.py` - 记录用户反馈到笔记

**功能**:

- 读取模板生成结构化笔记
- 接收用户输入（完成率、能量评分、问题描述）
- 写入完整笔记到 `notes/daily-recorder/`目录

**触发方式**:

```bash
python3 scripts/record_feedback.py --input '{"energy":4,"completion":80}'
```

**手动操作**（对话模式）:

1. AI 输出问询模板后，用户直接回复：
   - 能量评分：`4`
   - 完成率：`文案生成 [80%]`, `润色优化 [50%]`
   - 问题点：`AI 生成质量不稳定`
2. AI 调用脚本生成笔记

**输入字段**:

```json
{
  "early_feedback": { "energy": 4, "readiness": "可以开始" },
  "completion_rates": { "文案生成": 80, "润色优化": 50 },
  "energy_score": 3,
  "barriers": ["AI 生成质量不稳定"],
  "next_day_plan_ideas": "明天继续完善文案结构"
}
```

**输出示例**:

```
✓ 笔记已写入：~/.openclaw/workspace/notes/daily-recorder/2026-04-12-day_1.md
```

---

### 📋 `plan_next_day.py` - 规划次日计划

**功能**:

- **人工模式 (第 1 周期)**: 仅记录用户输入的计划
- **智能模式 (N≥2 周期)**: 基于历史数据生成优化建议

**触发方式**:

```bash
# 人工模式（推荐）
python3 scripts/plan_next_day.py --mode=manual \
  --input '{"tasks":[{"name":"大纲 AI 生成","goal":"完成 5000 字初稿"}]}'

# 智能模式（需至少 2 周期数据）
python3 scripts/plan_next_day.py --mode=smart \
  --history-data '{"task_adaptation":[...],"risk_alerts":[...]}'
```

**参数说明**:

- `--mode=manual`: 人工规划，需提供用户输入
- `--mode=smart`: 智能进化（需历史数据分析）

**输出示例 (智能模式)**:

```
=== 第 3 周期 - 智能进化模式 ===
## 今日核心任务

### 1. 大纲 AI 生成
- **优先级**: 高
- **时间窗建议**: 09:00-11:00（历史效率最高）

**风险预警**:
- AI 生成质量不稳定 → 应对策略：准备备选方案 / 降低单次字数要求
```

---

### 📊 `analyze_day.py` - 今日分析报告

**功能**:

- 读取今日交互笔记提取关键指标
- 计算完成率、能量状态、问题点、计划偏差度
- 输出结构化分析报告

**触发方式**:

```bash
python3 scripts/analyze_day.py
```

**分析维度**:
| 维度 | 说明 |
|-----|------|
| **完成率** | 各任务完成百分比 + 平均完成率 |
| **能量状态** | 评分 [1-5] → "极累"/"疲惫"/"正常"/"充沛"/"满电" |
| **问题点识别** | 列出所有记录的问题（如 AI 故障、时间冲突） |
| **计划偏差度** | 原计划 vs 实际执行对比，估算偏差百分比 |

**输出示例**:

```
============================================================
=== 今日分析报告 ===
日期：2026-04-12
============================================================

【完成率分析】
  文案生成: [80%]
  润色优化: [50%]
  平均完成率：[65.0%]
  状态：中等完成度 ⚠️

【能量状态】
  评分：3
  解读：正常

【问题点识别】
  - AI 生成质量不稳定

【计划偏差度】
  原计划：完成大纲初稿
  实际执行：完成大纲初稿 + 部分润色
  偏差度：[15%]
  状态：额外插入任务 ⚠️
============================================================
```

---

### 📈 `analyze_cycle.py` - 7 天周期分析

**功能**:

- 读取完整一周（7 天）的交互记录
- 统计完成率趋势、能量模式识别、障碍类型分布
- 生成第 N+1 周期的优化计划建议

**触发方式**:

```bash
python3 scripts/analyze_cycle.py
```

**前置条件**: ⚠️ **需至少完整 7 天记录**

**分析维度**:
| 维度 | 说明 |
|-----|------|
| **完成率趋势** | 7 天平均完成率 + 每日波动 |
| **能量模式** | 各周 Day 平均能量，识别高效时段 |
| **障碍类型分布** | 技术阻碍/时间分配/疲劳累积/计划偏差统计 |
| **风险预警** | 基于历史问题生成预案建议 |

**输出示例**:

```
============================================================
=== 周期总结与智能规划报告 ===
============================================================

【本周期汇总】
 本周期平均完成率：[72.5%] (中等完成度 ⚠️)
 本周期平均能量状态：[3.2] (正常)

【模式识别】
 主要障碍类型分布：[('技术阻碍', 4), ('时间分配', 2)]

【第 4 周期建议】
 - [风险预警]: 建议预设预案应对 AI 生成质量问题
============================================================
```

---

### ⏰ `setup_cron.py` - Cron 配置脚本

**功能**:

- **OpenClaw cron add CLI 模式**: 创建定时任务

**触发方式**:

```bash
# OpenClaw cron add CLI (推荐)
python3 scripts/setup_cron.py --mode=openclaw
```

**OpenClaw cron add CLI 模式**:

- ✅ 自动检测当前频道和 User ID
- ✅ 自动生成安装命令
- ⚠️ **安全设计**: 检测到旧任务时仅提醒，不强制删除（避免误操作）
- 🔒 **依赖检查**: 执行前确保 `openclaw` CLI 可用（参见上方"依赖声明"章节）

**常见错误处理**:
| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `command not found: openclaw` | CLI 未安装或未加入 PATH | 重新安装 OpenClaw 或检查 PATH |
| `permission denied` | 权限不足 | 使用 `sudo` 或联系管理员 |
| `connection refused` | Gateway 服务未运行 | 执行 `openclaw gateway start` |

---

## 🔄 Cron vs 手动触发对比

| 维度         | Cron 定时模式                | 手动对话模式                  |
| ------------ | ---------------------------- | ----------------------------- |
| **触发方式** | OpenClaw daemon              | 用户消息（`早反馈`/`晚复盘`） |
| **执行脚本** | `daily_query.py --mode=cron` | `daily_query.py` (自动检测)   |
| **输出风格** | 纯文本，无前缀说明           | 标准格式，包含上下文          |
| **日志记录** | `~/daily-recorder-cron.log`  | 实时返回到对话界面            |
| **适用场景** | 日常自动提醒                 | 临时/调试/补充/查询           |

---

## 📁 文件结构

```
daily-recorder-assistant/
├── SKILL.md                    # 本文件（核心流程）
├── scripts/
│   ├── config.py              # ⚙️ 全局配置模块（所有脚本共享）
│   ├── init_cycle.py          # 周期初始化脚本
│   ├── daily_query.py         # 问询/复盘核心逻辑
│   ├── record_feedback.py     # 状态记录脚本
│   ├── plan_next_day.py       # 明日规划脚本
│   ├── analyze_day.py         # 今日分析脚本
│   └── setup_cron.py          # Cron 配置脚本
├── references/                # 参考文档（按需加载）
│   ├── interaction-templates-zh.md    # 中文问询模板完整版
│   └── interaction-templates-en-full.md # 英文问询模板完整版
├── assets/                    # 模板文件（脚本直接引用）
│   ├── notes-template.md      # 状态记录模板
│   └── plan-template.md       # 明日规划模板
└── state.json                 # 运行时状态（不纳入 Git）
```

> **注意**:
>
> - `state.json` 是运行时文件，**不应提交到 Git**。建议 `.gitignore`中添加`state.json`。
> - 参考文档按需加载：脚本执行失败时检查 `references/`目录是否完整。

---

## 🐛 故障排查

| 问题               | 解决方案                                                    |
| ------------------ | ----------------------------------------------------------- |
| **状态文件丢失**   | `python3 scripts/init_cycle.py` 重新初始化                  |
| **模板加载失败**   | 检查 `references/`目录是否包含`interaction-templates-zh.md` |
| **今日笔记不存在** | 先执行 `record_feedback.py`或对话模式补充记录               |

### 🔧 OpenClaw CLI 依赖问题

若遇到与 cron 配置相关的错误，请先检查：

```bash
# 1. 验证 CLI 是否可用
openclaw --version

# 2. 检查 Gateway 服务状态
openclaw gateway status

# 3. 启动 Gateway（如未运行）
openclaw gateway start
```

**依赖说明**: `setup_cron.py`通过 `subprocess.run()` 调用 `openclaw CLI`,若该命令不可用将导致脚本失败。

---

**维护**: 此文档由 `daily-recorder-assistant` 技能维护
