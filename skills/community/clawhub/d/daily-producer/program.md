# Daily Producer — 完整技术文档

本文档是 daily-producer skill 的完整技术说明，详细描述系统的设计理念、每个环节的原理、数据流转方式、以及对应的文件和脚本。

---

## 一、系统概述

### 目标

为用户生成一份**个性化的每日 AI 资讯日报**。从用户画像出发，自动从 20+ 个信息平台采集资讯候选，经过时间筛选、深抓正文、去噪打分后，由 AI 选出最有价值的 15 条，生成结构化 JSON 并渲染为 HTML 页面。

### 核心设计原则

1. **画像驱动**：所有采集、筛选、排序、改写都基于 `config/profile.yaml` 中的用户画像，不做通用推荐
2. **脚本 + AI 协作**：机械性工作（采集、解析、筛选、校验）由 Python 脚本完成，需要语义理解的工作（选稿、写摘要、判断相关性）由 AI 完成
3. **全程留痕**：每个中间环节的产物都保存到 `output/raw/`，可追溯、可复盘
4. **通用去噪**：噪音过滤不依赖硬编码黑名单，完全基于 profile 关键词匹配，换任何画像都适用

### 技术栈

| 组件 | 技术 | 用途 |
|------|------|------|
| 采集引擎 | opencli (npm) | 通过 Chrome CDP 连接本地浏览器，复用登录态采集 73+ 平台 |
| 浏览器 | Chrome + Xvfb | 服务器无桌面环境下运行 Chrome，noVNC 远程登录网站 |
| 脚本 | Python 3.10+ | 数据处理流水线（7 个脚本） |
| AI | 大语言模型 | 选稿、写摘要、生成 sidebar |
| 渲染 | Python (render_daily.py) | JSON → HTML |

---

## 二、用户画像 (Profile)

### 文件位置

`config/profile.yaml`

### 结构模板

`reference/profile_template.yaml`

### 核心设计

画像分为四部分：

**第一部分：用户是谁（关心什么）**

```yaml
role: "AI 行业观察者"
role_context: "主要以个人视角持续关注 AI 行业动态..."

topics:
  - name: "大模型与模型能力演进"
    priority: high
    keywords:
      cn: ["大模型", "基础模型", "OpenAI", ...]
      en: ["large language model", "foundation model", "OpenAI", ...]

exclude_topics:
  - "不与 AI 相关的内容"
```

- `topics` 是整个系统的核心输入，所有关键词从这里获取
- `keywords` 分 cn/en 两组：cn 分发给国内平台搜索，en 分发给国外平台搜索
- 同一概念中英文各写一遍（如"大模型" + "large language model"）
- 品牌名两边都写（如 "OpenAI"）

**第二部分：去哪里找（信息源）**

```yaml
sources:
  platforms:        # opencli 原生支持的平台
    cn: [微博, 小红书, B站, 知乎, ...]
    global: [Twitter, Reddit, Hacker News, ...]
  websites:         # 通过 Google site: 搜索 + web read 采集
    cn: [机器之心, 量子位, InfoQ AI, ...]
    global: [OpenAI News, Anthropic News, TechCrunch, ...]
```

- platforms 带 opencli 命令模板（hot/search 等），脚本直接调用
- websites 走 `opencli google search "site:域名 关键词 after:日期"` + `opencli web read`
- **关键词不在 sources 里重复**，统一从 topics 获取

**第三部分：采集规则**

```yaml
collection:
  window_days: 3
  priority_order: [官方确认, 高讨论度, 开源实践, 背景报道]
  exclude_rules: [纯搬运, 情绪内容, 弱相关, 旧闻翻炒]
```

**第四部分：运行配置**

daily、pipeline、server、feishu 等固定参数。

### 初始化流程

当 `config/profile.yaml` 不存在时，按 `init/daily-init.md` 引导用户：
1. 环境检查（Python、opencli、飞书工具）
2. 画像推断（飞书 KB 自动推断 或 对话引导）
3. 群聊绑定（可选）
4. 平台选择（展示 `reference/opencli_platforms.yaml` 全部 31 个平台供选择）
5. 写入 `config/profile.yaml`（按 `reference/profile_template.yaml` 结构）

---

## 三、生产流水线

### 数据流

