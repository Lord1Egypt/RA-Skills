# ACP Fallback System - Resilient Agent Execution

## Overview
This skill provides automatic fallback for ACP vendors (Codex → Claude → Pi → API) and model fallback for subagents. If one vendor fails, it automatically tries the next.

## Usage

### For Agents - Use acp_exec Function

```bash
# Instead of direct acpx calls, use this wrapper
source scripts/acp-fallback.sh && acp_exec "your task here"
```

### ACP Vendor Priority (in order):
1. **codex** - Primary (fast, reliable)
2. **claude** - Fallback #1 (high quality)
3. **pi** - Fallback #2 (lightweight)
4. **direct-api** - Final fallback (uses OpenClaw's built-in models)

### What Happens on Failure:
- Vendor fails → Auto-retry with next vendor
- All vendors fail → Log error, return failure status
- Success → Return result immediately

## Implementation

### Core Functions

```bash
# acp_exec - Main entry point
# Usage: acp_exec "task description"
# Returns: Vendor used + result

# acp_exec_with_fallback - Full fallback chain
# Tries: codex → claude → pi → direct-api
# Returns: First successful result

# model_fallback - For subagent model switching
# Tries: MiniMax → DeepSeek → OpenAI → GLM-5
```

### Agent Integration

Agents should call these functions instead of direct acpx commands:
- Replace `npx acpx codex exec "..."` with `acp_exec "..."`
- Replace single-model subagent with fallback-enabled wrapper

## Error Handling

- Network errors: Retry with next vendor after 3s
- Auth errors: Skip to next vendor immediately  
- Rate limits: Wait 10s, then retry
- Timeout (>120s): Move to next vendor

## Logging

All fallback attempts logged to:
- `logs/acp-fallback.log`

## Success Metrics

Tracked:
- Vendor used
- Number of retries
- Total time
- Success/failure status
