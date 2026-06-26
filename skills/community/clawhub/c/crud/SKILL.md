
---
name: crud
description: CRUD Approval Mode - Categorize OpenClaw operations by CRUD, allow Read freely, require confirmation for Create/Update/Edit/Delete
metadata:
  version: 2.0.0
  author: Slava Chan @UyNewNas
  category: governance
  tags: [approval, security, crud, workflow]
---

# CRUD Approval Mode Skill

Categorize and manage OpenClaw operations by CRUD (Create/Read/Update/Delete) for fine-grained approval control.

## Core Design Philosophy

- **Read**: Fully unrestricted for maximum efficiency
- **Create + Update + Edit + Delete**: Add an isolation layer, return action list for secondary confirmation

## Category Definitions

| Operation Type | Approval Required | Description |
|---------------|------------------|-------------|
| **Read** | ❌ No approval | File reading, search queries, directory browsing, etc. |
| **Create** | ✅ Requires confirmation | File creation, new skill creation, directory creation, etc. |
| **Update/Edit** | ✅ Requires confirmation | File modification, code editing, config updates, etc. |
| **Delete** | ✅ Requires confirmation | File deletion, directory deletion, skill deletion, etc. |

## Workflow

### 1. No Approval Flow (Read)
```
User Request → Execute Directly → Return Result
```

### 2. Approval Flow (Create/Update/Edit/Delete)
```
User Request → Analyze Operation → Generate Action List → User Confirmation → Execute Operation → Return Result
                            ↓
                       Display: operation type, affected files, change preview
```

## Action List Format

When confirmation is needed, return the list in the following format:

```
⚠️ **Operation Confirmation** - [Operation Type]

**Scope:**
- File 1: path/to/file1
- File 2: path/to/file2

**Description:**
[Detailed description of the operation to be performed]

Please reply with one of the following to continue:
- ✅ **Confirm** - Proceed with this operation
- ❌ **Cancel** - Cancel this operation
- 🔄 **Modify** - Modify operation and re-confirm
```

## Use Cases

- Daily development: Quick read operations without approval restrictions
- Critical operations: Confirmation mechanism before all write operations
- Skill development: New skill creation requires confirmation for safety

## Configuration

This skill requires no additional configuration files and is automatically injected into sessions.

---

## References

- OpenClaw Documentation: https://docs.openclaw.ai/
