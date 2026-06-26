---
name: ecovacs-pet-control
description: Control Ecovacs FAMIBOT (pet) robots via the Open Platform Access Key (AK) and POST /robot/skill/pet/cmd. Covers device discovery, queries/settings, display/playSound, single motions, and the showcase_custom dance preset (~45s). Default gateway Mainland China https://open.ecovacs.cn.
---

# Ecovacs Pet (FAMIBOT) Control

## What you need

| You provide | Notes |
|-------------|-------|
| **AK (Access Key)** | Get one from the Ecovacs Open Platform “Service Overview” (Mainland China: `https://open.ecovacs.cn/`, non-China regions: `https://open.ecovacs.com/`) and put it in your env or pass to `set-ak`. **Do not** hand the skill a username/password to log in on your behalf. |
| **Device nickname fragment** | Used to fuzzy-match `nick` or `name` returned by the device list. |

---

## Three-step flow

1. **Configure AK** (`export ECOVACS_AK=...` or `python3 scripts/ecovacs.py set-ak <ak>`)
2. **List devices**: `python3 scripts/ecovacs.py devices`
3. **Control**: Use **`POST /robot/skill/pet/cmd`** or the script's `cmd` / `display` subcommands; **`cmd` must be in the gateway allowlist**, otherwise the gateway returns `command not enabled`.

Run from the **repository root**: `python3 scripts/ecovacs.py ...`. You may set **`ECOVACS_PORTAL_URL`** to a custom gateway base URL; when unset, the default is the Mainland China Open Platform domain.

---

## Usage constraints

- Requests use **`cmd` (string)** + **`data` (object)**; invalid parameters surface as cloud error messages.
- If the gateway returns **`command not enabled`**, that `cmd` is outside the deployment's supported set — use only commands listed below or ask a maintainer.

### Response fields and `set*` inputs

See [references/schema.md](references/schema.md).

### Supported commands

#### Queries

| Description | cmd |
|-------------|-----|
| Pet state / emotion / persona / gender / location & weather / initialization | `getPetState`, `getEmotion`, `getPerson`, `getPetGender`, `getLocationInfo`, `getInitiateState` |
| Microphone / camera / volume / eye brightness / language / wake idle timeout | `getMicro`, `getCamera`, `getVolume`, `getEyesLight`, `getLanguage`, `getWakeTimeout` |
| Latest diary entry | `getLatestDiary` |

#### Settings

| Description | cmd |
|-------------|-----|
| Microphone / camera / volume / wake idle timeout / wake word / gender | `setMicro`, `setCamera`, `setVolume`, `setWakeTimeout`, `setNickname`, `setPetGender` |

#### Control

| Description | cmd |
|-------------|-----|
| Display / motion sequences | `display` |
| Play sound (`category` **or** `file` + optional `count` / `moveTimeMs`) | `playSound` |

**Sound routing (conversation → payload)** — see [phoenix-single-action.md §2.2](references/phoenix-single-action.md):

| User intent | Send |
|-------------|------|
| “Bark happily” / vague mood sound | `{"category":"happy","count":1}` — gateway picks a random clip in that category |
| “Bark **loudly** / big happy bark” | `{"file":"happy-h-<1-5>","count":1}` — pick one `happy-h-1`…`happy-h-5` |
| “Soft / quiet bark” | `{"file":"happy-l-<1-5>","count":1}` |
| Other moods | `category` = `calm` / `attached` / `curious` / `angry` / `sad` / `scared`, or pick `file` with matching `{mood}-{l\|m\|h}-{n}` |

For `action_sequence` rows, each `play_sound` step needs an explicit `file` (choose using the table above before building JSON).

**Dance** — single preset in [references/dance-routines.md](references/dance-routines.md) (`showcase_custom` / 定制秀舞):

| User intent | CLI |
|-------------|-----|
| Dance / short dance / any legacy mood name | `display <nick> dance` |

