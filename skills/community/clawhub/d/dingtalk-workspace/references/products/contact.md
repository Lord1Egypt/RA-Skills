# Contact Reference

## User Operations

### Search Users

```bash
dws contact user search --keyword "<name|mobile|email>" [--limit <N>]
```

**Parameters:**
- `--keyword`: Search term (name, mobile, or email)
- `--limit`: Max results (default: 50)

**Example:**
```bash
dws contact user search --keyword "John" --jq '.result[] | {name: .orgUserName, userId: .userId, mobile: .mobile}'
```

### Get User by ID

```bash
dws contact user get --user-id <userId>
```

### Get Current User

```bash
dws contact user get-self
```

**Example:**
```bash
dws contact user get-self --jq '.result[0].orgEmployeeModel | {name: .orgUserName, dept: .depts[0].deptName, userId: .userId}'
```

### Batch Query Users

```bash
dws contact user batch-get --user-ids <id1,id2,id3>
```

## Department Operations

### Search Departments

```bash
dws contact dept search --keyword "<dept-name>"
```

### Get Department Info

```bash
dws contact dept get --dept-id <deptId>
```

### List Department Members

```bash
dws contact dept members --dept-id <deptId> [--limit <N>]
```

**Example:**
```bash
dws contact dept members --dept-id "12345" --jq '.result[] | {name: .name, userId: .userId}'
```

### List Sub-departments

```bash
dws contact dept sub-depts --dept-id <deptId>
```

## Common Patterns

### Find User's Department

```bash
# Get user info with department
dws contact user get --user-id <userId> --jq '.result.depts[0].deptName'
```

### List All Members in Multiple Departments

```bash
# First get dept IDs
dws contact dept search --keyword "Engineering" --jq '.result[] | .deptId'

# Then get members for each
dws contact dept members --dept-id <dept-id>
```

### Search by Mobile

```bash
dws contact user search --keyword "13800138000" --jq '.result[0] | {name: .orgUserName, userId: .userId}'
```
