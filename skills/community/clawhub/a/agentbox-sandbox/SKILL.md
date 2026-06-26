---
name: agentbox-clawhub
description: answer questions about agentbox cloud sandboxes using the official docs. use when the user wants help with agentbox quickstart, sandbox lifecycle, timeout, commands, filesystem read-write, environment variables, cli install or auth, python sdk usage, or custom sandbox templates.
---

# AgentBox ClawHub

Provide reliable AgentBox guidance based on the bundled summary of the official documentation.

## Response workflow

1. Identify whether the user is asking about:
   - quickstart
   - sandbox lifecycle or timeout
   - commands execution
   - filesystem read/write
   - environment variables or secrets
   - cli installation or authentication
   - python sdk usage
   - custom sandbox templates
2. Answer from `references/agentbox-official.md`.
3. Keep CLI and Python SDK paths separate. Do not mix them unless the user asks for both.
4. Prefer short, runnable examples.
5. If the user asks for something not covered by the bundled reference, say it is not documented in this skill and recommend checking the latest official docs.

## Core rules

- Do not invent undocumented methods, flags, or endpoints.
- Treat `agentbox.cloud/docs` as the source of truth for this skill.
- State units explicitly when talking about timeout values: seconds.
- Mention the default sandbox lifetime when relevant: 5 minutes unless the timeout is customized.
- For secrets, prefer per-command or per-run scoped environment variables over global variables when the task is a one-off.
- When the user asks how to create a custom sandbox, explain the Dockerfile-based template flow first.
- When the user asks how to run code or shell inside AgentBox, show `Sandbox(...).commands.run(...)` unless they specifically want another interface.

## Common answer patterns

### Quickstart

Use this structure:
- what to install
- how to authenticate or set API key
- minimal example
- one common next step

### Timeout or lifecycle

Use this structure:
- default behavior
- how to set timeout at creation
- how to extend or reset timeout later with `set_timeout`
- how to inspect start and end time with `get_info`

### Filesystem

Use this structure:
- read single file with `files.read`
- write single file with `files.write`
- warn that write overwrites existing content

### Environment variables

Use this structure:
- global envs at sandbox creation
- scoped envs for `run_code`
- scoped envs for `commands.run`
- recommend scoped envs for secrets

### Template creation

Use this structure:
- install CLI
- authenticate
- `agentbox template init`
- edit `agentbox.Dockerfile`
- `agentbox template build --platform linux_x86 -p YOUR_WORKPATH`
- start sandbox with the resulting template id

## Ready-to-adapt snippets

### Python SDK quickstart

```python
from agentbox import Sandbox

sandbox = Sandbox(
    api_key="ab_xxxxxxxxxxxxxxxxxxxxxxxxx",
    template="<YOUR_TEMPLATE_ID>",
    timeout=120,
)

result = sandbox.commands.run("ls -l")
print(result.stdout)
```

### Global environment variables

```python
from agentbox import Sandbox

sandbox = Sandbox(
    api_key="ab_xxxxxxxxxxxxxxxxxxxxxxxxx",
    template="<YOUR_TEMPLATE_ID>",
    timeout=60,
    envs={"MY_VAR": "my_value"},
)

result = sandbox.commands.run("echo $MY_VAR")
print(result.stdout)
```

### Scoped command environment variables

```python
result = sandbox.commands.run(
    "echo $MY_VAR",
    envs={"MY_VAR": "123"},
)
```

## Resources

- Official reference summary: `references/agentbox-official.md`
- ClawHub publish notes: `README.md`
