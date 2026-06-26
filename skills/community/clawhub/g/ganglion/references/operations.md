# Operational Procedures

## First-Time Setup

1. **Install Ganglion:**
   ```bash
   pip install ganglion
   ```

2. **Set your OpenAI API key:**
   ```bash
   export LLM_PROVIDER_API_KEY=sk-...
   ```

3. **Scaffold a project:**
   ```bash
   ganglion init ./my-subnet --subnet sn9 --netuid 9
   ```

4. **Edit config.py** with your subnet's metrics, tasks, output spec, and constraints.

5. **Verify the project loads:**
   ```bash
   ganglion status ./my-subnet
   ```

6. **Run the pipeline:**
   ```bash
   ganglion run ./my-subnet
   ```

## Starting and Stopping

### Local Mode
Local mode requires no persistent server. Each command loads the project, executes, and exits.

```bash
# Set convenience variable
export GANGLION_PROJECT=./my-subnet

# Run commands directly
ganglion status $GANGLION_PROJECT
ganglion run $GANGLION_PROJECT
```

### Remote Mode (HTTP Bridge)

**Start:**
```bash
ganglion serve ./my-subnet --bot-id alpha --port 8899 &
export GANGLION_URL=http://127.0.0.1:8899
```

**Verify it's running:**
```bash
# Health check (liveness)
curl -s "$GANGLION_URL/healthz" | jq

# Readiness check
curl -s "$GANGLION_URL/readyz" | jq

# Full status
curl -s "$GANGLION_URL/v1/status" | jq .data.running
```

**Stop:**
Kill the server process (Ctrl+C or `kill` the PID). There is no graceful shutdown endpoint — if a pipeline is running, it will be interrupted.

## Checking Health and Status

### Local Mode
```bash
ganglion status ./my-subnet
```

### Remote Mode
```bash
# Full status
curl -s "$GANGLION_URL/v1/status" | jq

# Is a pipeline currently running?
curl -s "$GANGLION_URL/v1/status" | jq .data.running

# How many tools/agents are registered?
curl -s "$GANGLION_URL/v1/status" | jq '{tools: (.data.tools | length), agents: (.data.agents | length)}'

# Knowledge summary
curl -s "$GANGLION_URL/v1/knowledge" | jq .data.summary
```

### Using the Healthcheck Script
```bash
bash skills/ganglion/scripts/healthcheck.sh
```

## Viewing Run History and Metrics

```bash
# Last 5 runs (remote only — requires persistence backend)
curl -s "$GANGLION_URL/v1/runs?n=5" | jq

# All metrics
curl -s "$GANGLION_URL/v1/metrics" | jq

# Metrics for a specific experiment
curl -s "$GANGLION_URL/v1/metrics?experiment_id=exp_001" | jq

# Leaderboard
curl -s "$GANGLION_URL/v1/leaderboard" | jq
```

## Running Pipelines

### Full Pipeline
```bash
# Local
ganglion run ./my-subnet

# With overrides
ganglion run ./my-subnet --overrides '{"target_metric": "accuracy", "max_epochs": 50}'

# Remote
curl -s -X POST "$GANGLION_URL/v1/run/pipeline" \
  -H "Content-Type: application/json" \
  -d '{"overrides": {"target_metric": "accuracy"}}' | jq
```

### Single Stage
```bash
# Local
ganglion run ./my-subnet --stage plan

# Remote
curl -s -X POST "$GANGLION_URL/v1/run/stage/plan" \
  -H "Content-Type: application/json" \
  -d '{"context": {"model": "resnet18"}}' | jq
```

### Direct Experiment (Remote Only)
Bypass the pipeline and call the `run_experiment` tool directly:

```bash
curl -s -X POST "$GANGLION_URL/v1/run/experiment" \
  -H "Content-Type: application/json" \
  -d '{"config": {"learning_rate": 0.001, "epochs": 10}}' | jq
```

## Querying Knowledge

### View All Knowledge
```bash
# Local
ganglion knowledge ./my-subnet

# Remote
curl -s "$GANGLION_URL/v1/knowledge" | jq
```

### Filter by Capability
```bash
# Local
ganglion knowledge ./my-subnet --capability training --max-entries 10

# Remote
curl -s "$GANGLION_URL/v1/knowledge?capability=training&max_entries=10" | jq
```

### Multi-Bot Knowledge
```bash
# View knowledge tagged by a specific bot
ganglion knowledge ./my-subnet --bot-id alpha --capability training
```

## Registering Tools and Agents (Remote Only)

