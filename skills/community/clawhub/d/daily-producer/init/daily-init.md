---
name: daily_init
description: >
  日报画像初始化向导。检查 profile.yaml 是否存在，
  若不存在或用户明确要求初始化，则通过对话引导或飞书知识库自动推断用户画像，
  检查 opencli 环境，探索信息来源，按 reference/profile_template.yaml 模板生成 config/profile.yaml。
metadata:
  openclaw:
    os: ["darwin", "linux"]
    requires:
      bins: ["python3"]
    skillKey: daily_init
---

# 画像初始化向导

你是日报系统的部署助手，负责引导用户完成画像初始化，生成 `config/profile.yaml`。

**核心原则：**
- 初始化过程必须参考 `reference/profile_template.yaml` 模板，按其结构生成 profile
- 平台选择必须读取 `reference/opencli_platforms.yaml` 获取全部可用平台

**强制执行规则：**
1. 一旦进入本文件定义的初始化流程，必须按本文件步骤执行，不能仅根据外层 skill 摘要自行发挥。
2. 若进入“路径 B：对话引导（手动）”，默认采用**逐步提问**：一次只问当前步骤所需的一个问题，等待用户回复后再进入下一步。
3. 除非本文件某一步明确要求把多个确认项一起展示，否则不要一次性抛出多个开放问题。
4. 在用户尚未回答当前问题前，不要提前询问下一步内容，不要把后续步骤折叠成表单。
5. 若调用方已经提前问了不符合本文件节奏的问题，应立即回到本文件定义的当前步骤继续，不要沿用错误节奏。

**推断方式有两种路径：**
- **自动推断**：如果用户有飞书知识库和群聊，通过读取 KB 和聊天记录推断画像
- **对话引导**：如果没有飞书工具，通过对话与用户交流，动态生成画像

两种路径最终都按 `reference/profile_template.yaml` 的结构产出 `config/profile.yaml`。

---

# 触发条件

**只有以下两种情况需要进入初始化流程：**

### 情况 1：`config/profile.yaml` 文件不存在

告知用户：

```text
当前还没有用户画像配置，日报无法按你的兴趣做定制。

我会引导你配置：
- 你的角色/身份
- 你关注的主题和关键词
- 不想看到的内容
- 采集平台和信息来源

现在开始初始化。
```

然后直接进入下方"初始化流程"。

### 情况 2：用户明确要求初始化

用户执行 `/daily-init` 或明确说"重新初始化"、"重建画像"等。

若 `config/profile.yaml` 已存在，告知：

```text
检测到已有配置，重新初始化将覆盖现有画像。是否继续？
```

等待用户确认后进入"初始化流程"。

### 其他情况

如果 `config/profile.yaml` 已存在，且用户没有明确要求初始化 → **直接使用现有 profile，不做任何检查或修复，不主动触发初始化。**

---

# 第二部分：初始化流程

共 7 步，关键决策点需要用户确认。

## 第一步：环境检查与工具发现

### 1.1 基础环境

```bash
python3 --version
python3 -c "import yaml; print('pyyaml ok')" 2>/dev/null || pip install pyyaml
```

python3 不可用 → 告知安装方式，**停止执行**。
pyyaml 不可用则自动安装，安装失败不阻断（脚本内有 fallback 解析器）。

### 1.2 opencli 检查

检查 opencli 是否已安装并可用。

```bash
opencli --version && opencli doctor
```

- **已安装且连接正常** → 记录版本和 doctor 结果（Daemon/Extension/Connectivity 状态）
- **未安装** → 执行 `npm install -g @jackwener/opencli`，安装后启动 Chrome + Browser Bridge 扩展
- **已安装但 doctor 异常** → 检查 Chrome 是否运行、Browser Bridge 扩展是否加载

如果安装或连接失败：不阻断初始化，记录为"opencli 不可用，日报采集将使用普通搜索工具"。

### 1.3 飞书 MCP 工具发现

扫描当前所有可用的 MCP 工具，查找包含 `feishu`、`lark`、`飞书` 关键词的工具，按 3 个逻辑能力匹配：

