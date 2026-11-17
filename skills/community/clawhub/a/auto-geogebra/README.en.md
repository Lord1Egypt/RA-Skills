<sub>🌐 <a href="README.md">中文</a> · <b>English</b></sub>

<div align="center">

# auto-geogebra

> *「A teaching idea is a spark; what you bring to class is a .ggb — this skill has already run every step on the real engine for you.」*

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-auto--geogebra-blueviolet)](SKILL.md)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![CI](https://github.com/zhjx19/auto-geogebra/actions/workflows/smoke.yml/badge.svg)](https://github.com/zhjx19/auto-geogebra/actions/workflows/smoke.yml)
[![smoke](https://img.shields.io/badge/smoke-22%20checks%20%2F%200%20FAIL-brightgreen)](scripts/smoke_test.py)
[![skills.sh](https://skills.sh/b/zhjx19/auto-geogebra)](https://skills.sh/zhjx19/auto-geogebra)

**Turn a university-math teaching idea into a runnable, editable, verifiable GeoGebra demo: clarify → design variables → generate commands → dual validation → real-engine export to .ggb.**

[Showcase](#showcase) · [Install](#quick-start) · [Triggers](#triggers) · [Differences](#how-its-different) · [Safety](#safety-boundaries)

</div>

---

<img src="assets/demo.gif" alt="Seven real GeoGebra examples" width="100%">

<sub>Seven real examples: derivative definition · linear transform · sphere cross-section · button secant · regular n-gon → circle · Taylor approximation · coin-toss frequency. All exported by the official engine via `tools/ggb-export`; .ggb files live in examples/.</sub>

---

## Why this exists

You have a great teaching moment in mind — "let students drag a point and watch the secant become the tangent" — and you hand it to an agent. What comes back is GeoGebra command text that *looks* right: half of it errors on import, the slider starts at zero so two points coincide and nothing renders, and after export the buttons silently do nothing.

GeoGebra has 500+ commands and a set of traps that **only the real engine reveals**: lowercase names with coordinates become *vectors*, objects clashing with built-in functions (`sec`, `tan`) get silently renamed, degenerate initial values "succeed" while creating nothing, and script commands always return `false` even when they work.

This skill turns "teaching idea → classroom-ready .ggb" into a validated pipeline: clarify requirements first (no guessing), design an interaction-variable table, generate commands, pass **L1 syntax + L2 semantic dual validation**, then execute every command against the official engine in a local headless browser — verified per-command, exported with read-back checks. Fully local, zero API keys.

> The in-product documentation is Chinese (the target audience is Chinese university math teachers); commands, file formats, and repo structure are universal.

## Showcase

```text
"Teach the derivative as the limit of secant slopes — point B approaches point A, the secant approaches the tangent."
```

You get: ① a requirement-confirmation sheet; ② validated command code with a dual-validation summary; ③ a real-engine-exported `.ggb` + preview image.

![Derivative example](assets/demo1-derivative-definition.png)

<sub>Example 1 · Derivative definition: drag h from 2 → 0.01 and watch the secant approach the tangent.</sub>

![Regular polygon example](assets/demo5-polygon-circle.png)

<sub>Example 5 · Regular n-gon approaching the circle: slide n; play/stop/reset buttons included.</sub>

![Coin toss example](assets/demo7-coin-toss.png)

<sub>Example 7 · Coin-toss frequency: one-click re-toss; frequency stabilizes to 0.5.</sub>

## Quick Start

```bash
npx skills add zhjx19/auto-geogebra
```

- Static validation: Python 3.8+, **no third-party dependencies**;
- Real-engine export (optional): Node 18+ with local Chrome/Edge (engine loads from CDN on first run);
- **Zero API keys**; nothing is uploaded.

First prompt after install:

```text
Build a GeoGebra demo for "derivative as the limit of secant slopes" — point B approaches point A, the secant approaches the tangent.
It should be draggable, pass dual validation, and come back as a .ggb file.
```

<details>
<summary>Claude Code plugin marketplace (optional)</summary>

This repo ships `.claude-plugin/marketplace.json`: add it in Claude Code via `/plugin marketplace add zhjx19/auto-geogebra`.
</details>

## Triggers

- "Turn this topic into a GeoGebra interactive demo"
- "Make a draggable math courseware and export a .ggb"
- "Design the interaction variables / sliders for this demo"
- "Validate these GeoGebra commands for me"
- "This concept is too abstract — I want students to see the change"
- "Add a reset / re-toss button to the classroom demo"
- "Build small demos for these concepts, one each"

## How it's different

| Dimension | Raw agent output | GeoGebra MCP | auto-geogebra |
| --- | --- | --- | --- |
| Command correctness | From model memory, often wrong | Depends on connected service | 500+ command index + L1 syntax + L2 semantic validation |
| Real-engine check | None | Yes (needs setup) | Built-in headless exporter: per-command verify + read-back + preview |
| Known traps | Discovered the hard way | — | Engine-tested rule base (vectors / reserved names / degenerate values / script silent failures) |
| Interactive buttons | None | Manual | `ggb_patch.py` injects onClick / onUpdate scripts |
| Teaching workflow | Generic | Generic | Requirement clarification + variable design + 28 university-math topic routes |
| Output | A blob of text | Execution result | Double-clickable .ggb + preview + validation summary |

## Safety boundaries

- **Does not replace the teacher's design**: the skill implements ideas; pedagogy stays yours;
- **Never fabricates artifacts**: without a browser/network it says so and delivers commands + instructions instead;
- **States the limits of static validation**: scripts, 3D, `Locus`, etc. are marked "must run to confirm";
- **No network upload**: validation and export are local (except the first engine CDN load);
- **Does not touch your files**: reads the material you give it, writes outputs to the path you choose.

## Repository layout

```text
auto-geogebra/
├── SKILL.md                      # Main workflow: clarify → design → implement → dual validation → export
├── test-prompts.json             # 5 real test scenarios
├── references/
│   ├── course-routing.md         # 28 university-math topic routes
│   ├── command-validation.md     # Static validation checklist
│   ├── anti-patterns.md          # Common failures & anti-patterns (engine traps / validation traps / teaching anti-patterns)
│   ├── patterns.md               # 6 teaching design patterns
│   ├── interaction-patterns.md   # Buttons / animation / reset patterns
│   └── workflow.md               # Teacher workflow quick reference
├── scripts/                      # L1/L2 validators, smoke test, index builder
├── data/                         # 500+ command index; zh→en command aliases
├── tools/ggb-export/             # Real-engine exporter (zero npm deps) + button script injector
├── examples/                     # 7 real examples (sources + .ggb + reproduction notes)
├── assets/                       # Demo GIF / screenshots + reproducible compose script
├── .claude-plugin/               # Claude Code plugin marketplace
└── .github/workflows/            # CI: smoke + validators (Windows / Ubuntu matrix)
```

## Verify & test

```bash
python scripts/smoke_test.py     # expect: 22 checks, 0 failures
```

CI runs the smoke test and both validators on **Windows and Ubuntu** for every push (see the Actions tab). When something errors or fails silently, check [references/anti-patterns.md](references/anti-patterns.md) first.

## Acknowledgements

- [Luban Skill Workshop](https://github.com/LearnPrompt) — polishing workflow and release checklist
- [GeoGebra manual](https://github.com/GeoGebra/manual) — source of the command index
- [ggbgen.pages.dev](https://ggbgen.pages.dev/) — online batch executor fallback

## License

[Apache License 2.0](LICENSE)

---

<div align="center">

*Turn the next teaching idea into something draggable in class.*

</div>
