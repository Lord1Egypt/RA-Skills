# Designing TUIs

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skill](https://img.shields.io/badge/type-skill-blue.svg)](./SKILL.md)

A structured skill and reference for designing **Terminal User Interfaces (TUIs)**. Covers dialogue-driven design, screenshot-to-code workflows, and the `.tui` schema for producing consistent, accessible, and framework-portable TUI implementations.

> **Use case**: AI-assisted TUI generation, design-to-code pipelines, and human-AI collaboration on terminal interfaces.

## What’s Inside

- `SKILL.md` — Primary skill entrypoint with the dual-route architecture, 3-phase decomposition protocol, proportion mechanism, comparison/iteration protocol, and accuracy expectations.
- `references/components-cheatsheet.md` — Component defaults, visual signatures, and disambiguation rules.
- `references/layout-inference-rules.md` — Layout direction, component identification, spacing, proportion, border, and color inference rules.
- `references/color-accessibility.md` — WCAG color standards, color-blind safe palettes (Okabe-Ito, IBM), contrast requirements, and TUI-specific accessibility guidelines.
- `references/schema-to-code-mapping.md` — `.tui` Schema → framework code (BubbleTea / Ink / Textual) conversion reference.
- `references/known-quirks.md` — tui-studio pitfalls and workarounds.
- `references/workflow-examples.md` — Dual-route workflow walkthroughs with 3-phase protocol examples.

## Quick Start

1. Read [`SKILL.md`](./SKILL.md) for the overall protocol.
2. Refer to [`references/components-cheatsheet.md`](./references/components-cheatsheet.md) when interpreting UI screenshots.
3. Use [`references/schema-to-code-mapping.md`](./references/schema-to-code-mapping.md) to turn `.tui` schemas into framework code.

## Supported Frameworks

- [Bubble Tea](https://github.com/charmbracelet/bubbletea) (Go)
- [Ink](https://github.com/vadimdemedes/ink) (React / Node.js)
- [Textual](https://github.com/Textualize/textual) (Python)
- [Ratatui](https://github.com/ratatui/ratatui) (Rust)

## Contributing

Suggestions for new components, framework mappings, or workflow examples are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).

## Keywords

`tui` `terminal-user-interface` `design-to-code` `screenshot-to-code` `bubble-tea` `ink` `textual` `ratatui` `cli` `ui-design` `accessibility` `wcag` `schema` `skill`