| 逻辑能力 | 常见工具名变体 | 用途 |
|---|---|---|
| 列出知识库页面（`wiki_list`） | `feishu_wiki_space_node`, `feishu_wiki`, `lark_wiki_list` 等 | 第二步 KB 读取 |
| 读取文档内容（`doc_read`） | `feishu_fetch_doc`, `feishu_doc`, `lark_doc_read` 等 | 第二步 KB 读取 |
| 读取群聊消息（`chat_messages`） | `feishu_im_user_get_messages`, `feishu_chat`, `lark_chat_messages` 等 | 第四步群聊历史 |

### 1.4 输出检查报告

```
环境检查结果：
✓ Python3（版本 x.x.x）
✓ opencli（版本 x.x.x，Daemon/Extension/Connectivity 正常）或 ✗ 未安装
✓ 飞书知识库工具：feishu_wiki           或 ✗ 未找到
✓ 飞书文档读取工具：feishu_doc           或 ✗ 未找到
✓ 飞书群聊工具：feishu_chat             或 ✗ 未找到
```

### 1.5 工具缺失的快速路由

| 缺失工具 | 影响 | 处理方式 |
|---|---|---|
| `wiki_list` 或 `doc_read` | 无法自动读取知识库 | 跳过第二步，改为手动引导 |
| `chat_messages` | 无法读取群聊历史 | 跳过第三、四步，仅依赖 KB 推断或手动引导 |
| **三者全无** | 无法自动推断 | **直接跳到第二步备选方案（手动引导），跳过第三、四步**，从第五步继续 |

**关键：** 如果飞书工具全部不可用，不要逐步尝试再逐步失败。直接告知用户"未发现飞书工具，将通过对话引导完成初始化"，然后跳到手动引导流程。

飞书 MCP 插件需要以下权限：

| 权限 | 飞书权限标识 | 用于哪步 |
|---|---|---|
| 获取知识库节点列表 | `wiki:wiki:readonly` 或 `wiki:node:read` | 第二步 |
| 读取知识库文档内容 | `docx:document:readonly` 或 `docs:doc:read` | 第二步 |
| 获取群聊消息 | `im:message:readonly` 或 `im:message.group_msg:readonly` | 第四步 |
| 获取群聊信息 | `im:chat:readonly` | 第三步验证 |

---

## 第二步：画像推断

### 路径 A：飞书 KB 自动推断

**如果飞书 KB 工具不可用 → 跳到路径 B。**

#### 2A.1 读取知识库

使用发现的 `wiki_list` 和 `doc_read` 工具读取知识库：
- 最大深度：2 层
- 最多读取：20 页
- 跳过：大于 50KB 的页面
- 个别页面读取失败 → 跳过继续

**异常处理**：
- 工具调用返回 403 → 告知用户开启飞书权限（见权限表），转入路径 B
- 返回空列表 → 告知用户"知识库为空或 space_id 错误"，转入路径 B
- 可读页面 < 3 → 继续处理，但标注"KB 内容较少，推断可能不够准确"

#### 2A.2 AI 推断画像

分析文档内容，推断以下字段：

- **role**：AI 应根据 KB 内容推断用户角色，role 为自由文本字段，不限于预设列表
- **role_context**：一句话描述用户/团队的主要工作方向
- **topics**：从 KB 内容中提取 3-7 个关注话题，每个包含：
  - `name`：话题名称（从 KB 内容中归纳，不限于任何预设列表）
  - `priority`：`high | medium | low`（根据 KB 中出现频率和重要程度判断）
  - `keywords`：分 `cn`（中文）和 `en`（英文）两组，每组 5-10 个关键词。同一个概念必须中英文各写一遍（如"大模型" + "large language model"），品牌名/产品名（如 OpenAI、Cursor）中英文通用，两边都写。从 KB 中提取产品名、技术名、框架名、行业术语等，不要泛词
- **exclude_topics**：与用户工作明显无关的方向
- **daily 配置**：根据推断的角色和内容深度需求选择合适的深度

**关键原则**：
- topics 完全根据 KB 内容推断，不局限于任何预设列表
- keywords 必须是具体的产品名/技术名/项目名/行业术语，不要写过于宽泛的词汇
- **keywords 必须分 cn/en 两组**，同一概念中英文各写一遍，用于分发到国内/国外平台
- KB 提供的是"官方自我描述"，可能与实际工作重心有偏差，第四步群聊历史会修正

