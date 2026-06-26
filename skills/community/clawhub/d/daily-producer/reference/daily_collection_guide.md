# 日报资讯采集指南

用于"生成日报"时的资讯采集阶段。只有在进入生成流程、且需要执行资讯采集时，才读取本文件。

目标：

- 优先获取用户关注领域内最近 3 日的资讯
- 先广泛建立候选池，再少量深挖正文
- 优先覆盖 profile.yaml 中配置的一手来源，并补充社区和多样性信号
- 在进入筛选和改写前，完整保留原始采集数据
- 优先使用 opencli 作为资讯采集入口

---

## 一、采集总原则

1. 默认只采集最近 3 日内的资讯；如果用户明确指定更短时间范围，则以用户要求为准
2. **国内源优先**：候选池应以中文/国内来源为主体，海外来源仅在该领域确实重要时纳入
3. 默认优先使用 opencli 抓取；**所有信息源的内容抓取都应先走 opencli 链路**。只有在 opencli 当前不可用、doctor 显示未连接、或目标站点确实不适配 opencli 时，才退回到普通搜索 / fetch 工具
4. 如果当前环境没有安装 opencli，应先完成安装，再进入采集
5. 不要一开始就抓取所有文章全文，先建立轻量候选池
6. 前 5 条候选优先从 `sources` 中配置的一手源产生
7. 社区、研究、开源等多样性信号用于补足，不应长期缺位
8. 采集过程必须完整留存原始数据，再进入去重、筛选、排序和改写

### opencli 强制检查

进入采集阶段后，必须先完成以下动作，才能开始真正抓取：

```bash
opencli --version && opencli doctor
```

确认 Daemon、Extension、Connectivity 三项均为 `[OK]`。只有在 opencli 整体不可用（doctor 失败）时，才允许退回 `web_search` + `web_fetch`。

这不是建议，而是执行门槛。没有完成这一步，不应直接进入普通搜索。

---

## 二、固定信息源与 opencli 采集方法

以下 5 个平台是日报的固定信息源。每次采集都必须覆盖，不可跳过。

### 2.1 微博（国内）

**登录要求：** 热搜不需要登录，搜索需要登录。

#### 热搜采集（不需要登录）

```bash
opencli weibo hot --limit 30 -f json
```

- **输出字段：** rank, word, hot_value, category, label, url
- **用途：** 快速了解当日全网热点，与用户画像关键词交叉匹配筛选相关条目
- **采集要点：**
  1. 先拿热搜列表
  2. 用画像 keywords 过滤，保留与用户领域相关的热搜条目
  3. 记录 hot_value 作为热度信号

#### 关键词搜索（需要登录）

```bash
opencli weibo search "<关键词>" --limit 10 -f json
```

- **输出字段：** rank, title, author, time, url
- **用途：** 按画像关键词精准搜索微博内容
- **采集要点：**
  1. 从 profile 的 topics[*].keywords 中取高优先级关键词
  2. 逐个关键词执行搜索（high priority 全部搜，medium 取前 3 个）
  3. 每个关键词取 10 条结果
  4. 合并去重后写入候选池
- **未登录降级：** 若返回 `🔒 Not logged in`，改用 `opencli weibo hot` 仅采集热搜

### 2.2 小红书（国内）

**登录要求：** 所有命令都需要登录。

#### 关键词搜索

```bash
opencli xiaohongshu search "<关键词>" --limit 10 -f json
```

- **输出字段：** rank, title, author, likes, published_at, url
- **用途：** 获取用户关注领域在小红书上的讨论和内容
- **采集要点：**
  1. 从 profile 的 topics[*].keywords 中取关键词
  2. 优先搜中文关键词，小红书以中文内容为主
  3. likes 数可作为热度信号参与排序
  4. published_at 用于时间窗口过滤

#### 首页推荐（补充信号）

```bash
opencli xiaohongshu feed --limit 10 -f json
```

- **输出字段：** title, author, likes, type, url
- **用途：** 发现推荐算法推送的热门内容，作为补充信号
- **采集要点：** 仅在搜索结果不足时使用，用画像关键词过滤后保留相关条目

#### 未登录降级

若返回 `🔒 Not logged in`，改用：
```bash
opencli google search "site:xiaohongshu.com <关键词>"
```

### 2.3 B站（国内）

**登录要求：** 热门不需要登录，搜索需要登录。

#### 热门视频（不需要登录）

```bash
opencli bilibili hot --limit 20 -f json
```

