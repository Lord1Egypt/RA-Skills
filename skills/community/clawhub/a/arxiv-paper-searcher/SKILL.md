name: arxiv-paper-searcher
description: 搜索并分析 arXiv 学术论文。默认执行“搜索 + 摘要分析 + 热点统计 + 趋势判断”的完整流程，并立即返回结构化报告。用户确认后，可基于同一检索条件创建 OpenClaw cron 定时监控任务，定期推送最新论文分析。
------------------------------------------------------------------------------------------------------------------------------

# arXiv Paper Searcher

**版本**：v1.0.2

用于搜索、整理并分析 arXiv 学术论文的技能。

该技能的默认行为是一次性完成完整流程，也就是**搜索 + 分析 + 报告输出**。
定时监控不是默认步骤，只有在用户明确同意后才创建。

## 适用场景

当用户有以下需求时触发本技能：

* 搜索某一主题的 arXiv 论文

* 查看某方向的最新论文

* 对检索结果做热点归纳、创新性评估和趋势总结

* 基于固定关键词持续跟踪新论文

**触发示例**

* 帮我搜索 arXiv 上关于 GNN 的最新论文，要 20 篇

* 查一下 transformer 相关的论文

* 搜索图神经网络的论文，10 篇

* 看看最近多模态大模型有什么新论文

* 帮我持续监控 diffusion model 的 arXiv 论文

## 默认行为

除非用户明确指定，否则使用以下默认值：

* 检索数量为 `20`

* 排序方式为 `date`

* 分析范围为**标题 + 摘要**

* 输出语言跟随用户

* 时区默认使用 `Asia/Shanghai`

* 定时监控默认使用 `sessionTarget: "current"`

如果用户只说“查一下某个方向的论文”，应直接执行，不要为了数量或排序方式反复追问。

## 工作模式

### 模式 1：单次执行（默认）

这是默认模式。用户提供主题后，直接完成搜索与分析，并返回完整报告。

#### 执行流程

1. 解析用户的搜索意图，提取关键词、数量和排序方式

2. 若用户未指定数量或排序，使用默认值

3. 调用搜索脚本获取论文结果

4. 逐篇阅读标题与摘要，完成分析

5. 统计热点研究方向

6. 归纳当前结果中的潜在趋势

7. 输出完整报告

8. 在报告结束后，主动询问用户是否需要开启定时监控

#### 单次执行必须完成的内容

* 返回论文列表

* 对每篇论文给出关注热点

* 对每篇论文给出创新性评估

* 汇总热点研究方向 Top 10

* 给出 3 到 5 条趋势判断

#### 单次执行后建议追问

> ✅ 已完成本次 arXiv 论文搜索与分析。
> 如需持续跟踪这一主题，我可以为你创建定时监控任务，按固定时间自动推送最新论文分析。
> 你只要回复“可以”或直接告诉我推送时间即可。

### 模式 2：定时监控（可选）

只有在用户明确表示需要持续跟踪时，才进入此模式。

#### 执行流程

**Step 1：确认检索配置**

优先复用刚才单次执行时的参数：

* 搜索关键词

* 论文数量

* 排序方式

* 时区

若用户明确要求修改，再更新配置。

**Step 2：确认推送时间**

可引导用户选择常见时间，也支持自定义：

> 好的，我来帮你设置定时推送。
> 你可以直接告诉我一个时间，例如
>
> * 每天早上 9 点
>
> * 每周一上午 9 点
>
> * 每周三晚上 8 点
>
> * 其他你希望的具体时间

**Step 3：先保存业务配置**

在创建定时任务前，把查询参数保存到技能自己的 `config.json`：

* `keyword`

* `max_results`

* `sort`

* `timezone`

这里的 `config.json` **只保存业务配置与绑定信息**，不充当调度真相源。

**Step 4：创建 OpenClaw cron 任务**

创建规则：

* 优先使用 OpenClaw cron 工具或 `openclaw cron add/edit/remove`

* 默认 `sessionTarget: "current"`

* 除非用户明确要求隔离执行或发到新对话，否则不要默认使用 `isolated`

* 不要直接编辑 `~/.openclaw/cron/jobs.json`

**Step 5：回写 job 绑定信息**

创建成功后，把返回的 `jobId` 写回技能配置：

* `job.job_id`

* `job.name`

* `job.enabled`

* `job.session_target`

* `job.schedule.kind`

