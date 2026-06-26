# DimOS Quick Reference

## Concepts

- **Module**: a subsystem that can publish/subscribe to typed streams, expose RPC methods, and run in a DimOS worker process.
- **Stream**: a typed data channel declared with `In[T]` or `Out[T]`.
- **RPC**: a callable method exposed between modules, marked with `@rpc`.
- **Skill**: an agent-facing method marked with `@skill`. In DimOS, `@skill` also makes the method RPC-callable.
- **Blueprint**: a composition of modules. `autoconnect(...)` wires streams by matching `(name, type)`.
- **MCP server/client**: `McpServer` exposes skills as MCP tools; `McpClient` lets the agent call those tools.

## Skill rules

Use this shape for new skills:

```python
@skill
def my_action(self, arg: float) -> str:
    """Describe exactly when and how the agent should use this action.

    Args:
        arg: A short, concrete description of the parameter.
    """
    return "Action complete."
```

Checklist:

- `@skill` only; do not also add `@rpc` to the same method.
- Add a docstring because the agent sees it as the tool description.
- Type-annotate every skill parameter.
- Use simple JSON-compatible arguments.
- Return a clear `str` that says what happened or why the action was refused.
- Avoid hidden side effects. The result string should match the actual execution outcome.

## Blueprint patterns

Minimal MCP-enabled pattern:

```python
from dimos.agents.mcp.mcp_client import McpClient
from dimos.agents.mcp.mcp_server import McpServer
from dimos.core.coordination.blueprints import autoconnect

my_agentic_blueprint = autoconnect(
    # robot_stack(),
    McpServer.blueprint(),
    McpClient.blueprint(),
    # skill_container.blueprint(),
)
```

If multiple modules could satisfy a Spec, use blueprint remappings to make the dependency explicit.

## CLI workflow

```bash
# List runnable blueprints
dimos list

# Start a safe test environment
dimos --replay run unitree-go2-agentic --daemon
dimos --simulation run unitree-go2-agentic --daemon

# Check status and logs
dimos status
dimos log -n 100
dimos log -f

# MCP discovery and calls
dimos mcp list-tools
dimos mcp modules
dimos mcp status
dimos mcp call <tool_name> --arg key=value
dimos mcp call <tool_name> --json-args '{"key": "value"}'

# Talk to the agent
dimos agent-send "what tools are available?"

# Stop
dimos stop
```

## Common code-review issues

- Missing skill docstrings.
- Missing parameter annotations.
- Returning `None` from a skill.
- Using a Go2-specific prompt for a G1 humanoid stack.
- Calling MCP commands before starting a blueprint that includes `McpServer`.
- Hardcoding robot IPs, ports, API keys, file paths, or local-only assumptions.
- Adding real robot movement without conservative bounds and a dry-run/simulation path.

## Suggested test sequence

1. Syntax-check generated code.
2. Run unit tests for the edited package.
3. Start replay/simulation.
4. Confirm the new skill appears in `dimos mcp list-tools`.
5. Call the skill with safe arguments.
6. Watch logs.
7. Only then consider real hardware with local supervision and an accessible stop mechanism.
