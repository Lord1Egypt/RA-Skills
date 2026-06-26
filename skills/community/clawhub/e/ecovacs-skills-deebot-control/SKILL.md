---
name: ecovacs-deebot-control
description: Control Ecovacs Deebot vacuums via the IoT API and a gateway. Users must obtain and provide an AK from the Open Platform; scripts/ecovacs.py and gateway /robot/skill/*. For control, battery, clean/recharge, nickname matching.
---

# Ecovacs Deebot control

## What you need

| Input | Notes |
|-------|--------|
| **AK (Access Key)** | Create or view it in the Ecovacs Open Platform “Service overview” (**China**: `https://open.ecovacs.cn/`, **Global**: `https://open.ecovacs.com/`), then copy it into env vars, a config file, or chat **yourself**. Pick the portal region that matches your account. **Do not** hand account passwords to automation; this skill **does not** log in on your behalf. |
| **Gateway base URL** (optional) | Defaults to the same host as the Open Platform (**China** `https://open.ecovacs.cn`, **Global** `https://open.ecovacs.com`). Override with `ECOVACS_PORTAL_URL` for a self-hosted or local gateway (e.g. `mcp_portal_services`). |
| **Device nickname fragment** | Used to pick one robot. Take a substring of `nick` or `name` from the device list (fuzzy match). |

If the AK is invalid (e.g. errno **3000**), refresh it on the Open Platform—do not try to replace user login with other APIs.

---

## Three steps

1. **Configure AK** → 2. **Device list** → 3. **Send commands**

### 1. Configure AK (pick one)

```bash
export ECOVACS_AK="YOUR_AK"
# or: python3 scripts/ecovacs.py set-ak <ak>
# writes ~/.ecovacs_session.json with {"ak":"..."} only
```

### 2. Device list

```bash
python3 scripts/ecovacs.py devices
```

Note the **nick / name** fragment you will use as `<nick>` below.

### 3. Common CLI operations

Let `SCRIPT=scripts/ecovacs.py`.

#### Queries

- Battery: `python3 "$SCRIPT" battery <nick>`
- Work state (clean / charge / station): `python3 "$SCRIPT" status <nick>`

#### Cleaning

- Whole-home auto clean: `python3 "$SCRIPT" clean <nick> start`
- Pause / resume / stop: `python3 "$SCRIPT" clean <nick> pause` or `resume` / `stop`

#### Charging

- Go charge / stop go-charge: `python3 "$SCRIPT" charge <nick> go` or `stop`

---

## HTTP gateway (no Python)

`BASE_URL` is the same as `ECOVACS_PORTAL_URL` (defaults to the regional Open Platform host).

**Device list**

```bash
curl -sS "${BASE_URL}/robot/skill/deviceList?ak=YOUR_AK"
```

**Control**: `POST /robot/skill/ctl` with JSON `ak`, optional `nickName` (fuzzy match on list), and `ctl.cmd` / `ctl.data`.

```bash
curl -sS -X POST "${BASE_URL}/robot/skill/ctl" -H 'Content-Type: application/json' \
  -d "{\"ak\":\"${AK}\",\"nickName\":\"nick-fragment\",\"ctl\":{\"cmd\":\"Charge\",\"data\":{\"act\":\"go\"}}}"
```

CloudCtl expects **`Charge`**, **`Clean`**, etc. with official casing—**not** lowercase `charge`.

More JSON examples (e.g. zone clean) are in [references/api.md](references/api.md).

---

## Errors and enums (troubleshooting)

Responses are usually two layers: outer `msg` / `code`; inner cloudctl payload under nested **`ctl.data`** with **`ret`** (`ok`/`fail`), **`errno`**, optional **`error`**.

| Situation | Meaning / next step |
|-----------|---------------------|
| Appendix F **5009** | Command or parameter combo **not supported** on this model (casing, firmware); verify model, try `GetWorkState` / `GetBatteryInfo` naming |
| Appendix F **10004** | Offline / timeout / powered off / re-provisioned |
| Appendix F **10000** | Low battery, cannot run |
| Appendix F **10005** | Host fault (lifted, dustbin missing, …) |
| Clean **10006** / Charge **10006** | Internal host fault (appendix C/D) |
| Appendix F **4000** | Malformed JSON |
| Appendix F **4504** | Token check failed—verify AK |
| `ret=fail` | Read `errno` and `error` together |

**Water level**: In **sweep-only** mode (no mopping / tank inactive), `SetWaterInfo` often fails (`ret=fail`); switch to a mopping-capable mode first.

**Clean enums**: `act` = `s`/`p`/`r`/`h`; `workMode` 0–3; zone clean uses **`type=spotarea`** + **`aid`** from **GetAreaList** `mssid`. **Charge**: `go` / `stopGo`.

Full tables: see “CloudCtl errors and enums” at the end of [references/api.md](references/api.md).

---

## How to read the docs

| File | Audience | Contents |
|------|----------|----------|
| **This SKILL.md** | End users | Inputs, three steps, CLI, HTTP |
| [references/api.md](references/api.md) | Integrators | Paths, bodies, enums, curl |
| [references/agent-internal.md](references/agent-internal.md) | Internal | Smart clean, rooms, polling, `GetWorkState` heuristics |

Prefer this page for user-facing guidance; use `references/agent-internal.md` only when you need implementation-level troubleshooting.
