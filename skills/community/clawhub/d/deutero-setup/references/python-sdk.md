# The Python SDK

`deutero` is the official Python client for the same Study Management API the MCP tools come from. It is how a **server or script** calls Deutero: a webhook receiver, a nightly reconciliation job, a CI step that rebuilds a study from a file, a notebook pulling transcripts. An agent in a session should still use the MCP tools; reach for the SDK when the code you are writing has to run without you.

Contents:
1. Install and authenticate
2. MCP tool → SDK method
3. Conventions that differ from MCP
4. Errors
5. Verifying webhooks
6. Things that catch people out

---

## 1. Install and authenticate

```bash
pip install "deutero>=0.2"      # or: uv add "deutero>=0.2"
```

Python 3.9+; depends only on `httpx` and `pydantic` v2. **Require 0.2 or later.** 0.1.x targeted an older API (`/api/v1/surveys/…`, `studies.generate`, thematic analysis, credit estimates) that no longer exists, so code or answers written against 0.1 will call methods that are gone. If `pip` cannot find 0.2, install from the repository: `pip install "git+https://github.com/deutero-ai/deutero-python"`.

```python
from deutero import Deutero

client = Deutero()                     # reads DEUTERO_API_KEY
client = Deutero(api_key="dtro_…")     # or explicitly
```

The key is an ordinary organization API key from **Settings → Generate API Key** (`mcp-clients.md`), sent as `X-API-Key`. No key is a `ValueError` at construction, not a 401 later. Defaults: base URL `https://dashboard.deutero.ai/study-api`, 120-second timeout; override with `base_url=` / `timeout=`, or pass your own `httpx.Client` as `http_client=` for proxies or retries (the SDK still adds the key header and base URL).

`AsyncDeutero` has identical methods, awaited:

```python
async with AsyncDeutero() as client:
    stats = await client.studies.get_stats(study_id)
```

Use either as a context manager (or call `close()`) so the connection pool is released.

## 2. MCP tool → SDK method

Every MCP tool — except the four generators and the four publication tools listed after the table — is one SDK method with the same parameters, spelled as Python keyword arguments. IDs are positional; everything else is keyword-only.

| MCP tool | SDK |
|---|---|
| `list_projects` / `create_project` / `get_project` / `update_project` | `client.projects.list()` / `.create(name=, description=)` / `.get(id)` / `.update(id, …)` |
| `list_studies` / `create_study` / `get_study` / `update_study` / `get_study_stats` | `client.studies.list(project_id)` / `.create(project_id=, name=, …)` / `.get(id)` / `.update(id, …)` / `.get_stats(id)` |
| `get_welcome` / `set_welcome` | `client.welcome.get(id)` / `.set(id, message=, consent=)` |
| `list_welcome_translations` / `upsert_welcome_translation` / `delete_welcome_translation` | `client.welcome.list_translations(id)` / `.upsert_translation(id, target_language=, translation_text=)` / `.delete_translation(id, translation_id)` |
| `get_screening` / `set_screening_settings` | `client.screening.get(id)` / `.set_settings(id, enabled=, …)` |
| `create_` / `update_` / `delete_` / `reorder_screening_question(s)` | `client.screening.create_question` / `update_question` / `delete_question` / `reorder_questions(id, question_ids=)` |
| `*_characteristic*` | `client.characteristics.*` — same shape as screening |
| `list_questions` / `create_question` / `update_question` / `delete_question` / `reorder_questions` / `validate_questions` | `client.questions.list` / `create` / `update` / `delete` / `reorder` / `validate` |
| `get_graph` / `set_graph` / `patch_graph` / `check_graph` | `client.graph.get` / `set(id, flow=, expected_graph_version=)` / `patch(id, ops=, expected_graph_version=)` / `check(id, flow=)` |
| `import_questions_to_graph` / `activate_graph` / `deactivate_graph` / `get_flow_signals` / `describe_graph_nodes` | `client.graph.import_questions` / `activate` / `deactivate` / `get_signals` / `describe_node_types()` |
| `get_recruitment` / `update_recruitment` | `client.recruitment.get(id)` / `.update(id, short_url_slug=, max_responses=, clear_max_responses=, redirect_url=)` |
| `list_embed_keys` / `create_embed_key` / `update_embed_key` / `get_embed_snippet` | `client.embed.list_keys()` / `.create_key(allowed_origins=, study_id=, …)` / `.update_key(key_id, …)` / `.get_snippet(id, publishable_key=, mode=)` |
| `list_personas` / `create_persona` / `update_persona` / `delete_persona` / `generate_personas` | `client.personas.list` / `create(id, content=)` / `update` / `delete` / `generate(id, count=, save=)` |
| `run_simulation` / `list_simulations` / `get_simulation` / `delete_simulation` | `client.simulations.run(id, persona_id= or persona=, model_tier=)` / `.list(id, status=, …)` / `.get(sim_id)` / `.delete(sim_id)` |
| `list_interviews` / `find_interviews_by_external_id` / `get_interview` / `get_transcript` / `get_interview_fetches_and_signals` | `client.interviews.list(id, completed=, simulated=, external_participant_id=, started_after=, started_before=, limit=, offset=)` / `.find_by_external_id(id, external_participant_id=)` / `.get(iid)` / `.get_transcript(iid)` / `.get_fetches_and_signals(iid)` |
| `bulk_transcripts` / `search_transcripts` | `client.transcripts.list(id, completed=, include_simulated=, …)` / `.search(id, q=, mode=, question_id=, …)` |
| `list_analyzable_questions` / `get_scale_responses` / `get_options_responses` | `client.analysis.list_questions(id, category=)` / `.get_scale_responses(id, question_id=)` / `.get_options_responses(id, question_id=)` |
| `run_clustering` / `get_optimal_clusters` / `get_latest_clustering` | `client.analysis.cluster(id, question_id=, n_clusters=)` / `.get_optimal_clusters(id, question_id=)` / `.get_latest_clustering(id)` |
| `list_webhook_event_types` / `list_webhooks` / `create_webhook` / `update_webhook` / `delete_webhook` / `rotate_webhook_secret` / `list_webhook_deliveries` | `client.webhooks.list_event_types()` / `.list()` / `.create(label=, url=, events=)` / `.update(wid, …)` / `.delete(wid)` / `.rotate_secret(wid)` / `.list_deliveries(wid, event_type=, success=, …)` |
| `get_credit_balance` / `health_health_get` | `client.credits.get_balance()` / `client.health()` |