```
profile.yaml (用户画像)
    │
    ├─ topics.keywords.cn ──→ 国内平台搜索（微博/小红书/B站/知乎/...）
    ├─ topics.keywords.en ──→ 国外平台搜索（Twitter/Reddit/HN/...）
    └─ sources.websites    ──→ Google site: 搜索 + web read
    │
    ↓ 汇合
{date}_index.txt (~950 条原始候选)
    │
    ↓ 时间筛选（过滤超 3 天 + 无时间字段的）
{date}_index_filtered.txt (~130 条)
    │
    ↓ 平台类直接保留 / 网站类 web read 深抓
{date}_detail.txt (~90 条，含正文)
    │
    ↓ 去噪（profile 关键词匹配）+ 打分排序
{date}_candidates.json (~70 条，结构化 JSON)
    │
    ↓ AI 选 15 条 + 写 summary + 生成 sidebar
{date}.json (最终日报)
    │
    ↓ 校验 → 渲染
{date}.html (日报页面)
```

### Step 01: 生成搜索查询

**脚本：** `scripts/build_queries.py`
**文档：** `reference/pipeline/01_build_queries.md`

**原理：**
从 profile 的 `topics[*].keywords` 提取关键词，按 cn/en 分组生成两类查询：

1. **platform 查询**（纯关键词，不带日期）
   - 用于 opencli 平台原生搜索（`opencli weibo search "大模型"`）
   - 不带日期是因为平台搜索会把日期文本当作搜索词的一部分，反而影响结果
   - 时间过滤交给后续的 filter_index.py

2. **google 查询**（带 `after:YYYY-MM-DD`）
   - 用于 `opencli google search`
   - Google 能识别 `after:` 语法做时间过滤

**关键词数量控制：**
- high priority topic：全部关键词
- medium：前 3 个
- low：前 1 个
- high 额外生成组合查询（如 `大模型 基础模型`）

**输出：** `output/raw/{date}_queries.txt`（默认自动保存）

---

### Step 02: 采集候选池

**脚本：** `scripts/collect_sources_with_opencli.py`
**文档：** `reference/pipeline/02_collect_sources.md`
**平台字段参考：** `reference/opencli_output_formats.md`

**原理：**
读取 profile 中的 `sources.platforms` 和 `sources.websites`，对每个信息源执行 opencli 命令采集资讯。

**采集方式：**

| 来源类型 | 采集方式 | 示例 |
|---------|---------|------|
| 平台 (platforms) | opencli 原生命令 | `opencli weibo search "大模型" --limit 10 -f json` |
| 平台热门 | opencli 热榜命令 | `opencli weibo hot --limit 30 -f json` |
| 网站 (websites) | Google site: 搜索 | `opencli google search "site:qbitai.com 大模型 after:2026-04-04" -f json` |
| 网站首页 | web read 直抓 | `opencli web read --url "https://www.qbitai.com/"` |

**关键词分发：**
- `keywords.cn` → 国内平台（微博/小红书/B站/知乎/即刻/V2EX/36氪）
- `keywords.en` → 国外平台（Twitter/Reddit/HN/YouTube/arXiv/Reuters）
- `keywords.cn[:3]` → 国内网站的 Google site: 搜索
- `keywords.en[:3]` → 国外网站的 Google site: 搜索

**特殊处理：**
- **Reddit**：自动探测 opencli reddit 是否可用。不通（服务器在国内直连被拦截）则切换到 Reddit JSON API + HTTP 代理（`PROXY_CONFIG` 配置）。API 模式反而多了 `created_utc` 时间字段。
- **限流防护**：每次 opencli 请求间隔 3 秒（`REQUEST_DELAY`）
- **关键词数量**：`--max-keywords` 参数控制每个语言组最多搜多少个词（默认 15，测试时可用 5）

**各平台返回字段差异很大**，脚本统一提取：

| 字段 | 提取来源（按优先级） |
|------|-------------------|
| title | title → word → name |
| text | text（Twitter 推文全文等） |
| author | author → channel |
| time | created_at → time → published_at → published → date → created_utc(转换) |
| hot | hot_value → likes → views → score → play → heat → votes → comments |
| url | url |

详细的各平台字段和时间格式见 `reference/opencli_output_formats.md`。

**输出：** `output/raw/{date}_index.txt`

---

### Step 03: 时间筛选

**脚本：** `scripts/filter_index.py`
**文档：** `reference/pipeline/03_filter_index.md`

**原理：**
解析 index.txt 中每条候选的 `time:` 字段，过滤掉超出时间窗口（默认 3 天）的旧内容。

**三种处理方式：**

