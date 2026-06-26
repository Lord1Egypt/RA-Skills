# Ecovacs Deebot Control — API Reference (English)

**Entry point:** end users start with [SKILL.md](../SKILL.md) in the repo root. This file lists gateway bodies, fields, and enums. Implementation heuristics live in [agent-internal.md](agent-internal.md) (internal; English text on branch `en`).

## Authentication (AK)

**The Access Key (AK) must be created or viewed by the user in the Ecovacs Open Platform “Service overview”, then handed to the integrator (China `https://open.ecovacs.cn/`, global `https://open.ecovacs.com/`). Users do not need to pick a base URL manually—use the portal that matches their account region.**

This skill pack **does not** use account passwords or client-side login APIs to obtain tokens. The gateway (e.g. `mcp_portal_services`) consumes the AK and performs cloud auth and forwarding. This documentation **does not** expose vendor-internal hostnames or login payloads.

---

## Gateway integration (recommended)

Let `BASE_URL` be the gateway root. By default it matches the Open Platform host (China `https://open.ecovacs.cn`, global `https://open.ecovacs.com`). Override with `ECOVACS_PORTAL_URL` for a self-hosted or local gateway.

### Device list (GET, redacted)

Prefer **GET**:

```bash
curl -sS "${BASE_URL}/robot/skill/deviceList?ak=YOUR_AK"
```

Example response:

```json
{
  "msg": "OK",
  "code": 0,
  "data": [
    { "nick": "T90pro201", "name": "..." }
  ]
}
```

Each row in `data` **does not** include `did`, `class`, or `resource` (the gateway fills these when controlling by `nickName`).

You may also `POST ${BASE_URL}/robot/skill/deviceList` with `Content-Type: application/json` and body `{"ak":"<AK>"}`—same semantics as GET.

### Control (cloudctl)

- `POST ${BASE_URL}/robot/skill/ctl`
- `Content-Type: application/json`

```json
{
  "ak": "<AK>",
  "nickName": "<substring to fuzzy-match nick or name>",
  "ctl": {
    "cmd": "<capability command>",
    "data": { }
  }
}
```

When `nickName` is present, the server matches a device and completes cloud-control fields. The “protocol cheat sheet” below maps `cmdName` / `body.data` to `ctl.cmd` / `ctl.data`.

### curl examples

```bash
export BASE_URL="https://open.ecovacs.cn"   # China; global: https://open.ecovacs.com
export AK="YOUR_AK"
```

Zone clean (`Clean` + `type=spotarea`; `nickName` is a nick/name fragment):

```bash
curl -sS -X POST "${BASE_URL}/robot/skill/ctl" -H 'Content-Type: application/json' \
  -d "{\"ak\":\"${AK}\",\"nickName\":\"device-nick-fragment\",\"ctl\":{\"cmd\":\"Clean\",\"data\":{\"act\":\"s\",\"type\":\"spotarea\",\"workMode\":0,\"aid\":[\"<mssid1>\",\"<mssid2>\"]}}}"
```

Go charge:

```bash
curl -sS -X POST "${BASE_URL}/robot/skill/ctl" -H 'Content-Type: application/json' \
  -d "{\"ak\":\"${AK}\",\"nickName\":\"Blue\",\"ctl\":{\"cmd\":\"Charge\",\"data\":{\"act\":\"go\"}}}"
```

Stop go-charge:

```bash
curl -sS -X POST "${BASE_URL}/robot/skill/ctl" -H 'Content-Type: application/json' \
  -d "{\"ak\":\"${AK}\",\"nickName\":\"Blue\",\"ctl\":{\"cmd\":\"Charge\",\"data\":{\"act\":\"stopGo\"}}}"
```

---

## Public surface vs internal boundary (no raw cloud URLs / login)

Discovery and control always use the **gateway** paths (`/robot/skill/deviceList`, `/robot/skill/ctl`). Vendor-internal hostnames, app-layer login, and direct-device APIs are **not** documented here. `scripts/ecovacs.py` only calls the gateway and never assembles internal addresses on the client.

### Device list (request/response semantics)

| Item | Notes |
|------|--------|
| Request | `GET ${BASE_URL}/robot/skill/deviceList?ak=<AK>`, or `POST` same path with JSON `{"ak":"<AK>"}` |
| Success `data[]` | Redacted device objects; common fields `nick`, `name`, `deviceName`, `status` (e.g. `1`≈online, `0`≈offline—confirm with your gateway) |
| Omitted | `did`, `class`, `resource`, etc.; filled server-side from `ak` + `nickName` when controlling |

### Control (request/response semantics)

| Item | Notes |
|------|--------|
| Request | `POST ${BASE_URL}/robot/skill/ctl` with `ak`, optional `nickName`, and `ctl` (`cmd` + `data`) as in the JSON above |
| Success | Outer `msg` / `code`; inner payload matches the per-command **`data`** shapes in the cheat sheet below |