**Not in 0.2 yet: the generators.** `draft_study`, `draft_study_from_site`, `generate_questions` and `generate_welcome` were added to the API after SDK 0.2 shipped, so they have no method. From code, call the REST routes directly with the same `X-API-Key`, under `https://dashboard.deutero.ai/study-api/api/v1`:

| MCP tool | REST |
|---|---|
| `draft_study` | `POST /study-drafts` |
| `draft_study_from_site` | `POST /study-drafts/from-site` |
| `generate_questions` | `POST /studies/{study_id}/questions/generate` |
| `generate_welcome` | `POST /studies/{study_id}/welcome/generate` |

These are not 0.1's removed `studies.generate`. A study draft and a welcome draft store nothing — pass the fields to `client.studies.create`, or the text to `client.welcome.set`, yourself; `generate_questions` saves what it writes. Allow for the latency — twenty seconds to two minutes — in your HTTP timeout.

**Not in 0.2 yet: participant contacts.** The contact step and its tools came after 0.2. Its settings are a `contact` object on `PUT /studies/{study_id}/characteristics/settings` (`collect_email`, `collect_phone`, `timing`, `required`, `message`); the details people gave are personal data, read with:

| MCP tool | REST |
|---|---|
| `list_study_contacts` | `GET /studies/{study_id}/contacts?include_declined=&completed=&test_runs=&limit=&offset=` |
| `get_interview_contact` | `GET /interviews/{interview_id}/contact` |

**Not in 0.2 yet: publication.** Publishing, pausing and validating a study also came after 0.2. Same base URL and key:

| MCP tool | REST |
|---|---|
| `get_publication_status` | `GET /studies/{study_id}/publication` |
| `validate_study` | `POST /studies/{study_id}/validate` |
| `publish_study` | `POST /studies/{study_id}/publish` (JSON body required, `{}` at minimum; optional `acknowledge_validation_run_id`, `acknowledge_credit_shortfall`) |
| `pause_study` | `POST /studies/{study_id}/pause` |

**Not in 0.2 yet: image uploads.** Images for `present_images` questions and flow steps, base64 in a JSON body (`{"image_base64": "…", "label": "…"}`):

