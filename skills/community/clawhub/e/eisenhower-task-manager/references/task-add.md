# Task Addition Flow

When user requests to add or insert a task, follow these steps:

## Steps

### 0. Read Latest State (CRITICAL)
- **ALWAYS** use the `Read` tool to read the target task file (e.g., `tasks.md`, `delegation.md`) **FIRST** to get the absolute latest state before making any modifications. Never rely on historical context memory.

### 1. Determine Level and Quadrant
- Judge task type: Personal execution → Four Quadrants; Delegated → Delegation List; Uncertain → Maybe List
- If four quadrants task, judge importance (valuable for business/team/personal growth) and urgency (has deadline/blocking others/expired)
- Determine quadrant: 🔥Q1 (Important+Urgent), 💼Q2 (Important+Not Urgent), ⚡Q3 (Not Important+Urgent), 🧘Q4 (Not Important+Not Urgent)

### 2. Determine Micro Priority
- Assign P0/P1/P2 within **same quadrant**:
  - **🔴 P0**: Must do today (hard deadline or blocking others)
  - **🟡 P1**: Complete within this week (near-term high priority)
  - **🟢 P2**: Within this month/quarter (important but not urgent)

### 3. Insert Task
- Insert new task at appropriate position within corresponding quadrant (in P0→P1→P2 order)
- Maintain relative order of other tasks in that quadrant
- Task format:
  ```markdown
  ### 🔥 Q1: Important + Urgent (Do Immediately)

  #### 1. Task Name【Tag】
  - [ ] **Status**: P0
  - [ ] **Description**: Task description
  - [ ] **Created**: YYYY-MM-DD
  - [ ] **Notes**: xxx
  ```

### 4. Renumber All Tasks
- Renumber all tasks (starting from 1)
- Ensure sequential numbers, no duplicates, no gaps
- Group by priority: 🔥Q1 → 💼Q2 → ⚡Q3 → 🧘Q4 → 🌱Maybe List → 👑Delegation List

### 5. Update Statistics
- Update task count for each quadrant
- Update number ranges for each quadrant
- Update last modified timestamp

### 6. Display Latest Task List
- Display original content of updated task list for user confirmation

## Examples

**User says**: "Add task: Hire new engineer, P0, Q1"

Operation flow:
1. Confirm quadrant is Q1, priority is P0
2. Insert new task at end of Q1 P0 group
3. Renumber (this task and all subsequent tasks +1)
4. Update statistics: Q1 count +1
5. Display updated complete list

**User says**: "Add task: Research AI painting, P2, Q4"

Operation flow:
1. Confirm quadrant is Q4, priority is P2
2. Insert new task at end of Q4 P2 group
3. Renumber
4. Update statistics: Q4 count +1
5. Display updated complete list
