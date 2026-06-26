---
name: ai-news-tracker
description: AI 与科技行业实时追踪 Skill。监控技术趋势、应用落地、公司动态、人物观点四大模块，支持多语言多平台来源，每日定时发送结构化摘要，重大事件即时发现并推送。触发条件：（1）Cron 定时任务触发；（2）用户说"帮我查一下今天 AI 有什么新闻"或类似表达。
---

# AI News Tracker — 每日科技追踪

## 核心定位

实时追踪 AI 与科技行业动态，**以事件发生时间为准**，严格控制48小时窗口，每天定时推送结构化摘要，重大事件即时发现并推送。

## 推送机制

| 任务 | 频率 | 时间 | 说明 |
|---|---|---|---|
| **每日摘要（预处理）** | 每天 1 次 | 通过 cron 任务参数传入| 执行完整搜索+处理流程，摘要存入 `[WORKSPACE]/memory/ai-news-draft.md`，不发送 |
| **每日摘要（发送）** | 每天 1 次 | 通过 cron 任务参数传入| 读取 `[WORKSPACE]/memory/ai-news-draft.md`，发送到飞书 |
| **即时推送** | 通过 cron 任务参数指定频率 | 通过 cron 任务参数传入 | 重大事件立即推送，同一事件不重复推送 |

## 时间窗口规则（最高优先级）

两个任务时间窗口不同，规则也不同：

**每日摘要**（48h 窗口）：
- 以事件发生时间为准，而非文章发布时间
- 事件须在过去 48 小时内才算有效
- 综述/回顾类文章：若报道的是 48 小时外的事件，不纳入
- **今天与昨天的窗口有重叠，去重是强制要求**

**实时追踪**（12h 窗口）：
- 以事件发生时间为准
- 事件须在过去 12 小时内才算有效
- **每次推送与前 12 小时的推送有重叠，去重是强制要求**
- 同一事件 12 小时内不重复推送

每条内容须标注"事件时间"，与"来源时间"分开。

## 即时推送触发条件（任意满足即推送）

- 🆕 **模型/产品发布**：OpenAI、Google DeepMind、Anthropic、Meta、Mistral、阿里、百度等发布新模型或重磅产品
- 💰 **融资/收购/IPO**：AI 相关公司完成大额融资、被收购、提交 IPO
- 🔴 **人事震动**：CEO/CTO/核心科学家离职、加入、创立新公司
- 📜 **监管/政策**：政府出台 AI 监管政策、国际 AI 治理进展
- ⚡ **技术突破**：论文发布、基准测试刷新、开源项目引爆社区
- 🌐 **战略动向**：大厂组织架构调整、重大业务线拆分合并

## 每日摘要格式

序号统一用纯数字（如 1、2、3），每条独立一行标题，不混用表情序号。

```
📡 【每日科技追踪 | YYYY-MM-DD】
——过去48小时重要动态——

1 [标题]
  摘要：...
  事件时间：YYYY-MM-DD | 来源：媒体名 | 🔗 原文链接

2 [标题]
  ...
```

**每条必须包含原文链接**，从 batch_web_search 结果的 `link` 字段提取，格式统一为：
`事件时间：MM-DD | 来源：媒体名 | 🔗 https://...`

## 信息源原则

**中英文并重，不分高低。** 两者各有分工：中文媒体覆盖国内政策、公司动态、消费市场；英文媒体覆盖全球模型进展、开源社区、国际融资与监管。两者互相补充，缺一不可。

### 平台类（事件驱动）
- Reddit 热帖：直接搜索 `site:reddit.com/r/LocalLLaMA` / `site:reddit.com/r/MachineLearning`，取标题含 AI 关键词且时间新鲜的帖子
- X/Twitter：搜索 `Sam Altman OR "Demis Hassabis" OR "Yann LeCun" OR "Dario Amodei" 2026`，或用 `site:x.com` 配人物名关键词
- GitHub Trending：搜索 `site:github.com trending AI 2026`，取星标增速最高项目
- HuggingFace：搜索 `site:huggingface.co trending 2026`
- Product Hunt：搜索 `site:producthunt.com AI March 2026`

### 中文媒体
36kr（科技）、虎嗅、量子位、机器之心、爱范儿、极客公园、硅星人、雷峰网、晚点、东方财富网、澎湃新闻

