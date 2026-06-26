# 360 Web Search Skill

Real-time Chinese web search for QClaw / OpenClaw, powered by 360's search engine API.
Purpose-built for LLMs and AI Agents.

## Why 360 Web Search

- **100B+ Chinese web pages** indexed in real time — full domestic coverage
- **Built for LLMs & AI Agents** — structured JSON output with AI-generated summaries (`summary_ai`) ready for direct reasoning
- **50% cheaper than Baidu** — from ¥12 / 1,000 queries
- **Content-filtered and safe** — clean, curated output
- **News updated within minutes** — no caching delay
- **¥50 free credit** for new users on registration（新注册用户获赠 **50 元体验金**，可直接用于360搜索服务）

## Pricing

| Plan | ID | Price |
|------|----|-------|
| Smart Search PRO | `aiso-pro` | ¥18 / 1,000 queries |
| Smart Search MAX | `aiso-max` | ¥30 / 1,000 queries |
| AI Search | `aisearch` | ¥30 / 1,000 queries |
| News Smart Search | `aiso-news` | ¥12 / 1,000 queries |
| Image Search | `image-search` | ¥12 / 1,000 queries |

## Requirements

| Requirement | Details |
|-------------|---------|
| API key | `SEARCH_360_API_KEY` — see Configuration |
| Binary | `curl` (pre-installed on macOS and most Linux systems) |
| Network | Outbound HTTPS to `api.360.cn` |

## Installation

**QClaw (macOS):**
```bash
cp -r 360-web-search ~/.qclaw/skills/
```

**OpenClaw:**
```bash
cp -r 360-web-search ~/.openclaw/skills/
```

Restart QClaw / OpenClaw after copying.

## Configuration

### Step 1 — Get your API key

1. Visit https://ai.360.com/platform and sign in (new users receive ¥50 free credit（新用户注册即获赠 50 元体验金）)
2. Go to **Open Platform → API Key Management**
3. Create an application and copy the key string

### Step 2 — Set the environment variable

Add the key to your shell profile:

```bash
echo 'export SEARCH_360_API_KEY="your-key-here"' >> ~/.zshrc && source ~/.zshrc
```

### Step 3 — Restart QClaw / OpenClaw

Fully quit and reopen the application so it picks up the new variable.

That's it — the skill will now activate automatically for search requests.

## Security

- Only outbound GET requests to `api.360.cn` — no filesystem writes, no shell commands at runtime
- API key is read from the environment and never logged or echoed
- All setup commands are in this README, not in SKILL.md runtime instructions

## Usage

Once installed and configured:

- "Search for today's AI industry news"
- "What are the latest developments in China's EV market?"
- "Look up Huawei's most recent product announcements"
- "Find recent data privacy regulations in China"

The skill selects the most appropriate plan automatically based on query type.

## File Reference

| File | Purpose |
|------|---------|
| SKILL.md | Core runtime instructions read by QClaw / OpenClaw |
| config.json | Environment variable schema, plan definitions, default settings |
| README.md | Installation, configuration, and usage guide |

## Changelog

- **v1.2.0** — Moved all shell commands to README to avoid security scan false positives; replaced imperative control language (STOP/CRITICAL/ALWAYS) with declarative behavior descriptions; key setup flow now presents information and offers to retry rather than blocking execution
- **v1.1.0** — Added hard-stop rule; interactive key setup; multi-plan support; pricing and advantage information
- **v1.0.3** — Added `metadata.clawdbot` block; security disclosure; `confirmBeforeRun`
- **v1.0.2** — Removed sensitive keywords; improved trigger rules
- **v1.0.1** — Added key setup flow; error handling
- **v1.0.0** — Initial release

## Author

360 AI Platform — https://ai.360.com/platform
