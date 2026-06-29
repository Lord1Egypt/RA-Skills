# AI 胶囊

[English](README.md)

一个 AI agent skill，根据**你真正关心的内容**筛选每天的 AI 资讯。

告诉它你的角色和熟悉的方向——它会对每篇文章按你的画像评分，把最相关的内容排在最前面。**所有文章都会出现在日报里，不会漏掉任何一条**，只是顺序不同。同样是 40 篇文章，做 Agent 工程的人和做模型微调的人看到的排序完全不同。

默认专注于 AI 行业资讯（HuggingFace、OpenAI、Anthropic、DeepMind、HN、Reddit……），但数据源系统本身与行业无关——放一个 `sources/finance.yaml` 或 `sources/crypto.yaml` 进去，同样的评分和日报流程就能跑起来。

支持 **Claude Code** 和 **OpenClaw**，任何兼容 `SKILL.md` 的 agent 运行时均可使用。

每天从 16 个来源抓取内容（HuggingFace 论文、OpenAI、Anthropic、DeepMind、Simon Willison、GitHub Trending、HN、Reddit 等），对每篇文章按 7 个维度打分（相关性、实用性、新颖性、深度、震撼感、认知冲击、跨界启发），再结合你的背景算出**个人匹配度**。最终你看到的日报里，对你最有用的文章排在最前面。

---

## 工作原理

每篇文章得到一个 **RUND+WPS** 分数：

| 维度 | 衡量什么 |
|-----|---------|
| R — 相关性 | 与你的技术栈匹配吗？ |
| U — 实用性 | 看完能直接做什么？ |
| N — 新颖性 | 这是真正的新信息吗？ |
| D — 深度 | 论文/源码级，还是博客摘要？ |
| W — 震撼感 | 违反直觉或算法优雅？ |
| P — 认知冲击 | 改变你的思维方式？ |
| S — 跨界启发 | 意想不到的领域组合？ |

**个人匹配度（F）** 根据你的 `familiar_areas` 配置对文章重新排序。你做 RAG 的话，Agent 架构文章比模型预训练文章排得更靠前。

每张卡片附带行动标签：
- `TRY` — 有 GitHub repo 或可运行代码
- `READ` — 值得完整阅读的深度内容
- `SCAN` — 30 秒扫标题+摘要即可

---

## 环境要求

