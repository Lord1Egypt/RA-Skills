# Free models

Read this when the user wants a free model, or a free model answers 429. The
main Skill is <https://beatapi.io/skill.md>.

The set of free models changes without notice; never hardcode ids. List what is
free right now with Search:

```sh
curl -sS -X POST https://api.beatapi.io/v1/capabilities/search \
  -H 'Content-Type: application/json' -d '{"query":"free","kind":"model"}'
```

- A card whose `price` reads `$0 input / $0 output per 1M tokens` is free.
  Today their ids end in `-free`.
- A free model runs like any text model:
  `{"reference":"model:<id>","input":{"input":"<prompt>"}}`. The same id also
  works on `/v1/chat/completions` and `/v1/responses`.
- Inspect shows its limit under `limits.rate_limit`:
  `successful_requests_per_minute_before_first_top_up` (1) and
  `successful_requests_per_minute_after_top_up` (10), counted per account apart
  from the normal rate limit. Read the numbers from Inspect rather than from
  this page.
- A 429 on a free model carries code `rate_limit_exceeded`: wait
  `error.retry_after_seconds`, or Search for the paid model of the same family
  (its id is not always the free id minus `-free`).
- Free models come with no stability guarantee and can be limited or withdrawn
  at any time; how long one stays available is not promised. A daily allowance
  may apply and is adjusted over time.
- A decision model is among them: `model:jev-1.13-free`. It takes `state` and
  `questions` instead of a prompt:
  <https://beatapi.io/skill-refs/recipes/decide-with-jev.md>.