- **输出字段：** rank, title, author, play, danmaku
- **用途：** 获取 B 站当前热门内容，与画像交叉匹配
- **采集要点：** play 和 danmaku 数可作为热度信号

#### 关键词搜索（需要登录）

```bash
opencli bilibili search "<关键词>" --limit 10 -f json
```

- **输出字段：** rank, title, author, score, url
- **用途：** 按关键词搜索 B 站视频内容
- **采集要点：**
  1. B 站视频标题通常信息密度高，可直接作为候选摘要
  2. score 可作为排序信号
  3. 视频类内容在日报中标注为 `[视频]`

#### 未登录降级

若搜索返回 `🔒 Not logged in`，仅使用 `opencli bilibili hot` 热门采集。

### 2.4 X / Twitter（国外）

**登录要求：** 所有命令都需要登录。

#### 关键词搜索

```bash
opencli twitter search "<keyword>" --limit 15 --filter top -f json
```

- **输出字段：** id, author, text, created_at, likes, views, url
- **参数说明：**
  - `--filter top`：按热度排序（默认）
  - `--filter live`：按时间排序（最新）
- **用途：** 获取海外社区对用户关注领域的讨论
- **采集要点：**
  1. 关键词用英文（取 profile keywords 中的英文关键词）
  2. 先用 `--filter top` 抓热门，再用 `--filter live` 补最新
  3. likes 和 views 可作为热度信号
  4. created_at 用于时间窗口过滤
  5. text 是推文全文，可直接作为候选摘要

#### 热门趋势（补充信号）

```bash
opencli twitter trending --limit 20 -f json
```

- **输出字段：** rank, topic, tweets, category
- **用途：** 发现全球热点趋势，与画像交叉匹配

#### 未登录降级

若返回 `🔒 Not logged in`，改用：
```bash
opencli google search "site:x.com <keyword>"
```

### 2.5 Reddit（国外）

**登录要求：** 基础搜索和浏览不需要登录。

#### 关键词搜索

```bash
opencli reddit search "<keyword>" --sort relevance --time week --limit 15 -f json
```

- **输出字段：** title, subreddit, author, score, comments, url
- **参数说明：**
  - `--sort`：排序方式，可选 `relevance`（默认）、`hot`、`top`、`new`、`comments`
  - `--time`：时间范围，采集时固定用 `week`（一周内）
  - `--subreddit`：限定子版块搜索（可选）
- **用途：** 获取海外技术/行业社区的深度讨论
- **采集要点：**
  1. 关键词用英文
  2. score（upvote 数）和 comments 数是重要的热度信号
  3. subreddit 名称可辅助判断来源可信度
  4. 如果画像中有明确的相关 subreddit，用 `--subreddit` 缩小范围

#### 热门帖子（补充信号）

```bash
opencli reddit hot --limit 20 -f json
# 或指定子版块
opencli reddit hot --subreddit "artificial" --limit 15 -f json
```

- **输出字段：** rank, title, subreddit, score, comments
- **用途：** 获取特定子版块的热门讨论

#### 指定子版块浏览

```bash
opencli reddit subreddit "<subreddit_name>" --limit 15 -f json
```

- **用途：** 直接浏览与用户领域相关的子版块最新帖子

---

## 三、采集执行流程

### 第一阶段：轻量候选池采集

按以下顺序执行，建立候选池：

**步骤 1：运行 opencli doctor 确认连接**

```bash
opencli doctor
```

记录结果。若失败，标记 `fallback_reason` 并退回 `web_search`。

**步骤 2：生成搜索查询**

```bash
python3 scripts/build_queries.py --date {date} --window 3
```

从输出中提取关键词列表，后续分发到各平台。

**步骤 3：国内平台采集（并行）**

以下三个平台的采集相互独立，可并行执行：

```bash
# 微博：热搜 + 关键词搜索
opencli weibo hot --limit 30 -f json
opencli weibo search "<关键词1>" --limit 10 -f json
opencli weibo search "<关键词2>" --limit 10 -f json

# 小红书：关键词搜索
opencli xiaohongshu search "<关键词1>" --limit 10 -f json
opencli xiaohongshu search "<关键词2>" --limit 10 -f json

# B站：热门 + 关键词搜索
opencli bilibili hot --limit 20 -f json
opencli bilibili search "<关键词1>" --limit 10 -f json
opencli bilibili search "<关键词2>" --limit 10 -f json
```

**步骤 4：国外平台采集（并行）**

