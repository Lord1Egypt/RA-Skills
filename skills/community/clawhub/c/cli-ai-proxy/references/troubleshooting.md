# Troubleshooting

## Proxy Won't Start

### Port already in use
```
Error: listen EADDRINUSE: address already in use 127.0.0.1:9090
```

Find and kill the existing process:
```bash
lsof -i :9090
kill <PID>
```

Or change the port in `config.yaml` or via env:
```bash
CLI_AI_PORT=9091 cli-ai-proxy start
```

### Node.js not found
```
ERROR: node not found
```

Install Node.js (v18+):
- macOS: `brew install node`
- Linux: `curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && sudo apt-get install -y nodejs`

### Build fails
```bash
# Clean and rebuild
cd <install-dir>
rm -rf dist/
npm run build
```

Check TypeScript version: `npx tsc --version` (needs 5.x+).

## CLI Not Available

> **Note on credentials.** The env vars below (`GEMINI_API_KEY`, `ANTHROPIC_API_KEY`) are consumed by the respective CLIs — **cli-ai-proxy never reads them**. The proxy only shells out to the CLI binary; all authentication state (OAuth tokens, API keys, session cookies) lives wherever the CLI puts it (usually under `~/.config/` or `~/.claude/` / `~/.gemini/`), managed by the CLI itself.

### Gemini CLI

Check installation:
```bash
which gemini
gemini --version
```

Install:
```bash
npm install -g @google/gemini-cli
```

Auth (handled entirely by the Gemini CLI, not the proxy):
```bash
gemini  # First run triggers OAuth login
# Or set the Gemini CLI's own API key env var:
export GEMINI_API_KEY=your-key
```

### Claude Code

Check installation:
```bash
which claude
claude --version
```

Install:
```bash
npm install -g @anthropic-ai/claude-code
```

Auth (handled entirely by Claude Code, not the proxy):
```bash
claude auth login
# Or set Claude Code's own API key env var:
export ANTHROPIC_API_KEY=your-key
```

## Request Errors

### 429 Too Many Requests
Concurrency limit reached. The proxy allows max 5 concurrent CLI processes by default.

Solutions:
- Wait for current requests to complete
- Increase `concurrency.max` in config.yaml
- Increase `concurrency.maxQueued` for more queue capacity

### 502 CLI Error
The CLI process exited with a non-zero code.

Check:
1. Proxy logs for stderr output from the CLI
2. Run the CLI manually to verify it works:
   ```bash
   echo "hello" | gemini --output-format stream-json --model gemini-2.5-flash
   ```
3. CLI auth may have expired — re-authenticate

### 503 CLI Not Found
The configured CLI binary was not found.

Check:
1. `which gemini` / `which claude` — is the binary in PATH?
2. If using custom paths in config.yaml, verify they exist
3. The proxy uses the PATH from its startup environment

### 504 Timeout
The CLI process exceeded the timeout limit (default: 5 minutes).

Solutions:
- Increase `timeout` in config.yaml (value in milliseconds)
- Check if the CLI is hanging on auth prompts
- Network issues between CLI and its API

## Image Issues

### "Cannot view images"
The CLI reports it cannot interpret image files.

Check:
- Image file exists in `tmp-images/` during the request
- The `tmp-images/` directory is NOT in `.gitignore` (Gemini CLI skips gitignored files)
- Image file is within the proxy's working directory (Gemini workspace restriction)

### Images not cleaned up
Temp images in `tmp-images/` should be auto-cleaned after each request.

If files remain:
```bash
rm -f <install-dir>/tmp-images/img-*
```

## OpenClaw Integration

### Provider not loading
After running `configure-provider.sh`:
1. Restart the OpenClaw gateway: `openclaw gateway restart`
2. Verify in `~/.openclaw/openclaw.json` that `models.providers.cli-ai-proxy` exists
3. Ensure the proxy is running: check `curl http://127.0.0.1:9090/health`

### "Message ordering conflict"
OpenClaw sends content in array format (`[{"type":"text","text":"..."}]`). The proxy supports this — ensure you're running the latest version.

### Model not found in OpenClaw
Verify models are registered in `agents.defaults.models` in `openclaw.json`:
```json
{
  "cli-ai-proxy/gemini": {},
  "cli-ai-proxy/claude": {}
}
```

## Logs

Proxy logs are at `proxy.log` in the installation directory.

View recent logs:
```bash
tail -50 <install-dir>/proxy.log
```

Follow live:
```bash
tail -f <install-dir>/proxy.log
```

Log levels: DEBUG, INFO, WARN, ERROR. Includes request timing, token counts, and CLI stderr output.
