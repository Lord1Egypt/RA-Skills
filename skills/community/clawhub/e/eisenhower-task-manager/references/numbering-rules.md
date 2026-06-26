# Task Numbering Rules

Complete numbering rules for all task lists.

## Overview

| File | Numbering Type | Key Rule |
|------|----------------|----------|
| tasks.md | Quadrant-continuous | Q1:1-N, Q2:N+1-M, Q3:M+1-P, Q4:P+1-Q |
| maybe.md | Simple sequential | 1, 2, 3... append to END |
| customer-projects.md | Per-customer | 1, 2, 3... per customer |
| delegation.md | Simple sequential | 1, 2, 3... append to END |
| archived.md | Simple sequential | 1, 2, 3... append to END |

## tasks.md (Quadrant Tasks)

**Rule**: Continuous numbering across quadrants

```
Q1: ### 1. Task A
      ### 2. Task B
Q2: ### 3. Task C  <- Q1_count + 1
      ### 4. Task D
Q3: ### 5. Task E  <- Q2_end + 1
Q4: ### 6. Task F  <- Q3_end + 1
```

**Verification**:
- Q2 starts at Q1_count + 1
- Q3 starts at Q2_end + 1
- Q4 starts at Q3_end + 1
- No gaps between quadrants

## maybe.md (Maybe List)

**Rule**: Sequential 1-N, always append to end

```markdown
#### 24. Task A
#### 25. Task B
#### 26. Task C  <- New task at END
```

**Never do this**:
```markdown
#### 16. Task A
#### 26. Task B  <- WRONG! Gap in middle
#### 17. Task C
```

**Verification**: last_number == total_count

## customer-projects.md (Customer Projects)

**Rule**: Per-customer numbering, independent across customers

```markdown
### Customer A
#### 1. Project X
#### 2. Project Y

### Customer B
#### 1. Project Z  <- Independent numbering
#### 2. Project W
```

**Verification**: Each customer's tasks numbered 1-N independently

## delegation.md (Delegation List)

**Rule**: Sequential 1-N, always append to end

```markdown
### 1. Task A @john
### 2. Task B @mary
### 3. Task C @peter  <- New task at END
```

**Format**: Include assignee: `### X. Task Name @assignee`

**Verification**: last_number == total_count

## archived.md (Archive)

**Rule**: Sequential 1-N, group by archive date

```markdown
## Archived 2026-04-15
### 1. Task A [Completed]
### 2. Task B [Deleted]

## Archived 2026-04-14
### 3. Task C [Completed]
```

**Format**: Include archive date: `### X. Task Name [Archived: YYYY-MM-DD]`

**Verification**: last_number == total_count

## Universal Numbering Checklist

After EVERY operation on ANY list:

- [ ] Read the file
- [ ] Scan all task numbers
- [ ] Check for duplicates
- [ ] Check for gaps
- [ ] Verify sequential from 1
- [ ] Fix issues if found
- [ ] Re-read to confirm

**Trigger auto-fix on phrases**:
- "check task numbering"
- "fix sequence"
- "序号问题"
