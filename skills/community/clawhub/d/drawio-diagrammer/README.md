# draw.io Diagrammer Skill

Generate aesthetically beautiful, professional draw.io diagrams — with a mandatory visual QA loop built in so your agent doesn't just build diagrams, it builds diagrams that actually look right.

## The problem with most diagram skills

Most diagram skills generate XML, export a PNG, and ship it. The result often looks broken at normal zoom: text overflowing boxes, arrows cutting through other elements, cramped spacing, elements touching that shouldn't be. These issues are invisible at thumbnail scale and obvious at full size.

This skill fixes that. A mandatory screenshot-analyze-fix loop is baked into every generation workflow. The agent exports, inspects every section, finds and fixes every issue, re-exports, and repeats until the diagram is clean. Nothing ships until it passes a visual check.

## What you get

- **Aesthetically beautiful diagrams** — proper spacing, consistent colors, clean typography, visual breathing room throughout
- **Mandatory visual QA loop** — export → inspect section by section → fix every issue → re-export → repeat until clean
- **Universal box spacing standards** — text never touches box walls; overflow-resistant height formulas included
- **Correct arrow routing** — chained arrows instead of fan-out patterns that cut through boxes
- **5 diagram types** — each with full XML templates, color palettes, and type-specific rules:
  - Flowcharts / SOPs (including two-column step + notes layout)
  - ERDs / database diagrams (crow's foot notation, PK/FK badges, color-coded table roles)
  - Architecture / system diagrams
  - UML class diagrams
  - Sequence diagrams
- **macOS + Linux/headless** CLI support

## Requirements

- draw.io desktop app installed (`drawio` binary available)
- macOS: `/Applications/draw.io.app/Contents/MacOS/draw.io`
- Linux/headless: `xvfb-run` + `drawio`

## File structure

```
SKILL.md                              # Main entrypoint
references/
├── visual-review-protocol.md         # Screenshot-analyze-fix loop (mandatory)
├── box-style-standards.md            # Universal spacing, height math, arrow routing
├── workflow-sop.md                   # Delivery workflow, file management
└── diagram-types/
    ├── flowchart.md
    ├── erd.md
    ├── class.md
    ├── sequence.md
    └── layout.md
```

## Usage

Invoke this skill whenever a user requests a diagram, flowchart, ERD, architecture visualization, or asks to edit an existing `.drawio` file. The skill handles type detection, generation, and the full visual QA loop automatically.

## What makes this different

| Feature | This skill | Generic diagram skills |
|---|---|---|
| Visual QA loop | Mandatory, every export | Not included |
| Section-by-section inspection | Yes, with PIL crop scripts | No |
| Box spacing standards | Universal, documented formula | Minimal or none |
| Arrow routing rules | Chained pattern enforced | Fan-out allowed (causes issues) |
| Known draw.io limitations | Documented and worked around | Not addressed |
| Format delivery | PNG first, then user picks format | Varies |
