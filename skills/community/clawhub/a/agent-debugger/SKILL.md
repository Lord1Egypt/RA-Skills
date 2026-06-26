---
name: agent-debugger
description: Debug AI agent issues systematically. Covers tool failures, infinite loops, context overflow, rate limits, and performance bottlenecks. Use when agents misbehave, loop infinitely, fail tools, hit limits, or produce unexpected outputs. Triggers on "debug", "fix agent", "agent stuck", "agent looping", "tool failed", "rate limit".
---

# Agent Debugger

Systematic debugging for AI agent issues. When your agent misbehaves, this skill helps identify and fix the problem.

## Common Agent Problems

### 1. Infinite Loops

**Symptoms:**
- Agent repeats same action
- Gets stuck in a pattern
- Never completes task

**Diagnosis:**
```
Agent log shows:
- Same tool called 10+ times
- Same output format repeated
- No progress between iterations
```

**Fixes:**

Add iteration limit:
```json
{
  "maxIterations": 5,
  "onLimit": "ask_user"
}
```

Add explicit stop condition:
```
In your instructions, add:
"If you've tried the same approach 3 times without success, stop and ask the user for guidance."
```

### 2. Tool Failures

**Symptoms:**
- Tool returns error
- Tool times out
- Tool not found

**Diagnosis:**
```
Check:
- Tool exists in available_tools
- Parameters match tool schema
- Tool has required permissions
- Rate limits not exceeded
```

**Fixes:**

Validate parameters first:
```python
# Before calling tool
required_params = tool.get("required", [])
for param in required_params:
    if param not in args:
        raise ValueError(f"Missing required parameter: {param}")
```

Add retry logic:
```json
{
  "retries": 3,
  "retryDelay": 1000,
  "retryOn": ["rate_limit", "timeout", "5xx"]
}
```

### 3. Context Overflow

**Symptoms:**
- "Context length exceeded" error
- Agent forgets earlier conversation
- Truncated outputs

**Diagnosis:**
```
Check context window:
- Current tokens vs max tokens
- Number of messages in history
- Size of file contents loaded
```

**Fixes:**

Use memory efficiently:
```
- Load only relevant files
- Use offset/limit for large files
- Summarize long conversations
- Clear old context periodically
```

Compress context:
```python
# Instead of full file
content = read("file.txt", offset=1, limit=100)

# Use memory_search for specific info
results = memory_search("important decision")
```

### 4. Rate Limiting

**Symptoms:**
- "Rate limit exceeded" error
- Requests blocked
- 429 status codes

**Diagnosis:**
```
Check:
- API rate limits (requests per minute/hour)
- Token limits (tokens per minute)
- Concurrent request limits
- Time until reset
```

**Fixes:**

Add backoff:
```python
import time
import random

def call_with_backoff(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError as e:
            wait = (2 ** attempt) + random.random()
            time.sleep(wait)
    raise Exception("Max retries exceeded")
```

Queue requests:
```python
from queue import Queue
from threading import Thread

request_queue = Queue()

def process_queue():
    while True:
        task = request_queue.get()
        result = execute(task)
        request_queue.task_done()
        time.sleep(0.1)  # Rate limit: 10 req/s
```

### 5. Memory Issues

**Symptoms:**
- Agent doesn't remember previous context
- MEMORY.md not loaded
- Memory files not found

**Diagnosis:**
```
Check:
- MEMORY.md exists
- memory/ directory exists
- Files have correct permissions
- Memory loaded at startup
```

**Fixes:**

Verify memory setup:
```bash
ls -la ~/.openclaw/workspace/
# Should show:
# MEMORY.md
# memory/
```

Add memory to instructions:
```
Before answering anything about prior work, decisions, dates, people, or todos: 
run memory_search on MEMORY.md + memory/*.md
```

### 6. Permission Errors

**Symptoms:**
- "Permission denied"
- "Access denied"
- Tools not working

**Diagnosis:**
```
Check:
- User permissions
- File permissions
- Tool policies
- Sandbox restrictions
```

