# Beauty Diagram skill

Turn Mermaid / PlantUML source into sleek, modern SVG or PNG — straight
from your agent. This skill teaches Claude (or any compatible agent) to call
the [`bd` CLI](https://www.npmjs.com/package/@beauty-diagram/cli) instead of
hand-authoring SVG, so you get consistent, slide-quality diagrams without
leaving the conversation.

## What it does

- Beautifies existing Mermaid / PlantUML files into polished SVG/PNG
- Renders model-generated diagram source on demand
- **Generates a diagram from a text prompt** via `bd ai generate`
  (Pro / Premium plans only)
- Produces shareable `https://www.beauty-diagram.com/s/...` links
- **Generates direct embed URLs** for README / Notion / blog use: runs
  `bd share` and returns `https://api.beauty-diagram.com/v1/share/<id>.svg`
  rather than emitting raw Mermaid — the URL works as a plain `<img src>`
  anywhere that renders images. Anonymous (watermarked) embeds are also
  available via `bd embed-url` with no sign-in required.
- Surfaces actionable error codes (`quota_exhausted`, `parse_failed`,
  `prompt_injection`, …) instead of silently retrying

## Requirements

- **Node.js** (for `npx @beauty-diagram/cli`); no global install needed
- **Optional**: a Beauty Diagram API key for unwatermarked output, share
  links, and higher quotas — anonymous demo mode works out of the box
  (1 export per IP per 24h)
- **For AI generation**: an API key with the `ai:write` scope on a Pro
  or Premium plan. Anonymous and free plans cannot call `bd ai generate`.

Get a key at <https://www.beauty-diagram.com/account/api-keys>.

## Triggering

The skill activates when a user asks for things like:

- "beautify this flowchart"
- "make this Mermaid diagram look like a deck slide"
- "give me an SVG of this architecture"
- "draw me a diagram of the signup flow"
- "share this diagram as a link"

## Example

```
You: Here's our service flow in Mermaid — make it slide-ready and give me a share link.

Agent (uses skill):
  $ bd beautify flow.mmd --theme modern --out flow.svg
  $ bd share flow.mmd --title "Service flow"
  → https://www.beauty-diagram.com/s/abc123
```

```
You: Draw me a deploy pipeline diagram and beautify it.

Agent (uses skill, Pro plan):
  $ bd ai generate "deploy pipeline with build, test, staging, prod" --out deploy.mmd
  $ bd beautify deploy.mmd --out deploy.svg
  → wrote deploy.mmd (editable) + deploy.svg (presentation)
```

```
You: Add this architecture diagram to my README as an embedded image.

Agent (uses skill, Pro/Premium plan):
  $ bd embed-url ./architecture.mmd --share
  → https://api.beauty-diagram.com/v1/share/abc12345xyz0.svg
  Injects into README: ![Architecture](https://api.beauty-diagram.com/v1/share/abc12345xyz0.svg)
```

See `examples/` for runnable diagram sources and `scripts/` for shell
wrappers you can drop into a repo.

## Source-level directives

Both the `bd` CLI and the Obsidian plugin support `bd:KEY=VALUE` directives
embedded at the **start of your diagram source** as native comments. The API
server does not parse them, but because they are valid comment syntax for both
Mermaid and PlantUML, the source renders normally everywhere — graceful
degradation at no cost.

### Grammar

**Mermaid** — one directive per `%%` comment line:

```
%% bd:theme=classic
%% bd:bg=transparent
flowchart LR
  A --> B
```

**PlantUML** — one directive per `'` comment line:

```
' bd:theme=classic
' bd:bg=transparent
@startuml
A -> B
@enduml
```

Rules:
- All `bd:` lines must appear **before the first non-blank, non-directive line**.
- Blank lines between directives are tolerated.
- Multiple directives stack — both `theme` and `bg` can be set together.

### Supported keys

| Key | Accepted values | Notes |
|---|---|---|
| `theme` | `classic`, `modern`, `slate`, `atlas`, `obsidian`, `brutalist`, `atelier`, `blueprint`, `memphis` | Overrides the render theme. Tier gating still applies — anonymous callers get watermarked output regardless of theme. |
| `bg` | `theme`, `white`, `dark`, `transparent` | Canvas background. `dark` automatically hue-lifts the diagram's ink so edges and labels stay legible; `transparent` is useful for overlaying on coloured slide backgrounds. Unknown values fall back to `theme`. |

Theme tiers: **Free** — `classic`, `modern`, `slate`; **Pro** — adds `atlas`,
`obsidian`, `brutalist`, `atelier`; **Premium** — adds `blueprint`, `memphis`.

### Override priority

```
CLI flag  >  source directive  >  server default
```

A `--theme atlas` flag always wins over a `%% bd:theme=classic` directive in
the source. Directives are useful when the file is the single source of truth
(shared repos, Obsidian vaults) and the CLI flags aren't part of the workflow.

### Why use directives instead of CLI flags?

- The theme intent **travels with the file** — anyone who opens the `.mmd` in
  the Obsidian plugin, or runs `bd beautify` without `--theme`, still gets the
  right style.
- Works transparently in the Obsidian plugin, where there is no CLI invocation.
- Directives are stripped before the source reaches the renderer — they do not
  appear in the SVG output.

## Files

```
beauty-diagram-skill/
├── SKILL.md          # agent-facing instructions
├── examples/         # sample Mermaid sources
│   ├── flowchart.mmd
│   └── sequence.mmd
└── scripts/          # copy-pasteable shell wrappers
    ├── beautify.sh
    ├── export.sh
    └── ai-generate.sh   # prompt → .mmd → .svg
```

## Links

- Site: <https://www.beauty-diagram.com>
- CLI on npm: <https://www.npmjs.com/package/@beauty-diagram/cli>
- API keys: <https://www.beauty-diagram.com/account/api-keys>

## License

MIT-0 (per ClawHub publishing terms).
