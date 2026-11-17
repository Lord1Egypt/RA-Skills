# Pairing — Live Collaboration on One Artifact

Pairing is synchronous collaboration where the exchange happens DURING production, not after. It trades throughput (two minds, one artifact) for error interception before errors are typed. Route here only when that trade wins.

## When Pairing Wins

- High ambiguity AND high undo cost: the spec would be wrong, and the rework expensive — review-after arrives too late, delegation ships the wrong thing confidently.
- Context transfer is a goal in itself (onboarding, bus-factor reduction): pairing transfers the WHY that review comments and docs strip out.
- Debugging with two live hypothesis streams: the navigator holds the hypothesis tree while the driver tests branches — neither role alone keeps both.

When it loses: mechanical work with writable acceptance criteria (delegate — pairing there is expensive supervision), and work needing deep solo focus where interruption costs more than errors. The routing checks in SKILL.md decide; pairing is a HOW of collaborating, not a reason to.

## Driver / Navigator

- **Driver** produces: types, executes, owns the next line.
- **Navigator** holds intent: watches for drift from the goal, tracks the plan, spots the wrong sub-problem being solved.
- The navigator speaks at intent level ("we're handling the error case before the happy path works"), never keystroke level ("missing semicolon") — keystroke backseat driving destroys the driver's flow and wastes the navigator's altitude. Exception: the driver asks.
- A silent navigator is not pairing; it is solo work with an audience. The navigator's output is a running commentary of intent-level observations — if there is nothing to say for long stretches, the work did not need pairing.

## Rotation

Swap roles at natural boundaries — a test passes, a section completes, a hypothesis dies. Never mid-thought on a timer: the swap's cost is context transfer, and mid-thought the context is at its largest. If one person has driven the whole session, the navigator has become a spectator — force the swap at the next boundary.

## Human–Agent Pairing

- **Agent drives, human navigates**: the human steers by objective and interrupts on direction ("wrong sub-problem"), not on syntax — syntax interruptions make the agent thrash between styles. The agent surfaces intent before each chunk ("next: X because Y") to give the human a hook to redirect early.
- **Human drives, agent navigates**: the agent restates the human's intent before each chunk and flags drift from the stated goal; it does not grab the wheel by rewriting unasked. Kill-class observation (data loss, security) → flag immediately; everything else waits for the boundary.
- Either way, the pairing contract is explicit up front: who decides on disagreement (default: the human), and what the agent may do without asking.

## Disagreement While Pairing

Park it. Note the disagreement in one line, finish the current step, resolve at the boundary — mid-flow debate destroys both roles at once (driver loses flow, navigator loses the map). At the boundary, it becomes a normal micro-exchange: positions, one question, decide, continue. If it deadlocks, the pairing contract's decision owner calls it and the objection goes to the record (`decision-log.md`).

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Two drivers | Both produce, nobody holds intent; drift goes unnoticed | Roles named out loud at session start |
| Keystroke navigation | Flow destroyed; navigator abandons the map for typos | Intent level only, unless asked |
| Pairing as surveillance | The navigator is auditing, not collaborating; driver performs instead of thinks | If the goal is verification, that is review — do it async |
| Never rotating | Navigator disengages into spectator | Swap at natural boundaries |
| Debating mid-flow | Both roles collapse simultaneously | Park in one line; resolve at the boundary |
