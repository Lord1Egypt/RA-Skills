# ALT-F1 OpenClaw Skill Conventions

Best practices extracted from 7 production skills:
[Jira](https://github.com/ALT-F1-OpenClaw/openclaw-skill-atlassian-jira-by-altf1be) ·
[OpenProject](https://github.com/ALT-F1-OpenClaw/openclaw-skill-openproject) ·
[HubSpot](https://github.com/ALT-F1-OpenClaw/openclaw-skill-hubspot-by-altf1be) ·
[SharePoint](https://github.com/ALT-F1-OpenClaw/openclaw-skill-sharepoint) ·
[X/Twitter](https://github.com/ALT-F1-OpenClaw/openclaw-skill-x-twitter) ·
[M365 Task Manager](https://github.com/ALT-F1-OpenClaw/openclaw-skill-m365-task-manager)

## Architecture

### Single-file CLI pattern
- One `.mjs` file in `scripts/` per skill
- ESM (`"type": "module"` in package.json)
- `#!/usr/bin/env node` shebang, `chmod +x`
- 2 core dependencies: `commander` + `dotenv`
- Node.js built-in `fetch` (no axios/got)

### Lazy config with Proxy
```js
let _cfg;
function getCfg() {
  if (!_cfg) {
    _cfg = { host: env('HOST'), token: env('TOKEN') };
  }
  return _cfg;
}
const CFG = new Proxy({}, { get: (_, prop) => getCfg()[prop] });
```
**Why:** Config is only validated when a command actually runs. `--help` and `--version` work without env vars set.

### Error wrapper
```js
function wrap(fn) {
  return async (...args) => {
    try {
      await fn(...args);
    } catch (err) {
      if (err.statusCode) {
        console.error(`ERROR (${err.statusCode}): ${err.message}`);
      } else {
        console.error(`ERROR: ${err.message}`);
      }
      process.exit(1);
    }
  };
}
```
Every command handler is wrapped: `program.command('list').action(wrap(cmdList))`

## Security

### Mandatory patterns
1. **`--confirm` for destructive operations** — every `delete` command requires `--confirm` flag
2. **`safePath()` for file operations** — prevent `../` path traversal
3. **`checkFileSize()` for uploads** — enforce size limits before sending
4. **No secrets to stdout** — never print tokens, keys, or passwords
5. **Rate-limit retry** — handle HTTP 429 with exponential backoff (3 attempts)

### Rate-limit retry pattern
```js
if (resp.status === 429) {
  const retryAfter = parseInt(resp.headers.get('retry-after') || '5', 10);
  const backoff = retryAfter * 1000 * attempt;
  if (attempt < retries) {
    console.error(`⏳ Rate limited — retrying in ${(backoff/1000).toFixed(0)}s`);
    await new Promise(r => setTimeout(r, backoff));
    continue;
  }
}
```

## Output Style

### Console formatting
- Emoji prefixes: `📋` items, `✅` success, `💬` comments, `📎` attachments, `⏱️` time, `🏷️` types
- Padded columns with `.padEnd()` for alignment
- Item counts at bottom: `\n${items.length} of ${total} items`
- Monospace IDs: `#${String(id).padEnd(6)}`
- Truncate long text: `text.substring(0, 200) + '...'`

### No markdown tables in output
Platform formatting rules:
- **Discord/WhatsApp:** Use bullet lists, not tables
- **Discord links:** Wrap in `<>` to suppress embeds
- **Terminal:** Padded columns are fine

## File Structure

```
openclaw-skill-{{name}}/
├── .github/
│   └── ISSUE_TEMPLATE/
│       └── bug_report.md       # Standard bug report template
├── scripts/
│   └── {{name}}.mjs           # Single CLI file (all commands)
├── docs/
│   ├── API-COVERAGE.md         # Supported vs unsupported API resources
│   ├── CHECKLIST.md            # Pre-publish quality gates
│   ├── CONVENTIONS.md          # ALT-F1 skill conventions
│   └── PUBLISHING.md           # ClawHub publish guide
├── references/                  # Optional: setup guides, API docs, examples
│   └── setup-guide.md          # (e.g. SharePoint cert auth walkthrough)
├── .env.example                # Required + optional vars (commented)
├── .gitignore                  # node_modules, .env, *.log, secrets
├── LICENSE                     # MIT
├── package.json                # ESM, bin, deps, engines >= 18
├── README.md                   # Badges, TOC, standard sections
└── SKILL.md                    # Frontmatter + OpenClaw instructions
```

## README Structure (standard order)

1. **Title** — `# openclaw-skill-{{name}}`
2. **Badges** — License, Node.js, Service, OpenClaw, ClawHub, Security, last-commit, issues, stars
3. **Description** — one line
4. **By-line** — `By [Abdelkrim BOUJRAF](...) / ALT-F1 SRL, Brussels 🇧🇪 🇲🇦`
5. **Table of Contents**
6. **Features**
7. **Quick Start** — clone, install, configure, use (4 steps)
8. **Setup** — prerequisites, credentials, env vars
9. **Commands** — entity table + examples
10. **Security** — auth, `--confirm`, rate limit, no secrets
11. **API Coverage** — link to `docs/API-COVERAGE.md`
12. **ClawHub** — slug + install command
13. **License** — MIT
14. **Author** — with 🇧🇪 🇲🇦, GitHub, X links
15. **Contributing**

## SKILL.md Frontmatter

```yaml
---
name: skill-name-by-altf1be
description: "Concise description with entities, actions, auth method."
homepage: https://github.com/ALT-F1-OpenClaw/openclaw-skill-{{name}}
metadata:
  {"openclaw": {"emoji": "🔧", "requires": {"env": ["HOST", "TOKEN"]}, "optional": {"env": ["MAX_RESULTS"]}, "primaryEnv": "HOST"}}
---
```

**Rules:**
- `name` = ClawHub slug (always ends with `-by-altf1be`)
- `description` = one sentence, include entities + auth method
- `metadata.requires.env` = vars that MUST be set
- `metadata.optional.env` = vars with defaults (new! — Jira/OpenProject use this)
- `metadata.primaryEnv` = the key env var for the service
- NO `license:` field — ClawHub enforces MIT-0

## package.json

```json
{
  "name": "openclaw-skill-{{name}}",
  "version": "1.0.0",
  "type": "module",
  "bin": { "{{name}}": "./scripts/{{name}}.mjs" },
  "dependencies": {
    "commander": "^12.0.0",
    "dotenv": "^16.0.0"
  },
  "engines": { "node": ">=18.0.0" }
}
```

## Versioning

- SemVer: `MAJOR.MINOR.PATCH`
- Git tags: `v1.0.0`, `v1.1.0`, etc.
- Bump with `npm version minor --no-git-tag-version`, then commit + tag + push

## ClawHub Publishing

```bash
clawhub publish . --slug {{slug}} --name "{{Name}} by altf1be" --version 1.0.0
```

**Known issue:** CLI v0.7.0 has `acceptLicenseTerms` bug ([#660](https://github.com/openclaw/clawhub/issues/660)).

---

## Natural Language Usage Section

Production skills (SharePoint, X/Twitter) include a "Usage with OpenClaw" section in README:
```markdown
### Usage with OpenClaw

Once installed as a skill, you can use natural language:

> "List all items"
> "Create a new item called X"
> "Delete item #42"
```
This helps users understand the skill works with conversational commands, not just CLI.

## References Directory (optional)

For skills that require complex setup (e.g. SharePoint cert auth, OAuth flows):
- Add `references/` directory with detailed guides
- Link from SKILL.md/README: `See [references/setup-guide.md](references/setup-guide.md)`
- Keeps SKILL.md concise while providing deep documentation

---

*Last updated: 2026-03-31 — based on 7 production ALT-F1 OpenClaw skills*