```bash
# Twitter：关键词搜索 + 趋势
opencli twitter search "<keyword1>" --limit 15 --filter top -f json
opencli twitter search "<keyword2>" --limit 15 --filter top -f json
opencli twitter trending --limit 20 -f json

# Reddit：关键词搜索 + 热门
opencli reddit search "<keyword1>" --sort relevance --time week --limit 15 -f json
opencli reddit search "<keyword2>" --sort relevance --time week --limit 15 -f json
opencli reddit hot --subreddit "<相关subreddit>" --limit 15 -f json
```

**步骤 5：合并去重**

将所有平台结果合并，按 URL 去重，写入 `output/raw/{date}_index.txt`。

每条记录必须包含：
- 来源平台（weibo / xiaohongshu / bilibili / twitter / reddit）
- 原始标题
- 作者
- 原始链接
- 发布时间（从 time / published_at / created_at 字段提取）
- 热度信号（hot_value / likes / play / views / score）
- 命中的画像关键词
- 抓取栈标记：`fetch_stack: opencli`

### 第二阶段：按需深挖正文

对第一阶段筛选出的高价值条目深抓正文：

```bash
# 通用网页正文抓取
opencli web read --url "<文章URL>"
```

- 自动转为 Markdown 格式，保存在 `./web-articles/` 目录
- 适用于所有平台的文章/帖子详情页

**各平台特有的详情命令：**

```bash
# 微博单条帖子
opencli weibo post <微博ID>

# 小红书笔记详情
opencli xiaohongshu note <note-id>

# 小红书笔记评论（判断社区反应）
opencli xiaohongshu comments <note-id> --limit 20

# B站视频字幕（提取视频内容）
opencli bilibili subtitle <bvid>

# Reddit 帖子 + 评论
opencli reddit read <post-id>
```

深抓结果写入 `output/raw/{date}_detail.txt`，每条记录标记 `fetch_stack: opencli`。

---

## 四、降级策略

### 整体不可用

若 `opencli doctor` 失败（Daemon/Extension/Connectivity 任一异常）：
- 退回 `web_search` + `web_fetch`
- 在 raw 留痕中写明 `fallback_reason: opencli doctor failed`
- 在最终结果中标记平台覆盖能力受限

### 单平台未登录

若某平台返回 `🔒 Not logged in`：

| 平台 | 降级方案 |
|------|---------|
| 微博 | 仅用 `opencli weibo hot`（热搜不需要登录） |
| 小红书 | `opencli google search "site:xiaohongshu.com <关键词>"` |
| B站 | 仅用 `opencli bilibili hot`（热门不需要登录） |
| Twitter | `opencli google search "site:x.com <keyword>"` |
| Reddit | 基础功能不需要登录，通常不会触发 |

降级时必须在 raw 留痕中写明：
```
fallback_reason: <平台> not logged in
fetch_stack: opencli-google-site (降级)
```

---

## 五、搜索查询构造规则

### 自动生成查询

进入采集前，先运行：

```bash
python3 scripts/build_queries.py --date {date} --window 3
```

脚本会根据 profile.yaml 自动生成一批带日期过滤的搜索查询，按话题优先级排列。

### 关键词分发规则

build_queries.py 生成的是通用搜索查询。分发到各平台时：

- **微博/小红书/B站：** 使用中文关键词，去掉日期后缀（平台内搜索自带时效排序）
- **Twitter/Reddit：** 使用英文关键词，去掉日期后缀
- **Google site: 搜索：** 保留完整查询（含日期过滤 `after:YYYY-MM-DD`）

### 手动补充查询

如果自动生成的查询命中不足，按以下模板构造补充查询：

**中文平台：**
- `"{话题关键词}"`
- `"{关键词} 最新"`
- `"{产品名} 发布"`

**英文平台：**
- `"{keyword}"`
- `"{keyword} release"`
- `"{keyword} announcement"`

### 搜索轮次规则

- **第一轮**：执行 `build_queries.py` 输出的全部关键词，分发到 5 个固定平台
- **第二轮**（如果候选不足）：对命中不足的话题变换关键词组合，尝试同义词、缩写、英文变体
- **第三轮**（如果仍不足）：扩大搜索范围，增加通用搜索 `opencli google search` / `opencli google news`

每轮结束后检查候选池数量和话题覆盖情况，达标后停止。

---

## 六、时间约束

默认时间窗口：最近 3 日。

强制要求：

- 超出时间窗口的内容不得作为本期资讯入选
- 候选池中每条资讯必须标注可验证的发布日期；无法确认日期的条目降低优先级或排除
- 如果需要引用更早内容，只能作为背景材料，且必须明确标注"背景"
- 在生成最终 payload 前，必须对每一条入选资讯再做一次日期校验
- 不要用"本周"、"近日"等模糊标注代替实际发布日期

