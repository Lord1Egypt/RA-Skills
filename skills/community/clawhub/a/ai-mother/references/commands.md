# AI Butler Reference Guide

## Common AI Agent Commands

### Claude Code
```bash
# One-shot task
claude --permission-mode bypassPermissions --print 'task description'

# Interactive mode
claude

# With specific model
claude --model claude-sonnet-4 'task'
```

### Codex
```bash
# Execute task
codex exec 'task description'

# Interactive mode
codex

# With yolo mode (auto-approve)
codex --yolo exec 'task'
```

### OpenCode
```bash
# Execute task
opencode 'task description'
```

### Gemini
```bash
# Execute task
gemini 'task description'
```

## Process States

| State | Meaning | Action |
|-------|---------|--------|
| R | Running | Normal, actively executing |
| S | Sleeping | Normal, waiting for event |
| T | Stopped | Suspended (Ctrl+Z), needs resume |
| Z | Zombie | Crashed, parent needs cleanup |
| D | Uninterruptible sleep | Usually I/O wait |

## Common Issues & Solutions

### Issue: Process Stopped (T state)
**Cause:** User pressed Ctrl+Z or process received SIGSTOP
**Solution:** Resume with `kill -CONT <PID>`

### Issue: Process Zombie (Z state)
**Cause:** Process finished but parent didn't collect exit status
**Solution:** Usually self-resolves; if not, restart parent process

### Issue: High CPU, No Progress
**Cause:** Infinite loop or stuck computation
**Solution:** 
1. Check logs for repeated errors
2. Send interrupt signal: `kill -INT <PID>`
3. If unresponsive, force kill: `kill -9 <PID>`

### Issue: AI Waiting for Input
**Cause:** AI needs user confirmation or data
**Solution:**
1. Check process logs
2. Use `process(action: "write")` to send input
3. Or use `process(action: "submit")` to send input + Enter

### Issue: Permission Denied
**Cause:** AI lacks file/directory permissions
**Solution:**
1. Check file permissions: `ls -la <path>`
2. Grant permissions if safe: `chmod +r <file>`
3. Or run AI with elevated permissions (requires owner approval)

## Safety Checklist

Before granting AI requests, verify:

- [ ] Request is within project scope
- [ ] No sensitive data exposure
- [ ] No destructive operations (rm, drop, delete)
- [ ] No external communications (email, API calls)
- [ ] No financial transactions
- [ ] No credential sharing
- [ ] Owner would approve this action

If ANY checkbox fails, escalate to owner.

## Escalation Template

```
🚨 AI Agent Needs Owner Decision

**Agent:** <AI name> (PID: <PID>)
**Project:** <path>
**Request:** <what AI wants to do>

**Context:**
<brief explanation of what AI is working on>

**Risk Assessment:**
<why this needs owner approval>

**Recommendation:**
<approve/deny + reasoning>

**Question for Owner:**
<specific question>
```

## Communication Templates

### To AI: Request Status
```
Hi! I'm the AI Butler checking in. Can you give me a quick status update?

1. What task are you working on?
2. What's your current progress?
3. Are you blocked on anything?
4. Do you need any help or permissions?
```

### To AI: Provide Help
```
I see you're stuck on <issue>. Here's what I found:

<information or solution>

Does this help? Let me know if you need anything else.
```

### To AI: Request Clarification
```
I need to understand your request better before I can help:

<specific questions>

Please provide these details so I can assist you properly.
```

### To Owner: Status Report
```
📊 AI Agent Status Report - <timestamp>

**Active Agents:** <count>

<agent details>

**Issues:** <any problems>
**Recommendations:** <suggested actions>
**Completed:** <finished tasks>
```

### To Owner: Urgent Issue
```
⚠️ Urgent: AI Agent Issue

**Agent:** <name> (PID: <PID>)
**Problem:** <brief description>
**Impact:** <what's affected>
**Immediate Action Needed:** <yes/no>

<details>
```