* `job.schedule.expr`

* `job.schedule.tz`

**Step 6：告知用户任务已创建成功并提醒会话绑定**

用户能得到两层确认：

* OpenClaw cron 侧已经创建成功

* 技能本地配置已绑定到对应 `job_id`

同时必须补充提醒：

* 默认结果会发回创建任务时所在的当前会话

* 因此不要随意删除当前会话

* 如果发送时当前会话已经不存在，可以回退到新对话继续发送

* 一旦回退到新对话，原会话上下文连续性会中断

#### 后续管理

用户后续可以直接说：

* 取消定时任务

* 把搜索词改成 XXX

* 数量改成 50 篇

* 改成每周一早上 8 点推送

处理原则：

1. 先修改 OpenClaw cron 中真实存在的 job

2. 再同步更新本地 `config.json` 里的 `job` 快照

3. 如果本地存在旧 `schedule` 但没有 `job_id`，应视为“仅有旧配置，不代表存在真实定时任务”

## 关键执行原则

### 1. 搜索和分析是一个完整动作

不要只返回论文链接或标题列表。
只要执行了搜索，就必须继续完成分析和总结。

### 2. 优先少打断用户

对于数量、排序、输出格式等非关键信息，优先使用默认值，不要频繁追问。

### 3. 定时任务必须后置

不要在搜索前就询问是否需要定时。
应先完成本次报告，再询问用户是否希望持续监控。

### 4. 分析必须基于摘要

不能只依赖标题或简单关键词匹配。
每篇论文至少要阅读标题和摘要后再判断研究热点与创新性。

### 5. 趋势判断要克制

趋势结论基于当前检索结果，不等同于整个领域的完整学术图景。
需要给出合理推断，但不要过度下结论。

### 6. 调度真相源只能有一个

OpenClaw cron 才是定时任务的调度真相源。
技能本地 `config.json` 只负责保存业务配置和 `job_id` 绑定信息。

### 7. 当前会话优先于隔离会话

对于“在同一个聊天里持续推送论文更新”的场景，默认用 `sessionTarget: "current"`。
只有在用户明确需要隔离上下文、独立 delivery 或不同投递目标时，才考虑 `isolated`。

### 8. 必须显式提醒当前会话绑定

只要成功创建了 `sessionTarget: "current"` 的监控任务，就必须提醒用户：

* 默认发送目标是当前会话

* 不要删除当前会话

* 若发送时当前会话已不存在，可回退到新对话继续发送

* 回退后视为新的上下文起点，不再默认继承被删除会话中的连续对话上下文

## 分析规范

## 分析维度

### 1. 关注热点

从摘要中提取论文主要关注的问题、方法或应用方向，例如：

* 注意力机制

* 图卷积

* 时空预测

* 多模态对齐

* 推理增强

* 数据高效训练

### 2. 创新性评估

按以下标准给出 `高 / 中 / 低`：

* **高**
  提出新架构、新理论、新训练范式，或明显突破现有方法边界

* **中**
  在已有方法上做重要改进，或将成熟方法迁移到新任务并取得较强效果

* **低**
  主要是实验复现、应用验证、工程整合、综述或资源整理

### 3. 研究方向统计

将相近主题聚类归并，统计高频方向，输出 Top 10。

### 4. 趋势判断

结合论文发布时间、主题分布和方法变化，给出 3 到 5 条趋势判断。
趋势描述应具体，避免泛泛而谈。

## 输出要求

### 每篇论文必须包含

* 原始论文标题，不翻译、不省略

* 作者

* 发布时间

* 关注热点

* 创新性评估

* arXiv 链接或 PDF 链接

### 推荐输出格式

```markdown
## 论文列表

### 1. [Paper Title]
- **作者**：Author A, Author B
- **时间**：2026-03-17
- **关注热点**：xxx、xxx、xxx
- **创新性**：高
- **链接**：arXiv / PDF

### 2. [Paper Title]
- **作者**：...
- **时间**：...
- **关注热点**：...
- **创新性**：中
- **链接**：...

## 热点研究方向 Top 10

1. 方向名称（出现次数）
2. 方向名称（出现次数）
3. ...

## 趋势判断

1. ...
2. ...
3. ...
```

## 搜索脚本

### 基本用法