---

## Core protocol reference (by capability)

**`/robot/skill/ctl` uses CloudCtl** (`ctl.cmd` / `ctl.data`). For clean/recharge use **`Clean`** and **`Charge`** with official casing—**not** lowercase `charge`.

Put **`ctl.cmd` / `ctl.data`** in **`POST /robot/skill/ctl`** (add `nickName` when needed). On success, inner shapes match cloudctl (`ret` / `errno`, etc.).

### CloudCtl: `Clean`

| `data.act` | Meaning |
|------------|---------|
| `s` | Start clean (needs `type`, `workMode`, etc.—see vendor appendix C) |
| `p` | Pause |
| `r` | Resume |
| `h` | Stop (after stop you cannot `resume` the same run per vendor docs) |

Zone clean: `act=s` with **`type=spotarea`** and `aid` as an array of area IDs from **`GetAreaList`** `list[].mssid` (appendix E). Official type name is **`spotarea`** (all lower). If the device returns `unknown type`, try firmware-consistent casing variants.

### CloudCtl: `Charge`

| `data.act` | Meaning |
|------------|---------|
| `go` | Start returning to dock |
| `stopGo` | Stop returning to dock |

```json
{ "cmd": "Charge", "data": { "act": "go" } }
```

---

### GetBatteryInfo

| cmd | body.data |
|-----|-----------|
| `GetBatteryInfo` | `{}` |
| `onBattery` (report) | `{ value: 0-100, isLow: 0/1 }` |

Inner `ctl.data` may be `{ ret, value, isLow }`; some models use **`{ ret, power }`** (`power` = percent).

---

### Clean state — `GetWorkState` (replaces deprecated `getCleanInfo_V2`)

Through the gateway use **`GetWorkState`** (PascalCase). Lowercase `getWorkState` can yield `errno=5009` on some models.

(Use the script `status` command or `POST /robot/skill/ctl` with `GetWorkState`.)

Response `data`:

```json
{
  "paused": 0,
  "robotState": {
    "state": "idle | mapping | cleaning | moving | video",
    "trigger": "app | voice | button | kick | schedule | batteryLow | alert | workComplete | breakPoint",
    "cleanState": {
      "cid": 123456,
      "type": "auto | freeClean | qcClean | entrust | spotClean | comeClean | smartClean | sprayClean | mapping",
      "entrust": 0
    }
  },
  "stationState": {
    "state": "idle | goCharging | emptying | goEmptying | washing | goWashing | spinDrying | drying | goDrying | selfCleaning | goSelfCleaning | dewatering",
    "trigger": "app | voice | button | breakPoint"
  }
}
```

**`robotState.state` meanings**

- `idle` → standby  
- `cleaning` → active clean job (check `paused` for pause vs running)  
- `mapping` → mapping  
- `moving` → remote driving  
- `video` → video task  

⚠️ `cleaning` + `paused=1` means **paused**, not finished.

**`trigger` (completion logic)**

| trigger | Meaning | Conclusion |
|---------|---------|------------|
| `workComplete` | Normal completion | ✅ done |
| `breakPoint` | Resume-from-breakpoint | ⏳ in progress |
| `batteryLow` | Low battery dock | ⚠️ aborted |
| `alert` | Alert stop | ❌ error |
| `app` / `button` / … | Interpret with `state` | context |

**`stationState.state` (short)**  
`emptying` auto-empty, `goEmptying` returning to empty, `washing` mop wash, `drying` dry, `goCharging` docking, `dewatering` draining, etc.

---

### Stats (`GetStats` / `onStats`)

```json
{ "cid": "...", "area": 10, "time": 600, "type": "auto", "avoidCount": 3, "aiopen": 1 }
```

- `area`: square meters  
- `time`: seconds  

---

### Speed (suction)

```json
// get: {}
// set: { "speed": 0 }
```

Values: `1000` quiet, `0` standard, `1` strong, `2` max

---

### WaterInfo

```json
// get: {}
// set: { "amount": 2 }
```

Values: `1` low … `4` ultra  
`enable`: `1` mopping mode, `0` sweep-only  

Constraint: in **sweep-only** mode, water level is usually rejected; `SetWaterInfo` needs a mopping-capable mode. Per ROP, `SetWaterInfo` uses `gear` (`low|medium|large|superLarge`), not numeric `amount`.

---

### WorkMode

```json
// get: {}
// set: { "mode": 0 }
```

`0` sweep+mop, `1` sweep only, `2` mop only, `3` sweep then mop  

ROP examples:  
`GetWorkMode`: `{"cmd":"GetWorkMode","data":{"noVoiceResp":1}}`  
`SetWorkMode`: `{"cmd":"SetWorkMode","data":{"noVoiceResp":1,"mode":0}}`

---

### LifeSpan (consumables)

