---
name: experience-summary-sys
description: 管理经验总结系统：定时生成每日/每周/每月/每季度/每年经验总结，以及按需调用历史经验的功能
metadata: {"openclaw": {"emoji": "📝", "always": true}}
---

# experience-summary-sys

> ⚠️ **本技能为"指导型"技能**，安装后需要按照以下步骤手动配置才能生效。
>
> **标签**: memory, cron, automation, 经验总结

管理经验总结系统：包括定时生成每日/每周/每月/每季度/每年经验总结，以及按需调用历史经验的功能。

---

## 🚀 5分钟快速开始

如果你只想快速配置好这个系统，按以下 3 步操作即可：

### 步骤 1：创建记忆目录

```bash
mkdir -p memory/daily memory/weekly
```

### 步骤 2：创建定时任务

复制以下命令一次性创建所有定时任务：

```bash
# 每日总结（每天北京时间 00:01）
openclaw cron add --name daily-summary --cron "1 0 * * *" --tz "Asia/Shanghai" --description "每天总结前一天对话" --system-event "generate-daily-summary"

# 每周总结（每周一北京时间 00:30）
openclaw cron add --name weekly-summary --cron "30 0 * * 1" --tz "Asia/Shanghai" --description "每周一总结上一周经验" --system-event "generate-weekly-summary"

# 每月总结（每月1日北京时间 01:30）
openclaw cron add --name monthly-summary --cron "30 1 1 * *" --tz "Asia/Shanghai" --description "每月1日总结上一月经验" --system-event "generate-monthly-summary"

# 每季度总结（每季度第一天北京时间 02:30）
openclaw cron add --name quarterly-summary --cron "30 2 1 1,4,7,10 *" --tz "Asia/Shanghai" --description "每季度第一天总结上一季度" --system-event "generate-quarterly-summary"

# 年度总结（每年1月1日北京时间 03:30）
openclaw cron add --name yearly-summary --cron "30 3 1 1 *" --tz "Asia/Shanghai" --description "每年1月1日总结上一年度" --system-event "generate-yearly-summary"
```

### 步骤 3：验证配置

```bash
openclaw cron list
```

看到 5 个任务列表就表示配置成功啦！✅

---

> 📖 **详细说明** 如果你想了解更多细节，请继续往下看。

---

## 📖 详细配置说明

### 功能概述

本技能提供两个核心能力：

1. **定时经验总结** — 自动生成周期性经验总结
2. **按需调用** — 在对话中智能检索并引用历史经验

---

### 第一步：创建记忆目录

在开始之前，需要创建用于存放经验总结的目录：

```bash
# 在 workspace 目录下创建
mkdir -p memory/daily memory/weekly memory/manual
```

或者手动在 `C:\Users\Admin\.openclaw\workspace\` 下创建：
- `memory/daily/` — 存放每日总结（自动生成）
- `memory/weekly/` — 存放每周总结（自动生成）
- `memory/manual/` — 存放手动记录的日志

> 📌 **提示**：手动记录的日志不会被自动任务覆盖，适合记录重要事项或临时笔记。

---

### 第二步：创建定时任务

执行以下命令创建定时任务（使用正确的参数格式）：

#### 每日总结（每天北京时间 00:01 执行）

> ⚠️ **重要**：每日总结现在会同时处理**正常会话**和**被删除/重置的会话**！

**处理逻辑**：
1. 读取 `sessions/` 目录下所有 `.jsonl` 文件
2. **正常会话**：读取修改时间为前一天的普通 .jsonl 文件
3. **被删除/重置会话**：读取文件名包含 `.jsonl.reset.*` 或 `.jsonl.deleted.*` 且时间戳在前一天的
4. 统一解析，标记来源类型
5. 合并写入 `memory/daily/YYYY-MM-DD.md`

**容错处理**：
- 如果当天没有任何会话，仍生成"今日无对话"占位文件
- 确保 weekly-summary 始终有数据可读

```bash
openclaw cron add \
  --name daily-summary \
  --cron "0 1 * * *" \
  --tz "Asia/Shanghai" \
  --description "每天总结前一天对话（含被删除/重置的会话）" \
  --system-event "generate-daily-summary"
