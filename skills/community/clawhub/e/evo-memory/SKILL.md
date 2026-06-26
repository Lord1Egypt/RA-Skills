---
name: self-evolution
description: 自我进化记忆系统。两层记忆架构（L1原则+L2经验）+ 双层信号捕获 + 定时综合反思。Use on every session for continuous self-improvement and learning.
metadata: {"clawdbot":{"emoji":"🧬","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/.openclaw/workspace/self-evolution/"]}}
---

# Self-Evolution 自进化记忆系统

## 每次会话必做

### 第一步：加载记忆

1. 读 `principles.md` — L1 永久原则，全部加载
2. 读 `patterns/index.md` — L2 经验索引
3. 根据当前话题，判断 index 中哪些经验相关，读取对应的 pattern 文件
4. 整个会话复用已加载的 L2，不再重复匹配

### 第二步：事前预防

开始任务前，检查已加载的 L1/L2 中有没有和当前任务相关的坑。有则先提醒用户再执行。

示例："开始之前提醒一下：根据 P042，配置提供商名要避开内置插件名..."

### 第三步：对话中捕获信号

对话过程中，发现以下信号时写一行到 `pending.jsonl`：

| 信号 | 怎么识别 |
|------|---------|
| 用户纠正 | 用户说"不对/错了/应该是..." |
| 操作失败重试 | 同一操作做了 2 次以上 |
| 用户给新知识 | "其实应该.../你不知道的是..." |
| 用户表达偏好 | "我喜欢.../以后都.../别再..." |
| 用户满意 | "牛啊/完美/就是这样" |

**写入格式**（每条一行 JSON）：

```json
{"ts":"时间","signal":"类型","brief":"一句话标题","detail":"详细描述：发生了什么、为什么错/对、用户原话要点","source":"agent"}
```

| 字段 | 说明 | 示例 |
|------|------|------|
| `brief` | 一句话标题，快速扫描用 | "提供商名不要用 qwen" |
| `detail` | 综合时的决策依据，包含上下文和原因 | "用户配置 AI 模型时用 qwen 作为提供商名，触发内置插件劫持致 4008 错误。用户纠正应改用 aliyun" |

规则：
- brief 控制在 20 字以内，detail 控制在 100 字以内
- detail 必须包含：发生了什么 + 为什么（原因/后果）
- 拿不准要不要记？**记**。宁可多记，综合时再筛
- 不记录：一次性指令、上下文特定操作、假设性问题

### 第四步：引用记忆时标注来源

回复中用到了某条 L1/L2 记忆时，在回复里标注（如"参考 P042"）。会话结束时一次性批量写入 `stats/citation-log.jsonl`，不要逐条写。

格式：`{"ts":"时间","source":"principles.md","entry":"P042_禁用qwen","action":"cited","context":"用户问提供商配置"}`

---

## 用户显式触发时（直接写入，不经 pending）

用户明确表达了信号，跳过 pending 直接写入：

| 用户说 | 你的动作 |
|-------|---------|
| "记住：XXX" | 直接写入 `principles.md`（L1） |
| "这个经验记一下" | 问用户什么场景下需要，写入对应 `patterns/` 文件（L2）+ 更新 `index.md` |
| "反思一下 / 回顾一下" | 回顾当前上下文 + 读 pending，生成反思报告，直接写入 L1/L2 |
| "好了 / 满意 / 完成" | 快速检查：这次有没有值得记的？有就直接写入 |
| "不对 / 有问题" | 理解具体纠正了什么，分类后直接写入 L1 或 L2 |

如果 pending 中有之前积累的信号，一并处理并清空。

---

## 定时综合（Heartbeat 触发）

Heartbeat 触发时检查：

```
pending.jsonl 有 5 条以上信号？ → 触发综合
距上次综合超过 24h 且 pending 不为空？ → 触发综合
都不满足？ → 跳过，不打扰用户
```

综合流程：
1. 读 `pending.jsonl`
2. 合并去重（同一事件的 hook 粗信号和 agent 细信号，以细信号为准）
3. 对每个发现自主分类 L1 或 L2
4. 生成反思报告推送给用户
5. 用户批量审阅确认后，写入正式记忆
6. 清空 `pending.jsonl`

---

## L1/L2 分类规则

自主分类，不逐条问用户：

```
这条经验如果在需要时没被加载，会导致犯错或失败吗？
├─ 会 → L1
└─ 不会，只是效率低一点 → L2

拿不准？→ 默认放 L1
```

---

## L1 写入格式（principles.md）

```markdown
### P001: 简短标题
category: 配置/技能/调研分析/多代理/排障/通用/其他
source: 2026-03-28 什么事得出的
why: 为什么要遵守（用于举一反三）
generalize: 泛化规律（从个例提炼的通用模式）
---
具体内容，1-3 句话说清楚。
```

编号规则：在 principles.md 中找到最大的 P 编号，+1。

---

## L2 写入格式（patterns/*.md）

写入对应领域文件，同时更新 index.md：

**领域文件中的条目**：
```markdown
## 简短标题
context: 什么场景下需要加载这条经验（自然语言描述）
tags: [关键词1, 关键词2, 关键词3]
source: 2026-03-28 什么事得出的
---
具体内容，包括步骤、命令、注意事项等。
```

**index.md 中追加一行**：
```markdown
- 简短标题 | file: config.md | context: 什么场景下需要加载
```

领域文件选择：
- config.md — 配置类（提供商、API、端口、认证）
- skills.md — 技能类（安装、加载、SKILL.md 格式）
- multi-agent.md — 多代理协作（subagent、调度、飞书群）
- debug.md — 排障类（错误诊断、日志分析、重启修复）
- research.md — 调研分析（调研方法、报告结构、信息整理）
- general.md — 通用经验
- other.md — 以上都不合适时的兜底

---

## 反思报告格式

```markdown
## 自进化反思报告
时间: YYYY-MM-DD HH:MM

### 发现 1: [类型] 简短描述 → 已分类为 L1/L2
- 事件：发生了什么
- why: 为什么值得记住
- generalize: 通用规律
- **agent 分类：L1/L2（理由）**

### 发现 2: ...

> 以上分类由我自主完成。如有异议请指出，我会调整。

### 记忆系统健康度
- L1 原则数: X 条，本次新增 X 条
- L2 经验数: X 条，本次新增 X 条
```

---

## 用户主动回顾

| 用户说 | 动作 |
|-------|------|
| "有哪些原则" | 读 `principles.md`，按 category 分组展示 |
| "关于XX的经验" | 读 `patterns/index.md`，语义搜索相关条目并展示 |
| "记忆统计" | 从 `stats/citation-log.jsonl` 生成统计报告 |
| "清理记忆" | 列出零引用条目和长期未验证的 L1，引导审查 |

---

## 文件路径速查

| 文件 | 用途 |
|------|------|
| `principles.md` | L1 永久原则 |
| `pending.jsonl` | 信号临时队列 |
| `patterns/index.md` | L2 语义索引 |
| `patterns/config.md` | 配置类经验 |
| `patterns/skills.md` | 技能类经验 |
| `patterns/multi-agent.md` | 多代理协作经验 |
| `patterns/debug.md` | 排障经验 |
| `patterns/research.md` | 调研分析经验 |
| `patterns/general.md` | 通用经验 |
| `patterns/other.md` | 未分类兜底 |
| `stats/citation-log.jsonl` | 引用日志 |
| `config.yaml` | 配置项 |

所有路径基于 `~/.openclaw/workspace/self-evolution/`。
