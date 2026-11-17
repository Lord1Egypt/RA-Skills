---
name: berrys
description: Use when the user asks to make, edit, storyboard or review images, video, audio or ads "in Berrys", "on my Berrys canvas" or "with Berrys", or mentions a Berrys project. Teaches the playground_* MCP tools - choosing a path, checking prices, spend approvals, waiting on jobs, reviewing outputs, canvas links.
---

# Using Berrys

Berrys is a canvas for AI images, video and audio. You talk with the user and plan the work. Berrys runs it on the user's canvas, with the user's credits and approvals. Everything you do can be seen, edited and reverted in Berrys. Keep the user in control.

## Default models

Unless the user explicitly chooses another model, use **Nano Banana 2** (`google:nano-banana-2`) for images and **Seedance 2.0 Mini** (`bytedance:seedance-2.0-mini`) for videos. Preserve models already selected on existing nodes. If a default is unavailable or incompatible, explain and ask before substituting; do not choose the first model in the catalogue.

## Start

For greetings, brainstorming without a request to generate, and questions about what Berrys can do, answer without selecting, listing, reading or opening a project. Use `playground_capabilities_discover` without `projectId` if you need a product overview. No canvas preview is needed.

For creative work:
1. Use an explicitly named or linked project, or the project already established for the same creative task in this conversation. Use `playground_context_current` only when the user refers to their open project or selection. It returns live context without a preview.
2. A fresh request to generate images, video or audio authorizes creating a new project automatically when no project is named, linked or established for that task. Call `playground_project_create` with a concise name from the brief. Do not ask for separate permission or a project name, and do not inspect or list existing projects first. A new chat alone does not create a project.
3. Reuse the created project for follow-up edits, variations, quotes and approval on the same task. Start another project only for an explicitly separate new task. If the user wants to continue existing work but the intended project is unclear or no live context is available, ask which project. Never pick a recent, first-listed or QA project on their behalf.
4. Before writing, call `playground_capabilities_discover` with the chosen project to check available actions.
5. Creating the empty project spends no credits and does not approve generation. Show the quote and obtain approval before any paid generation. Use canvas previews for requested canvas work or review, and media previews to show actual results.

When someone describes an outcome rather than model settings, use `playground_content_prepare`: brief, optional intended use and a short deliverables list. It returns explicit prompts, assumptions and an exact quote. Ask only for missing product/reference material or required copy. For speech, draft the words from the brief and let the user review them; ask for wording only when they require exact copy. Keep the prepared request together through approval so the user never has to learn node IDs or model names.
If they provide a product page, use `playground_web_page_read` for its facts and imagery after the project is chosen. If they attach an image, use the upload/import tools and pass the returned image node ID as a reference. On follow-up requests, identify the saved result from this conversation or `playground_run_delivery`, then make the requested variation in the same project.

## Playbooks, workflow inputs and recovery

- Explore and load built-in playbooks with `playground_skills_discover` and `playground_skill_load` without a project. Search by `query` or `category`, and follow `nextOffset`. Include `projectId` only for private project skills, with `scope: "project"` when loading one.
- Find implemented editing operations with `playground_actions_discover`. It hides unavailable actions by default. Check availability rather than promising an unsupported edit.
- For a chosen workflow, `playground_workflow_inspect` shows a form in compatible chat hosts. `playground_workflow_inputs_set` saves free edits to text/List inputs, prompts, aspect ratios, durations, voice/music direction and image reference choices. Saved, active and approved work stays read-only. Hosts without forms can use the same structured inputs through chat.
- `playground_workflow_quote` prices the next ready stage without preparing approval or generating anything. Continue through the existing quote and chat-confirmation flow only when the user wants to run it.
- `playground_run_delivery.recovery` lists individual receipts, including List outputs. Use `playground_media_retry_quote` for only the selected confirmed failures. Its `retryPlan` provides exact replacement items for `playground_media_generate`; a quote still requires preparation and explicit chat approval before generation. Preserve completed, active and uncertain items. Never rerun an entire List because one item failed. Restore missing references or discuss unsupported inputs instead of silently dropping them.

## How Berrys speaks

Keep it clear, warm and direct. Talk about what the user can make: on-brand images, video clips, voiceovers and reusable workflows. Use short sentences, concrete outcomes and one useful next step. Show the credit cost before generation and wait for approval.

