---
name: dataify-agent-onboarding
description: "Set up and verify a first Dataify workflow, then route the user to MCP, local skills, or REST without losing their original task. Use for first-time setup, installation, authentication, or choosing an integration path. Do not use for an already-configured search or scraping request."
metadata:
  author: Dataify
  version: "1.1.1"
  documentation: https://doc.dataify.com
  support: https://www.dataify.com/
---

# Dataify Agent Onboarding

Help a new user reach one successful Dataify action. Preserve the original goal: diagnose the environment, recommend one access path, resolve only the blocking setup issue, then continue the goal.

## Workflow

1. Run `scripts/onboard.py --goal "<user goal>" --json`.
2. If credentials are configured, route immediately to the recommended capability.
3. If credentials are missing, show only the setup command for the detected platform. Never ask for the value in chat.
4. Use MCP for an MCP-compatible client, a specific Skill for an agent session, and REST only when the user is integrating code without either runtime.
5. After setup, use `--verify` to distinguish present, ready, invalid credentials, insufficient balance, rate limiting and service/network failure. Continue the original task only after a real readiness success.

Read [access-paths.md](references/access-paths.md) only when two access paths are genuinely plausible.

Use `--verify` when the user wants a real readiness check. Optional product diagnostics are local-only and disabled by default; setting `DATAIFY_TELEMETRY_FILE` records allowlisted status events without queries, URLs, output, or credentials.

## Quick Start

```bash
python3 scripts/onboard.py --goal "research competitors with current web data" --verify --json
```

## Parameter interaction policy

- For a clear, low-risk, read-only, and low-cost request, apply safe defaults and execute immediately. A short execution summary is optional; do not pause for confirmation.
- Ask only for a missing required input, a material ambiguity, a high-volume or multi-page scope, a media download, a choice that materially changes credit usage, an irreversible action, or an explicit user request to review parameters.
- When confirmation is required, show only user-facing values that affect the target, scope, output, or cost. Prefer one concise sentence; use a compact table only when three or more consequential values are easier to compare.
- Never show fixed fields, empty optional fields, unchanged defaults, credentials, or internal implementation parameters such as engine selectors, response-format flags, offsets, spider IDs, and file-name templates.
- Keep advanced filters hidden unless the user asks for them or they are needed to resolve ambiguity. Never substitute documentation example values for missing required user input.
- After returning results, offer relevant refinements instead of forcing all optional decisions before the first result.

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
