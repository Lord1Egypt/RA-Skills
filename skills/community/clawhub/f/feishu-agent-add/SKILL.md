---
name: feishu-agent-add
description: Use this skill when users want to add a Feishu agent for OpenClaw, especially when they say things like “帮我增加一个名字叫xxx，用来做xxx的飞书agent”, want a guided prompt flow, or want a one-command way to generate the matching OpenClaw config.
license: MIT
---

# feishu-agent-add

This skill is the conversational front end for the local script `scripts/add_feishu_agent.py`.

This project is designed for OpenClaw users, but the skill name intentionally stays short: `feishu-agent-add`.

## When To Use

Use this skill when the user wants to:

- add a new Feishu-connected OpenClaw agent
- avoid hand-editing `openclaw.json`
- configure a new agent through a few follow-up questions
- get a ready-to-run one-line command for advanced usage

## Core Rule

Do not hand-edit `openclaw.json` unless the user explicitly asks for manual fallback.

Prefer running:

```bash
python3 scripts/add_feishu_agent.py ...
```

The script is the execution core. This skill should mainly:

1. understand the user's request
2. ask only for missing required fields
3. preview the plan
4. run the script
5. summarize the result and next steps

## Required Inputs

Collect these fields before execution:

- `agent_name`
- `purpose`
- `agent_id`
  - if missing, propose one derived from the name
- `app_id`
- `app_secret`

These can use defaults unless the user says otherwise:

- `workspace_path`
  - default: `~/.openclaw/workspace-{agent_id}`
- `model`
  - default: inherit from the current OpenClaw config
- `enable_agent_to_agent`
  - default: `true`
- `workspace_mode`
  - default: `auto`
- `init_templates`
  - default: `true`

## Conversational Flow

### 1. Parse what the user already gave

For a request like:

> 帮我增加一个名字叫小红书运营，用来做内容选题和文案生成的飞书agent

extract:

- `agent_name = 小红书运营`
- `purpose = 内容选题和文案生成`
- `agent_id = xiaohongshu` or another short slug candidate

If `agent_id` is missing, propose one instead of asking an open-ended question.

### 2. Ask the minimum follow-up questions

Only ask for the missing required fields. Prefer one compact message.

Typical follow-up:

- proposed `agent_id`
- Feishu `App ID`
- Feishu `App Secret`

Only ask about optional fields if the user indicates they care.

### 3. Preview before execution

Before running the script, summarize:

- agent name
- agent id
- purpose
- workspace path
- whether agent-to-agent collaboration will be enabled

### 4. Run the script

Run from the skill directory:

```bash
python3 scripts/add_feishu_agent.py \
  --agent-id <agent-id> \
  --agent-name "<agent-name>" \
  --purpose "<purpose>" \
  --app-id <app-id> \
  --app-secret <app-secret> \
  --json-output \
  --yes
```

Add optional flags only when needed:

- `--model <model>`
- `--workspace-path <path>`
- `--disable-agent-to-agent`
- `--workspace-mode cli|mkdir|auto`
- `--no-init-templates`
- `--dry-run`

## Advanced User Mode

If the user prefers a single terminal command, give them a ready-to-run example instead of a manual JSON recipe.

Use this pattern:

```bash
python3 scripts/add_feishu_agent.py \
  --agent-id trader \
  --agent-name "交易小助手" \
  --purpose "股票和 ETF 分析" \
  --app-id cli_xxx \
  --app-secret secret_xxx \
  --yes
```

## Output Expectations

After execution, summarize:

- whether config was written successfully
- the workspace path
- whether starter files were initialized
- that OpenClaw should be restarted
- where to refine the agent identity, usually `SOUL.md`

If the script fails, report the concrete reason and do not improvise partial manual edits unless the user asks for that fallback.

## Notes

- The script already handles validation, backup, and config updates.
- Prefer `--dry-run` first when the user asks for a preview.
- If the user asks how to install or use this project, point them to `README.md`.
