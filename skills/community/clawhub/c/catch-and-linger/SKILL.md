---
name: catch-and-linger
description: Capture URLs into the user's CatchLinger bookmark collection. Resolves URLs, GitHub stars, or local Chrome/Edge bookmarks; extracts content; generates a title, summary and a few broad, reusable tags; then saves via REST or MCP. Use when the user asks to 收藏 / 收录 / 加入 CatchLinger / 保存这些链接 / 导入书签 / 同步 GitHub star / 整理收藏 / save links / bookmark this / add to CatchLinger / import bookmarks / sync GitHub stars / organize bookmarks.
license: Apache-2.0
---

# catch-and-linger

把链接收进用户的 CatchLinger 收藏系统：**解析正文 → AI 解读 → 写入统一存储**。

## 核心原则

1. **先解读，再收录；单条与批量都适用。** 服务端不抓正文、不调用任何模型。Agent 必须逐条读取网页内容，自己生成 `title` / 内容梗概 `summary`，再从梗概所表达的内容中提炼至多 3 个 `tags`，完成标签归一后才调用写入接口。书签、GitHub star 只是 URL 来源，不能跳过网页解读。
2. **标签用于聚合多篇收藏，抽象程度略高于文章关键词。** 优先用领域/技术栈，加一个确有帮助的学习方式或使用场景，例如 HashMap 源码文章用 `java`、`源码阅读`，不为单个类、方法或问题新增标签。系统没有预设分类清单，具体词汇仍由你根据内容和用户既有标签决定。
3. **但标签命名空间要克制。** 用户的标签空间是长期资产，碎片化（`gis` 与 `gis数据`、`springboot` 与 `spring boot`）会让检索越来越难用。**新增标签前必须先过一遍 `tag-resolver.mjs`**（见「标签归一」一节）—— 能复用既有标签就别新造。
4. **每个用户拥有独立的一套标签。** 其他用户的标签你既看不到也用不了。
5. **重复录入是 upsert，不会产生重复条目。** 详见「重复录入」一节。

## 输出语言 / Output language

Before capturing any links, choose the user's output language. Write every summary, natural-language tag, extraction-failure explanation, and final report in that language, even when this skill or the source page uses another language. English users receive English output; Chinese users receive Chinese output. Keep technical names such as Java, React, PostgreSQL, and GIS unchanged.

按以下优先级确定本次输出语言，并在同一批次中保持一致：

1. 用户本次明确指定的语言，例如「梗概和标签用英文」或 “Summarize and tag in English”。
2. 当前对话中用户已明确表达的语言偏好。
3. 用户本次自然语言请求的语言：英文用 `en-US`，简体中文用 `zh-CN`，繁体中文用 `zh-TW`；混合请求按主要表达语言判断。
4. 只有 URL、无语言线索时使用英文；用户后续指定语言时以其指令为准。

`summary` 和一般主题标签按上述语言生成，包括抓取失败时的限制说明；`title` 保留页面真实标题，不强制翻译。原网页的 `lang`、GitHub 仓库的编程语言、书签文件夹名称，以及本文件中的中文示例，都不是用户的输出语言设置。中文输出中的通用主题用中文（如「源码阅读」「性能优化」），技术栈名称仍用 `java` / `react` 等原名；英文输出使用 `source code` / `performance optimization` 等英文标签，不照搬中文示例。

当前 Web 的界面语言来自浏览器 Cookie / Accept-Language，`GET /account` 不返回语言偏好；API Key 通道不能据此自动读取用户在网页上选择的语言。不要把「界面支持 i18n」当成「采集结果会自动翻译」，也不要根据操作系统语言覆盖对话偏好。

标签归一必须携带本次语言，例如 `node scripts/tag-resolver.mjs resolve "database" "performance optimization" --locale en-US`。先用目标语言提炼候选，再做归一；resolver 不负责翻译。语言参数会阻止中英文标签之间的自动复用，避免 `database` 被既有「数据库」替代；中文候选同样不会被英文通用主题顶替。跨语言同义的历史标签可以保留，不为本次收录批量翻译或改名。简繁体选词由 Agent 遵循用户偏好，resolver 不做简繁转换。

## 环境准备

需要两个环境变量：

