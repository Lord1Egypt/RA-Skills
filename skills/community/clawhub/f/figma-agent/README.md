<h1 align="center">Figma Agent</h1>

<p align="center">
  <strong>Workflow-driven Figma skill for OpenClaw — inspect designs directly, then create, review, and edit screens through structured Figma workflows.</strong><br>
  Built on the official <a href="https://help.figma.com/hc/en-us/articles/32132100833559">Figma Remote MCP server</a>.
</p>

<p align="center">
  <a href="https://github.com/rasimme/figma-agent/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
  <a href="https://github.com/rasimme/figma-agent/blob/main/CHANGELOG.md"><img src="https://img.shields.io/badge/version-v0.3.0-blue.svg" alt="Version"></a>
  <a href="https://clawhub.ai"><img src="https://img.shields.io/badge/ClawHub-skill-purple.svg" alt="ClawHub"></a>
</p>

<p align="center">
  <a href="#what-this-skill-does">What this skill does</a> •
  <a href="#core-architecture">Core architecture</a> •
  <a href="#supported-workflows">Supported workflows</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#image-delivery">Image Delivery</a> •
  <a href="#limitations">Limitations</a>
</p>

---

## What this skill does

Figma Agent is not just a raw MCP wrapper. It is a structured OpenClaw skill for working with Figma in two modes:

- **Direct read / inspect** for screenshots, metadata, design context, variables, and Code Connect inspection
- **Structured write / edit workflows** for building screens, reviewing existing work, applying tokens, and iterating on designs through ACP coding sessions

Typical use cases:

- "Show me this screen and tell me what is off"
- "Build the next step based on this existing screen"
- "Replace hardcoded colors with design-system tokens"
- "Inspect local variables and Code Connect mappings"
- "Create a production-ready screen using existing components"

---

## Core architecture

The skill is intentionally split into four layers:

1. **`SKILL.md`** — routing surface for deciding direct read vs ACP write/edit
2. **`references/workflow-selection.md`** — workflow and strategy selection
3. **`references/core-rules.md`** — global execution rules and constraints
4. **`references/prompting-patterns.md` + playbooks** — prompt structure and step-by-step execution

### Runtime model

- **Read / inspect** goes directly to Figma MCP
- **Write / create / edit** goes through an ACP coding session with Figma MCP available

This hybrid model keeps inspection fast while preserving a stronger execution path for canvas changes.

### Execution model

The controller should operate in three phases:

1. **Route & Brief** — choose the workflow, identify the actual risks, and produce a lean execution brief
2. **Execute** — perform the direct read or ACP write/edit task
3. **Done Gate** — require structural checks first and screenshot confirmation second before reporting success

---

## Supported workflows

### Read / Inspect

- **Read-only inspection** — screenshots, metadata, design context, variables, Code Connect context
- **Variable Discovery** — inspect local tokens and styles before searching externally
- **Design Audit Review** — review a finished design and identify issues or cleanup opportunities

### Create / Edit

- **Native Screen Generation** — production-ready, design-system-aligned screen creation
- **Screen Review Loop** — screenshot, isolate issues, apply targeted fixes, validate
- **Color Tokenization** — replace hardcoded values with variable bindings
- **HTML-to-Figma Prototyping** — rapid exploration from HTML/CSS, then cleanup
- **Stitch Import Cleanup** — fix imported Stitch output for native Figma quality
- **State Variants / Next Steps** — prefer **Copy + Edit** over rebuild when most of the screen already exists

### Execution principles

- **Design-system-first** — use local variables, styles, components, and Code Connect before creating anything raw
- **Component-instance-first** — if a suitable component exists, instantiate it instead of rebuilding it visually
- **Section-by-section** — build in small validated steps, not giant write calls
- **Validate after every write** — structural checks first, screenshots second

---

## Quick Start

### Prerequisites

- [OpenClaw](https://github.com/openclaw/openclaw) installed
- [Node.js](https://nodejs.org) available
- Figma account connected to a supported MCP client
- **Full Seat** in Figma for write operations (`use_figma`)

### Install

**Via ClawHub (recommended):**

```bash
clawhub install figma-agent
```

**Manual install:**

```bash
cd ~/.openclaw/skills
git clone https://github.com/rasimme/figma-agent.git
cd figma-agent
npm install
```

### Bootstrap authentication

```bash
node ~/.openclaw/skills/figma-agent/scripts/bootstrap-token.mjs
```

The bootstrap script extracts or refreshes the Figma MCP token from a supported MCP client and writes the Figma server config into your OpenClaw config.

Then restart OpenClaw:

```bash
openclaw gateway restart
```

### Verify

Check that Figma MCP is configured in `~/.openclaw/openclaw.json` under `mcp.servers.figma`, then try a simple read action such as `get_screenshot` or `get_metadata`.

---

## Image Delivery

For chat delivery, screenshots should be sent as actual image attachments, not inline base64 blobs.

### Recommended pattern

1. Save the screenshot to disk with `--out`
2. Reply with `MEDIA:<path>`

Example:

```bash
node scripts/figma-mcp-cli.mjs get_screenshot \
  fileKey=<fileKey> nodeId=<nodeId> scale=2 \
  --out ~/workspace-dev-botti/screenshots/validate.png
```

Then in chat:

```text
MEDIA:screenshots/validate.png
```

### Important distinction

- `image` tool = image analysis / vision input
- `MEDIA:<path>` = actual chat attachment delivery

This matters especially on Telegram, where inline base64 is not the same as a native image attachment.

---

## Tool coverage

The skill supports the official Figma Remote MCP toolset for inspection and canvas operations. Commonly used tools include:

- `get_design_context`
- `get_screenshot`
- `get_metadata`
- `get_variable_defs`
- `search_design_system`
- `get_code_connect_map`
- `get_figjam`
- `whoami`
- `use_figma`
- `create_new_file`
- `generate_figma_design`
- `generate_diagram`
- Code Connect mapping helpers

For full tool-level details, see [`references/figma-api.md`](references/figma-api.md).

---

## Limitations

Current known constraints:

- **Write operations require a Full Seat** in Figma
- **Large write calls are fragile** — split work into smaller sections
- **Remote MCP write behavior still has edge cases** — validate after each change
- **Some Plugin API behavior differs in Remote MCP** — see [`references/plugin-api-gotchas.md`](references/plugin-api-gotchas.md)
- **Image delivery works best through local file output + `MEDIA:`**
- **State variants should usually duplicate and edit existing screens rather than rebuild from scratch**
- **Playbooks guide the agent, not ACP automatically** — critical execution constraints must still be injected into ACP prompts when relevant

---

## Project structure

```text
figma-agent/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE
├── package.json
├── references/
│   ├── core-rules.md
│   ├── figma-api.md
│   ├── plugin-api-gotchas.md
│   ├── prompting-patterns.md
│   └── workflow-selection.md
└── scripts/
    ├── bootstrap-token.mjs
    ├── figma-mcp-cli.mjs
    ├── figma-mcp.mjs
    └── token-scanner.mjs
```

---

## License

MIT — see [LICENSE](LICENSE).
