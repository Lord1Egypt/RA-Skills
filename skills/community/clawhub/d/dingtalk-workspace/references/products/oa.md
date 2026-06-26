# Approval (OA) Reference

## Approval Operations

### List Pending Approvals

```bash
dws oa approval list --status pending [--limit <N>]
```

**Example:**
```bash
dws oa approval list --status pending --jq '.result[] | {instanceId: .instanceId, title: .title, applicant: .applicantName}'
```

### List All Approvals

```bash
dws oa approval list [--status <pending|approved|rejected|all>] [--start <date>] [--end <date>]
```

### Get Approval Detail

```bash
dws oa approval get --instance-id <instanceId>
```

**Example:**
```bash
dws oa approval get --instance-id "inst123" --jq '.result | {title: .title, status: .status, applicant: .applicantName}'
```

### Approve Instance

```bash
dws oa approval approve --instance-id <instanceId> [--comment "<comment>"]
```

**Example:**
```bash
dws oa approval approve --instance-id "inst123" --comment "Approved" --yes
```

### Reject Instance

```bash
dws oa approval reject --instance-id <instanceId> --comment "<reason>"
```

**Example:**
```bash
dws oa approval reject --instance-id "inst123" --comment "Needs more details" --yes
```

### Revoke Instance

```bash
dws oa approval revoke --instance-id <instanceId>
```

## Process Operations

### List Approval Processes

```bash
dws oa process list
```

**Example:**
```bash
dws oa process list --jq '.result[] | {name: .name, processId: .processId}'
```

### Get Process Detail

```bash
dws oa process get --process-id <processId>
```

## Common Patterns

### Auto-Approve Low-Value Requests

```bash
# Get pending approvals
dws oa approval list --status pending --jq '.result[] | select(.title | contains("Expense")) | .instanceId'

# Approve each
for inst in $INSTANCES; do
  dws oa approval approve --instance-id "$inst" --comment "Auto-approved" --yes
done
```

### Batch Process Pending Approvals

```bash
# List with details
dws oa approval list --status pending --jq '.result[] | "\(.instanceId): \(.title) - \(.applicantName)"'

# Process one by one based on business logic
```

### Get My Pending Approvals

```bash
dws oa approval list --status pending --jq '.result[] | select(.handlerName == "Your Name") | {title: .title, instanceId: .instanceId}'
```
