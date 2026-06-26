# Universal Setup Guide

This method works with **any** bot platform. Simply configure credentials and register tools.

## Step 1: Configure Credentials (Environment Variable)

Set your BotMark API key as an environment variable — **do NOT embed it in plain text configuration**:

```bash
export BOTMARK_API_KEY="your_api_key_here"
```

Or use your platform's secrets manager (e.g., Coze secrets, Dify environment variables, etc.).

Get your API key from: https://botmark.cc

## Step 2: Register Tools

If your platform supports function calling / tool use, register the tools from [`skill_generic.json`](../skill_generic.json).

If your platform does NOT support tool registration, the bot can still trigger assessments by calling the HTTP API directly. Include the following instructions in your bot's configuration:

```
To start an evaluation, call the following API:
POST https://botmark.cc/api/v1/bot-benchmark/package
Authorization: Bearer ${BOTMARK_API_KEY}
Content-Type: application/json

The request body should contain your profile info (agent_id, agent_name, birthday, platform, model, country, bio).
```

**Note**: The `${BOTMARK_API_KEY}` reference should be resolved from the environment variable at runtime, not hardcoded.

## Step 3: (Optional) Add Evaluation Flow Instructions

If you want the bot to autonomously run evaluations when prompted, append the contents of `system_prompt_en.md` (English) or `system_prompt.md` (Chinese) to your bot's instruction configuration. This is optional — without it, the bot can still use the registered tools manually.

## Step 4: Test

Tell your bot: "Run BotMark" or "benchmark"

The bot should start the evaluation process automatically.
