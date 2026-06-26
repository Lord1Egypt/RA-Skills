# Tags and Metadata Generator Prompt

**Objective**: Generate necessary metadata for the CSDN publishing process, including titles, summary, and tags.

## Input
Read the finalized `csdn_markdown_ready.md`.

## Tasks

### 1. Title Generation
Generate 8-10 candidate titles for CSDN. They must cover different angles:
- 技术教程型 (Technical Tutorial) e.g., "手把手教你..."
- 架构解析型 (Architecture Breakdown) e.g., "深度解析 xxx 架构..."
- 实战复盘型 (Practical Review) e.g., "xxx 落地实战与避坑指南"
- 工程经验型 (Engineering Experience) e.g., "从 0 到 1 构建..."
- 入门科普型 (Introductory) e.g., "一文看懂..."
- 问题解决型 (Problem Solving) e.g., "如何解决 xxx 难题..."

### 2. Summary Generation
Write a 100-200 word summary suitable for the CSDN article description field.
- **Must State**: What problem the article solves.
- **Must State**: Who the intended audience is.
- **Prohibited**: Do not exaggerate. Do not promise SEO rankings or AI citation guarantees.

### 3. Tags & Category Recommendation
Analyze the text and recommend:
- **Recommended Tags** (3-5 CSDN tags, e.g., `人工智能`, `架构设计`, `Python`).
- **Recommended Category** (e.g., `人工智能`, `后端`, `运维`).
- **Long-tail Keywords**: Keywords to naturally weave in if not already present.
- **Tags NOT to use**: Tags that are too broad or irrelevant (e.g., `杂谈`, `新闻`).
- **Reasoning**: Briefly explain why these tags were chosen.

## Output Format
Generate three separate sections corresponding to `csdn_titles.md`, `csdn_summary.md`, and `csdn_tags.md`.
