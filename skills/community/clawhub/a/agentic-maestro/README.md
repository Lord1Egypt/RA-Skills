# agentic-maestro

Orchestrated delegation for coding agents. A strong model conducts: it plans, writes exact rulings,
arbitrates review findings and merges. Cheaper sub-agents execute precise briefs. An independent
reviewer checks every result. Works with Claude Code, Codex and OpenCode, and any host that reads
Agent Skills.

## What is inside

| Path | Purpose |
|---|---|
| `SKILL.md` | The playbook: when to spawn a sub-agent at all, how to write a brief, how to run build -> review -> fix -> merge |
| `references/harnesses.md` | How to spawn on each agent: Claude Code (Agent tool or `claude -p`), Codex (`codex exec`), OpenCode (`opencode run`) |
| `references/checklist.md` | A pre-review checklist and how a project grows its own from recurring review findings |
| `references/operations.md` | Running several executors at once: lanes, git, reviewer prompts, context hygiene, cost ledger |
| `templates/` | Build, fix and integration brief templates, the shared rules block, a Claude Code sub-agent definition, an example brief spec |
| `scripts/brief.mjs` | Assembles a brief from a JSON spec; refuses any missing value, excerpt or convention |
| `scripts/spawn.mjs` | Runs one headless agent (`claude`, `codex` or `opencode`) on a brief and records session id, exit code, tokens and cost |
| `scripts/scope-check.sh` | Lists files an executor changed outside its brief's map, before you spend a review |
| `scripts/codemap.mjs` | Generates `docs/CODEMAP.md` so executors navigate without exploring |
| `scripts/excerpt.sh`, `scripts/conv.sh` | Quote a pattern excerpt and the matching project conventions into a brief |
| `scripts/gate.sh`, `scripts/gate_lock.py` | A machine-wide lock so parallel executors never run more than N heavy checks at once |

## Requirements

- Node.js 18+ and bash for the scripts (`python3` for the lock on macOS).
- At least one agent CLI: Claude Code, Codex or OpenCode.

## Safety notes

- The scripts never read secrets, make network calls of their own, or install anything. `spawn.mjs`
  starts the agent CLI you choose, in the working directory you pass, with your existing login.
- Write-mode executors run with auto-approved edits inside their working directory: give each one a
  disposable git worktree. Read-only mode (reviews, scouts) cannot edit files.
- Every brief tells executors never to read secrets or credential files and to report anything the
  brief does not decide instead of guessing.

## Source

Open source (MIT): https://github.com/Akramovic1/agentic-maestro
