# Code To Mindmap

[中文版](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0-blue)](SKILL.md)

> Converts source code into visual mind maps, node graphs, and tree diagrams using Mermaid syntax

## What Problem This Solves

Code structure is hard to grasp from raw text — class hierarchies, function relationships, and module dependencies are invisible in a flat file. This skill parses source code and produces a visual diagram that reveals the architecture at a glance.

**When triggered:** Source code + visualization/mindmap/flowchart intent.

## Features

- **Multi-language support** — parses Python, JavaScript/TypeScript, Go, and general class/function structures
- **Hierarchical visualization** — shows modules → classes → methods → nested logic as a tree
- **Smart diagram selection** — mindmap for class-heavy files, graph for import dependencies, tree for directory structure
- **External library distinction** — marks imported stdlib/packages differently from project-internal calls

## Quick Start

```bash
# Via ClawHub
clawhub install code-to-mindmap

# Or manually
cp -r code-to-mindmap ~/.openclaw/skills/
```

### Usage

```
/code-to-mindmap
```

Paste source code and ask to visualize it as a mind map.

```
/code-to-mindmap/hierarchy
```

Shows project file/folder tree without analyzing imports.

## Modes

| Mode | Description |
|------|-------------|
| `/code-to-mindmap` | Parses code, outputs Mermaid mindmap or graph |
| `/code-to-mindmap/hierarchy` | Shows file/folder structure only, no import analysis |

## Examples

| Scenario | Diagram |
|----------|---------|
| Single Python class | Center = class name, methods as child nodes |
| Multi-file project | Multiple sub-diagrams per module, import edges |
| Anonymous/lambda functions | Listed as "anonymous / lambda" node |
| 20+ node codebase | Split into sub-diagrams, top-level summary first |

## Directory Structure

```
code-to-mindmap/
├── SKILL.md
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # Mermaid syntax guide, parsing patterns
├── scripts/          # render.py — Mermaid to PNG/SVG
└── tests/
```

## License

MIT License — see [LICENSE](LICENSE).