- [Claude Code](https://claude.ai/code) 或 [OpenClaw](https://openclaw.ai)
- Python 3.9+

---

## 安装

### Claude Code

```
/plugin marketplace add WebPudge/ai-capsule
/plugin install ai-capsule@ai-capsule
```

然后初始化 Python 环境：

```bash
bash ~/.claude/plugins/ai-capsule/scripts/setup-env.sh
```

然后说 `daily`。

### OpenClaw

```bash
openclaw skills install ai-capsule
cd ~/.openclaw/skills/ai-capsule
bash scripts/setup-env.sh
```

然后在 OpenClaw 会话中说 `daily`。

---

Claude 会引导你完成简短配置（角色、熟悉方向、输出语言），把配置写到 `~/.ai-capsule/config.yaml`。你的数据存在 `~/.ai-capsule/data/`，与 skill 本体分离，升级 skill 不会丢数据。

---

## 使用方式

对 Claude 说：

| 说什么 | 发生什么 |
|-------|---------|
| `daily` 或 `每日模式` | 抓取今日 AI 资讯，全部评分，输出排序日报 |
| `reconfigure` 或 `重新配置` | 重新走一遍配置引导 |
| 粘贴 URL | 对单篇文章评分 |
| 粘贴文章正文 | 对单篇文章评分 |

---

## 日报示例

以下是 2026 年 6 月实际生成的日报片段（engineer 视角，熟悉 LLM 应用开发 / RAG / Agent 框架）：

---

### #1 ★★★★☆ 6.9/10 · [Conan — Claude Code 可视化操控界面](https://conan.sh)

🔗 [https://conan.sh](https://conan.sh)
📌 **Product Hunt 日榜** · engineer · 学习模式 · 🎯 **TRY**
`匹配:9` `实用:8` `新颖:7` `深度:5` | `震撼:6` `认知:6` `跨界:3`

- **匹配：** 直接是 Claude Code 的配套工具，对重度使用 Claude Code 的工程师直接有用
- **实用：** 可下载安装的 macOS 应用，GitHub Releases 提供 dmg，今天就能用
- **新颖：** Claude Code 的可视化 HUD 是目前缺少的配套工具，Context 窗口监控是痛点解法
- **深度：** 产品页面，功能描述清晰但无技术实现细节
- **震撼：** Claude Code 上下文监控可视化解决了开发者实际痛点，完成度超出产品公告预期
- **认知：** 把 AI 编程工具的运行状态可视化为 HUD 的思路，改变了"黑盒"操作体验
- **跨界：** 无跨领域启发

**内容：** macOS 原生应用，为 Claude Code 提供实时 HUD，包含 Timeline（提示/工具调用流式展示）、Context 窗口用量监控、Pulse 吞吐量、Skills & MCP 可视化，$29 买断制

**价值：** 你重度使用 Claude Code——装上 Conan 立刻能看清每次对话消耗了多少 context、哪些工具被调用了多少次，帮你判断什么时候该 /compact，避免在 context 快满时才意识到浪费了大段工作

---

### #3 ★★★★☆ 7.0/10 · [Mapping SQLite result columns back to their source table.column](https://simonwillison.net/2026/Jun/13/sqlite-column-provenance/)

🔗 [https://simonwillison.net/2026/Jun/13/sqlite-column-provenance/](https://simonwillison.net/2026/Jun/13/sqlite-column-provenance/)
📌 **Simon Willison** · engineer · 学习模式 · 🎯 **TRY**
`匹配:7` `实用:8` `新颖:7` `深度:7` | `震撼:5` `认知:5` `跨界:3`

- **匹配：** 数据库查询溯源是 RAG 和 Agent 工具调用中 SQL 结果处理的实际问题
- **实用：** 三种方案均有代码，GitHub 仓库 column_provenance.py 可直接取用
- **新颖：** 通过 ctypes 桥接 sqlite3_column_table_name() 是多数开发者不知道的技巧
- **深度：** 分析了三种方案的原理和适用条件，有实际代码支撑
- **震撼：** ctypes 绕过 Python 标准库的方式有一定技巧性，但属于已知模式
- **认知：** 揭示 SQLite 内部有 SQLITE_ENABLE_COLUMN_METADATA 标志这一隐藏能力
- **跨界：** 无跨领域视角

**内容：** Simon Willison 用 Claude Code 研究如何将 SQL 查询结果列反向映射到来源 table.column，探索了 apsw、ctypes 桥接 SQLite C API、EXPLAIN 分析三种方案，实现代码发布在 GitHub

**价值：** 你做 RAG 时 Agent 工具调用经常要执行 SQL 并解释结果——column_provenance.py 可以直接拿来用，让 Agent 返回"users.name 来自 users 表"而不是裸列名，对多表 JOIN 结果的可解释性有直接提升

---

### #5 ★★★★☆ 6.9/10 · [Why AI hasn't replaced software engineers, and won't](https://simonwillison.net/2026/Jun/14/why-ai-hasnt-replaced-software-engineers/)

🔗 [https://simonwillison.net/2026/Jun/14/why-ai-hasnt-replaced-software-engineers/](https://simonwillison.net/2026/Jun/14/why-ai-hasnt-replaced-software-engineers/)
📌 **Simon Willison** · engineer · 学习模式 · 🎯 **READ**
`匹配:8` `实用:6` `新颖:6` `深度:7` | `震撼:6` `认知:8` `跨界:3`

- **匹配：** 直接讨论 AI 对软件工程师角色的影响，工程师读者的核心关切
- **实用：** 提供了 WARN 法案这一具体数据来源，以及决策/验证/理解三个框架维度
- **新颖：** 用三个具体认知瓶颈反驳流行的"阈值论"，不是主流框架内的通常论点
- **深度：** Arvind Narayanan 深度分析，有学术背景，Simon 补充自身观点，论证层次完整
- **震撼：** 无违反直觉的颠覆性发现，三点框架属于预期内的分析
- **认知：** "决策与问责比代码输入更核心"的视角对重新定位工程师价值有冲击力
- **跨界：** 引入劳动经济学数据（WARN法案）分析技术趋势，属于相邻领域借鉴但不算意外

**内容：** Arvind Narayanan 和 Sayash Kappor 论证 AI 尚未替代软件工程师的三个根本瓶颈：决策规范、验证问责、深度上下文理解；以纽约州 WARN 法案数据（零家公司标注 AI 原因）为实证支撑

**价值：** 你是 AI 应用工程师，这篇帮你把"为什么你没被替代"说清楚——决策规范和验证问责正是你每天在做的事，用这个框架跟 PM/老板/客户解释 AI 工具的边界很有说服力

---

同样这 31 篇文章，换成做模型微调的研究员来看，排序会完全不同——上面的 SQLite 和 Agent 工具内容会排到后面，模型架构或训练相关的文章会浮到前列。

---

## 配置文件

配置存在 `~/.ai-capsule/config.yaml`（首次运行时自动创建）：

```yaml
initialized: true
default_identity: engineer      # engineer | pm | researcher | learner | founder
default_purpose: learn          # learn | solve | scout
output_language: zh             # zh | en | 其他语言名称
familiar_areas:
  - LLM 应用开发
  - RAG
  - Agent 框架
data_dir: ~/.ai-capsule/data
```

自定义配置路径：`export AI_CAPSULE_CONFIG=/path/to/config.yaml`

### 示例：LLM 应用工程师

```yaml
initialized: true
default_identity: engineer
default_purpose: learn
output_language: zh
familiar_areas:
  - LLM 应用开发
  - RAG
  - Agent 框架
  - Prompt Engineering
dislikes: 纯营销软文、没有代码的趋势分析
data_dir: ~/.ai-capsule/data
```

使用这份配置，RAG 检索策略或 Agent 工具调用的文章排名会高于泛泛的 AI 行业动态。一篇语音识别论文即使整体质量不错，个人匹配度评分也会很低——它仍然会出现在日报里，只是排在靠后的位置。

---

## 数据来源

### 内置 AI 来源（开箱即用 16 个）

**RSS（自动抓取）：** HuggingFace Papers · OpenAI Blog · Microsoft Research · Ben's Bites · Hacker News

**URL 抓取：** Anthropic（3 个 feed）· Google DeepMind · Meta AI · Simon Willison · Eugene Yan · Chip Huyen · Product Hunt 日榜 · GitHub Trending

**X/Twitter：** @Zai_org · @dotey · @_akhaliq · @omarsar0 · @karpathy（各最新 5 条推文）

**搜索：** Reddit LocalLLaMA

### 扩展到其他行业

数据源按行业文件组织，新建 `sources/{行业}.yaml` 即可扩展：

```bash
# 向 AI 行业列表新增一个来源
bash scripts/add-source.sh --industry ai --type rss --name "我的博客" --url https://example.com/feed

# 开辟新行业（金融、加密、安全等）
cp sources/ai.yaml sources/finance.yaml
# 然后编辑 sources/finance.yaml，填入对应领域的 feed

# 对指定行业运行日报
# 对 Claude 说 "daily --industry finance"
```

## X/Twitter 代理配置

如果你的网络无法直接访问 X/Twitter，twitter-cli 底层的 HTTP 库（curl-cffi）不会自动读取系统代理设置。可以配置代理地址：

```bash
export https_proxy=http://127.0.0.1:7890
```

或者写入 shell 配置文件（`~/.zshrc` / `~/.bashrc`）中：

```bash
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
```

`fetch.py` 会自动检测 `https_proxy` / `HTTPS_PROXY` 环境变量；如未设置，会尝试自动探测本地常见的代理端口（ClashX 7890、Surge 6152 等）。

四种来源类型在任意行业都通用：

| 类型 | 由谁抓取 | 适用场景 |
|------|---------|---------|
| `rss` | `fetch.py` 自动 | RSS/Atom feed、API |
| `webfetch` | Agent 运行时 | 无 RSS 的博客、榜单、页面 |
| `tavily` | Agent 运行时 | Reddit、论坛、基于搜索的发现 |
| `twitter` | `fetch.py` 自动 | X/Twitter 账号时间线——通过 fetch.py 脚本调用 twitter-cli + browser-cookie3 |

---

## Agent 兼容性

适配任何能抓 URL 和执行 Bash 的 agent：

| 运行时 | 使用的抓取工具 |
|-------|-------------|
| Claude Code | `WebFetch` |
| Codex / shell agent | `curl` + Python 解析 |
| Tavily agent | `tavily_extract` |
| OpenClaw | 自动 fallback 到系统 Python |

---

## 项目结构

```
ai-capsule/
  SKILL.md              # skill 入口（Claude 的执行指令）
  fetch.py              # RSS/API 抓取脚本
  sources_extract.py    # 数据源配置读取器
  requirements.txt
  scripts/
    setup-env.sh        # 一次性 Python 环境初始化
    add-source.sh       # 新增数据源
  sections/
    scoring.md          # RUND+WPS+F 评分框架
    output-format.md    # 卡片格式规范
    daily-mode.md       # 每日模式执行流程
  sources/
    ai.yaml             # AI 行业数据源列表
```

用户数据（`~/.ai-capsule/`）：
```
config.yaml             # 你的配置和偏好
data/
  daily-YYYY-MM-DD.md   # 每日日报
  history.jsonl         # 所有已评分文章
  dedup-titles.txt      # 已见标题（防止重复评分）
```

---

## 隐私声明

**X/Twitter 数据源：** 使用 X/Twitter 数据源时，`fetch.py` 会通过 `browser-cookie3` 读取本机 Chrome 浏览器 Cookie 数据库。仅读取 `x.com` 域名的 Cookie，这些 Cookie 以环境变量形式传递给 `twitter-cli`（仅存于进程内存），不会写入磁盘、上传或分享。如果 Cookie 过期，日报末尾会提示重新登录 x.com。

其他所有数据源通过 RSS、HTTP 请求或搜索 API 抓取公开内容。你的配置和评分历史存储在本地 `~/.ai-capsule/`。

## License

MIT