| 变量 | 说明 |
|---|---|
| `CATCHLINGER_API_BASE` | 例如 `https://<你的站点>/api/trove` |
| `CATCHLINGER_API_KEY` | `trv_` 开头的长效 API Key |
| `GITHUB_USERNAME` | 可选；GitHub 用户名。设了就能**免 Token** 读 star 列表（也可临时用 `--user` 传） |
| `GITHUB_TOKEN` | 可选；设了配额从 60 次/小时提到 5000 次/小时，也能读私密 profile 的 star |
放在环境变量里，或写进 `~/.config/catchlinger/env`（`KEY=VALUE` 格式，每行一条）。

如果缺少 `CATCHLINGER_API_KEY`，明确提示用户登录 [CatchLinger](https://catchlinger.sxyicheng.tech)，前往「我的语言 → 连接 Agent」手动生成新的 API Key；不要替用户生成或猜测 Key。

## 三种模式

根据用户意图选择模式：

### 模式 A — 单个或多个 URL

```bash
node scripts/fetch-content.mjs "<url>" ["<url2>" ...]
```

一次可传多个 URL，输出 JSON 数组；只传一个时输出单个对象。

### 模式 B — GitHub star 列表

```bash
node scripts/github-stars.mjs [--limit 50] [--user <GitHub用户名>]
```

输出 `{ mode, count, stars: [{ full_name, html_url, description, topics, language, starred_at, ... }], rateLimit }`。
每个 star 视为一个待收录链接，其 `html_url` 就是目标 URL。

**用户名从哪来（按优先级）**：

| 来源 | 说明 |
|---|---|
| `--user <name>` | 命令行显式指定 |
| `GITHUB_USERNAME` | 环境变量 |
| **CatchLinger 账号** | 调 `GET /account` 拿 `github_username` —— CatchLinger 用 GitHub OAuth 登录时服务端已经存下了它，**所以默认什么都不用配** |
| `GITHUB_TOKEN` | 上面都没有时的兜底：读认证用户自己的 star |

拿到用户名后走**公开端点** `GET /users/{username}/starred` —— **不需要 GITHUB_TOKEN**。

**两种端点**：

| 端点 | 何时用 | 要 Token 吗 | 配额 |
|---|---|---|---|
| `GET /users/{username}/starred` | 知道用户名 | **不要** | 匿名 60 次/小时；带了 Token 则 5000 次/小时 |
| `GET /user/starred` | 不知道用户名但有 Token | 要 | 5000 次/小时 |

公开端点只能读**公开 profile** 的 star；profile 是私密时它返回空列表（此时才需要 Token）。

> `401` → Token 无效或已吊销。
> `403` → 触发限流；不要无限重试。
> `404` → 用户名不存在。

> **配额提示**：列 star 列表可以免 Token，但**逐个抓仓库详情**（`fetch-content.mjs` 遇到 GitHub 链接会走 API）每个仓库消耗一次配额。star 数量多时建议配 `GITHUB_TOKEN`。

### 模式 C — 本地 Chrome / Edge 收藏夹

```bash
node scripts/read-bookmarks.mjs [--browser chrome|edge|all] [--profile Default] [--limit 200] [--folder "书签栏"]
```

输出 `{ count, total_read, errors, bookmarks: [{ url, title, folder, date_added }] }`。
浏览器正在运行时也能读取；单个浏览器失败不影响另一个。

此输出只是待处理清单，不能直接转换成保存请求。`title` 可在网页标题不可得时作为备选；`folder` 只是原收藏夹位置，不能代替正文，也不能直接充当内容标签。「工作」「学习」「待看」等文件夹名不作为默认标签；标签应由 Agent 阅读内容后提炼。

## 标准工作流

```
⓪ 确定输出语言（用户指令 / 对话偏好 / 请求语言）
        ↓
① 取得 URL 列表（模式 A / B / C）
        ↓
② 取得正文：node scripts/fetch-content.mjs "<url1>" "<url2>" ...
        ↓
③ Agent 逐条解读：真实标题 → 内容梗概 summary → 从梗概提炼 ≤3 个候选标签
        ↓
③.5 标签归一：node scripts/tag-resolver.mjs resolve "<所有候选标签>" ... --locale <输出语言>
        ↓
④ 写入：node scripts/catchlinger-api.mjs save-many '[{...}]'（标签用归一后的）
        ↓
⑤ 汇报：新增 N 条 / 更新 M 条 / 失败 K 条
```

### ② 抓正文

- GitHub 仓库链接会自动改走 GitHub API，返回结构化的仓库信息（语言 / Stars / Topics / 描述），信息质量优于 HTML 抓取。
- `extraction` 是脚本按文本长度给出的初步判断，Agent 仍需检查实际内容是否为正文，不能把登录页、验证码或错误页当成原文。
  - `full` —— 阅读返回的正文或仓库资料，再生成内容梗概；不表示原文一定完整，正文可能已截断。
  - `partial` —— 正文较短。可通过可用的浏览器或阅读工具进一步取得正文；仍无法取得时，依据 `og_description` / `meta_description` 等真实元信息整理，并在梗概中说明「未取到完整正文，仅依据页面元信息整理」。不要仅凭该标记断言页面一定是动态渲染。
  - `none` —— 抓取失败。若仍有可信的页面元信息，可以据此写有限梗概并说明限制；只有书签标题或域名时，明确写「未能抓取正文（实际原因），暂无法生成内容梗概」，不推测文章观点或功能，不强行生成主题标签。

上面的失败说明是中文示意，实际按输出语言表述。例如英文用户应收到 “Could not retrieve the article (HTTP 403); a content summary is unavailable.”，而不是中文提示。

### ③ AI 解读

对每个 URL 产出：

| 字段 | 要求 |
|---|---|
| `title` | 必填，≤300 字符。用页面真实标题；没有就用域名 + 内容类型 |
| `summary` | 本 Skill 收录时必填，≤1000 字符。Agent 阅读内容后用自己的话写成梗概，通常 2–4 句：主题是什么、主要讲了什么或提供什么能力、解决什么问题或适用什么场景；具体程度以实际读到的内容为准。不要只复述标题。抓取失败按上节如实注明 |
| `tags` | 从上述梗概中的核心主题提炼，通常 **1–2 个**，最多 **3 个**，单独保存为字符串数组。使用可聚合多篇内容的领域、技术栈、学习方式或使用场景，不必凑满；信息不足时可为空，不把标签列表拼进梗概 |

**`summary` 是内容梗概，不是采集日志。** 禁止用「从 Edge 收藏夹『xx』导入」「来自 GitHub star」「已收录」等来源说明替代梗概。采集通道保存在 `source`（如 `bookmark`），不占用 `summary` 或内容标签。

例如，实际读到的文章讨论 HashMap 扩容触发条件、容量变化和元素迁移时，可写：

```json
{
  "summary": "解析 Java HashMap 扩容的触发条件、容量变化及元素迁移过程，并结合源码说明相关实现。适合在理解哈希表机制或阅读 Java 集合源码时参考。",
  "tags": ["java", "源码阅读"],
  "source": "bookmark"
}
```

这只是字段示例，不能把其中的结论套用到未读取的网页。API 为兼容手工录入与局部更新仍允许省略 `summary`，不代表本 Skill 可以省略网页解读。

同样的已读内容，英文用户可保存为：

```json
{
  "summary": "Explains when Java HashMap resizing occurs, how capacity changes, and how entries are transferred, with references to the implementation. Useful for understanding hash tables and reading Java collection source code.",
  "tags": ["java", "source code"],
  "source": "bookmark"
}
```

### 批量收录

按能读完并核对的小批次处理（例如每批 5–10 条）：**抓取 → Agent 解读 → 梗概与候选标签 → 标签归一 → 保存 → 核对响应**，再处理下一批。不得为了数量或执行时限，把整批链接降级为来源说明或照搬文件夹标签。

保存前逐条检查梗概是否有实际内容依据、梗概和主题标签是否符合本次输出语言、标签是否由内容提炼且不超过 3 个。采集脚本只负责读取或搬运，不能用脚本拼接标题、域名、文件夹名来冒充 AI 梗概。

批次超时或响应缺失时，先核实已处理条目再续跑；完成数以服务端确认结果和链接核对为准。不能仅凭总数差异推断遗漏条目都是重复项。汇报时单独说明未能生成内容梗概的条数和原因，不将其算作成功解读。

### 标签粒度：先归组，再归一

标签是回看和检索时的入口，不是文章关键词清单。保存前先用 `node scripts/tag-resolver.mjs list` 浏览已有词汇，优先选语义合适的较宽标签，再用 resolver 检查拼写与近义词。

- 将细节留在标题和摘要里：具体类名、API、方法名、错误码、版本号、单个算法/参数，通常不另建标签。
- 优先复用合适的上位标签；已有很多细标签不等于应继续沿用同样粒度。新建前问自己：「这个标签能自然容纳多篇不同内容吗？与已有较宽标签相比，是否真的多了一个有用入口？」
- 批量采集先通览内容，收敛为一小组可复用主题，再逐条分配；避免为每个网页各造一个专属标签。
- 不粗化到失去用途，例如不用「技术」「学习」取代所有主题。稳定的技术栈或独立领域仍可作为标签；用户明确要求细分时尊重其选择。

| 内容 | 合适的候选标签 | 通常不新增的细标签 |
|---|---|---|
| Java HashMap 扩容与源码解析 | `java`、`源码阅读` | `hashmap`、`resize`、`红黑树转换` |
| Java ArrayList 扩容实现 | `java`、`源码阅读` | `arraylist`、`grow方法` |
| MySQL 某条慢 SQL 的排查 | `mysql`、`性能优化` | `某个执行计划节点`、`具体错误码` |
| React useEffect 依赖问题 | `react`、`开发实践` | `useeffect依赖数组`、`某个hook参数` |

这些是粒度示例，不是预置分类或固定词表。只选择内容确实支持的标签，随后执行下面的归一流程。

标签建议：
- 归一由服务端做（小写、去 `#`、折叠空白），你直接给有意义的名称即可。
- 中文标签完全支持。
- **来源站点不是主题标签**（掘金 / 知乎 / CSDN / 公众号……）——`items.source` 记录的是**采集通道**（`skill` / `mcp` / `manual` / `bookmark` / `github`），不是发布平台。要标注「这篇来自掘金」时可以有意识地用它，resolver 只给提示、不强制。
- **产出的是「候选标签」，必须先过「标签归一」再写入。**

### ③.5 标签归一（**必做**）

标签空间是长期资产。碎片化一旦成规模就没法收拾，所以**新增任何标签前先查一遍既有标签**：

```bash
node scripts/tag-resolver.mjs resolve "标签1" "标签2" "标签3" --locale zh-CN
# English output:
node scripts/tag-resolver.mjs resolve "database" "performance optimization" --locale en-US
```

批量场景把**所有条目用到的候选标签一次传进去**（去重由脚本处理），一次拿回整张映射表。
语言参数仅约束本次匹配，不更改服务端标签，也不翻译候选。省略 `--locale` 时脚本保留旧的跨语言匹配行为，因此本 Skill 收录时必须显式传入。

返回的每个候选有三种 `action`：

| action | 含义 | 你该怎么做 |
|---|---|---|
| `reuse` | 命名空间里已有等价标签 | **直接用 `resolved`**，不要新造 |
| `candidate` | 有相近的既有标签，但**不一定等价** | 读 `reason` 和 `candidates`：能表达你的语义就用 `resolved`；不能就换候选或新建。**不要默认新建** |
| `new` | 没有匹配的既有名称 | 仍需通过上面的粒度判断；若已有合适的较宽标签，改用它，不因 `new` 自动新建 |

配套还有 `warning` 字段：命中「来源站点名」黑名单时会提示别用。

**匹配规则**（resolver 内部逻辑，你只需理解结论）：

| 关系 | 例子 | 处理 |
|---|---|---|
| 归一后同词 | `springboot` / `spring boot` | 复用既有那一个（统一拼写） |
| 等价组 | `jdk8` → `jdk`、`gis数据` → `gis` | 统一到 `canonical` |
| 同族但不等价 | `java` / `java nio` / `java并发` | **只提示，不自动替换**——它们确实不同 |
| 上下位 | `向量数据库` ⊃ `数据库` | 给出候选，由你判断 |

等价组 / 同族组定义在 `data/tag-aliases.json`，可以随时增删：

- `equivalent` —— 真正等价的同一个概念，`canonical` 是首选写法。**命中后 resolver 直接复用 canonical**。
- `related` —— 同一族但不等价，只作提醒。
- `avoid` —— 不该作为标签的来源站点名。

> 发现新的同义标签时，**顺手把等价组补进 `data/tag-aliases.json`**，下次就自动收拢了。

### ④ 写入

单个：

```bash
node scripts/catchlinger-api.mjs save '{"url":"https://...","title":"...","summary":"...","tags":["a","b"],"source":"skill"}'
```

批量（推荐，单次 ≤50 条）：

```bash
node scripts/catchlinger-api.mjs save-many '[{"url":"...","title":"...","summary":"...","tags":["..."]}, ...]'
```

`source` 可选：`manual` / `skill` / `mcp` / `github` / `bookmark` —— 记录「这条是从哪来的」。模式 B 用 `github`，模式 C 用 `bookmark`，其他用 `skill`。

响应：

```json
{ "items": [{ "id": "...", "created": true, "tags": ["..."] }],
  "created": 1, "updated": 0, "errors": [] }
```

### ⑤ 汇报

最后向用户汇总：**新增 N 条 / 更新 M 条 / 失败 K 条**（失败时列出失败的 URL 与原因）。批量中单条失败不影响其余。

## 硬约束

| 约束 | 值 | 越界表现 |
|---|---|---|
| 单次提交条数 | ≤ 50 | 服务端拒绝，请分批 |
| 每个收藏的标签数 | ≤ 3 | `422 MAX_TAGS_EXCEEDED`，请砍到 3 个 |
| 新增标签前必须过 resolver | `action=reuse` 不得新造同名标签 | 命名空间碎片化 |
| title 长度 | ≤ 300 | 422 |
| summary 长度 | ≤ 1000 | 422 |

超限时**先砍标签再重试**，不要盲目重试同一个请求。

## 重复录入（upsert）

同一 URL 再次提交**不会**新建重复条目，而是更新既有条目。字段级规则：

| 字段 | 没传时 | 传了时 |
|---|---|---|
| `title` | 保留原值 | 覆盖（非空才覆盖） |
| `summary` | 保留原值 | 覆盖（非空才覆盖） |
| `tags` | **完全保留原标签** | 整体替换该条标签 |
| `notes` | 不追加 | 追加一条新笔记（笔记不覆盖） |
| `collected_at` / 归档状态 / 已读状态 / 点击次数 | **不变** | 仍不变 |

要点：
- **没传 `tags` 就不会清空已有标签** —— 只补标题/摘要的局部更新很安全。
- 响应里的 `created` 告诉你这次是新建（`true`）还是更新（`false`）。
- 重录**不会**重置收藏时间，所以超期提醒不会被反复导入刷掉。

## 排查

```bash
node scripts/catchlinger-api.mjs search --q 关键词 --limit 10   # 确认是否已收录
node scripts/catchlinger-api.mjs stats                          # 总数 / 未读 / 超期
node scripts/catchlinger-api.mjs tags                           # 既有标签（完整 JSON）
```

标签命名空间工具：

```bash
node scripts/tag-resolver.mjs list                             # 紧凑列出既有标签（name×count）
node scripts/tag-resolver.mjs resolve "标签" [...]              # 解析候选标签 → 复用哪个既有标签
node scripts/tag-resolver.mjs audit                            # 找出既有标签里的近重复分组
node scripts/tag-resolver.mjs merge <from> <to> [--dry-run]   # 把 from 合并进 to
```

`merge` 会把挂了 `from` 的收藏逐条改挂到 `to`，再删掉 `from` 标签。
**先 `--dry-run` 看影响面**（会打印受影响的条目与新的标签集），确认后再执行。
注意 Agent 通道每个收藏至多 3 个标签：合并不会增加标签数，但如果某条收藏本来就超过 3 个，合并会失败并被单独列出（需在 Web 端手工调整）。

接口返回错误时，脚本会打印 `{ "error": { "code": "...", "message": "..." } }` 并以非 0 退出码结束。常见码：

| 码 | 含义 | 处理 |
|---|---|---|
| `UNAUTHORIZED` | API Key 无效或已吊销 | 明确要求用户登录 [CatchLinger](https://catchlinger.sxyicheng.tech)，前往「我的语言 → 连接 Agent」手动生成新的 API Key，再更新 `~/.config/catchlinger/env`；不要替用户生成或猜测 Key。 |
| `MAX_TAGS_EXCEEDED` | 标签超过 3 个 | 砍到 3 个再提交 |
| `VALIDATION_ERROR` | 字段不合法 | 按 message 修正 |
| `INVALID_SCHEME` | 不是 http/https 链接 | 跳过该 URL |

## 也可以走 MCP

如果 MCP 已配置（`catchlinger` 服务器），同样的能力以工具形式提供：`catchlinger_save`、`catchlinger_save_many`、`catchlinger_search`、`catchlinger_list_tags`、`catchlinger_manage_tag`、`catchlinger_get`、`catchlinger_update`、`catchlinger_archive`、`catchlinger_delete`、`catchlinger_add_note`、`catchlinger_mark_read`、`catchlinger_stats`、`catchlinger_list_reminders`、`catchlinger_account`。

MCP 使用与 Skill 的 `CATCHLINGER_API_KEY` 相同的 `trv_` API Key，通过 `Authorization: Bearer <API Key>` 发送；工具所需 scope 必须已授予。REST 与 MCP 走同一套 service 层。
