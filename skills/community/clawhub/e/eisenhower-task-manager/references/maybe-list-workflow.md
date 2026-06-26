# Maybe List Operations

Step-by-step workflow for Maybe List management.

## Adding Tasks to Maybe List

### Step 1: Read File
```bash
read: ~/.openclaw/workspace/tasks/maybe.md
```

### Step 2: Find Last Task Number
Scan headers (`#### N. Task Name`) and identify highest number.

### Step 3: Calculate New Number
```
New Number = Last Number + 1
```

### Step 4: Append to End
Add after last existing task. Never insert in middle.

### Step 5: Update Metadata
- Update total count in header
- Update `Last Updated` timestamp

### Step 6: Verify
- No duplicate numbers
- No gaps in sequence
- Last number equals total count

## Example

**Before (25 tasks):**
```markdown
#### 24. Task A
#### 25. Task B
```

**After adding Task C:**
```markdown
#### 24. Task A
#### 25. Task B
#### 26. Task C
```

## Critical Warning

If you see numbering like:
```markdown
#### 16. Task A
#### 26. Task B  <- WRONG! Gap present
#### 17. Task C
```

STOP immediately and renumber ALL tasks sequentially.

## Maybe List Numbering Rules

1. Sequential: 1, 2, 3, 4...
2. Always append to END
3. Never insert in middle with out-of-sequence numbers
4. Verify: last_task_number == total_task_count
5. If discrepancy: renumber ALL tasks
