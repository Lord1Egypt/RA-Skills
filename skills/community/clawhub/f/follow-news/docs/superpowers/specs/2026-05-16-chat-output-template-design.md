# Chat Output Template Design

## 目标

新增一个通用 IM 输出模板，用于 Telegram、飞书、微信、企业微信等聊天场景。模板关注可读性和转发稳定性，让每条新闻以“标题、内容总结、链接”的形式独立呈现，避免当前 Discord 列表式输出信息过薄的问题。

这个模板不追求单个平台的最佳渲染能力，而是使用各平台都能稳定展示的纯文本和轻量 Markdown。

## 范围

- 新增 `references/templates/chat.md`，作为 Telegram、飞书、微信等聊天工具的通用模板说明。
- 将 `<TEMPLATE>` 可选值扩展为包含 `chat`。
- 为确定性 acceptance renderer 增加 `chat` 输出模式和 golden 样例。
- 保留原始新闻标题和链接，不把标题改写成摘要。
- 为每条可见新闻增加一段更完整的中文内容总结。
- 链接统一使用 `🔗 URL`，不使用 `<URL>` 或 Markdown inline link。

## 非目标

- 不为 Telegram、飞书、微信分别拆出多个模板。
- 不修改抓取、去重、打分、排序、主题选择逻辑。
- 不引入新的 LLM enrichment pipeline。
- 不强制所有内容出现固定的 `理由：` 字段。
- 不要求 GitHub Releases 和 GitHub Trending 与普通新闻一样扩成长段总结。

## chat 模板输出格式

`chat` 用于 Telegram、飞书、微信、企业微信等通用 IM 场景。每条新闻使用固定三段结构：

```markdown
{{title_line}}

{{summary}}

🔗 {{url}}
```

其中 `title_line` 使用：

```markdown
{{index}}. {{emoji}} [{{score}}/10] {{title}}
```

规则如下：

- `index` 在每个 section 内从 1 开始。
- `emoji` 使用 topic emoji 或固定 section emoji。
- `score` 从 `quality_score` 映射到 10 分制，优先保持一位小数以内的紧凑表达。
- `title` 使用源数据原始标题，不做总结式改写。
- `summary` 是一段中文内容总结，通常 2-4 句。
- `summary` 可以包含价值判断或影响解释，但不固定使用 `理由：` 标签。
- `url` 使用源数据原始链接，单独成行。
- URL 必须为裸 URL，前缀固定为 `🔗 `。
- 不得使用 `<URL>`、Markdown inline link 或 HTML link。
- 每条新闻之间空一行。

每个 topic section 使用：

```markdown
## {{topic_title}}

{{news_item_1}}

{{news_item_2}}
```

过滤后没有可见新闻的 topic section 不应渲染。所有被渲染的 topic section 至少包含一条可见新闻。

## 内容生成约束

可用 summary material 包括 `title`、`snippet`、`summary`、`full_text`、`transcript`、release notes、repo metadata、source metadata 等已经进入 merged JSON 的字段。生成总结时只能使用这些字段中明确出现的信息，不得基于常识、外部知识或模型推测补全公司、人名、指标、发布时间、观点影响等内容。

当新闻缺少充足 summary material 时，使用 `title`、`snippet`、`summary`、`full_text` 中可用的信息生成更短、更谨慎的总结。不能凭空补充事实。

发布时间缺失时不得编造；如只存在抓取时间，应避免把抓取时间写成新闻发布时间。

同一 topic 内的排序逻辑沿用现有 merged JSON 和 renderer 规则，不在 `chat.md` 中重新定义。`chat.md` 只定义输出结构和摘要风格。

## 源类型规则

普通 topic 新闻的总结应说明三件事：发生了什么、核心信息是什么、为什么值得关注。重点是把标题背后的事实、观点或产品变化说清楚，而不是重复标题。

Twitter/X 或 KOL 内容应说明发言者的 display name、handle 或已知身份，以及其提出的观点或动作。只有在 evidence 中明确出现身份、公司、职位或背景时，才可写入总结；否则不要推断其行业地位。互动数据只有在能解释传播强度、争议程度或重要性时才写进总结；否则不展示 likes、reposts、views 等数字。

RSS 和 Web 内容应优先包含产品、模型、版本、公司、人名、指标、发布时间等具体信息。发布时间缺失时不得编造；如只存在抓取时间，应避免把抓取时间写成新闻发布时间。只有 snippet 可用时，摘要应更谨慎；有 full text 或更丰富 evidence 时，可以写得更完整。

