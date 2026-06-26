# Configuration Reference

## Project Directory Structure

```
my-subnet/
├── config.py              # Subnet configuration (REQUIRED)
├── tools/                 # Tool functions (auto-discovered)
│   └── run_experiment.py
├── agents/                # Agent classes (auto-discovered)
│   └── explorer.py
├── prompts/               # Prompt sections (created by update_prompt mutations)
│   └── explorer.py
├── components/            # Model components (optional)
│   └── my_backbone.py
├── knowledge/             # Knowledge store data (created automatically)
│   ├── patterns.json
│   └── antipatterns.json
└── skill/                 # OpenClaw skill documentation
    └── SKILL.md
```

## config.py

The main configuration file. Must define two required objects and may define two optional ones.

### Required Exports

#### subnet_config (SubnetConfig)

```python
from ganglion.orchestration.task_context import SubnetConfig, MetricDef, OutputSpec, TaskDef

subnet_config = SubnetConfig(
    netuid=9,
    name="My Subnet",
    metrics=[
        MetricDef(name="accuracy", direction="maximize", weight=1.0, description="Primary metric"),
    ],
    tasks={
        "main": TaskDef(name="main", weight=1.0, metadata={}),
    },
    output_spec=OutputSpec(
        format="pytorch_model",
        description="A trained classifier model",
    ),
    constraints={"max_params": 10_000_000},
)
```

**SubnetConfig fields:**

| Field | Type | Description |
|-------|------|-------------|
| `netuid` | `int` | Bittensor subnet network UID |
| `name` | `str` | Human-readable subnet name |
| `metrics` | `list[MetricDef]` | Scoring metrics (name, direction, weight, description) |
| `tasks` | `dict[str, TaskDef]` | Named tasks (name, weight, metadata) |
| `output_spec` | `OutputSpec` | Expected output format and constraints |
| `constraints` | `dict` | Arbitrary constraints passed to agents |
| `docker_prefabs` | `dict[str, DockerPrefab]` | Named container templates (optional, default `{}`) |

**DockerPrefab fields** (`from ganglion.compute.protocol import DockerPrefab`):

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | — | Prefab identifier |
| `image` | `str` | — | Container image (e.g. `ghcr.io/org/trainer:latest`) |
| `env` | `dict[str, str]` | `{}` | Default environment variables |
| `gpu_type` | `str \| None` | `None` | GPU type (e.g. `"A100"`, `"A10G"`) |
| `gpu_count` | `int` | `0` | Number of GPUs |
| `cpu_cores` | `int` | `2` | CPU cores |
| `memory_gb` | `int` | `8` | Memory in GB |
| `timeout_seconds` | `int` | `3600` | Job timeout |
| `artifacts_dir` | `str` | `"/outputs"` | Where the container writes artifacts |

A prefab is infrastructure config — it declares what a container looks like, not what it does. Call `prefab.to_job_spec(command, **overrides)` to create a `JobSpec`. The command is supplied per invocation; overrides layer on top of prefab defaults (`env` dicts are merged, scalar fields are replaced).

**MetricDef fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | — | Metric identifier |
| `direction` | `"minimize"` or `"maximize"` | — | Optimization direction |
| `weight` | `float` | `1.0` | Relative importance |
| `description` | `str` | `""` | Human-readable description |

#### pipeline (PipelineDef)

```python
from ganglion.orchestration.pipeline import PipelineDef, StageDef
from ganglion.policies.retry import EscalatingRetry, FixedRetry

pipeline = PipelineDef(
    name="my-pipeline",
    stages=[
        StageDef(
            name="plan",
            agent="Explorer",
            output_keys=["plan"],
            retry=FixedRetry(max_attempts=2),
        ),
        StageDef(
            name="experiment",
            agent="Explorer",
            depends_on=["plan"],
            input_keys=["plan"],
            output_keys=["experiment_result"],
            retry=EscalatingRetry(max_attempts=3, base_temp=0.2, temp_step=0.15),
        ),
        StageDef(
            name="evaluate",
            agent="Explorer",
            depends_on=["experiment"],
            input_keys=["experiment_result"],
            output_keys=["evaluation"],
            is_optional=True,
        ),
    ],
    default_retry=FixedRetry(max_attempts=3),
)
```

