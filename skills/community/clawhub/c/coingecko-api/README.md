# CoinGecko Agent SKILL

An installable package that teaches AI agents to use the [CoinGecko API](https://www.coingecko.com/en/api). The agent reads the live [API docs](https://docs.coingecko.com) on every request, so endpoints, parameters, and plan limits are always current.

Works with Claude Code, Gemini CLI, Codex CLI, and other SKILL-compatible agents. Setup takes under 3 minutes.

📖 [Documentation](https://docs.coingecko.com/ai-integration/agent-skill) · 🦞 [ClawHub](https://clawhub.ai/coingecko/skills/coingecko-api)

## Installation

### Coding Agents

Via [skills.sh](https://skills.sh/):

```bash
npm install -g skills
npx skills add coingecko/skills -g -y
```

`-g` installs globally for all agents. See [npmjs/skills](https://www.npmjs.com/package/skills) for details.

Via GitHub:

```bash
git clone https://github.com/coingecko/skills.git coingecko-skills
mv coingecko-skills ~/.claude/skills/coingecko
```

The path varies by agent and OS. The example above is for Claude Code on Mac/Linux.

### Claude Web

1. Download [skills-main.zip](https://github.com/coingecko/skills/archive/refs/heads/main.zip).
2. Go to [claude.ai/customize/skills](https://claude.ai/customize/skills) and select **+** → **Upload a skill**.
3. Upload `skills-main.zip`.

Then go to [claude.ai/settings/capabilities](https://claude.ai/settings/capabilities) and add these domains to your **Domain allowlist**:

- `api.coingecko.com`
- `pro-api.coingecko.com`
- `api.geckoterminal.com`
- `docs.coingecko.com`

> [!TIP]
> For the best experience, especially on the Claude free plan, set up the [CoinGecko MCP Server](https://docs.coingecko.com/ai-integration/mcp-server) alongside the SKILL.

## Try It Out

- *"If I invested $100 in Bitcoin back in December 2018, how much would it be worth today?"*
- *"What was the ATH of XPL?"*
- *"What is the current market cap of DZnQi17HFgSM8mJ4nhVicz32B97XyTsd6MUVuDJgP9Jo from Solana?"*
- *"What are the top NFT collections this week?"*

## Feedback

[Share feedback](https://tally.so/r/2EgG4p) or [open a GitHub issue](https://github.com/coingecko/skills/issues/new?labels=community).

## Maintainers

### Publishing

Every push to `main` publishes to [ClawHub](https://clawhub.ai/coingecko/skills/coingecko-api) via [`.github/workflows/publish.yml`](.github/workflows/publish.yml), using the `CLAWHUB_PUBLISH_TOKEN` Actions secret. Running the workflow manually does a dry run. Files in [`.clawhubignore`](.clawhubignore) are not shipped.

### Manual publish

From the repo root:

```bash
clawhub skill publish . --owner @coingecko --slug coingecko-api --name "CoinGecko API"
```

Add `--dry-run` to preview.

## License

[MIT](LICENSE)
