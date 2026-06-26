# 非 GitHub 区块内容摘要质量设计（2026-05-16）

## 目标

统一提升非 GitHub 区块（KOL、话题文章、RSS Blog Picks、Reddit、Podcast）的中文摘要质量，使其不再偏短、重复或空泛，并保持输出不臆测事实。

本设计不改变抓取、打分、去重与排序核心链路，不引入新的 LLM 写作服务，只强化“已有字段可用时如何生成摘要”的规则与验收约束。

## 范围

### 包含

- KOL（固定区块）摘要的可读性与密度；
- 话题 section（`topics` 下）的非 GitHub 条目摘要；
- Blog Picks 摘要；
- Reddit 条目摘要；
- Podcast 摘要；
- Twitter/X Trending（`Trending` 非 GitHub 的讨论项，不含 GitHub Trending section）；
- `references/digest-prompt.md` 与三类模板文档（`chat` / `discord` / `email`）中的摘要约束；
- acceptance 测试用例，覆盖非 GitHub 区块的摘要质量约束。

### 不包含

- `📦 GitHub Releases` 与 `🐙 GitHub Trending` 的内容扩写规则（保留原有简短风格）；
- 新增抓取器、去重、排序、质量评分逻辑；
- 新增独立的服务器端/本地摘要服务；
- 外部知识注入与推断事实（严格基于 merged JSON 现有字段）。

## 设计

### 一、摘要语义约束（模板与 prompt 共用）

对非 GitHub 区块新增以下约束：

1. 摘要倾向于围绕三层信息组织，而不是强制每条都同时具备三种信息：
   - 发生了什么（核心动作/变更）
   - 发生在什么对象上（项目/人/组织、版本/功能点）
   - 为什么值得关注（影响/后果，必须能被证据支持）
2. 当证据不足时，优先保留“发生了什么”和“对象是什么”；只有证据明确支持时才写“为什么值得关注”。
3. 允许输出 2-4 句；优先 2 句，必要时 3-4 句。
4. Discord 和 Email 的平台长度限制优先级高于句数目标。若存在平台长度压力，摘要可压缩到 1-2 句，但仍需保留最具体的事实信息。
5. 仅使用 merged JSON 已有字段：`title`, `summary`, `snippet`, `full_text`, `chat_summary`, `transcript`, `release`/`repo` 元数据，以及 `source_name/display_name/handle` 等 source metadata。
6. 字段优先级是证据权重，不是互斥选择：`full_text` 优先作为主要事实来源；`summary`、`snippet`、`title` 可以作为补充上下文，用于补足对象名称、来源标题或缺失的简要背景，但不能覆盖或改写更高优先级字段中的明确事实。
7. 不可编造时序、动机、观点来源、行业地位；无法支持时必须收敛为简短保守表述。
8. 同一条事实仅保留一次，不重复复述标题内容。

### 二、按源类型的输出约束

- KOL / Twitter：
  - 先给出观点或动作，再给出可见证据（若已知）。
  - 继续保留四项互动指标，字段固定为 `metrics.impression_count`、`metrics.reply_count`、`metrics.retweet_count`、`metrics.like_count`。
  - 缺失、`null`、空字符串或不可解析的指标统一显示为 `0`；真实值为 `0` 时也显示 `0`。允许显示 `0`，因为它比省略字段更稳定，也能暴露上游缺失或账号低互动的真实状态。
  - 指标展示顺序固定为 `👁 views | 💬 replies | 🔁 reposts | ❤️ likes`，使用现有 K/M 格式化逻辑。
  - 不得将指标当作事实结论依据，只用于传播强度补充。
- 非 GitHub Topic 文章（`render_topic_sections` 类）：
  - 摘要以最高质量可用字段为主：`full_text` > `summary` > `snippet` > `title`。
  - 低优先级字段可作为补充上下文，例如标题中的产品名、source metadata 中的作者名、snippet 中的短背景；但不得与高优先级字段冲突，也不得替代高优先级字段中的主要事实。
  - 允许引用项目名、方法、参数、规模等具体名词（若字段可见）。
