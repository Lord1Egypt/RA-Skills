# API Endpoint Reference

Extracted from the published OpenAPI specs (verified 2026-11-18):

- Fine-tuning API: <https://api.intelligence.crusoecloud.com/v1/swagger.json>
- Deployment API: <https://api.crusoecloud.com/v1/openapi.json> — all SSD paths
  are `/v1/projects/{project_id}/foundry/selfserve/...`

## Serverless Fine-Tuning (Intelligence API)

| Endpoint | Purpose |
|---|---|
| `POST /files` | Upload a dataset (`multipart/form-data`, `purpose=fine-tune`) → file ID |
| `GET /files` / `GET /files/{id}` | List / inspect uploaded files |
| `GET /files/{id}/content` | Download file or checkpoint contents (binary stream) |
| `DELETE /files/{id}` | Delete an uploaded file |
| `POST /uploads`, `POST /uploads/{id}/parts`, `POST /uploads/{id}/complete` | Resumable multipart upload for large files |
| `POST /fine_tuning/jobs` | Create an SFT job |
| `GET /fine_tuning/jobs` | List jobs (`limit` default 20, paginate with `after=<last id>`) |
| `GET /fine_tuning/jobs/{id}` | Retrieve one job (poll this) |
| `POST /fine_tuning/jobs/{id}/cancel` | Cancel a job |
| `GET /fine_tuning/jobs/{id}/events` | Job event log (`level`: info/warn/error) |
| `GET /fine_tuning/jobs/{id}/metrics` | Training/validation metrics |
| `GET /fine_tuning/jobs/{id}/checkpoints` | List checkpoints emitted by the job |
| `POST /fine_tuning/jobs/estimate_price` | Pre-flight price estimate (same body as create) |
| `GET /public/models` | Base models available for fine-tuning |
| `GET /models` / `GET /models/{model}` | Registry models visible to the project |
| `GET /models/{model}/download` | **Download an adapter zip** for a registry model id (`ftmodel-...`, from `checkpoint.fine_tuned_model_id`). The older `GET /files/{id}/content` now returns 400 for adapters. |
| `GET /batches`, `POST /batches` | Batch inference (separate feature; out of scope here) |

### CreateFineTuningJobRequest

```json
{
  "model": "<base model id>",
  "training_file": "<file id>",
  "validation_file": "<file id, optional>",
  "suffix": "up-to-64-chars",
  "seed": 12345,
  "method": {
    "type": "supervised",
    "supervised": {"hyperparameters": { ... }}
  }
}
```

### Hyperparameters (FineTuneSupervisedHyperparameters)

| Field | Default | Notes |
|---|---|---|
| `n_epochs` | — | Always set explicitly |
| `batch_size` | — | Power of 2, 16–1024 |
| `learning_rate` | — | Always set explicitly |
| `learning_rate_multiplier` | 1 | OpenAI-compat scaling; leave at 1 |
| `checkpoint_steps` | 100 | Steps between checkpoint saves; more frequent = slower job |
| `eval_steps_per_epoch` | 4 | Eval passes per epoch |
| `early_stopping_patience` | null | Eval calls without improvement before stop |
| `lora_variant` | "lora" | `"lora"` (1/rank) or `"rslora"` (1/sqrt(rank)) |
| `lora_rank` | — | Power of 2, 2–256 |
| `lora_alpha` | — | Power of 2, 1–512 |
| `lora_dropout` | — | 0–1 |
| `lr_scheduler` | "cosine" | cosine/linear/constant/constant_with_warmup |
| `warmup_ratio` | 0.0 | 0–1 fraction of steps; typical 0.03–0.1 |
| `weight_decay` | — | L2 coefficient |
| `overlong_row_behavior` | "error" | error / drop / exact |
| `expert_lora_sharing` | per_expert | MoE only: per_expert / shared_outer / shared_ab |
| `quant_lora_method` | — | For natively-quantized MoE experts: weight_lora / qat_qlora |
| `top_k_gating` | — | MoE only: power of 2, 1–16 |

### FineTuningJob fields worth reading

- `status`: `validating_files` → `queued` → `running` → `succeeded` |
  `failed` | `cancelled` | `paused`
- `error`: failure detail (present when failed)
- `result_files`: checkpoint IDs usable with `GET /files/{id}/content`
- `fine_tuned_model`: name of the model being created
- `trained_tokens`: billable token count
- `estimated_finish`: Unix timestamp ETA

### FineTuningJobCheckpoint fields

- `id` — checkpoint object id (UUID; **not** the download key)
- `fine_tuned_model_checkpoint` — checkpoint identifier string
  (`checkpoint-<step>-<job_id>`)
- `fine_tuned_model_id` — registry model id (`ftmodel-...`); the key for
  `GET /models/{id}/download` and deployment create
- `step_number`, `metrics` (typed object in the SDK; `valid_loss` can be
  `null` on short runs), `fine_tuning_job_id`, `created_at`

`result_files` on the job holds legacy `adapter:...` ids; downloads via
`/v1/files/{id}/content` for those now return a 400 pointing at
`/v1/models/{model_id}/download`.

