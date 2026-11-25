---
name: "event-kit-materials"
description: "Turn one event into an event kit: posters, one teaser clip, one spoken read, and an optional jingle. The event kit starts with the copy and a frame plan. An ecommerce event plan uses the same kit: after the name, time, and offer are set, it makes the posters, clip, and read. Use it for a store event, a launch, or a promotion."
---

# Event Kit Materials

## What you get

- The event copy and a frame plan. The copy carries the name, the time, and the offer.
- The posters you confirm, sharing one look.
- One spoken read of the copy you accept.
- One teaser cut: the main poster in motion, with that read on it.
- One instrumental jingle under the read, unless you strike it.

## Ways to run it

- Kit. The default. Copy and plan, then posters, the read, the teaser, and the jingle.
- Copy and plan. Strike the pieces on the card.
- A voice you supply. One clone, only when you hand over a clean single-speaker sample and confirm you have the rights to it.

Open this for a store event, a launch, or a promotion, once the name, the time, and the offer are known.

## Scope and adjacent routes

Use this route for the pieces one event needs: a store event, a launch, or a promotion. A standing brand look with no event date belongs on a visual-creation workflow. A product listing set belongs on a product-asset workflow.

## Inputs and defaults

The hard input is the event: its name, when it happens, and the offer. Ask only for what is missing among those three. Default to one vertical poster, one square poster, one spoken read in the user's language, one teaser from the vertical poster, and one instrumental jingle. Do not invent ticket sales, a live room, or an ad account.

## Golden path

1. Write the copy and the frame plan and show them. This writing is free.
2. Upload a brand or product image with `beatra.assets.upload` when one is supplied. The first poster is `beatra.images.transform` after `{"capability": "image_to_image"}` from that image, or `beatra.images.generate` after `{"capability": "text_to_image"}` when there is no image. Later posters are `beatra.images.transform` from the accepted poster. The name, time, and offer sit in a clear band; one `beatra.images.edit` after `{"capability": "image_edit"}` sets those exact words if they come back wrong.
3. `beatra.voices.list`, then one `beatra.speech.synthesize` after `{"capability": "text_to_speech"}`. A supplied sample is one `beatra.voices.clone` after `{"capability": "voice_clone"}`, only after the user confirms the rights. One instrumental `beatra.music.generate` after `{"capability": "text_to_music"}`.
4. Materials card, then the video card: one `beatra.videos.animate` after `{"capability": "image_to_video"}` from the vertical poster, the read as `driving_audio`, a model that admits it.
5. One `beatra.videos.compose` keeps the read and ducks the jingle. Poll with `beatra.tasks.get` and deliver the kit plus `billing.net_charged_credits`.

## Decisions that require confirmation

Planning and the written deliverable are free. They are not approval.

Before every paid call, show a current production card and wait:

1. Work — what will be made, in the user's words, and whether this call is a generate, a clone, or a lookup.
2. Credits — the live price just read from the model card. Do not reuse a remembered number.
3. Count — one paid call per slot. The materials card may list the posters, the read, and the jingle; each slot has its own `client_request_id`. The teaser waits for its own card.
4. Identity — one new opaque `client_request_id` per call. A changed prompt, file, model, or control mints a new ID.
5. If we stop here — the free writing remains usable.
6. If the balance is insufficient — relay the official message and its top-up URL. Do not retry until the user says they have topped up.

A voice clone is its own card. Submit it only after the user confirms they have the rights to that sample, with `consent_attested` true. A lookup and a generate are two cards. Approved posters and audio do not authorize the teaser. Invoke every remote Beatra tool only through the bundled `scripts/mcp_client.py`. The tool name is the command argument and the JSON arguments are the standard input. Do not configure, call, or use a host Beatra Connector. Do not use REST/OpenAPI as a fallback.

If a create response is lost, retry only the identical payload and the same `client_request_id`. If the task id is lost, call `beatra.tasks.list`, then `beatra.tasks.get`, and match the frozen request before any identical retry. Call `beatra.tasks.cancel` only when the user asks to cancel, then confirm that task with `beatra.tasks.get`.

When the user asks how many credits remain, call `beatra.wallet.get`. When they ask what was charged, call `beatra.wallet.ledger`.

## References by task

Read [the scenario workflow](references/workflow.md) for the teaser payload and a worked kit.
Read [answers when a run goes wrong](references/faq.md) when a task stalls, a response is lost, a price looks wrong, or the poster lost the time or the offer.
Read [installation and authentication](references/installation-and-auth.md) when the connection is not ready.
Read [installation registration](references/installation-registration.md) for first-use registration.
Read [Bundled MCP Client diagnostics](references/mcp-connection.md) when a call fails before a task exists.
Read [tasks and results](references/tasks-and-results.md) when a task is queued, running, or missing.
Read [billing, errors, and recovery](references/billing-errors-and-recovery.md) when a charge, a refund, or a lost response needs the shared rules.
Read [uninstall and disconnect](references/uninstall-and-disconnect.md) when the user wants to stop and remove the connection.

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
