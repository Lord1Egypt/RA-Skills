# clawpage-skill

English docs. Chinese version: [docs/README.zh-CN.md](docs/README.zh-CN.md).

`clawpage-skill` turns long text into interactive Clawpage web apps.
You can ask for a page in natural language, and the skill routes to page/template create or update workflows, then publishes a URL.

Official website: `https://clawpage.ai`

## What you can do

- Convert long stock-market analysis text into a chart-driven dashboard
- Build insight hubs, utility tools, and interactive mini apps
- Update existing pages by `pageId` with new content/style/behavior
- Control TTL and access code during publish

## Install

This repo is a **Claude Code plugin**. Sub-skills shell out to [`@clawpage.ai/cli`](https://www.npmjs.com/package/@clawpage.ai/cli) (the runtime), so you only need this plugin loaded — `npx` fetches the cli on demand.

### Supply-chain note

The plugin invokes `npx -y @clawpage.ai/cli@<latest>` by default. This means **npm package code from `@clawpage.ai/cli` will execute on your machine** the first time you trigger any sub-skill. Three layers of trust:

1. **Source**: cli source is at [github.com/clawpage/clawpage-cli](https://github.com/clawpage/clawpage-cli), MIT licensed, ~150 LOC of glue + standard `node:fs`/`node:https`. Audit before first run if you want.
2. **Provenance**: every npm release after `0.3.0` carries [npm provenance](https://docs.npmjs.com/generating-provenance-statements) attestations linking the published tarball to the GitHub commit it was built from. Verify with `npm view @clawpage.ai/cli@<version>`.
3. **Pin a version (recommended for production)**: edit your local copy of any sub-skill SKILL.md and replace `npx -y @clawpage.ai/cli` with `npx -y @clawpage.ai/cli@0.3.0` (or whichever you've audited). Updates then become opt-in.

If you'd rather avoid `npx` entirely: `npm install -g @clawpage.ai/cli@0.3.0` once, then change SKILL.md commands from `npx -y @clawpage.ai/cli ...` to `clawpage ...`.

### Claude Code

```text
/plugin marketplace add https://github.com/clawpage/clawpage-marketplace
/plugin install clawpage@clawpage-marketplace
```

(Or test locally before submitting to the official marketplace: `claude --plugin-dir /path/to/clawpage-skill`.)

### Codex

```bash
git clone https://github.com/clawpage/clawpage-skill ~/.codex/skills/clawpage
```

The repo ships a root-level `SKILL.md` (symlinked to `skills/clawpage-skill/SKILL.md`) so Codex's flat-skill discovery picks it up natively.

### Gemini CLI

```bash
gemini extensions install https://github.com/clawpage/clawpage-skill
```

The repo ships a root-level `gemini-extension.json` so Gemini registers it as an extension. The router skill is auto-discovered from `skills/clawpage-skill/SKILL.md`.

### OpenClaw

```bash
openclaw skills install clawpage-skill
```

OpenClaw resolves the skill name against its registry and installs into the underlying coding-CLI backend it's currently routed to.

## First-time auth

Once the skill is loaded, a one-time:

```text
Use clawpage-skill to init.
```

…will run `npx -y @clawpage.ai/cli init`, register a fresh account, and write your token to `~/.clawpage/keys.local.json`. After that, every subsequent invocation of the skill (from any directory) just works.

If you prefer to set the token manually, write it yourself:

```bash
mkdir -p ~/.clawpage
cat > ~/.clawpage/keys.local.json <<'EOF'
{
  "clawpage": {
    "token": "sk_xxx",
    "apiHost": "https://api.clawpage.ai"
  }
}
EOF
```

## Example: long stock analysis → visual page

User prompt:

```text
Use clawpage-skill to build a stock analysis dashboard from this long market note.
Requirements:
1) extract 5 key conclusions
2) include KPI cards and 7D/30D/90D trend switching
3) mobile-first layout
4) publish and return publicUrl, rootUrl, accessUrl, pageId, expiresAt
```

Typical workflow:
- choose `stock-analysis-terminal` template
- transform raw text into structured modules (summary, risks, observations)
- scaffold via `npx -y @clawpage.ai/cli scaffold stock-analysis-terminal <page-name>` → `~/.clawpage/pages/<page-name>/`
- publish via `npx -y @clawpage.ai/cli publish --page-dir <page-name> ...`
- return `publicUrl` (if available), preview/protected URLs, page protection state, and expiry info

## Template catalog

Shipped with `@clawpage.ai/cli`. List at runtime: `npx -y @clawpage.ai/cli scaffold --list`.

- `stock-analysis-terminal`
- `insight-collection-hub`
- `utility-workbench`
- `concept-animation-lab`
- `mini-game-arcade`
- `general_template`

## Direct CLI usage

Dry-run a template bundle (no publish, no auth required):

```bash
npx -y @clawpage.ai/cli scaffold general_template /tmp/preview
npx -y @clawpage.ai/cli publish --page-dir /tmp/preview --title "Preview" --dry-run
```

Publish a page project (default: `~/.clawpage/pages/<page-name>` for bare names; pass `./...` for cwd-relative project-scoped):

```bash
npx -y @clawpage.ai/cli publish \
  --page-dir my-dashboard \
  --title "My Page" \
  --subtitle "Optional"
```

Common flags:
- `--page-id <id>` update existing page
- `--ttl-ms <number|null>` override TTL (`null` = permanent)
- `--pagecode <text|null>` set/remove access code
- `--page-name <text>` set page name (use with `--pagecode null` for stable `publicUrl`)
- `--dry-run` bundle only

Subcommand reference: see [`@clawpage.ai/cli` README](https://www.npmjs.com/package/@clawpage.ai/cli).

## Localization placeholders

Use semantic placeholders for localized text, for example `[EXPIRE_AT]`, `[GENERATED_AT]`, `[SEARCH_PLACEHOLDER]`.
Skill instructions require the LLM to fill these placeholders directly using the user's preferred language before publish.
Do not use numeric key placeholders or maintain key-mapping tables.

## Security

- `~/.clawpage/keys.local.json` holds your `sk_*` owner token. Never commit it; never paste into a public Clawpage page (it would steal the whole account).
- Project-scoped `./keys.local.json` (cwd) takes precedence over the global one — handy for per-project accounts.

## License

This project is licensed under the MIT-0 License (MIT No Attribution). See `LICENSE`.
