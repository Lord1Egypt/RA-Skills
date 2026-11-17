# ABS agent API

Base: `<site>/api/agent/v1`, where `<site>` is `base_url` in this skill's `config.json`
(for example `https://www.ucai.net`). Every call sends the user's access token — except `GET /search`,
which also works without one (anonymous, capped per network address):

```
Authorization: Bearer abs_pat_…
```

The token acts as the user (same role, visibility and expiry) and works only on this API.
`lang` is `zh` or `en` and sets the language of the answer, titles and links.

| Method and path | Body / query | Returns |
|---|---|---|
| `GET /me` | – | `user`, `site`, `token`, `can` (search, ask, learn, plan, diagnose, save_diagnosis) |
| `GET /search` | `q`, `limit` (1–20, default 8), `lang` | `results[]`: kind, id, title, url, excerpt, provenance, provenance_label; rules also status, status_label; `signed_in`; without a token also `note` |
| `POST /ask` | `{"question", "lang"}` | `answer` (with `[Source N]` / `[来源N]`), `sources[]`: ref, kind, id, title, url, provenance, status |
| `GET /cards/{id}` | `lang` | `id`, `name`, `markdown`, `url`, `provenance`, `sources[]` (file, pages, note), `rules[]` (key, value, status, status_label, note, source), `pages[]` (pdf, pages, topic, check) |
| `GET /courses` | `lang` | `courses[]`: id, title, summary, lessons, progress, url |
| `GET /courses/{id}` | `lang` | `title`, `summary`, `lessons[]`: title, objective, points, task, check, pages, url |
| `GET /pages/{pdf}/{page}` | – | one original page as `image/png` (shares the web reader's limit, about 40 pages a minute) |
| `POST /plans` | `{"question", "lang", "start_date"}` | `code`, `status`, `markdown`, `no_flow_reason`, `url` |
| `GET /plans/{code}` | – | same as above (own plans only) |
| `GET /plans?limit=20` | – | `plans`: your own plans, newest first (`code`, `status`, `question`, `proposed_at`, `url`) |
| `POST /diagnoses` | `{"question", "company", "filename", "content_base64", "lang", "save"}` | `answer`, `sources[]`, `saved_id`, `url` |

Limits per user per minute, shared with the web app: search 30, ask 20, plans 6, diagnoses 5, pages 40.
Without a token, search is limited per network address per minute and per day.

Rule `status`: `textbook` (stated in the source material), `industry_standard` (not in the textbook, or from a
non-Danaher source), `design_decision` (ABS's own judgement), `customer_calibrated` (set per customer).
`provenance: non_dbs_external` marks material from another company.

Errors: `401` token missing, invalid, revoked or expired (the response has `WWW-Authenticate: Bearer`);
`403` the role cannot do it; `404` not found or not visible; `413` file too large; `429` too many calls;
`503` the AI model is unavailable.

## curl

```bash
curl -H "Authorization: Bearer $ABS_TOKEN" "https://www.ucai.net/api/agent/v1/search?q=SMED&lang=en"
```

```bash
curl -X POST -H "Authorization: Bearer $ABS_TOKEN" -H "Content-Type: application/json" \
  -d '{"question":"How do I set takt time for a new cell?","lang":"en"}' \
  https://www.ucai.net/api/agent/v1/ask
```

The skill package itself: `GET <site>/api/agent/skill.zip` (public) · `GET <site>/api/agent/skill.md` (public).
