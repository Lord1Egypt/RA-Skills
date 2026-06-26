# Troubleshooting

## Startup Errors

### FileNotFoundError: No config.py found

**Cause:** The project directory path is wrong or `config.py` doesn't exist.

**Fix:**
```bash
# Verify the path
ls -la ./my-subnet/config.py

# If no project exists, scaffold one
ganglion init ./my-subnet --subnet generic
```

### ValueError: config.py must define 'subnet_config'

**Cause:** `config.py` exists but doesn't export a `subnet_config` variable.

**Fix:** Ensure `config.py` contains:
```python
subnet_config = SubnetConfig(...)
```

### ValueError: config.py must define 'pipeline'

**Cause:** `config.py` exists but doesn't export a `pipeline` variable.

**Fix:** Ensure `config.py` contains:
```python
pipeline = PipelineDef(...)
```

### ImportError: Could not load config

**Cause:** `config.py` has a syntax error or imports a missing module.

**Fix:**
```bash
python3 -c "import importlib.util; spec = importlib.util.spec_from_file_location('c', './my-subnet/config.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)"
```
This will show the actual import/syntax error.

### ImportError: openai package is required

**Cause:** The `openai` Python package is not installed.

**Fix:**
```bash
pip install openai>=1.0
# or reinstall ganglion with all deps
pip install ganglion
```

---

## API Key & LLM Errors

### OpenAI AuthenticationError / Invalid API key

**Cause:** `LLM_PROVIDER_API_KEY` is not set, empty, or invalid.

**Fix:**
```bash
export LLM_PROVIDER_API_KEY=sk-...
# Verify it's set
echo $LLM_PROVIDER_API_KEY | head -c 10
```

### RateLimitError during pipeline execution

**Cause:** OpenAI API rate limit exceeded. The LLM client retries automatically with exponential backoff (up to 5 retries, max 60s delay).

**If retries exhaust:**
- Wait a few minutes and retry
- Switch to a model with higher rate limits
- Reduce pipeline concurrency

### APIConnectionError

**Cause:** Network issue reaching the LLM API.

**Fix:**
- Check network connectivity
- If using a custom `base_url`, verify it's reachable
- The client retries automatically — transient issues usually resolve

---

## Pipeline Errors

### PipelineValidationError: Dependency graph contains a cycle

**Cause:** Stage dependencies form a circular chain (e.g., A depends on B, B depends on A).

**Fix:**
```bash
# View the pipeline to find the cycle
ganglion pipeline ./my-subnet
# or
curl -s "$GANGLION_URL/v1/pipeline" | jq '.data.stages[] | {name, depends_on}'
```
Remove or restructure the circular dependency.

### PipelineValidationError: Stage 'X' depends on 'Y' which does not exist

**Cause:** A stage's `depends_on` references a non-existent stage name.

**Fix:** Check stage names and dependencies in `config.py` or use `PATCH /pipeline` to fix.

### PipelineValidationError: input_key 'X' not produced by any upstream stage

**Cause:** A stage declares `input_keys` that no upstream stage produces in its `output_keys`.

**Fix:** Add the missing key to an upstream stage's `output_keys`, or remove it from `input_keys`.

### Stage failed: Agent 'X' not found in registry

**Cause:** A pipeline stage references an agent class that isn't registered. Either the file is missing from `agents/`, has a syntax error, or the class name doesn't match.

**Fix:**
```bash
# Check registered agents
ganglion agents ./my-subnet

# Check the agents directory
ls ./my-subnet/agents/
```

### Max turns reached without calling finish()

**Cause:** The agent looped for 50 turns without completing. It may be stuck, confused, or the tools aren't returning useful results.

**Fix:**
- Review the agent's system prompt — is it clear about when to call `finish()`?
- Review the tools — are they returning actionable information?
- Increase `max_turns` if the task genuinely needs more iterations
- Use EscalatingRetry to inject stall-breaking prompts

---

## Mutation Errors

### ConcurrentMutationError: Cannot mutate during a pipeline run

**Cause:** You tried to register a tool, agent, or patch the pipeline while a pipeline is executing.

