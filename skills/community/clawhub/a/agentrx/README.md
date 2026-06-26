# AgentRx OpenClaw Skill

Recovery infrastructure for AI agents. When your tool calls fail,
AgentRx tells you exactly what to do next.

## Installation

Copy this folder to your OpenClaw skills directory:
cp -r agentrx-openclaw ~/.openclaw/skills/agentrx

Or install via ClawHub once published:
npx clawhub install agentrx

## Configuration

Add these to ~/.openclaw/.env:
AGENTRX_API_KEY=your_api_key_here
AGENTRX_BASE_URL=https://agentrx-production.up.railway.app

Beta API key (free tier, rate limited):
AGENTRX_API_KEY=beta_openclaw_try_agentrx_2026

This shared key lets you test immediately. For a dedicated production
key with higher limits, email chainassetslab@gmail.com

## What It Does

Classifies tool failures into 10 signatures and returns a direct
plaintext instruction in openclaw_instruction telling the agent
exactly what to do next. No interpretation required.

Failure signatures: AGENT_LOOP, AUTH_FAILURE, RATE_LIMIT_EXCEEDED,
NETWORK_LATENCY, HALLUCINATED_PARAM, HALLUCINATED_VALUE,
SCHEMA_MISMATCH, RESOURCE_MISSING, TOOL_DEPRECATED, UNKNOWN

## Usage

After any tool failure:
bash scripts/recover.sh "agent_id" "tool_name" "error message" 0

Before risky tool calls:
bash scripts/preflight.sh "agent_id" "tool_name" '{"key":"val"}' '{}'

## Links

Live API: https://agentrx-production.up.railway.app/docs
PyPI SDK: https://pypi.org/project/agentrx-sdk
GitHub:   https://github.com/chainassetslab/agentrx
Contact:  chainassetslab@gmail.com
