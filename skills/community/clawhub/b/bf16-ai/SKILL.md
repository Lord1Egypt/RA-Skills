---
name: bf16-uncensored-api
description: Configure OpenClaw, Claude Code, Codex CLI, OpenCode, Goose, and autonomous agents to use bf16.ai 1M-context uncensored LLM APIs (DeepSeek V4.1 Flash Fast, GLM-5.3, Kimi K3.1 Pro 2.8T) with strict zero prompt retention and pay-as-you-go pricing.
homepage: https://bf16.ai/docs/clients/openclaw
---

# bf16.ai Uncensored 1M-Context API Skill

Use this skill whenever configuring an OpenClaw agent, coding CLI, or self-hosted daemon to connect to **bf16.ai** (`https://api.bf16.ai`).

## Endpoints & Protocols

- **OpenAI Chat Completions**: `https://api.bf16.ai/v1/chat/completions` (`baseURL = https://api.bf16.ai/v1`)
- **OpenAI Responses API** (Codex CLI): `https://api.bf16.ai/v1/responses` (`baseURL = https://api.bf16.ai/v1`)
- **Anthropic Messages API** (Claude Code): `https://api.bf16.ai/v1/messages` (`ANTHROPIC_BASE_URL = https://api.bf16.ai`, **no `/v1` suffix**)
- **Live Model Discovery**: `GET https://api.bf16.ai/v1/models`

## Recommended Model Routing

1. **Interactive Coding & Agent Loops (`$0.28 in / $0.055 cached / $1.12 out`)**: `deepseek/deepseek-v4.1-flash-uncensored-fast`
2. **24/7 Subagents, Cron Daemons & High-Volume Loops (`$0.26 in / $0.045 cached / $1.00 out`)**: `deepseek/deepseek-v4.1-flash-uncensored`
3. **Structured JSON & Browser-Use Vision (`$0.30 in / $0.065 cached / $1.12 out`)**: `zai-org/glm-5.3-flash-uncensored`
4. **Flagship Refactoring (`$1.35 in / $0.25 cached / $4.20 out`)**: `zai-org/glm-5.3-uncensored`
5. **2.8T Multimodal Architecture & Deep Audits (`$1.95 in / $0.28 cached / $6.90 out`)**: `moonshotai/kimi-k3.1-pro-uncensored`

## Quick OpenClaw Setup

```bash
export BF16_API_KEY="sk-bf16-v1-..."
bash scripts/configure-openclaw.sh
```

## Quick Claude Code Setup

```bash
env -u ANTHROPIC_API_KEY \
  ANTHROPIC_BASE_URL="https://api.bf16.ai" \
  ANTHROPIC_AUTH_TOKEN="$BF16_API_KEY" \
  ANTHROPIC_MODEL="deepseek/deepseek-v4.1-flash-uncensored-fast" \
  ANTHROPIC_DEFAULT_OPUS_MODEL="moonshotai/kimi-k3.1-pro-uncensored" \
  ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek/deepseek-v4.1-flash-uncensored" \
  CLAUDE_CODE_SUBAGENT_MODEL="deepseek/deepseek-v4.1-flash-uncensored" \
  claude
```

## Guardrails

- Mint a dedicated API key per daemon host at https://bf16.ai/dashboard/keys with an explicit daily USD spend cap.
- Keep local approval gates enabled for external messages, financial actions, and destructive shell commands.
