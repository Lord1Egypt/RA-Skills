# Task Completion Flow

When user requests to complete a task, **must strictly follow these steps**, cannot skip or simplify.

## Task Type Judgment

First confirm the task type:
- **Main Task List Task**: In `tasks/tasks.md`
- **Delegation Task**: In `tasks/delegation.md`
- **Maybe List Task**: In `tasks/maybe.md`

According to task type, execute corresponding completion flow.

---

## Scenario One: Main Task List Completion Flow

Applicable to tasks in `tasks/tasks.md` (Four Quadrant Tasks).

### Steps

#### 0. Read Latest State (CRITICAL)
- **ALWAYS** use the `Read` tool to read `tasks/tasks.md` **FIRST** to get the absolute latest state before making any modifications. Never rely on historical context memory.

#### 1. Mark Complete
- Find corresponding task in task list file
- Change `[ ]` to `[x]` or add ✅ mark
- Update task status description (e.g., add completion time, notes, etc.)

**Note: This is only temporary marking, subsequent steps must be executed!**

#### 2. Delete Completed Task from Task List
- Delete complete task entry (including title line and description lines)
- Task content has been saved to archive file, main list only keeps incomplete tasks

#### 3. Renumber All Tasks
- After deleting completed task, renumber remaining tasks
- Ensure sequential numbers starting from 1, no duplicates, no gaps
- Renumber by priority groups (P0, P1, P2, P3, P4)

#### 4. Move Completed Task to Archive File
- Open `tasks/archived.md` file
- Add completed task to archive list
- Include: original number, task name, completion time, notes
- Maintain historical record format of archive file

#### 5. Update Progress Statistics
- Update task count statistics for each priority
- Update last modified timestamp

#### 6. Display Latest Task List
- Display original content of updated task list for user confirmation

---

## Scenario Two: Delegation Task Completion Flow

Applicable to tasks in `tasks/delegation.md` (Tasks delegated to subordinates).

### Steps

#### 1. Mark Complete
- Find corresponding task in delegation list
- Update status to `✅ Completed`
- Update `Last Review` to current date

#### 2. Delete Completed Task from Delegation List
- Delete complete task entry (including title line and description lines)

#### 3. Renumber All Delegation Tasks
- After deleting completed task, renumber remaining tasks
- Ensure sequential numbers starting from 1, no duplicates, no gaps

#### 4. Move Completed Delegation Task to Archive File
- Open `tasks/archived.md` file
- Add completed task to archive list
- Include: original number, task name, owner, completion time, notes
- Example format:
  ```markdown
  #### X. Task Name【Tag】- @owner
  - ✅ Completed
  - **Original Number**: X
  - **Owner**: @xxx
  - **Deadline**: YYYY-MM-DD
  - **Completion Time**: YYYY-MM-DD
  - **Notes**: Brief description
  ```

#### 5. Update Delegation Task Statistics
- Update total task count, in-progress count, completed count
- Update `@xxx owner tasks` statistics
- Update average completion rate
- Update last modified timestamp

#### 6. Display Latest Delegation List
- Display original content of updated delegation.md for user confirmation

---

## Scenario Three: Maybe List Task Completion Flow

Applicable to tasks in `tasks/maybe.md`.

### Steps

#### 1. Mark Complete
- Find corresponding task in Maybe List
- Update status to `✅ Completed`

#### 2. Delete Completed Task from Maybe List
- Delete complete task entry

#### 3. Renumber Tasks
- Renumber remaining tasks

#### 4. Move to Archive File
- Add completion record in `tasks/archived.md`

#### 5. Update Statistics
- Update total task count, completed count
- Update last modified timestamp

---

## ⚠️ Important Reminder

**DO NOT only execute Step 1 (mark complete) and stop!** Must fully execute all steps of the corresponding scenario.

## Examples

**User says**: "Complete task 5" (Main Task List)

Correct flow:
1. Find task 5 in tasks.md, temporarily mark as `[x]`
2. Delete complete entry of task 5
3. Renumber (original 6→5, 7→6, etc.)
4. Add task record in archived.md
5. Update statistics (P? count -1, archived +1)
6. Display updated tasks.md content

**User says**: "Complete task 3" (Delegation Task)

Correct flow:
1. Find task 3 in delegation.md, mark as `✅ Completed`
2. Delete complete entry of task 3
3. Renumber (original 4→3, 5→4, etc.)
4. Add task record in archived.md (include owner info)
5. Update statistics (in-progress -1, completed +1)
6. Display updated delegation.md content
