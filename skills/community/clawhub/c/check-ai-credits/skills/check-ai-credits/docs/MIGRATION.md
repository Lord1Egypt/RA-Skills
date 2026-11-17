# Migration map: Python scripts → check-ai-credits

Reference while porting. Source of truth for endpoint semantics:
the legacy Python balance scripts (read-only; never modified by this project).

| Provider | Python source | TS target | Status |
|---|---|---|---|
| deepseek | `deepseek-balance.py` | `src/providers/deepseek.ts` | ported |
| deepinfra | `deepinfra-balance.py` | `src/providers/deepinfra.ts` (incl. `--models`) | ported |
| codex | `codex-balance.py` | `src/providers/codex.ts` | ported (read-only token) |
| grok | `grok-balance.py` | `src/providers/grok.ts` (credits unit, no USD conversion) | ported (read-only token) |
| mimo | `mimo-balance.py` | `src/providers/mimo.ts` (MIMO_COOKIE → CodexBar fallback) | ported; Chrome cookie decryption NOT ported (needs keychain → intentionally deferred, fallback covers macOS hosts) |
| claude/gemini/kimi/openrouter | CodexBar rows in `usage-logger.py` | `codexbarProvider()` factory | ported |
| apikeyfun | CodexBar plugin in `usage-logger.py` | `apikeyfunProvider` in `src/providers/codexbar.ts` | ported |
| logger/trend | `usage-logger.py` | `src/core/log.ts` + `src/core/trend.ts` | ported (7-day least squares, clip-after-reset, LOW flags) |

## Snapshot schema (kept from Python)

`provider, source, timestamp, currency, balance, usedPercent, resetsAt,
monthCost, monthPeriod, details, error` — `timestamp` is mandatory (trend
ordering depends on it). CodexBar extras (window/pace/resetDescription) live
under `details`.

## Known unit pitfalls carried over

- DeepInfra `/payment/usage` costs are **cents**; checklist amounts are USD.
  `available = (-stripe_balance) - recent`.
- Grok currency is `CREDITS`, never convert to USD.
- DeepInfra `topup_amount` / `topup_threshold` are integer cents.
- Never refresh OAuth tokens (codex/grok) — read-only by design.
- Relay keys against the official DeepSeek endpoint → 401 by design.

## Deferred (not in v0.1)

- Chrome cookie decryption for MiMo (keychain + AES-128-CBC) — port of
  `lib/provider_balance.py::chromium_cookies`; blocked by keychain prompt
  policy, add when explicitly authorized.
- npm/brew distribution packaging; Hub publish (external gate).