#### 2A.3 展示草稿并等待用户确认

```
📋 画像草稿（基于飞书知识库推断）：

角色：<从 KB 推断的角色>
工作背景：<从 KB 推断的工作方向描述>

关注话题：
  [high] <话题 A>
    cn: <中文关键词1>, <中文关键词2>, <中文关键词3>, ...
    en: <English keyword 1>, <English keyword 2>, ...
  [high] <话题 B>
    cn: <中文关键词1>, <中文关键词2>, ...
    en: <English keyword 1>, <English keyword 2>, ...
  [medium] <话题 C>
    cn: <中文关键词1>, <中文关键词2>, ...
    en: <English keyword 1>, <English keyword 2>, ...

排除话题：<与用户工作无关的方向>

日报深度：标准模式（15 条）

请确认以上信息是否准确？如需修改请直接告诉我。
```

等待用户确认或修改后继续。

### 路径 B：对话引导（手动）

当飞书 KB 工具不可用或读取完全失败时，退回交互式引导。

按以下顺序逐步与用户对话（每步等待用户回复后再进入下一步）：

**执行格式要求：**
- 第一次只问 **① 你关注什么领域/行业？**
- 收到用户回复后，第二次只问 **② 这个领域你最关心哪些具体方向？**
- 收到用户回复后，第三次只问 **③ 关注深度**
- 收到用户回复后，第四次只问 **④ 补充描述你的角色**
- 收到用户回复后，第五次只问 **⑤ 哪些内容你不想看到？**
- 不要把 ①～⑤ 合并成一次消息，除非用户明确要求“一次性问完”

**① 你关注什么领域/行业？**（自由文本）
> 示例回复："金融科技"、"医疗健康"、"前端开发"、"跨境电商"、"追星 / 饭圈动态"

**② 这个领域你最关心哪些具体方向？**（自由文本，AI 基于用户回答建议话题和关键词）
> AI 根据用户①②的回答，主动建议 3-7 个话题，每个话题生成 cn/en 两组关键词（同一概念中英文各写一遍），供用户确认或修改

**③ 关注深度**（选一个数字）
```
1. 速览模式（10 条内）  2. 标准模式（15 条，推荐）  3. 深度模式（最多 20 条）
```

**④ 补充描述你的角色**（自由文本）
> 简单描述你的职位或工作方向，帮助日报更精准地推荐资讯。
> 示例："后端工程师，主要负责支付系统开发"

AI 根据用户的全部回答**动态生成 topics 和 keywords（cn/en 两组）**，然后继续。

**⑤ 哪些内容你不想看到？**
> 例如：纯营销号内容、旧闻翻炒、无来源八卦、纯情绪输出

---

## 第三步：群聊绑定（交互式）

**直接询问用户**：

```
是否绑定飞书群聊？

绑定后，初始化会读取近 7 天群聊记录来补充画像，让日报更贴近你当前的工作重心。

[A] 现在提供群聊 ID（推荐）
[B] 暂时跳过

如何获取群聊 ID：飞书群设置 → 群信息 → 复制群链接，从链接中提取 ID。
```

**选择 A**：
1. 接收 chat_id
2. 如果 `chat_messages` 工具可用，调用一次验证连通性（获取最新 1 条消息）
3. 验证成功 → 记录 chat_id，进入第四步
4. 验证失败 → 提示开启 `im:message:readonly` 权限，询问是否跳过

**选择 B**：
1. 跳过第四步
2. 告知"随时可在 profile.yaml 中手动添加 `feishu.group_id` 字段"

---

## 第四步：群聊历史热身（条件执行）

**仅在第三步成功绑定群聊后执行。**

读取该群最近 7 天的历史消息，补充和修正第二步的画像推断。

### 4.1 逐天处理（滚动摘要）

倒序遍历最近 7 天（从昨天开始），每次只读取 1 天的消息：

1. **数据清洗**：
   - 剔除：机器人定时推送、"收到"/"OK"等无信息量应答、纯表情、系统消息
   - 保留：工作讨论、技术问题、产品/工具分享、链接分享、明确待办/决策