---

## 七、来源策略

### 国内源优先原则

本技能面向国内用户，采集时应遵循以下优先级：

1. **国内一手源**（微博、小红书、B站 + 官方公众号、行业媒体）→ 最优先
2. **国内媒体补充**（机器之心、量子位等）→ 通过 `opencli google search "site:..."` + `opencli web read` 采集
3. **海外权威源**（Twitter、Reddit）→ 有选择地引入

### 媒体源处理方式

对于中文 AI 媒体等无专用 opencli 适配器的站点：

```bash
# 首页最新文章列表
opencli web read --url "https://www.jiqizhixin.com/"
opencli web read --url "https://www.qbitai.com/"

# 定向关键词搜索
opencli google search "site:jiqizhixin.com <关键词>"
opencli google search "site:qbitai.com <关键词>"

# 单篇文章全文
opencli web read --url "<文章URL>"
```

### 多样性补充

候选池中应尽量补齐以下信号类别：
- 一手产品 / 平台 / 行业更新
- 国内媒体报道和聚合信号
- 社区讨论和用户反馈
- 开源 / GitHub 信号（如果用户领域涉及开源项目）
- 研究 / 学术 / 行业报告

### GitHub 信号（条件性）

如果用户的领域涉及开源项目：
- `gh search repos "<关键词>" --sort stars`
- 日报中纳入 1-2 条开源条目
- 如果用户领域与 GitHub / 开源无关，可跳过

---

## 八、原始数据留存要求

这是强制要求：所有拉取到的资讯原始数据都必须留存，再进入筛选和加工。

默认输出：

- 第一阶段：`output/raw/{date}_index.txt`
- 第二阶段：`output/raw/{date}_detail.txt`

### 第一阶段建议保留

- 抓取时间
- 搜索词 / 平台命令
- 来源平台
- 原始标题
- 原始链接
- **来源发布日期**（格式 `YYYY-MM-DD`）：从各平台输出的 time / published_at / created_at 字段提取；无法确认时填 `unknown`
- 热度信号（hot_value / likes / views / score / play）
- 简介 / snippet / text
- 抓取栈标记（`fetch_stack: opencli` 或 `fetch_stack: fallback-web`）

### 第二阶段建议保留

- 抓取时间
- 深挖命令
- 来源平台
- 原始标题
- 原始链接
- 清洗后的正文
- 若抓取受阻，保留真实返回内容并标记异常状态

### 文本格式要求

- 每条记录用明显分隔线分开
- 元信息写成键值行
- 后面紧跟抓取到的原始文本
- 允许持续追加，不要求固定 JSON 结构

---

## 九、采集约束

1. 不要跳过第一阶段直接全文抓取所有文章
2. 不要只保留最后入选日报的条目，必须保留全部候选池
3. 原始文件内容应尽量贴近抓取结果本身，不要提前改写成日报文案
4. 第二阶段只深挖少量高价值条目，不要默认把所有候选全文抓下来
5. 如果页面存在明显验证码、反爬、挑战页，也应保留真实返回结果，并在后续筛选时降低其可用性
6. **所有 opencli 命令统一使用 `-f json` 输出**，便于程序化解析

---

## 十、最小执行清单

进入筛选与加工前，至少确认：

- [ ] 已运行 `opencli doctor` 确认连接正常
- [ ] 已从 5 个固定平台（微博/小红书/B站/Twitter/Reddit）执行采集
- [ ] 每个平台至少执行了热搜/热门或关键词搜索之一
- [ ] 已建立最近 3 日候选池
- [ ] 候选池中国内来源占比 > 50%
- [ ] 已将候选池原始数据保存到 `output/raw/{date}_index.txt`
- [ ] 已对少量高价值条目完成 detail 深抓
- [ ] 已将深抓原始数据保存到 `output/raw/{date}_detail.txt`
- [ ] 如有降级或退回普通工具，已记录 `fallback_reason`
- [ ] 每条记录都标记了 `fetch_stack`

---

## 十一、汇报要求

采集完成后，最终汇报必须明确写出：

1. 是否运行了 `opencli doctor`，结果如何
2. 5 个固定平台各自的采集情况：
   - 执行了哪些命令
   - 返回了多少条结果
   - 是否降级，降级原因
3. 候选池总量和各平台占比
4. 深抓了多少条，使用了哪些命令
5. 是否有平台完全失败，原因是什么