Reddit 内容应区分被分享链接本身和社区讨论。被分享链接本身提供的信息可以包括文章、项目、论文、产品发布等；社区讨论信息可以包括 subreddit、score、评论量或主要争议点。社区评论、点赞数和争议焦点只能作为传播或讨论热度信号，不能作为事实结论来源。

Podcast 内容只有在 transcript 可用时，才写 transcript-backed insight。缺少 transcript 时，只允许基于标题、节目名、snippet、时长和 source metadata 写元数据支持的总结；不得写“嘉宾认为”“节目指出”“深入讨论了某观点”等内容型 insight，除非这些信息明确出现在标题、snippet 或 metadata 中。

GitHub Releases 和 GitHub Trending 保持短摘要风格，优先突出 repo、版本号或 trending 状态、主要变化、语言、star 信息。GitHub 类条目通常控制在 1 句，避免写成普通新闻长摘要。除非 release notes 或 repo metadata 中明确提供背景，否则不扩展行业判断。

## 模板关系

`discord.md` 继续服务 Discord 风格输出；`chat.md` 服务 IM 风格输出。两者可以共享基础字段、topic 分组和排序规则，但输出结构不同。排序逻辑沿用现有 merged JSON 和 renderer 规则，`chat.md` 只定义输出结构和摘要风格。

`chat` 是推荐给 Telegram、飞书、微信、企业微信的默认选择。后续如果某个平台确实需要专有能力，再单独新增平台模板。

## 数据流

现有 pipeline 继续生成 merged JSON。最终输出阶段根据 `<TEMPLATE>` 选择模板：

- `discord` 使用现有 Discord 结构。
- `email` 使用现有 HTML email 结构。
- `markdown` 保持现有兼容语义。
- `chat` 使用新的标题、总结、链接结构。

Acceptance renderer 需要支持渲染 `chat` 样例，便于测试输出结构是否稳定。

## 错误处理和降级

当新闻缺少可用 summary material 时，使用 `title`、`snippet`、`summary`、`full_text` 中可用的信息生成更短总结。不能凭空补充事实。

当某条新闻缺少可用链接时，该条内容不进入最终可见输出。过滤后没有可见新闻的 topic section 也不应渲染。

当分数为显式非法值时，renderer 不应报错。`chat` topic 输出中，显式非数字、`NaN` 或非有限分数渲染为 `[0/10]`；缺失、`null` 或空字符串分数不进入 topic section。有效数字分数低于阈值时同样跳过。

当内容过长时，summary 应压缩为一个紧凑段落，避免 IM 群聊刷屏。

## 测试计划

- 新增或扩展 acceptance renderer 测试，覆盖 `chat` 输出模式。
- 增加 `tests/golden/daily-chat.md`，锁定标题、总结、链接三段结构。
- 验证链接行使用 `🔗 https://...`，不出现 `<https://...>`。
- 验证缺少 URL 的新闻会被过滤，且过滤后为空的 topic section 不渲染。
- 验证所有被渲染出来的 topic section 至少包含一条可见新闻。
- 验证 snippet-only 新闻不会生成超出 snippet 或 title 的额外事实。
- 验证 Podcast 无 transcript 时不会生成 transcript-backed insight。
- 验证 Podcast 有 transcript 时可以生成基于 transcript 的内容总结。
- 验证 Reddit 输出区分原链接内容和社区讨论，不把社区反应写成事实。
- 验证 Twitter/X 互动数据只有在解释传播强度或重要性时才出现。
- 验证显式非数字、`NaN` 或非有限 score 在 `chat` topic 输出中渲染为 `[0/10]`。
- 验证缺失、`null` 或空字符串 score 不进入 `chat` topic section。
- 验证 GitHub Releases 和 GitHub Trending 仍然保持短摘要，不被普通新闻规则强行扩写。
- 保留现有 Discord golden 测试，避免 `chat` 改动破坏 Discord 输出。

## 风险

更完整的中文总结会增加输出长度，在群聊里可能造成刷屏。模板需要限制每条 summary 为一个紧凑段落。

`chat` 总结质量仍然依赖最终生成阶段使用的 evidence。如果输入材料只有标题，输出必须短而谨慎。

如果把 `chat` 规则混入 `discord`，会让渠道语义变得不清晰。因此本设计选择新增模板，而不是改名或复用 Discord 模板。

## 验收标准

- 存在 `references/templates/chat.md`，明确描述通用 IM 输出格式。
- `<TEMPLATE>` 文档包含 `chat`。
- Acceptance renderer 可以生成 `chat` 样例。
- Golden 样例中的每条新闻包含标题行、内容总结和 `🔗 URL` 链接行。
- `chat` 输出不包含 `<URL>` 链接包裹格式。
- 现有 Discord 输出测试继续通过。
