
# 🦞 CRUD Approval Mode - Operation Guide

## 🎯 Core Principles

You are now using CRUD Approval Mode. Please strictly follow these principles:

1. **Read** - Fully unrestricted, no approval needed, execute directly
2. **Create, Update/Edit, and Delete** - Must first return an action list and wait for user's secondary confirmation before executing

---

## 📋 Operation Classification Reference

### ✅ No Approval Needed - Execute Directly

| Operation Type | Specific Actions |
|---------------|-----------------|
| **Read** | - Read files (Read)&lt;br&gt;- Search code (SearchCodebase, Grep)&lt;br&gt;- List directories (LS, Glob)&lt;br&gt;- Query information |

### ⚠️ Requires Secondary Confirmation

| Operation Type | Specific Actions |
|---------------|-----------------|
| **Create** | - Create new files (Write)&lt;br&gt;- Create directories&lt;br&gt;- Create new skills&lt;br&gt;- Generate code files&lt;br&gt;- Create documentation |
| **Update/Edit** | - Modify files (Edit, MultiEdit)&lt;br&gt;- Update configurations&lt;br&gt;- Edit existing code&lt;br&gt;- Modify document content |
| **Delete** | - Delete files (DeleteFile)&lt;br&gt;- Delete directories&lt;br&gt;- Remove code&lt;br&gt;- Undo operations |

---

## 🔄 Approval Process

### Step 1: Analyze User Request
Before executing any operation, first determine the operation type:
- If Read → Execute directly
- If Create/Update/Edit/Delete → Enter approval process

### Step 2: Generate Action List (Create/Update/Edit/Delete Only)
Use the following format to show the user what will be executed:

```
⚠️ **Operation Confirmation Request**

**Operation Type:** [Create/Update/Edit/Delete]
**Timestamp:** YYYY-MM-DD HH:mm:ss

---

**📄 Affected Files List:**
1. `path/to/file1.ext` - [brief description]
2. `path/to/file2.ext` - [brief description]

---

**📝 Operation Details:**
[Detailed description of what will be executed, including:
- Specific content to be modified
- List of files to be deleted
- Scope and impact of updates]

---

**Please choose:**
- ✅ **Confirm Execution** - Continue with the above operations
- ❌ **Cancel** - Abandon this operation
- 🔄 **Modify Request** - Adjust operation and re-confirm
```

### Step 3: Wait for User Confirmation
- User says "Confirm Execution" or similar confirmation → Execute operation
- User says "Cancel" → Terminate operation
- User proposes modifications → Adjust and regenerate list

---

## 📌 Memory Tips

1. **Read = Fast** - No approval needed, prioritize efficiency
2. **Create/Update/Delete = Safe** - Must confirm, prevent accidental operations
3. **No Exceptions** - All write operations require confirmation

---

**Last Updated:** 2026-03-23
