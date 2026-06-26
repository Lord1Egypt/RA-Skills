---
name: frontier-knowledge-digest
version: 1.0.0
description: >
  Daily digest of cutting-edge science, AI, and top journal papers worldwide.
  Searches 12+ domains including Nature, Science, arXiv, AI news, biomedicine,
  physics, quantum computing, neuroscience, robotics, and more.
  Generates structured, rated reports with star ratings and source links.
  Triggers: "前沿知识简报", "科技新闻", "最新论文", "daily digest",
  "frontier knowledge", "science news", "AI news today".
tags: [science, research, ai-news, journal, arxiv, nature, digest, daily, chinese, english]
---

# Frontier Knowledge Digest (前沿知识简报)

Deliver a curated daily briefing of humanity's latest and most impactful knowledge discoveries — spanning cutting-edge science, AI breakthroughs, and top-tier journal publications.

---

## When to Use

- "帮我获取今天的前沿知识简报"
- "最近有什么重要的科技/AI新闻？"
- "有什么值得关注的新论文？"
- "每日知识简报" / "daily digest"

---

## Execution Flow

### Step 1: Search Latest Information

Use web search to query across 12+ domains in parallel:

| # | Domain | Search Query |
|---|--------|-------------|
| 1 | AI/Tech News | `AI news today latest developments machine learning OpenAI DeepMind Anthropic` |
| 2 | Tech Startups | `tech news today startup funding product launch` |
| 3 | Top Journals | `Nature Science Cell journal latest papers this week breakthrough` |
| 4 | arXiv | `arXiv trending papers AI machine learning LLM` |
| 5 | Biomedicine | `medical research breakthrough NEJM Lancet latest` |
| 6 | Physics/Astronomy | `physics astronomy quantum computing breakthrough research` |
| 7 | Energy/Climate | `clean energy climate research renewable breakthrough` |
| 8 | Neuroscience | `neuroscience brain research breakthrough consciousness` |
| 9 | Robotics/Space | `robotics humanoid robot SpaceX space exploration news` |
| 10 | Materials Science | `materials science nanotechnology superconductor breakthrough` |
| 11 | Social Sciences | `economics research psychology behavioral science study` |
| 12 | AI Ethics/Policy | `AI regulation policy ethics governance news` |
| 13 | Web3/FinTech | `blockchain crypto fintech regulation news` |

### Step 2: Filter & Rate

Filter results to keep only high-value content:

| Rating | Criteria |
|--------|----------|
| ⭐⭐⭐ | Milestone discoveries (Nobel-prize level, paradigm shifts) |
| ⭐⭐ | Important advances (top journals, high impact) |
| ⭐ | Worth noting (interesting, practical) |

### Step 3: Generate Report

Output in structured format:

```markdown
# 🌍 前沿知识简报 | {date}

## 📊 今日概览
- 共筛选 X 条值得关注的信息
- 重点领域：{field1}, {field2}...

---

## 🔬 顶级期刊 (Nature/Science/Cell)
### 1. [Paper Title] ⭐⭐⭐
- **来源**: Nature | 2026-XX-XX | [Original Link](url)
- **核心发现**: 3-5 sentence detailed description

## 🤖 AI/Machine Learning
## 🧬 Biomedicine
## 🔭 Physics/Astronomy/Math
## ⚛️ Quantum Computing
## 🧠 Neuroscience
## 🤖 Robotics/Automation
## 🚀 Space/Aerospace
## 🌱 Energy/Climate
## 🧪 Materials Science
## 📊 Economics/Society/Psychology
## ⚖️ AI Ethics/Policy
## 🔗 Web3/FinTech
## 💡 Tech Industry News

---

## 📌 This Week's Must-Reads
Recommend 1-2 most worthwhile deep-reads

---

> Generated: {timestamp}
> Saved to: ~/Documents/FrontierKnowledge/{year-month}/{date}-daily-digest.md
```

### Step 4: Save Locally

Save the generated report to:
```
~/Documents/FrontierKnowledge/{year-month}/{date}-daily-digest.md
```

---

## Category Reference

| Category | Icon | Coverage |
|----------|------|----------|
| Top Journals | 🔬 | Nature, Science, Cell |
| AI/ML | 🤖 | LLM, Deep Learning, AI Companies |
| Biomedicine | 🧬 | NEJM, Lancet, Drug R&D, Clinical Trials |
| Physics/Astronomy | 🔭 | Particle Physics, Astrophysics, Math Proofs |
| Quantum Computing | ⚛️ | Quantum Advantage, Error Correction |
| Neuroscience | 🧠 | Consciousness, Brain-Computer Interface |
| Robotics | 🤖 | Humanoid Robots, Industrial Automation |
| Space | 🚀 | SpaceX, Mars Missions, Satellite Tech |
| Energy/Climate | 🌱 | Clean Energy, Carbon Capture |
| Materials | 🧪 | Nanomaterials, Superconductors |
| Economics/Society | 📊 | Economic Research, Behavioral Science |
| AI Ethics | ⚖️ | Regulations, Ethics Discussions |
| Web3/FinTech | 🔗 | Blockchain, DeFi, Payment Innovation |
| Tech Industry | 💡 | Funding, Acquisitions, Product Launches |

---

## Configuration Options

### Interest Weights
Users can adjust focus areas via conversation:
- "我更关注 AI 和生物医学" → Prioritize these categories
- "暂时不想看物理方面的" → Skip physics section

### Time Range
- Default: Last 24-48 hours
- Adjustable: "帮我看看这周的重要新闻" → This week

---

## Guidelines

1. **Quality over quantity** — Only recommend truly valuable content
2. **No duplicates** — Check history to avoid repeat recommendations
3. **Detailed descriptions** — Each item should have 3-5 sentences explaining the discovery, method, and significance
4. **Source links** — Always provide original article links
5. **Star ratings** — Help users quickly identify priority items
6. **Flexible categories** — Skip categories with no noteworthy news; never force-fill
