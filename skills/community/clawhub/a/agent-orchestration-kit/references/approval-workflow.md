# Approval Workflow

How deliverables move from draft to executed. This applies to any output that has external impact.

---

## Pipeline Stages

```
Agent delivers [READY] → Leader reviews → [PENDING APPROVAL] → [APPROVED] → [EXECUTED]
                                                  ↓                  ↓
                                              [REVISION]         [REJECTED]
```

These are **task file states**, not callback signals. Agents use `[READY]` signal in their callback; Leader manages the pipeline states in the task file.

### 1. Agent Delivery
- Agent completes work and callbacks with `[READY]` signal
- Leader reviews the output (quality gate)

### 2. PENDING APPROVAL
- Leader presents output to owner with `[PENDING APPROVAL]` tag
- Output includes: deliverable, summary, context, recommended action
- Owner must explicitly respond

### 3. Owner Response Options
- **"approve"** or **"looks good"** → Task status moves to `APPROVED`
- **"revise [feedback]"** → Task status moves to `REVISION`, Leader sends revision request to agent
- **"reject"** or **"skip this"** → Task status moves to `REJECTED`, output is discarded

Note: These are **task file status values**, not callback signals. Agents never use these strings — Leader manages them in the task file.

### 4. APPROVED
- Output is confirmed and ready for execution
- Leader or agent executes the approved action

### 5. EXECUTED
- Action has been carried out (published, deployed, pushed, sent, etc.)
- Log the execution in task file

## Rules

1. **No external action without explicit owner approval.** This is the core rule.
2. Agents must tag all external-facing output with `[PENDING APPROVAL]`.
3. Approval is per-item — bulk approval is allowed when owner says "approve all".
4. Stale approvals (>48h without response) should be flagged by Leader.
5. Maximum 2 revision attempts (original + 1 revision). If the revision is also rejected, escalate to Leader for discussion with owner.
6. **Multi-agent rework**: When output goes through review + rework loops across multiple agents, the final output still requires explicit owner approval. Rework between agents does not bypass this workflow.

## Approval Shortcuts

The owner can use these shortcuts in conversation:
- `approve` / `lgtm` / `ship it` — approve the most recent pending item
- `approve all` — approve all pending items
- `revise: [feedback]` — request changes with specific feedback
- `reject` / `kill it` / `nah` — reject the most recent pending item
- `show queue` — list all pending approval items

## Reviewer Integration

- **Leader-initiated**: Leader invokes Reviewer at its discretion (high-stakes, complex, rework failures)
- **Owner-requested**: Owner explicitly asks for a review — Leader must invoke Reviewer
- Reviewer provides `[APPROVE]` or `[REVISE]`
- Leader evaluates Reviewer feedback as a peer, not as a directive
- Leader may override Reviewer (must document reason)
- Maximum 2 review rounds per task
- After review, Leader includes a brief review summary (what was flagged, action taken, verdict)
