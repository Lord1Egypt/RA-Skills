---
name: ai-news-daily
description: AI 应用工程师专属的每日资讯日报技能。收集 AI 行业动态（AI 龙头公司官方博客/权威来源），按六大板块组织内容，面向 AI 应用开发工程师，重点关注能力落地和技术实用。当用户说"AI 日报"、"每天 AI 资讯"、"帮我看看今天 AI 圈发生了什么"、"生成一份日报"时触发。
---

# AI 应用工程师日报（ai-news-daily）

## 内容结构（6+1 板块）

### 🔷 AI 龙头官网资讯
**本板块价值：** 官方能力声明，判断"模型现在能做什么之前不能做的"
**数据源：** OpenAI News / Anthropic News / Google DeepMind Blog / Meta AI Blog / Microsoft AI Blog
**选文标准：** 官方能力声明、产品更新、API 变化；**不看** Benchmark 排名

---

### 1. 🧠 模型能力边界
**本板块价值：** 判断"能不能用它替代现有方案"
**选文标准：** 模型新能力 vs 旧能力对比，有应用场景结论；优先选有工程落地视角的论文

---

### 2. 🏭 生产环境反馈
**本板块价值：** 真实量化数据，比论文数字更有参考价值
**选文标准：** 崩溃率、成功率、延迟、成本——量化指标优先；优先选有数字的结论

---

### 3. 🏗️ 工程模式与落地架构
**本板块价值：** 什么场景用什么方案，Multi-Agent 什么时候值得拆
**选文标准：** RAG vs Agent 的判断标准、可复用的工程模式、架构决策经验

---

### 4. 🛠️ 开发者工具进展
**本板块价值：** 框架解决了什么痛点，比追踪新框架重要
**选文标准：** 功能更新 > 新框架发布；解决实际问题是唯一标准；关注 LlamaIndex、LangChain、Dify、Coze 等

---

### 5. 🛡️ 安全与合规
**本板块价值：** 踩了就是事故，出现就是警示级别
**选文标准：** Prompt 注入、工具链风险、数据隔离、版权问题；出现即标记为 ⚠️

---

### 6. 📚 AI应用工程师学习方向
**本板块价值：** 适合应用工程师的实战提升资源，不追热点论文
**选文标准：**
- 优先：实战教程、踩坑复盘、架构经验分享、工具对比测评
- 其次：有应用场景的有结论论文
- 少追：新 Benchmark 排名、新模型技术报告（应用工程师用不上）
- 推荐资源类型：代码示例、架构图谱、技术决策复盘

---

## 数据源（按优先级）

### 必抓龙头官网
- OpenAI News: `https://openai.com/news/`
- Anthropic News: `https://www.anthropic.com/news`
- Google DeepMind Blog: `https://deepmind.google/blog/`
- Meta AI Blog: `https://ai.meta.com/blog/`
- Hugging Face Blog: `https://huggingface.co/blog/`

### 权威科技媒体
- The Verge AI: `https://www.theverge.com/ai-artificial-intelligence`
- VentureBeat AI: `https://venturebeat.com/category/ai/`
- TechCrunch AI: `https://techcrunch.com/category/artificial-intelligence/`

### 技术社区
- Simon Willison: `https://simonwillison.net/`（LLM 安全、工具生态）
- LlamaIndex Blog: `https://blog.llamaindex.ai/`（RAG + Agent 落地）
- arXiv CS.AI: `https://arxiv.org/list/cs.AI/recent`（新论文，抓标题筛选）

### 国内源
- 机器之心: `https://www.jiqizhixin.com/`
- 量子位: `https://www.qbitai.com/`

---

## 工作流程

### Step 1：抓取龙头官网（必做，3-5个）
按优先级依次抓取 OpenAI、Anthropic、LlamaIndex Blog、Simon Willison

### Step 2：抓取权威媒体（必做，2-3个）
The Verge AI、VentureBeat AI

### Step 3：筛选 arXiv 新论文（选做，抓标题）
优先选有应用场景、有量化结论、有工程实践的论文

### Step 4：整理输出
按6+1板块结构组织，每条注明来源 URL，热度星级标注

---

## 输出格式模板

```markdown
# 🤖 AI 应用工程师日报 · YYYY-MM-DD

> **定位：** AI 应用工程师每日学习提升 | **数据源：** 龙头官网 · 科技媒体 · 技术社区 · arXiv

---

## 🔷 AI 龙头官网资讯

> **本板块价值：** 官方能力声明，判断"模型现在能做什么之前不能做的"

[内容...]

---

## 1. 🧠 模型能力边界

> **本板块价值：** 判断"能不能用它替代现有方案"

[内容...]

---

## 2. 🏭 生产环境反馈

> **本板块价值：** 真实量化数据，比论文数字更有参考价值

[内容...]

---

## 3. 🏗️ 工程模式与落地架构

> **本板块价值：** 什么场景用什么方案，Multi-Agent 什么时候值得拆

[内容...]

---

## 4. 🛠️ 开发者工具进展

> **本板块价值：** 框架解决了什么痛点，比追踪新框架重要

[内容...]

---

## 5. 🛡️ 安全与合规

> **本板块价值：** 踩了就是事故，出现就是警示级别

[内容...]

---

## 6. 📚 AI应用工程师学习方向

> **本板块价值：** 适合应用工程师的实战提升资源，不追热点论文

[内容...]

---

📊 **数据来源：** [列出实际抓取的来源] | **日期：** YYYY-MM-DD | **板块：** 6+龙头资讯
```

---

## 注意事项

- 安全与合规板块出现即标注 ⚠️，不需热度星级
- 学习板块优先选可直接用于实战的内容，减少纯论文推荐
- 每条新闻必须附 URL，保持可溯源
- 输出语言：中文
- 保持客观，不对新闻内容做主观评价
