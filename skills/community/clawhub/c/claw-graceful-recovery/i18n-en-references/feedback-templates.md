# User Feedback Templates Reference

All feedback is sent via Claw's WeChat response channel. Raw error stack traces are strictly prohibited.

---

## Standard Feedback Template

```
⚠️ Task aborted: [brief task description]
Reason: [error type]
Suggestion: [optional, provide alternative or explain limitation]

Ready. Send your next instruction.
```

---

## Scenario-Based Templates

### Scenario 1: Single file/operation permission denied

```
⚠️ Task aborted: reading /var/log/system.log
Reason: Insufficient permissions (root required)
Suggestion: Try running sudo manually in terminal, then retry

Ready. Send your next instruction.
```

### Scenario 2: Some files skipped in a batch task

```
Done: Processed 8/10 files
Skipped:
  - /etc/hosts (insufficient permissions)
  - /var/log/auth.log (access denied)

All other files processed normally. Ready. Send your next instruction.
```

### Scenario 3: 3+ consecutive instructions fail due to permissions

```
⚠️ Notice: The last 3 instructions were all aborted due to permission issues.
Claw's current runtime environment may lack necessary file system permissions.
Suggestion: Check whether Claw has access to the target directory?
Pausing execution, waiting for your instructions.
```

### Scenario 4: WeChat channel itself unavailable (extreme case)

When the AI cannot send feedback to the user, silently write to log:

```bash
echo "[$(date)] Permission error recovery: <operation description> | <error type>" >> ~/claw_recovery.log
```

---

## Prohibited Feedback Formats (anti-examples)

```
# ❌ PROHIBITED: Sending raw error stack trace
Error: EACCES: permission denied, open '/var/log/system.log'
    at Object.openSync (fs.js:462:3)
    at Object.readFileSync (fs.js:364:35)

# ❌ PROHIBITED: Exposing system paths to user
Cannot access /Users/admin/.ssh/id_rsa, permission denied

# ❌ PROHIBITED: Technical descriptions
errno: -13, code: 'EACCES', syscall: 'open'
```

---

## Feedback Language Principles

1. Use English, concise, no more than 3 lines (except Scenario 2)
2. Do not use technical terms (use "insufficient permissions" instead of "EACCES")
3. Do not expose full file paths; use generic descriptions like "system log file"
4. Always end with "Ready. Send your next instruction." (except Scenario 3)
