---
name: careermax-cover-letter-writer
description: CareerMax AI (careermax.ai) — generate tailored cover letters from resume text and job descriptions. Use when the user wants a cover letter, application letter, role-specific pitch, or customized job application message.
version: 0.1.2
metadata:
  openclaw:
    requires:
      env:
        - CAREERMAX_API_KEY
      bins:
        - npx
    primaryEnv: CAREERMAX_API_KEY
    homepage: https://careermax.ai/ai-agent
---

# CareerMax Cover Letter Writer

Generate tailored cover letters that connect a candidate's resume to a specific job description.

## Setup

1. Sign in to [CareerMax](https://careermax.ai).
2. Open Settings → API Keys.
3. Create a new API key and copy it. The key starts with `cmx_live_` and is shown only once.
4. Set the environment variable:

```bash
export CAREERMAX_API_KEY="cmx_live_..."
```

## How it works

1. The skill connects to CareerMax through the `@careermax/agent-toolkit` MCP server.
2. For MCP usage, provide `resumeText` and `jobDescription`.
3. The agent can retrieve the stored resume first with `get_resume`, then pass the resume text into `generate_cover_letter`.
4. The CLI can generate a cover letter from a saved CareerMax job ID.
5. AI-generation operations use preview/confirm — the agent shows a summary and credit cost before execution.

## Tools

- `generate_cover_letter` — Generate a tailored cover letter from resume text and a job description

## MCP usage

```bash
CAREERMAX_API_KEY="cmx_live_..." npx -y --package @careermax/agent-toolkit@latest careermax-mcp
```

## CLI usage

```bash
npx -y --package @careermax/agent-toolkit@latest careermax cover-letter generate --job-id <id>
```