---
name: brightdata-research
description: >
  Use when the user asks to batch-search candidates, verify public web evidence, dedupe results, and organize them into Feishu/Lark docs.
  Use especially for requests like "继续搜更多并追加到飞书", "帮我批量找一批候选并整理到飞书", "搜索+抓取+汇总+落文档/落表", "帮我调研一批XX平台", "扩展候选池", even if the user does not explicitly name this skill.
  Also use when the user says "检查飞书文档里有没有重复" or "去重" in the context of a research document — this skill covers dedup-and-cleanup as a sub-workflow.
  Do NOT use for: single-page summaries, one-off Q&A, pure code tasks, or tasks that don't involve batch research + structured output.
---

# brightdata-research

> GitHub: https://github.com/16Miku/brightdata-research-skill
> ClawHub: https://clawhub.ai/16miku/brightdata-research

把"批量搜索 + 网页抓取 + 候选验证 + 结构化整理 + 飞书追加写入"做成一个稳定、可复用的研究流水线。

## 执行模式

本 skill 有两种执行模式。根据环境状态自动选择。

### Mode A — 直接执行

前提：搜索、抓取、飞书写入能力均已就绪。
行为：跳过环境准备，直接进入 Step 0 开始研究流程。

### Mode B — 环境准备 + 执行

前提：首次使用，或 preflight 发现缺少关键能力。
行为：先按 `references/environment-checklist.md` 逐项检查并修复，然后进入 Mode A。

环境准备的自动修复顺序见 `references/lark-cli-install-and-auth.md` 和 `references/brightdata-mcp-setup.md`。

## 核心原则

1. **搜索和抓取可以并行。**
2. **最终去重、风险分层、飞书写入必须由主代理串行完成。**
3. **先汇总，再写入。** 不要边搜索边直接写飞书。
4. **保留 evidence。** 每条候选都应尽量保留公开证据链接。
5. **环境不齐就降级。** 缺搜索、抓取、飞书、subagent 或 git/worktree 条件时，明确说明并切到 fallback。
6. **不要依赖脆弱的 shell 多行拼接。** 写飞书时优先构造稳定的完整 Markdown。
7. **上下文复用。** 如果当前对话已有历史候选池或目标文档信息，直接复用，不要重复询问用户。

## 标准工作流

### Step 0. 明确本轮目标

从用户请求或历史上下文提取：
- 研究主题
- 目标数量
- 范围 / 国家 / 语言 / 模型范围
- 已有候选池或目标飞书文档
- 是"继续追加"还是"新建文档"
- 是否允许使用 subagent

**上下文复用规则：** 如果当前对话里已经出现过目标文档 URL/ID、历史候选列表、或研究主题，直接复用这些信息，不要再问用户"请提供文档 ID"。

### Step 1. Preflight 环境检查

按 `references/environment-checklist.md` 检查：

| 能力 | 检查方式 | 缺失时行为 |
|------|----------|------------|
| 搜索 | 检查 BrightData MCP 工具或 CLI 是否可用 | 不能扩充候选池，只能验证用户给定名单 |
| 抓取 | 检查 BrightData scrape 工具或 CLI 是否可用 | 只输出低置信度线索 |
| 飞书写入 | 检查 lark-cli / lark-doc skill 是否可用 | 先输出 Markdown，告知用户未写入飞书 |
| 目标文档 | 检查上下文是否有 doc_id / URL | 询问用户：新建还是追加 |
| 历史去重 | 尝试读取已有文档内容 | 只做本轮内部去重，声明无法保证历史去重 |
| subagent | 检查 git 仓库和 HEAD 是否可解析 | 改为主代理串行执行 |

如果缺失项可自动修复（如 lark-cli 未安装），按 Mode B 修复后继续。
如果缺失项无法自动修复（如用户未提供 API token），明确告知用户并降级。

### Step 2. 制定搜索批次

把任务拆成多个独立批次：
- 不同 query 变体
- 不同语言关键词
- 不同来源入口（官网、文档、pricing、help、faq、terms、privacy）
- 不同平台类别关键词（gateway、aggregator、relay、OpenAI-compatible API 等）

### Step 3. 并行搜索与初筛

优先使用 BrightData 搜索和抓取工具：
- 搜索候选平台
- 获取官网、文档页、定价页、条款页等公开入口
- 记录标题、URL、摘要、来源 query

初筛时保留高相关候选，剔除明显无关页、镜像页、纯广告页。

### Step 4. 去重

去重分两阶段：

**阶段 A — 本轮内部去重：**
1. 域名规范化：去掉 www/http(s)/尾部斜杠，统一小写
2. 品牌别名识别：同一平台可能有多个域名或品牌名（如 openrouter.ai 和 OpenRouter），应识别为同一候选
3. 保留证据更完整、官网性更强的一条

**阶段 B — 历史去重（如果能读取历史文档）：**
1. 读取已有飞书文档内容
2. 提取历史候选名单（名称 + 域名）
3. 与本轮候选交叉比对
4. 已在历史文档中出现的，不重复写入，但在去重说明中列出

如果无法读取历史文档，只做阶段 A，并明确声明。

### Step 5. 结构化字段提取

默认推荐字段：
- 名称
- 官网
- 文档/API 页
- 定价页或价格线索
- 支持模型证据
- OpenAI-compatible / 统一 API 兼容证据
- 初步风险等级
- 备注

