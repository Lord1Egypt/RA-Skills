---
name: crusoe-sft
description: Launch and manage supervised fine-tuning (SFT) jobs on Crusoe Serverless Fine-Tuning — upload a chat-format dataset, create a LoRA fine-tuning job, poll its status, inspect events and metrics on failure, pick the best checkpoint by validation loss, and download the adapter. Part of the crusoe-training family. Use when the user wants to fine-tune or train a model on their data, train a LoRA adapter, or ask about fine-tuning hyperparameters or checkpoints on Crusoe.
---

# Serverless Fine-Tuning (SFT)

Train a LoRA adapter on Crusoe's managed infrastructure via the
OpenAI-compatible fine-tuning API. Read `../../references/setup-and-auth.md`
for client setup and `../../references/dataset-format.md` before touching the
user's data. Paths below are relative to this skill's root.

## Workflow

### 0. Gather inputs

Collect and confirm with the user before any API call:

- **Base model id** — list live availability with `GET /v1/public/models` and
  show options if the requested one is absent.
- **Dataset path** — must be `.jsonl` or `.parquet`, ≤3 GB.
- **Goal** — what the model should learn; drives data-format review.
- **Budget appetite** — offer a price estimate before creating the job.

### 1. Validate the dataset

```bash
python3 ../../scripts/validate_dataset.py train.jsonl --model <base-model-id>
```

Errors must be fixed before upload. Review warnings with the user (see
`../../references/dataset-format.md` for what they mean). If the user wants a
proper validation set, use `--holdout 0.1 --train-out ... --val-out ...`.

### 2. Upload

```python
with open("train.jsonl", "rb") as f:
    train_file = client.files.create(file=f, purpose="fine-tune")
print(train_file.id)
```

curl:

```bash
curl https://api.intelligence.crusoecloud.com/v1/files \
  -H "Authorization: Bearer $API_TOKEN" \
  -F "file=@train.jsonl" -F "purpose=fine-tune"
```

Repeat for `validation_file` if the user has one. Reuse an existing file when
the user re-runs: `client.files.list()` first and match by filename.

### 3. (Optional) Estimate price

```python
est = client.post(
    "/fine_tuning/jobs/estimate_price",
    body={
        "model": base_model_id,
        "training_file": train_file.id,
        "method": {"type": "supervised", "supervised": {"hyperparameters": hparams}},
    },
    cast_to=object,  # required: openai SDK custom requests need an explicit cast
)
print(est)  # {'object': 'fine_tuning.job.price_estimate', 'estimated_price': '...', 'currency': 'usd'}
```

This is a file-size-based estimate, not a quote (actual billing uses
`trained_tokens`). Surface it and get confirmation.

### 4. Create the job

Show the full payload, get an explicit yes, then:

```python
job = client.fine_tuning.jobs.create(
    model=base_model_id,
    training_file=train_file.id,
    validation_file=val_file.id,          # omit to let Crusoe hold out 10%
    suffix="my-model",                    # <=64 chars, becomes part of the model name
    method={
        "type": "supervised",
        "supervised": {"hyperparameters": hparams},
    },
)
print(job.id, job.status)
```

**Hyperparameter defaults to propose** (full table with defaults:
`../../references/api-endpoints.md`):

- `n_epochs: 1–3` (start small; overfitting shows fast on LoRA)
- `batch_size`: power of 2 in 16–1024 (64 is a safe start)
- `learning_rate`: `1e-4` for ≤9B models, `1e-5`–`2e-5` for larger
  (heuristics — adjust to user's domain size)
- `lora_rank: 16`, `lora_alpha: 32`, `lora_dropout: 0.0` unless the user cares
- `checkpoint_steps: 100`, `eval_steps_per_epoch: 4` (defaults)
- `overlong_row_behavior`: leave at `error` unless the user accepts dropping

Let the user override anything; never silently pick different values than
what you showed them.

### 5. Poll until terminal

```python
import time

terminal = {"succeeded", "failed", "cancelled"}
while True:
    job = client.fine_tuning.jobs.retrieve(job.id)
    print(job.status)
    if job.status in terminal:
        break
    time.sleep(60)
```

Statuses: `validating_files`, `queued`, `running`, `succeeded`, `failed`,
`cancelled`, `paused`. Validation and queueing can take a while — that is
normal; report it rather than re-creating the job.

On **failure**, fetch the event log and show the error entries before
proposing anything:

```python
events = client.fine_tuning.jobs.list_events(fine_tuning_job_id=job.id)
for event in events.data:
    if event.level in ("warn", "error"):
        print(event.level, event.message)
```

Common causes: malformed rows (see dataset-format), rows over the context
window, oversized files. Cancel with
`client.fine_tuning.jobs.cancel(fine_tuning_job_id=job.id)` if the user wants
out.

### 6. Pick a checkpoint

```python
checkpoints = client.fine_tuning.jobs.checkpoints.list(fine_tuning_job_id=job.id).data
for ckpt in checkpoints:
    # metrics is a typed object (attribute access), not a dict
    print(ckpt.step_number, ckpt.metrics.train_loss, ckpt.metrics.valid_loss,
          ckpt.fine_tuned_model_checkpoint, ckpt.fine_tuned_model_id)
```

Checkpoint fields:

- `fine_tuned_model_checkpoint` — checkpoint identifier string
  (`checkpoint-<step>-<job_id>`)
- `fine_tuned_model_id` — registry model id (`ftmodel-...`); the key for
  adapter download and for deployment
- `metrics` — SDK returns a typed object; `valid_loss` may be `null` on very
  short runs

Pick the checkpoint with the best **validation** loss (not training loss).
Show the user the metrics table and let them confirm.

A succeeded job response also carries `result_files` (legacy `adapter:...`
ids) and `trained_tokens` (what was actually billed).

### 7. (Optional) Download the adapter

Use the registry model id. The docs' older path (`/v1/files/{id}/content`)
now returns `400: Adapter downloads have moved to
/v1/models/{model_id}/download`:

```bash
curl "$URL/v1/models/<ftmodel-id>/download" \
  -H "Authorization: Bearer $API_TOKEN" -o adapter.zip
```

The zip contains `adapter_model.safetensors` + `adapter_config.json`.

### 8. Handoff to deployment

If the user wants to serve the adapter, continue with
`../crusoe-self-serve-deployments/SKILL.md`, passing along:

- the checkpoint's `fine_tuned_model_id` (`ftmodel-...`) — used as
  `fine_tuned_model_id` in the deployment create body
- the base model's display name (`Qwen/Qwen3.5-2B` style) — deployment
  flavors are keyed by this display name, not the fine-tuning model id

## Guardrails

- Never launch a job without showing payload + price estimate + explicit
  confirmation.
- Never re-upload a dataset that already exists (`files.list()` first).
- Never pick a checkpoint silently; show the metrics.
- If a job fails twice for the same data reason, stop and re-examine the
  dataset with the user instead of re-running.
