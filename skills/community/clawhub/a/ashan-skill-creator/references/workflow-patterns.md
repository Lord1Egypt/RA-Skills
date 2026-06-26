# Workflow Patterns Reference

Common patterns for structuring Skill content.

---

## Pattern 1: Sequential Workflow

Best for: Fixed-step, sequential processes.

```markdown
## Steps

### Step 1: Prepare
[What + how to verify]

### Step 2: Execute Core Operation
[Specific commands/API calls]

### Step 3: Validate Result
[How to confirm success/failure]
```

---

## Pattern 2: Task Branches

Best for: Single Skill supporting multiple operation types.

```markdown
## Supported Operations

### Type A: Export
[Steps]

### Type B: Import
[Steps]

### Type C: Query
[Steps]
```

---

## Pattern 3: Reference Navigation

Best for: Content too large for SKILL.md, must split into references/.

In SKILL.md:
```markdown
## Detailed References

- **API docs**: See `references/api.md`
- **Common errors**: See `references/errors.md`
- **Examples**: See `references/examples.md`
```

In references/api.md:
```markdown
# API Reference

## Authentication
[Details]

## Endpoint List
[Complete list]
```

---

## Pattern 4: Good/Bad Example Pairs

```markdown
## Examples

### ✅ Correct
User: "Export JZ March invoices"
Agent: [correct steps]
Output: [standards-compliant Excel]

### ❌ Wrong
User: "Export invoices"
Agent: [wrong operation]
Result: [wrong format / missing fields]
Why: Didn't confirm company + month first
```