- Reddit：
  - 区分“原始内容”和“社区讨论”，避免把 `score/comments` 写成内容事实。
  - 只在“讨论语境”中提及社区热度。
- Podcast：
  - 有 transcript 才允许做更深内容提炼；
  - 无 transcript 只能基于标题/节目名/snippet/时长/节目元数据写元数据型摘要。
- Blog Picks：
  - 仍以 2-4 句为目标；在 `full_text`、`summary` 或 `snippet` 能支持时，优先体现关键洞察点，而不是“标题重述+泛泛评价”。

### 三、模板实现边界

- `references/templates/chat.md`：
  - 将非 GitHub 条目摘要定义为倾向性的“事实-对象-影响”表达顺序（可在 1 段中按证据充分程度表达）。
  - 明确：非 GitHub 允许 2-4 句，避免只输出 1 句标题重述。
- `references/templates/discord.md` 与 `references/templates/email.md`：
  - 在现有结构内，将 `description`/`summary` 的语义描述定义为“摘要内容”，并要求非 GitHub 区块具备上述约束。
  - KOL 摘要依旧使用固定 metric 片段，正文不再“留白”。
- `references/digest-prompt.md`：
  - 添加“非 GitHub 摘要质量合约”章节，覆盖 KOL / topic / Reddit / Blog Picks / Podcast；
  - 明确排除 GitHub Releases、GitHub Trending。

### 四、验收与回归

在 acceptance 测试中加入非 GitHub 质量断言，测试目标应偏结构和字段可见性，避免使用过度语义化的自然语言判断：

- 目标段落（非 GitHub）摘要不为空，且不完全等于 `title`。
- 对 fixture 中有 `chat_summary` 或 `summary` 的非 GitHub 条目，断言最终输出包含该字段中的关键稳定短语，例如项目名、产品名、动作动词或明确对象名称。
- 对 fixture 中只有 `title`/`snippet` 的条目，断言输出不包含 fixture 未提供的公司名、日期、角色或指标。
- 对 Discord/Email 相关规则，只断言文档契约和样例结构；不通过脆弱的句数统计强制平台输出固定 2-4 句。
- KOL 每条都包含四项互动指标；
- 不影响现有 GitHub Releases / GitHub Trending golden 及格式。

## 实施边界与文件影响

- 修改文件（预期）：
  - `references/digest-prompt.md`
  - `references/templates/chat.md`
  - `references/templates/discord.md`
  - `references/templates/email.md`
  - `tests/test_acceptance_digest.py`（如新增/调整断言）
- 不修改文件：
  - `scripts/fetch-*`, `scripts/merge-sources.py`, `scripts/run-pipeline.py` 等抓取与合并核心逻辑。

## 风险与回退

- 风险：更高摘要约束可能导致某些输出字数上升。
  - 缓解：明确平台长度阈值高于句数目标。Discord/Email 可以压缩为 1-2 句，Chat 可以保留 2-4 句目标。
- 风险：模板约束被误读为强制事实扩展。
  - 缓解：测试中加入“无 `full_text`/`summary` 时不得添加新事实”的负向断言。
- 回退：如影响稳定性，优先降级为“保守摘要 + 保留已有字段”，不改 pipeline。

## 变更后的验收标准

- 非 GitHub 五类内容（KOL、non-GitHub topic、Blog Picks、Podcast、Reddit）满足“证据驱动 + 倾向性三段结构”摘要要求；
- KOL 非 GitHub 区块每条摘要与热度指标固定展示；
- `references/digest-prompt.md` + `references/templates/chat.md` + `references/templates/discord.md` + `references/templates/email.md` 保持一致约束；
- GitHub Releases 与 GitHub Trending 的既有输出风格未变化；
- golden 测试链路与新增断言通过。

## 设计自检

- TBD / TODO：无占位符；
- 约束一致性：非 GitHub 与 GitHub 区块规则在文档层面已显式分叉；
- 范围控制：只覆盖输出规则与验收，不涉及抓取与排序；
- 歧义处理：`source_type == "github"` 与 `github_trending` 已明确排除范围；摘要结构是倾向性组织方式，不强制凭空补齐三类信息。