```

#### 每周总结（每周一北京时间 00:30 执行）

**处理逻辑**：
1. 读取 `memory/daily/` 目录下上一周的 .md 文件
2. 按日期排序，去重凝练
3. 写入 `memory/weekly/YYYY-WXX.md`

**容错处理**：
- 如果上一周没有任何 daily 文件，仍生成"本周无对话"占位文件

```bash
openclaw cron add \
  --name weekly-summary \
  --cron "30 0 * * 1" \
  --tz "Asia/Shanghai" \
  --description "每周一总结上一周经验" \
  --system-event "generate-weekly-summary"
```

#### 每月总结（每月1日北京时间 01:30 执行）

> 📌 **输出到 MEMORY.md**，格式：`## 📊 YYYY年MM月经验总结`

**处理逻辑**：
1. 读取 `memory/weekly/` 目录下上一月的周总结文件
2. 去重凝练，提取核心经验
3. 追加到 `MEMORY.md` 文件末尾

**容错处理**：
- 如果上一月没有任何 weekly 文件，仍生成"本月无对话"记录

```bash
openclaw cron add \
  --name monthly-summary \
  --cron "30 0 1 * *" \
  --tz "Asia/Shanghai" \
  --description "每月1日总结上一月经验" \
  --system-event "generate-monthly-summary"
```

#### 每季度总结（每季度第一天北京时间 02:30 执行）

> 📌 **输出到 MEMORY.md**，格式：`## 📊 YYYY年QN季度经验总结`

**处理逻辑**：
1. 从 MEMORY.md 中提取上一季度的月总结章节
2. 凝练季度核心成果
3. 追加到 `MEMORY.md` 文件末尾

```bash
openclaw cron add \
  --name quarterly-summary \
  --cron "30 0 1 1,4,7,10 *" \
  --tz "Asia/Shanghai" \
  --description "每季度第一天总结上一季度" \
  --system-event "generate-quarterly-summary"
```

#### 年度总结（每年1月1日北京时间 03:30 执行）

> 📌 **输出到 MEMORY.md**，格式：`## 🏆 YYYY年度经验总结`

**处理逻辑**：
1. 从 MEMORY.md 中提取上一年度的季度总结章节
2. 凝练年度核心成果
3. 追加到 `MEMORY.md` 文件末尾

**额外功能**：
- 可附带执行 sessions 目录清理，删除 90 天前的被删除/重置会话文件

```bash
openclaw cron add \
  --name yearly-summary \
  --cron "30 0 1 1 *" \
  --tz "Asia/Shanghai" \
  --description "每年1月1日总结上一年度" \
  --system-event "generate-yearly-summary"
```

#### 查看和管理定时任务

```bash
# 查看所有任务
openclaw cron list

# 查看特定任务详情
openclaw cron runs <jobId>

# 禁用任务
openclaw cron update <jobId> --disabled

# 启用任务
openclaw cron update <jobId> --disabled=false

# 立即执行
openclaw cron run <jobId>
```

---

### 第三步：修改 AGENTS.md 添加调用规则

编辑 `AGENTS.md` 文件，在 `### 📝 Write It Down` 章节之后添加：

```markdown
### 🔍 按需调用历史经验

当用户提问涉及历史对话、之前解决的问题或之前的经验总结时，你应该主动检索相关经验。

**触发条件（满足任一即触发）：**

- 用户提到"之前"、"上次"、"以前"、"那个"
- 用户提到具体日期或时间范围（如"上周"、"昨天"）
- 用户请求查看"之前的经验"、"之前的总结"
- 当前问题与近期解决的问题相似

**检索范围：**

- `memory/daily/` — 近 7 天的每日总结
- `memory/weekly/` — 近 4-5 周的周经验总结
- `MEMORY.md` — 全部长期记忆

**调用方式：**

1. 使用 `memory_search` 工具检索相关内容
2. 根据相关性筛选（相似度 > 0.5）
3. 将找到的相关经验融入回答，格式如：
   > 💡 根据之前的经验：...
4. 每次最多引用 2-3 条相关经验，避免信息过载

**不触发的情况：**

- 用户只是日常寒暄
- 问题明显是新话题，与历史无关
- 已有上下文已包含所需信息
```

