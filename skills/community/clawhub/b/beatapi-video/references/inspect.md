# Inspect: read a capability's contract

Read this when you need a capability's inputs, readiness, price tiers or
`schema_hash`. Step 2 of the Search → Inspect → Run loop in the main Skill
(<https://beatapi.io/skill.md>). Inspect needs no key.

```sh
curl -sS -X POST https://api.beatapi.io/v1/capabilities/inspect \
  -H 'Content-Type: application/json' -d '{"reference":"data:xiaohongshu.app_v2.search_notes"}'
```

Over MCP, pass the same JSON to `capabilities_inspect`.

Read `input_schema` (required fields, types, limits), `pricing`, `execution.mode`
(`sync` answers directly, `async` returns a task) and `readiness`:

| readiness | meaning |
| --- | --- |
| `ready` | input, output and price are published |
| `runnable` | runs; the output shape is not published, so read what you need from `data` |
| `listed` | cannot run through Run; `next` says why. Search for an alternative |

`pricing.price_usd` is the cheapest published shape (a Search card shows it as
"from $…"); `pricing.tiers` lists every shape with its price (veo-3.1: Lite
$0.15, Quality $1.85 for the same 8 s). Pick the tier before a paid run; the
task's `credits_reserved` is that tier's price.

A guessed or misspelled reference returns 404 with `suggestions`. `schema_hash`
fingerprints `input_schema` and `output_schema` together: cache a contract by it,
and re-inspect only when a later reply shows a different hash.
