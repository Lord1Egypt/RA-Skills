# Execution Modes

## 1. Benchmark input modes

### `prompt_only` (default)
- send only the raw prompt
- no memory
- no hidden scaffolding
- no benchmark-specific system prompt injection
- fairness-first mode

### `agent_context`
- send prompt plus one fixed shared context/system layer
- use the same context for every compared model in the run
- record that context in metadata/spec
- realism-focused mode

---

## 2. Execution strategies

### `sequential`
- run one model at a time
- easier to debug
- lower orchestration overhead

### `subagent_orchestrated`
- one orchestrator coordinates multiple subagents
- one subagent typically handles one model
- best for larger batches
- orchestrator validates and aggregates results
- may run with bounded parallelism (for example `max_parallel=2` or `max_parallel=4`) when the endpoint can tolerate concurrent load
- should surface a progress update whenever one subagent/model finishes
- should preserve output ordering in final artifacts even if subagents complete out of order

---

## 3. Operational modes

### `prepare`
Collect benchmark context and build/refine the benchmark spec.

### `run`
Execute benchmark runs, compute metrics, and score models locally.

Operational notes for `run`:
- If the runtime exposes provider-prefixed names (for example `cliproxy/gpt-5.2`) but the endpoint expects raw model ids (for example `gpt-5.2`), normalize the model name before calling the endpoint.
- When a user adds custom models, verify them before the run starts; if a name does not match the trusted provider catalog, ask the user to confirm or correct it.
- Prefer trusted local provider catalogs/config over guesswork when verifying model ids, but avoid publishing private/local defaults in public skill assets.

### `publish`
Prepare delivery artifacts, then deliver as web, PDF, or both.

### `rerank`
Reuse old raw results and apply new scoring weights/formulas without rerunning models.