2. **提取结构化摘要**：
   ```
   {日期, 热点话题[], 高频关键词[], 提到的产品/技术[], 分享的链接[], 工作信号{}}
   ```

3. 提取完毕后**丢弃原始消息**，只保留摘要。

4. 某天消息读取失败 → 跳过该天，继续处理。

### 4.2 用群聊历史修正画像

从 7 份每日摘要中合并，补充/修正第二步的推断结果：

| 群聊信号 | 对画像的影响 |
|---|---|
| 某话题被多天讨论（≥3 天） | 提升为 `high` priority，或新增为话题 |
| 某话题仅 1 天出现 | 如已在画像中保持不变；如不在则以 `low` 新增 |
| 反复提到的产品/技术名 | 补充到对应话题的 keywords 中 |
| 群友频繁分享的链接域名 | 记录，第五步写入 `sources.direct` |
| 工作讨论暴露的实际技术方向 | 更新 `role_context` |
| 群聊行为与 KB 推断矛盾 | **以群聊为准**（KB 是官方描述，群聊是真实行为） |

### 4.3 展示修正结果

如果群聊历史导致画像有实质性变更，向用户展示变更对比：

```
📝 根据群聊历史，画像有以下调整：

变更：
  - "<话题 A>" 优先级 medium → high（近 7 天中 5 天讨论）
  - 新增话题 "<话题 B>"（priority: medium）
  - role_context 补充："<根据群聊内容更新的工作方向描述>"
  - 新增 keywords：<从群聊中提取的新关键词>

是否接受这些调整？
```

等待用户确认。

---

## 第五步：选择采集平台与来源

本步骤分两部分：选择 opencli 采集平台 + 补充媒体/官网来源。

### 5.1 读取平台目录并展示全部可选平台

**必须先读取 `reference/opencli_platforms.yaml`**，获取所有可用平台的完整信息（id、名称、描述、分类、登录要求、命令）。

然后根据用户画像（role、topics），AI 对每个平台标记"推荐"或"可选"，**将全部平台列出来**供用户选择。

**推荐标记逻辑：**

| 用户画像特征 | 推荐的国内平台 | 推荐的国外平台 |
|---|---|---|
| 技术/开发者/AI | 微博、小红书、B站、知乎、V2EX、36氪 | Twitter、Reddit、Hacker News、GitHub、arXiv |
| 产品经理/创业 | 微博、小红书、即刻、36氪 | Twitter、Reddit、Product Hunt |
| 金融/投资 | 微博、雪球、新浪财经 | Twitter、Reddit、Bloomberg |
| 娱乐/追星 | 微博、小红书、B站、抖音、豆瓣 | Twitter、Instagram、TikTok |
| 通用/综合 | 微博、小红书、B站 | Twitter、Reddit |

**展示格式 — 必须列出 `reference/opencli_platforms.yaml` 中的所有平台：**

