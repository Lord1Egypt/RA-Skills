# AgentPathfinder

Cryptographically signed audit trails for AI agent tool calls. Every tool invocation is HMAC-SHA256 signed. Full arguments and results logged.

## Installation

```bash
pip install agentpathfinder
```

## Quick Start

```bash
# Create a task
pf create deploy "test,build,push,restart"

# Check status
pf status <task-id>

# View audit trail
pf audit <task-id>
```

## SDK Usage

```python
from agentpathfinder import TaskEngine
from agentpathfinder.tool_audit import AuditedToolExecutor

task = TaskEngine()
task_id = task.create_task("deploy", [
    {"name": "test"},
    {"name": "build"},
    {"name": "push"},
    {"name": "restart"},
])

audit = task.get_tool_audit(task_id, step_number=1)
executor = AuditedToolExecutor(audit)

# Every command is automatically logged
result = executor.exec("pytest tests/ -v")

# Check for hanging calls
audit.detect_hanging_calls()
```

## CLI Reference

- `pf create <name> <steps>` — Create task (comma-separated steps)
- `pf status <task_id>` — Show task status
- `pf audit <task_id>` — Show audit trail
- `pf reset-step <task_id> <step>` — Reset failed step

## Development

```bash
python3 -m pytest tests/ -v
```

## License

MIT © CertainLogic