| MCP tool | REST |
|---|---|
| `upload_question_image` | `POST /studies/{study_id}/questions/{question_id}/images` (optional `position`) |
| `delete_question_image` | `DELETE /studies/{study_id}/questions/{question_id}/images/{image_id}` |
| `upload_flow_image` | `POST /studies/{study_id}/graph/images` (returns the `url` for a step's `images`) |

**Not in 0.2 yet: branding.** The brand theme, the start screen's hero image and the welcome's start-screen copy came after 0.2. `client.welcome.set` sends only `message` and `consent`, so set the copy fields (`title`, `time_estimate`, `footer`, `continue_label`, `consent_yes_label`, `consent_no_label`, `hero_alt`) with the REST `PUT`:

| MCP tool | REST |
|---|---|
| `get_theme` | `GET /theme` (optional `?study_id=`) |
| `set_theme` | `PUT /theme` (`{"theme": {…}, "custom_css": "…", "study_id": "…"}`; fields left out are unchanged) |
| `set_welcome` with start-screen copy | `PUT /studies/{study_id}/welcome` |
| `upload_welcome_hero` / `delete_welcome_hero` | `POST` / `DELETE /studies/{study_id}/welcome/hero` (`{"image_base64": "…", "alt": "…"}`) |

`plan-interview-research/references/branding.md` has the fields and refusals.

A refusal comes back as a non-2xx whose JSON `detail.code` names the reason (`plan-interview-research/references/publishing.md`). In the SDK's error types, that's a `ConflictError` for `study_locked` on any locked write. A script that publishes should branch on the code, not on the status: 402 covers both `plan_limit_reached` and credits, and 409 covers both `credit_shortfall` and `validation_issues`. SDK 0.2's study models predate `status`, so if your version doesn't expose it, read it from `GET /studies/{study_id}` directly. Validation can take a minute, so size the timeout for it.

The renames worth remembering: `run_clustering` → `analysis.cluster`, `bulk_transcripts` → `transcripts.list`, `search_transcripts` → `transcripts.search`, `list_analyzable_questions` → `analysis.list_questions`, `describe_graph_nodes` → `graph.describe_node_types`.

## 3. Conventions that differ from MCP

- **`None` means "not sent".** An argument left as `None` is omitted from the request, so the server default applies, and on an `update` the field is left unchanged. You cannot clear a field by passing `None`; use the explicit clear flag where one exists (`clear_max_responses=True`).
- **Responses are Pydantic models**, not dicts — `study.id`, `stats.completed_interviews`, `page.interviews`. `model_dump()` when you need a dict. IDs come back as `uuid.UUID`; every method accepts a `str` or a `UUID`.
- **`qtype` is inferred when omitted**: `scale=` → scale, `options=` → choices, `slots=` → slots, `expected_image=` → image_upload, otherwise text. Name it anyway when it matters; an inferred type is a silent one. Field names inside configs are the API's (`{"minScale": 1, "maxScale": 5, …}`) — `plan-interview-research/references/question-types.md` has them.
- **Flows and patch ops** take plain dicts in the API's JSON shape or the typed `FlowDocument` / `FlowNode` / `FlowEdge` / `PatchOp` models. On the models, the keywords `from` and `class` are `from_` and `class_`.
- **Pagination is yours.** `interviews.list` returns `total`, `limit`, `offset` and one page (server default 50). A sweep loops on `offset` until it has `total` rows.
- **Simulations run in the background.** `simulations.run` returns at once; poll `simulations.get(run.id)` while `status == "running"`, every 10 seconds or so.
- **Enums** — `StudyType`, `ModelTier`, `NodeType`, `SearchMode`, `AnalysisCategory` — are importable from `deutero` and accepted wherever a string is. `ModelTier` is `open_weights` / `standard` / `premium`; there is no `FRONTIER` member (the API still accepts the string as an alias). The model tier is still the user's decision — `plan-interview-research` says why — so a script takes it as input rather than hard-coding one.

## 4. Errors

Every non-2xx raises; nothing returns an error body for you to inspect.

| Status | Exception | Usual meaning |
|---|---|---|
| 400, 422 | `ValidationError` | bad arguments; also an invalid flow on `graph.set` / `graph.patch`, with the problems in `e.body` |
| 401 | `AuthenticationError` | key wrong, disabled or deleted |
| 402 | `InsufficientCreditsError` | out of credits |
| 403 | `PermissionDeniedError` | the plan does not include the feature (`plan-limits.md`) |
| 404 | `NotFoundError` | wrong ID, or another organization's |
| 409 | `ConflictError` | stale `expected_graph_version` — re-read `graph.get` and retry; or `study_locked` — the study is open, pause it before editing |
| 429 | `RateLimitError` | back off |
| 5xx | `InternalServerError` / `BadGatewayError` | server side |

All are `APIError` (with `.status_code`, `.message`, `.body`), which is a `DeuteroError`; `ConnectionError`, `TimeoutError` and `WebhookVerificationError` are `DeuteroError` too. The SDK does not retry — bring an `httpx` transport with retries if a job needs them.

**`PermissionDeniedError` is a subclass of `AuthenticationError`.** Catch it first, or a plan gate is reported as a bad key and someone regenerates a key that was fine:

```python
from deutero import AuthenticationError, PermissionDeniedError

try:
    client.simulations.run(study_id, persona_id=persona_id)
except PermissionDeniedError as e:     # 403 — plan, not credentials
    print("Not on this plan:", e.message)
except AuthenticationError:            # 401
    print("API key rejected")
```

## 5. Verifying webhooks

`deutero.webhooks` verifies and parses what Deutero POSTs to a receiver. It needs no API key and makes no network call, so it is the right import in a receiver that never calls the API otherwise.

```python
from deutero import webhooks
from deutero.webhooks import InterviewCompletedEvent

try:
    # WEBHOOK_SECRET = os.environ["DEUTERO_WEBHOOK_SECRET"]  # read once at startup
    event = webhooks.unwrap(request.get_data(), request.headers, secret=WEBHOOK_SECRET)
except webhooks.WebhookVerificationError:
    abort(400)

if isinstance(event, InterviewCompletedEvent) and event.data.completed:
    ...  # event.data.external_participant_id, event.webhook_id
```

- Pass the **raw body bytes**. Anything re-serialised will not verify.
- The secret is the `whsec_…` value exactly as `create_webhook` / `rotate_secret` returned it. The same function verifies Interview Flow signals, with the per-step secret from `graph.get_signals`.
- The seven organization events parse into typed classes (`InterviewStartedEvent`, `InterviewCompletedEvent`, `AnalysisCompletedEvent`, `SimulationCompletedEvent`, `StudyCreatedEvent`, `CreditsExhaustedEvent`, `StudyFullEvent`). Flow signals and any type the SDK does not know come back as a plain `WebhookEvent` with `data` as a dict — so branch on `isinstance` or `event.type`, and ignore what you do not recognise.
- `event.webhook_id` is the `webhook-id` header: the deduplication key. `event.simulated` is true for a signal from a simulated interview.
- Timestamps more than 5 minutes from now are rejected; `tolerance=` changes that, `tolerance=None` disables it for replaying stored deliveries.
- `webhooks.verify(...)` checks without parsing; `webhooks.sign(body, secret=, msg_id=)` builds valid headers for testing your receiver locally; `webhooks.parse_event` parses **without verifying** and belongs in tests only.

`recruit-participants/references/webhook-events.md` has the payloads and the delivery semantics — one attempt, no retries — which the SDK does not change.

## 6. Things that catch people out

- **Using 0.1.x.** See §1. If a call like `client.studies.generate`, `client.studies.set_model_tier`, `client.analysis.run` or `client.credits.estimate_*` appears in code you are asked to fix, it was written for the old API; port it rather than debugging it.
- **Catching `AuthenticationError` before `PermissionDeniedError`.** See §4.
- **`simulated` vs `include_simulated`.** `interviews.list` takes `simulated`; `interviews.find_by_external_id` and `transcripts.list` / `.search` take `include_simulated`. Both default to real interviews only. Leave that default alone in anything that pays people.
- **Test runs** (the researcher's own Try Interview / Preview interviews) are left out by the server unless asked for, so SDK 0.2 calls already return participants only. The switches (`test_runs` on `GET /studies/{id}/interviews`, `include_test_runs` on the by-external-id, transcripts and search routes) and the `test_run` field on every row are newer than 0.2. To ask for test runs, or to read `test_run`, call REST.
- **`survey_id` is the study ID** in webhook payloads and some responses, under its older name.
- **Secrets shown once.** `webhooks.create`, `webhooks.rotate_secret` and `embed.create_key` return a signing secret exactly once. Write it to the secret manager in the same code path that created it.
- **Putting the key in code.** `Deutero()` with `DEUTERO_API_KEY` in the environment is the whole point of the fallback; a key in a committed script is a leaked key.