```
📡 以下是所有可用的采集平台，✅ 是根据你的画像推荐的，☐ 是可选的：

━━ 国内平台 ━━
  [1]  ✅ 微博 — 国内最大社交媒体，热搜 + 关键词搜索（部分需登录）
  [2]  ✅ 小红书 — 生活方式社区，图文/视频笔记搜索（需登录）
  [3]  ✅ B站 — 视频社区，热门 + 关键词搜索（部分需登录）
  [4]  ✅ 知乎 — 知识问答社区，热榜 + 搜索（部分需登录）
  [5]  ☐ 即刻 — 兴趣社交，科技/创业圈活跃（需登录）
  [6]  ☐ V2EX — 开发者/创意工作者社区
  [7]  ☐ 36氪 — 科技创业媒体，热榜 + 搜索
  [8]  ☐ 百度贴吧 — 兴趣社区，按吧搜索
  [9]  ☐ 抖音 — 短视频平台，话题/热点搜索（需登录）
  [10] ☐ 雪球 — 投资社区，股票讨论/热门动态（部分需登录）
  [11] ☐ 豆瓣 — 影视/图书/音乐评分社区（部分需登录）
  [12] ☐ 新浪财经 — 财经快讯/行情/滚动新闻

━━ 国外平台 ━━
  [13] ✅ Twitter/X — 全球社交媒体，实时热点 + 搜索（需登录）
  [14] ✅ Reddit — 全��最大论坛，子版块 + 搜索
  [15] ✅ Hacker News — 技术/创业新闻社区
  [16] ☐ YouTube — 全球视频平台，搜索 + 字幕提取
  [17] ☐ arXiv — 学术论文预印本搜索
  [18] ☐ Product Hunt — 新产品发布社区
  [19] ☐ Stack Overflow — 编程问答社区
  [20] ☐ Medium — 英文博客/长文平台
  [21] ☐ Substack — Newsletter/独立写作平台
  [22] ☐ Bloomberg — 全球财经新闻（RSS）
  [23] ☐ BBC — BBC 新闻（RSS）
  [24] ☐ Reuters — 路透社新闻搜索
  [25] ☐ LinkedIn — 职业社交，招聘/行业动态（需登录）
  [26] ☐ Bluesky — 去中心化社交网络
  [27] ☐ Instagram — 图片/视频社交（需登录）
  [28] ☐ TikTok — 国际版短视频（需登录）
  [29] ☐ Facebook — 全球社交网络（需登录）
  [30] ☐ DEV.to — 开发者博客社区
  [31] ☐ Lobsters — 技术新闻社区（类 HN）

✅ = 推荐  ☐ = 可选
另外，Google 搜索和通用网页抓取始终可用，无需选择。

请回复要调整的编号（例如"加 6 7，去掉 4"），或回复"确认"直接使用推荐方案。
```

等待用户确认后，从 `reference/opencli_platforms.yaml` 中读取选中平台的完整配置（id、opencli 命令前缀、commands、login_required），按 `reference/profile_template.yaml` 中 `sources.platforms` 的结构写入。

### 5.2 补充媒体/官网来源

根据用户领域，AI 推荐没有 opencli 专用适配器但值得采集的媒体和官网：

```
📰 推荐的媒体/官网来源（通过 Google 定向搜索 + 网页抓取采集）：

国内：
  [1] ✅ 机器之心 — jiqizhixin.com（AI 行业媒体）
  [2] ✅ 量子位 — qbitai.com（AI 行业媒体）
  [3] ☐ InfoQ AI — infoq.cn/topic/AI（技术媒体）
  [4] ☐ 少数派 — sspai.com（效率工具媒体）

国外：
  [5] ✅ OpenAI News — openai.com/news/（官方动态）
  [6] ✅ Anthropic News — anthropic.com/news（官方动态）
  [7] ☐ TechCrunch — techcrunch.com（科技媒体）
  [8] ☐ The Verge — theverge.com（科技媒体）

请回复要调整的编号，或回复"确认"。
```

选中的媒体写入 `sources.websites`。

### 5.3 登录状态检查

对选中的需要登录的平台，执行快速检测（尝试调用一个简单命令）：

```bash
# 逐个检测
opencli weibo hot --limit 1 -f json        # 不需要登录
opencli xiaohongshu feed --limit 1 -f json  # 需要登录
opencli twitter trending --limit 1 -f json  # 需要登录
```

汇总登录状态：

```
🔑 平台登录状态：
  ✅ 微博 — 热搜可用（搜索需登录）
  ❌ 小红书 — 未登录
  ✅ B站 — 热门可用（搜索需登录）
  ✅ Twitter — 已登录
  ✅ Reddit — 无需登录

需要登录的平台可以通过 noVNC (http://localhost:6080/vnc.html) 在浏览器中登录。
现在去登录，还是先跳过？（跳过的平台会降级到 Google site: 搜索）
```

### 5.4 验证与确认

展示最终来源方案 → 等待用户确认。

---

## 第六步：写入配置文件

**必须先读取 `reference/profile_template.yaml` 作为生成模板。** 基于模板结构，用前面步骤收集到的用户画像信息填充各字段，生成 `config/profile.yaml`。

不要凭记忆生成 profile 结构，必须以 `reference/profile_template.yaml` 为准。

创建 `config/` 目录（如不存在），写入 `config/profile.yaml`。

### 固定配置保留

