<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ricardodpalmeida/openclaw-excalidraw-diagrams/main/.github/assets/banner-dark.jpg">
  <img alt="excalidraw diagrams: clean, hand-drawn diagrams from a short boxes-and-arrows spec. A sketched Web app box points to an Orders API box, in blue, inside a dashed Backend frame next to Postgres." src="https://raw.githubusercontent.com/Ricardodpalmeida/openclaw-excalidraw-diagrams/main/.github/assets/banner-light.jpg">
</picture>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT-0" src="https://img.shields.io/badge/license-MIT--0-1F5AA6?style=flat-square"></a>
  <img alt="Agent Skill" src="https://img.shields.io/badge/Agent%20Skill-SKILL.md-18191B?style=flat-square">
  <a href="https://clawhub.ai/ricardodpalmeida/skills/excalidraw-diagrams"><img alt="On ClawHub" src="https://img.shields.io/badge/ClawHub-excalidraw--diagrams-6B7280?style=flat-square"></a>
  <a href="https://github.com/Ricardodpalmeida/openclaw-excalidraw-diagrams/actions/workflows/ci.yml"><img alt="CI status" src="https://img.shields.io/github/actions/workflow/status/Ricardodpalmeida/openclaw-excalidraw-diagrams/ci.yml?branch=main&style=flat-square&label=CI"></a>
</p>

Ask an agent for an Excalidraw diagram and it often writes the JSON by hand: boxes overlap, labels spill out and arrows float loose from their shapes. **Excalidraw Diagrams** is an Agent Skill that has your agent describe the diagram as a short spec of boxes, arrows and groups, then hands the drawing to a deterministic Python builder. You get a real Excalidraw file for Obsidian or excalidraw.com, laid out, labelled and bound, so it stays editable: move a box and its arrows follow.

## Quick navigation

