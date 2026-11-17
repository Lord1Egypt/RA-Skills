---
name: chatgpt-image-handoff
description: Route a multi-image content job through the best available generation backend, prepare a resumable prompt pack with readable-text fact boundaries, optionally operate an approved ordinary ChatGPT browser session with Computer Use, test an optional multi-image ZIP delivery when the active surface supports it, repair useful generated backgrounds with an allowlist-only mixed overlay, import outputs under stable names, and resume visual QA. Use when built-in ImageGen is unavailable or flaky, Codex may or may not have Computer Use, a user needs a manual ChatGPT fallback, repeated browser round trips should be reduced, exact names or numbers must not be invented, or external image outputs must re-enter a checked local asset pipeline without losing job state. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/content/chatgpt-image-handoff
---

# ChatGPT Image Handoff

Turn an image-generation gap into a recoverable local workflow. Default to `backend=auto`, preserve one job per image even when several jobs share one ZIP delivery, and converge every backend on the same import, QA, and human-confirmation contract.

## Inputs

Collect:

- a JSON spec with `run_id`, shared visual direction, dimensions, and ordered image jobs
- one self-contained prompt and stable intended filename per job
- approved reference-image paths when needed
- a local handoff directory, preferably under an ignored runtime folder
- `backend`, defaulting to `auto`
- `preferred_backend`, defaulting to `chatgpt_computer_use`
- per-job `fact_sensitivity`: `low`, `medium`, or `high`
- per-job `render_strategy`: `auto`, `generative`, `mixed`, or `deterministic`
- optional `text_policy` with `mode`, `allowed_text`, `forbidden_patterns`, and `extra_readable_text`
- an existing `jobs.json` when resuming

Require Python 3 and Pillow for the bundled import and contact-sheet scripts. Route incomplete copy, unstable claims, or missing source anchors back to the upstream planning skill.

## Backend Decision

Treat backend selection as runtime capability routing, not as an installation assumption.

| Backend | Select when | Handoff |
| --- | --- | --- |
| `chatgpt_computer_use` | Computer Use exists and the active ChatGPT session is authenticated | Use ordinary Chat one job at a time; test ZIP only when native archive delivery is already supported |
| `built_in_imagegen` | The built-in generator is available and healthy | Return the queue to `resilient-imagegen` for serial generation |
| `manual_chatgpt_handoff` | Computer Use is unavailable or unsuitable and ChatGPT use is allowed | Give the prepared pack to the user, then resume at download import |
| `mixed` | Generated visuals are useful but exact text or structure needs deterministic overlay | Generate backgrounds, then finish in `cards-to-images` |
| `deterministic` | External ChatGPT transmission is declined or exact text and diagrams dominate | Render locally in `cards-to-images` |

For `backend=auto`, try the preferred backend first when viable, then use this default order:

1. `chatgpt_computer_use`
2. `built_in_imagegen`
3. `manual_chatgpt_handoff`
4. `mixed` or `deterministic`

Do not silently choose a paid CLI or API path. Leave that as a separately confirmed `resilient-imagegen` fallback.

Choose the render strategy per job before selecting the runtime backend:

- keep low-density conceptual visuals `generative`
- use a strict allowlist for readable names, numbers, filenames, labels, or claims
- recommend `mixed` for `fact_sensitivity=high` when a local renderer is available
- let generation create the background and composition in `mixed`; add approved copy deterministically
- record an explicit `generative` override when the user prefers full image generation, then require strict allowlist QA

Keep visual composition high freedom. Keep readable factual text low freedom.

## Workflow

### 1. Prepare The Pack

Run:

```bash
python <skill-dir>/scripts/prepare_handoff.py \
  --spec <spec.json> \
  --out <handoff-dir>
```

Confirm the pack contains:

- `master-prompt.md`
- `jobs.json`
- `prompts/<job-id>.md`
- `inbox/`
- `imported/`
- `reports/`
- `reports/text-overlay-plan.json` for `mixed` or `deterministic` jobs

Treat `jobs.json` as the source of truth. Keep this runtime directory out of public commits because it may contain local paths and reviewed working files.

For a resumed run whose pending or failed prompts must inherit a revised fact policy, run:

```bash
python <skill-dir>/scripts/prepare_handoff.py \
  --spec <spec.json> \
  --out <handoff-dir> \
  --resume \
  --refresh-prompts
```

Refresh only `queued`, `failed`, or `needs_revision` jobs. Preserve completed images and invalidate external approval for every changed prompt.

### 2. Inspect Capabilities

Determine actual runtime state:

- mark Computer Use `available` only when its tool and skill are exposed
- read the active browser state to classify ChatGPT as `authenticated`, `login_required`, or `unknown`; do not assume a session from the machine or project
- mark built-in ImageGen `healthy` only when the generator exists and is not in a known failed state
- mark the local renderer `available` when `cards-to-images` can produce deterministic or mixed output
- record whether ChatGPT transmission is `pending`, `approved`, or `denied`

