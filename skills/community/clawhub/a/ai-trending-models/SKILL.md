---
name: ai-trending-models
description: "This skill should be used when the user wants to discover, collect, or summarize the latest trending and viral open-source AI or LLM projects. Triggers include: 收集最新爆火AI开源项目, 最近有哪些热门大模型, 给我找前沿AI开源项目, what are the trending AI repos, latest open-source LLM projects, or any variation asking for hot trending new AI model releases and repositories."
---

# AI Trending Models Skill

## Purpose

Systematically collect and summarize the latest, most viral open-source AI / large-language-model
(LLM) projects from authoritative sources, and present a structured, actionable intelligence
report to the user.

## Trigger Conditions

Load this skill whenever the user asks to:
- Find / collect / scout the latest trending AI open-source projects
- Summarize recent hot LLM / multimodal / agent frameworks
- Track what's blowing up on GitHub, HuggingFace, arXiv, or AI news outlets

## Workflow

### Step 1 — Run the automated fetcher (preferred)

Execute `scripts/fetch_trending.py` to pull live data from multiple sources:

```bash
python3 scripts/fetch_trending.py
```

The script outputs a structured JSON file (`trending_report.json`) with raw data.
Read and interpret that file for the final report.

If the script cannot run (network issues, missing deps), fall back to Step 2.

### Step 2 — Manual web research fallback

Query each source listed in `references/sources.md` using web_fetch or web_search.
Collect at minimum:
- GitHub Trending (past 7 days, filter: AI / ML / LLM)
- HuggingFace Models — trending tab
- arXiv cs.AI / cs.CL — last 7 days, sorted by submission count
- Papers With Code — trending methods
- Twitter / X — #OpenSourceAI, #LLM hashtags top posts

### Step 3 — Deduplicate & rank

Rank projects by composite signal:
1. GitHub stars velocity (stars gained / days since release)
2. Cross-source mention frequency (appears in GitHub + HuggingFace + arXiv = higher rank)
3. Recency (prefer projects released or updated within 30 days)
4. Community buzz (forks, issues, PR activity, social mentions)

### Step 4 — Produce the report

Output a clean Markdown report following the template in `references/report_template.md`.

Key sections:
- **执行摘要 / Executive Summary** — 3-sentence overview of what's hot right now
- **TOP 10 爆火项目** — ranked table with: rank, project name, org/author, stars ⭐, stars delta Δ, category, one-line description, link
- **按方向分类** — group projects by: LLM底座 | 多模态 | Agent/工具链 | 推理加速 | 数据/微调 | 其他
- **值得关注的论文** — top 5 arXiv papers linked to open-source code
- **趋势洞察** — bullet-point analysis of what the data signals for the industry

## Output Standards

- Language: match the user's language (default Chinese 中文)
- Format: Markdown with emoji for visual clarity
- Stars count: use K notation (e.g. 12.4K)
- Always include direct URLs to GitHub repos / HuggingFace model pages
- Date-stamp the report header with the collection date
- If data is older than 3 days, note it clearly

## Quality Rules

- Minimum 10 projects in the main table; aim for 15–20
- No duplicates across GitHub / HuggingFace entries for the same project
- Verify each project is genuinely open-source (has an open license)
- Flag projects that are "demo-only" or have no released weights
- Prioritize projects with working code over paper-only releases