如果用户有自定义字段，优先满足用户字段 schema。

### Step 6. 风险分层

使用 checklist 式评分：

| 维度 | 有=1分 | 无=0分 |
|------|--------|--------|
| 可访问的官网 | 1 | 0 |
| 公开 API 文档 | 1 | 0 |
| 定价页或明确价格信息 | 1 | 0 |
| Terms of Service / Privacy Policy | 1 | 0 |
| 可查证的公司/团队主体 | 1 | 0 |
| OpenAI-compatible 或统一 API 兼容证据 | 1 | 0 |

分层规则：
- **A / 较低风险**（5-6 分）：公开资料完整，文档与能力证据充足
- **B / 中风险**（3-4 分）：有一定公开证据，但部分维度需补验
- **C / 高风险 / 待验证**（0-2 分）：主要依赖搜索摘要，暂不适合高置信纳入

每条候选附一句风险原因。

### Step 7. 主代理统一收口

主代理负责：
- 汇总所有候选
- 最终去重
- 字段格式统一
- 风险口径统一
- 决定哪些算"新增不重复候选"
- 生成最终写入飞书的 Markdown

### Step 8. 串行写入飞书

如果用户要求写入飞书文档：
1. 先遵守 `lark-shared` 与 `lark-doc` 的认证和安全规则
2. 复用现有文档 ID；若无则按用户意图新建或先确认
3. 默认使用 `--as user` 访问用户自己的文档
4. 以统一模板生成一轮完整 Markdown
5. 由主代理一次性或顺序串行追加写入

不要让 subagent 直接写同一个飞书文档。

## 输出格式

默认按下面结构向用户汇报，并尽量按同结构写入飞书文档：

```md
## 第X轮新增候选（来源说明）

### 1. 平台名称
- 官网：
- 文档：
- 定价：
- 支持模型证据：
- OpenAI 兼容证据：
- 初步风险：A/B/C（得分 X/6，原因：...）
- 备注：

## 本轮待进一步验证候选
...

## 本轮去重说明
- 本轮内部去重：哪些被合并
- 历史去重：哪些平台已在历史轮次出现，因此不重复写入

## 本轮阶段性结论
- 本轮新增较高可信候选：
- 本轮新增待验证候选：
- 下一步建议：
```

如果用户没有要求写飞书，也建议先按这个模板输出到对话中。

## 何时调用 subagent

适合调用 subagent 的场景：
- 需要扩展多组搜索 query
- 需要并行搜索多个类别或多个国家 / 语言
- 需要对多个候选分别做公开网页核验
- 需要快速拉回 5-10 个新候选并形成候选池

### subagent 可负责
- 搜索 query 扩展
- 搜索结果拉取
- 单个平台公开信息初步核验
- 初步结构化字段整理

### subagent 不应负责
- 最终历史去重判定
- 最终风险分层定稿
- 飞书文档写入
- 最终面向用户的主结论

如果环境不满足 subagent/worktree 前置条件，改为主代理串行执行。详见 `references/subagent-git-prerequisites.md`。

## 子工作流：文档去重清理

当用户要求"检查飞书文档有没有重复"或"去重"时，执行以下子流程：

1. 读取目标飞书文档全文
2. 提取所有候选平台的名称和域名
3. 域名规范化 + 品牌别名识别
4. 找出完全重复条目（同一平台在不同轮次被当作新候选重复写入）
5. 区分"重复"与"补充验证"（后续轮次对已有平台补充新证据，不算重复）
6. 向用户报告发现的重复项，由用户确认后删除

## 边界与禁忌

- 不要把搜索结果摘要当成已核验事实；能补官网或文档页就尽量补。
- 不要把营销话术直接当能力证明；优先找 docs、pricing、terms、privacy、company 等公开页。
- 不要为了追求数量忽略去重；"新增不重复候选"比"看起来很多"更重要。
- 不要在写飞书前跳过统一整理步骤。
- 不要多个 agent 并发写同一文档。
- 不要输出无法回溯来源的结论。
- 不要假装环境齐全；缺前置条件时应明确说明并降级。

## 成功标准

以下条件大致满足时，可认为本轮执行成功：
- 成功找到了本轮新增、不重复的候选
- 候选至少具备核心结构化字段
- 已明确区分"较高可信"与"待进一步验证"
- 风险评级基于 checklist 打分，而非纯主观判断
- 最终写入飞书时格式稳定、换行正常、无明显重复
- 在新环境里也能先做 preflight，再决定完整执行还是降级执行

## 参考文档索引

| 文档 | 用途 |
|------|------|
| `references/environment-checklist.md` | Preflight 检查清单，区分可自动修复和需用户介入的项 |
| `references/brightdata-mcp-setup.md` | BrightData MCP 和 CLI 的安装、认证与验证 |
| `references/lark-cli-install-and-auth.md` | lark-cli 安装、配置、认证的完整步骤 |
| `references/feishu-setup.md` | 飞书文档写入规则和身份选择 |
| `references/known-failures-and-fallbacks.md` | 常见失败场景和降级策略 |
| `references/subagent-git-prerequisites.md` | subagent/worktree 的前置条件和降级规则 |
| `references/smoke-tests.md` | 每项能力的最小验证命令 |
