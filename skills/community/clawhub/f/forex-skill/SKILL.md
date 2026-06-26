# Forex VSA & PVA Analysis Agent

## Overview
This OpenClaw agent is designed to automate Forex market analysis using Volume Spread Analysis (VSA) and Price Volume Analysis (PVA). It integrates with OpenRouter to process market sentiment and technical data.

## Features
- **Volume Spread Analysis:** Detects professional "smart money" activity by analyzing price spreads and volume.
- **PVA Filters:** Identifies climax volume and high-volume churn candles.
- **OpenClaw Integration:** Utilizes the latest 2026 agent framework for real-time position management.
- **Multi-Model Support:** Configured to work with high-context LLMs via OpenRouter and TypingMind.

## Configuration
The agent requires a valid OpenClaw configuration key. Ensure your `config.json` uses the `key` field rather than `apiKey` for compatibility with v0.15.0.

## Installation
Once synced, this skill can be deployed directly into your OpenClaw environment to begin monitoring currency pairs for VSA setups.# Forex Skill