Resolve and persist the backend:

```bash
python <skill-dir>/scripts/resolve_backend.py \
  --handoff <handoff-dir> \
  --computer-use available \
  --chatgpt-session authenticated \
  --built-in-imagegen unhealthy \
  --local-renderer available \
  --chatgpt-transmission pending
```

Use `unknown` when a capability has not been checked. Do not turn uncertainty into a positive capability claim.

### 3. Execute The Selected Branch

For `built_in_imagegen`, hand the queue to `resilient-imagegen` and import each selected local output before starting the next job.

For `deterministic` or `mixed`, hand the approved card or illustration package to `cards-to-images`; keep the same stable filenames and job ids.

When a generated image already has a useful composition but contains unapproved readable text, do not keep regenerating the full card. Create a reviewed mixed-overlay plan whose text elements exactly match the job allowlist, then render it locally:

```bash
python <skill-dir>/scripts/render_mixed_overlay.py \
  --source <reviewed-generated-background> \
  --plan <mixed-overlay-plan.json> \
  --output <derived-image.png> \
  --report <mixed-render-report.json>
```

The renderer locks the reviewed source checksum, can normalize a matching-ratio source when the plan explicitly sets `source_fit=resize_matching_ratio`, makes source text unreadable with a declared blur-and-tint treatment, rejects text outside `allowed_text`, and can require every approved string to appear exactly once. Import the derived image with `--generation-backend mixed --replace`, then repeat strict visual QA. Keep layout choices in the reviewed plan; do not use this renderer as automatic OCR or an unreviewed redaction tool.

A `mixed` result must retain a materially visible and relevant generated visual contribution. Review the full generated card first. When incorrect readable text is confined to one or two clear regions and the rest of the composition is strong, preserve the accepted pixels and patch only those regions with reviewed copy. Use a text-free background with reserved copy zones when text failures are widespread or cannot be isolated safely. Do not apply blur or tint strong enough to erase the composition or series style. If the generated source becomes visually incidental after the overlay, classify and report the result as `deterministic`, not `mixed`. Treat visual continuity with already accepted series images as part of strict QA.

A full-card `generative` attempt may be finished as `mixed` after human review when its failures are localized. Keep the requested render strategy and the final per-image generation backend as separate provenance fields so the repair does not rewrite history.

For a strict `generative` job, send the approved readable-text allowlist with the prompt. Permit creative visual metaphors while rejecting every additional readable label, identifier, metric, hash, checksum, timestamp, version, or path.

For `manual_chatgpt_handoff`:

1. Give the user `master-prompt.md` once.
2. Give one `prompts/<job-id>.md` at a time.
3. Ask the user to place downloaded results in the chosen downloads folder or `inbox/`.
4. Resume from detection and import without rebuilding completed jobs.

For `chatgpt_computer_use`:

1. Read and follow the installed `computer-use` skill.
2. Use its persistent JavaScript runtime for every GUI action.
3. Fetch fresh app state before every decision and after every action.
4. Prefer accessibility elements; use screenshot-guided coordinates only when required.
5. Stay in the user-approved authenticated browser window and ordinary Chat surface. Do not require a specific Chrome profile, project, or Work mode.
6. Use one job at a time by default. Consider one ZIP batch only when the active surface has demonstrated native multi-image archive delivery; preserve separate job ids and files.
7. Never reuse stale element indices.
8. Verify a new local image or ZIP archive before marking any job downloaded.

For an optional ChatGPT ZIP batch, read [ZIP batch delivery](references/zip-batch.md), then prepare the reviewed batch:

```bash
python <skill-dir>/scripts/batch_zip.py prepare \
  --handoff <handoff-dir> \
  --batch-id <stable-batch-id> \
  --job-id <job-id> \
  --job-id <job-id>
```

Send only the generated `batches/<batch-id>/work-prompt.md`. Require separate exact filenames, `qa-report.json`, `batch-manifest.json`, and one ZIP. Treat ZIP delivery as an experimental optimization of browser interaction, not a relaxation of per-image QA. A misclassification as missing-image editing, a programmatic-rendering proposal, or a missing archive is a batch failure; record it with `batch_zip.py fail` and return to ordinary Chat one job at a time.

When the user requires ChatGPT-native image generation, reject Python, Pillow, SVG, HTML, Canvas, deterministic drawing, screenshots, or placeholders inside ChatGPT as backend substitution. Record the batch as failed and retry fewer jobs through the native image tool.

Before the first ChatGPT submission, list the exact prompt and reference files, destination, and purpose. Request action-time confirmation immediately before typing the first prompt or uploading any reference. One confirmation may cover the unchanged reviewed batch. Stop for login, account verification, CAPTCHA, quota, billing, or an unexpected destination.

Do not encode selectors, coordinates, conversation ids, account identifiers, or active-session details in public artifacts.