**StageDef fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | — | Unique stage identifier |
| `agent` | `str` | — | Name of the registered agent class |
| `retry` | `RetryPolicy` | `None` | Stage-level retry policy (falls back to pipeline default) |
| `is_optional` | `bool` | `False` | If true, pipeline continues even if this stage fails |
| `depends_on` | `list[str]` | `[]` | Stages that must complete first |
| `input_keys` | `list[str]` | `[]` | Keys this stage reads from TaskContext |
| `output_keys` | `list[str]` | `[]` | Keys this stage writes to TaskContext |

**Pipeline validation rules:**
- No duplicate stage names
- No cycles in the dependency graph
- All `depends_on` references must exist
- All `input_keys` must be produced by an upstream stage's `output_keys`

### Optional Exports

#### persistence (PersistenceBackend)

Enables run history, metrics queries, and checkpointing. Must implement the `PersistenceBackend` protocol:

```python
class PersistenceBackend(Protocol):
    async def save_checkpoint(self, stage, context_snapshot, result) -> None: ...
    async def load_checkpoint(self, stage) -> tuple[dict, Any] | None: ...
    async def save_run(self, pipeline_result) -> None: ...
    async def load_run_history(self, n=10) -> list[Any]: ...
    async def query_metrics(self, experiment_id=None) -> list[dict]: ...
```

Without persistence, `GET /v1/runs` and `GET /v1/metrics` return empty lists.

#### knowledge (KnowledgeStore)

Enables cross-run strategic memory.

```python
from ganglion.knowledge.store import KnowledgeStore
from ganglion.knowledge.backends.json_backend import JsonKnowledgeBackend

knowledge = KnowledgeStore(
    backend=JsonKnowledgeBackend("./knowledge/"),
    max_patterns=500,
    max_antipatterns=500,
)
```

**KnowledgeStore parameters:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `backend` | `KnowledgeBackend` | — | Storage backend |
| `max_patterns` | `int` | `500` | Max patterns before trimming |
| `max_antipatterns` | `int` | `500` | Max antipatterns before trimming |
| `bot_id` | `str` | `None` | Set automatically by `--bot-id` CLI flag |

**Available backends:**

| Backend | Import | Storage |
|---------|--------|---------|
| `JsonKnowledgeBackend(dir)` | `ganglion.knowledge.backends.json_backend` | JSON files in directory |
| `SqliteKnowledgeBackend(path)` | `ganglion.knowledge.backends.sqlite_backend` | SQLite database file |
| `FederatedKnowledgeBackend(local, peers)` | `ganglion.knowledge.backends.federated` | Write local, read from all peers |

**Federated setup (multi-bot on same filesystem):**
```python
from ganglion.knowledge.backends.federated import FederatedKnowledgeBackend, FilesystemPeerDiscovery

backend = FederatedKnowledgeBackend(
    local=JsonKnowledgeBackend("./shared/alpha/"),
    peers=FilesystemPeerDiscovery(base_dir="./shared/", local_bot_id="alpha"),
)
knowledge = KnowledgeStore(backend=backend)
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `LLM_PROVIDER_API_KEY` | Yes | OpenAI API key (read by the openai SDK for LLM calls) |
| `GANGLION_PROJECT` | No | Convention for local mode — set to project directory path |
| `GANGLION_URL` | No | Convention for remote mode — set to HTTP bridge URL |

`GANGLION_PROJECT` and `GANGLION_URL` are conventions used in skill mode detection, not read by the Ganglion code itself. All configuration is file-based via `config.py`.

The `LLM_PROVIDER_API_KEY` is read by the `openai` Python SDK (a dependency) and is required for any pipeline execution involving LLM agents.

## LLM Client Configuration

The LLM client defaults can be overridden programmatically in config.py or via agent kwargs:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `api_key` | `None` (falls back to `LLM_PROVIDER_API_KEY`) | API key |
| `base_url` | `None` (OpenAI default) | Base URL for OpenAI-compatible APIs |
| `model` | `gpt-4o` | Default model |
| `request_timeout` | `120.0` | Request timeout in seconds |
| `max_retries` | `5` | Max LLM API retries |
| `base_delay` | `1.0` | Initial retry backoff (seconds) |
| `max_delay` | `60.0` | Maximum retry backoff (seconds) |

## Minimal Working Config

```python
from ganglion.orchestration.task_context import SubnetConfig, MetricDef, OutputSpec, TaskDef
from ganglion.orchestration.pipeline import PipelineDef, StageDef

