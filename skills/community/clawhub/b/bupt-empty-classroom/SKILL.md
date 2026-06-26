---
name: bupt-empty-classroom
description: Query empty classrooms at BUPT (Beijing University of Posts and Telecommunications) Xitucheng campus. Use when the user needs to find available/empty classrooms for a specific building and time period at Xitucheng campus. Supports selecting buildings (教2, 教3, 教4, 未来学习大楼) and time periods.
---

# BUPT Empty Classroom Query

This skill queries the BUPT empty classroom system at https://ec.jray.xyz/

## Workflow

### Step 1: Open the website
Use `agent-browser` to open the URL:
```bash
agent-browser open https://ec.jray.xyz/
```

### Step 2: Verify campus selection
- The page defaults to "西土城" (Xitucheng) campus
- Verify it's selected (look for `[checked]` on radio "西土城")
- If not, click on it: `agent-browser click @e2`

### Step 3: Select building
Click on the building button:
- 教2: `agent-browser click @e6`
- 教3: `agent-browser click @e7`
- 教4: `agent-browser click @e8`
- 未来学习大楼: `agent-browser click @e9`

### Step 4: Select time period
After clicking the building, the time period buttons will appear. Each button shows the format:
`HH:MM 节次 HH:MM`

Example buttons:
- 08:00 01 08:45 (第1节)
- 08:50 02 09:35 (第2节)
- ...and so on

Click on the desired time period button (check refs from snapshot).

### Step 5: Extract results
After selecting the time period, the page will show a table with empty classrooms:

| Column | Description |
|--------|-------------|
| 教室 | Classroom ID (e.g., 教4-203) |
| 座位数 | Number of seats |
| 类型 | Room type (if available) |
| 来源 | Data source (usually "教务") |

Use `agent-browser snapshot` or `agent-browser snapshot -i` to get the full table.

## Example Session

```bash
# Step 1: Open website
agent-browser open https://ec.jray.xyz/

# Step 2: Get initial snapshot to see refs
agent-browser snapshot -i

# Step 3: Click on building (e.g., 教4)
agent-browser click @e8

# Step 4: Get updated snapshot
agent-browser snapshot -i

# Step 5: Click on time period (e.g., 17:25 11 18:10)
agent-browser click @e20

# Step 6: Get final results
agent-browser snapshot
```

## Common Issues

1. **Button refs change after each navigation**: Always re-run `snapshot` after clicking a building or time period.

2. **Some time periods are disabled**: Passed time periods show `[disabled]` and cannot be clicked.

3. **No empty classrooms**: If no classrooms are shown after selecting a time period, it means all classrooms are occupied at that time.

## Notes

- The website defaults to current date
- Only Xitucheng campus is fully supported (沙河 campus can be selected but workflow is same)
- Data source is usually the university's academic system (教务)
