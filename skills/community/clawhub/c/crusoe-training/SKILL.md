---
name: crusoe-training
description: Run the post-training lifecycle on Crusoe Intelligence Foundry. Prepare and validate chat-format datasets, launch supervised fine-tuning (SFT) jobs, monitor training runs, pick and download LoRA adapter checkpoints, and deploy base models or fine-tuned adapters to dedicated self-serve inference endpoints — all through Crusoe's OpenAI-compatible APIs. Use when the user wants to fine-tune or train a model on their data, create a LoRA adapter, upload a training dataset to Crusoe, deploy a fine-tuned model, or stand up a dedicated inference deployment.
---

# Crusoe Training

This skill family covers the Crusoe Intelligence Foundry post-training APIs:

- **Serverless Fine-Tuning (SFT)** — upload a dataset, launch a LoRA fine-tuning
  job, poll it, pick a checkpoint. OpenAI-compatible API at
  `https://api.intelligence.crusoecloud.com/v1`.
- **Self-Serve Deployments (SSD)** — deploy a base model or a fine-tuned
  adapter (from SFT or Hugging Face) to reserved-capacity inference, then serve
  it over an OpenAI-compatible chat completions endpoint.
- **Crusoe Mill** — not covered yet; planned as a third sub-skill.

## Route the task

| If the user wants to... | Read next |
|---|---|
| Fine-tune a model / launch an SFT job / train a LoRA adapter | `skills/crusoe-sft/SKILL.md` |
| Deploy a base model or fine-tuned adapter to a dedicated endpoint | `skills/crusoe-self-serve-deployments/SKILL.md` |
| Prepare, convert, or validate training data | `references/dataset-format.md`, then run `scripts/validate_dataset.py` |
| Set up API keys, URLs, or clients | `references/setup-and-auth.md` |
| Look up an endpoint, request field, object field, or status value | `references/api-endpoints.md` |

Paths are relative to this skill's root directory. Read only what the task
needs; the sub-skill files contain their own workflows and link back to the
shared references.

## Shared setup (do this once per session)

1. Confirm the user has an Intelligence API key (Console → Admin → Security →
   Intelligence API keys). Never ask them to paste it into chat; have them
   `export API_TOKEN='...'` in their shell.
2. Build the OpenAI client against Crusoe's gateway (details and curl
   equivalents in `references/setup-and-auth.md`):

```python
from openai import OpenAI
import httpx, os

client = OpenAI(
    api_key=os.environ["API_TOKEN"],
    base_url="https://api.intelligence.crusoecloud.com/v1",
    http_client=httpx.Client(proxy=None, trust_env=False),
)
```

3. Check availability of the requested base model at runtime with
   `GET /v1/public/models` rather than a memorized list.

## End-to-end pipeline

The typical journey crosses both sub-skills:

```
dataset ──upload──▶ file ID ──job──▶ SFT job ──succeed──▶ checkpoints
                                                          │ fine_tuned_model_checkpoint
                                                          ▼
                              deployment (registry source) ──Ready──▶ inference alias
```

Handoff fields:

- The SFT job's checkpoints expose `fine_tuned_model_checkpoint` — that
  identifier is what the deployment create call consumes as the registry
  source (`registry_model_id` / `fine_tuned_model_id`).
- A deployment gets a user-chosen alias; that alias is the `model` string in
  inference requests.

If the user asks for the whole pipeline, run SFT first
(`skills/crusoe-sft/SKILL.md`), confirm the best checkpoint with them, then
continue with `skills/crusoe-self-serve-deployments/SKILL.md`.

## Ground rules

- **Money is involved.** Training bills by trained tokens; deployments bill
  GPU-hours until deleted. Call the price-estimate endpoint before launching
  jobs, surface the number, and confirm before anything billable starts.
- **Confirm before creating.** Show the user the exact job/deployment payload
  (model, files, hyperparameters, flavor, replicas) and get an explicit yes.
- **Poll, don't spam.** Training runs for minutes to hours; deployment
  provisioning up to ~40 minutes. Poll at a sane interval and report progress.
- **Fail loudly.** On a failed job, fetch `GET /fine_tuning/jobs/{id}/events`
  and surface the error entries before proposing a fix.
- **No silent substitutions.** If the requested model or flavor isn't
  available, say so and show what is; never silently train on or deploy to a
  different model.

## Sources

Authored from the public docs and API specs below (verified 2026-11-18). If
behavior contradicts them, the live API wins — re-check these and tell the
user what drifted:

- Docs: <https://docs.crusoe.ai/managed-ai/overview/>
  (`serverless-fine-tuning/*`, `self-serve-deployments/*`)
- Fine-tuning API spec: <https://api.intelligence.crusoecloud.com/v1/swagger.json>
- Deployment API spec: <https://api.crusoecloud.com/v1/openapi.json>
  (selfserve endpoints under `/projects/{project_id}/foundry/selfserve/`)
