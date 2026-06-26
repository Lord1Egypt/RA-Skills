# Agent详细注册表
> 每个Agent的完整能力定义、工作区路径、触发条件
> 最后更新：2026-04-11

---

## 虾调查（Researcher）

```python
{
    "代号": "虾调查",
    "英文名": "Research & CI Analyst",
    "能力描述": "爬取/清洗/去重/归档，结果写入本地知识库，维护分类/更新/版本/来源",
    "工具依赖": ["tavily","openclaw-serper","search-reddit","linkedin-cli","weixin-reader-oc","ai-video-summarizer","youtube-transcript-analyzer"],
    "工具说明": "7个专属工具自动持有，无需每次声明",
    "记忆路径": "agents/research-agent/MEMORY.md",
    "工作区": "agents/research-agent/",
    "记忆上下文": "市场结构/竞品格局/客户决策模型/搜索行为分析",
    "触发条件": "CMO调度 / 系统流程调用",
    "输出规范": "竞品对比表/市场规模估算/前景三情景/行动建议，写入本地知识库（knowledge-base/）",
    "知识库维护": "归档时标注来源/日期/版本；更新时保留历史版本；版本冲突时标注废弃版本",
    "隔离规则": "采集数据写入调用系统的data/目录；知识库共享供所有系统读取"
}
```

---

## 虾调度（Distribution Commander）

```python
{
    "代号": "虾调度",
    "英文名": "Distribution Commander",
    "能力描述": "分发策略/渠道组合/节奏控制/内容筛选，决定分发哪些渠道和节奏",
    "工具依赖": [],  # 按需临时声明
    "记忆路径": "agents/distribution-commander/MEMORY.md",
    "工作区": "agents/distribution-commander/",
    "触发条件": "内容审核通过后 / CMO调度",
    "核心职责": "3层决策引擎（价值判断/客户阶段归类/渠道组合）/有权筛选内容不分发"
}
```

---

## 虾规划（Content Strategist）

```python
{
    "代号": "虾规划",
    "英文名": "Content Strategist",
    "能力描述": "内容策略制定/关键词矩阵/SEO规划/转化路径设计",
    "工具依赖": [],  # 按需临时声明
    "记忆路径": "agents/content-strategist/MEMORY.md",
    "工作区": "agents/content-strategist/",
    "触发条件": "CMO调度"
}
```

---

## 虾写作（Decision Conversion Writer）

```python
{
    "代号": "虾写作",
    "英文名": "Decision Conversion Writer",
    "能力描述": "文案撰写/邮件模板/落地页/技术文章，专注转化型内容",
    "工具依赖": [],  # 按需临时声明
    "记忆路径": "agents/writing-agent/MEMORY.md",
    "工作区": "agents/writing-agent/",
    "触发条件": "虾规划完成后 / CMO调度"
}
```

---

## 虾审核（Growth Quality Controller）

```python
{
    "代号": "虾审核",
    "英文名": "Growth Quality Controller",
    "能力描述": "内容质量审核/7维度评分/否决机制，确保发布质量",
    "工具依赖": [],  # 按需临时声明
    "记忆路径": "agents/review-agent/MEMORY.md",
    "工作区": "agents/review-agent/",
    "触发条件": "虾写作完成后",
    "审核标准": "7维度评分（满分35，≥25分才能发布）/SERP竞争判断/转化路径检查"
}
```

---

## LinkedIn Agent

```python
{
    "代号": "LinkedIn Agent",
    "英文名": "LinkedIn B2B Generator",
    "能力描述": "B2B核心触达/帖子发布/评论互动，对话驱动型获客",
    "工具依赖": [],  # 按需临时声明
    "记忆路径": "agents/linkedin-agent/MEMORY.md",
    "工作区": "agents/linkedin-agent/",
    "触发条件": "虾调度调用",
    "触达阶段": "全阶段"
}
```

---

## Email Agent

```python
{
    "代号": "Email Agent",
    "英文名": "Email Conversion Operator",
    "能力描述": "开发信/跟进邮件/序列发送，承接LinkedIn转交的意向客户",
    "工具依赖": [],  # 按需临时声明
    "记忆路径": "agents/email-agent/MEMORY.md",
    "工作区": "agents/email-agent/",
    "触发条件": "虾调度调用",
    "触达阶段": "评估/决策"
}
```

---

## 虾展会（Exhibition Agent）

```python
{
    "代号": "虾展会",
    "英文名": "Exhibition Agent",
    "能力描述": "展会全流程：选址评估/展位设计/现场执行/展后跟进",
    "工具依赖": [],  # 按需临时声明
    "记忆路径": "agents/expo-operator/MEMORY.md",
    "工作区": "agents/expo-operator/",
    "触发条件": "CMO调度 / 展会筹备期",
    "典型展会": "沙特FMF / MiningWorld Russia / 莱州Gold"
}
```

---

## Brand & Website Agent

```python
{
    "代号": "Brand & Website Agent",
    "英文名": "Brand & Website Architect",
    "能力描述": "官网优化/产品页/案例系统/信任承载/品牌物料",
    "工具依赖": [],  # 按需临时声明
    "记忆路径": "agents/brand-website-agent/MEMORY.md",
    "工作区": "agents/brand-website-agent/",
    "触发条件": "CMO直接调度（不经过虾调度）",
    "定位": "信任基础设施，所有渠道的信任承接底座"
}
```

---

## 虾优化（Growth Analyst）

```python
{
    "代号": "虾优化",
    "英文名": "Growth Analyst",
    "能力描述": "效果分析/四象限分类/策略反馈，发现问题并上报CMO",
    "工具依赖": [],  # 按需临时声明
    "记忆路径": "agents/growth-analyst/MEMORY.md",
    "工作区": "agents/growth-analyst/",
    "触发条件": "内容发布后数据触发"
}
```

---

*最后更新：2026-04-11*
