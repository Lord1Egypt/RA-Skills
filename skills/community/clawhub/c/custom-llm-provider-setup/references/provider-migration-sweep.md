# Provider Migration Sweep — moving a running Hermes stack to a new provider

Use when the main model/provider changes (e.g. migrating off a credit-burning
free-tier proxy to a hosted catalog like NVIDIA NIM): every LLM consumer must
be repointed, not just the headline model. A half-swept stack silently keeps
billing the old provider through auxiliary tasks and delegation children.

## Where the LLM pins live (all under `~/.hermes/config.yaml`, plus one per profile)

| Pin | Keys | Default value to know about |
|---|---|---|
| Main agent | `model.provider`, `model.default`, `model.base_url`, `agent.reasoning`, `agent.reasoning_effort` | — |
| Auxiliary tasks (17) | `auxiliary.<task>.provider/.model/.base_url` for: vision, compression, skills_hub, approval, mcp, title_generation, tts_audio_tags, triage_specifier, kanban_decomposer, profile_describer, curator, monitor, background_review, moa_reference, moa_aggregator, web_extract, session_search | many default to `provider: auto`, which can route to OpenRouter on its own |
| Delegation children | `delegation.provider/model/base_url` | empty by default — children silently inherit the main model |
| Cron | `cron.provider` | `openrouter` |
| MOA presets | `moa.presets.<name>.reference_models[]`, `.aggregator`, plus legacy top-level `moa.reference_models/aggregator` | often hold stale model slugs even while disabled |
| Profiles | same keys under `~/.hermes/profiles/<name>/config.yaml` | cloned configs keep OLD pins — a profile sweep is mandatory |

## Procedure

1. **Backup first**: `cp <config.yaml> <config.yaml>.bak-<slug>` for the default and every profile config you will touch.
2. **Probe every candidate model** (see SKILL.md validation section) before writing any config. Present the probe table to the user and let them pick the roster.
3. **Scalars via `hermes config set`** (the `patch` tool refuses config.yaml). For each auxiliary task: `hermes config set auxiliary.<task>.provider <p>` + `.model` + `.base_url`. Then `delegation.*`, `cron.provider`, `agent.reasoning*`.
4. **Sweep profiles**: repeat step 3 with `--profile <name>` for each profile, plus their `model.default`. Do not assume profile configs share the default's pins — clones diverge the day they are made.
5. **Neutralize stale MOA blocks**: even a disabled `moa:` preset section can reference the old provider. A targeted `str.replace('provider: openrouter', 'provider: nvidia')` python edit is acceptable when the block is inert; verify with grep afterwards.
6. **Verify no old-provider stragglers**: `grep -n '<old-provider>'` across default + profile configs. Distinguish inert leftovers (provider-scoped config sections like `openrouter:` response-cache settings; another provider's own catalog slugs) from live pins — only live pins must be zero.
7. **Validate YAML**: `python3 -c "import yaml; yaml.safe_load(open(f))"` for every file you touched.
8. **Live smoke test**: `hermes chat -Q --provider <p> -m <model> -q "Reply with the single word OK"` — expect `OK`.
9. **Restart with drain**: `hermes gateway restart` waits for in-flight turns; then `hermes gateway status` must show every profile serving. Finish with `hermes doctor`.
10. **Day-after audit**: `hermes insights --days 1` — old-provider spend must be $0; any residual usage names its consumer, repoint it.

## Rate-budget sizing (free tiers)

Free tiers usually share one requests-per-minute budget across ALL models (NIM: ~40 RPM global). Size the stack to it:

- Parent + aux + delegation children share the budget; on shared RPM, single-model stacks survive but multi-tier fallback chains only catch model-specific errors — a provider-wide 429 is better absorbed by `agent.api_max_retries`.
- Halve `delegation.max_concurrent_children` from 12 to ~6 when moving onto a shared free-tier budget.
- MOA multiplies calls per turn (council = 1 main + N refs + 1 aggregator). Keep `moa.enabled: false` globally and activate per session only when the RPM budget allows.

## Pitfalls

- The `-Q` one-shot flag requires `-q "<prompt>"` for the prompt — a bare positional prompt is rejected as an unrecognized argument.
- A probe `200` on a small prompt does not guarantee usable agent behavior on long prompts — the user's live trial is the final gate.
- Third-party "free models" listings can be wrong about what the provider actually serves free; the account's own model list + probe is ground truth.
- A bare-probe `500` is NOT proof a model is broken. Minimal probes (no tools, no streaming, tiny `max_tokens`) do not represent agent traffic — models that only serve on a Responses-API transport fail `chat_completions` probes while working fine in live sessions. Before declaring a model dead: check the provider's own model list (absence there is a real verdict), try the other endpoint, and weight live traffic over any probe. Label negative probe findings as probe-scoped — wrongly calling a working model dead silently removes it from the fleet and misconfigures the stack.
- A model that 500s on probes but answers in real traffic can still be promoted — but note the transport caveat (e.g. Responses-API-only model behind a `codex_responses` `api_mode`) in any fleet documentation so future probes are read correctly.
- Price-shape the fleet before slotting models: flat-priced models remove peak/off-peak multipliers (e.g. DeepSeek-style 2x peak pricing) from the highest-volume slots (delegation defaults, aux tasks). A capped/promo-allowance model is a natural delegation default for short child contexts.
- `providers:` entries for old providers can stay in config (as emergency fallbacks) — presence is not a live pin; only grep hits inside `model:`/`auxiliary:`/`delegation:`/`cron:`/`moa:` blocks count as consumers.
