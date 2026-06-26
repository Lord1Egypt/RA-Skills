# Skill Builder — Meta-Skill for Creating Skills

## Metadata

```yaml
---
name: skill-builder
version: 1.0.0
description: |
  Helps create high-quality OpenClaw skills following Anthropic's best practices.
  Use when creating, updating, or auditing any skill in the workspace.
---

---

## When to Use This Skill

Trigger phrases:
- "create a new skill"
- "build a skill"
- "make a new capability"
- "add a skill for"
- "audit our skills"
- "improve this skill"
- "review our skill setup"

---

## The Skill Creation Workflow

### Phase 1: Use Case Definition (Before Writing Code)

Before creating any skill, define 2-3 concrete use cases:

For each use case, specify:
1. **Trigger** — What the user says that should activate this skill
2. **Sequence** — Step-by-step actions the skill performs
3. **Expected Result** — What the user gets at the end

**Example Use Case Template:**
```
Use Case #1: [Title]
- Trigger: "[specific phrase user would say]"
- Sequence: [step 1] → [step 2] → [step 3]
- Result: [what gets produced]
```

### Phase 2: Skill Structure

Every skill must have:

```
skill-name/
├── SKILL.md           # Required: Main instructions
├── references/        # Optional: Additional docs
├── scripts/           # Optional: Executable code
├── assets/            # Optional: Templates, configs
└── tests/            # Optional: Test cases
```

### Phase 3: SKILL.md Anatomy

```yaml
---
name: skill-name
description: |
  [What it does]. Use when user mentions [trigger phrases].
  Example triggers: "do X", "help with Y", "use [skill-name]"
---
```

**Critical: The description field is the most important part.**
- Must include WHAT the skill does
- Must include WHEN to use it
- Must include specific trigger phrases
- Bad: "Helps with projects" (never triggers)
- Good: "Manages project workflows including creation, tracking, and updates. Use when user mentions 'project', 'create task', or 'track progress'"

### Phase 4: Writing the Instructions

Structure SKILL.md as:

1. **Identity** — Name, role, primary function
2. **Responsibilities** — What it must handle
3. **Boundaries** — What it must NOT do
4. **Tool Access** — What tools/functions it can use
5. **Workflow** — How it handles tasks
6. **Examples** — 2-3 concrete usage examples

### Phase 5: Testing

Test each skill on three dimensions:

| Test Type | Purpose |
|-----------|---------|
| Triggering | Skill loads for relevant queries, NOT for unrelated ones |
| Functional | Skill produces correct outputs |
| Performance | Measures improvement over baseline |

---

## Quality Checklist

Before finalizing any skill, verify:

- [ ] Description includes "Use when..." clause
- [ ] At least 3 trigger phrases listed
- [ ] Clear responsibilities section
- [ ] Boundaries defined (what NOT to do)
- [ ] Tool permissions explicitly stated
- [ ] Workflow documented with examples
- [ ] Triggering test passed
- [ ] Functional test passed
- [ ] No overgeneralization (skill won't trigger on unrelated queries)

---

## Common Failure Modes

| Failure | Cause | Fix |
|---------|-------|-----|
| Skill never triggers | Vague description | Add specific trigger phrases |
| Skill triggers too often | Overly broad description | Narrow the use case definition |
| Skill produces bad output | Missing boundaries | Add explicit "never do X" rules |
| Skill conflicts with others | No scope definition | Add explicit scope/limits |

---

## OpenClaw-Specific Notes

When building OpenClaw skills:
- Use the existing skill format (`SKILL.md` in skill folder)
- Reference OpenClaw tools by their exact names
- Follow the workspace memory paths exactly
- Respect the agent delegation rules in AGENTS.md
- Include security considerations for sensitive operations

---

## Example: Well-Formed Skill Description

```yaml
---
name: github-pr-review
description: |
  Reviews GitHub pull requests for code quality, security, and style consistency.
  Use when user mentions "review PR", "check pull request", "look at PR #N",
  "GitHub review", or "needs review".
  Does NOT: approve merges, write code, or modify existing PRs.
---
```

---

## Audit Existing Skills

When auditing skills, check:
1. Description has clear triggers
2. Boundaries are explicit
3. No conflicting scopes
4. Tools are properly scoped
5. Instructions are actionable

If a skill fails audit, update its SKILL.md following this workflow.
