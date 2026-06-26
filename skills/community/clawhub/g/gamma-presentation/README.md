# Gamma Presentation Generator Skill

Generate professional presentations with Gamma AI from your agent. Describe what you want and get a polished deck — no Gamma account needed.

## Two Modes

**BYOK** — Bring your own Gamma API key:
```bash
export GAMMA_API_KEY=sk-gamma-...
```

**Managed** — Use a shared key (for friends/teammates):
```json
// ~/.gamma/config.json
{"api_key": "sk-gamma-..."}
```

## Usage

```bash
# Generate from a topic
bun run generate.ts --topic "Q2 Product Roadmap" --format pdf --output ./roadmap.pdf

# Generate from detailed content
bun run generate.ts --content "Create a 10-slide pitch deck about..." --output ./pitch.pdf
```

## Install

### Claude Code
```bash
# Symlink into skills
ln -s /path/to/gamma-skill ~/.claude/skills/gamma
```

### OpenClaw / PCClaw
```bash
cp SKILL.md ~/.openclaw/skills/gamma/SKILL.md
```

### ClawhHub
```bash
npx clawhub install gamma-presentation
```

## How It Works

1. Skill receives topic or content from the user
2. Calls Gamma API to generate presentation
3. Polls until generation completes (~30-90s)
4. Downloads the result as PDF or PPTX
5. Returns the file to the user

The API key is never exposed to the user. Skill owner pays for generations.

## Cost

~$0.01/credit. Typical 8-slide deck = 50-100 credits ($0.50-$1.00).

## Requirements

- [Bun](https://bun.sh) runtime
- Gamma API key (get one at [gamma.app](https://gamma.app))

## License

MIT
