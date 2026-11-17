# Execution Contract 2.1

`Docs/ACTIVE_PACKET.md` is the compact current authorization shared by governance and execution. Version 2.1 keeps `contract_version: "2.0"` so existing readers remain compatible.

## New Packet Frontmatter

```yaml
---
contract_version: "2.0"
packet_id: "GOAL-001"
goal_readiness: "Ready for Execution"
project_state: "Active"
execution_state: "Ready"
alignment_state: "Aligned"
stage_review: "Not Reviewed"
qa_required: true
qa_decision: "Not Reviewed"
size: "Medium"
governance: "Standard"
stage: 1
max_stages: 10
stage_minutes: 60
autonomy_mode: "Bounded"
acceptance_mode: "Layered"
delivery_class: "Runtime"
context_profile: "Compact"
write_scope: "."
outside_write_policy: "Deny"
authority_fingerprint: "sha256:..."
updated_at: "YYYY-MM-DDTHH:mm:ssZ"
---
```

Older 2.0 packets remain readable. Missing 2.1 policy fields use conservative defaults and produce one migration warning, not one warning per field.

## Required Sections

- Desired Outcome
- User And Situation
- Current Stage Outcome
- Scope
- Non-Goals
- Acceptance Criteria
- Allowed Changes
- Protected Boundaries
- Evidence Required
- Stop Conditions
- Authority Sources
- Assumptions And Decisions
- Current Evidence
- One Next Action

Keep a new packet at roughly 120 lines or fewer and exactly one immediate action. Use `{baseDir}/templates/en/ACTIVE_PACKET.md`.

## Ownership

| Field or content | Authority |
| --- | --- |
| Desired outcome, Core Target, Non-Goals | Owner or authorized Controller |
| Size, governance, delivery class, stages, Work Order | Controller |
| Implementation state and execution evidence | Developer |
| Stage review | Stage Reviewer |
| Alignment decision | Controller or designated alignment reviewer |
| Final QA decision | Independent QA for Standard and Full |
| Project acceptance state | Controller after valid QA decision |

One agent may change roles during bounded execution, but that does not create independent acceptance authority.

## Layered State Transitions

```text
Ready -> In Progress
In Progress -> Stage Reviewer Passed -> next authorized stage
In Progress -> Stage Reviewer Needs Fix -> Needs Fix -> In Progress
Terminal Standard/Full stage -> Ready for Independent Acceptance
Independent QA Failed -> Needs Fix on the same Packet and Work Order
Independent QA Accepted -> Accepted or Accepted With Risk
Any authority contradiction -> Invalid State
```

`Ready for Review` remains readable for older packets. New Standard and Full terminal deliveries use `Ready for Independent Acceptance`.

## Authority Fingerprint

List only current authority files under `Authority Sources`. Compute SHA-256 over each normalized project-relative path plus its bytes in listed order. Reuse TARGET, ACCEPTANCE, and Work Order context while the fingerprint is unchanged.

A changed fingerprint triggers formal alignment before further execution. A missing or contradictory authority source makes bootstrap read-only and requires one consolidated Owner decision.

## Claim Classes

- `Runtime`: executable behavior verified through the relevant user or operator flow.
- `Contract`: types, interfaces, schemas, or compatibility rules.
- `Governance`: policy, workflow, authority, or state-control material.
- `Artifact`: a document, package, report, fixture, or generated deliverable.
- `Mixed`: criteria span more than one class; label every criterion.

Passing a Contract, Governance, or Artifact criterion does not prove Runtime behavior.

## Write Rules

- Resolve the workspace, Docs directory, existing targets, and nearest existing parents to real paths.
- Reject any write that escapes the workspace through `..`, symlink, or junction resolution.
- Update the packet atomically where possible.
- Keep one current fact in one authoritative location.
- Link evidence instead of pasting long logs.
- Append compact records to `Docs/LOOP_RUNS.jsonl`.
- Never store credentials, private data, full transcripts, or hidden reasoning.
