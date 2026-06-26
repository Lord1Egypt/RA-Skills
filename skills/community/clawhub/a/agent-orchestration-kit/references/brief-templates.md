# Brief Templates

_Standard templates for dispatching tasks to agents. Leader reads this before composing briefs._

---

## Universal Structure (All Agents)

### Required Fields (every brief must have)

```markdown
**Task ID:** T-{YYYYMMDD}-{HHMM}
**Callback to:** {Leader's current session key — agent MUST callback to this session when done}

**Task:** [one-line description]

**Acceptance Criteria:**
- [ ] [verifiable condition 1]
- [ ] [verifiable condition 2]
- [ ] ...

**Execution Boundary:**
- Deliver: [what to report back]
- DO NOT: [specific actions that require Leader confirmation]
```

### Optional Fields (include when relevant)

```markdown
**Context:**
- Spec: [file path or link]
- Prior output: [file path from previous agent]
- Related files: [shared/ paths, reference docs, etc.]

**Dependencies:**
- Requires output from: [agent name] — [what output]
- Input files: [paths]

**Priority:** normal | urgent | low
- urgent: owner is actively waiting, prioritize speed
- normal: standard turnaround
- low: no rush, quality over speed

**Deadline:** [expected completion time or "no deadline"]

**Reference:**
- Spec doc: [path]
- Reference files: [paths]
- Prior conversation context: [summary]
```

---

## Owner-Facing Templates (Leader → Owner)

_These are owner-visible workflow messages. They are not agent briefs._

### Kickoff / Status Message Template

_This is the status message sent to the notification channel and edited in-place on every callback._

```markdown
📋 {task name}
ID: T-{id}

1. ⏳ {Agent} → {step description}
2. — {Agent} → {step description} (after: 1)
3. — Leader → {step description} (after: 2)

⏳ In progress: Step 1
```

**Icons:** ⏳ = in progress · ✅ = done · — = waiting · ❌ = failed · 🔍 = under review

**Rules:**
1. Send immediately after dispatch → record returned messageId as `notification_status_msg` in task file.
2. On every callback → edit this message (update icon + bottom status line).
3. On completion → send a separate Result Delivery message (see below).

### Progress Template

```markdown
Progress update: {task summary}

- Completed: {completed step/result}
- Currently working: {active step}
- Dependency status: {if relevant}
- Waiting on: {agent/blocker/decision if any}
- Next update: {when}
```

### Result Delivery Template

```markdown
✅ Task complete

Task ID: {id}
Result summary:
- {what was done}
- {key output / file / commit / path}
- {important status: pending approval / local only / not pushed / etc.}

My assessment:
{quality / recommendation / caveat}

Decision needed:
{approval / revision / next step}
```

### Blocked / Needs-Info Template

```markdown
This task is blocked: {reason}

I need you to provide:
1. {item}
2. {item}

Once I have this, I'll continue without restarting.
```

---

## Agent-Specific Templates

### Executor

```markdown
**Task:** [description]

**Context:**
- Files to modify: [paths]
- Reference: [spec, config, or instruction]

**Acceptance Criteria:**
- [ ] [specific verifiable outcome]
- [ ] [file state after completion]

**Output:**
- Report: what was changed/created
- File paths of modified/created files

**Execution Boundary:**
- Deliver: results + file paths
- DO NOT: push to git, deploy, restart services — unless explicitly instructed
- DO NOT: expand scope beyond what's listed
```

### Reviewer (on-demand, spawned)

```markdown
**Review Task:** [what to review]

**Deliverable:**
- [Path to content/code being reviewed]
- [Original brief — attached or path]

**Review Standards:**
- Brief compliance — does output meet acceptance criteria?
- [Technical correctness / quality / factual accuracy — as applicable]

**Prior Context:**
- Revision round: [1st / 2nd / rework after feedback]
- Previous feedback: [summary if applicable]

**Output:**
- [APPROVE] or [REVISE]
- Specific, actionable feedback (shorter than the deliverable)
- Max 2 review rounds
```

---

## Rework Brief (Revision Request)

_Use this template when sending rework/revision requests to agents after quality review._

```markdown
**Task ID:** T-{YYYYMMDD}-{HHMM}
**Callback to:** {Leader's current session key}
**Round:** {1/2 or 2/2}

**[REVISION REQUEST]**

**What was delivered:** {one-line summary of agent's output}

**Issues found:**
1. {specific issue with concrete example}
2. {specific issue with concrete example}

**Expected fix:**
- [ ] {verifiable correction 1}
- [ ] {verifiable correction 2}

**Context:** {any additional info — original brief reference, updated requirements, reviewer feedback}
```

---

## Callback Payload Contract (All Agents)

Callbacks sent via `sessions_send` must include:

- `task_id` (canonical: `[TASK_CALLBACK:T-{id}]`)
- `agent`
- `signal`
- `output`
- `files` (optional)

If a callback is malformed (missing required fields), Leader should request a resend.

---

## Execution Boundary — Common Defaults

| Agent | Common boundaries |
|-------|------------------|
| Executor | No git push, no deploy, no service restart, no scope expansion |
| Reviewer | Read-only, no modifications |
| _(Specialists)_ | _(Define per agent: deliver only, no publish, no deploy, etc.)_ |

These are defaults. Each brief may override based on task context (e.g., owner pre-approved a push → brief can say "push allowed after tests pass").
