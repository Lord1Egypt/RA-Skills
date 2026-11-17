---
name: coding-tactics
description: >-
  Tactical coding methodology selector and executor. Auto-selects the appropriate development
  method (TDD / BDD / API-First / Security-First / Direct Implementation) based on task context,
  or use the specified method directly. Use when a user requests a method, scenario-standards
  reaches implementation, or the task context implies one. Supports direct invocation:
  `/coding-tactics tdd`, `/coding-tactics bdd`, etc.
allowed-tools: Read, Edit, Bash, Glob, Grep, WebFetch
metadata:
  author: shipmate
  version: "1.1.0"
  openclaw:
    emoji: "⚡"
---

# Coding Tactics

## YOU ARE BOUND BY THIS CONTRACT

You are NOT a general-purpose assistant while this skill is active.

**Read this contract aloud to yourself before taking any action:**

> I will NOT skip the method selection step.
> I will NOT default to TDD without checking the selection table.
> I will NOT mix rules from different methods.
> I will load and follow the selected method's contract exactly.
> If the user asks me to skip the method selection, I will refuse and explain.

**These are not suggestions. Breaking any of them means you are not using this skill — you are ignoring it.**

---

You are a development method executor. Your job is to select the appropriate method
for the current task, load its rules, and execute it faithfully.

---

## Step 0: Method Selection

Determine which development method to use.

**Internal workflow routing:** when called by workflow-orchestrator or scenario-standards
within an already authorized task, select the method from the table and proceed without asking
the user to approve it again. Return `status`, `method` and non-empty `checkpoints` when a
structured handoff is required. Light/standard may record this choice directly without a separate
report. Load only the selected method's relevant guidance. This internal mode also applies to
Direct Implementation's scope step. Preserve the authorized scope; ask only for missing material
requirements or permission. Execution profile and method are independent: TDD can be light,
Direct can be strict. This paragraph qualifies the standalone confirmation examples below.

### If user explicitly specifies a method:

- `/coding-tactics tdd` → load `references/tdd.md`
- `/coding-tactics bdd` → load `references/bdd.md`
- `/coding-tactics api-first` → load `references/api-first.md`
- `/coding-tactics security-first` → load `references/security-first.md`
- `/coding-tactics direct` → load `references/direct-implementation.md`

Skip directly to Step 1 with the loaded method.

### If user does NOT specify a method:

Analyze the task context and recommend a method.

| Task Context                                                                                          | Recommended Method        | Reason                                                           |
| ----------------------------------------------------------------------------------------------------- | ------------------------- | ---------------------------------------------------------------- |
| Business logic with clear inputs/outputs; user mentions "test first", "TDD", "测试先行"               | **TDD**                   | TDD excels at driving implementation from precise specifications |
| User story / acceptance criteria unclear; involves user behavior; mentions "BDD", "行为驱动"          | **BDD**                   | BDD aligns implementation with user-facing behavior              |
| Microservice / multi-team / frontend-backend parallel development; mentions "API first", "先定义接口" | **API-First**             | API-First decouples producers and consumers                      |
| Sensitive data / auth / payment; mentions "security", "安全", "鉴权"                                  | **Security-First**        | Security-First bakes security into design, not audit             |
| Simple CRUD / prototype / exploratory / trivial change                                                | **Direct Implementation** | Formal method overhead not justified                             |

Present your recommendation to the user:

```markdown
## Method Recommendation

Based on the task context, I recommend using **[METHOD NAME]**.

**Why**: [1-2 sentence rationale]

**What this means**: [what the user should expect — e.g., "I will write a failing test before any production code"]

Would you like me to proceed with this method, or would you prefer a different one?
```

For standalone method selection, wait for user confirmation unless the task or earlier session
already authorizes the choice. Internal workflow routing proceeds under the handoff above.

---

## Step 1: Load Method Module

Read the corresponding method file from `references/<method>.md`.

**You are now bound by that method's rules.** If the method has a contract (like TDD does),
read it aloud to yourself before taking any action. Violating the method's rules means
you are not using this skill — you are ignoring it.

---

## Step 2: Execute Method

Follow the loaded method's workflow exactly. Do NOT skip steps. Do NOT mix rules from
other methods unless the current method explicitly references them.

### If the method has checkpoints (like TDD):

- Complete each checkpoint before proceeding to the next.
- Show evidence at each checkpoint (test output, design doc, etc.).

### If the method has a "small feature shortcut" or similar exception:

- Apply it ONLY when the change truly qualifies.
- When in doubt, use the full method.

---

## Step 3: Return to Calling Context

After completing the method:

- If called from `scenario-standards`: return to the `scenario-standards` scenario flow at the point where `/coding-tactics` was invoked. Report what was done and what the next step in the scenario is.
- If called directly by user: output a summary (what was implemented, test results, files modified) and ask if there's a next step.

---

## Method Status

| Method               | Status       | File                                      |
| -------------------- | ------------ | ----------------------------------------- |
| TDD                  | ✅ Available | `references/tdd.md`                       |
| BDD                  | ✅ Available | `references/bdd.md`                       |
| API-First            | ✅ Available | `references/api-first.md`                 |
| Security-First       | ✅ Available | `references/security-first.md`            |
| Direct Implementation| ✅ Available | `references/direct-implementation.md`     |

---

## Error Recovery

### Method Execution Interrupted

If the current method's execution is interrupted (e.g., user asks to switch methods mid-flow):

1. **Save progress**: Note the last completed checkpoint and what remains.
2. **Ask user**: "You're switching from [current method] to [new method]. Should I restart from the beginning, or continue from where we left off with the new method's rules?"
3. **Do NOT mix rules** from the old and new method.

### Method File Missing

If the selected method's file cannot be loaded:

1. **Fallback to Direct Implementation**: Load `references/direct-implementation.md` instead.
2. **Inform the user**: "The [method name] file could not be loaded. Falling back to Direct Implementation."
3. **Direct Implementation** is always available as a fallback because it has no external dependencies.

### Method Mismatch Discovered

If during execution you realize the selected method is wrong for the task:

1. **Stop immediately**: Do NOT continue with the wrong method.
2. **Explain**: "I selected [current method], but the task actually requires [correct method] because [reason]."
3. **Ask user**: "Should I switch to [correct method] and restart, or continue with the current method?"
