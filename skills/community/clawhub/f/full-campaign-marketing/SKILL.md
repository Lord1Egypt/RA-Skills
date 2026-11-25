---
name: "full-campaign-marketing"
description: "Turn a product and an audience into one full-campaign marketing pack: topics taken from public posts, one poster, one product clip, and one jingle. Full-campaign marketing writes the plan, then makes the pictures, clip, and music. Use it when one offer should leave as a set of publishable pieces the same day."
---

# Full-campaign Marketing

## What you get

- A campaign plan: the offer, the audience, the topics worth using, and the line each piece will say.
- One poster. A product photo, when you supply one, is the product on that poster.
- One spoken product clip made from the poster, under ten seconds.
- One instrumental jingle, ducked under the voice in the finished clip.

## Ways to run it

- Plan and pieces. The default. The plan is free, then the poster, the clip, and the jingle.
- Plan only. Strike the pieces on the card.
- With a live read. One public lookup before the plan is frozen, on Douyin, Xiaohongshu, or TikTok, including comments when the line should use buyer language.

Open this when one offer should leave the same day as a poster, a spoken clip, and a jingle.

## Scope and adjacent routes

Use this route when one offer should leave as a small set of pieces, not when the job is only a poster or only a review of files you already have. A product listing set belongs on a product-asset workflow. A review of finished files belongs on a marketing-asset review.

## Inputs and defaults

The hard input is the product and who it is for. Ask only for that. Default to one vertical poster, one vertical clip under ten seconds that speaks, one instrumental jingle, and the clip joined with that jingle. Do not invent ad-account numbers, store sales, live-room data, or WeChat metrics. Public posts are the only outside read.

## Golden path

1. Write the campaign plan and show it. This writing is free.
2. If a live read is in scope, use `beatra.social.tools.search` and `beatra.social.tools.get`, copy `schema_hash`, show a lookup card, and call `beatra.social.execute` once. Allowed keys are `social.douyin.hot_search.list`, `social.douyin.video.search`, `social.douyin.video.comments.list`, `social.xiaohongshu.note.search`, `social.xiaohongshu.note.comments.list`, `social.tiktok.video.search`.
3. Upload a product photo with `beatra.assets.upload` when one is supplied. The poster is `beatra.images.transform` after `{"capability": "image_to_image"}` from that photo, or `beatra.images.generate` after `{"capability": "text_to_image"}` when there is no photo. One `beatra.images.edit` repairs a poster that lost the product.
4. `beatra.voices.list`, then one `beatra.speech.synthesize` after `{"capability": "text_to_speech"}` of the clip's line. One instrumental `beatra.music.generate` after `{"capability": "text_to_music"}`.
5. Materials card, then the video card: one `beatra.videos.animate` after `{"capability": "image_to_video"}` from the poster, the line as `driving_audio`, a model that admits it, duration the next whole second and under ten.
6. One `beatra.videos.compose` keeps the line's sound and ducks the jingle. Poll with `beatra.tasks.get` and deliver the plan, the poster, the clip, and `billing.net_charged_credits`.

## Decisions that require confirmation

Planning and the written deliverable are free. They are not approval.

Before every paid call, show a current production card and wait:

1. Work — what will be made, in the user's words, and whether this call is a generate or a lookup.
2. Credits — the live price just read from the model card or from `beatra.social.tools.get`. Do not reuse a remembered number.
3. Count — one paid call per slot. The materials card may list the poster, the line, and the jingle; each slot has its own `client_request_id`. A later lookup page is another call. The clip waits for its own card.
4. Identity — one new opaque `client_request_id` per call. A changed prompt, file, model, or control mints a new ID.
5. If we stop here — the free writing remains usable.
6. If the balance is insufficient — relay the official message and its top-up URL. Do not retry until the user says they have topped up.

A lookup and a generate are two cards. Approved posters, lines, and jingles do not authorize the clip. Invoke every remote Beatra tool only through the bundled `scripts/mcp_client.py`. The tool name is the command argument and the JSON arguments are the standard input. Do not configure, call, or use a host Beatra Connector. Do not use REST/OpenAPI as a fallback.

If a create response is lost, retry only the identical payload and the same `client_request_id`. If the task id is lost, call `beatra.tasks.list`, then `beatra.tasks.get`, and match the frozen request before any identical retry. Call `beatra.tasks.cancel` only when the user asks to cancel, then confirm that task with `beatra.tasks.get`.

When the user asks how many credits remain, call `beatra.wallet.get`. When they ask what was charged, call `beatra.wallet.ledger`.

## References by task

Read [the scenario workflow](references/workflow.md) for the clip payload and a worked pack.
Read [answers when a run goes wrong](references/faq.md) when a task stalls, a response is lost, a price looks wrong, or the poster lost the product.
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
