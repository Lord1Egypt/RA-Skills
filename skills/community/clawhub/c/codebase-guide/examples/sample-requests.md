# Sample API Requests & Responses

All examples use `GANGLION_URL=http://127.0.0.1:8899`.

## Observation

### Get Full Status
```bash
curl -s "$GANGLION_URL/v1/status" | jq
```
```json
{
  "data": {
    "subnet": {
      "netuid": 9,
    "name": "SN9 Pretrain",
    "metrics": [{"name": "loss", "direction": "minimize", "weight": 1.0, "description": "Cross-entropy loss"}],
    "tasks": {"pretrain": {"name": "pretrain", "weight": 1.0, "metadata": {}}},
    "output_spec": {"format": "huggingface_model", "shape_constraints": {}, "description": "A pretrained language model"},
    "constraints": {"max_gpu_hours": 24}
  },
  "pipeline": {
    "name": "sn9-pipeline",
    "stages": [
      {"name": "plan", "agent": "Planner", "depends_on": [], "input_keys": [], "output_keys": ["plan"]},
      {"name": "train", "agent": "Trainer", "depends_on": ["plan"], "input_keys": ["plan"], "output_keys": ["model_path", "metrics"]}
    ],
    "default_retry": "FixedRetry(max_attempts=3)"
  },
  "tools": [
    {"name": "run_experiment", "description": "Run a training experiment", "category": "training"}
  ],
  "agents": [
    {"name": "Planner", "module": "planner"},
    {"name": "Trainer", "module": "trainer"}
  ],
  "knowledge": {"patterns": 12, "antipatterns": 5},
    "mutations": 0,
    "running": false
  }
}
```

### List Tools (Filtered)
```bash
curl -s "$GANGLION_URL/v1/tools?category=training" | jq
```
```json
{
  "data": [
    {
      "name": "run_experiment",
      "description": "Run a training experiment with the given config.",
      "category": "training",
      "parameters": {
        "type": "object",
        "properties": {
          "config": {"type": "object"}
        },
        "required": ["config"]
      }
    }
  ]
}
```

### Get Knowledge (Filtered)
```bash
curl -s "$GANGLION_URL/v1/knowledge?capability=training&max_entries=3" | jq
```
```json
{
  "data": {
    "patterns": [
      {
        "capability": "training",
      "description": "Conv+Gaussian head achieved best CRPS",
      "config": {"architecture": "conv_gaussian", "lr": 0.001},
      "metric_value": 0.85,
      "metric_name": "crps",
      "stage": "train",
      "timestamp": "2026-03-04T10:30:00",
      "source_bot": "alpha"
    }
  ],
  "antipatterns": [
    {
      "capability": "training",
      "error_summary": "LSTM diverged after 100 epochs",
      "config": {"architecture": "lstm", "lr": 0.01},
      "failure_mode": "numerical_instability",
      "stage": "train",
      "timestamp": "2026-03-04T09:15:00",
      "source_bot": "alpha"
    }
  ],
    "summary": {"patterns": 12, "antipatterns": 5}
  }
}
```

### Read Source File
```bash
curl -s "$GANGLION_URL/v1/source/tools/run_experiment.py" | jq .data.content -r
```
```python
from ganglion.composition.tool_registry import tool
from ganglion.composition.tool_returns import ExperimentResult

@tool("run_experiment", category="training")
def run_experiment(config: dict) -> ExperimentResult:
    """Run a training experiment with the given config."""
    return ExperimentResult(
        content=f"Experiment completed with config: {config}",
        experiment_id="exp-001",
        metrics={"score": 0.0},
    )
```

### Get Run History
```bash
curl -s "$GANGLION_URL/v1/runs?n=3" | jq
```
```json
{
  "data": [
    {
      "success": true,
      "failed_stage": null,
      "results": {"plan": {"success": true, "attempts": 1}, "train": {"success": true, "attempts": 2}}
    }
  ]
}
```

---

## Execution

