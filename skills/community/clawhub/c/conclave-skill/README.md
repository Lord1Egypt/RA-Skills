# Conclave

[![Hermes Skill](https://img.shields.io/badge/Hermes-Skill-blue)](https://github.com/MCLYang/conclave-skill)
[![Version](https://img.shields.io/badge/version-1.6.2-green)]()

> **Conclave** is a multi-agent reasoning skill that orchestrates multiple AI CLIs into structured debates. Each agent independently analyzes the problem, challenges competing arguments, identifies flaws and contradictions, and refines the reasoning through multiple rounds of discussion — helping you reach more reliable conclusions than relying on a single AI.

---

## Core Capabilities

| Capability | Description |
|------------|-------------|
| **Independent Positioning** | Five agents (Hermes, Claude, Codex, Gemini, Qwen) analyze the same brief in parallel, unseen by each other, preventing anchoring. |
| **Anonymous Rebuttal** | Each agent receives the other four's R1 arguments (anonymized) and must identify at least one fatal flaw plus a concrete alternative solution. |
| **Structured Convergence** | Chair (Hermes) synthesizes consensus and divergence points after each round; divergence points are sent back for further debate (dynamic rounds, hard ceiling 8). |
| **Unanimous Sign-off** | Final draft circulated to all five; any objection must include a specific clause, specific reason, and an executable alternative. No-destruction-without-construction = invalid vote. |
| **External Audit** | Manus reviews the final draft before delivery; a fatal-level objection triggers an extra round. |
| **Automatic Archiving** | Every debate gets its own folder; all intermediate files are persisted by round. See **Security & Privacy** below for retention controls. |

## ⚠️ Security & Privacy

- **Data persists locally**: Debates are stored under `~/.hermes/debates/` indefinitely. Do not debate topics containing regulated personal data, trade secrets, or classified information unless you accept this risk.
- **Data leaves your machine**: Prompts are sent to Claude (Anthropic), Codex (OpenAI), Gemini (Google), and Qwen (Alibaba) cloud APIs. The optional Manus advisor receives the final draft via MCP. Review each provider's data policy.
- **No password storage**: This skill never prompts for, stores, or logs passwords. The macOS keychain must be unlocked manually by the user in an interactive terminal before background sessions.
- **Input validation**: Topic slugs are sanitized to 1-32 lowercase letters, digits, and hyphens.
- **Cleanup**: Run `bash ~/.hermes/skills/conclave/scripts/cleanup.sh [days]` to purge debates older than the retention period. Default is 90 days; use `0` for a dry-run preview.

---

## Quick Start

```bash
# 0. First time on this machine? Detect + install all CLIs/dependencies,
#    then configure each provider key it flags as [ACTION]
bash ~/.hermes/skills/conclave/scripts/install.sh

# 1. Initialize a debate arena
bash ~/.hermes/skills/conclave/scripts/init_debate.sh <topic-slug>

# 2. Pre-flight check (update all CLIs, then ignition-ping every agent)
bash ~/.hermes/skills/conclave/scripts/preflight.sh <arena-path>

# 3. Load the skill in a Hermes session and launch the debate
skill_view(name='conclave')
```

---

## Arena Directory Structure

Each debate auto-generates an isolated folder under `~/.hermes/debates/`:

```
conclave-20260813-medlibya/
├── 00_preflight/          # Pre-flight ping results
├── 01_brief/              # Brief + anonymous mapping + user constraints
├── 02_r1/                 # R1 positioning (5 agents' raw outputs)
├── 03_r2/                 # R2 rebuttals
├── 04_r3~06_r5/           # Convergence rounds (created on demand)
├── 07_verdicts/           # Chair synthesis per round
├── 08_signoff/            # Final draft + individual sign-offs
├── 09_deliver/            # Final report + meeting minutes (deliverables)
└── index.md               # Full index: timeline, file map, key decisions
```

---

## Workflow

```
R1 Positioning   → 5 agents in parallel, unseen, written to 02_r1/
R2 Rebuttal      → Anonymous cross-examination + alternatives, written to 03_r2/
R3–R5 Convergence → Chair synthesizes divergence points into 07_verdicts/; sent back
Sign-off         → Final draft circulated; objections must carry alternatives
Delivery         → final.md + minutes.md land in 09_deliver/
```

---

## Key Disciplines

- **Constructive Opposition**: Any objection must answer "What do you think is the correct approach?" Destruction without construction = invalid.
- **Retry on Failure**: Any agent call failure → immediate identical retry; 2 consecutive failures → mark absent, debate continues.
- **Chair Neutrality**: Chair does not weight its own views; user override is the supreme arbiter.

---

## Deliverables

| File | Path | Description |
|------|------|-------------|
| **Final Report** | `09_deliver/final.md` | Decision doc: executive summary + consensus list + divergence rulings + minority opinions |
| **Meeting Minutes** | `09_deliver/minutes.md` | Process doc: round-by-round evolution, kill list, agent contributions, file index |
| **Arena Index** | `index.md` | Timeline + file map + key-decision quick-reference |

---

## Lessons from the Field

- **R1 Alignment = High-Confidence Signal**: When all five independently pick the same direction, it graduates directly to consensus without further debate.
- **Audit-Agent Value Density**: The most rigorous agent's (e.g., Claude) objections should directly rewrite final numbers, not just serve as QC.
- **Cost Expectation**: A full Conclave session (~30–50 CLI calls, 1.5–3 wall-clock hours). Use Codex medium/low effort for speed; parallelize all agents via `terminal(background=true)`.

---

## Installation

Install via the Hermes skills hub or clone from the source repository. Then run `bash ~/.hermes/skills/conclave/scripts/install.sh` to set up the four panelist CLIs and their dependencies — it auto-detects macOS, Linux, WSL, and Windows (Git Bash/MSYS2) and tells you exactly which provider keys to configure.

---

## License

MIT