### Register a New Tool
```bash
curl -s -X POST "$GANGLION_URL/v1/tools" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_tool",
    "code": "from ganglion.composition.tool_registry import tool\nfrom ganglion.composition.tool_returns import ExperimentResult\n\n@tool(\"my_tool\", category=\"training\")\ndef my_tool(config: dict) -> ExperimentResult:\n    \"\"\"Run my custom experiment.\"\"\"\n    return ExperimentResult(content=\"done\", metrics={\"score\": 0.5})",
    "category": "training"
  }' | jq
```

### Register a New Agent
```bash
curl -s -X POST "$GANGLION_URL/v1/agents" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MyAgent",
    "code": "from ganglion.composition.base_agent import BaseAgentWrapper\nfrom ganglion.composition.tool_registry import build_toolset\n\nclass MyAgent(BaseAgentWrapper):\n    def build_system_prompt(self, task):\n        return \"You are a training agent.\"\n    def build_tools(self, task):\n        return build_toolset(\"my_tool\", \"finish\")"
  }' | jq
```

### Verify Registration
```bash
curl -s "$GANGLION_URL/v1/tools" | jq '.data[].name'
curl -s "$GANGLION_URL/v1/agents" | jq '.data[].name'
```

## Modifying the Pipeline (Remote Only)

### Add a Stage
```bash
curl -s -X PATCH "$GANGLION_URL/v1/pipeline" \
  -H "Content-Type: application/json" \
  -d '{
    "operations": [{
      "op": "add_stage",
      "stage": {
        "name": "validate",
        "agent": "Validator",
        "depends_on": ["train"],
        "input_keys": ["model_path"],
        "output_keys": ["validation"]
      }
    }]
  }' | jq
```

### Remove a Stage
```bash
curl -s -X PATCH "$GANGLION_URL/v1/pipeline" \
  -H "Content-Type: application/json" \
  -d '{"operations": [{"op": "remove_stage", "stage_name": "validate"}]}' | jq
```

### Update a Stage
```bash
curl -s -X PATCH "$GANGLION_URL/v1/pipeline" \
  -H "Content-Type: application/json" \
  -d '{
    "operations": [{
      "op": "update_stage",
      "stage_name": "train",
      "updates": {"agent": "NewTrainer", "is_optional": true}
    }]
  }' | jq
```

## Swapping Retry Policies (Remote Only)

```bash
# Swap policy for a specific stage
curl -s -X PUT "$GANGLION_URL/v1/policies/train" \
  -H "Content-Type: application/json" \
  -d '{"retry_policy": {"type": "escalating", "max_attempts": 5, "temperature_step": 0.1}}' | jq

# Swap the pipeline default policy
curl -s -X PUT "$GANGLION_URL/v1/policies/default" \
  -H "Content-Type: application/json" \
  -d '{"retry_policy": {"type": "fixed", "max_attempts": 3}}' | jq
```

## Rolling Back Mutations

```bash
# Undo the last mutation
curl -s -X POST "$GANGLION_URL/v1/rollback/last" | jq

# Undo all mutations (back to index 0)
curl -s -X POST "$GANGLION_URL/v1/rollback/0" | jq

# Check how many mutations exist
curl -s "$GANGLION_URL/v1/status" | jq .data.mutations
```

## Reading Project Source Files (Remote Only)

```bash
# Read a specific tool
curl -s "$GANGLION_URL/v1/source/tools/train.py" | jq .data.content -r

# Read config
curl -s "$GANGLION_URL/v1/source/config.py" | jq .data.content -r

# Read an agent
curl -s "$GANGLION_URL/v1/source/agents/explorer.py" | jq .data.content -r
```

## Multi-Bot Setup

### Same Machine (Filesystem Peer Discovery)

```bash
# Terminal 1
ganglion serve ./my-subnet --bot-id alpha --port 8899

# Terminal 2
ganglion serve ./my-subnet --bot-id beta --port 8900
```

Or local mode:
```bash
# Terminal 1
ganglion run ./my-subnet --bot-id alpha

# Terminal 2
ganglion run ./my-subnet --bot-id beta
```

Both bots read from and write to the same knowledge directory. Each bot's entries are tagged with its `bot_id`.

### Federated Setup (Different Hosts)

Configure the `FederatedKnowledgeBackend` in `config.py` — see configuration reference for details.

## Updating Prompts (Remote Only)

```bash
curl -s -X POST "$GANGLION_URL/v1/prompts" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "Planner",
    "prompt_section": "constraints",
    "content": "Focus on architectures with fewer than 10M parameters."
  }' | jq
```