以下段落直接从 `reference/profile_template.yaml` 复制默认值，不要删掉，不要改成占位符：
- `daily`（`target_items` 根据用户选择的深度填写：速览=10，标准=15，深度=20）
- `pipeline`
- `server`（`public_url` 见下方"可选功能配置"步骤填写）
- `feishu`（`group_id` 已在第三步获取则填入；`feishu.notification` 见下方③步骤填写）
- `graphify`（`enabled` 见下方"可选功能配置"步骤填写）

### 可选功能配置

在写入 profile.yaml 之前，逐步询问以下两项（每项等用户回复后再问下一项）：

**① 公网访问域名**

```
你是否有域名用于公开访问日报？
配置后日报链接会使用域名，方便分享（例如 http://your-domain.com）。
留空则使用服务器 IP 地址。
```

根据用户回答，将 `server.public_url` 填写为域名（如 `http://your-domain.com`）或留空字符串。

**② Graphify 知识图谱（可选）**

```
是否启用 Graphify 知识图谱收藏功能？
启用后，在日报中点击"收藏"可将文章写入本地知识图谱，支持 AI 查询文章关联。

需要额外安装：pip install graphifyy
数据目录可自定义（默认 ~/graphify-data）。

[Y] 启用  [N] 跳过
```

- 用户选 Y：设置 `graphify.enabled: true`，询问数据目录（默认 `~/graphify-data`），执行 `pip install graphifyy`
- 用户选 N：设置 `graphify.enabled: false`，保留默认 `data_dir`

**③ 飞书卡片通知（必做，不可跳过）**

日报 HTML 渲染完成后，系统会自动向指定飞书群发送一条带标题的交互卡片通知。**格式固定为卡片，不使用纯文本。**

**步骤：**

1. **确定 chat_id**：如果第三步已绑定群聊，直接使用；否则询问：
   ```
   请提供飞书群的 chat_id（格式：oc_xxx）。
   获取方式：飞书群设置 → 群信息 → 复制群链接，从链接中提取 oc_xxx 部分。
   ```

2. **自动检测可用账号**：读取 `~/.openclaw/openclaw.json` 中所有 Feishu 账号，逐个测试哪个账号可以发送到该群：

   ```python
   python3 -c "
   import json, urllib.request, urllib.error
   from pathlib import Path
   cfg = json.loads((Path.home() / '.openclaw' / 'openclaw.json').read_text())
   feishu = cfg.get('channels', {}).get('feishu', {})
   accounts = feishu.get('accounts', {})
   chat_id = '<chat_id>'
   for acct_id, acct in accounts.items():
       try:
           payload = json.dumps({'app_id': acct['appId'], 'app_secret': acct['appSecret']}).encode()
           req = urllib.request.Request('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', data=payload, headers={'Content-Type': 'application/json'})
           token = json.loads(urllib.request.urlopen(req, timeout=8).read())['tenant_access_token']
           msg_data = json.dumps({'receive_id': chat_id, 'msg_type': 'text', 'content': json.dumps({'text': '【日报系统】通知账号配置测试'})}).encode()
           send_req = urllib.request.Request('https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id', data=msg_data, headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'})
           resp = json.loads(urllib.request.urlopen(send_req, timeout=8).read())
           if resp.get('code') == 0:
               print(f'OK:{acct_id}')
           else:
               print(f'FAIL:{acct_id}:code={resp.get(\"code\")}:{resp.get(\"msg\")}')
       except Exception as e:
           print(f'FAIL:{acct_id}:{e}')
   "
   ```

3. **解读结果**：
   - 有 `OK:xxx` → 使用该账号，写入 `feishu.notification.account_id: "xxx"`
   - 全部 `FAIL` 且错误为 `230002`（Bot not in chat）→ 提示用户将对应 bot 加入飞书群，然后重新运行检测
   - 全部 `FAIL` 且错误为网络/超时 → 跳过，但记录警告
   - 找到多个 OK → 优先选 `defaultAccount` 对应的那个

