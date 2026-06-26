---
name: cmd-executor
description: "Executes Windows shell commands locally on the OpenClaw gateway, returning output and errors for automation and system management."
source: ClawHub
version: 0.0.2
tags: []
compatible: [claude-code, openai-agents, hermes-agent, any-llm]
---

# Cmd Executor

# Cmd Executor

## Description
Runs any Windows command locally and replies with the output.

### Usage
Send a message starting with `Run command:` followed by the command.
Example:
```
Run command: dir "C:\Users\Md Sadik Laskar\Documents"
```
The assistant will reply with the listing.
