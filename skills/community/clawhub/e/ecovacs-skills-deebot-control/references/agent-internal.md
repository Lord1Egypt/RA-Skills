# Internal implementation reference (not for default end-user replies)

Automation-oriented: smart clean, room/zone clean, async polling, notifications, state parsing. End users only need AK, gateway, and nicknames; this section is **implementation detail**.

Through the gateway prefer CloudCtl **`Clean` / `Charge`** (`act` `s`/`p`/`r`/`h`, zones `type=spotarea` + `aid`, stop dock `stopGo`). See [api.md](api.md) section “CloudCtl: `Clean` / `Charge`”.

---

## Strategy overview

```
Sense environment → derive parameters for smart clean
Rooms/zones → GetAreaList for mssid, then Clean(type=spotarea, aid=[...])
Notify → on completion (e.g. Feishu) via scheduled job
Cache capabilities → persist clean-type per did for later reuse
```

---

## Zone clean (`GetAreaList` + `Clean`)

Goal: implement “clean by room/zone” using commands documented in `product_design_rop`.

```bash
# 1) Area list (list[].mssid)
curl -sS -X POST "${BASE_URL}/robot/skill/ctl" -H 'Content-Type: application/json' \
  -d "{\"ak\":\"${AK}\",\"nickName\":\"device-nick-fragment\",\"ctl\":{\"cmd\":\"GetAreaList\",\"data\":{}}}"

# 2) Zone clean: Clean(type=spotarea) + aid=[mssid...]
curl -sS -X POST "${BASE_URL}/robot/skill/ctl" -H 'Content-Type: application/json' \
  -d "{\"ak\":\"${AK}\",\"nickName\":\"device-nick-fragment\",\"ctl\":{\"cmd\":\"Clean\",\"data\":{\"act\":\"s\",\"type\":\"spotarea\",\"workMode\":0,\"aid\":[\"<mssid1>\",\"<mssid2>\"]}}}"
```

---

## Command cheat sheet (`ctl.cmd` / `ctl.data`)

| Goal | cmd | `data` highlights |
|------|-----|-------------------|
| Whole home (CloudCtl, preferred) | `Clean` | `act:"s"` + `type:"auto"` + `workMode` (see api.md) |
| Zone clean (preferred) | `Clean` | `act:"s"` + `type:"spotarea"` + `aid` from `GetAreaList` `mssid` |
| Pause / resume / stop | `Clean` | `act:"p"` / `"r"` / `"h"` |
| Dock / stop dock | `Charge` | `act:"go"` / `"stopGo"` |
| Battery | `GetBatteryInfo` | `{}` |
| Work state | `GetWorkState` | `{}` (**do not** use deprecated `getCleanInfo_V2`; avoid lowercase `getWorkState`—5009 on some models) |
| This-run stats | `GetStats` | `{}` |
| Suction | `GetSpeed` / `SetSpeed` | `SetSpeed`: `{speed:"mute|standard|strong|superStrong"}` |
| Water | `GetWaterInfo` / `SetWaterInfo` | `SetWaterInfo`: `{gear:"low|medium|large|superLarge"}`; often rejected in **sweep-only** mode |
| Sweep/mop mode | `GetWorkMode` / `SetWorkMode` | `GetWorkMode`: `{noVoiceResp:1}`; `SetWorkMode`: `{noVoiceResp:1,mode:0}` (0 = sweep+mop …) |
| Consumables | `getLifeSpan` | `{type:"brush,sideBrush,heap,filter"}` |
| Consumables (ROP array) | `GetLifeSpan` | `{type:["brush","sideBrush","heap","filter"],noVoiceResp:1}` (omit `type` = all) |
| Manual empty | `StationEmpty` | `{act:"start"}` |

Full tables: [api.md](api.md).

---

## `GetWorkState` state machine

(Prefer the script `status` or `POST /robot/skill/ctl` with `GetWorkState`.)

Payload shape: see [api.md](api.md) “Clean state — `GetWorkState`” (some models nest `robotState`, others flatten to `cleanSt` / `chargeSt` / …).

**`robotState.state`**

- `idle` → standby  
- `cleaning` → job present (check `paused`)  
- `mapping` → mapping  
- `moving` → remote  
- `video` → video task  