```bash
python ~/.openclaw/workspace/skills/arxiv-paper-searcher/scripts/arxiv_search.py \
  -q "ti:gnn OR ti:\"graph neural network\"" \
  -m 20 \
  -s date \
  -o ~/.openclaw/workspace/skills/arxiv-paper-searcher/papers.json
```

### 参数说明

| 参数             | 说明                                   | 默认值    |
| -------------- | ------------------------------------ | ------ |
| `-q, --query`  | 搜索关键词，支持 arXiv 查询语法                  | 必填     |
| `-m, --max`    | 最大返回数量                               | `20`   |
| `-o, --output` | 输出 JSON 文件路径                         | 可选     |
| `-s, --sort`   | 排序方式，支持 `date`、`updated`、`relevance` | `date` |

## 配置存储

用户检索配置保存在：

`~/.openclaw/workspace/skills/arxiv-paper-searcher/config.json`

v1.1 的推荐结构：

```json
{
  "schema_version": 2,
  "keyword": "ti:gnn OR ti:\"graph neural network\"",
  "max_results": 20,
  "sort": "date",
  "timezone": "Asia/Shanghai",
  "job": {
    "job_id": "job-123",
    "name": "arXiv Monitor · GNN",
    "enabled": true,
    "session_target": "current",
    "schedule": {
      "kind": "cron",
      "expr": "0 9 * * *",
      "tz": "Asia/Shanghai"
    },
    "bound_at": "2026-04-05T09:00:00+08:00",
    "updated_at": "2026-04-05T09:00:00+08:00",
    "notes": null
  },
  "updated_at": "2026-04-05T09:00:00+08:00"
}
```

## OpenClaw cron 任务示例

创建每日论文监控时，推荐任务形态如下：

```json
{
  "name": "arXiv Monitor · GNN",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "current",
  "payload": {
    "kind": "agentTurn",
    "message": "请使用当前技能的已保存配置执行一次完整 arXiv 监控流程。检索关键词是 ti:gnn OR ti:\"graph neural network\"。返回数量是 20。排序方式是 date。时区按 Asia/Shanghai 处理。请先搜索最新论文，再基于标题和摘要逐篇分析，最后输出完整结构化报告。报告必须包含论文列表、每篇论文的关注热点、创新性评估、热点研究方向 Top 10，以及 3 到 5 条趋势判断。"
  }
}
```

说明：

* `sessionTarget: "current"` 适合把结果发回创建任务的当前会话

* 该模式下优先依赖会话绑定，不默认走 `isolated + announce`

* 不要直接改 `jobs.json`

## 推荐工具脚本

* `scripts/arxiv_search.py`
  arXiv 论文搜索脚本

* `scripts/config_manager.py`
  查询配置与 `job_id` 绑定管理

* `scripts/openclaw_cron_builder.py`
  构造 `cron.add` / `cron.update` JSON 载荷

## 配置管理脚本示例

保存业务配置：

```bash
python scripts/config_manager.py --save \
  --keyword 'ti:gnn OR ti:"graph neural network"' \
  --max 20 \
  --sort date \
  --timezone Asia/Shanghai
```

绑定新建的 cron job：

```bash
python scripts/config_manager.py --bind-job \
  --job-id 'job-123' \
  --job-name 'arXiv Monitor · GNN' \
  --session-target current \
  --schedule-kind cron \
  --schedule-expr '0 9 * * *' \
  --timezone Asia/Shanghai
```

解绑本地记录：

```bash
python scripts/config_manager.py --unbind-job
```

## Cron JSON 构造示例

构造 `cron.add` 载荷：

```bash
python scripts/openclaw_cron_builder.py \
  --build-add \
  --session-target current \
  --schedule-kind cron \
  --cron '0 9 * * *' \
  --tz Asia/Shanghai
```

构造 `cron.update` 载荷：

```bash
python scripts/openclaw_cron_builder.py \
  --build-update \
  --job-id 'job-123' \
  --session-target current \
  --schedule-kind cron \
  --cron '0 8 * * 1' \
  --tz Asia/Shanghai
```

## 依赖

```bash
pip install arxiv
```

## 不要做的事

* 不要只返回论文列表，不做分析

* 不要在用户未同意时自动创建定时任务

* 不要把论文标题翻译成中文

* 不要仅凭标题判断热点和创新性

* 不要把当前批次结果的趋势判断表述成整个领域的定论

* 不要把本地 `config.json` 当成真正的调度器

* 不要直接编辑 `~/.openclaw/cron/jobs.json`

