---
name: baidu-text-translate
description: Use this skill whenever you need to translate text with the trans-cli tool (Baidu Translation AI API). Covers JSON output contract, Baidu-specific language codes (jp/kor/fra/spa/ara — not ISO defaults), exit code semantics, error decision tree, first-time API key setup, QUOTA_EXCEEDED / AUTH_FAILED recovery, environment self-diagnosis via `trans doctor`, and listing supported languages via `trans languages`. Trigger on any of: running `trans text`, shell pipelines with translation, trans-cli errors, API key configuration, `trans doctor` checks, or looking up language codes.
homepage: https://fanyi.baidu.com
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["trans"],"env":["TRANS_API_KEY"]},"install":[{"id":"npm","kind":"npm","package":"@bdtrans/trans-cli","bins":["trans"],"label":"Install trans-cli (npm)"}]}}
---

# baidu_text_translate — Agent Reference

`trans text` wraps the Baidu AI Translation API. Use `--json` — it separates
success (stdout) from errors (stderr) and gives you structured fields to act on.

```bash
trans text --json "你好世界"                             # auto-detect → English
trans text --json --from zh --to jp "你好"               # explicit languages
trans text --json --to fra --reference "使用正式语气" "你好"  # custom instruction
echo "早上好" | trans text --json                        # stdin pipe
```

---

## Environment Diagnosis

Before translating, verify the environment with `trans doctor`:

```bash
trans doctor           # human-readable output
trans doctor --json    # JSON output for Agent parsing
```

**JSON contract** (stdout):
```json
{
  "checks": [
    {"name":"api_key",     "ok":true,  "source":"env/config", "message":"configured"},
    {"name":"connectivity","ok":true,  "latency_ms":243,       "message":"reachable"},
    {"name":"account",     "ok":true,                          "message":"valid"}
  ],
  "all_ok": true
}
```

| Exit | `all_ok` | Meaning |
|------|----------|---------|
| 0 | `true` | All checks passed — ready to translate |
| 2 | `false` | At least one check failed — inspect `checks[].ok` |

**When a check fails**, `help_url` in the failing check points to the fix:
- `api_key.ok:false` → set `TRANS_API_KEY` (see Configuration below)
- `account.ok:false` → key invalid/expired or quota exhausted

Run `trans doctor --json` as the first step when diagnosing any trans-cli failure.

---

## JSON Contract

**Success** (stdout, exit 0):
```json
{"from":"zh","to":"en","source":"你好","translated":"Hello"}
```

| Field | Note |
|-------|------|
| `from` | API-detected language — may differ from `--from auto` |
| `to` | Target language |
| `source` | Original input |
| `translated` | Result |

**Error** (stderr, exit ≠ 0):
```json
{"code":"AUTH_FAILED","message":"…","help_url":"https://…","raw_code":"52001"}
```

`help_url` and `raw_code` are omitted when not applicable.

---

## Error Decision Tree

| Exit | `code` | Cause | Action |
|------|--------|-------|--------|
| 0 | — | OK | Use `translated` |
| 1 | `INVALID_INPUT` | Empty text | Fix input, don't retry |
| 1 | `INVALID_LANGUAGE` | Wrong lang code (e.g. `ja` → should be `jp`) | Fix `--to`/`--from`, see Language Codes below |
| 2 | `CONFIG_MISSING` | `TRANS_API_KEY` not set | Stop — run `trans doctor --json` then guide user to set up API key |
| 2 | `AUTH_FAILED` | Key invalid/expired (`raw_code` 52001–52003) | Stop — run `trans doctor --json` then guide user to API key page |
| 3 | `QUOTA_EXCEEDED` | Balance = 0 | Stop — guide user to recharge (see below) |
| 3 | `RATE_LIMITED` | QPS exceeded | Wait 1 s, retry once |
| 3 | `API_ERROR` | Unexpected API error | Retry once; if persists, report `raw_code` + `message` |
| 4 | `NETWORK_ERROR` | No connectivity | Retry twice with 2 s gap; if persists, report |

Exit 2 requires human intervention — the agent cannot fix auth or config.
Exit 1 means the agent passed bad arguments — fix the call, not the environment.

---

## Language Codes

Baidu does **not** follow ISO 639. When unsure of a code, query locally:

```bash
trans languages                    # full list (200+ languages)
trans languages --filter jp        # search by code
trans languages --filter 日语      # search by name
trans languages --json             # JSON output for Agent parsing
```

The six most common ISO traps:

| Baidu (correct) | ISO (wrong for Baidu) | Language |
|-----------------|----------------------|----------|
| `jp` | `ja` | Japanese |
| `kor` | `ko` | Korean |
| `fra` | `fr` | French |
| `spa` | `es` | Spanish |
| `ara` | `ar` | Arabic |
| `vie` | `vi` | Vietnamese |

Other common codes that match ISO: `zh` `cht` `en` `ru` `de` `pt` `it` `nl` `hi` `th`
Use `auto` for source-language auto-detection.

---

## Configuration

Priority: `--api-key flag > TRANS_API_KEY env > ~/.trans-cli/config.json`

Config file field: `api_key`.

```bash
trans config init               # create empty config skeleton (~/.trans-cli/config.json)
trans config init --force       # overwrite existing config
trans config set api_key <KEY>  # write api_key (creates file if absent)
```

---

## Getting an API Key (First-Time Setup)

Guide the user through these steps — the agent cannot do this on their behalf:

1. Open the Baidu Translation Open Platform and sign in: <https://fanyi-api.baidu.com/>
2. Go to Developer Center: <https://fanyi-api.baidu.com/manage/developer>
3. Click "Use Now" → select "General Translation" → complete identity verification
4. Get your API Key: <https://fanyi-api.baidu.com/manage/apiKey>
5. Write to config: `trans config set api_key <KEY>`
   or set the environment variable `TRANS_API_KEY`
6. Verify: `trans doctor --json` — `all_ok:true` means success

---

## Recharging (QUOTA_EXCEEDED)

Recharge portal: <https://fanyi-api.baidu.com/manage/account>
Takes effect immediately — no restart needed. Auto-renewal can be enabled on the same page.
Usage details: <https://fanyi-api.baidu.com/api/trans/user/usage>

---

## Non-Obvious Behaviours

- Multiple positional args join with a space: `trans text hello world` → `"hello world"`
- When both stdin and positional args are given, positional args win silently
- The `from` field in JSON is the API's detected language, not the `--from` flag value
- `trans doctor` checks are short-circuit: if `api_key` fails, connectivity/account are skipped
- `--reference` is optional; omitting it sends no extra field to the API
