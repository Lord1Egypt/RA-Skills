---
title: "Patterns and Best Practices"
source:
  - https://docs.github.com/en/copilot/how-tos/copilot-cli/best-practices-copilot-cli
category: reference
---

Operational patterns for using Copilot CLI effectively, especially in automation and agent workflows.

## Claude Code vs Copilot CLI Decision Matrix

| Scenario | Claude Code | Copilot CLI |
|----------|-------------|-------------|
| Large ground-up build | Preferred (cleaner stdout) | Fallback |
| Quick fix / surgical edit | Good | Good |
| Rate-limited on Claude Code | Switch to Copilot CLI | Use this |
| Structured output parsing | Clean stdout | PTY ANSI codes |
| Long iterative review loops | Rate limit risk | Better for many iterations |
| CI/CD automation | Not designed for CI | Built-in CI support |

**Key:** different binaries, different model registries, different rate limits. Not interchangeable.

## Prompt Engineering for Long Specs

- Model attention fades on 2000+ char specs (recency bias)
- Put **critical constraints at beginning AND end**
- Use emphasis: `CRITICAL:`, `REQUIREMENT:`, `MUST:`
- Number requirements — models track numbered lists better
- For JSON output: `Output ONLY JSON` at the end

## Polling for Structured Output

- Poll with `timeout: 60000–90000ms`
- If JSON appears truncated, poll again (agent may still be writing)
- `--output-format json` = JSONL streaming (harder to parse)
- Natural output with embedded JSON is often more reliable
- Multiple polls are normal — don't assume truncation = failure

## Session Naming and Traceability

Add comment tag in prompt: `copilot --yolo --no-ask-user -p 'Build V3... #my-task-v3'`

Export transcripts: `--share='./session-report.md'` or `--share-gist`

## Temp Directory Workflow

```bash
dir=$(mktemp -d) && cd "$dir"
git init && git config user.email "bot@example.com" && git config user.name "Bot"

# Pre-trust (--yolo won't bypass trust prompt)
python3 -c "
import json; p='$HOME/.copilot/config.json'
c=json.load(open(p))
c.setdefault('trusted_folders',[]).append('$dir')
json.dump(c, open(p,'w'), indent=2)
"

copilot -p "Build something..." --yolo --no-ask-user
```

**Remember:** `/tmp` cleaned periodically — copy builds to permanent storage.

## Anti-Patterns

| Anti-pattern | Why it fails | Do this instead |
|-------------|-------------|-----------------|
| `-i` in scripts | Hangs waiting for input | Use `-p` |
| `--yolo` to skip trust | Trust prompt is separate | Pre-trust in config |
| Short timeouts for large tasks | SIGTERM kills mid-work | Size by complexity |
| Assuming servers persist | Killed between exec spawns | Restart before each use |
| Re-initing existing repos | Corrupts git history | Only `git init` for new temp dirs |
| Ignoring rate limits | Task fails silently | Copilot CLI as Claude Code fallback |