#### 检索范围与权重

| 来源 | 时间范围 | 权重 |
|------|----------|------|
| memory/daily/ | 近 7 天 | 时间越近权重越高 |
| memory/weekly/ | 近 4-5 周 | 已凝练，权重较高 |
| MEMORY.md | 全部 | 精选内容，最可靠 |

#### 调用阈值

- **相似度 ≥ 0.5** — 触发调用
- **相似度 < 0.5** — 不调用
- **每次最多引用** — 2-3 条

---

### 第四步：验证与测试

#### 验证定时任务

```bash
# 查看任务状态
openclaw cron list

# 查看特定任务详情
openclaw cron runs <jobId>
```

#### 验证按需调用

测试触发条件：
- 说"之前我们聊了什么？"
- 说"上次那个问题解决了吗？"
- 问一个之前已经解决过的类似问题

---

### 第五步：容错与边界处理

为保证系统稳定运行，建议添加以下容错机制：

**1. 空数据处理**
- 如果某天的 sessions 为空，daily-summary 仍生成"今日无对话"占位文件
- 如果某周的 daily 文件全空，weekly-summary 生成"本周无对话"占位文件
- 如果某月的 weekly 文件全空，monthly-summary 生成"本月无对话"记录

**2. 输出格式统一**
不同周期任务的输出格式使用不同前缀区分：
| 任务 | 输出格式 | 示例 |
|------|----------|------|
| monthly | `## 📊 YYYY年MM月经验总结` | `## 📊 2026年3月经验总结` |
| quarterly | `## 📊 YYYY年QN季度经验总结` | `## 📊 2026年Q1季度经验总结` |
| yearly | `## 🏆 YYYY年度经验总结` | `## 🏆 2025年度经验总结` |

**3. 会话文件清理（可选）**
为避免 sessions 目录文件堆积，可在 yearly-summary 中附带执行清理：

```bash
# 清理 90 天前的被删除/重置会话文件
find sessions/ -name "*.jsonl.reset.*" -mtime +90 -delete
find sessions/ -name "*.jsonl.deleted.*" -mtime +90 -delete
```

---

### 第六步：自定义配置

#### 修改检索范围

在 AGENTS.md 中修改 `检索范围` 部分：

```markdown
**检索范围：**
- `memory/daily/` — 可自定义天数，如"近 10 天"
- `memory/weekly/` — 可自定义周数
- `MEMORY.md` — 可选择仅检索特定章节
```

#### 修改调用阈值

在 AGENTS.md 中修改 `调用方式` 部分的相似度阈值：

```markdown
2. 根据相关性筛选（相似度 > 0.7）  # 可调整 0.3-0.9
```

#### 修改输出位置（高级）

如果需要修改输出位置，可调整各任务的 `写入路径` 部分：
- daily-summary: `memory/daily/`
- weekly-summary: `memory/weekly/`
- monthly/quarterly/yearly: `MEMORY.md`（根目录）

---

## 附录：记忆文件示例

### 每日总结示例 (memory/daily/2026-03-31.md)

```markdown
# 2026-03-31（星期二）

## 正常会话
- 会话数：3 个
- 关键对话：
  - 用户: "配置 cron 任务"
  - 助手: "已创建 daily-summary 任务"

## 被删除/重置的会话（2个）
### 1. xxx.jsonl.reset (@ 04:33)
- 用户: "上次那个问题解决了吗？"
- 助手: "已查询，问题是..."

### 2. xxx.jsonl.deleted (@ 16:08)
- 用户: "用 Chrome 打开微信文章"
  - 助手: "已启动 Chrome 远程调试模式..."

## 关键信息
- 用户偏好：温柔的台湾女生语气
- 学到的知识：Chrome CDP 可控制浏览器自动化
- 重要决策：采用合并方案处理所有会话
```

### 每周总结示例 (memory/weekly/2026-W13.md)