### Price estimate response

`{"estimated_price": "<decimal string>", "currency": "usd"}` — derived from
raw training-file size, not a quote. Actual billing uses `trained_tokens`.

## Self-Serve Deployments (Crusoe Cloud API)

Base: `https://api.crusoecloud.com/v1/projects/{project_id}/foundry/selfserve/`

| Endpoint | Purpose |
|---|---|
| `GET  /flavors` | List deployment flavors (hardware/model shapes) for the project |
| `POST /deployments` | Create a deployment |
| `GET  /deployments` | List deployments |
| `GET  /deployments/{id}` | Retrieve one deployment (poll this) |
| `PATCH /deployments/{id}` | Update name, replica count, and/or target checkpoint |
| `DELETE /deployments/{id}` | Delete (billing stops) |
| `GET  /deployments/{id}/progress` | Provisioning progress: `{percent, message, updated_at}` |
| `GET  /deployments/{id}/progress/stream` | SSE variant of progress |
| `GET  /deployments/operations` / `.../operations/{id}` | Track async operations |
| `GET  /deployments/{id}/activity` | Activity feed |

Also under `/v1/projects/{project_id}/foundry/`: `deployed-models` (models
available for inference in the project), `credentials` (HF tokens), `loras`
(legacy adapter deployments).

### SelfServeFlavor fields

Real payload (verified live): `id`, `flavor_type`, `model_name` (display
name such as `Qwen/Qwen3.5-2B` — **not** the fine-tuning model id),
`gpu_type`, `gpus_per_instance`, `quantization`, `provider`, `lora_suitable`,
`fused_lora_supported`, `multi_lora_supported`, `max_loras`,
`max_lora_rank`, `context_length`, `price_per_hour`. Pick by `model_name` +
desired configuration + (`lora_suitable`/`fused_lora_supported` for adapters);
`price_per_hour` drives the cost conversation. Not every model offers every
configuration (e.g. Qwen3.5-2B has only `throughput` and `multi_lora`).

### Create deployment body

Per the docs quickstart (field names there are authoritative for customers):

- Base model: `{"flavor_id", "deployment_name", "replicas"}`
- Fused LoRA: adds `"fine_tuned_model_id": "<checkpoint identifier>"`
- Multi-LoRA: adds
  `"multi_lora_enabled": true, "adapters": [{"name", "source": {"type":
  "registry", "registry_model_id": "<checkpoint id>"}}]`, or
  `{"type": "huggingface", "url": "https://huggingface.co/<org>/<repo>",
  "credential_id": "<optional for private repos>"}`

If the API rejects a field name, retry with the v1-spec spelling
(`fine_tuned_model` instead of `fine_tuned_model_id`) — the spec and docs
drift occasionally.

### SelfServeDeploymentDetail fields

`status`, `deployment_name` (the alias used as `model` in inference),
`model`, `fine_tuned_model`, `flavor_type`, `gpu_type`, `gpus_per_replica`,
`target_replicas`, `available_replicas`, `context_length`, `hourly_cost`,
`quantization`, `provider`, `id`, `created_at`.

### Deployment lifecycle statuses

The API returns **lowercase** values (`creating`, `ready`, `failed`,
`deleting`); the docs show Title Case — compare case-insensitively. Lifecycle:
`creating` → `ready` (serving) → `scaling up` / `scaling down` / `syncing` →
`failed` | `deleting` → deleted (subsequent `GET` returns 404). Provisioning
can take up to ~40 minutes (observed ~4 minutes for a 2B model). Create and
delete return `202` with an `operation_id`.

### Multi-LoRA specifics

- Adapter slots (`max_loras`) and max rank (`max_lora_rank`) come from the
  flavor configuration; more replicas do not add slots.
- Adapter states: `pending`, `downloading`, `loading`, `ready`, `failed`,
  `deleting`. Only `ready` adapters accept requests (no fallback to base).
- Adapter model IDs at inference: `<deployment alias>_<adapter name>`.
  Renaming the deployment renames every adapter ID.
- Adding/removing adapters does not restart the deployment.
- Supported adapters: standard PEFT LoRA on the deployment's base model with
  rank ≤ `max_lora_rank`. Not supported: DoRA, QA-LoRA, `modules_to_save`,
  `rank_pattern`, `alpha_pattern`.
- Adapters themselves are free; you pay the deployment's GPU-hours.

## Inference

OpenAI-compatible chat completions against the deployment alias:

- Python client base_url: `https://api.inference.crusoecloud.com/v1`
- Raw endpoint: `https://api.inference.crusoecloud.com/v1/chat/completions`
- `model` = deployment alias (base/fused) or
  `<alias>_<adapter-name>` (multi-LoRA)
- Thinking base models (Qwen3.5, GLM) may return the answer in
  `message.reasoning` with `content: null` when the adapter was trained on
  non-thinking data. Pass `"chat_template_kwargs": {"enable_thinking": false}`
  in the request body to get plain `content` (verified live), or train with
  thinking-formatted data.

Throughput is bounded by replica count, not shared rate limits.