### 4. Detect And Import Outputs

Scan recent image downloads without changing them:

```bash
python <skill-dir>/scripts/detect_downloads.py \
  --handoff <handoff-dir> \
  --downloads <downloads-dir>
```

Import one verified result:

```bash
python <skill-dir>/scripts/ingest_images.py import \
  --handoff <handoff-dir> \
  --job-id <job-id> \
  --source <downloaded-image>
```

Copy the original into `inbox/`, create the stable output under `imported/`, record checksums and dimensions, and refresh the contact sheet. Refuse a different replacement unless `--replace` is explicit. Never delete the original download. Pass `--generation-backend mixed` or `--generation-backend deterministic` when a local derived output overrides the run-level backend.

Import one reviewed ZIP archive:

```bash
python <skill-dir>/scripts/batch_zip.py import \
  --handoff <handoff-dir> \
  --batch-id <stable-batch-id> \
  --archive <downloaded.zip>
```

Preserve the ZIP, reject unsafe entries, import only manifest filenames, and leave missing files resumable. Never trust the archive's `qa-report.json` as a local QA pass.

### 5. Inspect And Record QA

Open every imported image. Check:

- subject, composition, order, dimensions, and intended ratio
- exact Chinese, numbers, filenames, arrows, and Skill names
- mobile-size legibility, safe margins, cropping, and consistent series direction
- invented claims, logos, private paths, watermarks, or fake interfaces
- readable text outside `text_policy.allowed_text`
- any match or semantic equivalent from `text_policy.forbidden_patterns`
- whether the result should become a visual background with deterministic text overlay

Record QA:

```bash
python <skill-dir>/scripts/ingest_images.py qa \
  --handoff <handoff-dir> \
  --job-id <job-id> \
  --status passed \
  --text-policy-status passed \
  --notes "checked at mobile size"
```

Use `needs_revision` when the image fails. Route exact typography and source-backed diagrams to deterministic or mixed rendering instead of repeatedly trusting generated text.

Treat an invented checksum, hash, commit id, timestamp, version, metric, filename, or path as a factual failure even when it looks decorative. For strict jobs, compare all readable text with the stored allowlist before passing QA.

For a strict failure, add each extra phrase with `--observed-extra-text` and each matched deny item with `--matched-forbidden-pattern`. The script must refuse `status=passed` until `text_policy_qa=passed` with no recorded extras.

### 6. Resume And Hand Off

Read `jobs.json` after any interruption. Resume only `queued`, `failed`, or `needs_revision` jobs. Read [UI recovery rules](references/ui-recovery.md) before retrying a browser, session, or download failure.

For ZIP delivery, also read `zip_batches.<batch-id>` and `batches/<batch-id>/batch-import-report.json`. Resume only the listed missing jobs; do not regenerate images that were imported successfully.

When all images pass QA:

- hand `imported/` and `reports/contact-sheet.png` to `cards-to-images` or `article-to-illustrations`
- update the downstream image manifest with `generation_backend` and the handoff `run_id`
- keep `human_confirmation=pending`
- route to `md-img-r2` plan mode only when stable public URLs are needed

Record an approval only after the user has reviewed the images:

```bash
python <skill-dir>/scripts/ingest_images.py confirm \
  --handoff <handoff-dir> \
  --job-id <job-id> \
  --status approved
```

## State Contract

Use job states `queued`, `prompt_submitted`, `generating`, `downloaded`, `imported`, `qa_passed`, `needs_revision`, and `failed`.

Store these policy fields on every prepared job:

```yaml
fact_sensitivity: high
requested_render_strategy: auto
render_strategy: mixed
recommended_render_strategy: mixed
render_strategy_reason: high fact sensitivity with an available deterministic text renderer
text_policy:
  mode: allowlist
  allowed_text: []
  forbidden_patterns: []
  extra_readable_text: reject
text_policy_qa:
  status: pending
  observed_extra_text: []
  matched_forbidden_patterns: []
```

Keep this runtime block in `jobs.json`:

```yaml
generation_runtime:
  requested_backend: auto
  preferred_backend: chatgpt_computer_use
  computer_use: unknown
  chatgpt_session: unknown
  built_in_imagegen: unknown
  local_renderer: unknown
  chatgpt_transmission: pending
  selected_backend:
  selection_reason:
external_handoff:
  destination: ChatGPT
  status: not_started
zip_batches: {}
```

Require a local file, checksum, dimensions, and visual QA before claiming success. Do not infer completion from generator UI text.

## Boundaries

- Keep account and session state local; publish only the generic workflow and scripts.
- Do not automate account creation, billing, CAPTCHA handling, R2 upload, URL rewriting, or platform publishing.
- Do not send sensitive or unreviewed material to ChatGPT.
- Do not overwrite reviewed images silently.
- Stop at human image confirmation before any external publication.

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)
