---
name: bring-your-own-model
description: >
  Upload and use your own LoRA or checkpoint on Runware. Use when the user says "import my LoRA",
  "upload my checkpoint", "host my own model", "I trained a model elsewhere, use it here", "bring
  my own weights", or wants to run their custom safetensors through the Runware API like any
  catalog model. You give it an AIR you control, then generate with it everywhere. To create a new
  LoRA from images on Runware rather than upload an existing one, use train-style-model.
---

# Bring your own model

Take a model you already have (a LoRA or a full checkpoint, as a hosted `safetensors` file) and import it into Runware so it becomes a first-class catalog model. You assign it an AIR you own, declare its architecture, and from then on you call it in `imageInference` exactly like any built-in model. The task type is `modelUpload`.

## Inputs to collect

- **The model file as a `downloadURL`.** A reachable URL to your `safetensors`. Runware downloads it server-side, so it must be publicly fetchable (or signed).
- **`category`** - what kind of weights: `lora`, `checkpoint`, `lycoris`, `vae`, or `embeddings`. (Ask if ambiguous, most "my own model" cases are `lora` or `checkpoint`.)
- **`architecture`** - the base family the weights were trained on (a FLUX or SDXL family identifier). This must match a known architecture so inference can pair it correctly.
- **The AIR to assign** under the `runware` source you control (e.g. `runware:<id>@<n>`), plus a human `name` and `version`.
- Optional: `positiveTriggerWords` (for a LoRA), `defaultWeight`, and whether to keep it `private`.

## Models

- This is not a model-picking task, it is a model-importing task. The "model" is yours.
- Confirm the exact `modelUpload` schema (its enums and required fields) via `runware-run` before calling, the accepted `architecture` values and `category` enum are the gate. Do not hardcode an architecture string from memory, resolve it live.
- To generate *after* import, route the model choice through `runware-models` only to confirm your new AIR is showing as available, then call it like any catalog model.

## Workflow

1. **Resolve the `modelUpload` schema** (`runware-run`). Confirm the required set: `taskType`, `category`, `architecture`, `format`, `name`, `version`, `downloadURL`. `format` is `safetensors`.
2. **Assign your AIR.** Pick `runware:<id>@<n>` (the `runware` source is for account-owned models). Set `name` and `version`. This AIR is how you will call the model forever after.
3. **Submit `modelUpload`** with the file URL, category, architecture, and AIR. Add `positiveTriggerWords` / `defaultWeight` for a LoRA if you have them.
4. **Wait pragmatically (see Technique).** A LoRA deploys in about 2 minutes, a full checkpoint can be 10s of GB and takes much longer. Poll the *model's availability*, not the upload task.
5. **Generate with it.** Run `imageInference` with `model` set to your AIR. For a LoRA, attach it via the inference schema's LoRA field on a compatible base, for a checkpoint, use the AIR directly as the `model`.

## Technique

- **You control the AIR, so name it deliberately.** The `air` you pass becomes the model's permanent handle. Re-using the same AIR (plus `uniqueIdentifier`) makes the upload **idempotent**, re-submitting the identical `modelUpload` does not create a duplicate, it returns the existing deployed model.
- **Match `architecture` to how the weights were trained.** A LoRA trained on a FLUX base only composes with FLUX bases at inference time, the same for SDXL. Mismatched architecture is the most common reason a freshly imported model produces garbage.
- **Trust readiness, not the upload task.** There is a known backend issue: the model finishes downloading, deploys, and is genuinely usable (`ready`), but `getResponse` for the upload's `taskUUID` can stay `processing` **indefinitely** and never report a terminal status. Do not block on that poll. Instead, treat readiness pragmatically:
  - Re-issue the **same** `modelUpload` (idempotent) and read its status, a deployed model comes back `ready`.
  - Or query the model directly via `runware-models` and check it lists as available.
  - Or simply attempt a small `imageInference` against the new AIR, if it runs, it is ready.
- **LoRAs are cheap to iterate, checkpoints are not.** Because a LoRA lands in ~2 minutes you can import several variants and A/B them, a multi-GB checkpoint is a slower, heavier commit, get the architecture right the first time.
- **For ongoing lifecycle, prefer `modelManagement`.** It is the successor with one task type and `operation: import | update | delete`. `import` is parameter-identical to `modelUpload` (the successor for adding a model), `update` edits fields, `delete` removes a model by AIR + `uniqueIdentifier` + `category` and is a quick synchronous op.

## Parameters that matter

- `category` - `lora` | `checkpoint` | `lycoris` | `vae` | `embeddings`. Drives which extra fields apply (`type`, `defaultWeight`, `positiveTriggerWords` for LoRA/LyCORIS, `defaultScheduler`/`defaultSteps`/`defaultCFG` for checkpoints).
- `architecture` - must match a recognized base family (FLUX / SDXL etc.). Confirm the accepted string against the live schema, do not invent it.
- `format` - `safetensors` (the only accepted format).
- `air` + `uniqueIdentifier` - your permanent handle and the idempotency key. Same pair = same model, no duplicate.
- `downloadURL` - must be server-fetchable. Local files are not accepted here, host them first.
- `private` - defaults to `true`, keep it private unless you intend to publish.
- `positiveTriggerWords` (LoRA/LyCORIS) and `defaultWeight` - carry the trigger phrase and a sensible default strength so inference calls work without re-specifying.

## Quality bar

- The import used only schema-valid fields, with `architecture` matched to how the weights were trained (verified, not guessed).
- Readiness was confirmed by the model actually generating or listing as available, not by waiting on the upload `taskUUID` to report terminal (it may never).
- A first real `imageInference` against the assigned AIR produces a coherent result (not architecture-mismatch noise), retry the import with the correct `architecture` if it does not.
- The AIR + `uniqueIdentifier` are recorded so the user can call, update, or delete the model later.

## Related skills

`runware-run` (resolve the `modelUpload` schema, then run inference with your AIR), `runware-models` (confirm the imported model is available), `runware-prompting` (prompt it well, include any `positiveTriggerWords`), `train-style-model` (train a new model on Runware instead of importing one).
