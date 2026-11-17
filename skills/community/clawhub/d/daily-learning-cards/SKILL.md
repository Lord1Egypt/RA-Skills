# daily-learning-cards v1.1.0

每日学习卡片自动生成 - 从会话记录中提炼知识，生成结构化学习卡片。

---

## 📑 快速导航

| 章节 | 内容 |
|------|------|
| [它到底能干嘛](#它到底能干嘛) | 功能概览：每日卡片 + 每周周报 + 每周测试 |
| [适用人群](#适用人群) | 检查你是否适合使用 |
| [快速开始](#快速开始) | 3 步上手 |
| [配置说明](#配置说明) | config.json 各字段详解 |
| [常见问题](#常见问题) | FAQ 和故障排查 |
| [更新日志](#更新日志) | 版本历史 |

---

---

## 它到底能干嘛？

这是一套完整的**学习闭环系统**，不是单一定时任务：

| 产出 | 频率 | 内容 |
|------|------|------|
| 📝 **每日学习卡片** | 每天 | 提取当日对话中的主题、决策、踩坑、新概念、金句 |
| 📊 **每周学习周报** | 每周一 | 汇总上周学习概览，Elon 经理点评 + 下周建议 |
| 📋 **每周测试题** | 每周一 | 基于上周学习卡片出 20 道题（70% 本周 + 30% 历史） |

三项自动串联：每日卡片 → 周报 → 测试 → 错题本，形成"输入 → 沉淀 → 检验"的闭环。

---

## 适用人群

**正在用 OpenClaw 的人。** 需要满足：
- ✅ 有 OpenClaw 运行环境
- ✅ 日常通过飞书、WebUI、钉钉、微信、QQ 等渠道与 AI 对话
- ✅ 想把每天的对话沉淀为结构化知识

> ⚠️ **对话渠道自动识别（5 种）：** session 文件会自动检测消息来源渠道（Feishu / WebUI / DingTalk / WeCom / QQBot），无需手动配置。如需开启或关闭特定渠道的学习卡片生成，在 `config.json` 的 `channels.sources` 中添加或移除渠道名即可。全部渠道代码：`feishu`、`webui`、`dingtalk`、`weixin`、`qqbot`。

不是 OpenClaw 用户？这套 Skill 你用不了——定时任务和消息投递依赖 OpenClaw 基础设施。

---

## 为什么选它

| 对比项 | daily-learning-cards | 手动记录 |
|--------|---------------------|---------|
| 自动提取 | ✅ 从会话记录自动抓取 | ❌ 靠记忆回顾 |
| 结构化输出 | ✅ 主题/决策/踩坑/概念/金句 | ❌ 碎片化笔记 |
| 多渠道支持 | ✅ 飞书/WebUI/钉钉/微信/QQ 自动合并 | ❌ 需要手动整理 |
| 每日自动推送 | ✅ 定时投递到消息渠道 | ❌ 需要自己提醒 |
| AI 排序 | ✅ 按内容丰富度排序 | ❌ 按时间线堆叠 |
| 自动测试 | ✅ 每周出题检验吸收率 | ❌ 无法自动生成 |

---

## 功能特性

- 📚 **智能提取**：自动从多渠道对话记录中提取学习内容
- 🧠 **AI 整合**：基于内容丰富度进行重要性排序，提炼核心知识
- 📝 **结构化输出**：自动生成包含主题、决策、踩坑、新概念、金句的学习卡片
- 📤 **自动投递**：通过 OpenClaw 自动投递到配置好的消息渠道
- ⚙️ **高度可配置**：支持用户自定义提取规则、数量限制、输出格式

---

## 快速开始

### 1. 安装

```bash
clawhub install daily-learning-cards
```

### 2. 回答几个问题

装完第一次对话，我会检测到这是新装的，然后问你几个问题：

- 你用哪些对话渠道？（飞书、WebUI、钉钉、微信、QQ）
- 每天几点生成学习卡片？周报和测试在哪天什么时间？
- 推送发到哪个渠道？

你回答完，我帮你：① 写配置 ② 配好定时任务。你什么都不用动。以后想改设置，直接告诉我。

---

## 第一次运行 — 配置向导（Agent 执行）

**执行条件：** 检测到 `~/.daily-learning-cards/config.json` 不存在，或存在但没有 `channels.sources` 字段。

**执行步骤：**

### Step 1: 告知用户
"检测到你刚安装了每日学习卡片技能，需要先做一次配置。我会问你几个问题，你回答完就行。"

### Step 2: 询问配置项
依次问（但一次只问 1-2 个问题，别列清单）：

1. **对话渠道：** "你现在用哪些对话渠道？飞书、WebUI、钉钉、微信、QQ？多选哦"
   - 写入 `config.json` → `channels.sources`

2. **生成时间：** "每天几点生成学习卡片？比如 10:00？"
   - 写入 `config.json` → `schedule.hour` / `schedule.minute`

3. **周报/测试：** "周报和测试大概什么时间生成？默认周一 11:00 和 11:30"
   - 周报：`weekly-summary-cron.sh` 的 cron 时间
   - 测试：`weekly-exam.sh` 的 cron 时间

4. **推送渠道：** "学习卡片发到你哪个渠道？飞书？还是微信/钉钉？"
   - 写入 `config.json` → `channels.delivery`
   - 如果选飞书，再问飞书群 ID 或私聊 ID → `feishu.target`

### Step 3: 写入配置

写入 `~/.daily-learning-cards/config.json`：

```json
{
  "channels": { "sources": ["feishu", "webui"], "delivery": "feishu" },
  "schedule": { "hour": 10, "minute": 0, "timezone": "Asia/Shanghai" },
  "feishu": { "target": "用户给的 ID" }
}
```

### Step 4: 配置定时任务

使用 `openclaw cron add` 创建三个定时任务：

- 每日学习卡片 → 每天
- 每周周报 → 每周一
- 每周测试 → 每周一（紧接周报后，留 30 分钟间隔）

**注意：** 路径用 `\$SKILL_DIR`（OpenClaw 自动注入的环境变量，指向 skill 安装目录），而不是硬编码路径。

### Step 5: 确认
"配置完成！以后每天 10:00 学习卡片会自动发到你的 XX 渠道。如果想改，直接告诉我就行。"

---

## 架构设计

```
┌─────────────────┐     ┌─────────────┐     ┌─────────────┐
│  memory/feishu/ │     │  extract.js │     │ generate-   │
│  memory/webui/  │ ──▶ │  (数据提取)  │ ──▶ │ card.js     │
│  memory/dingtalk/│     │  5种渠道    │     │ (AI整合)    │
│  memory/weixin/ │     │  自动识别    │     │             │
│  memory/qqbot/  │     │             │     │             │
│  ...可扩展...   │     │             │     │             │
└─────────────────┘     └─────────────┘     └──────┬──────┘
                                                    │
                                                    ▼
┌─────────────────┐     ┌─────────────┐     ┌─────────────┐
│  OpenClaw cron  │     │   stdout    │     │  learning-  │
│   --announce    │ ◀── │  (摘要输出)  │ ◀── │  cards/     │
│                 │     │             │     │  YYYY-MM-DD.md
└─────────────────┘     └─────────────┘     └─────────────┘
```

**设计原则：**
- **数据提取**（脚本）：确定性的结构化提取
- **内容整合**（AI）：理解性的重要性排序和提炼
- **消息投递**（OpenClaw）：平台无关的自动投递

---

## 配置文件

### 用户配置

位置：`~/.daily-learning-cards/config.json`

```json
{
  "extract": {
    "maxTopics": 20,
    "maxPitfalls": 6,
    "maxConcepts": 6,
    "maxInsights": 6,
    "minInsightLength": 10
  },
  "summary": {
    "includeTopics": true,
    "includeDecisions": true,
    "includePitfalls": true,
    "includeConcepts": true,
    "includeInsights": true,
    "emojiStyle": "unicode"
  },
  "schedule": {
    "hour": 10,
    "minute": 0,
    "timezone": "Asia/Shanghai"
  },
  "channels": {
    "sources": ["webui", "feishu"],
    "delivery": "feishu"
  },
  "feishu": {
    "target": "oc_xxxxx"
  },
  "language": "zh"
}
```

### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `extract.maxTopics` | number | 20 | 最大主题数 |
| `extract.maxPitfalls` | number | 6 | 最大踩坑记录数 |
| `extract.maxConcepts` | number | 6 | 最大新概念数 |
| `extract.maxInsights` | number | 6 | 最大金句数 |
| `extract.minInsightLength` | number | 10 | 金句/洞见的最小字符长度 |
| `summary.emojiStyle` | string | "unicode" | Emoji 样式：unicode/text |
| `schedule.hour` | number | 10 | 定时小时 |
| `schedule.minute` | number | 00 | 定时分钟 |
| `language` | string | "zh" | 语言：zh/en/bilingual |
| `channels.sources` | string[] | ["webui","feishu"] | 收集渠道（从哪些 memory/ 子目录读取，可扩展如 dingtalk/weixin）|
| `channels.delivery` | string | "feishu" | 推送渠道（投递到哪个消息渠道）|
| `feishu.target` | string | — | 飞书推送目标（群/私聊 ID），仅 `channels.delivery=feishu` 时生效 |

---

## 提取规则

### 自动提取的字段

**1. 主题（Topics）**
- 识别：`## 新主题：{主题名}` 或 `### 时间：{时间}`
- 提取：主题名称、来源渠道

**2. 决策（Decisions）**
- 识别：`| 选项 | 考虑因素 | 结果 |` 表格
- 提取：选项、考虑因素、结果

**3. 踩坑记录（Pitfalls）**
- 识别：`**踩坑记录：**` + `- **问题：** {描述}`
- 提取：问题、解决方案、教训

**4. 新概念（Concepts）**
- 识别：`**新概念：**` + `- **术语：** {术语}`
- 提取：术语、定义、应用场景

**5. 金句/洞见（Insights）**
- 识别：`> "{金句}"` 或 `> {金句}`
- 提取：金句内容

### 自动过滤的内容

以下系统噪音会被自动过滤：
- "morning"
- "两件事都已完成"
- "心跳检查"
- "启动检查"
- "HEARTBEAT_OK"

---

## 输出格式

### 摘要（stdout）

每日推送到消息渠道的摘要格式：

保存到 `memory/learning-cards/YYYY-MM-DD.md` 的完整格式：

```markdown
# 学习卡片 - 2026-04-18

## 基本信息
- **日期：** 2026-04-18
- **渠道：** 飞书 + WebUI（多渠道合并）
- **主题数：** 12 个
- **决策数：** 12 个
- **踩坑数：** 7 个
- **新概念：** 5 个

---

## 核心主题

### 1. 落款格式问题
**来源：** 飞书

### 2. 今日记忆文件检查
**来源：** 飞书

...

---

## 重要决策

| 选项 | 考虑因素 | 结果 | 来源 |
|------|---------|------|------|
| 统一超时时间 | 提高系统稳定性 | 采纳 | 飞书 |
...

---

## 踩坑记录

### 1. follow-builders脚本使用openclaw message send发送命令无法执行
**来源：** 飞书
- **解决方案：** 修改脚本直接调用技能的JS文件
- **教训：** 命令需要在正确的环境中执行

...

---

## 新概念

### 1. 定时任务超时控制
**来源：** 飞书
- **定义：** 为定时任务设置最大执行时间限制
- **应用场景：** 防止任务无限期运行

...

---

## 金句 / 洞见

1. > "超时控制是系统稳定性的关键要素"
   > —— 飞书

...

---

## 数据来源

- **飞书：** memory/feishu/2026-04-18.md
- **WebUI：** memory/webui/2026-04-18.md
- 更多渠道同理（如钉钉 → `memory/dingtalk/`）

---

*💃 金银 Planet · 自我提升部*
```

---

## 故障排除

### 问题 1：卡片未生成

**症状：** 定时任务运行但无卡片生成

**检查：**
```bash
# 1. 检查昨日是否有会话记录
ls -la memory/*/

# 2. 检查日志
tail -20 /tmp/daily-learning-cards.log

# 3. 手动运行查看输出
bash daily-learning-cards.sh
```

**解决：**
- 确保昨日有对话记录
- 检查 `extract.js` 是否正常输出 JSON

---

### 问题 2：内容提取不完整

**症状：** 踩坑记录/新概念/金句未提取

**检查：**
```bash
# 检查记忆文件格式
ls memory/*/2026-04-18.md 2>/dev/null
cat memory/feishu/2026-04-18.md 2>/dev/null | grep -A3 "踩坑记录"
```

**解决：**
- 确保使用标准格式：`- **问题：** {描述}`
- 检查 `extract-rules.md` 中的识别规则

---

### 问题 3：主题数量不对

**症状：** 提取的主题数与预期不符

**检查：**
```bash
# 查看配置
cat ~/.daily-learning-cards/config.json | grep maxTopics

# 测试提取
node scripts/extract.js 2026-04-18 | grep -c '"title"'
```

**解决：**
- 修改 `~/.daily-learning-cards/config.json` 中的 `maxTopics`
- 主题按内容丰富度排序，不是按时间顺序

---

### 问题 4：定时任务未触发

**症状：** 到时间了没有收到学习卡片

**检查：**
```bash
# 查看 cron 任务
openclaw cron list | grep "学习卡片"

# 检查任务状态
openclaw cron info <任务ID>
```

**解决：**
- 重新创建 cron 任务
- 检查 `--announce` 参数是否正确配置

---

## 高级用法

### 自定义提取规则

编辑 `prompts/extract-rules.md`：

```markdown
# 自定义提取规则

## 新增提取字段

### 6. 关键数据（KeyData）

**识别方式：**
- 表格格式：`| 数据 | 数值 | 意义 |`

**提取内容：**
- name: 数据名称
- value: 数值
- meaning: 意义
```

### 自定义摘要模板

编辑 `prompts/summary-template.md`：

```markdown
# 我的自定义摘要模板

## 输出格式

```
📚 今日学习总结 · {日期}

🎯 核心收获：{主题数} 个主题
💡 关键洞见：{金句数} 条

{主题列表}

---
💪 继续加油！
```
```

---

## 与其他技能协作

```
┌─────────────────┐
│ learning-cards  │ 每日生成学习卡片
│   (本技能)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ learning-examiner│ 基于卡片出题测试
│   (学习考官)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ learning-manager│ 生成周报汇总
│   (Elon)        │
└─────────────────┘
```

---

## 技术细节

### 文件结构

```
daily-learning-cards/
├── _meta.json                    # Skill 元数据
├── SKILL.md                      # 本文件
├── daily-learning-cards.sh       # 主脚本（每日卡片入口）
├── weekly-summary-cron.sh        # 周报脚本（每周一 11:00）
├── weekly-exam.sh                # 测试脚本（每周一 11:30）
├── refine-memory.sh              # 记忆文件精炼脚本
├── prompts/                      # Prompts 目录
│   ├── summary-template.md       # 摘要模板
│   └── extract-rules.md          # 提取规则
├── scripts/                      # 脚本目录
│   ├── extract.js                # 数据提取
│   ├── generate-card.js          # 学习卡片生成
│   ├── generate-exam.js          # 考题生成
│   ├── extract-insights.js       # 金句提取
│   ├── extract-pitfalls.js       # 踩坑提取
│   ├── extract-concepts.js       # 新概念提取
│   └── load-config.js            # 配置加载（含初始化向导）
├── config.json                   # 用户配置
└── README.md                     # 简要说明
```

### 依赖

- **Node.js** ≥ 16.0
- **Bash** ≥ 4.0
- **OpenClaw**（用于定时任务和消息投递）

---

## 更新日志

### v1.0.0 (2026-05-08)
- 🎉 初始版本
- ✅ 多渠道合并（飞书/WebUI/钉钉/微信/QQ 等可扩展）
- ✅ 自动飞书推送
- ✅ 智能内容过滤
- ✅ AI 整合生成（重要性排序）
- ✅ 用户配置文件支持
- ✅ Prompts 外置
- ✅ 踩坑/新概念/金句列表化
- ✅ 统计概览优化

_更多更新即将到来_

---

## 许可证

MIT-0 - 自由使用，无需署名。

---

## 反馈与支持

如有问题或建议，请：
1. 检查本 SKILL.md 的故障排除章节
2. 查看日志文件：`/tmp/daily-learning-cards.log`
3. 联系开发者

💃 金银 Planet · 自我提升部
