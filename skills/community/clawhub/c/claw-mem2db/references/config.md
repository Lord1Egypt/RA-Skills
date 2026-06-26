# Configuration

`claw-mem` reads `~/.claw-mem/config.json`. The `CLAW_MEM_DATA_DIR` env var overrides the dataDir.

## Memory-layer fields (owned by claw-mem)

```json
{
  "enabled": true,
  "dataDir": "~/.claw-mem",
  "tokenBudget": 8000,
  "maxObservations": 50,
  "maxSummaries": 10,
  "dedupWindowMs": 30000,
  "skipTools": ["TodoWrite", "AskUserQuestion", "Skill"]
}
```

### `tokenBudget`

Hard cap on how many tokens of memory context are injected. 8000 is a reasonable default for a 200K context model; turn down if prompts are already tight.

### `maxObservations` / `maxSummaries`

Ceiling on how many items `buildContext` considers. Higher = more recall, worse latency.

### `dedupWindowMs`

If the same tool call (same content hash) happens within this window, only one observation is recorded. Reduces noise from repeated operations like `ls` or `pwd`.

### `skipTools`

Observer ignores these tool names entirely — they produce no observation. Useful for:
- Meta-tools that don't produce domain knowledge (`TodoWrite`, `AskUserQuestion`, `Skill`)
- Read-only exploration that would flood memory (`Read`, `Glob` — consider adding these for large codebases)

## Umbrella composition (for the full claw-mem binary)

When installed as the full `@chainofclaw/claw-mem` package, config also inherits:

- `storage.*` — owned by the underlying `@chainofclaw/node` library
- `node.*` — same
- `backup.*` / `backup.carrier.*` — owned by `@chainofclaw/soul`
- `bootstrap.*` — meta

See [`coc-node` references/config.md](https://clawhub.ai/skill/coc-node) and [`coc-soul` references/config.md](https://clawhub.ai/skill/coc-soul) for details on those subtrees.

## Modify config safely

```bash
claw-mem config set tokenBudget 12000
claw-mem config set skipTools '["TodoWrite","AskUserQuestion","Skill","Read"]'
```

For JSON arrays / objects pass them inside single quotes. `config set` carefully does **not** coerce hex strings (like `0xac09…`) to numbers.
