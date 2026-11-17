# AI Sentinel - ClawHub Skill

This folder contains the ClawHub skill package for AI Sentinel. It provides an interactive setup wizard that installs and configures the `ai-sentinel` OpenClaw plugin (published on npm) for prompt injection protection.

## Folder Structure

```
ai-sentinel/
├── SKILL.md        # Skill entry point (required by ClawHub)
├── CHANGELOG.md    # Version history
├── skill-card.md   # Registry skill card (risks, use case, outputs)
└── README.md       # This file (developer reference)
```

## Declarations (must match SKILL.md frontmatter)

The security scanner compares registry metadata against SKILL.md content and flags mismatches. Current declarations:

| Field              | Value |
|--------------------|-------|
| Optional env vars  | `AI_SENTINEL_API_KEY` (Pro tier only) |
| Required config    | `openclaw.config.ts` |
| External services  | `https://api.zetro.ai` (Pro tier only) |
| Installed packages | `ai-sentinel` (npm, via `openclaw plugins install`) |
| Files written      | `.env`, `.gitignore`, `~/.openclaw/openclaw.json` (all with explicit user confirmation) |

## Publishing to ClawHub

```bash
clawhub publish . --slug ai-sentinel --version <X.Y.Z> --changelog "<summary>"
```

Versioning tracks the `ai-sentinel` npm plugin version the skill installs. Before publishing a skill update that references new plugin features, ensure the plugin is published to npm first (`npm view ai-sentinel version`).

## Testing

To manually test before publishing:

1. Open an OpenClaw project with `openclaw.config.ts`
2. Copy this folder into the project's skills directory
3. Invoke the skill and walk through the setup wizard
4. Verify per SKILL.md Step 7: plugin listed in `openclaw plugins list`, initialization line in gateway logs, a known injection pattern is detected, and benign messages pass through

## Related Files (monorepo)

- `packages/ai-sentinel/` - The OpenClaw plugin published to npm (hooks, scanner, patterns)
- `packages/ai-sentinel/src/scanner/patterns.ts` - The 42 detection patterns across 7 categories
- `packages/ai-sentinel/src/scanner/preprocess.ts` - Obfuscation-resistant preprocessing
