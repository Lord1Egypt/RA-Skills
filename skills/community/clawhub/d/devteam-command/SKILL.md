---
name: devteam-command
description: Reusable Dev Team pipeline. Call anytime to spawn full pipeline: Planner → PM → Coder → Tester → Fixer → Reporter. Use for any coding task.
---

# DevTeam Command - Reusable Pipeline

## 🚀 Quick Start

### Call Anytime

```typescript
// Import skill
import { spawnDevTeam } from '@/skills/devteam-command'

// Spawn full pipeline
await spawnDevTeam('Your task description here')
```

### Or Use Command

```bash
# Full pipeline
/devteam "Fix UI rendering issue"

# Specific agent
/devteam planner "Analyze requirements"
/devteam coder "Implement feature"
/devteam tester "Write tests"
```

---

## 📋 Pipeline Steps

| Step | Agent | Time | Output |
|------|-------|------|--------|
| 1 | Planner | 10 min | PLAN.md |
| 2 | PM | 15 min | TASKS.md |
| 3 | Coder | 60 min | Code |
| 4 | Tester | 20 min | BUGS.md |
| 5 | Fixer | 30 min | Fixed Code |
| 6 | Reporter | 10 min | RELEASE.md |

**Total:** ~2.5 hours

---

## 🎯 Usage Examples

### Example 1: Bug Fix

```typescript
await spawnDevTeam(`
  Bug: Homepage không hiển thị comics
  
  Details:
  - API: 200 OK, 24 items
  - UI: Không render
  - Error: React #418
`)
```

### Example 2: New Feature

```typescript
await spawnDevTeam(`
  Add search functionality:
  - Search input component
  - API: GET /api/search?keyword=
  - Search results page
  - Debounce input
`)
```

### Example 3: Testing

```typescript
await spawnDevTeam(`
  Write E2E tests:
  - Test homepage loading
  - Test category navigation
  - Test comic detail
  - Target: All critical paths
`)
```

---

## 🔧 Configuration

### Models

```typescript
const MODELS = {
  planner: 'bailian/qwen3-coder-plus',
  pm: 'bailian/qwen3.5-plus',
  coder: 'bailian/qwen3-coder-plus',
  tester: 'bailian/qwen3.5-plus',
  fixer: 'bailian/qwen3-coder-plus',
  reporter: 'bailian/kimi-k2.5',
}
```

### Timeouts

```typescript
const TIMEOUTS = {
  planner: 600000,      // 10 minutes
  pm: 900000,           // 15 minutes
  coder: 3600000,       // 60 minutes
  tester: 1200000,      // 20 minutes
  fixer: 1800000,       // 30 minutes
  reporter: 600000,     // 10 minutes
}
```

---

## 📊 Output Files

After pipeline completes:

```
docs/
├── PLAN.md          # Requirements & plan
├── TASKS.md         # Detailed tasks
├── BUGS.md          # Bug reports (if any)
└── RELEASE.md       # Release notes
```

---

## 💡 Best Practices

### ✅ Do

- Clear, detailed task description
- Include acceptance criteria
- Provide context and links
- Wait for completion before next task

### ❌ Don't

- Vague descriptions
- Multiple unrelated tasks
- Skip testing phase
- Ignore bug reports

---

## 🔄 Reuse Anytime

**Skill is reusable!** Call anytime:

```typescript
// Task 1
await spawnDevTeam('Fix bug A')

// Task 2 (later)
await spawnDevTeam('Add feature B')

// Task 3 (anytime)
await spawnDevTeam('Write tests for C')
```

---

*Skill Version: 1.0.0*
*Created: 2026-03-06*
*Reusable: Yes*