Explain a limit only when it affects the request. For example: “Joining clips is not available here. You can still create and download individual clips.” Do not turn a capability overview into a list of unavailable features. Do not narrate deployment switches, QA projects, development processes, internal IDs or role flags unless the user asks for technical diagnostics. Do not inspect account connections or unrelated projects to answer a general question.

## Access

Connect once with OAuth. The app follows the user’s existing project roles: viewers can read; editors can edit and request generation. Capability names describe available actions, not additional setup. Paid generation always waits for the user to confirm the exact request and cost in their agent chat.

| Capability | Lets you |
|---|---|
| `canvas:read` | Read the canvas, models, prices, quotes, jobs, runs and approvals. |
| `canvas:edit` | Add, connect, tidy and revert nodes; upload and import media; compare and stitch. Free. |
| `media:spend` | Run paid image, video and audio generation (`playground_media_generate`, `playground_node_run`). |
| `agent:start` | Hand a brief to the Berrys agent (`playground_brief_start`, `playground_run_steer`). |
| `agent:approve` | General agent-plan approval is unavailable. Direct paid requests use the scoped confirmation tool after the user confirms in chat. |
| `memory:read` / `memory:write` | Read / save project memory. |
| `connector:read` | Read the user's connected Drive, Shopify, Meta Ads or Gmail accounts. |

If a call fails with `forbidden`, tell the user the `userAction` (which project role is needed, or which exact request needs confirmation in chat). Don't retry until they say it's done.

## Pick a path

Decide once, up front:

- **Build it yourself** when you know what to make: a few images or clips, a storyboard you planned with the user, or edits to specific nodes. You control every prompt and every credit.
- **Hand it to the Berrys agent** (`playground_brief_start`) when the user wants Berrys to plan and produce the whole thing ("just make it", a full ad or film from a brief), or when the job needs the agent's own research, video understanding or multi-step production plan.

Don't mix the two on the same nodes at once.

### Build it yourself

**Quick generate** (no canvas planning)
1. For an everyday brief, call `playground_content_prepare` with the project, intended use and deliverables. It prices up to 20 items, returns the exact prompts, reference thumbnails and a ten-minute quote without creating nodes or spending credits. For precise instructions, call `playground_media_generate` with `quote: true` instead. Use `playground_models_list` only when comparing model options or a budget needs alternatives.
2. Show the itemized quote, references, assumptions and total. Let the user correct the brief before submitting.
3. When the user wants to proceed, call `playground_media_generate` with the returned `mediaGenerateRequest` (or the same directly quoted items) and a **new** `idempotencyKey`. This prepares confirmation in chat and spends nothing by itself.
4. Follow **Spend approval and waiting** below. Deliver original files, available dimensions and a concise summary; suggest one relevant next step.

**Build on the canvas** (storyboards, shot lists, chains of nodes)
1. `playground_canvas_read` for the nodes and the current `revision`.
2. `playground_canvas_apply_operations` to add or connect nodes (free). `playground_storyboard_prepare` turns a text group into shot nodes.
3. `playground_node_run` with `nodeIds` and `quote: true`. Show the credits and references, and retain its ten-minute `quoteId`.
4. `playground_node_run` again without `quote`, with its returned `quoteId` and a new `idempotencyKey`. The user then approves in Berrys.
5. Follow **Spend approval and waiting**, then **Review your outputs**.

`playground_node_run` runs image, video and audio nodes. Set their fields with `playground_canvas_apply_operations` first:
- **Image:** `prompt` (stored in a wired Text node), `modelId`, `aspectRatio`; connect up to three image references.
- **Video:** `instructions` (the prompt), `modelId`, `aspectRatio`, `duration`; connect references, or frames with role `first_frame` / `last_frame`.
- **Audio:** `instructions` (speech: the words to say; music: the lyrics), `modelId` (`minimax:speech-2.8-hd`, `minimax:speech-2.8-turbo`, `minimax:music-2.5` or `minimax:music-1.5`), plus `voice` for speech or `style` for music. Keep the words on the audio node itself; an audio node fed by Text nodes is refused.

Prompt Helper and Video Story nodes can't be run from here, because they run in the browser. Write prompts yourself, or use `playground_video_analyze` for facts about a clip. `playground_media_generate` also takes `kind: "audio"` items (`prompt` holds the words, plus optional `voice` or `style`).