```markdown
# 2026年第13周经验总结 (2026-03-23 ~ 2026-03-29)

## 本周完成
- 完成了 OpenClaw 工作空间初始化
- 配置了飞书和 QQ 通信渠道
- 建立了经验总结系统的完整流程

## 重要决策
- 决定使用"经验总结系统"作为首个发布的技能
- 采用最小可行版本(MVP)快速验证

## 技术细节
- cron 定时任务使用北京时间需要设置 timezone
- memory_search 工具的相似度阈值建议设为 0.5
- AGENTS.md 的修改会影响所有通道的智能体
```

---

## 常见问题 FAQ

### Q1：定时任务没有执行怎么办？

1. 检查 Gateway 状态：`openclaw gateway status`
2. 重启 Gateway：`openclaw gateway restart`
3. 查看任务执行日志：`openclaw cron runs <jobId>`

### Q2：按需调用没有返回结果是什么原因？

1. 确认 AGENTS.md 已正确修改
2. 检查 memory_search 工具是否可用
3. 确认相关记忆文件已存在
4. 检查触发条件是否满足

### Q3：如何手动触发一次总结？

```bash
openclaw cron run daily-summary
```

### Q4：被删除/重置的会话会丢失吗？

**不会！** 每日总结现在会同时处理：
- 正常的 .jsonl 文件
- .jsonl.reset.* 文件（重置的会话）
- .jsonl.deleted.* 文件（删除的会话）

所有经验都会统一写入 `YYYY-MM-DD.md`，确保经验不遗漏。

### Q5：如何查看历史被删除的会话？

- 每日总结文件：`memory/daily/YYYY-MM-DD.md`（包含正常+被删除会话）
- 历史汇总：`memory/daily/history-deleted.md`（可选，用于长期追溯）

---

## 文件结构

经验总结系统的完整文件结构如下：

```
C:\Users\Admin\.openclaw\workspace\
├── AGENTS.md                    # 含按需调用规则
├── MEMORY.md                    # 长期记忆（精选，monthly/quarterly/yearly 追加）
├── memory/
│   ├── daily/                   # 每日总结（自动生成）
│   │   ├── 2026-03-31.md
│   │   └── ...
│   ├── weekly/                  # 周经验总结（自动生成）
│   │   └── 2026-W13.md
│   ├── manual/                  # 手动记录的日志（不会被自动任务覆盖）
│   │   └── 2026-04-03.md
│   └── heartbeat-state.json     # 心跳状态
└── cron/                        # 定时任务配置
```

---

## 相关命令

- `openclaw cron status` — 检查定时任务调度器状态
- `openclaw cron list` — 列出所有定时任务
- `openclaw cron runs <jobId>` — 查看任务执行历史
- `openclaw status` — 查看整体状态

---

## 更新日志

- **v1.4.0** (2026-04-03)：优化配置与容错机制
  - 修正 cron 时间表达式（monthly: 01:30, quarterly: 02:30, yearly: 03:30）
  - 添加 memory/manual/ 目录说明
  - 添加容错机制与空数据处理
  - 明确输出格式（monthly/quarterly/yearly 区分）
  - 添加会话文件清理策略（90天前）
  - 调整步骤编号（原第五步→第六步）

- **v1.3.0** (2026-04-02)：增强被删除/重置会话处理
  - 每日总结现在同时处理正常会话和被删除/重置的会话
  - 更新记忆文件格式示例（区分正常/重置/删除）
  - 添加 FAQ 说明（Q4、Q5）
  - 合并输出：所有会话统一写入一个 .md 文件

- **v1.2.0** (2026-04-01)：优化发布版本
  - 添加标签（Tags）便于搜索
  - 添加"5分钟快速开始"板块
  - 修正 cron 命令参数（--cron, --tz）
  - 简化步骤说明

- **v1.1.0** (2026-04-01)：根据用户反馈优化
  - 添加技能类型说明（指导型）
  - 补充完整的 cron 创建命令
  - 添加目录创建步骤
  - 增加记忆文件示例
  - 添加常见问题 FAQ