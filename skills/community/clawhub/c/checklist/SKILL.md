---
name: checklist
version: 1.2.1
description: Collaborative task checklist manager for AI agents with sequential, parallel, and looping execution. Features agent coordination, dependencies, deadlock prevention, and loop safety.
---

# Checklist 📋

**Collaborative task checklist manager for AI agents with advanced execution modes.**

---

## 🎯 When to Use

Use this skill when:
- **Multi-agent collaboration** - Multiple AI agents need to coordinate
- **Sequential tasks** - Steps must execute in order
- **Parallel tasks** - Steps can run simultaneously
- **Looping workflows** - Repeat until condition is met
- **Complex coordination** - Avoid deadlocks and infinite loops

---

## 🌐 Execution Modes

### 1. Sequential (串行)
Steps execute one after another:
```
A → B → C → D
```

### 2. Parallel (并行)
Steps execute simultaneously:
```
A
B ← Branch together
C
```

### 3. Loop (循环)
Repeat until exit condition:
```
while condition:
    A → B
    if exit_condition:
        break
```

---

## ⚡ Quick Commands

### Execution Control
```bash
# Set execution mode
checklist mode sequential   # 串行
checklist mode parallel    # 并行
checklist mode loop       # 循环

# Configure loop
checklist loop set 5                 # Set max 5 iterations
checklist loop condition "<expr>"   # Set exit condition
checklist loop count                 # Show current loop count

# Run checklist
checklist run                        # Execute with current mode
checklist run --dry-run             # Preview without executing

# Safety
checklist check                      # Check for deadlocks
checklist validate                   # Validate entire workflow
```

### Agent Commands
```bash
checklist agent register <name>
checklist agent use <name>
checklist assign <item> <agent>
checklist claim
checklist status
```

### Task Commands
```bash
checklist create <template>
checklist done <item>
checklist depend <item> <dep>
checklist tree
```

---

## 🔄 Execution Modes Detail

### Sequential Mode
```
✅ Sequential: Items execute in order
   1 → 2 → 3 → 4 → 5

✅ Item 3 can only start after Item 2 completes
```

### Parallel Mode
```
✅ Parallel: Items in same "group" run together
   Group 1: [1, 2] (parallel)
         ↓
   Group 2: [3, 4] (parallel)
         ↓
   Group 3: [5] (final)
```

### Loop Mode
```
✅ Loop: Repeat until exit condition

Loop Config:
  - Max iterations: 5 (default, configurable)
  - Exit conditions:
    - All items done
    - Custom condition met
    - Manual break

Loop Example:
  Iteration 1: [1, 2, 3] → Check exit → Continue
  Iteration 2: [1, 2, 3] → Check exit → Continue
  Iteration 3: [1, 2, 3] → Exit condition met → Stop
```

---

## 🛡️ Safety Features

### 1. Loop Protection
```bash
# Default: Max 5 iterations
checklist loop set 5

# After 5 loops, automatically exits
# Even if not all items complete
```

### 2. Exit Conditions
```bash
# Exit when specific item done
checklist loop condition "item.5.done == true"

# Exit when all required items done
checklist loop condition "all_required_done"

# Exit when iteration count reached
checklist loop condition "count >= 5"
```

### 3. Deadlock Prevention
```bash
# Check for potential deadlocks
checklist check

🔍 Deadlock Detection:
   - Circular dependencies: NONE
   - Unreachable items: NONE
   - Agent conflicts: NONE
   ✅ Workflow is safe to execute
```

### 4. Validation
```bash
# Validate entire workflow
checklist validate

🔍 Validation:
   - All items have valid references: ✅
   - No circular dependencies: ✅
   - Agents assigned: 3/15
   - Max loop iterations: 5
   - Exit condition: defined
   ✅ Checklist is valid
```

---

## 📋 Usage Examples

