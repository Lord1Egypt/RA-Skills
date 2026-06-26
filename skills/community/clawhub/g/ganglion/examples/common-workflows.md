# Common Workflows

## Workflow 1: First-Time Project Setup and Run

**Goal:** Scaffold a new subnet project, configure it, and run the first pipeline.

### Steps

1. **Scaffold:**
   ```bash
   ganglion init ./sn9-pretrain --subnet sn9 --netuid 9
   ```

2. **Verify the project was created:**
   ```bash
   ls ./sn9-pretrain/
   # Expected: config.py  tools/  agents/  skill/
   ```

3. **Set your API key:**
   ```bash
   export LLM_PROVIDER_API_KEY=sk-...
   ```

4. **Verify it loads:**
   ```bash
   ganglion status ./sn9-pretrain
   ```

5. **Run the pipeline:**
   ```bash
   ganglion run ./sn9-pretrain
   ```

6. **Check the result:** The output is JSON with `success`, `failed_stage`, and per-stage `results`.

---

## Workflow 2: Iterative Mining Loop (Local Mode)

**Goal:** Run repeated mining cycles, using accumulated knowledge to improve each run.

### Steps

1. **Set the project path:**
   ```bash
   export GANGLION_PROJECT=./sn9-pretrain
   ```

2. **Check prior knowledge:**
   ```bash
   ganglion knowledge $GANGLION_PROJECT --capability training
   ```

3. **Review what tools and agents are available:**
   ```bash
   ganglion tools $GANGLION_PROJECT
   ganglion agents $GANGLION_PROJECT
   ```

4. **Run the pipeline:**
   ```bash
   ganglion run $GANGLION_PROJECT
   ```

5. **Check knowledge after the run:** New patterns and antipatterns are recorded automatically.
   ```bash
   ganglion knowledge $GANGLION_PROJECT
   ```

6. **Repeat** steps 2-5. Each run benefits from knowledge accumulated in prior runs.

---

## Workflow 3: Remote Mode with Dynamic Mutation

**Goal:** Start the HTTP bridge, observe state, register new tools/agents, modify the pipeline, and run.

### Steps

1. **Start the server:**
   ```bash
   ganglion serve ./sn9-pretrain --bot-id alpha --port 8899
   ```

2. **Set the URL:**
   ```bash
   export GANGLION_URL=http://127.0.0.1:8899
   ```

3. **Observe current state:**
   ```bash
   curl -s "$GANGLION_URL/v1/status" | jq
   curl -s "$GANGLION_URL/v1/tools" | jq '.data[].name'
   curl -s "$GANGLION_URL/v1/pipeline" | jq '.data.stages[].name'
   ```

4. **Register a new tool:**
   ```bash
   curl -s -X POST "$GANGLION_URL/v1/tools" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "evaluate_model",
       "code": "from ganglion.composition.tool_registry import tool\nfrom ganglion.composition.tool_returns import ExperimentResult\n\n@tool(\"evaluate_model\", category=\"evaluation\")\ndef evaluate_model(model_path: str, dataset: str = \"default\") -> ExperimentResult:\n    \"\"\"Evaluate a trained model.\"\"\"\n    return ExperimentResult(content=\"Evaluated\", metrics={\"score\": 0.9})",
       "category": "evaluation"
     }' | jq
   ```

5. **Add a new stage to the pipeline:**
   ```bash
   curl -s -X PATCH "$GANGLION_URL/v1/pipeline" \
     -H "Content-Type: application/json" \
     -d '{
       "operations": [{
         "op": "add_stage",
         "stage": {
           "name": "final_eval",
           "agent": "Explorer",
           "depends_on": ["experiment"],
           "input_keys": ["experiment_result"],
           "output_keys": ["final_score"]
         }
       }]
     }' | jq
   ```

6. **Verify the pipeline:**
   ```bash
   curl -s "$GANGLION_URL/v1/pipeline" | jq '.data.stages[] | {name, depends_on}'
   ```