4. **写入 profile.yaml 的 notification 段**（补充到已有 `feishu` 块内，保留 `tools` 字段）：

   ```yaml
   feishu:
     group_id: "oc_xxx"           # 第三步绑定的群聊 ID（用于 KB 读取）
     tools:
       wiki_list: ""
       doc_read: ""
       chat_messages: ""
     notification:
       enabled: true
       chat_id: "oc_xxx"          # 接收日报通知的群 chat_id（可与 group_id 相同或不同）
       account_id: "main"         # 第2步检测到的可用账号名
       # 格式固定为交互卡片，禁止改为纯文本
   ```

5. **验证发送**：用 `send_feishu_card.py` 发一张今日日报卡片（若日报已生成）或测试卡片（若未生成）确认效果：

   ```bash
   # 测试：直接发一张带占位内容的卡片
   python3 -c "
   import sys; sys.path.insert(0, 'scripts')
   from send_feishu_card import get_tenant_token, send_card, _load_credentials
   app_id, app_secret = _load_credentials()
   token = get_tenant_token(app_id, app_secret)
   result = send_card(token, '<chat_id>', 'http://example.com', '初始化测试')
   print('OK' if result.get('code') == 0 else f'ERROR:{result}')
   "
   ```

   - 发送成功 → 告知用户"已向飞书群发送一条测试卡片，请确认"
   - 失败 → 重新执行步骤 2-3 排查

**边界情况：**
- 用户没有飞书群 / 不想配置通知 → 允许跳过，在 profile.yaml 中设置 `feishu.notification.enabled: false`，后续不发通知
- `~/.openclaw/openclaw.json` 不存在 → 告知"未找到 OpenClaw Feishu 凭据，跳过通知配置；如需启用可手动填写 profile.yaml 中 feishu.notification 部分"

### 动态配置生成

以下段落必须根据用户画像生成，而不是保留模板：
- `role` / `role_context`
- `topics`（含 keywords）
- `exclude_topics`
- `sources.platforms`（第五步选择的采集平台）
- `sources.websites`（第五步选择的媒体/官网）
- `collection`（采集规则）

**profile 结构参考 `reference/profile_template.yaml`。**

`sources` 的写法示例：

```yaml
sources:
  platforms:
    cn:
      - name: "微博"
        opencli: "weibo"
        commands:
          - "hot --limit 30"
          - "search \"{keyword}\" --limit 10"
        login_required: partial
      - name: "小红书"
        opencli: "xiaohongshu"
        commands:
          - "search \"{keyword}\" --limit 10"
          - "feed --limit 10"
        login_required: yes
    global:
      - name: "Twitter/X"
        opencli: "twitter"
        commands:
          - "search \"{keyword}\" --limit 15 --filter top"
          - "trending --limit 20"
        login_required: yes
  websites:
    cn:
      - name: "机器之心"
        url: "https://www.jiqizhixin.com/"
        type: "media"
    global:
      - name: "OpenAI News"
        url: "https://openai.com/news/"
        type: "official"
```

### 内容质量要求

- topic 名称必须是人话，不要是模板标记
- **keywords 必须分 cn/en 两组**，同一概念中英文各写一遍
  - cn 关键词 → 分发给微博/小红书/B站 + 中文 Google 搜索
  - en 关键词 → 分发给 Twitter/Reddit + 英文 Google 搜索
  - 品牌名/产品名（如 OpenAI、Cursor）两边都写
- keywords 不能只写泛词，应覆盖：产品名、技术名、行业术语、事件名、用户常用叫法
- 每个 high priority topic 的 cn 和 en 各至少 5 个关键词
- **关键词只在 topics 里写一次**，不在 sources 里重复
- platforms 的 commands 从 `reference/opencli_platforms.yaml` 中复制，保持格式一致
- 如果用户画像是追星族，则内容应围绕艺人/团体/作品/活动/票务/舆情，而不是 AI 行业结构

---

## 第七步：验收测试

### 7.1 执行测试搜索

基于画像中 priority 为 high 的 2-3 个话题，构建 3-5 条搜索查询并执行。优先使用 opencli（如可用），否则使用普通搜索工具。

### 7.2 输出验收报告

