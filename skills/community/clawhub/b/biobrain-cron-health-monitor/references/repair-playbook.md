# Cron Repair Playbook

## Step-by-Step Repair Process

### 1. Identify the Failure
```
cron(action="get", jobId="<your-job-id>")
```
Check `state.consecutiveErrors`, `state.lastError`, `state.lastRunStatus`

### 2. Classify the Error
Match against common-errors.md patterns:
- "Message failed" → Pattern A
- "LLM request failed" → Pattern B
- "Write failed" → Pattern C
- Timeout → Pattern D
- No output → Pattern E

### 3. Apply the Fix

**For Pattern A (Message failed):**
```
cron(action="update", jobId="<your-job-id>", patch={
  payload: {
    message: "Original prompt... IMPORTANT: Send result via sessions_send to main. Do NOT use message tool."
  }
})
```

**For Pattern B (LLM failed):**
```
cron(action="update", jobId="<your-job-id>", patch={
  payload: {
    model: "zai/glm-4-flash",
    fallbacks: ["zai/glm-4-flash"]
  }
})
```

**For Pattern C (Write failed):**
Add directory creation to the payload message:
```
message: "...First create the output directory with exec(mkdir -p), then write the file..."
```

**For Pattern D (Timeout):**
```
cron(action="update", jobId="<your-job-id>", patch={
  payload: { timeoutSeconds: 600, lightContext: true }
})
```

**For Pattern E (No output):**
```
cron(action="update", jobId="<your-job-id>", patch={
  payload: {
    message: "Original prompt... CRITICAL: Do NOT reply HEARTBEAT_OK. Execute fully and write results."
  }
})
```

### 4. Verify the Fix
After patching, trigger an immediate test run:
```
cron(action="run", jobId="<your-job-id>")
```
Wait for completion, then check `cron(action="get", jobId="<your-job-id>")` for `lastRunStatus`.

### 5. Document the Repair
Log the repair in the relevant department's notes:
```
write path="company/departments/{dept}/repair_log_YYYYMMDD.md"
```

## Escalation Path

| Level | Action |
|-------|--------|
| 1. Auto-fix | Apply known pattern fix |
| 2. Re-test | Trigger manual run, verify |
| 3. Escalate | If 2 fixes fail → flag for CEO |
| 4. Disable | If critical and unfixable → disable cron |