### Run Full Pipeline
```bash
curl -s -X POST "$GANGLION_URL/v1/run/pipeline" \
  -H "Content-Type: application/json" \
  -d '{"overrides": {"target_metric": "accuracy"}}' | jq
```
```json
{
  "data": {
    "success": true,
    "failed_stage": null,
    "reason": null,
    "results": {
      "plan": {"success": true, "attempts": 1, "error": null, "structured": {"plan": "..."}},
      "train": {"success": true, "attempts": 2, "error": null, "structured": {"metrics": {"accuracy": 0.92}}}
    }
  }
}
```

### Run Single Stage
```bash
curl -s -X POST "$GANGLION_URL/v1/run/stage/plan" \
  -H "Content-Type: application/json" \
  -d '{"context": {"model_family": "transformer"}}' | jq
```
```json
{
  "data": {
    "success": true,
    "attempts": 1,
    "error": null,
    "structured": {"plan": "Try transformer with attention heads 4, 8, 16"}
  }
}
```

### Run Direct Experiment
```bash
curl -s -X POST "$GANGLION_URL/v1/run/experiment" \
  -H "Content-Type: application/json" \
  -d '{"config": {"learning_rate": 0.001, "epochs": 10}}' | jq
```
```json
{
  "data": {
    "success": true,
    "content": "Experiment completed with config: {'learning_rate': 0.001, 'epochs': 10}",
    "structured": null,
    "metrics": null
  }
}
```

---

## Mutation

### Register a Tool
```bash
curl -s -X POST "$GANGLION_URL/v1/tools" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "analyze_results",
    "code": "from ganglion.composition.tool_registry import tool\nfrom ganglion.composition.tool_returns import ToolOutput\n\n@tool(\"analyze_results\", category=\"analysis\")\ndef analyze_results(experiment_id: str) -> ToolOutput:\n    \"\"\"Analyze results of a past experiment.\"\"\"\n    return ToolOutput(content=f\"Analysis of {experiment_id}\")",
    "category": "analysis"
  }' | jq
```
```json
{"data": {"path": "/home/user/sn9-pretrain/tools/analyze_results.py"}}
```

### Register a Tool (Validation Failure)
```bash
curl -s -X POST "$GANGLION_URL/v1/tools" \
  -H "Content-Type: application/json" \
  -d '{"name": "bad_tool", "code": "def bad_tool(x):\n    pass", "category": "misc"}' | jq
```
```json
{"detail": {"error": {"code": "VALIDATION_FAILED", "message": "No @tool decorator found; Function 'bad_tool' missing docstring"}}}
```

### Patch Pipeline
```bash
curl -s -X PATCH "$GANGLION_URL/v1/pipeline" \
  -H "Content-Type: application/json" \
  -d '{
    "operations": [
      {"op": "add_stage", "stage": {"name": "analyze", "agent": "Explorer", "depends_on": ["train"], "input_keys": ["metrics"], "output_keys": ["analysis"]}},
      {"op": "update_stage", "stage_name": "train", "updates": {"is_optional": true}}
    ]
  }' | jq
```
```json
{
  "data": {
    "pipeline": {
      "name": "sn9-pipeline",
      "stages": [
        {"name": "plan", "agent": "Planner", "depends_on": []},
        {"name": "train", "agent": "Trainer", "depends_on": ["plan"], "is_optional": true},
        {"name": "analyze", "agent": "Explorer", "depends_on": ["train"]}
      ]
    }
  }
}
```

### Update a Prompt
```bash
curl -s -X POST "$GANGLION_URL/v1/prompts" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "Trainer",
    "prompt_section": "strategy",
    "content": "Prioritize transformer architectures. Start with small models (< 100M params) and scale up only if results are promising."
  }' | jq
```
```json
{"data": {"path": "/home/user/sn9-pretrain/prompts/trainer.py"}}
```

---

## Rollback

### Undo Last Mutation
```bash
curl -s -X POST "$GANGLION_URL/v1/rollback/last" | jq
```
```json
{"data": null}
```

### Undo All Mutations
```bash
curl -s -X POST "$GANGLION_URL/v1/rollback/0" | jq
```
```json
{"data": null}
```

### Rollback When No Mutations Exist
```bash
curl -s -X POST "$GANGLION_URL/v1/rollback/last" | jq
```
```json
{"detail": {"error": {"code": "ROLLBACK_ERROR", "message": "No mutations to rollback"}}}
```
