# CoVe Plugin — Usage Guide

## Installation Methods

### Method 1: OpenClaw Native Skill (Recommended)

Copy the skill files into your OpenClaw directory:

```bash
# Copy skill definition (enables auto-discovery)
cp SKILL.md ~/.openclaw/cove-skill.md

# Copy the CLI tool
cp src/verifier.js /usr/local/bin/cove-verify
chmod +x /usr/local/bin/cove-verify

# Copy supporting modules next to verifier.js or set NODE_PATH
mkdir -p /usr/local/lib/cove
cp src/*.js /usr/local/lib/cove/
```

Your agent will automatically discover and use `cove-verify` when `nativeSkills` is set to `"auto"` in your OpenClaw config.

### Method 2: Plugin Directory

```bash
git clone https://github.com/bhawanakatiyar/cove-plugin.git ~/.openclaw/plugins/cove-verification
```

### Method 3: Standalone CLI

```bash
# Run directly from the plugin directory
node src/verifier.js -r "Your text to verify"

# Or create an alias
alias cove-verify="node /path/to/cove-plugin/src/verifier.js"
```

## Configuration

### Config File Location

CoVe looks for config in this order:
1. `<plugin-dir>/config/default.yaml`
2. `~/.openclaw/cove.yaml`

### Configuration Options

```yaml
# Verification policy
# basic    — memory + workspace only
# standard — adds web search
# deep     — multi-step reasoning + web search
policy: "basic"

# Automatically rewrite response with corrections
auto_correct: true

# How many correction attempts before giving up
max_correction_attempts: 1

# Log verification results to stdout (captured by OpenClaw)
log_results_to_dashboard: true

# Override the LLM model used for verification
# null = use COVE_MODEL env var or default (gemini-2.0-flash)
model_override: null

# Automatically verify all responses (use with caution — doubles LLM cost)
auto_verify: false

# Knowledge source configuration
knowledge_sources:
  # Read agent memory files from ~/.openclaw/workspace/memory/
  use_system_memory: true

  # Additional directories to scan for knowledge
  document_paths: ["/home/bk/docs/knowledge"]

  # Enable Brave Search for web verification (requires BRAVE_API_KEY)
  enable_web_search: false
```

## CLI Reference

```
cove-verify [options]

Options:
  -r, --response TEXT    Response text to verify
  --stdin                Read response from stdin (or pipe)
  -p, --policy POLICY    basic | standard | deep (default: basic)
  -f, --format FORMAT    text | json (default: text)
  --strict               Exit code 2 if any claim is unverifiable
  --no-correct           Report inaccuracies without auto-correcting
  --help                 Show help
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All claims verified (or no claims found) |
| 1 | One or more claims are inaccurate |
| 2 | Strict mode: unverifiable claims found |

## Programmatic Usage

```javascript
const { verifyResponse } = require('./src/verify_claims');

const report = await verifyResponse(
  "Alice signed up on March 1st and is on the Basic plan.",
  { policy: 'standard', auto_correct: true }
);

console.log(report.verified);          // false
console.log(report.correctedResponse); // "Alice signed up on March 17th..."
console.log(report.summary);           // { total: 2, verified: 1, inaccurate: 1, unverifiable: 0 }
```

## Knowledge Sources

CoVe reads from these locations by default:

| Source | Path | Contents |
|--------|------|----------|
| Agent memory | `~/.openclaw/workspace/memory/` | Memory files (`.md`, `.txt`) |
| Workspace | `~/.openclaw/workspace/` | User files (`.csv`, `.json`, `.md`, etc.) |
| Agent docs | `~/.openclaw/*.md` | Agent instructions, skill docs |
| Custom paths | Configured in `document_paths` | Any text files |

Supported file types: `.md`, `.txt`, `.csv`, `.json`, `.yaml`, `.yml`, `.xml`, `.html`, `.log`

Files larger than 10 KB per file are skipped. Total knowledge context is capped at 50 KB.

## Cost Considerations

Each `cove-verify` call makes 2-3 LLM calls:
1. **Claim extraction** (~500 tokens)
2. **Claim verification** (~1000-2000 tokens depending on knowledge base size)
3. **Correction** (~500 tokens, only if inaccuracies found)

With `gemini-2.0-flash`, this costs approximately $0.001–0.003 per verification. Use selectively for important claims, not every message.

## Troubleshooting

### "LLM request timed out"
The sidecar proxy at localhost:8888 is not responding. Make sure your OpenClaw instance is running.

### "Failed to parse LLM response"
The LLM returned an unexpected format. Try a different model via `COVE_MODEL` env var.

### "No source files found"
No readable files found in memory/workspace. Check that your workspace has `.md`, `.csv`, or other text files.

### Web search returns no results
Set `BRAVE_API_KEY` environment variable or add it to `~/.openclaw/.brave-api-key`.
