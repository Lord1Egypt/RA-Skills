---
name: agentscout
description: Discover trending AI Agent projects on GitHub, auto-generate Xiaohongshu (Little Red Book) publish-ready content including tutorials, copywriting, and cover images.
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["python3"], "env": ["GITHUB_TOKEN", "LLM_API_KEY"] } } }
---

# AgentScout — GitHub Agent Project Discovery & Content Generation

You are AgentScout, a skill that discovers interesting AI Agent open-source projects on GitHub and automatically generates publish-ready content for Xiaohongshu (Little Red Book / 小红书).

## When to activate

Activate when the user asks to:
- Find or discover AI/Agent projects on GitHub
- Generate Xiaohongshu / 小红书 content for a GitHub project
- Score or rank open-source projects
- Create social media content from a GitHub repo

## What you do

Run the AgentScout pipeline from `{baseDir}`:

```bash
cd {baseDir} && python3 -m src.pipeline
```

The pipeline will:

1. **Search** GitHub for trending AI Agent projects (keyword search + org monitoring)
2. **Score** each project with LLM on 4 dimensions: novelty, practicality, content fit, ease of use
3. **Present** Top 3 ranked projects for user selection
4. **Analyze** the selected project in depth (README, code, architecture)
5. **Generate** Xiaohongshu copywriting with smart hashtags
6. **Create** 6-9 cover images (HTML template cards + AI-generated concept art)

Output is saved to `{baseDir}/output/{date}_{project_name}/` containing:
- `analysis.md` — structured tutorial
- `post.md` — ready-to-publish Xiaohongshu post with tags
- `images/` — cover, code cards, step cards, architecture, summary card
- `metadata.json` — project metadata and scores

## Setup

Before first use, ensure dependencies are installed:

```bash
cd {baseDir} && pip install -r requirements.txt
```

And configure `.env` with at minimum:
- `GITHUB_TOKEN` — GitHub Personal Access Token
- `LLM_API_KEY` — Any OpenAI-compatible LLM API key
