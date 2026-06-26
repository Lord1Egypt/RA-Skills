# AWP Platform Adapter: Standalone (awp-protocol)

This adapter generates `agent.py` files for the **AWP standalone runtime**
included in the `awp-protocol` package.

## When to Use

Use this adapter when:
- You want to run AWP workflows without installing any external agent framework
- You are prototyping or testing a workflow
- You want the simplest possible setup

## agent.py Template

For each agent, generate this `agent.py`:

```python
from __future__ import annotations

from typing import Any, Dict

from awp.agent import AWPAgent


class Agent(AWPAgent):
    """AWP agent: {{AGENT_ID}}."""

    @property
    def name(self) -> str:
        return "{{AGENT_ID}}"

    def run(self, task: str, state: Dict[str, Any]) -> Dict[str, Any]:
        state = state or {}
        return {self.name: {"result": "default", "confidence": 0.0}}
```

## How Execution Works

The standalone runtime (`awp.runtime.WorkflowRunner`) does NOT call `agent.py`
directly.  Instead, it:

1. Reads `agent.awp.yaml` for configuration
2. Loads prompts from `workflow/instructions/SYSTEM_PROMPT.md`
3. Loads user prompt from `workflow/prompt/00_INTRO.md`
4. Builds context from previous agent outputs in state
5. Calls the LLM via an OpenAI-compatible API
6. Parses the response as JSON matching `output_schema.json`
7. Returns `{agent_id: parsed_result}`

The `agent.py` file serves as:
- A class definition that other platforms can import
- A place for custom agent logic (override `run()` if needed)
- A marker file for AWP validation (R11)

## Running a Workflow

```python
from awp.runtime import WorkflowRunner

runner = WorkflowRunner("path/to/my-workflow")
result = runner.run("Analyze the quarterly report")
print(result)
```

Or via CLI:

```bash
awp run path/to/my-workflow --task "Analyze the quarterly report"
```

## Custom Agent Logic

If you need logic beyond the standard prompt-LLM-parse cycle, override `run()`:

```python
from awp.agent import AWPAgent
from awp.runtime.agent import StandaloneAgent


class Agent(AWPAgent):
    @property
    def name(self) -> str:
        return "{{AGENT_ID}}"

    def run(self, task: str, state: dict) -> dict:
        # Use StandaloneAgent for LLM calls
        from pathlib import Path
        sa = StandaloneAgent(Path(__file__).parent, Path(__file__).parents[2])
        base_result = sa.run(task, state)

        # Custom post-processing
        result = base_result[self.name]
        result["custom_field"] = "enriched"

        return {self.name: result}
```

## Dependencies

```
pip install awp-protocol
```

Environment variables for LLM access:
```bash
export LLM_API_KEY=sk-...          # API key
export LLM_MODEL=provider/model    # Model identifier
export LLM_BASE_URL=https://...    # API endpoint (default: OpenRouter)
```
