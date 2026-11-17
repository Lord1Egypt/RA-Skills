# AutoWhisper Skill

**Audience: Human (project overview)**

**Never make marketing content again.** Hand AutoWhisper's AI CMO one product
and the whole job leaves your desk: it learns what you sell, watches what your
rivals post, and makes content that doesn't look like an ad — in every
language, on every channel you've connected, every day. Drive it in natural
language from Claude Code, Cursor, n8n, or any MCP-capable agent.

Two things make that promise credible: the content **doesn't read as an
advertisement** (a hard ad dies in an organic feed), and the CMO **has seen
what your competitors are posting** before it writes a word.

(Honest scope: posting ≠ traffic. AutoWhisper guarantees the content exists,
fits your brand, and goes out — not that it goes viral.)

## Quick Start

### 1. Install skill

```bash
npx skills add xnjiang/autowhisper-skill
```
Or tell your AI: `Install skill from https://autowhisper.xyz/skill`

### 2. Get your token

Sign up at https://autowhisper.xyz (new accounts get free credits), open
**Settings → Connect your agent**, and copy your API token.

### 3. Configure token

```bash
mkdir -p ~/.config/autowhisper
echo '{"api_token": "your_token_here"}' > ~/.config/autowhisper/credentials.json
```

### 4. One-time: connect a platform to publish

Publishing needs a connected social account. Ask your AI to
`connect my tiktok` (OAuth platforms return a link you click once; Chinese
platforms connect with your handle). After that, your agent can publish on
its own.

### 5. Use it

```
"Add my product https://mystore.com/widget and start the CMO"
"Generate a UGC video for my product"
"Publish the approved content"
"What did the CMO do — show me analytics"
```

## How it works

Your agent talks to AutoWhisper's CMO (the same brain as the web dashboard
chat) over a small HTTP API. See `SKILL.md` (for agents) and
`references/api-reference.md` (endpoints).

## License

MIT — see `LICENSE`.
