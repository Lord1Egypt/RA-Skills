# Deep Research

An [OpenClaw](https://github.com/anthropics/openclaw) skill for deep research — produces comprehensive, well-sourced Markdown reports. Works with any AI platform: [Gemini CLI](https://github.com/google-gemini/gemini-cli), Claude Code, or any tool that supports SKILL.md-style prompts.

## Architecture

```mermaid
flowchart LR
    Q[Query] --> D[Decompose<br/>3-5 sub-questions]
    D --> B[Breadth Search<br/>8-15 web searches]
    B --> R[Deep Read<br/>5-10 full pages]
    R --> G[Gap Analysis<br/>2-3 follow-ups]
    G --> S[Synthesize<br/>structured report]
    S --> C[Quality Check<br/>citations & accuracy]
    C --> report[Markdown Report]

    style Q fill:#4a9eff,color:#fff
    style report fill:#34d399,color:#fff
```

**Tool mapping** — the skill adapts to whatever tools are available:

| Step | Gemini CLI | Claude Code | Generic |
|------|-----------|-------------|---------|
| Web search | `google_web_search` | `WebSearch` | any search tool |
| Page fetch | `web_fetch` | `WebFetch` | any fetch tool |

## Quick Start

**Option A: Gemini CLI Skill**
```bash
git clone https://github.com/yangsjt/deep-research.git ~/projects/deep-research
gemini skills link ~/projects/deep-research
```

**Option B: Standalone Script**
```bash
git clone https://github.com/yangsjt/deep-research.git ~/projects/deep-research
./scripts/search.sh -p "Latest developments in RISC-V 2026"
```

**Option C: Any AI Platform** — Copy `SKILL.md` into your AI's prompt or skill config. The methodology is self-contained; it only requires web search and page fetch capabilities.

> **Note:** Gemini CLI requires [Google AI Premium](https://one.google.com/explore-plan/gemini-advanced) and OAuth auth (`gemini login`). No separate API keys needed.

## Usage

### Script

```bash
./scripts/search.sh -p "AI Agent frameworks comparison 2026"
./scripts/search.sh -p "WebAssembly component model" -n "wasm" --background
./scripts/search.sh --help   # all options
```

### Interactive (Skill Mode)

Trigger with any of these phrases in your AI assistant:

> `deep search` · `deep research` · `深度研究` · `深度思考` · `深度学习` · `comprehensive research`

```
$ gemini
> deep search: State of RISC-V in consumer electronics
```

## License

[MIT](LICENSE)
