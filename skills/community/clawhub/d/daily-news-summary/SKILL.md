---
name: daily-news-digest
description: 每日从多个权威新闻来源（BBC RSS、南华早报、36氪、TechCrunch、The Verge、Microsoft/NVIDIA官方博客等）抓取最新资讯，自动生成四板块新闻日报：国际重要新闻、中国重要新闻、AI重要新闻、AI科技巨头动态。输出带原文链接的Markdown文件。当用户需要生成每日新闻摘要、科技资讯日报、AI行业动态汇总、国际时事简报，或设置定时自动化新闻任务时使用。
description_zh: 每日从BBC、南华早报、36氪、TechCrunch等17个权威来源抓取新闻，自动生成四板块结构化日报（国际、中国、AI、科技巨头），输出带原文链接的Markdown文件。
description_en: Daily news digest generator fetching from 17 authoritative sources (BBC, SCMP, 36Kr, TechCrunch, The Verge, Microsoft/NVIDIA blogs, etc.) and producing a four-section structured report with original URLs.
version: 1.0.0
author: MZCny
tags:
  - news
  - daily
  - rss
  - ai
  - tech
  - international
  - china
  - digest
  - briefing
---

# Daily News Digest

每日新闻日报生成器。从17个权威来源并行抓取新闻，整理为四板块结构化日报。

## Workflow

### Step 1: Fetch Sources

使用 `web_fetch` 工具并行抓取以下来源。**RSS源优先**，部分失败不影响整体流程。

**国际新闻：**
- http://feeds.bbci.co.uk/news/world/rss.xml （BBC国际新闻官方RSS）
- https://www.scmp.com/rss/91/feed （南华早报RSS，英文，大中华区深度报道）

**中国综合新闻：**
- https://news.sina.com.cn/ （新浪新闻首页）
- https://www.people.com.cn （人民网首页）
- https://www.chinanews.com （中国新闻网首页）

**中国深度报道：**
- https://www.caixin.com （财新网首页）
- https://www.thepaper.cn （澎湃新闻首页）

**AI+科技行业（RSS优先）：**
- https://36kr.com/feed （36氪RSS）
- https://techcrunch.com/feed/ （TechCrunch RSS）
- https://www.theverge.com/rss/index.xml （The Verge RSS）
- https://www.ithome.com （IT之家首页）
- https://www.qbitai.com （量子位首页）
- https://www.jiqizhixin.com （机器之心首页）

**科技巨头官方动态：**
- https://openai.com/news （OpenAI官方新闻）
- https://www.anthropic.com/news （Anthropic官方新闻）
- https://news.microsoft.com/source/feed/ （Microsoft Source RSS）
- https://blogs.microsoft.com/feed/ （Microsoft官方博客RSS）
- https://blogs.nvidia.com/feed/ （NVIDIA Blog RSS）
- https://nvidianews.nvidia.com/news/rss.xml （NVIDIA官方新闻RSS）

**补充：**
- https://www.newatlas.com （New Atlas科技新闻）

### Step 2: Categorize Content

从抓取结果中提取并分类到四板块：

**板块一：国际重要新闻**
- 中东局势、地缘冲突、大国关系
- 全球经济、金融市场、能源价格
- 重大国际事件
- 优先使用BBC RSS + 南华早报RSS

**板块二：中国重要新闻**
- 宏观政策、外交动态
- 财经数据、上市公司重要公告
- 科技发射、社会热点
- 南华早报RSS有大量大中华区深度报道

**板块三：AI重要新闻**
- 大模型发布与迭代
- AI产品与应用落地
- 行业趋势与深度分析
- 优先使用36氪RSS、TechCrunch RSS、The Verge RSS、量子位、机器之心

**板块四：AI科技巨头动态**
- 按公司分类列出最新动态（OpenAI、Anthropic、Google、Microsoft、Meta、NVIDIA、DeepSeek、华为、字节、阿里等）
- 每条动态附简要解读
- 优先使用Microsoft Source RSS、NVIDIA Blog RSS、官方博客

### Step 3: Generate Markdown Report

文件格式要求：
- 标题：每日新闻日报 | YYYY年MM月DD日
- 标注生成时间和信息来源
- **每条新闻末尾必须标注来源名称，并附上原文URL链接**（格式：`（[来源名称](URL)）`）
- 包含"今日最值得关注的Top 5事件"
- 末尾包含"信息来源说明"表格
- 语言：中文

### Step 4: Save File

- 保存路径：工作区根目录
- 文件名格式：`新闻日报_YYYY-MM-DD.md`

## Optional: Automation

用户可要求创建定时自动化任务（如"每天早上8点自动生成"）。此时使用 WorkBuddy 的 `automation_update` 工具创建 recurring 任务，将上述 Workflow 作为自动化 prompt，schedule 设为 `FREQ=DAILY;BYHOUR=8;BYMINUTE=0`。

## News Sources Reference

详见 [`references/news_sources.md`](references/news_sources.md)，包含17个来源的详细分类、URL、类型和可靠性评级。

## Notes

- 如果某个网站抓取失败，继续用其他成功抓取的来源生成日报
- BBC RSS、36氪RSS、TechCrunch RSS、The Verge RSS、南华早报RSS、NVIDIA Blog RSS、Microsoft Source RSS是目前最稳定可靠的来源
- Reuters网页版和RSS经常失败，如果失败则依赖BBC+南华早报+新浪获取国际新闻
- 联合早报RSS已停用，Google/Meta官方博客RSS暂不可用
- **务必保留每条新闻的原文链接，方便用户点击阅读原文**
- 不要编造新闻，只基于实际抓取到的内容整理
- Twitter/X API 可作为可选扩展（需用户自备 Bearer Token），本 Skill 不涉及