[Examples](#from-spec-to-drawing) · [Workflow and spec](#how-it-works) · [Install](#install) · [Package contents](#what-is-inside) · [Release notes](CHANGELOG.md)

## From spec to drawing

Real output, not a mock-up. The spec on the left is [examples/ci-pipeline.json](examples/ci-pipeline.json); the drawing on the right is what `build_diagram.py` wrote from it, exported with Excalidraw's own renderer.

<table>
<tr>
<td width="56%">

```json
{
  "title": "CI pipeline",
  "direction": "TB",
  "theme": "clean",
  "nodes": [
    {"id": "push", "label": "git push",
     "shape": "ellipse", "color": "gray"},
    {"id": "build", "label": "Build"},
    {"id": "test", "label": "Unit tests"},
    {"id": "scan", "label": "Security scan",
     "color": "orange"},
    {"id": "pass", "label": "All green?",
     "shape": "diamond", "color": "yellow"},
    {"id": "deploy", "label": "Deploy to\nstaging",
     "color": "green"},
    {"id": "fix", "label": "Fix and\nrecommit",
     "color": "red"}
  ],
  "edges": [
    {"from": "push", "to": "build"},
    {"from": "build", "to": "test"},
    {"from": "build", "to": "scan"},
    {"from": "test", "to": "pass"},
    {"from": "scan", "to": "pass"},
    {"from": "pass", "to": "deploy", "label": "yes"},
    {"from": "pass", "to": "fix", "label": "no"},
    {"from": "fix", "to": "build", "style": "dashed"}
  ]
}
```

</td>
<td width="44%" align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ricardodpalmeida/openclaw-excalidraw-diagrams/main/.github/assets/example-ci-dark.png">
  <img alt="Hand-drawn CI pipeline: git push leads to Build, which fans out to Unit tests and Security scan, both feeding an All green? diamond that leads to Deploy to staging on yes and to Fix and recommit on no, with a dashed arrow back to Build." src="https://raw.githubusercontent.com/Ricardodpalmeida/openclaw-excalidraw-diagrams/main/.github/assets/example-ci-light.png">
</picture>
</td>
</tr>
</table>

Left to right works too, with groups, colors, a decision and an answer that loops back to the user ([examples/rag-architecture.json](examples/rag-architecture.json), sketch theme):

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ricardodpalmeida/openclaw-excalidraw-diagrams/main/.github/assets/example-rag-dark.png">
  <img alt="Hand-drawn RAG request flow: User sends a question to an Application group with API, Content safety and Retriever; the Retriever queries a Data platform group with Vector index and Document store and sends context to an LLM, whose output goes to a Grounded? diamond that answers the User." src="https://raw.githubusercontent.com/Ricardodpalmeida/openclaw-excalidraw-diagrams/main/.github/assets/example-rag-light.png">
</picture>

## How it works

1. The agent writes a temporary spec of nodes, edges and optional groups, for the destination and format you asked for.
2. `build_diagram.py` assigns layers, routes edges around nodes, sizes every label and binds text and arrows in both directions, with deterministic IDs.
3. `validate.py` checks the structure, the two-way bindings, fonts and overlapping shapes, and warns about edge crossings.
4. The agent fixes errors and adjusts direction, rank or node order for crossings. When the intended renderer is available, it also checks label fit, arrow endpoints and legibility.
5. It returns the file path, any unresolved warnings and the visual inspection result. If rendering was unavailable, it says so; a valid JSON scene is not a visual pass.

| Spec field | Values |
|---|---|
| `direction` | `TB` (top to bottom, default) or `LR` (left to right) |
| `theme` | `sketch` (hand-drawn, default) or `clean` (straight lines) |
| `font` | `excalifont` (default), `virgil`, `helvetica`, `cascadia`, `nunito`, `lilita`, `comic` |
| node `shape` | `rectangle` (default), `ellipse`, `diamond` |
| node and group `color` | `blue`, `green`, `red`, `orange`, `purple`, `yellow`, `cyan`, `pink`, `gray`, `white` |
| node `rank`, `link` | pin a node to a layer; attach a URL or an `[[Obsidian link]]` |
| edge `style` | `solid` (default), `dashed`, `dotted`, plus `"bidirectional": true` |

Layouts the builder cannot express, such as grids, can still be written by hand with the [file format reference](references/excalidraw-format.md) and then validated. The builder uses only Python's standard library, makes no network calls and never overwrites an existing file without `--force`.

## Install

OpenClaw is the primary target:

```bash
openclaw skills install @ricardodpalmeida/excalidraw-diagrams            # this workspace
openclaw skills install @ricardodpalmeida/excalidraw-diagrams --global   # all agents
```

The folder is a standard Agent Skill, so other agents that read `SKILL.md` can use it too. Clone it into the agent's skills folder under the skill's name:

| Agent | Command |
|---|---|
| Claude Code | `git clone https://github.com/Ricardodpalmeida/openclaw-excalidraw-diagrams ~/.claude/skills/excalidraw-diagrams` |
| Codex | `git clone https://github.com/Ricardodpalmeida/openclaw-excalidraw-diagrams ~/.codex/skills/excalidraw-diagrams` |
| GitHub Copilot | `git clone https://github.com/Ricardodpalmeida/openclaw-excalidraw-diagrams ~/.copilot/skills/excalidraw-diagrams` |

The instructions call the skill folder `{baseDir}`: OpenClaw fills it in, and elsewhere it means the folder you cloned into. It needs Python 3.9 or newer and nothing else. Then ask in plain words, for example "draw our CI pipeline as an Excalidraw diagram in my Obsidian vault". The skill loads only for explicit Excalidraw requests.

To try the builder without an agent:

```bash
python3 scripts/build_diagram.py --spec examples/ci-pipeline.json --out ci-pipeline.excalidraw
python3 scripts/validate.py ci-pipeline.excalidraw
```

Open the file on excalidraw.com, or name it `.excalidraw.md` and open it in Obsidian with the Excalidraw plugin.

## What is inside

```
SKILL.md                          workflow and the full spec format
scripts/build_diagram.py          layout, label sizing, two-way bindings, deterministic IDs
scripts/validate.py               structure, bindings, fonts and overlap checks
references/excalidraw-format.md   the file format, for layouts the builder cannot express
examples/                         sample specs, built and validated in CI
tests/                            python3 -m unittest discover -s tests
```

Release notes are in [CHANGELOG.md](CHANGELOG.md).

## License

[MIT-0](LICENSE). Use, share, modify and redistribute it, including commercially, without an attribution requirement. The same license applies on ClawHub.

## Author

**Ricardo Pacheco Almeida**, Senior AI Tech Lead and Architect and PhD student researching enterprise and solution architectures for generative AI, including multi-agent structures.

[Website](https://me.ricbits.cc/en/) · [LinkedIn](https://www.linkedin.com/in/ricardodpa/) · [GitHub](https://github.com/Ricardodpalmeida) · [ClawHub](https://clawhub.ai/ricardodpalmeida)

More skills by the same author:

| Skill | What it does |
|---|---|
| [data-storycraft](https://github.com/Ricardodpalmeida/data-storycraft-skill) | Turn analysis into charts, slides and reports that make the point |
| [Whetstone](https://github.com/Ricardodpalmeida/whetstone) | Scale your coding agent's engineering care to the risk of each change |
| [Book Capture for Obsidian](https://github.com/Ricardodpalmeida/book-capture-obsidian-skill) | Turn photos, ISBNs or Goodreads exports into Obsidian book notes |
| [Microsoft Learn MCP](https://github.com/Ricardodpalmeida/openclaw-mslearn-mcp) | Ground Microsoft answers in current Learn docs and code samples |
| [Multi-cloud Docs](https://github.com/Ricardodpalmeida/multicloud-docs) | Ground cloud and AI platform answers in each vendor's own current docs |
| [LadybugDB openCypher](https://clawhub.ai/ricardodpalmeida/skills/ladybug-opencypher-updated) | Work with LadybugDB property graphs using openCypher and Python |
