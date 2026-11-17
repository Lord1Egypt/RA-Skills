# check-ai-credits

**English** · [简体中文](README.zh-CN.md)

**Check AI provider credits and balance across 10 providers from one CLI.**
One command answers "how much credit do I have left?" for DeepSeek, DeepInfra,
Codex (ChatGPT), Grok, MiMo, Claude, Gemini, Kimi, OpenRouter and the
apikey.fun relay — with burn trend and estimated days-left.

- Single static binary (TypeScript + Bun), zero runtime dependencies
- Auto-discovers local credentials (env vars, CLI auth stores, CodexBar)
- Read-only: never refreshes or rewrites OAuth tokens, never prints secrets
- Uniform snapshot schema → JSON output ready for dashboards/cron

## Install

```bash
# as a skill (any Agent-Skills-compatible agent)
npx skills add mfang0126/check-ai-credits

# from source (requires Bun >= 1.1)
# clone this repository (ssh or https), then:
cd check-ai-credits && bun install && bun run build   # -> dist/check-ai-credits
```

## 60-second method

```bash
check-ai-credits                 # all configured providers
check-ai-credits deepseek        # one provider
check-ai-credits --json          # machine-readable snapshots
check-ai-credits --trend         # burn rate + days-left from logged history
check-ai-credits --list          # credential detection status per provider
check-ai-credits deepinfra --models   # per-model month breakdown (DeepInfra)
```

## Provider matrix

| Provider | ID | Credential source (auto-detected) | Metric |
|---|---|---|---|
| DeepSeek official | `deepseek` | `DEEPSEEK_API_KEY` (env / agent env file) | wallet balance USD |
| DeepInfra | `deepinfra` | `DEEPINFRA_API_KEY` (env / agent env file) | prepaid pool, month spend |
| Codex (ChatGPT) | `codex` | `~/.codex/auth.json` (Codex CLI, read-only) | credits + rate-limit window |
| Grok (xAI) | `grok` | `~/.grok/auth.json` (Grok CLI, read-only) | monthly credits + prepaid |
| Xiaomi MiMo | `mimo` | `MIMO_COOKIE` env, else CodexBar fallback | CNY balance + plan |
| Claude | `claude` | CodexBar usage | window used % |
| Gemini | `gemini` | CodexBar usage | window used % |
| Kimi | `kimi` | CodexBar usage | window used % |
| OpenRouter | `openrouter` | CodexBar usage | window used % |
| apikey.fun relay | `apikeyfun` | CodexBar plugin | shared wallet balance |

Providers whose credentials are not present report `not configured` with a
login/setup URL instead of failing the whole run.

## Credential resolution (per provider, in order)

1. Process environment variable
2. Your agent's env file (e.g. Hermes's `$HERMES_HOME/.env`; never exported)
3. Local CLI auth store (`~/.codex/auth.json`, `~/.grok/auth.json`) — **read-only**
4. CodexBar CLI (macOS menu-bar app) for web-session providers
5. Interactive fallback: the tool prints the login URL and exits non-zero

Security rules baked into the code: OAuth access tokens are never refreshed or
rewritten (re-refreshing would rotate the CLI's own refresh token and log you
out), secrets are never echoed in any output mode, and there is no telemetry.

## Evidence

| Capability | How it was verified |
|---|---|
| Balance semantics correct | Cross-checked at release time against an independent implementation (legacy Python direct-connect scripts kept outside this repo) on the same endpoints: DeepSeek balance and DeepInfra spendable/month matched exactly |
| Trend algorithm | 40 fixture tests cover 7-day least-squares, reset clipping, LOW thresholds (`bun test`) |
| Endpoint reality | Live smoke at release time against DeepSeek `GET /user/balance` ([platform.deepseek.com](https://platform.deepseek.com)), DeepInfra `/payment/checklist` ([deepinfra.com/dash](https://deepinfra.com/dash)) and the other providers' billing surfaces |
| Type safety | TypeScript strict `tsc --noEmit`, zero errors |

## JSON snapshot schema

```jsonc
{
  "provider": "deepseek",
  "source": "api",
  "timestamp": "2026-09-24T00:00:00.000Z",
  "currency": "USD",
  "balance": 12.34,
  "usedPercent": null,
  "resetsAt": null,
  "monthCost": null,
  "monthPeriod": null,
  "details": { },     // provider-specific extras
  "error": null
}
```

## Trend log

Snapshots are appended to `$CHECK_AI_CREDITS_LOG` (default
`~/.check-ai-credits/log.json`). `--trend` fits a least-squares burn rate over
a 7-day window, clips quota series before the last reset, and flags low
balances (USD wallet < 5, or < 20% remaining). Use `--no-log` to skip
appending.

## Repo layout

```
SKILL.md            # skill entry (frontmatter, ≤60-char description)
src/
  cli.ts            # CLI entry
  types.ts          # unified snapshot schema + Provider interface
  core/             # env/http/auth/codexbar/trend/log
  providers/        # one adapter per provider
  registry.ts       # 10-provider registry
  format.ts         # human-readable output formatting
test/               # bun:test fixtures (no live API calls)
docs/MIGRATION.md   # endpoint semantics + unit pitfalls
README.zh-CN.md     # Chinese version of this file
```

Adding a provider = one file in `src/providers/` implementing the `Provider`
interface (`detect()` + `fetch()`), one registry entry in `src/registry.ts`.

## Development

```bash
bun run typecheck   # tsc --noEmit, strict
bun test            # fixture-based unit tests (no live API calls)
bun run build       # single-file binary
```

## License

MIT