**Fixes:**

Check file permissions:
```bash
ls -la /path/to/file
chmod 600 ~/.openclaw/workspace/sensitive.json
```

Review tool policies:
```json
{
  "tools": {
    "exec": {
      "security": "ask",  // or "allowlist" or "full"
      "ask": "on-miss"    // or "always" or "off"
    }
  }
}
```

### 7. Performance Issues

**Symptoms:**
- Slow responses
- Timeouts
- High resource usage

**Diagnosis:**
```
Profile the agent:
- Time each tool call
- Count tokens used
- Measure context growth
- Identify bottlenecks
```

**Fixes:**

Optimize context:
```python
# Instead of loading entire file
content = read("large_file.txt", limit=50)

# Use targeted search
results = memory_search("specific topic")
```

Reduce tool calls:
```
# Bad: Multiple calls
file1 = read("file1.txt")
file2 = read("file2.txt")
file3 = read("file3.txt")

# Good: Parallel or combined
files = read(["file1.txt", "file2.txt", "file3.txt"])
```

## Debugging Workflow

### Step 1: Reproduce

```
1. Document exact steps to trigger issue
2. Note expected vs actual behavior
3. Check if issue is consistent or intermittent
4. Try with minimal example
```

### Step 2: Isolate

```
1. Disable other skills
2. Reduce context to minimum
3. Simplify task
4. Test each component separately
```

### Step 3: Diagnose

```
1. Check logs (if available)
2. Review tool outputs
3. Examine context window
4. Verify configuration
```

### Step 4: Fix

```
1. Apply fix
2. Test fix
3. Document fix
4. Update instructions if needed
```

### Step 5: Prevent

```
1. Add guardrails
2. Update error handling
3. Add logging
4. Document in memory
```

## Debugging Tools

### Check Agent Status

```python
# If you have access to session tools
status = session_status()
print(f"Model: {status['model']}")
print(f"Tokens used: {status['usage']['total_tokens']}")
print(f"Reasoning: {status['reasoning']}")
```

### Clear Context

```
If agent is stuck:
1. Start new session
2. Load only essential memory
3. Re-approach task fresh
```

### Enable Verbose Mode

```json
{
  "thinking": "verbose",
  "reasoning": "on"
}
```

This shows internal reasoning, helping identify where logic fails.

## Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `context_length_exceeded` | Too much context | Compress, summarize, limit |
| `rate_limit_exceeded` | Too many requests | Backoff, queue, wait |
| `tool_not_found` | Wrong tool name | Check spelling, install skill |
| `permission_denied` | Insufficient access | Check permissions, ask user |
| `invalid_parameters` | Wrong params | Validate against schema |
| `timeout` | Slow response | Increase timeout, optimize |
| `memory_not_found` | No memory files | Create MEMORY.md |

## Best Practices

### 1. Defensive Coding

```python
# Always check before acting
if not os.path.exists(file):
    return "File not found"

try:
    result = risky_operation()
except ExpectedError:
    handle_error()
```

### 2. Progress Tracking

```
In agent instructions:
"Track your progress. After each major step, note what you've done and what's next."
```

### 3. Checkpointing

```
For long tasks:
- Save progress periodically
- Document current state
- Allow resuming from checkpoint
```

### 4. Logging

```python
# Add to critical operations
log(f"Starting operation: {operation}")
log(f"Parameters: {params}")
log(f"Result: {result}")
log(f"Error: {error}")
```

## When to Ask for Help

Ask the user when:
- Multiple fix attempts failed
- Issue is intermittent
- Would require destructive actions
- Need information only user has
- Configuration changes needed

## Prevention Tips

1. **Set limits early** - max iterations, max tokens, max retries
2. **Validate inputs** - check parameters before calling tools
3. **Handle errors gracefully** - don't crash, report and adapt
4. **Log important events** - helps debugging later
5. **Test edge cases** - empty inputs, large files, special characters
6. **Monitor resources** - tokens, time, memory usage
7. **Document quirks** - save lessons in MEMORY.md