| 条目类型 | 判断 | 处理 |
|---------|------|------|
| 有时间且在窗口内 | time 能解析且 >= cutoff | 保留，标记 `time_status: in_window` |
| 有时间但超出窗口 | time 能解析且 < cutoff | 过滤 |
| 无时间字段 | time 缺失或无法解析 | **过滤**（宁缺毋滥） |
| 网站类 | region == "website" | **保留**，标记 `time_status: google_filtered`（Google 搜索自带 `after:` 过滤） |

**时间格式解析：**
`parse_time` 函数支持 12 种时间格式，覆盖 Twitter（英文日期）、小红书（ISO）、微博（中文月日/相对时间/今天昨天）、YouTube（英文相对时间）、Reddit API（Unix 时间戳转换后的无秒格式）、Google news（RFC 2822）等。

**为什么无时间字段要过滤：**
B站搜索、知乎搜索、HN、V2EX 等平台的 opencli 适配器不返回时间字段。虽然可能有新内容，但无法验证时效性，全部保留会引入大量旧内容噪音。宁可少几条也不要混入过期信息。

**输出：** `output/raw/{date}_index_filtered.txt`

---

### Step 04: 深抓正文

**脚本：** `scripts/collect_detail.py`
**文档：** `reference/pipeline/04_collect_detail.md`

**原理：**
filtered index 中的条目分两类：

1. **平台类条目**（`time_status: in_window`）：已有完整内容（微博全文、Twitter 推文、Reddit 帖子标题），直接复制到 detail，不做额外请求。

2. **网站类条目**（`time_status: google_filtered`）：来自 Google site: 搜索，只有标题 + URL + snippet，需要用 `opencli web read --url` 抓取正文。

**深抓流程：**
1. 从 filtered index 中提取所有网站类条目的 URL
2. 按 URL 去重（同一篇文章被不同关键词搜到，URL 相同只抓一次）
3. 逐个执行 `opencli web read --url`，每次间隔 3 秒
4. 正文截取前 2000 字符保存（避免 detail.txt 过大）
5. 标记 `fetch_status: success / FAILED`

**常见失败：** OpenAI community、Anthropic 官网、部分 TechCrunch 文章有反爬机制，`opencli web read` 会超时。失败的条目保留但标记失败，不影响后续流程（标题和 snippet 仍可用于 AI 判断）。

**输出：** `output/raw/{date}_detail.txt`

---

### Step 05: 去噪打分

**脚本：** `scripts/prepare_payload.py`
**文档：** `reference/pipeline/05_prepare_payload.md`

**原理：**
从 detail.txt 中解析所有候选条目，基于 profile 关键词匹配度过滤噪音，按热度 + 关键词匹配打分排序，输出结构化 JSON。

**去噪逻辑（核心设计）：**

不使用硬编码黑名单（如"r/nfl 是体育"），完全基于 profile 关键词匹配，**通用于任何用户画像**。

核心概念——**具体关键词 vs 泛义关键词**：
- 具体关键词：含中文（"智能体"）、含大写品牌名（"OpenAI"）、多词短语（"AI coding"）
- 泛义关键词：短的常见英文单词（agent, model, tool, product）

泛义关键词单独命中不可靠——"agent" 可能指经纪人/特工/执法人员，需要和其他关键词共同出现才算有效。

**噪音判断规则：**

| 条目类型 | 保留条件 |
|---------|---------|
| 标题为空 | → 过滤 |
| 命中 exclude_topics | → 过滤 |
| 网站类（region=website） | → 直接保留（Google 已过滤） |
| 平台搜索结果（有 keyword） | 宽松：搜索词在内容中出现，或命中 ≥1 个 profile 关键词 |
| 热门/趋势类（无 keyword） | 严格：命中 ≥1 个具体关键词，或命中 ≥2 个任意关键词 |

**打分：**

```
得分 = 热度分(0-50) + 关键词匹配分(0-30) + 来源可信度分(0-5)
```

- 热度分：`min(50, log10(hot+1) * 10)`，对数归一化，防止单一超高热度帖子垄断
- 关键词匹配：每命中 1 个 +5，最高 30
- 可信度：tier-1 来源（Twitter、微博、量子位等）+5

**不去重**：同一事件在多平台出现时全部保留，因为多源出现 = 更可靠，交叉验证在 AI 生成 JSON 阶段完成。

**输出：** `output/raw/{date}_candidates.json`（结构化 JSON，含 `ai_todo` 指令告诉 AI 下一步做什么）

