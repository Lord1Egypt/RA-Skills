# Common Cron Error Catalog

## Error: "Message failed"
**Frequency:** Very common in isolated sessions
**Root cause:** The `message` tool requires channel auth (feishu, telegram, etc.) which isolated sessions don't inherit
**Fix:** Replace `message` tool calls with `sessions_send` to main agent
**Prevention:** Always specify "Do NOT use message tool, use sessions_send to main" in cron payload

## Error: "LLM request failed"
**Frequency:** Common with third-party models
**Root cause:** Model provider timeout, rate limit, invalid model name, expired API key
**Fix:** 
1. Check if model name is correct (e.g., `zai/glm-4-flash` not `glm-4-flash`)
2. Switch to a known-working free model
3. Add `fallbacks` array in payload
**Prevention:** Use free-tier models (zai/glm-4-flash) for internal tasks

## Error: "Write failed"
**Frequency:** Moderate
**Root cause:** 
- Template variable `{workspace_root_dir}` doesn't resolve in isolated sessions
- Parent directory doesn't exist
- File path contains invalid characters
**Fix:** 
1. Use absolute paths or create directories first
2. Avoid template variables in file paths
3. Use `exec` to `mkdir -p` before writing
**Prevention:** Test file paths in isolated sessions before deploying cron

## Error: Timeout / No response
**Frequency:** Moderate
**Root cause:** Task too complex, model too slow, or network issues
**Fix:**
1. Increase `timeoutSeconds`
2. Add `lightContext: true` to reduce context loading
3. Simplify the task prompt
4. Split into smaller tasks
**Prevention:** Set generous timeouts (300s+) for complex tasks

## Error: "HEARTBEAT_OK" (no real output)
**Frequency:** Common with vague prompts
**Root cause:** Agent interprets task as routine check-in and responds with minimal output
**Fix:** Add explicit instructions: "Do NOT reply HEARTBEAT_OK. Execute the task fully."
**Prevention:** Be specific in payload messages about expected output

## Error: "consecutiveSkipped" increasing
**Frequency:** Rare
**Root cause:** Cron scheduler skipping runs (disabled, or overlapping runs)
**Fix:** Check if job is enabled; check if previous run is still executing
**Prevention:** Set reasonable intervals between runs
