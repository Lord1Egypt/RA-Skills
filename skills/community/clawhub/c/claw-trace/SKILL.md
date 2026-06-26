---
name: claw-trace
license: MIT
description: |
  Track and visualize the OpenClaw agent's work process. Record tool call inputs, outputs, duration, and status, and present them in an easy-to-read format.
  **IMPORTANT**: When config `enable = true`, this skill MUST automatically show trace output after EVERY tool call, WITHOUT waiting for user to ask "show trace".
  Only applicable to OpenClaw platform.
---

# Claw Trace - Work Process Visualization

This Skill is used to record and display the AI agent's work process.

## Feature Modules (Configurable)

User can say "enable XX feature" or "use simple mode" to switch.

### Module 1: Call Table (Enabled by Default)

| Step | Tool | Input | Result | Duration |
|------|------|-------|--------|----------|
| 1 | web_search | query: "xxx" | ❌ Failed | 0ms |
| 2 | web_fetch | url: "xxx" | ✅ Success | 230ms |

### Module 2: Flowchart (Enabled by Default)

[User Request]
    ↓
1. web_search → ❌
    ↓
2. web_fetch → ✅
    ↓
[Reply to User]

### Module 3: Statistics (Optional)

```
📊 Work Statistics
⏱️ Total Time: 8.5s
🔧 Tool Calls: 15 times
✅ Success Rate: 87% (13/15)

📈 Tool Usage Ranking:
  1. web_fetch  - 10 times (67%)
  2. exec       - 3 times (20%)
```

### Module 4: Detailed Log (Optional)

Record complete input/output for each call (except sensitive info).

### Module 5: Save to File (Optional)

Generate Markdown report saved to workspace.

### Module 6: Filters (Optional)

Filter tool calls by various criteria:

| Filter Type | Command | Example |
|-------------|---------|---------|
| By tool name | "filter: tool_name" | "filter: web_search" |
| By result | "filter: success" / "filter: failed" | "filter: failed" |
| By time | "filter: last N calls" | "filter: last 5 calls" |
| By keyword | "filter: keyword in output" | "filter: error" |

Multiple filters can be combined: "filter: web_search and failed"

### Module 7: Export Format (Optional)

Choose export format:
- Markdown (default)
- JSON
- HTML (with syntax highlighting)

## Usage

### Configuration File

The Skill has a config file `config.json` with the following options:

```json
{
  "enable": false,        // Whether to enable by default (default: false, on-demand)
  "mode": "simple",       // Mode: simple / full
  "enabledModules": {
    "table": true,        // Call table
    "flowchart": true,   // Flowchart
    "statistics": false,  // Statistics
    "detailedLog": false,// Detailed log
    "saveToFile": false  // Save to file
  },
  "language": "auto"       // Language: auto / zh / en
}
```

### User Commands

User can modify config through conversation:

| Command | Action |
|---------|--------|
| "enable trace" | enable = true |
| "disable trace" | enable = false |
| "use simple mode" | mode = simple |
| "use full mode" | mode = full |
| "enable statistics" | statistics = true |
| "enable filters" | filters = true |
| "filter: tool_name" | filter by tool name |
| "filter: success/failed" | filter by result |
| "filter: last N calls" | filter by count |
| "output in English" | language = en |
| "output in Chinese" | language = zh |

### Workflow

1. **Each time Skill is called**: Read `config.json` first to get current config
2. **Based on config**:
   - enable = false → Don't show (unless user explicitly requests)
   - enable = true → **MUST automatically show** trace output after every tool call, do NOT wait for user to ask
3. **When user modifies config**: Update config.json and save

### ⚠️ Important Rule

**When enable = true, trace output MUST be included in EVERY reply after tool calls automatically, without waiting for user to say "show trace"!**

### Language Auto-Detection

- Output language follows user's language
- User speaks Chinese → Output in Chinese
- User speaks English → Output in English

## Notes

- Sensitive info (API Keys, passwords) should not be recorded
- Truncate overly long output with [...]
- Clearly indicate reasons for failed calls
- Keep output concise, don't over-detail

## ⚠️ Security Guidelines

### Sensitive Data Redaction (MANDATORY)

Before displaying any tool call input/output, you MUST redact the following:

**Must redact:**
- API Keys, Tokens, Passwords (patterns: `key=`, `token=`, `password=`, `Authorization:`)
- File contents that may contain secrets
- User credentials or private data

**How to redact:**
- Replace with `[REDACTED]` or `[HIDDEN]`
- Keep the structure but mask values
- Example: `{"api_key": "sk-xxx"}` → `{"api_key": "[REDACTED]"}`

### Safe Defaults

Default configuration is set to:
- `enable: false` (off by default, user must explicitly enable)
- `detailedLog: false` (don't record full inputs/outputs)
- `saveToFile: false` (don't persist to disk)

### Best Practices

1. **Test before enabling** - Enable in a safe environment first
2. **Review outputs** - Check that no secrets appear in traces
3. **Use simple mode** - Avoid detailed logging in production
4. **Disable after use** - Turn off when not needed