---

### Step 06: AI 生成日报 JSON

**无脚本，由 AI 执行**
**文档：** `reference/pipeline/06_generate_json.md`
**结构示例：** `reference/daily_payload_example.json`

**原理：**
这是整个流水线中唯一需要 AI 完成的步骤。AI 读取 candidates.json（~70 条去噪后的候选）+ profile.yaml（用户画像），完成以下任务：

1. **选稿**（从 ~70 条选 15 条）
   - 跳过明显噪音（如 "Agent" 指经纪人的误命中条目）
   - 同一事件多平台出现 → 合并为一条，记录多源交叉验证
   - 按优先级分配：major(2-3) > notable(3-5) > normal(5-7) > minor(0-2)
   - 确保 topics 覆盖均衡

2. **写摘要**
   - `what_happened`：事实描述，不加观点
   - `why_it_matters`：对行业/用户的影响

3. **写 relevance**：与用户画像（role + role_context）的具体关系

4. **生成 sidebar**
   - overview（3 条速览）
   - actions（3-4 条行动建议，每条含可执行的 prompt）
   - trends（rising/cooling/steady + insight）

5. **标注 credibility**
   - 多源交叉验证 → high
   - 单源可信 → medium
   - 泄露/未确认 → low

**输出：** `output/daily/{date}.json`

---

### Step 07: 校验 JSON

**脚本：** `scripts/validate_payload.py`
**文档：** `reference/pipeline/07_validate_payload.md`

**原理：**
校验 AI 生成的 JSON 是否符合渲染器契约。检查项包括：

- meta：date/date_label/role 非空
- left_sidebar：overview(≥2)、actions(≥2，type 合法)、trends(rising/cooling/steady + insight)
- articles：≥5 条，每条有 id(唯一)/title/priority(合法值)/source/url(http开头)/summary(what+why)/relevance/tags
- data_sources：非空数组

**校验失败时：** 输出具体错误列表（如 `[articles[2].summary.why_it_matters] 缺失`），AI 修改后重新校验，直到通过。

**输出：** stdout（通过/失败 + 统计）

---

### Step 08: 渲染 HTML

**脚本：** `scripts/render_daily.py`
**文档：** `reference/pipeline/08_render_html.md`
**视觉基线：** `reference/daily_example.html`

**原理：**
读取日报 JSON，按模板渲染为 HTML 页面。页面包含：
- 顶部 header（日期、角色）
- 左侧栏（速览、行动建议、趋势雷达）
- 右侧文章卡片流（按 priority 排列）
- 页脚数据来源

旧 HTML 自动归档到 `output/archive/`。

渲染器内置时间窗口校验，超出 3 天的 article 会输出警告。`--force` 参数可跳过警告继续渲染。

**输出：** `output/daily/{date}.html`

---

## 四、opencli 采集引擎

### 架构

```
opencli (npm 全局包)
    │
    ├── Chrome (Xvfb 虚拟显示)
    │   ├── Browser Bridge 扩展 (CDP 通信)
    │   └── 已登录的网站 session (通过 noVNC 登录)
    │
    ├── Daemon (端口 19825)
    │
    └── 73+ 平台适配器
        ├── 社交媒体: twitter, weibo, xiaohongshu, ...
        ├── 视频: bilibili, youtube, douyin, ...
        ├── 技术社区: hackernews, reddit, v2ex, stackoverflow, ...
        ├── 新闻媒体: bbc, bloomberg, reuters, 36kr, ...
        ├── 学术: arxiv, ...
        ├── 搜索: google search/news/trends
        └── 通用: web read (任意 URL → Markdown)
```

### 连接检查

```bash
opencli doctor
# [OK] Daemon: running on port 19825
# [OK] Extension: connected (v1.5.5)
# [OK] Connectivity: connected
```

### 保活机制

`/root/opencli-keepalive.sh` 通过 crontab 每分钟检查，Xvfb/Chrome/x11vnc/websockify/daemon 任一挂掉自动重启。

### 平台目录

`reference/opencli_platforms.yaml` 列出了全部 31 个可用平台（12 国内 + 17 国外 + 2 通用），每个含 id、名称、描述、分类、登录要求、命令模板。

### 各平台输出字段

`reference/opencli_output_formats.md` 记录了每个平台每个命令的 JSON 输出字段、时间字段名和格式。在 2026-04-05 全量采集中实测验证过。

---