⚠️ `cleaning` + `paused=1` means **paused**, not finished.

**`trigger` (completion)**

| trigger | Meaning | Conclusion |
|---------|---------|------------|
| `workComplete` | Normal completion | ✅ done |
| `breakPoint` | Resume segment | ⏳ continue |
| `batteryLow` | Low-battery dock | ⚠️ aborted |
| `alert` | Alert stop | ❌ error |
| `app` / `button` / … | combine with `state` | product rules |

**`stationState`**: `emptying` dust collection, `washing` mop wash, `drying` dry, `goCharging` returning to dock, etc.

---

## Smart clean (weather + time window, example: Suzhou)

**Humidity → water gear (`SetWaterInfo.gear`)**

- ≥75%: `gear:"low"`  
- 45–74%: `gear:"medium"`  
- <45%: `gear:"large"`  

**Time window → suction (example)**

- Quiet hours (e.g. 12:30–14:00, 22:00–08:00): `speed:1000` or `0`  
- Daytime: `speed:1` or `2`  

Order: confirm mopping-capable mode (not sweep-only), then `SetWaterInfo`, `SetSpeed`, then `Clean act=s` (e.g. `type=auto`). Default path can follow “smart clean” playbook.

---

## Charging (`GetChargeState`)

- `isCharging`: `1` on dock  
- `mode`: e.g. `autoEmpty` while emptying  
- `chargeRate` is **power**, not SoC—use `GetBatteryInfo` for percent  

You may still issue clean while charging/emptying if `code=0` indicates the robot will run when ready.

---

## Async polling + Feishu-style completion pings

**Trigger:** after a successful clean command (e.g. `Clean act=s`), **immediately** schedule polling (do not wait for transient state).

### Poll priority

1. `GetWorkState` → `robotState.state` / `trigger` / `paused` (or flat `cleanSt`/`chargeSt`/`stationSt`).  
2. `cleaning` + `paused==0` → in progress, silent return.  
3. `cleaning` + `paused==1` → paused, silent return.  
4. `mapping` → mapping, silent return.  
5. `idle` + `stationState.state != idle` → dock task, silent return.  
6. `idle` + `trigger == workComplete` → ✅ finished → summary notify.  
7. `idle` + `trigger` in `batteryLow` / `alert` → ⚠️ abnormal end, notify with reason.  
8. `idle` + `trigger` in `app` / `button` → may treat as normal end per product policy.  
9. `idle` + other/`none` → not started or initial, silent return.

### On completion

- `GetStats` → `area` (m²), `time` (seconds → minutes)  
- Battery via script / `GetBatteryInfo`  
- Send human-readable summary (Feishu, etc.); **delete the scheduled job** after send.  
- **Anti-stall:** after ~≥60 polls (~2h) still not terminal → alert + delete job.

Rule: only completion/abnormal branches notify and delete jobs—otherwise stay silent.

---

## Errors (gateway / business)

### Gateway / historical codes

| code | Meaning | Action |
|------|---------|--------|
| 0 | OK | — |
| 3000 | Token invalid | Ask user to refresh AK on Open Platform |
| 3003 | Permission denied | Check device `class` / `toType` |
| 30000 | Device timeout | Offline |
| 20011 + format | Bad `value` | Fix body vs protocol |

### CloudCtl inner (`errno` / `error`, excerpt)

Parse **`ctl.data`** (full tables in [api.md](api.md) “CloudCtl errors and command enums”):

| errno | Typical meaning |
|-------|-----------------|
| 4000 | Malformed body |
| 4504 | Token check failed |
| 5009 | **Model does not support command/params** (e.g. lowercase `getWorkState`, wrong cmd) |
| 10000 | Low battery |
| 10004 | Offline / timeout / off / reprovisioned |
| 10005 | Host fault (dustbin, lifted, …) |
| 10006 | Internal host fault (`Clean`/`Charge` responses) |

**`ret`:** `ok` success, `fail` needs `errno`/`error`.

---

## What not to say to end users by default

- Do **not** paste polling pseudocode or full protocol tables in default replies.  
- “How do I control?” → point to SKILL “What you need” + script commands.  
- “Why did it fail?” → short reason + AK refresh pointer is enough.
