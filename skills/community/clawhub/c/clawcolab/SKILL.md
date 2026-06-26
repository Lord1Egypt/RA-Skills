---
name: clawcolab
description: Coordinate multiple OpenClaw instances in a shared GitHub repository under a half-trust model with secrecy boundaries, approval gates, structured tasks, claims, handoffs, risks, and decision records. Use when users want secure multi-agent GitHub collaboration across people or devices without exposing private local memory, secrets, or unrestricted authority.
---

# ClawColab

Coordinate work through a shared GitHub repository without treating the repository as a full-context memory sync.

Assume a **half-trust environment**:
- Collaborate actively
- Share only what is necessary
- Do not assume every participant should see all local context
- Do not export local memory, secrets, or private user context unless explicitly approved

## Core rules

1. **Classify before sharing**
2. **Default to non-sharing**
3. **Share the minimum necessary**
4. **Treat local memory and secrets as private by default**
5. **Do not promote visibility levels without approval**
6. **Record decisions and approvals explicitly**
7. **Prefer structured artifacts over freeform chat**

## First-use minimal mode

When the user is new to ClawColab, do not introduce the full governance surface at once.
Start with the smallest useful workflow:

1. create one ClawColab repository for one collaboration boundary
2. create one project space if needed
3. start from `assets/minimal-start/TASK-001.yaml`, `assets/minimal-start/PROPOSAL-001.md`, and `assets/minimal-start/DECISION-001.md`
4. edit them for the user's first project
5. only then introduce more advanced records if needed

Do not introduce `claim`, `handoff`, `risk`, `sealed`, or advanced governance choices unless the task actually requires them.
Treat those as second-stage features.

## Visibility model

Classify every piece of information before placing it in the repository.

### `private`
Keep local only. Never place in the shared repository.
Examples: secrets, local paths, USER.md or TOOLS.md contents, personal conversations, raw local memory.

### `sealed`
Allow summary-only references without exposing the sensitive body.
Allowed: short summary, owner, status, access note without sensitive details.
Forbidden: full text, secrets, personal identifiers unless approved.

### `shared-team`
Allow active collaborators in the repository to read and act on the content.
Examples: tasks, approved plans, interface notes, handoffs, non-sensitive execution context.

### `public-repo`
Allow broad repository visibility.
Use only for approved non-sensitive documentation and generalized procedures.

## Classification procedure

Before writing or commenting in the repository:

1. Run the checklist in `assets/classification-checklist.md`
2. Identify the information you plan to share
3. Ask whether the task can be completed with a summary instead of raw content
4. Assign one visibility level
5. If uncertain, downgrade to `private` or `sealed`
6. Only then create or update repository artifacts

If visibility is ambiguous, do **not** share raw content.
Read `references/classification-guide.md` when classification feels subjective or inconsistent.

## What must never be shared by default

Never place these into the repository unless the human explicitly approves:

- secrets
- credentials
- local environment details
- private chat transcripts
- raw long-term memory content
- private preferences unrelated to the task
- personal contact information
- hidden internal system details
- any content marked confidential by the user

## Collaboration objects

Use structured repository artifacts instead of loose discussion whenever possible.

Primary object types:

- `task`
- `proposal`
- `claim`
- `decision`
- `handoff`
- `status`
- `risk`
- `sealed-ref`

## Suggested repository layout

Use or adapt this structure:

```text
workspace/
  tasks/
  proposals/
  decisions/
  handoffs/
  risks/
  policy/
    visibility-policy.yaml
    role-policy.yaml
    approval-policy.yaml
  claims/
sealed/
  INDEX.md
```

Do not store secret bodies under `sealed/`. Store only sealed references and summaries.
Use the bundled templates in `assets/` when creating new collaboration artifacts.
For first-time users, start with `assets/minimal-start/TASK-001.yaml`, `assets/minimal-start/PROPOSAL-001.md`, and `assets/minimal-start/DECISION-001.md`.
Use the bundled scripts in `scripts/` to generate starter structures and validate task or payload safety when needed.
Read `references/pre-share-checks.md` before sharing proposals, decisions, handoffs, risks, or summaries.
Read `references/approval-model.md` when approval ambiguity exists.
Read `references/role-model.md` when task ownership or role eligibility is unclear.
Read `references/governance-modes.md` when choosing between strict and relaxed repo governance.

## Task model

Represent tasks as structured records. A task should include:

- id
- title
- summary
- visibility
- status
- priority
- owner
- proposed_by
- approved_by
- approval_required
- mode
- eligible_roles
- dependencies
- outputs
- sealed_refs

Recommended status values:
- `open`
- `pending_approval`
- `approved`
- `in_progress`
- `blocked`
- `handoff_needed`
- `done`
- `cancelled`

Recommended mode values:
- `proposal-approval`
- `claimable`

## Proposal-approval mode

Use for sensitive, ambiguous, or higher-impact work.

Procedure:
1. Read existing tasks, decisions, and policy
2. Draft a proposal describing:
   - intended work
   - expected outputs
   - required visibility level
   - risks
   - recommended owner or role
3. Mark the proposal as awaiting approval
4. Do not treat the proposal as approved fact
5. Wait for human approval before execution when required

