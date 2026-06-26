# Troubleshooting

## Commands: Quick Status Check

Run these before diagnosing failures:

```bash
whoami && echo "HOME=$HOME" && echo "SHELL=$SHELL"
echo "PATH=$PATH"
command -v claude && claude --version
test -n "$ANTHROPIC_API_KEY" && echo "API_KEY=set" || echo "API_KEY=missing"
test -n "$ANTHROPIC_AUTH_TOKEN" && echo "AUTH_TOKEN=set" || echo "AUTH_TOKEN=missing"
command -v jq || echo "jq=missing"
```

## Common Failures

### 403 Authentication Error
```
API Error: 403 {"error":{"type":"forbidden","message":"Request not allowed"}}
```
- **Cause**: API key not set or expired
- **Fix**: Check `ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN` env vars
- **Also check**: Are env vars set in non-interactive shells? (`.bashrc` guard)

### Command Not Found
```
claude: command not found
```
- **Cause**: claude CLI not in PATH
- **Fix**: `npm install -g @anthropic-ai/claude-code` or add install path to PATH

### Timeout
```
TIMEOUT: node invoke timed out
```
- **Cause**: Exec tool timeout shorter than API response time
- **Fix**: Increase timeout to 600+, use `background=true`
- **Fix**: Use `--output-format stream-json` to keep output flowing

### Permission Denied
```
permission_denials: [...]
```
- **Cause**: default permission mode blocks file operations
- **Fix**: Use `--permission-mode acceptEdits` or `--dangerously-skip-permissions`

### Invalid Request (Multi-line)
```
INVALID_REQUEST: SYSTEM_RUN_DENIED
```
- **Cause**: Some exec environments block multi-line heredocs
- **Fix**: Write script to `/tmp/` first, then execute

## Environment Loading

If environment variables aren't available in non-interactive shells:

1. Check `.bashrc` for interactive guard:
   ```bash
   grep -n "return" ~/.bashrc | head -3
   ```
2. If guard exists (`case $- in...` or `[ -z "$PS1" ]`), move API key exports above it
3. Alternative: use `bash -lc '...'` to force login shell
