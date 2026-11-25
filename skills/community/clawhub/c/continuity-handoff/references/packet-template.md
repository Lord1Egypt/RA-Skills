---
type: continuity-handoff
schema_version: "1.0"
work: "<portable human-readable identity>"
work_slug: "<stable-lowercase-slug>"
source_runtime: "OpenClaw"
source_agent: "<agent id or unknown>"
source_session: "<session key/id if exposed, otherwise unknown>"
source_gateway_device: "<gateway/device if known, otherwise unknown>"
target_runtime: "<OpenClaw, Codex, other, or undecided>"
transcript_inherited: false
implementation_started: false
---

# Mission

<One paragraph stating the outcome that must continue.>

# Current goal and checkpoint

- Active goal: <goal or explicitly none>.
- Last completed checkpoint: <strongest verified point>.
- Exact next action: <one bounded action>.
- Work state: <implemented, code-proven, test-proven, runtime-proven, or end-to-end-proven; specify evidence>.

# Project and runtime binding

- Project: <portable identity, not a machine path>.
- Repository: <owner/name or local-only>.
- Branch and commit: <observed values, or unknown>.
- Working tree: <clean/dirty and relevant files, or not inspected>.
- OpenClaw agent / source session: <only what the source runtime exposed>.
- Gateway / execution device: <observed, reported, or unknown>.
- Target workspace and identity: <how the target will find the work; or unresolved>.

# Accepted decisions

- <Decision and reason.>

# Proven results and evidence

- <Claim; proof level; exact file, command, test, issue, or timestamp.>
- <Link to compact source evidence. Do not paste complete logs or transcripts.>

# Failures and do-not-repeat

- <Attempt, observed failure, and invariant it establishes.>

# Dependencies and owners

- <Service/tool/access dependency; current owner; availability condition.>

# Protected state and authorization

- <Exact data, sessions, identities, accounts, jobs, or resources that must not be changed.>
- <Actions authorized, actions not authorized, and any approval still required.>

# Open questions and known gaps

- <Only decisions or proof gaps that can change the next action. Unknown is not false.>

# Evidence lineage

- Source runtime observation: <date/time and source session locator if available>.
- Target runtime counters: <separate; record only after target execution>.
- Omitted history: <what was not transferred or verified>.

# Required acknowledgement before implementation

The receiving agent replies with the mission and resume point, verified versus
unverified facts, the next read-only check, protected state and authorization,
and whether implementation has started. It then verifies current project state
before acting.