### Hand it to the Berrys agent

V1 defaults to direct generation. Check capabilities first: delegation is available only when `switches.agentStartsEnabled` is true. Do not request a paid agent turn when disabled. Delegation can have planning/review charges beyond media generation; show and obtain approval for those costs before using it.

1. `playground_brief_start` with the brief, any reference node IDs in `files`, and `connectorAccountIds` if the agent should read connected sources (requires project access). It returns `runId` and `canvasUrl` at once.
2. Call `playground_run_events` with `runId`, `afterSeq` (the last `nextAfterSeq` you got, 0 at first) and `waitSeconds: 25`. The server waits for new events, so you don't need to poll fast. If you lost the `runId`, pass `conversationId` instead.
3. When `pendingApprovals` is not empty, tell the user what is waiting and its credit ceiling, and send them to the `canvasUrl` to approve. To redirect the agent mid-plan, use `playground_run_steer`.
4. When the run ends (`retry_after_seconds` is null), the final `response` is in the events result. Call `playground_run_delivery` and only report work as done if it lists real assets.
5. If the run fails or stalls, call `playground_run_diagnose` and follow its `next` action. To continue, send another `playground_brief_start` with the same `conversationId`.

## Spend approval and waiting

A paid call (not a quote) returns one of:

- **`approval_required`**: every paid request waits for the user. Show the exact references, prompts, model, output count, per-item credits and total in chat, then ask the user to confirm. Do not open an approval page. After explicit user confirmation, call `playground_approval_decide` for each item with its `approvalId`, `inputFingerprint` and `maxCredits` equal to its quoted credits; videos first. Never call approve before the user confirms. After they approve, repeat the exact same call with the **same** `idempotencyKey` (it never charges twice) or call `playground_media_jobs_list` to get the `dispatchIds`.
- **`submitted`**: already approved by the user and submitted. You get `dispatchIds`.
- **`completed`**: an exact replay found that every dispatch finished. Confirm the assets with `playground_run_delivery` before reporting completion.
- **`needs_reconciliation`**: a provider submission is uncertain. Check the existing dispatch and run receipts; do not start another paid request with a new key.

Then wait on each job with `playground_media_job_get` and `waitSeconds: 25`. The server holds the call until the job finishes or the time runs out. Repeat while `retry_after_seconds` is not null. For many jobs, `playground_media_jobs_list` reads them all in one call. On partial failure, keep completed outputs and quote only empty/failed nodes for new work; never repeat the whole batch with a new key. Without `waitSeconds`, wait at least `retry_after_seconds` between calls.

If you get `insufficient_credits`, stop and tell the user to top up in Berrys (or offer cheaper models from `playground_models_list`).

## Quotes and idempotencyKey

Execution requires the matching server-issued `quoteId`. If the prompt, model, references or price ceiling changes, or ten minutes pass before approval, request a fresh quote. A quote is not a credit reservation. Do not invent a quote ID or bypass an expired quote. Replaying an existing request with the same key reads its existing results even after the quote expires.

- **New request, new key.** Every distinct paid call or canvas write gets a fresh key. That includes the real run after a quote: the run is a new request.
- **Same key only to retry the identical request** whose answer you lost (timeout, dropped connection). The server then returns the original result instead of charging again.
- Reusing a key with different inputs fails with `idempotency_conflict`. Don't fire a paid call again blindly; if unsure whether it went through, check `playground_media_jobs_list` first.

## Review your outputs

Read `playground_run_delivery.generationReview` for per-item references, status and billing receipts to show in this chat. Report actual recorded credits and refunds; leave missing receipts pending instead of treating the quote as a final charge. Balances exclude credits held by other jobs. On partial failure, use the returned retryRequest to select only confirmed empty failures. Never regenerate `needs_reconciliation` work or revert a batch with successful outputs merely to retry a missing item.

Don't hand back work you haven't checked. Forward returned native image content to the user using the host’s image-display mechanism. Do not replace it with Markdown embeds of remote storage URLs: those may render as blank placeholders. The completed-media tools also expose a read-only chat gallery on compatible hosts. If a preview cannot be displayed, say so and provide a labelled original-file link; do not report that an image was shown. Use native video/audio playback where available and a result link otherwise. Always retain the canvas link. A file being on the canvas is separate from a creative review passing.