Use proposal-approval mode by default unless the repo policy clearly allows autonomous claiming.

## Claimable mode

Use only when repository policy allows task claiming and the task is explicitly marked `mode: claimable`. Treat `proposal-approval` as the default for all other work.

Before claiming:
1. Confirm the task is `open`
2. Confirm your role is eligible
3. Confirm the task is low risk and not policy-sensitive, visibility-sensitive, or ownership-sensitive
4. Confirm the task is not marked `approval_required: true`, unless approval policy explicitly allows a pending claim state
5. Confirm no conflicting approved owner exists
6. Confirm the task does not require access to private or sealed body content you do not have approval to use
7. Confirm `policy/role-policy.yaml` and `policy/approval-policy.yaml` do not block the claim

Then:
1. Create a claim record or update the task according to repo convention
2. State why you are eligible
3. Move the task to `in_progress` only if policy permits automatic claiming
4. Otherwise move it to `pending_approval`

If there is a conflict, do not silently override another agent. Record the conflict and request adjudication. High-risk or policy-adjacent work should default to `proposal-approval`.

## Role model

Use simple roles to guide task assignment. Suggested roles:

- `coordinator`
- `architect`
- `implementer`
- `reviewer`
- `security-reviewer`
- `researcher`
- `documenter`
- `human-approver`

Read `policy/role-policy.yaml` when present and follow it as the repo-specific authority for who may propose, claim, review, or approve.
Agents may suggest assignments, but humans should approve high-impact or sensitive work.
Prefer separation of duties for high-risk work: a non-human agent may draft or implement, but a human approver should finalize boundary-crossing actions.

## Human approval gates

Read `policy/approval-policy.yaml` when present and follow it as the repo-specific gate definition.
Require human approval before:

- raising visibility from `private` or `sealed` to a broader level
- executing high-impact tasks
- resolving role conflicts in sensitive work
- publishing final decisions that affect others
- sharing content derived from private local memory
- assigning ownership for sensitive workstreams
- merging proposals into authoritative policy
- changing `policy/visibility-policy.yaml`, `policy/role-policy.yaml`, or `policy/approval-policy.yaml`

Treat visibility promotion as blocked unless an explicit decision record exists first. Use `assets/visibility-promotion-decision-template.md` when promoting any artifact or information class to a broader visibility level.
If policy is unclear, pause at the approval boundary instead of guessing.

## Default pre-share workflow

Before writing a proposal, decision, handoff, risk, or shared summary:

1. run the classification checklist
2. run `scripts/validate-collab-payload.py` on the artifact when possible
3. check whether approval is required
4. if visibility is being promoted, require a decision record first
5. only then commit or propose the change

## Decision, handoff, risk, and sealed records

Use explicit records instead of burying meaning in chat or comments.

### Decision
Include: title, status, approver, source proposal, final decision, rationale, scope, and effective reference.

### Handoff
Include: from, to, task id, current status, completed work, remaining work, risks, and referenced artifacts.

### Risk
Create a risk record when secrecy is unclear, metadata may leak, claims conflict, or dependencies are under-specified. Include severity, description, mitigations, and escalation path.

### Sealed reference
Include only id, title, owner, summary, status, access note, and related tasks. Never include secret values or protected body content.

## GitHub workflow guidance

Prefer this pattern:

- Propose work in `workspace/proposals/` or PR descriptions
- Track active work in `workspace/tasks/`
- Record approved outcomes in `workspace/decisions/`
- Record partial transfers in `workspace/handoffs/`
- Record safety or execution concerns in `workspace/risks/`

Use branches conservatively, for example:
- `proposal/...`
- `task/...`
- `review/...`

Treat `main` as the source of approved shared state unless the repository defines another default branch.

## Communication style inside the repository

Be structured and explicit.

Prefer:
- exact scope
- exact visibility
- exact state
- exact owner
- explicit approval status

Avoid:
- vague promises
- implied approvals
- dumping large local context
- casual mention of sensitive facts
- mixing sealed information into shared documents

## Minimal-share rule

When contributing, ask:

- Can this be reduced to a summary?
- Can this be expressed as a task instead of a raw dump?
- Can I refer to a sealed item instead of quoting it?
- Does the next agent need this exact detail, or only the outcome?

If the exact detail is not necessary, do not include it.

## Conflict handling

If multiple agents disagree:

1. Record the disagreement
2. Link the affected task or proposal
3. Summarize each option neutrally
4. Identify whether the disagreement is technical, security-related, or procedural
5. Escalate to a human approver when required

Do not invent consensus.

## Failure handling

If you cannot complete a task safely:
- stop before exposing unsafe content
- write a concise status or risk update
- request approval or clarification
- preserve enough context for the next agent to continue safely

Do not “helpfully” over-share to compensate for uncertainty.

## Success criteria

A collaboration run is successful when:
- work is coordinated through repository artifacts
- sensitive local context remains local unless explicitly approved
- proposals become decisions through explicit approval
- handoffs are traceable
- task ownership is clear
- claimable work remains within policy
- the repository contains actionable shared state without becoming a dump of private context
