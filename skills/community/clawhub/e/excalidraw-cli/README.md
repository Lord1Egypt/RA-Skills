[![ClawHub](https://img.shields.io/badge/ClawHub-excalidraw-cli-red)](../..) [![License](https://img.shields.io/badge/license-MIT--0-blue)](../..) [![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)](../..)

---
name: excalidraw-cli
version: 2.0.0
description: Generate Excalidraw diagrams (flowcharts, sequences, architecture) as valid .excalidraw JSON
tags: ["excalidraw", "diagrams", "flowchart", "architecture", "cli", "drawing", "python", "open-source", "agent", "automation", "MIT"]
---

# Excalidraw Diagram CLI

**Generate Excalidraw diagrams — flowcharts, sequences, architecture — as valid .excalidraw JSON.**

> *Keywords: excalidraw, diagrams, flowchart, architecture, cli, drawing, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Drawing diagrams by hand is slow and not version-controllable. Excalidraw Diagram CLI solves this: Generate Excalidraw diagrams — flowcharts, sequences, architecture — as valid .excalidraw JSON.

**Best for:** Engineers documenting architecture, agents generating diagrams, and tech writers.

## Features

- **Generate a flowchart**
- **Build a sequence diagram**
- **Compose an architecture map**
- **Merge/overlay diagrams**
- **Export valid Excalidraw JSON**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/excalidraw-cli/main/excalidraw_cli.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python excalidraw_cli.py self-test     # prove it works end-to-end
python excalidraw_cli.py diagram --help   # diagram subcommand
python excalidraw_cli.py merge --help   # merge subcommand
python excalidraw_cli.py info --help   # info subcommand
python excalidraw_cli.py export --help   # export subcommand
```

## Use cases

1. Generate a flowchart
1. Build a sequence diagram
1. Compose an architecture map
1. Merge/overlay diagrams
1. Export valid Excalidraw JSON

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Drag-drop in Excalidraw | Diagrams as code, diff-able in git. |
| Mermaid only | Native Excalidraw JSON, hand-drawn style. |
| Screenshots | Regenerate from text anytime. |

## FAQ (SEO / AEO)

**Q: Diagram types?**  
A: flow, sequence, architecture (--type).

**Q: Valid output?**  
A: Emits Excalidraw-compatible JSON you can open in the app.

**Q: Compose?**  
A: merge/overlay combine diagrams.

**Q: Offline?**  
A: Yes.

## Geo / local reach

Built and maintained by [@itsPremkumar](https://github.com/itsPremkumar) (Chennai, India · serving developers worldwide). 
Free for individuals and teams everywhere. Documentation in English; tool output is locale-neutral.

## CI integration

```yaml
# .github/workflows/verify.yml
name: Verify
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Self-test excalidraw-cli
        run: python excalidraw_cli.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/excalidraw-cli)