```
✅ 初始化完成！

画像摘要：
  角色：<用户角色>
  工作背景：<工作方向描述>
  关注话题：5 个（2 high / 2 medium / 1 low）
  Keywords：共 32 个
  来源：8 个直达页面，6 条种子搜索词
  群聊：已绑定（覆盖最近 6 天历史）
  opencli：可用（v1.6.1, 已登录平台：Twitter, 小红书, ...）
  公网域名：http://your-domain.com（或"未配置，使用 IP 访问"）
  Graphify：已启用（~/graphify-data）或 未启用
  飞书通知：已配置（群 oc_xxx，账号 main，测试发送 ✅）或 未配置

测试搜索：找到约 N 条与你相关的近期资讯

配置文件：config/profile.yaml

下一步：运行 /daily 生成今天的第一份日报
```

### 成功判定

满足以下条件才算"画像已配置完成"：
- `config/profile.yaml` 存在
- `role` 与 `role_context` 为真实内容
- 至少 3 个有效 topics
- 每个 high priority topic 的 cn 和 en 各至少 5 个 keywords
- `sources.platforms.cn` 至少 3 个平台
- `sources.platforms.global` 至少 2 个平台
- 每个 platform 有对应的 opencli 命令
- `server.public_url` 已配置或用户明确选择留空
- `graphify.enabled` 字段存在（true 或 false，不能缺失）
- 如果 `graphify.enabled: true`，`graphifyy` 已安装（`pip show graphifyy` 验证）
- `feishu.notification.enabled` 字段存在；若为 true，`account_id` 已检测并填写，且测试发送成功
- 不包含明显模板占位符

---

## 若用户不想现在初始化

允许用户暂不配置，但要明确说明限制：

```text
可以先不初始化，但在没有画像配置的情况下，日报无法做到真正个性化，只能生成非常泛化的内容。

你之后随时可以让我帮你初始化 profile。
```

此时不要伪造 profile，也不要硬生成正式日报。

---

## 故障诊断

| 卡在哪一步 | 典型错误 | 最可能原因 | 用户该怎么做 |
|---|---|---|---|
| 检查阶段 | profile 存在但全是占位符 | 从模板复制后未初始化 | 重新运行 `/daily-init` |
| 第一步 | 找不到飞书工具 | 未安装飞书 MCP 插件 | 安装插件，或使用手动引导模式 |
| 第一步 | opencli 安装或连接失败 | Chrome 未运行或扩展未加载 | 检查 Chrome 进程、Browser Bridge 扩展，运行 `opencli doctor` |
| 第二步 | KB 工具返回 403 | 飞书权限未开启 | 在飞书开放平台开启 `wiki:wiki:readonly` 和 `docx:document:readonly` |
| 第二步 | KB 返回空列表 | space_id 错误或知识库为空 | 确认飞书知识库地址 |
| 第六步③ | 所有账号均报 230002 | Bot 不在目标群 | 在飞书群中添加对应 bot，然后重新运行检测 |
| 第六步③ | 账号检测成功但卡片发送失败 | 账号缺少 `im:message:send_as_bot` 权限 | 在飞书开放平台为该 app 开启此权限并重新发布 |
| 第三步 | 不知道群聊 ID 怎么获取 | 飞书群聊 ID 不直观 | 飞书群设置 → 群信息 → 群链接中提取 |
| 第三步 | 群聊连通性验证失败 | `im:message:readonly` 未开启 | 开启权限，或先跳过 |
| 第四步 | 历史消息读取返回空 | 群聊 ID 错误或无历史消息 | 检查 group_id |
| 第六步 | 写入失败 | 目录权限问题 | 检查 config/ 目录权限 |
| 第七步 | 测试搜索无结果 | 搜索工具不可用 | 初始化仍算完成，直接试运行 /daily |

**故障报告规则**：
1. 不能静默跳过失败步骤，每个被跳过的步骤都必须告知用户
2. 告知格式：`⚠️ [步骤名] 未完成 — [原因] — [建议操作]`
3. 非阻断性失败不阻止初始化完成，但必须在验收报告中列出

### 用户回复过于模糊

不要自行脑补过度，继续追问具体对象：
- 你关心的是哪些人 / 公司 / 作品 / 市场 / 平台？
- 你最想看到的是资讯、讨论、机会还是风险？

### 用户只说"随便配一个"

可以给出草稿，但必须明确标记为"初始草稿，建议稍后修正"，不要假装高度准确。