```json
// get (ROP): { "type": ["brush","sideBrush","heap","filter"], "noVoiceResp": 1 }
```

Returns `[ { "type": "brush", "left": 80, "total": 100 } ]`  
Types include `brush`, `sideBrush`, `heap`, `filter`, `roundMop`, `wbHeap`, etc.

---

### AutoEmpty (dock dust collection)

```json
// get: {}
// start: { "act": "start" }
// set auto: { "enable": 1, "frequency": "auto|standard|smart|10|15|25" }
```

Status: `0` off, `1` running, `2` done, `3` lid open, `4` bag missing, `5` bag full

---

### CachedMapInfo

```json
// get: {}
```

Returns `[ { "mid": "...", "index": 0, "name": "...", "status": 0, "using": 1 } ]`

---

### MapSet / MapSet_V2 (areas)

```json
// get: { "mid": "<map_id>", "type": "ar" }
```

Returns subsets: `[ { "mssid": "...", "name": "Living room", "subtype": 1 } ]`

`subtype`: `0` default, `1` living, `2` dining, `3` bedroom, `4` study, `5` kitchen, `6` bath …

---

### Sched_V2 (schedules)

```json
// get: { "type": 1 }
// add:
{
  "act": "add", "enable": 1,
  "sid": "1", "repeat": "0000000",
  "hour": 8, "minute": 0,
  "mid": "<map_id>",
  "content": {
    "name": "clean",
    "jsonStr": "{\"router\":\"plan\",\"content\":{\"type\":\"auto\",\"value\":\"\"}}"
  }
}
// delete: { "act": "del", "sid": "1", "mid": "<map_id>" }
```

`repeat`: 7 chars Sun–Sat, `1` = scheduled, `0000000` = once

---

### Error codes (`onError`)

Common: `0` clean finished, `102` stuck, `103` cliff, `104` low battery, `110` dustbin missing

---

### Event codes (`onEvt`)

Common: `1` clean start, `2` pause, `3` stop, `1025` low-battery dock charging, `1099` auto-empty done

---

## CloudCtl errors and command enums (excerpt)

For agents parsing gateway/cloud responses: outer `code`/`msg`; business payload under **`data` → … → `ctl.data`** with **`ret`**, **`errno`**, optional **`error`**. Tables align with vendor appendices C/D/E/F.

### Common cloud API errno (appendix F)

| errno | Meaning |
|-------|---------|
| 4000 | Malformed body |
| 4500 | Server internal error |
| 4501 | Invalid appid |
| 4504 | Token check failed |
| 4508 | `ts` skew vs server (~2 min) or bad `sig` |
| 4509 | appid deleted |
| 4511 | appid not configured for model |
| 4512 | appid not configured for this command on model |
| 5009 | **Command/params not supported on this model** (casing, firmware mismatch) |
| 10000 | Low battery, cannot run |
| 10004 | Offline / timeout / powered off / reprovisioned |
| 10005 | Host fault (lifted, dustbin, …) |

### Clean response errno (appendix C)

| errno | Meaning |
|-------|---------|
| 10000 | Low battery |
| 10005 | Host fault |
| 10006 | Internal host fault |

### Charge response errno (appendix D)

| errno | Meaning |
|-------|---------|
| 10006 | Internal host fault |

### Clean `data` fields (appendix C)

| Field | Meaning |
|-------|---------|
| `act` | `s` start · `p` pause · `r` resume · `h` stop (**no resume after `h`**) |
| `workMode` | `0` sweep+mop · `1` sweep · `2` mop · `3` sweep then mop |
| `type` (when `act=s`) | `auto` whole home · **`spotarea`** zones (`aid` from `GetAreaList`) · `spot`, `combination`, `border`, `voiceBorder`, … |
| `aid` | Area ID list; required for `spotarea` |
| `atype` | Used with `type=combination` |
| `tri` | Trigger source (`btn`, `val`, `app`, …) |

**Room `atype` (appendix C, mirrors `GetAreaList` `subType`)**  
`1` living · `2` dining · `3` bedroom · `4` study · `5` kitchen · `6` bath · `7` laundry · … (see vendor table)

**Furniture `ftype` (appendix C)**  
`2000` sofa · `2001` table · `2002` coffee table · … · `2021` zone clean

### Charge `data.act` (appendix D)

| `act` | Meaning |
|-------|---------|
| `go` | Start dock return |
| `stopGo` | Stop dock return |

### `GetAreaList` `list[]` (appendix E)

| Field | Meaning |
|-------|---------|
| `mssid` | Area ID for `Clean` `spotarea` `aid` |
| `name` | Area name (may be empty) |
| `subType` | Room type `0` unspecified · `1`–`6` living–bath · … |

### Inner `ret` (appendices C/D/E)

| `ret` | Meaning |
|-------|---------|
| `ok` | Success |
| `fail` | Failure—read `errno` / `error` |
