---
name: aixplain-agent-builder
description: Design and deploy aiXplain agents with conservative defaults, read-only discovery first, and explicit approval gates for higher-risk actions.
---

# aiXplain Agent Builder

Use this skill to plan, inspect, and build aiXplain agents with conservative defaults, read-only discovery first, and explicit approval gates for higher-risk actions.

## Default Operating Mode

Start in **read-only planning mode**.

Until the user explicitly approves a higher-risk step, do not:

- install or upgrade packages
- request sensitive values in chat when existing environment configuration should be used
- upload local files to remote storage
- create authenticated integration tools
- enable write actions on integrations
- create runtime-execution tools or custom script-backed tools
- bypass standard SDK or platform flows with direct export calls

If the user wants execution or deployment, confirm that the required environment is already configured. Do not auto-fix the environment.

## Supported Commands

- **Plan agent**: define the agent goal, tool strategy, and approval gates
- **Inspect marketplace**: search existing tools, models, or integrations before proposing custom work
- **Build approved agent**: create an agent only after the user approves the plan
- **Debug existing agent**: inspect configuration, traces, and tool choices without widening permissions

## Workflow

### 1. Plan First

Before building anything, present a short plan covering:

- agent name
- description
- instructions
- expected inputs and outputs
- proposed tools or integrations
- whether each tool is read-only or write-capable
- which steps require approval

Wait for approval before creating or updating an agent.

### 2. Search Before Hardcoding

Always search for existing marketplace assets before proposing a new tool or integration.

```python
import os
from aixplain import Aixplain

aix = Aixplain(api_key=os.getenv("AIXPLAIN_API_KEY"))

tool_results = aix.Tool.search(query="web search").results
integration_results = aix.Integration.search(query="google drive").results
model_results = aix.Model.search(query="gpt").results
```

Do not say a capability is unavailable until you have searched for it.

### 3. Prefer Existing Read-Only Assets

Use this order of preference:

1. Existing marketplace tool
2. Existing integration with a non-empty least-privilege read-only action set
3. Custom or write-capable setup only after explicit approval

Treat these as higher-risk and require approval before proposing them:

- authenticated integrations
- remote file uploads
- database write actions
- runtime code tools
- custom script-backed tools

See `references/safety-gates.md`.

### 4. Build Only After Approval

When the user approves the plan, build the agent with the smallest necessary surface area.

```python
import os
from aixplain import Aixplain

aix = Aixplain(api_key=os.getenv("AIXPLAIN_API_KEY"))
search_tool = aix.Tool.get("<PUBLIC_TOOL_ID>")

agent = aix.Agent(
    name="My Agent",
    description="Summarizes and answers with linked sources.",
    instructions="Use only attached tools. If a request needs missing access, say so clearly.",
    tools=[search_tool],
    output_format="markdown",
    max_tokens=4000,
).save()
```

Do not specify a custom `llm` unless the user explicitly asks for one.

### 4.1 Integration File Handling

Do not upload local files by default when configuring integrations such as:

- aiR Knowledge Base
- SQLite and other DB-style integrations
- Python Sandbox

Preferred behavior:

- pass the local file path directly when the integration accepts file-backed config during connect or build
- use file upload only when calling `.run()` and the runtime input itself must be a file asset

Practical rule:

- setup time: prefer direct local file paths
- runtime: upload only if the specific `.run()` input requires a remote file reference

If a backend rejects the direct file path, report the backend-specific validation clearly instead of treating upload as the default first step.

### 4.2 OAuth Integration Behavior

For OAuth-based integrations, a newly created tool may be created successfully but remain unusable until the connection flow is completed.

Treat this as the normal flow:

- create the tool
- capture and return `redirect_url`
- tell the user the tool is not runnable yet
- wait for the user to complete the connection flow
- only then run the tool

Treat the presence of `redirect_url` as the expected pending-auth state.

Typical pattern:

```python
tool = integration.connect(name="My OAuth Tool")

if getattr(tool, "redirect_url", None):
    print(tool.redirect_url)
    # User must complete OAuth before the tool is runnable.
```

Before the connection flow is completed, report the tool as pending and provide the `redirect_url`.

### 5. Deployment and Debugging

After a successful save, share only the standard Studio links:

- Visual builder: `https://studio.aixplain.com/build/<AGENT_ID>/schema`
- Analytics: `https://studio.aixplain.com/dashboard/analytics/?agent=<AGENT_ID>`

For debugging, prefer SDK-visible agent configuration, run output, and Studio traces before proposing tool changes.

For detailed execution tracing during SDK runs, prefer:

```python
result = agent.run(
    query="...",
    progress_verbosity=3,
)
```

Observed behavior in this environment:

- `progress_verbosity=3` works with the installed aiXplain v2 agent path
- it returns full step traces, including model thoughts, tool calls, tool inputs, and tool outputs
- depending on SDK or shell buffering, the trace may appear in the final returned payload rather than as truly incremental live stdout

Use this for debugging or verification runs when you need the exact search, tool, and output trace.

## References

- `references/safety-gates.md` - approval rules for risky actions
- `references/read-only-patterns.md` - safe search and build examples
