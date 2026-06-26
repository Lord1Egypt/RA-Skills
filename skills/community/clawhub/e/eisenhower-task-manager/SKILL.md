---
name: task-manager
description: Task management based on Eisenhower Matrix + P0-P2 priority with Customer Project Management. Four quadrants for execution, separate Customer Project List for all customer work.
repository: https://github.com/yayayahei/skills/tree/main/eisenhower-task-manager
---

# Task Manager - Four-Level System

**Repository:** [yayayahei/skills/eisenhower-task-manager](https://github.com/yayayahei/skills/tree/main/eisenhower-task-manager)

## Architecture

**Tasks Directory Configuration:**
By default, the skill operates in the `tasks/` directory relative to this SKILL.md. You can override this globally by setting the `EISENHOWER_TASKS_DIR` environment variable to an absolute path (e.g., `export EISENHOWER_TASKS_DIR=/Users/xxx/tasks`).

| Layer | File | Purpose |
|-------|------|---------|
| Customer | `tasks/customer-projects.md` | ALL customer projects (single source of truth) |
| Execution | `tasks/tasks.md` | Four quadrants (personal + customer tasks requiring YOUR execution) |
| Future | `tasks/maybe.md` | Ideas for later evaluation |
| Delegation | `tasks/delegation.md` | Tasks assigned to others |
| Archive | `tasks/archived.md` | Completed/deleted history |

## Core Principles

1. **Customer projects NEVER duplicate** - exist only in Customer Project List
2. **Personal execution only** - customer tasks enter quadrants only when YOU must execute
3. **Sequential numbering** - 1-N per file, no gaps, no duplicates
4. **Auto-fix numbering** - after EVERY operation, verify and fix sequence

## Four Quadrants

| Q | Name | Strategy | When |
|---|------|----------|------|
| Q1 | Important + Urgent | Execute immediately | Deadlines, blockers |
| Q2 | Important + Not Urgent | Plan & schedule | OKRs, strategic work |
| Q3 | Not Important + Urgent | Batch process | Maintenance, delegatable |
| Q4 | Not Important + Not Urgent | Postpone/delete | Exploration, optional |

## Priority Tiers (within quadrant)

- **P0**: Today (hard deadline or blocking)
- **P1**: This week
- **P2**: This month/quarter

## Customer Project Workflow

```
New Customer Project
    ↓
Add to Customer Project List (record all)
    ↓
Need YOUR execution?
    ├─ YES → Add to appropriate Quadrant, tag with [Customer/ProjectName]
    └─ NO → Keep in Customer Project List only
    ↓
Regular Review → Update status (Active/Blocked/Pending)
    ↓
Completed → Archive entry + complete quadrant task if exists
```

## Task Numbering Rules

### Quadrant Tasks (tasks.md)
- Q1: 1 to N
- Q2: (N+1) to M
- Q3: (M+1) to P
- Q4: (P+1) to Q
- Continuous sequence across quadrants, no gaps

### Maybe List (maybe.md)
- Sequential: 1, 2, 3... 
- **ALWAYS append to END** - never insert in middle
- Verify: last_number == total_count

### Customer Projects (customer-projects.md)
- Per-customer numbering: 1, 2, 3...
- Independent across customers

### Delegation List (delegation.md)
- Sequential: 1, 2, 3...
- **ALWAYS append to END**
- Verify: last_number == total_count
- Format: `### X. Task Name @assignee`

### Archive (archived.md)
- Sequential: 1, 2, 3...
- **ALWAYS append to END**
- Group by archive date
- Format: `### X. Task Name [Archived: YYYY-MM-DD]`

## Numbering Verification (MUST RUN AFTER EVERY OPERATION)

1. Read target file
2. Scan for: duplicates, gaps, wrong transitions
3. Reassign sequential numbers starting from 1
4. Re-read to verify
5. Repeat if issues remain

**Numbering Checklist:**
- [ ] Sequential from 1, no gaps
- [ ] No duplicates
- [ ] Q2 starts at Q1_count+1, Q3 at Q2_end+1, etc.

## Operations

### Add Task

See [references/task-add.md](references/task-add.md) for complete workflow.

**Quick Guide:**
0. **CRITICAL: ALWAYS use the Read tool to read the target file FIRST to get the latest state before modifying it.**
1. Determine level: Quadrants / Delegation / Maybe
2. Determine quadrant (if applicable): Q1/Q2/Q3/Q4
3. Assign priority: P0/P1/P2
4. Insert at appropriate position
5. Renumber ALL tasks (sequential from 1)
6. Update statistics
7. Display updated list
8. **(Optional)** Offer to open Dashboard for visual review

### Complete Task

See [references/task-complete.md](references/task-complete.md) for complete workflow.

**Key Points:**
- **MUST NOT stop at just marking [x]** - full flow required
- Delete completed task from source file
- Renumber remaining tasks
- Move to archived.md
- Update statistics
- Display updated list
- **(Optional)** Offer to open Dashboard to see updated status

**Three Scenarios:**
1. **Main Task List** (tasks.md) - Four Quadrant tasks
2. **Delegation List** (delegation.md) - Delegated tasks  
3. **Maybe List** (maybe.md) - Future tasks

### Post-Operation Dashboard Offer

After any task operation (add/complete/update), the skill SHOULD offer to open the dashboard:

```markdown
✅ Task Added Successfully

**Summary:**
- Task: [Task Name]
- Location: Q2 #15
- Priority: P1

📊 Would you like to view the task dashboard?
→ User approves: Launch dashboard and open browser
→ User declines: Continue with next operation
```

**Implementation:** Check if user wants to open dashboard after major operations.

### Add Customer Project

**Step 1**: Add to Customer Project List
```markdown
### [Customer Name]

#### X. Project Name [Status]
- **Status**: Active / Blocked / Pending / Completed
- **Type**: Implementation / Support / POC / Maintenance
- **Description**: Brief
- **Created**: YYYY-MM-DD
- **Last Review**: YYYY-MM-DD
- **Notes**: Progress, blockers
```

**Step 2**: If personal execution needed, also add to Quadrants

### Complete Customer Project

1. Mark Completed in Customer Project List
2. Archive the entry in archived.md
3. Complete related quadrant task if exists

### Add to Maybe List

1. Read `tasks/maybe.md`
2. Find highest task number (N)
3. Append new task as #(N+1) at END
4. Update total count and timestamp

### Check/Fix Numbering

Trigger phrases: "check task numbering", "fix sequence", "序号问题"

**Action**: Read file → scan issues → auto-fix → re-verify → repeat if needed

## Output Format (MUST OUTPUT AFTER EVERY OPERATION)

```markdown
✅ [Operation] Completed

**Summary:**
- Operation: [Add/Update/Complete/Move/Delete]
- Target: [Task name/ID]
- Location: [Q1/Q2/Q3/Q4/Customer/Maybe/Delegation/Archive]

**Statistics:**
| Quadrant | Count |
|----------|-------|
| Q1 | X |
| Q2 | X |
| Q3 | X |
| Q4 | X |
```

See [references/output-examples.md](references/output-examples.md) for detailed examples.

## Healthy Metrics

| List | Target | Warning |
|------|--------|---------|
| Customer Projects | 5-15 | - |
| Q1 | 3-5 | >5 indicates poor planning |
| Q2 | 8-12 | Core investment area |
| Q3 | 5-10 | Automate gradually |
| Q4 | <10 | Clean up regularly |
| Maybe | <20 | Review monthly |
| Delegation | <15 | Review weekly |

## Time Rhythm

- **Daily**: Check Q1, customer escalations
- **Weekly**: Review Customer Projects, Q2 planning, Delegation check
- **Monthly**: Archive completed, review blocked, adjust priorities

## Task Tags

- Customer tasks in quadrants: `[Customer/ProjectName]`
- Blocked tasks: `🚫 Blocked`
- Status: P0/P1/P2

## Dashboard (Optional)

A real-time web dashboard is available to view all tasks in a friendly format.

**Location**: `dashboard/`

**Features**:
- 📊 Real-time statistics showing task counts by quadrant
- 🔥 Four-quadrant matrix view with color coding
- 🏢 Customer projects overview with filtering
- 👑 Delegation list with assignee and deadline info
- 🌱 Maybe list for future ideas
- 🎨 Dark theme with modern UI design
- 🌐 Bilingual support (English/Chinese)
- ⚡ Real-time updates via WebSocket when markdown files change
- 📱 Responsive layout for different screen sizes
- 💡 **Hover to see full task details** - Mouse over any task card to see complete information including description, subtasks, tags, and timestamps
- 💻 **Integrated Terminal** - A built-in, resizable web terminal with automatic shell detection and history persistence across page reloads

### Dashboard Launch Workflow

After completing task operations, the skill will **offer** to open the dashboard:

```
✅ [Operation] Completed

Would you like to view the task dashboard?
[Open Dashboard] [Skip]

If approved → Auto-start dashboard and open browser
If skipped  → Dashboard remains available for manual launch
```

### Manual Launch (Anytime)

#### Method 1: Daemon Mode (Recommended for Long-term Use)

Run in background, service continues after terminal closes:

```bash
cd dashboard
# Start in background, no terminal dependency
./start.sh --daemon 

# Optional: You can specify custom task directory via flag or environment variable
./start.sh --daemon --tasks-dir /your/custom/path
# OR
export EISENHOWER_TASKS_DIR=/your/custom/path
./start.sh --daemon
```

**Features**:
- ✅ Service continues after terminal closes
- ✅ Auto PID management, prevents duplicate starts
- ✅ Logs output to `dashboard.log`
- ✅ Shows access URL and PID after startup

Stop the daemon:

```bash
./stop.sh               # Gracefully stop the service
```

#### Method 2: Foreground Mode (For Debugging)

Suitable for development and debugging, service stops when terminal closes:

```bash
cd dashboard
./start.sh              # Run in foreground, Ctrl+C to stop
```

#### Advanced Usage

```bash
# Specify port (default 8080)
./start.sh --daemon --port 3000

# Check running status
curl http://localhost:8080/api/health
```

### Architecture

**Tasks Directory Configuration:**
By default, the skill operates in the `tasks/` directory relative to this SKILL.md. You can override this globally by setting the `EISENHOWER_TASKS_DIR` environment variable to an absolute path (e.g., `export EISENHOWER_TASKS_DIR=/Users/xxx/tasks`).
- Markdown files are the single source of truth
- Node.js server parses markdown in real-time
- WebSocket pushes updates to browser when files change
- No database required - pure markdown-driven
- Enhanced error handling: global exception capture, port conflict detection

## Reference Materials

| File | Purpose |
|------|---------|
| `references/task-add.md` | **Complete workflow for adding tasks** - levels, quadrants, priorities, renumbering |
| `references/task-complete.md` | **Complete workflow for completing tasks** - 3 scenarios (Main/Delegation/Maybe), archiving |
| `references/numbering-rules.md` | Numbering rules for all 5 task lists |
| `references/output-examples.md` | Output format examples |
| `references/maybe-list-workflow.md` | Step-by-step Maybe List operations |
| `references/templates.md` | Statistics and report templates |
| `references/dashboard-offer.md` | Dashboard offer workflow after task operations |
| `dashboard/` | Real-time web dashboard (`./start.sh --daemon` for background mode) |

**Critical**: Always read `task-add.md` or `task-complete.md` before performing those operations to ensure full workflow compliance.

---

*Version: 8.3 (Fixed dirty read issue by enforcing read before modify)*
*Last Updated: 2026-06-17*
