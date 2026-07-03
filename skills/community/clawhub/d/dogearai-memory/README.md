# DogearAI Memory — Claude skill

Give your AI tools a shared, persistent memory. This skill teaches the assistant to
**recall** your saved context before it works, and **save** durable new facts — so you
never re-explain your project, preferences or decisions in a different tool again.

Powered by [**DogearAI**](https://dogearai.com), your own cross-tool AI memory layer.
Write a memory once → every AI tool that reads DogearAI remembers it. And you own it.

## Setup — just a token

1. Sign in at **[dogearai.com](https://dogearai.com)** and generate a token.
2. Set it as an environment variable:
   ```
   export DOGEAR_TOKEN=dg_xxxxxxxx     # macOS/Linux
   setx DOGEAR_TOKEN dg_xxxxxxxx       # Windows
   ```
3. Done. The skill does the rest — no MCP server, no config files, nothing to learn.

## What it does

- **Recall** — at the start of a task, loads what you've saved instead of asking you to
  repeat it.
- **Save** — when you state something durable, stores it; DogearAI's server classifies
  and files it for you.

Runs through a bundled, dependency-free Python script (`dogear.py`) that calls the
DogearAI API with your token. No vector DB, no lock-in — your memory is plain markdown,
scoped to your account, and portable. Curate it anytime in the DogearAI dashboard.
