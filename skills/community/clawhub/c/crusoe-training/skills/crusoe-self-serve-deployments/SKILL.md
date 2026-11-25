---
name: crusoe-self-serve-deployments
description: Create, monitor, update, and delete Crusoe Self-Serve Deployments — reserved-capacity inference endpoints for base models or fine-tuned LoRA adapters (from Serverless Fine-Tuning checkpoints or Hugging Face), then run OpenAI-compatible chat completions against the deployment alias. Part of the crusoe-training family. Use when the user wants to deploy a model, serve a fine-tuned adapter, scale or update a deployment, or stand up a dedicated inference endpoint on Crusoe.
---

# Self-Serve Deployments (SSD)

Reserved-capacity inference on Crusoe's managed infrastructure. Read
`../../references/setup-and-auth.md` for auth and
`../../references/api-endpoints.md` for field-level detail. Paths are relative
to this skill's root.

Management API base:
`https://api.crusoecloud.com/v1/projects/{project_id}/foundry/selfserve/`

Inference (OpenAI-compatible):
`https://api.inference.crusoecloud.com/v1` (chat completions; the deployment
alias is the `model`).

## Inputs to collect first

- **project_id** — from the Console URL; required in every management URL.
- **What to serve** — a base model, a fine-tuned checkpoint (from SFT: the
  checkpoint's `fine_tuned_model_checkpoint` id), or a Hugging Face adapter
  repo (private repos need a project credential, see setup-and-auth.md).
- **Deployment configuration** — Responsiveness (low latency) / Throughput
  (cost at scale) / Balanced (general); Multi-LoRA deployments use the
  Multi-LoRA configuration only.
- **Replica count** — throughput is bounded by replicas, not shared limits.

## Workflow

### 1. Discover flavors

Flavors are the concrete (model, hardware, configuration) shapes available to
the project. Always list them rather than guessing ids:

```python
import httpx, os

BASE = f"https://api.crusoecloud.com/v1/projects/{project_id}/foundry/selfserve"
HEADERS = {"Authorization": f"Bearer {os.environ['API_TOKEN']}"}

flavors = httpx.get(f"{BASE}/flavors", headers=HEADERS).json()["flavors"]
for fl in flavors:
    print(fl["id"], fl["model_name"], fl["flavor_type"],
          fl.get("lora_suitable"), fl["price_per_hour"])
```

Filter by `model_name` — the **display name** (`Qwen/Qwen3.5-2B`), not the
fine-tuning model id — plus configuration intent (`flavor_type`) and, for
adapters, `lora_suitable` / `fused_lora_supported`. Note not every model
offers every configuration. Show price per hour and let the user pick.

### 2. Choose the deployment type

Ask the user when intent is unclear; recommend and confirm otherwise:

| Type | When | Body shape |
|---|---|---|
| Base model | Serving one stock model | `{flavor_id, deployment_name, replicas}` |
| Fused LoRA | One fine-tuned model in production; best latency/throughput | adds `"fine_tuned_model_id": "<checkpoint id>"` |
| Multi-LoRA | Comparing/evaluating several adapters side by side | adds `"multi_lora_enabled": true, "adapters": [...]` |

Multi-LoRA adapter entries:

```json
{
  "name": "<adapter_name>",
  "source": {
    "type": "registry",
    "registry_model_id": "<fine_tuned_model_checkpoint from the SFT job>"
  }
}
```

or `{"type": "huggingface", "url": "https://huggingface.co/<org>/<repo>",
"credential_id": "<only for private repos>"}`.

Field-name note: the published v1 spec spells the fused field
`fine_tuned_model`; the docs use `fine_tuned_model_id`. If the create call
rejects the field, retry with the other spelling.

Show the full payload (including hourly cost from the flavor) and get an
explicit yes before creating.

### 3. Create

```python
resp = httpx.post(
    f"{BASE}/deployments",
    headers=HEADERS,
    json={
        "flavor_id": flavor_id,
        "deployment_name": "my-model",   # this alias is the inference model id
        "replicas": 1,
        # fused:  "fine_tuned_model_id": "<checkpoint id>",
        # multi-lora: "multi_lora_enabled": True, "adapters": [...]
    },
)
print(resp.json())  # includes deployment id + operation id
```

### 4. Poll to Ready

Provisioning reserved capacity can take **up to ~40 minutes**.

```python
import time

while True:
    dep = httpx.get(f"{BASE}/deployments/{deployment_id}", headers=HEADERS).json()
    status = dep["status"]
    progress = httpx.get(f"{BASE}/deployments/{deployment_id}/progress", headers=HEADERS).json()
    print(status, progress.get("percent"), progress.get("message"))
    if status.lower() == "ready":
        break
    if status.lower() == "failed":
        raise SystemExit(f"deployment failed: {dep}")
    time.sleep(60)
```

Statuses come back **lowercase** (`creating`, `ready`, `scaling up`,
`scaling down`, `syncing`, `failed`, `deleting`); compare case-insensitively.
Provisioning can take up to ~40 minutes. Poll at a sane interval; never
re-create a deployment that is still `creating`.

### 5. Smoke-test inference

```python
from openai import OpenAI
import httpx, os

infer = OpenAI(
    api_key=os.environ["API_TOKEN"],
    base_url="https://api.inference.crusoecloud.com/v1",
    http_client=httpx.Client(proxy=None, trust_env=False),
)
reply = infer.chat.completions.create(
    model="my-model",  # the deployment alias
    messages=[{"role": "user", "content": "Say 'deployment works' and nothing else."}],
)
print(reply.choices[0].message.content)
```

For **Multi-LoRA**, `model` is the adapter's id: `<deployment alias>_<adapter
name>`. Requests to an adapter that isn't `ready` error out — no silent
fallback to the base model.

Thinking base models (Qwen3.5, GLM-5.x) trained on non-thinking data may
return `content: null` with the answer in `message.reasoning`. If that
happens, retry with `"chat_template_kwargs": {"enable_thinking": false}` in
the request body (verified live), and tell the user — it also hints the
dataset should carry thinking-formatted turns.

### 6. Manage

- **Scale**: `PATCH .../deployments/{id}` with `{"replicas": N}` — serves
  traffic while scaling.
- **Rename**: same PATCH with `{"deployment_name": "..."}` — status goes
  `Syncing` then back to `Ready`. Renaming a Multi-LoRA deployment renames
  every adapter's model id (`<new-alias>_<adapter>`); clients must update.
- **Swap checkpoint**: PATCH with the new `fine_tuned_model` /
  `fine_tuned_model_id`; use `"rolling_update": true` to avoid downtime.
- **Delete**: `DELETE .../deployments/{id}` returns `202`; the deployment
  transitions through `deleting`, then `GET` returns 404. **Billing stops
  only on deletion.** Always offer this when the user is done testing.

## Guardrails

- **GPU-hours bill from creation until deletion.** Before creating, state the
  flavor's `price_per_hour` × replicas. After a smoke test, ask whether to
  keep or delete the deployment.
- Confirm every create/scale/delete with the user; these are all billable or
  destructive.
- Never invent a `flavor_id` — always list flavors for the user's project.
- If the checkpoint's base model has no `lora_suitable` flavor, say so
  instead of deploying onto an incompatible shape.
- Adapter constraints (Multi-LoRA): standard PEFT LoRA only, rank ≤ flavor's
  `max_lora_rank`; DoRA/QA-LoRA/`modules_to_save`/`rank_pattern`/
  `alpha_pattern` are not supported.