## 五、文件索引

### 核心配置

| 文件 | 用途 |
|------|------|
| `config/profile.yaml` | 用户画像（topics/keywords/sources） |
| `reference/profile_template.yaml` | profile 结构模板 |
| `reference/opencli_platforms.yaml` | 全部 31 个平台目录 |

### 流水线脚本

| 脚本 | 步骤 | 输入 | 输出 |
|------|------|------|------|
| `scripts/build_queries.py` | 01 | profile.yaml | `raw/{date}_queries.txt` |
| `scripts/collect_sources_with_opencli.py` | 02 | profile.yaml | `raw/{date}_index.txt` |
| `scripts/filter_index.py` | 03 | `raw/{date}_index.txt` | `raw/{date}_index_filtered.txt` |
| `scripts/collect_detail.py` | 04 | `raw/{date}_index_filtered.txt` | `raw/{date}_detail.txt` |
| `scripts/prepare_payload.py` | 05 | `raw/{date}_detail.txt` + profile | `raw/{date}_candidates.json` |
| `scripts/validate_payload.py` | 07 | `daily/{date}.json` | stdout |
| `scripts/render_daily.py` | 08 | `daily/{date}.json` | `daily/{date}.html` |

### 流水线文档

| 文档 | 内容 |
|------|------|
| `reference/pipeline/00_overview.md` | 总览 + 一键执行命令 |
| `reference/pipeline/01_build_queries.md` | 关键词生成逻辑 |
| `reference/pipeline/02_collect_sources.md` | 各平台采集方式 |
| `reference/pipeline/03_filter_index.md` | 时间格式解析、筛选规则 |
| `reference/pipeline/04_collect_detail.md` | 平台类 vs 网站类处理 |
| `reference/pipeline/05_prepare_payload.md` | 去噪规则、打分公式 |
| `reference/pipeline/06_generate_json.md` | AI 选稿和 JSON 生成规则 |
| `reference/pipeline/07_validate_payload.md` | JSON 校验项清单 |
| `reference/pipeline/08_render_html.md` | 渲染参数和时间窗口警告 |

### 参考文档

| 文档 | 内容 |
|------|------|
| `reference/opencli_output_formats.md` | 各平台 JSON 字段、时间格式（实测验证） |
| `reference/daily_payload_example.json` | 日报 JSON 结构示例 |
| `reference/daily_example.html` | HTML 视觉基线 |
| `reference/daily_collection_guide.md` | 采集执行指南（早期版本） |
| `reference/index_to_detail_guide.md` | index → detail 流程说明（早期版本） |

### 初始化

| 文件 | 内容 |
|------|------|
| `init/daily-init.md` | 画像初始化向导（环境检查 → 画像推断 → 平台选择 → 写入 profile） |

---

## 六、典型执行数据

以 2026-04-06 为例：

| 步骤 | 产出 | 数量 |
|------|------|------|
| 01 build_queries | 搜索查询 | 90 条（platform + google） |
| 02 collect_sources | 原始候选 | ~370 条写入文件（21 个平台/网站，max-results=5） |
| 03 filter_index | 筛选后 | 132 条 |
| 04 collect_detail | 深抓后 | 132 条（68 平台 + 64 网站，45 URL 深抓全部成功） |
| 05 prepare_payload | 去噪后 | 99 条 |
| 06 AI 生成 | 最终日报 | 15 条（3 major + 5 notable + 6 normal + 1 minor） |
| 07 validate | 校验 | ✅ 通过（含 URL 交叉校验） |
| 08 render | HTML | 1 个页面 |

各平台采集成功率：

| 平台 | 成功率 | 条目数 | 备注 |
|------|--------|--------|------|
| B站 | 6/6 ✅ | 70 | 无时间字段 |
| 知乎 | 6/6 ✅ | 63 | 无时间字段 |
| HackerNews | 7/7 ✅ | 140 | 无时间字段 |
| Reddit | 6/6 ✅ | 95 | API+代理模式 |
| arXiv | 5/5 ✅ | 50 | 论文日期偏早 |
| Reuters | 5/5 ✅ | 50 | — |
| Twitter | 6/6 ✅ | 95 | — |
| 微博 | 6/6 ✅ | 80 | — |
| 小红书 | 6/6 ✅ | 60 | — |
| YouTube | 5/6 ⚠️ | 95 | 偶发超时 |
| 36氪 | 1/7 ⚠️ | 20 | 频繁超时 |
