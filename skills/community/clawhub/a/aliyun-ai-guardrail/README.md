# Aliyun AI Guardrail 

An OpenClaw Skill that installs and configures the AI Guardrail hook powered by Alibaba Cloud.

## Usage

After installing the skill, tell OpenClaw:

- "install aliyun-ai-guardrail"
- "configure aliyun-ai-guardrail"
- "set up aliyun-ai-guardrail"

The skill will automatically:

1. Copy the built-in hook package to a temp directory, run `npm install`, and install it via `openclaw hooks install`
2. Prompt you for your Alibaba Cloud AccessKey ID and AccessKey Secret
3. Write the AKSK to the environment variable config in `openclaw.json`
4. Remind you to restart the Gateway for the config to take effect

## How the Hook Works

The hook is mounted on the `agent:bootstrap` event, automatically enabled for all agent sessions. It performs real-time security checks on user messages sent to the LLM. Messages that trigger interception rules are replaced with a safety prompt. Detection results are cached so historical messages won't trigger duplicate API calls. API calls have a 1-second timeout and will pass through on timeout.

