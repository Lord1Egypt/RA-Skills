# AI Weekly Insights Agent (Open-Source Project Overview)

This project automatically compiles high-value AI updates every week and outputs a readable, structured, and traceable Markdown weekly report. It can also run in OpenClaw Skill form.

---

## Project Goals

This project is designed to solve three practical problems:

- Information is scattered: official announcements, industry media, papers, and open-source updates are spread across many platforms.
- Information is noisy: duplicate content is common, signal-to-noise ratio is low, and tracking consistency is difficult.
- Output is unstable: many tools can fetch data, but few can consistently produce readable weekly reports.

So this project focuses on **stable weekly output**, not on building a heavyweight news platform.

---

## Current Features (v1)

- Default weekly time window: 7 days (`168h`)
- Automatic aggregation of: official announcements, industry news, open-source updates, research papers, and OpenClaw leaderboard
- Paper ratio control (default max: 20%)
- Source link and publish date preserved for each item
- OpenClaw leaderboard Top 3 output (rank, author, purpose, link)
- LLM-generated long-form Chinese interpretation (target: 200+ characters)
- Output path: `daily_docs/ai_weekly_YYYYMMDD.md`

---

## Output Strategy

- News first: prioritize official and industry news
- Paper throttling: papers are capped at 20% by default
- Official backfill: widen the fetch window when official news is insufficient
- Traceability: publish date appears in both body and links section
- Visible errors: fetch failures are recorded under a dedicated "Fetch Errors" section

---

## OpenClaw Skill Mode

Recommended triggers:

- `Generate AI weekly report`
- `Generate this week's report`
- `Refresh OpenClaw leaderboard`

Recommended command:

```bash
python3 run_daily_digest.py --use-llm --window-hours 168 --max-paper-ratio 0.2 --min-official-items 3
```

Output file:

- `daily_docs/ai_weekly_YYYYMMDD.md`

---

## Environment Variables and Key Security

This project supports two configuration approaches:

1. Local user `.env`
2. Environment variable injection from OpenClaw runtime

Required:

- `ARK_API_KEY`
- `ARK_ENDPOINT_ID` (recommended)

Optional:

- `ARK_MODEL`
- `DIGEST_WEBHOOK_URL`

Open-source security conventions:

- Never commit a real `.env`
- Commit only `.env.example`
- `.gitignore` should exclude `.env` and generated report files

`.env.example`:

```env
ARK_API_KEY=your_ark_api_key_here
ARK_ENDPOINT_ID=ep-your-endpoint-id
ARK_MODEL=model_name
DIGEST_WEBHOOK_URL=
```

> Real keys should exist only in runtime environments and must never appear in repositories, logs, screenshots, or issues.

---

## Suggested Repository Structure

```text
ai-weekly-agent/
  run_daily_digest.py
  sources.json
  SKILL.md
  README.md
  LICENSE
  .env.example
  .gitignore
  daily_docs/
```

---

## Quick Start

```bash
python3 run_daily_digest.py --use-llm
```

Common parameters:

- `--window-hours 168`: weekly time window (default)
- `--max-paper-ratio 0.2`: upper bound for paper ratio
- `--min-official-items 3`: minimum target count for official news
- `--focus-skill "tavily"`: track ranking for a specific OpenClaw skill

### Source Categories

1. **Official Announcements**: OpenAI, Anthropic, Google AI, Meta AI, Microsoft AI official blogs
2. **Research Papers**: arXiv (cs.AI/cs.CL/cs.CV), Papers with Code, Semantic Scholar trending
3. **Code & Open Source**: GitHub Trending, Hugging Face Trending, Awesome repositories
4. **Industry Media**: TechCrunch AI, The Verge AI, VentureBeat AI, MIT Tech Review AI
5. **Community Discussion**: Reddit (r/MachineLearning, etc.), Hacker News, X (Twitter) lists
6. **Chinese AI Media**: Jiqizhixin, QbitAI, Xinzhiyuan, 36Kr AI columns
7. **China Official Model Sources**: official pages, developer platforms, and official social channels of domestic foundation model vendors