Fixed script ~45s; `length` is ignored. Aliases (`cheerful`, `点头舞`, etc.) all map to the same dance.

**Persona / mood (read-only)**: `getPerson`, `getPetState`, `getEmotion`.

**Sleep**: `display <nick> sleep`.

**Motion protocols** — **two paths; do not mix fields between them**:

| Path | When | Doc |
|------|------|-----|
| `play_action` | One step: `display … action`, bare `playSound` | [phoenix-single-action.md](references/phoenix-single-action.md) |
| `action_sequence` | Multi-step, dance, `playSound` + `actions`, timed | [phoenix-action-control.md](references/phoenix-action-control.md) + [action-sequence.md](references/action-sequence.md) |

**Critical — pick one protocol and its field names only:**

| Topic | `play_action` (single) | `action_sequence` (composite) |
|-------|------------------------|-------------------------------|
| Head `angle` | **×100** on wire (`30°` → `"3000"`); script accepts degrees in CLI JSON | **Degrees as-is** (`"-14"`, `"44"`); **must stay in range** |
| Head ranges | Script converts degrees; still respect device limits when choosing values | `nod_head` −14~+22 · `shake_head` −60~+60 · `cock_head` −20~+20 |
| Tail speed | Wire field `angle` = speed×100; CLI may use `percent` / `angle` 0–100 | Field **`percent`** 0–100 only — **not** `angle` |
| Sound | Wire field `angle` = filename; CLI `file` or `category` via `playSound` | Field **`file`** — **not** `angle` |
| `moveTimeMs` | `-1` allowed (default speed / continuous tail) | **Must be >0**; `-1` is replaced by script defaults |
| Timing | No `delay` | Every row needs **`delay`** (ms) |

Common mistakes: copying a single-action JSON into `actions[]` (×100 angles, `-1` times); using `percent` in `display action wag_tail` without letting the script convert (OK in CLI, wrong on raw wire); using `angle: "3000"` in a dance step (device expects `"30"`).

| Utility | Script |
|---------|--------|
| Enter sleep | `display <nick> sleep` |
| Stop motion / cancel device-side scheduled routines | `display <nick> reset` |

Before sending any `display` motion/persona action through `scripts/ecovacs.py display ...`, the script checks `getCamera`. If `enable != 1`, it wakes the pet through the skill gateway with `setCamera {"enable":1}`, waits until `getCamera.enable=1`, switches work mode back to `standard` with `setWorkMode {"mode":"standard"}`, and only then sends the action. Set `ECOVACS_SKIP_WAKE_CHECK=1` only for debugging when you intentionally want to bypass this guard.

**Dance / timed barks / multi-step shows**: one `action_sequence` per show. **Dance**: `build_dance_sequence()` → **`showcase_custom`** — see **[references/dance-routines.md](references/dance-routines.md)**.

**Default timing limits** (hand-built JSON only; **preset dance is exempt** — see below):

| Scope | Default cap | Override |
|-------|-------------|----------|
| Single step (`play_action` or one `actions[]` row) | **delay + duration ≤ 10s** | `"user_timing": true` on the JSON object |
| Hand-built `action_sequence` (non-scheduled) | **end time ≤ ~20s** | same flag, or `conditions.scheduled` / repeat |
| **Preset dance** (`display … dance` → `showcase_custom`) | **~45s fixed script** | Script sets `user_timing: true` automatically — do not trim steps to fit 20s |
| Debug | skip all checks | `ECOVACS_SKIP_TIMING_LIMIT=1` |

`user_timing` is stripped before the gateway sees the payload.

---

## Script examples