**Fix:** Wait for the current run to complete, then retry the mutation.

```bash
# Check if a run is in progress
curl -s "$GANGLION_URL/v1/status" | jq .data.running
```

### Tool validation failed: No @tool decorator found

**Cause:** The tool code submitted via `POST /tools` doesn't contain a `@tool(...)` decorator.

**Fix:** Ensure the code follows the required pattern:
```python
from ganglion.composition.tool_registry import tool

@tool("my_tool", category="training")
def my_tool(param: str) -> ...:
    """Docstring is required."""
    ...
```

### Tool validation failed: Parameter 'X' missing type hint

**Cause:** A tool function parameter doesn't have a type annotation.

**Fix:** Add type hints to all parameters: `def my_tool(x: int, y: str = "default")`.

### Tool validation failed: Blocked import

**Cause:** The tool code uses a blocked import (`subprocess`, `os.system`, `shutil.rmtree`, `socket`, `http.server`).

**Fix:** Remove the blocked import. These are blocked for safety — tools run in the same process.

### Agent validation failed: Missing build_system_prompt / build_tools

**Cause:** The agent class doesn't implement the required methods.

**Fix:** Ensure the agent class inherits from `BaseAgentWrapper` and implements both `build_system_prompt(self, task)` and `build_tools(self, task)`.

### PipelineOperationError: Stage 'X' already exists

**Cause:** Tried to add a stage with a name that's already in the pipeline.

**Fix:** Use `update_stage` instead, or choose a different name.

---

## Knowledge Store Errors

### Empty knowledge (no patterns or antipatterns)

**Cause:** Either no runs have completed yet, or the `knowledge` object isn't defined in `config.py`.

**Fix:**
```bash
# Check if knowledge is configured
ganglion status ./my-subnet | python3 -c "import sys,json; d=json.load(sys.stdin); print('knowledge:', d.get('knowledge'))"
```
If `null`, add a `knowledge = KnowledgeStore(...)` to `config.py`.

### Knowledge not compounding across runs

**Cause:** The knowledge store is configured but the backend directory doesn't persist between runs, or different paths are used.

**Fix:** Verify the knowledge backend directory exists and is the same path across runs:
```bash
ls ./my-subnet/knowledge/
cat ./my-subnet/knowledge/patterns.json | python3 -m json.tool | head -20
```

---

## Rollback Errors

### No mutations to rollback

**Cause:** The mutation log is empty — either no mutations have been made, or the server was restarted (mutations are in-memory only).

**Fix:** This is expected after a server restart. Mutation history does not persist across restarts.

---

## Connection & Network Errors

### Connection refused when calling the HTTP bridge

**Cause:** The bridge server isn't running, or it's on a different host/port.

**Fix:**
```bash
# Check if the server is running
curl -s http://127.0.0.1:8899/v1/status | jq

# Try with the correct host/port
curl -s http://<host>:<port>/v1/status | jq
```

### Server returns 500: Bridge not configured

**Cause:** Internal error — `configure()` was not called before the server started handling requests. This shouldn't happen with normal `ganglion serve` usage.

**Fix:** This indicates a bug or a custom startup script that skipped configuration. Use `ganglion serve` directly.

---

## Tool Loading Warnings

### "Failed to load tool from X.py"

**Cause:** A Python file in `tools/` has a syntax error, missing import, or doesn't contain a `@tool` decorated function. Logged as a warning — other tools still load.

**Fix:**
```bash
# Test the file directly
python3 -c "exec(open('./my-subnet/tools/problem_file.py').read())"
```

### "Failed to load agent from X.py"

**Cause:** A Python file in `agents/` has a syntax error or doesn't contain a `BaseAgentWrapper` subclass.

**Fix:** Same approach — test the file directly with Python.

---

## Getting Diagnostic Information

When reporting issues, gather:

```bash
# Python version
python3 --version

# Ganglion version
pip show ganglion

# Full status dump
ganglion status ./my-subnet 2>&1

# List of files in project
ls -R ./my-subnet/

# Config file contents
cat ./my-subnet/config.py

# Recent knowledge
ganglion knowledge ./my-subnet --max-entries 5 2>&1
```