- For clips, call `playground_video_analyze`: duration, black frames, silence and loudness, plus any visual analysis Berrys already has. Flag clips that are cut short, black or silent.
- To pick between takes, place them side by side with `playground_media_compare` and look at the images or clips yourself before you choose.
- If an output is wrong (off-brief, broken, bad continuity), say so, fix the prompt or settings, quote again, and regenerate with a new `idempotencyKey`. Don't present a bad output as finished.
- For localized images, inspect the rendered words against the requested language and exact headline. A completed job or verified delivery receipt only proves the file landed on the canvas; it does not prove the text is accurate. Flag incorrect or unreadable text for review and regeneration.
- For continuity between shots, `playground_video_extract_frames` takes the last frame of one clip to use as the next shot's `first_frame`. Only when `switches.assemblyEnabled` is true, stitch finished clips with `playground_media_compose`. To cut a clip to a range, call `playground_video_trim` with `startSeconds` and `endSeconds`. It's free, and it adds a Clip node; poll `playground_run_delivery` with the `runId` it returns.
- Film stitching and trimming need a running assembly worker. If a run stays `waiting_assembly` with zero attempts, report that the service has not picked it up; do not keep polling indefinitely or claim the film is ready. Cancel or revert the queued run when the user asks.

## Other rules

- **Credits, not dollars.** Show costs in Berrys credits.
- **Canvas writes need a revision.** Pass `expectedRevision` from `playground_canvas_read`. On `revision_conflict`, read the canvas again and rebuild the change; don't resend the old one.
- **Always give the user the `canvasUrl`** from each result so they can see the work.
- **Open the workspace:** call `playground_canvas_open` with the project and optional node IDs. If the host can open a browser beside chat, reuse that project tab. Otherwise show its link. Never claim an embedded canvas opened just because the server returned a URL.
- **Drive images:** discover the user’s Berrys-connected Drive accounts with `playground_connected_sources_list`. Use `playground_drive_image_import` with the selected `accountId` and file ID; it copies the image into provider-fetchable Berrys reference storage and returns a File node ID. Another agent’s Drive connection is not inherited. If the agent already has authorized downloadable bytes, use the signed upload path instead. Do not submit a Drive sharing-page URL as an image.
- **Uploads:** for local files use `playground_media_upload_begin`, PUT the bytes to the signed URL, then `playground_media_upload_complete`. Never paste the signed URL into chat. For public URLs use `playground_asset_import`.
- **Use an uploaded image:** upload completion only adds a File node. To use it in generation, pass that returned node ID in `referenceNodeIds` for `playground_media_generate`, or connect it to the target image/video node before `playground_node_run`. Verify the reference edge before requesting approval. Images already generated will not gain the reference retroactively.
- **Errors** come back as `structuredContent.error` with `code`, `retryable` and `userAction`. Tell the user the `userAction` when there is one; retry only when `retryable` is true.
- **Undo:** `playground_run_revert` undoes one run's canvas changes; `playground_canvas_snapshots_list` / `playground_canvas_snapshot_restore` restore the whole canvas.
- **Memory:** `playground_memory_propose` saves a note that takes effect immediately: the Berrys agent reads it on every later turn. Only save what the user asked you to remember or clearly decided, and tell them what you saved.

## Playbooks for bigger jobs

Berrys hosts step-by-step playbooks for whole jobs. For anything bigger than a few quick images or clips:

1. Call `playground_skills_discover`. Playbooks have `category: "Playbooks"` and are listed first.
2. Load `berrys-start-here` with `playground_skill_load` (`id: "berrys-start-here"`, `version` from discover). It maps the request to the right playbook: ecommerce images, product ad, script to video, resize, batch from a list, refine loop, character or brand kit, open project, still to motion, themed series, social carousel, mockup pack.
3. Load that playbook and follow it on top of this skill. Playbooks are self-contained; this skill's rules on pricing, approvals, waiting, idempotency keys and links still apply.

Other skills in the list are method notes written for the Berrys agent; load them when a playbook names one for craft.

## Who does what

Brainstorm, write scripts and pick shots here, with the user. Use Berrys to build the canvas and run generation. Show the plan and the cost before anything is spent.
