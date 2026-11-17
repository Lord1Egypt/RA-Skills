# Frameworks — Choosing One, Or None

Framework capabilities and version numbers move fast; the selection criteria below do not. Verify current feature claims against the project's docs before committing, and prefer a small proof against your hardest case over a comparison table.

**Before recommending a framework**, read `## Stack` in `~/Clawic/data/agents/memory.md` and `framework` in `config.yaml`. Recommending a migration to a team that already ships on something else needs the cost of that migration in the same sentence.

## Decide By What You Will Need In Six Months

Ranked by how expensive it is to add later:

| Need | Add later cost | Frameworks help |
|---|---|---|
| Durable execution — a task survives a process restart and resumes | Very high: it re-shapes the whole loop | Strongly |
| Human-in-the-loop pause and resume mid-task | High: needs externalized state | Strongly |
| Explicit graph control flow with per-node retries | High | Strongly |
| Tracing and eval integration | Medium: instrument the loop yourself | Somewhat |
| Streaming with tool calls | Medium | Somewhat |
| Provider portability | Medium | Somewhat |
| A tool-calling loop with retries and caps | Low: it is the 30 lines in `implementation.md` | Barely |
| Prompt templating | Low | No |

If only the bottom rows apply, the raw provider SDK plus your own loop wins on debuggability and on the number of layers between a bug and its cause.

## The Categories

| Category | What it is | Pick when | The cost |
|---|---|---|---|
| **Raw SDK** | Provider client, your loop | Single loop, ≤10 tools, one team owns it | You write retries, tracing, state, resumption |
| **Graph / state-machine** | Nodes, edges, checkpointed state | Branching workflows, pause for a human, resume after a crash | A real learning curve; your control flow must fit the graph model |
| **Role-orchestration** | Agents-as-roles with delegation built in | Prototyping a multi-role idea quickly | Encourages the split that SKILL.md Rule 1 warns about |
| **Managed / hosted agent runtime** | The provider hosts loop, state and tools | Fastest path to something running, no infrastructure | Portability, cost visibility, and behavior you cannot fully inspect |
| **Durable-execution engine** | A general workflow engine with model calls inside steps | Long-running processes, hours to days, strict exactly-once needs | Not agent-shaped out of the box; you build the loop on top |

## Evaluate Against Your Hardest Case, Not A Demo

Before adopting, build one thing in it: the ugliest real task, with a tool that fails, a human approval, and a resume after a kill -9. Then answer:

- Can you read the actual prompt and tool schemas the framework sends? If not, you have lost the main debugging surface.
- Can you set all three caps — turns, deadline, money — and get the end reason back (SKILL.md Rule 2)?
- Does a killed process resume, or restart?
- Is state inspectable as data you could dump, or is it inside the framework?
- Can you swap the model without changing agent code, and does a swap re-run your evals automatically (`evaluation.md`)?
- What is the version cadence, and what broke in the last two minor releases? Fast-moving frameworks pin their breakage to your release schedule.

## Migration Cost, Honestly

- **Portable**: prompts, tool implementations, eval sets, traces you own. Usually the majority of the real work.
- **Rewritten**: the loop, state handling, memory wiring, human-in-the-loop plumbing, streaming.
- **Lost**: framework-specific graph definitions, checkpoints in the old format, any behavior that depended on the framework's defaults.
- Keep the boundary explicit from day one: business logic in your own tool functions, prompts in files, evals framework-independent. That discipline turns a rewrite into a re-wiring.

## Framework-Agnostic Rules That Survive Any Choice

- Prompts live in files with version tags, never buried in code (`prompts.md`).
- Tools are plain functions with typed inputs and outputs; the framework only registers them (`tools.md`).
- Evals call the agent through the same entry point production uses, or they measure a different system (`evaluation.md`).
- Traces record model snapshot, prompt version and end reason whatever the tracing backend is (`implementation.md`).
- All three caps exist even if the framework offers only one.
- Pin the framework version and put it in the release bundle (SKILL.md Rule 8) — a minor upgrade that changes a default prompt is a behavior change with no diff in your repository.

## When "No Framework" Is The Right Answer

- The task is one model call with tools resolved once. A loop is not needed, let alone a framework.
- The workflow is fixed: write the workflow, call the model at the steps that need judgment (`architecture.md`).
- The team is one person and the debugging budget is small. Every abstraction layer is a place a bug can hide from you.
- You are still learning the domain: build it raw first, feel which of the "add later cost" rows you actually hit, then adopt with evidence.

**When a framework is chosen or rejected**, write `~/Clawic/data/agents/artifacts/decision-framework.md` — the choice, the alternatives, the hardest-case test each one passed or failed, the version pinned, and what would justify revisiting — add its `## Boxes` line, and set `framework` in `config.yaml` plus the version in `## Stack`, all in the same turn (`memory-template.md`).
