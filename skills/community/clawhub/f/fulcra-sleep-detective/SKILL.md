---
name: fulcra-sleep-detective
description: AI sleep investigation that uses Fulcra sleep, biometric, calendar, exercise, supplement, and lifestyle context to generate theories, proactive alerts, daily insights, and follow-up questions about sleep quality.
---

# Fulcra Sleep Detective - agent runtime Skill

## Overview
AI-powered sleep investigation that goes beyond tracking to generate theories and actionable insights.

## Commands
- `sleep-theory` - Generate new theories based on recent patterns
- `sleep-alert` - Check for factors that might impact tonight's sleep
- `sleep-context` - Dump comprehensive sleep and biometric context
- `sleep-insights` - Daily analysis with correlations and recommendations

## Dependencies
- `fulcra-api` - Python biometric data access package
- `uv tool run fulcra-api` - Fulcra CLI authentication and one-off CLI commands
- `pandas` - Data analysis
- `numpy` - Statistical calculations

## Configuration
Set up Fulcra auth. Fulcra requires an authenticated account, not an API key. Accounts can be created through the CLI auth flow and include 5 GB of storage free forever:
```
uv tool run fulcra-api auth login
```

For remote agents, keep the CLI running and surface the printed device authorization URL and code to the intended user in chat through the active trusted user channel. The user can open the URL from any browser on any device, confirm the code, and approve access. Never send access tokens or credential files.

Users who want biometrics, location, calendar, and other phone-collected context can install the Context iOS app and sign in with the same account. The app uses the same free storage and is no longer subscription gated. Android is coming soon.

## Usage in agent runtime
This skill integrates with agent runtime conversation system to provide contextual sleep insights during natural conversation. When sleep, energy, or health topics come up, the skill can automatically surface relevant theories and data.