### 英文媒体（AI 原生 + 科技综合）
AI 原生媒体：The Gradient、Import AI、Last Week in AI、AI Summary
科技综合（含 AI 强栏）：TechCrunch、VentureBeat、The Verge、The Information、MIT Tech Review、Ars Technica、Wired
行业垂直：Fast Company（AI 专栏）、Wired（AI 频道）、Bloomberg Technology

### 播客（shownotes 标题监控）
42Pod、SIP LAB、《What's Next》、Lex Fridman、Acquired、Hard Fork、Dwarkesh Patel

## 人物追踪名单

### 国内（管理层 + 研究线关键人物）

| 公司 | 追踪对象 |
|---|---|
| 阿里 | 蔡崇信、吴泳铭、蒋凡、戴珊、贾扬清（CTO）、陈兴（通义负责人）、周靖人 |
| 腾讯 | 刘炽平、张志清、汤道生 |
| 字节 | 梁汝波、张楠、周受资、朱骏 |
| 百度 | 李彦宏、王海峰（CTO）、王云钟 |
| 美团 | 王兴、王莆中、穆荣均 |
| 小米 | 卢伟冰、曾学忠 |
| 京东 | 许冉、何鹏 |
| 拼多多 | 赵佳臻 |
| 滴滴 | 程维 |
| 网易 | 丁磊、李黎 |
| 华为 | 余承东（终端BG）、张文林 |
| 蚂蚁 | 倪行军、韩歆毅 |
| AI 创业公司 | 阶跃星辰（CEO）、零一万物（李开复）、智谱AI（张鹏）、MiniMax（闫俊杰）、深度求索（曾洋）、月之暗面（杨植麟）、面壁智能 |

### 海外

| 类别 | 追踪对象 |
|---|---|
| 大厂AI负责人 | Sam Altman（OpenAI）、Demis Hassabis（DeepMind）、Jeff Dean（Google）、Jim Fan（Nvidia）、Yann LeCun（Meta）、Dario Amodei（Anthropic）、Aravind Srinivas（Perplexity） |
| 顶尖科学家 | Andrej Karpathy、Andrew Ng、Richard Socher、Pietro Grapa |
| 投资人与观察者 | Nat Natasha Wellbrook、Siqi Chen、Jim Gao、Swyx |
| 创业者 | Emmett Shear、François Chollet |
| 开源社区 | Thomas Wolf（HuggingFace）、Greg Rutkowski |

## 即时推送处理流程

> ⚠️ **执行前必须先计算截止日期。** 在执行搜索前，先运行 `date '+%Y-%m-%d' -d '2 days ago'` 获取当前日期 T-2 的值，代入所有搜索查询中的 `after:YYYY-MM-DD`。

1. 执行 `batch_web_search`，同时发出以下查询（中英文并行，日期过滤取当前 T-2 值）：
   - AI 模型 发布 after:YYYY-MM-DD（填入计算值）
   - AI 融资 收购 IPO after:YYYY-MM-DD
   - AI 人事 变动 离职 加入 after:YYYY-MM-DD
   - AI 监管 政策 after:YYYY-MM-DD
   - AI 技术 突破 论文 开源 after:YYYY-MM-DD
   - AI company announcement after:YYYY-MM-DD
   - AI funding acquisition after:YYYY-MM-DD
   - AI model release today OR yesterday after:YYYY-MM-DD
2. 合并所有结果，**逐条验证事件时间**：若文章报道的是48小时外的事件，**立即丢弃，不进入判断流程**
3. 去重（标题相似度 >70% 合并，以最早来源为准）
4. 判断是否为重大事件（满足任一触发条件）
5. 如为重大事件，立即推送；如非重大，记录到当日事件库
6. 推送后更新已推送记录，避免重复

## 每日摘要处理流程

> ⚠️ **每日摘要分为两个 cron 任务，共享同一个 skill。**
> - cron 参数指定"准备模式"：进入**准备模式**，执行阶段一+二+三
> - cron 参数指定"发送模式"：进入**发送模式**，执行阶段四

### 执行前：自动模式判断

