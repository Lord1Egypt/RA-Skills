# Installation and activation

## Install from ClawHub
```bash
clawhub install dr-api-execution-bootstrap --workdir /home/Echo/.openclaw/workspace --force
```

## Apply in a workspace
Tell the agent:

```text
Apply dr-api-execution-bootstrap to this workspace.
```

## Recommended bootstrap prompt for another agent
```text
You are my API execution agent.
Apply dr-api-execution-bootstrap to this workspace and persist its rules in startup memory.
Use direct in-session API execution by default.
Do not spawn subagents unless I explicitly ask.
Use fast mode single-run chain.
Do one upfront preflight only: token, app code/function key, and one sanity endpoint.
After preflight, execute the full API chain continuously.
Keep responses concise and do not narrate every API call unless I ask.
For write operations, show one concise batch preview and wait for approval.
Then validate with a minimal real test and report either:
Configured and validated
or
Configured, but blocked by: <reason>
```

## What success looks like
- agent runs API calls directly in the current session
- no subagent fallback by default
- one preflight only, then continuous execution
- concise outputs
- predictable approval behavior for writes
