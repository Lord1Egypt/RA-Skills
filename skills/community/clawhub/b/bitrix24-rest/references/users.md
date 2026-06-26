# Users, Departments, and Org Structure

Use this file for user lookup, department hierarchy, subordinates, managers, and org-structure reports.

## Users

- `user.current` — current webhook user (always start here to get own ID)
- `user.get` — get users by filter (supports `UF_DEPARTMENT`, `ACTIVE`, etc.)
- `user.search` — fast fuzzy search by name, position, department
- `profile` — basic info about current user (no scope required)

## Departments

- `department.get` — list departments (supports `PARENT`, `UF_HEAD`, `NAME` filters)
- `department.add` / `department.update` / `department.delete`
- `department.fields` — field schema

Key fields in `department.get`:

- `ID` — department ID
- `NAME` — department name
- `PARENT` — parent department ID (use to build tree)
- `UF_HEAD` — user ID of department head
- `SORT` — sort order

## Org Structure Helpers (Messenger API)

- `im.department.employees.get` — employees of given department(s)
- `im.department.managers.get` — managers/heads of given department(s)
- `im.department.colleagues.list` — colleagues of current user (for managers: returns subordinates)
- `im.department.get` — department data by ID
- `im.search.user.list` — search users by name/position
- `im.search.department.list` — search departments by name
- `im.user.get` — get user data by ID

`BX24.selectUsers` is frontend-only, not usable from REST.

## Common Use Cases

### Get current user identity

```bash
python3 scripts/bitrix24_call.py user.current --json
```

### Build department tree

Get all departments, use `PARENT` field to reconstruct hierarchy:

```bash
python3 scripts/bitrix24_call.py department.get --json
```

### Get subdepartments of a specific department

```bash
python3 scripts/bitrix24_call.py department.get \
  --param 'PARENT=1' \
  --json
```

### Get department head

```bash
python3 scripts/bitrix24_call.py im.department.managers.get \
  --param 'ID[]=5' \
  --param 'USER_DATA=Y' \
  --json
```

### Get all employees of a department

```bash
python3 scripts/bitrix24_call.py im.department.employees.get \
  --param 'ID[]=5' \
  --json
```

### Get subordinates (for a manager)

`im.department.colleagues.list` returns subordinates when called by a manager:

```bash
python3 scripts/bitrix24_call.py im.department.colleagues.list --json
```

### Get users by department

```bash
python3 scripts/bitrix24_call.py user.get \
  --param 'filter[UF_DEPARTMENT]=5' \
  --param 'filter[ACTIVE]=true' \
  --json
```

### Search users by name

```bash
python3 scripts/bitrix24_call.py user.search \
  --param 'FILTER[NAME]=Ivan' \
  --json
```

## Building Reports by Department

To build a report by department with subordinates:

1. Get all departments: `department.get`
2. For each department, get employees: `im.department.employees.get` or `user.get` with `filter[UF_DEPARTMENT]`
3. For each department, get head: `im.department.managers.get`
4. Cross-reference with task/timeman data as needed

## Working Rules

- Always start with `user.current` to know the webhook user's ID.
- Use `department.get` with `PARENT` filter to navigate the tree.
- `UF_HEAD` in department data gives the head's user ID directly.
- Pagination: page size 50, use `START=0`, `START=50`, etc.

## Good MCP Queries

- `user current get search`
- `department get fields`
- `im department employees managers colleagues`
- `im search user department`