### Example 1: Sequential Deployment
```
User: Deploy app sequentially

AI: [Execute: checklist create deploy]
[Execute: checklist mode sequential]

✅ Mode: Sequential

Execution Order:
  ⏳ 1. Run tests
  ⏳ 2. Build
  ⏳ 3. Deploy to staging
  ⏳ 4. Verify
  ⏳ 5. Deploy to prod
```

### Example 2: Parallel Testing
```
User: Run tests in parallel

AI: [Execute: checklist create test-suite]
[Execute: checklist mode parallel]

✅ Mode: Parallel

Parallel Groups:
  Group 1 (concurrent):
    🔄 Unit tests
    🔄 Integration tests  
    🔄 Lint checks
    ↓ All complete →
  Group 2:
    ✅ Generate report
```

### Example 3: Loop with Exit
```
User: Poll API until successful, max 5 times

AI: [Execute: checklist create api-poll]
[Execute: checklist mode loop]
[Execute: checklist loop set 5]
[Execute: checklist loop condition "item.3.done == true"]

Loop Config:
  - Max iterations: 5
  - Exit: item #3 (API success)
  - Current: 0/5

Iteration 1:
  ⏳ 1. Send request
  ⏳ 2. Check response
  ⏳ 3. Verify success
  → Not done, continue...

Iteration 3:
  ⏳ 1. Send request
  ⏳ 2. Check response
  ✅ 3. Verify success ← Exit condition met!
  
🔄 Loop exited at iteration 3
✅ Exit condition satisfied
```

### Example 4: Deadlock Prevention
```
User: Create conflicting dependencies

AI: [Execute: checklist add "Task A"]
[Execute: checklist add "Task B"]
[Execute: checklist depend 1 2]
[Execute: checklist depend 2 1]

[Execute: checklist check]

🔍 Deadlock Detection:
   ⚠️  WARNING: Circular dependency detected!
   
   1 → 2 → 1
   
   Resolution suggestions:
   - Remove one dependency
   - Merge into single item
   
✅ Checklist NOT safe - fix before running
```

---

## 🔧 Implementation

### Loop State
```json
{
  "loop": {
    "enabled": true,
    "mode": "sequential|parallel|loop",
    "max_iterations": 5,
    "current_iteration": 0,
    "exit_condition": "item.3.done == true",
    "exit_reason": "condition_met|max_reached|manual"
  }
}
```

### Safety Checks
```
Before Execution:
1. Validate all references ✓
2. Check circular dependencies ✓
3. Verify agents available ✓
4. Check loop config ✓
5. Confirm exit condition ✓

During Execution:
- Monitor for infinite loops
- Track iteration count
- Check exit conditions

After Execution:
- Final validation
- Generate completion report
```

---

## 🎯 Best Practices

### 1. Always Set Exit Conditions
```bash
# Good
checklist loop condition "item.success.done == true"

# With timeout
checklist loop set 10
```

### 2. Use Sequential for Dependent Tasks
```bash
checklist mode sequential
checklist depend 2 1
checklist depend 3 2
```

### 3. Use Parallel for Independent Tasks
```bash
checklist mode parallel
# Items in same group run together
```

### 4. Check Before Running
```bash
checklist check   # Deadlock check
checklist validate   # Full validation
```

### 5. Monitor Loop Count
```bash
checklist loop count   # Show current iteration
```

---

## ⚠️ Important Notes

### Loop Safety

| Scenario | Behavior |
|----------|----------|
| No exit condition | Uses max_iterations (default: 5) |
| Exit condition never met | Stops at max_iterations |
| Deadlock detected | Blocks execution, shows warning |
| Circular dependency | Prevents running, suggests fix |

### Maximum Limits

| Limit | Default | Max |
|-------|---------|-----|
| Loop iterations | 5 | 100 |
| Parallel items | 10 | 50 |
| Total items | 100 | 500 |

---

## 🦞 Summary

**One line: Complex task → Choose mode (sequential/parallel/loop) → Set safety limits → Run with confidence → Automatic exit**

---
