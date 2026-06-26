# AI Daily Brief · AI 每日简报

## 📋 功能说明

每天上午 8:00 自动推送前一天（24 小时内）全球 AI 行业重要动态，让你起床就可以了解到全球 AI 业的大新闻。

---

## 🎯 推送内容

### 1. 🏢 AI 行业大公司新闻
- OpenAI、Google AI、Microsoft AI、Meta AI、Anthropic、DeepMind 等
- 来源：官方博客、权威科技媒体

### 2. 💬 AI 行业巨头言论
- Sam Altman (OpenAI CEO)
- Satya Nadella (Microsoft CEO)
- Sundar Pichai (Google CEO)
- Mark Zuckerberg (Meta CEO)
- Dario Amodei (Anthropic CEO)
- Demis Hassabis (DeepMind CEO)
- 等头部达人

### 3. 🛠️ LLM/Agent/Skills 技术产品
- 新模型发布
- Agent 框架更新
- AI 工具/产品发布
- 来源：GitHub、Product Hunt、Hugging Face

### 4. 📄 精选论文
- Agent 相关论文
- 知识库/RAG 论文
- LLM 架构/训练论文
- 来源：arXiv、ACL Anthology、机构官方博客

---

## ⏰ 定时任务

**执行时间：** 每天上午 8:00（Asia/Shanghai 时区）

**推送渠道：** 飞书（当前会话）

**下次执行：** 明天上午 8:00

---

## 🔧 配置说明

### 必需配置

| 配置项 | 说明 | 状态 |
|--------|------|------|
| `TAVILY_API_KEY` | Tavily 搜索 API 密钥 | ✅ 已配置 |
| `BOCHA_API_KEY` | 博查搜索 API 密钥（备用） | ✅ 已配置 |

### 信源优先级

| 优先级 | 类型 | 示例 |
|--------|------|------|
| ⭐⭐⭐ | 官方博客 | OpenAI Blog、Google AI Blog |
| ⭐⭐⭐ | 权威媒体 | Reuters、The Verge |
| ⭐⭐⭐ | 头部达人 | Sam Altman Twitter |
| ⭐⭐⭐ | 论文预印本 | arXiv cs.CL/cs.LG/cs.AI |
| ⭐⭐ | 中文权威 | 机器之心、量子位 |

---

## 📝 输出格式

```markdown
# 🤖 AI 每日简报 | 2026-03-15

> 过去 24 小时全球 AI 行业重要动态

---

## 🏢 大公司新闻

### 1. 【OpenAI】GPT-5 新进展
**来源：** OpenAI Blog | **时间：** 12 小时前
**摘要：** OpenAI 宣布 GPT-5 训练完成...
**链接：** [阅读原文](url)

---

## 💬 巨头言论

### 1. Sam Altman (@sama)
**平台：** Twitter | **时间：** 8 小时前
**言论：** "AGI 的到来比大多数人想象的要近..."
**链接：** [查看原文](url)

---

## 🛠️ 技术产品

### 1. LangChain v0.2
**类型：** Agent 框架
**发布方：** LangChain
**亮点：** 新增多 Agent 协作功能...
**链接：** [了解更多](url)

---

## 📄 精选论文

### 1. "Agent RAG:..."
**机构：** Stanford
**亮点：** 提出新的 RAG 架构...
**链接：** [arXiv](url)

---

## 📊 今日概览

| 类别 | 数量 |
|------|------|
| 大公司新闻 | 3 条 |
| 巨头言论 | 2 条 |
| 技术产品 | 3 条 |
| 精选论文 | 2 条 |
```

---

## 🚀 手动触发

如需手动生成简报，可以说：

```
"生成今天的 AI 每日简报"
"昨天 AI 行业有什么大新闻"
"推送 AI 每日简报"
```

---

## ⚠️ 注意事项

1. **周末/节假日** — 正常推送，标注"周末简报"
2. **无重要新闻** — 某类别如无重要动态，标注"今日暂无"，不强制填充
3. **重大事件** — 如有重大 AI 事件，可增加"特别关注"板块
4. **信源验证** — 所有新闻必须来自可信信源，不传播谣言

---

## 📅 创建时间

- **Skill 安装：** 2026-03-15
- **定时任务：** 每天 08:00 (Asia/Shanghai)
- **下次执行：** 2026-03-16 08:00

---

*让 AI 资讯追着你跑，而不是你追着 AI 跑 🏃‍♂️💨*