subnet_config = SubnetConfig(
    netuid=0,
    name="My Subnet",
    metrics=[MetricDef("score", "maximize")],
    tasks={"default": TaskDef("default")},
    output_spec=OutputSpec(format="model_weights"),
)

pipeline = PipelineDef(
    name="minimal",
    stages=[
        StageDef(name="run", agent="Explorer", output_keys=["result"]),
    ],
)
```

## Full Production Config

```python
from ganglion.orchestration.task_context import SubnetConfig, MetricDef, OutputSpec, TaskDef
from ganglion.orchestration.pipeline import PipelineDef, StageDef
from ganglion.policies.retry import EscalatingRetry, FixedRetry, ModelEscalationRetry
from ganglion.policies.stall import ConfigComparisonStallDetector
from ganglion.knowledge.store import KnowledgeStore
from ganglion.knowledge.backends.json_backend import JsonKnowledgeBackend

subnet_config = SubnetConfig(
    netuid=9,
    name="SN9 Pretrain",
    metrics=[
        MetricDef("loss", "minimize", weight=1.0, description="Cross-entropy loss"),
        MetricDef("perplexity", "minimize", weight=0.5, description="Perplexity"),
    ],
    tasks={
        "pretrain": TaskDef("pretrain", weight=1.0, metadata={"max_steps": 10000}),
    },
    output_spec=OutputSpec(
        format="huggingface_model",
        description="A pretrained language model",
        shape_constraints={"max_params": 1_000_000_000},
    ),
    constraints={
        "max_gpu_hours": 24,
        "min_dataset_size": 100_000,
    },
)

stall_detector = ConfigComparisonStallDetector(
    extract_config=lambda r: r.structured.get("config", {})
    if isinstance(r.structured, dict) else {}
)

pipeline = PipelineDef(
    name="sn9-pipeline",
    stages=[
        StageDef(
            name="plan",
            agent="Planner",
            output_keys=["plan", "search_space"],
            retry=FixedRetry(max_attempts=2),
        ),
        StageDef(
            name="screen",
            agent="Screener",
            depends_on=["plan"],
            input_keys=["plan", "search_space"],
            output_keys=["candidates"],
            retry=FixedRetry(max_attempts=3),
            is_optional=True,
        ),
        StageDef(
            name="train",
            agent="Trainer",
            depends_on=["plan"],
            input_keys=["plan"],
            output_keys=["model_path", "metrics"],
            retry=EscalatingRetry(
                max_attempts=5,
                base_temp=0.1,
                temp_step=0.1,
                stall_detector=stall_detector,
            ),
        ),
        StageDef(
            name="evaluate",
            agent="Evaluator",
            depends_on=["train"],
            input_keys=["model_path", "metrics"],
            output_keys=["evaluation", "submission"],
        ),
    ],
    default_retry=FixedRetry(max_attempts=3),
)

knowledge = KnowledgeStore(
    backend=JsonKnowledgeBackend("./knowledge/"),
    max_patterns=500,
    max_antipatterns=500,
)
```