```bash
SCRIPT="./scripts/ecovacs.py"

python3 "$SCRIPT" cmd <nickname-fragment> getPetState '{}'
python3 "$SCRIPT" cmd <nickname-fragment> getCamera '{}'
python3 "$SCRIPT" cmd <nickname-fragment> setWakeTimeout '{"timeout":180}'

python3 "$SCRIPT" cmd <nickname-fragment> getPerson '{}'
python3 "$SCRIPT" display <nickname-fragment> dance
python3 "$SCRIPT" display <nickname-fragment> dance showcase_custom

python3 "$SCRIPT" cmd <nickname-fragment> playSound '{"category":"happy","count":1}'

python3 "$SCRIPT" cmd <nickname-fragment> playSound '{"file":"happy-h-3","count":1}'

python3 "$SCRIPT" display <nickname-fragment> sleep
python3 "$SCRIPT" display <nickname-fragment> reset
python3 "$SCRIPT" display <nickname-fragment> action shake_head '{"angle":"30","moveTimeMs":"-1","count":"3"}'

python3 "$SCRIPT" display <nickname-fragment> action wag_tail '{"percent":30,"moveTimeMs":"-1"}'

python3 "$SCRIPT" cmd <nickname-fragment> playSound '{"file":"happy-h-1","count":1,"conditions":{"scheduled":"0","repeat_type":"1","repeat_count":"10"}}'
```

---

## HTTP calls (no Python available)

Default gateways: Mainland China `https://open.ecovacs.cn`, non-China regions `https://open.ecovacs.com` (override with **`ECOVACS_PORTAL_URL`** if needed).

**Device list**

```bash
curl -sS "${BASE_URL}/robot/skill/deviceList?ak=YOUR_AK"
```

**Pet control**

```bash
curl -sS -X POST "${BASE_URL}/robot/skill/pet/cmd" -H 'Content-Type: application/json' \
  -d "{\"ak\":\"${AK}\",\"nickName\":\"nickname-fragment\",\"cmd\":\"getPetState\",\"data\":{}}"
```

The field name must be **`nickName`** exactly as above (uppercase `N`).

Compatibility path: `POST /robot/skill/ctl` + `ctl` is still accepted for pet devices and is also subject to the **`cmd` allowlist**.

---

## Recommended verification order

Use the script and HTTP examples earlier in this document (`get*` first, then `set*` / `display`) to confirm `nickName` resolution and allowlist behavior before relying on higher-risk writes.

---

## Errors and troubleshooting (summary)

| Case | What to do |
|------|------------|
| Outer `code != 0` | Read `msg` (invalid AK, device not found, not FAMIBOT, **command not enabled**) |
| `command not enabled` | Use only commands listed in **Supported commands** above; ask a maintainer if the user needs something else |
| `setCamera` / `setWorkMode` blocked before a display action | Automatic wake-up could not complete; wake the pet in the app and retry |
| Token errors like 4504 | Check / rotate the AK |
| 3003 | Verify nickname matches the right device and that the model supports the capability |

More detailed troubleshooting (including "why was this judged not-pet") lives in `references/troubleshooting.md`.

---

## Doc map

| File | Audience | Content |
|------|----------|---------|
| **This SKILL.md** | Agent / user | AK, device list, `pet/cmd` usage, public capability name-level notes |
| [references/api.md](references/api.md) | User | Gateway URLs and request body fields |
| [references/schema.md](references/schema.md) | User | Common response fields, `set*` input names and compatibility rules |
| [references/troubleshooting.md](references/troubleshooting.md) | User | Common error branches and resolution paths |
| [references/phoenix-single-action.md](references/phoenix-single-action.md) | Agent | 单步 `play_action` 字段 |
| [references/phoenix-action-control.md](references/phoenix-action-control.md) | Agent | 编排 `action_sequence` 字段表 |
| [references/action-sequence.md](references/action-sequence.md) | Agent | `delay` / `conditions`、helper、场景（无重复字段表） |
| [references/dance-routines.md](references/dance-routines.md) | Agent / user | 唯一预设 **`showcase_custom`**（定制秀舞）结构与 CLI |

Supported commands are listed in **this SKILL.md**; protocol docs describe only those motion paths. Legacy multi-routine names (`cheerful_motion`, `party`, `点头舞`, …) are **aliases** to `showcase_custom` only.