7. **Run the pipeline:**
   ```bash
   curl -s -X POST "$GANGLION_URL/v1/run/pipeline" \
     -H "Content-Type: application/json" \
     -d '{}' | jq
   ```

8. **Check metrics:**
   ```bash
   curl -s "$GANGLION_URL/v1/metrics" | jq
   ```

---

## Workflow 4: Multi-Bot Knowledge Sharing

**Goal:** Run multiple mining sessions that share knowledge.

### Same Machine Setup

1. **Terminal 1 — Start bot alpha:**
   ```bash
   ganglion serve ./sn9-pretrain --bot-id alpha --port 8899
   ```

2. **Terminal 2 — Start bot beta:**
   ```bash
   ganglion serve ./sn9-pretrain --bot-id beta --port 8900
   ```

3. **Run alpha:**
   ```bash
   curl -s -X POST "http://127.0.0.1:8899/v1/run/pipeline" -H "Content-Type: application/json" -d '{}' | jq .data.success
   ```

4. **Run beta:**
   ```bash
   curl -s -X POST "http://127.0.0.1:8900/v1/run/pipeline" -H "Content-Type: application/json" -d '{}' | jq .data.success
   ```

5. **Check shared knowledge from either bot:**
   ```bash
   curl -s "http://127.0.0.1:8899/v1/knowledge" | jq '.data.patterns | length'
   curl -s "http://127.0.0.1:8900/v1/knowledge" | jq '.data.patterns | length'
   ```

Both bots see patterns from all bots. The knowledge store tags entries with `source_bot` so you can tell who discovered what.

### Local Mode Alternative

```bash
# Terminal 1
ganglion run ./sn9-pretrain --bot-id alpha

# Terminal 2 (after alpha finishes)
ganglion run ./sn9-pretrain --bot-id beta
```

---

## Workflow 5: Recovering from a Bad Mutation

**Goal:** A mutation broke the pipeline — undo it.

### Steps

1. **Check mutation count:**
   ```bash
   curl -s "$GANGLION_URL/v1/status" | jq .data.mutations
   ```

2. **Undo the last mutation:**
   ```bash
   curl -s -X POST "$GANGLION_URL/v1/rollback/last" | jq
   ```

3. **Verify the pipeline is valid again:**
   ```bash
   curl -s "$GANGLION_URL/v1/pipeline" | jq
   ```

4. **If multiple bad mutations, undo them all:**
   ```bash
   # Undo everything back to mutation index 0
   curl -s -X POST "$GANGLION_URL/v1/rollback/0" | jq
   ```

---

## Workflow 6: Running a Quick Experiment Without the Full Pipeline

**Goal:** Test a specific configuration directly without going through all pipeline stages.

### Steps (Remote Only)

1. **Run the experiment:**
   ```bash
   curl -s -X POST "$GANGLION_URL/v1/run/experiment" \
     -H "Content-Type: application/json" \
     -d '{"config": {"learning_rate": 0.001, "epochs": 10, "architecture": "resnet18"}}' | jq
   ```

2. **Check the result:** The response includes `success`, `content`, and `metrics`.

Note: This calls the registered `run_experiment` tool directly. If no such tool exists, you'll get an error.

---

## Workflow 7: Swapping Retry Policy After Poor Results

**Goal:** A stage keeps failing — switch to a more aggressive retry strategy.

### Steps

1. **Check current pipeline and retry policies:**
   ```bash
   curl -s "$GANGLION_URL/v1/pipeline" | jq '.data.stages[] | {name, retry}'
   ```

2. **Swap to escalating retry with stall detection:**
   ```bash
   curl -s -X PUT "$GANGLION_URL/v1/policies/train" \
     -H "Content-Type: application/json" \
     -d '{"retry_policy": {"type": "escalating", "max_attempts": 5, "temperature_step": 0.1}}' | jq
   ```

3. **Re-run the pipeline:**
   ```bash
   curl -s -X POST "$GANGLION_URL/v1/run/pipeline" -H "Content-Type: application/json" -d '{}' | jq
   ```