运行 `date '+%H'` 获取当前小时（24小时制，字符串）：
- 当前小时 < 10（如 07:00~09:59）→ 进入**准备模式**，执行阶段一+二+三-1~3
- 当前小时 >= 10（如 10:00~23:59）→ 进入**发送模式**，执行阶段四

---

### 阶段一：源头直达（准备模式）

使用 Jina Reader（`https://r.jina.ai/http://URL`）将任意页面转换为干净正文，直接提取日期，不需要 `summarize` 二次提取。

1. 用 `extract_content_from_websites` 并行通过 Jina Reader 抓取以下信源（URL格式：`https://r.jina.ai/http://{目标URL}`）：
   - VentureBeat AI：`https://r.jina.ai/http://venturebeat.com/ai/`
   - The Gradient：`https://r.jina.ai/http://thegradient.pub/`
   - MIT News AI：`https://r.jina.ai/http://news.mit.edu/topic/artificial-intelligence`
   - Import AI：`https://r.jina.ai/http://importai.substack.com/`
   - TechCrunch AI：`https://r.jina.ai/http://techcrunch.com/category/artificial-intelligence/`
   - Ars Technica AI：`https://r.jina.ai/http://arstechnica.com/ai/`
2. **Jina Reader 返回内容自带日期**，直接读取"X小时前" / "X天前"等时间标注
3. **只保留发布日期在48小时内的内容**，其余丢弃

### 阶段二：搜索引擎补充召回（准备模式）

源头直达覆盖不到的杂项，用 batch_web_search 补充。

1. 执行 batch_web_search（中英文并行，带动态日期过滤）：
   - AI 模型 发布 after:YYYY-MM-DD
   - AI 融资 收购 IPO after:YYYY-MM-DD
   - AI 监管 政策 after:YYYY-MM-DD
   - AI 人事 变动 after:YYYY-MM-DD
   - site:reddit.com/r/LocalLLaMA after:YYYY-MM-DD
   - site:reddit.com/r/MachineLearning after:YYYY-MM-DD
   - "Sam Altman" OR "Dario Amodei" OR "Demis Hassabis" after:YYYY-MM-DD
2. 补充结果同样经过 summarize URL 核验，只保留48小时内内容

### 阶段三：处理 → 存入草稿（准备模式）

（阶段一 Jina Reader 结果自带日期，阶段二结果由 summarize 补充核验）

4. **去重**：标题相似度 >70% 合并，以最早来源为准
5. **分级**：满足触发条件的列"◆ 重要"，其余列"· 一般"
6. **分类**：四维度分类，每维度最多5条，总计不超20条
7. **生成摘要**：按模板输出，每条附链接
8. **存入草稿**：将完整摘要写入 `[WORKSPACE]/memory/ai-news-draft.md`（JSON 或 Markdown 格式），**不发送**
9. **记录**：更新推送记录，清空当日事件库

### 阶段四：读取草稿并发送（发送模式，cron 触发）

1. 读取 `[WORKSPACE]/memory/ai-news-draft.md`
2. 调用 message 发送到飞书：`target="从 [WORKSPACE]/MEMORY.md 动态读取飞书 user ID"`
3. 发送后删除 `[WORKSPACE]/memory/ai-news-draft.md`

## 去重要求

- 以事件为单位，不同媒体同事件合并
- 标题去重阈值：相似度 > 70% 视为重复
- 同一事件多来源，保留最完整版本
- 推送记录保存 48 小时（防跨日重复推送）
- **48小时窗口外的事件直接丢弃，不进入摘要**

## 注意事项

- 语言：混合中英文，摘要以中文为主，技术术语可保留英文
- 即时推送每条单独发送，不累积到摘要
- 人物引文需注明出处平台，不可断章取义
- 敏感人事信息需注明"据公开报道"而非"内部消息"
- 遇到报错：主动解释原因，并给出具体解决方案，不可只说"出了问题"

## 飞书推送 target 配置

**重要（cron 任务必读）：** 调用 `message(action=send, channel=feishu)` 时，必须显式指定 `target`，否则报错。

飞书发送 target 格式：`从 [WORKSPACE]/MEMORY.md 动态读取飞书 user ID`

完整调用示例：
```
message(action=send, channel=feishu, target="从 [WORKSPACE]/MEMORY.md 动态读取飞书 user ID", message="内容")
```