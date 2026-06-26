# Environment Variables

Set in shell before launching `claude`, or in `settings.json` under `env`.

## Authentication

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | API key (overrides subscription) |
| `ANTHROPIC_AUTH_TOKEN` | Custom Authorization header value |
| `ANTHROPIC_BASE_URL` | Override API endpoint (proxy/gateway) |
| `ANTHROPIC_MODEL` | Model setting name |
| `CLAUDE_CODE_OAUTH_TOKEN` | OAuth access token (alternative to `/login`) |

## Model Configuration

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Pin Sonnet model |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Pin Opus model |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Pin Haiku model |
| `ANTHROPIC_CUSTOM_MODEL_OPTION` | Add custom model to `/model` picker |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Model for subagents |
| `CLAUDE_CODE_EFFORT_LEVEL` | Effort: low/medium/high/max/auto |

## Bash & Tool Control

| Variable | Purpose |
|----------|---------|
| `BASH_DEFAULT_TIMEOUT_MS` | Default bash timeout (default: 120000) |
| `BASH_MAX_TIMEOUT_MS` | Max bash timeout (default: 600000) |
| `BASH_MAX_OUTPUT_LENGTH` | Max chars before middle-truncation |
| `CLAUDE_CODE_SHELL` | Override shell detection |
| `CLAUDE_CODE_SHELL_PREFIX` | Wrap all bash commands |
| `CLAUDE_ENV_FILE` | Shell script sourced before each command |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | Reset to project dir after each command |

## Context & Compaction

| Variable | Purpose |
|----------|---------|
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | Compaction trigger % (1-100) |
| `CLAUDE_CODE_AUTO_COMPACT_WINDOW` | Override context window for compaction |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Max output tokens |
| `DISABLE_AUTO_COMPACT` | Disable auto-compaction |
| `DISABLE_COMPACT` | Disable all compaction |
| `MAX_THINKING_TOKENS` | Override thinking budget (0 to disable) |

## Features Toggle

| Variable | Purpose |
|----------|---------|
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | Disable auto memory |
| `CLAUDE_CODE_DISABLE_CLAUDE_MDS` | Don't load any CLAUDE.md files |
| `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING` | Disable checkpointing |
| `CLAUDE_CODE_DISABLE_THINKING` | Force-disable extended thinking |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | Disable background tasks |
| `CLAUDE_CODE_DISABLE_FAST_MODE` | Disable fast mode |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` | Remove git instructions from prompt |
| `CLAUDE_CODE_DISABLE_MOUSE` | Disable mouse tracking in fullscreen |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` | No auto terminal title updates |
| `CLAUDE_CODE_ENABLE_TASKS` | Enable tasks in print mode |
| `CLAUDE_CODE_NO_FLICKER` | Enable fullscreen rendering |

## MCP & Plugins

| Variable | Purpose |
|----------|---------|
| `MCP_TIMEOUT` | MCP server startup timeout (default: 30000) |
| `MCP_TOOL_TIMEOUT` | MCP tool execution timeout |
| `MAX_MCP_OUTPUT_TOKENS` | Max tokens in MCP responses |
| `ENABLE_TOOL_SEARCH` | Control MCP tool search behavior |
| `CLAUDE_CODE_PLUGIN_CACHE_DIR` | Override plugins root directory |

## Telemetry & Diagnostics

| Variable | Purpose |
|----------|---------|
| `DISABLE_TELEMETRY` | Opt out of Statsig telemetry |
| `DISABLE_ERROR_REPORTING` | Opt out of Sentry |
| `DISABLE_AUTOUPDATER` | Disable auto-updates |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | Disable all non-essential traffic |
| `CLAUDE_CODE_DEBUG_LOGS_DIR` | Override debug log path |

## Provider-Specific

| Variable | Purpose |
|----------|---------|
| `CLAUDE_CODE_USE_BEDROCK` | Use Amazon Bedrock |
| `CLAUDE_CODE_USE_VERTEX` | Use Google Vertex AI |
| `CLAUDE_CODE_USE_FOUNDRY` | Use Microsoft Foundry |
| `ANTHROPIC_VERTEX_PROJECT_ID` | GCP project for Vertex |
| `ANTHROPIC_BEDROCK_BASE_URL` | Custom Bedrock endpoint |

## Proxy & Network

| Variable | Purpose |
|----------|---------|
| `HTTP_PROXY` | HTTP proxy |
| `HTTPS_PROXY` | HTTPS proxy |
| `NO_PROXY` | Domains/IPs to bypass proxy |
| `API_TIMEOUT_MS` | API request timeout (default: 600000) |

## Session Control

| Variable | Purpose |
|----------|---------|
| `CLAUDE_CONFIG_DIR` | Override config directory (default: `~/.claude`) |
| `CLAUDE_CODE_SIMPLE` | Minimal tools, skip discovery (same as `--bare`) |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY` | Auto-exit after idle (ms) |
| `CLAUDE_CODE_TASK_LIST_ID` | Share task list across sessions |
| `IS_DEMO` | Demo mode: hide email, skip onboarding |
