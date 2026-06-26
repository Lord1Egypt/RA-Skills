---
name: task-extractor
description: Extract, track, and verify completion of multiple tasks from a single user message. Use when a message contains 3+ actionable items or mixes multiple unrelated asks. Prevents the common failure mode where agents address 2 of 6 requests and silently drop the rest.
---

# Task Extractor

## When to Trigger
A user message contains 3+ actionable items, mixes asks across different domains, or has a history of dropped tasks.

## Process
1. **Extract** every task from the message — err on the side of capturing more.
2. **Number** each task explicitly.
3. **Track** in a hot index: `| # | Task | Status | Evidence |`
4. **Execute** each in order (or delegate to appropriate skill).
5. **Reconcile** after completion — compare extracted list against actual completions.

## Example
```
User: "Fix the deploy bug, update the landing page copy, 
       check if Stripe webhook is working, and email the client"

Extracted:
1. Fix deploy bug → coder
2. Update landing page copy → coder
3. Check Stripe webhook → verifier
4. Email client → GATE (needs approval)
```

## Rules
- Missing a task is worse than capturing an extra one.
- Mark each explicitly: ✅ done | 🔄 in progress | ❌ blocked | ⏭️ deferred.
- At end of run, list any DROPPED tasks — these are the most important to surface.
- If a task needs human approval, mark as GATE and don't execute silently.
