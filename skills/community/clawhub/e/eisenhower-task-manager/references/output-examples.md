# Output Format Examples

Detailed examples for operation output formats.

## After Adding a Task

```markdown
✅ Task Added Successfully

**Summary:**
- Operation: Add new task
- Task: #18 - Example Task Name
- Location: Q2 (Important + Not Urgent)
- Priority: P1

**Statistics:**
| Quadrant | Count | Task Numbers |
|----------|-------|--------------|
| Q1 | 4 | 1-4 |
| Q2 | 14 | 5-18 |
| Q3 | 4 | 19-22 |
| Q4 | 0 | - |
| Total | 22 | - |
```

## After Adding to Customer Projects

```markdown
✅ Customer Project Task Added

**Summary:**
- Operation: Add customer project sub-task
- Customer: Customer Name
- Task: Task Name Description
- Status: Active

**Customer Project Summary:**
| Metric | Value |
|--------|-------|
| Total Sub-tasks | 4 |
| Active | 3 |
| Blocked | 1 |

**Next Step:** Consider adding to Q2 if personal execution required.
```

## After Completing a Task

```markdown
✅ Task Completed

**Summary:**
- Operation: Complete task
- Task: #5 - Example Completed Task
- Moved to: Archive

**Statistics:**
| Quadrant | Before | After |
|----------|--------|-------|
| Q2 | 14 | 13 |
| Completed | - | +1 |

Great progress!
```

## After Adding to Maybe List

```markdown
✅ Maybe List Task Added

**Summary:**
- Operation: Add to Maybe List
- Task: #26 - Example Future Task
- Location: Maybe List

**Statistics:**
| Metric | Value |
|--------|-------|
| Total Maybe Tasks | 26 |
| Last Number | 26 |

Status: Sequential numbering verified.
```
