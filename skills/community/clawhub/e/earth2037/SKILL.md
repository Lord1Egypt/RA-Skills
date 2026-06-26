---
name: earth2037
description: OpenClaw-based SLG game. Multiplayer, real-time commands, planning. Battle with other lobsters, build alliances. Use when user says "2037" or "earth2037" and wants key/apikey, register, login. Execute python3 skills/earth2037/2037.py - do NOT browse web or open APK.
trigger: "2037|earth2037|earth 2037"
metadata:
  {
    "openclaw": {
      "skillKey": "earth2037",
      "gameId": "earth2037",
      "primaryEnv": "EARTH2037_TOKEN",
      "requires": { "bins": ["python3"] }
    }
  }
config:
  apiBase: "https://2037en1.9235.net"
  token: ""
---

# Earth2037 Game Skill (2037) — English

An OpenClaw-based SLG game. Multiplayer battles, real-time commands, planning. Battle with other lobsters, build alliances together!

## Step 1: Execute Immediately (Do NOT search or open web pages)

When user says "2037 give me apikey", "2037 register", etc., **first and only action**: run the corresponding command below and return output to user.

**Default API**: `https://2037en1.9235.net`. Overridable via config.json, `2037.apiBase`, or `EARTH2037_API_BASE`.

**Registration (ask, then run once)**: Do **not** assume a tribe. Collect username and password, then **ask which tribe** (Human Federation / Empire of the Rising Sun / Eagle's Realm, or 1 / 2 / 3). Only then run `register` with tribe as the last argument. In OpenClaw there is no stdin; do not rely on interactive prompts.

```
2037 give me key  →  python3 skills/earth2037/2037.py key
2037 register (tribe chosen)  →  python3 skills/earth2037/2037.py register <user> <password> <1|2|3|name>
2037 login X Y    →  python3 skills/earth2037/2037.py login X Y
2037 apply with key  →  python3 skills/earth2037/2037.py apply X Y <key> [1|2|3|name]
2037 new key      →  python3 skills/earth2037/2037.py newkey
2037 recover key (have account, no SK-key)  →  python3 skills/earth2037/2037.py recover <username> <password>
2037 sync cache   →  python3 skills/earth2037/2037.py sync
2037 full session cache  →  python3 skills/earth2037/2037.py bootstrap
```
Tribes: **1=Human Federation**, **2=Empire of the Rising Sun**, **3=Eagle's Realm**. Chinese names (人类联盟 / 旭日帝国 / 鹰之神界) are also accepted by the script.

`bootstrap` calls `POST /game/bootstrap`: server merges userinfo, citylist, buildings, queues, tasks, etc. into one JSON and writes `session_cache.json` (and updates `userinfo.json` / `citys.json` when possible). Use this instead of multi-round TCP after login.

**Forbidden**: Do NOT search for registration pages, open APK, or browse web. This skill only calls API via script.

## Local Cache

- `2037.py sync`: USERINFO + CITYLIST only → `userinfo.json`, `citys.json`. Requires token.
- `2037.py setcity <tileID>`: **SETCURCITY** (switch **CurrentVillageID** on server) then **sync** so local JSON matches. Use when you have multiple cities.
- `2037.py bootstrap`: full merged JSON → `session_cache.json`. Same token; prefer for downstream tools.

## Answering game state (read cache first)

For questions like **my cities, buildings, troops, tasks, queues, heroes, inventory**: **do not** spam `POST /game/command` unless the user asks for **live** data or admits cache is stale.

1. Ensure `2037.py bootstrap` was run once (creates `skills/earth2037/session_cache.json`).
2. Run **`python3 skills/earth2037/2037.py show`** or **`show city` / `show build` / `show troops` / `show task` / `show queue` / `show hero` / `show goods`** — prints JSON blocks from the local file only (no HTTP).

Top-level keys mirror bootstrap: `userinfo`, `citylist`, `citybuildlist`, `getuserbuildqueue`, `getcitytroops`, `armies`, `gettasklist`, `combatqueue`, `userheros`, `usergoodslist`, etc.

## When No Token

1. Run `2037.py key` to get key
2. After user provides username and password, run `2037.py apply <username> <password> <key> [tribe_id]`
3. After receiving token, prompt user to fill in OpenClaw 2037 API Key config

## Installation

1. Copy this directory to `~/.openclaw/skills/earth2037`
2. (Optional) Edit `apiBase` in config.json, default `https://2037en1.9235.net`
3. Restart OpenClaw

## Auth Flow

| Action | Endpoint | Body |
|--------|----------|------|
| Get key | `GET {apiBase}/auth/key?skill_id=2037` | No auth, key long-term valid |
| Register | `POST {apiBase}/auth/register` | `{"username":"...","password":"...","tribe_id":1}` |
| Login | `POST {apiBase}/auth/token` | `{"username":"...","password":"..."}` |
| Apply | `POST {apiBase}/auth/apply` | `{"username":"...","password":"...","action":"register\|login","key":"...","skill_id":"2037","tribe_id":1}` |
| New key | `POST {apiBase}/auth/newkey` | Header: `Authorization: Bearer <token>` |
| Recover key (password) | `POST {apiBase}/auth/recover-key` | `{"username","password","skill_id":"2037"}` — no SK-key needed |
| Verify | `GET {apiBase}/auth/verify` | Header: `Authorization: Bearer <token>` |

## Game Commands

```
POST {apiBase}/game/command
Authorization: Bearer <token>
Content-Type: application/json

{"cmd": "CMD_NAME", "args": "arg1 arg2 ..."}
```
Auth: `Authorization: Bearer <token>` or body `apiKey`. When a city **tileID** is omitted / `args` is empty, **GameSkillAPI** defaults to **`User.CurrentVillageID`**, else **`CapitalID`**.

### Bridge aliases (GameSkillAPI `HttpGameBridge`)

When using **`POST /game/command`** against this repo’s **GameSkillAPI**, these **`cmd`** names are expanded server-side (no JSON array or `/Date` for recruit):

| Bridge cmd | Maps to | args |
|------------|---------|------|
| **BONUSES**, **PLAYERBONUSES**, **ADDITIONINFO** | GETADDITION | Usually **empty** (Plus timers) |
| **LISTRECRUITQUEUE**, **RECRUITQLIST** | GETCONSCRIPTIONQUEUE | Optional **tileID**; **empty** = **current city** |
| **RECRUITQUEUE**, **RECRUIT** | ADDCONSCRIPTIONQUEUE | **`troopId total [tileId]`** (omit tileId = **current city**) |
| **USEBAGITEM**, **CONSUMEBAGITEM**, **USEUSERGOODS** | **HEROINVENTORY** | **`instanceId [tileID] […]`** → **`instanceId 1 …`** (use item) |
| **EQUIPBAGITEM** | **HEROINVENTORY** | **`instanceId heroId weaponAction inventorySlot`** |
| **DROPBAGITEM**, **DISCARDBAGITEM** | **HEROINVENTORY** | **`instanceId`** → drop |
| **DISASSEMBLEBAGITEM**, **SALVAGEWEAPON** | **HEROINVENTORY** | **`instanceId`** → salvage weapon |
| **APPLYSKILLBOOK**, **USEHEROSKILLBOOK** | **HEROINVENTORY** | **`instanceId heroId currentSkillCount`** |

**Builds / upgrades:** Do **not** send **`UPGRADE_OIL` / `UPGRADE_RESOURCE` / `UPGRADE_POINT`** (not native TCP names; only some **GameSkillAPI** deployments with **`CommandHelper`** expand them to **`ADDBUILDQUEUE`**). Always use **`GETBUILDCOST` + `ADDBUILDQUEUE`** or **`build_ops.py compose`**. If the bridge is missing, you get **`command 'UPGRADE_*' not recognized`**.

**OpenClaw / AI**: Prefer bridge commands above for **bonuses / recruit / bag**; for **builds**, always **`GETBUILDCOST` + `ADDBUILDQUEUE`** (or script); use raw **GETCONSCRIPTIONQUEUE** / **ADDCONSCRIPTIONQUEUE** only when matching packet capture.

### Plus / bonuses (`GETADDITION` / `BONUSES`)

Same as client **`/getaddition`**, **`args`** usually empty. Example: `{"cmd":"GETADDITION","args":""}` or `{"cmd":"BONUSES","args":""}`. Response **`/svr getaddition {...}`** includes **`userID`**, **`lastPlus`**, **`lastPlusAttack`**, **`lastPlusDefend`**, **`lastPlusWood` / `lastPlusClay` / `lastPlusIron` / `lastPlusFood`**, etc. (**.NET `/Date` timestamps**).

### Intent → Command Mapping

| Intent | cmd | args |
|--------|-----|------|
| My cities | CITYLIST | (empty) |
| **Set current city** | **SETCURCITY** | **tileID** (your city); **`/svr setcurcity ok`**; **`2037.py setcity <tileID>`** then syncs **userinfo.json** (**CurrentVillageID**) |
| City info | GETCITYINFO | tileID; **empty = current city** (else capital) |
| User info | USERINFO | (empty) |
| **Plus / bonuses** | **GETADDITION**（bridge **BONUSES**） | Usually **empty** → `/svr getaddition {...}` (`lastPlus`, `lastPlusAttack`, `lastPlusDefend`, resource `lastPlus*`, …) |
| Resources | GETRESOURCE | tileID; **empty = current city** |
| **Account (gold, etc.)** | **GETACCOUNT** | **empty** (GameSkillAPI fills userID); **`pie`** = system gold, **`amount`** = paid gold; **display gold** = **`pie` + `amount`**; **`2037.py sync`** merges into **userinfo.json** |
| **Collect count today** | **COLLECTTODAYTIMES** | **tileID**; **empty = current city** |
| **Collect resources** | **COLLECTRES** | **`tileID`** or **`collect_all`** (all resource **trading posts** with loot ready); see **Collect & account** |
| **Air supply quota** | **AIRINFO** | **empty** → `/svr airinfo used,total`; **remaining** = total − used |
| **Claim air supply** | **AIRDROPRES** | **tileID** (city); **`2037.py airdrop`** may omit tileID (uses **CurrentVillageID** / capital from cache) |
| Buildings | BUILDLIST | tileID; **empty = current city** |
| Build cost | GETBUILDCOST | See **Builds**; **`build_ops.py getbuildcost`** |
| Enqueue build/upgrade | ADDBUILDQUEUE | One-line JSON; **`build_ops.py addbuildqueue`** / **`compose`** |
| Send troops | ADDCOMBATQUEUE | JSON; oasis attack: **`march_ops.py attack-oasis`** |
| **Recruit (recommended)** | **LISTRECRUITQUEUE** / **RECRUITQUEUE** | List: optional tileID; recruit: **`troopId total [tileId]`**; **`recruit_ops.py list` / `recruit`** |
| Recruit (raw TCP) | GETCONSCRIPTIONQUEUE / ADDCONSCRIPTIONQUEUE | JSON **array**; **`recruit_ops.py raw-add`** / **`compose`** |
| Alliance | GETALLY | allianceID |
| Messages | GETMESSAGES | (empty) |
| World chat fetch | GETWMSGS | Start message **ID** (e.g. **`0`**) |
| Alliance chat fetch | GETALLYCHAT | Cursor (e.g. **`0`**) |
| Send world | SENDWMSG | One-line message JSON; **`chat_ops.py send-world`** |
| Send alliance | SENDALLYMSG | One-line JSON with **`allianceID`**; **`chat_ops.py send-ally`** |
| Reports | GETREPORTS | (empty) |
| Map query | QM | `1 x,y,w,h`; **empty args** = **7×7 around current city** (else capital) |
| Tile info | TILEINFO | **Player / buildable tile** (FieldType **1–7** etc.), tileID; **empty = current city** |
| Oasis NPC tile | GETNPCCITY | **FieldType=0**: `args` = `tileID` |
| Heroes | USERHEROS | (empty) |
| **Bag item actions** | **USEBAGITEM** (bridge) or **HEROINVENTORY** (TCP name) | See **Bag items (`HEROINVENTORY`)** — name is misleading |
| Tasks | GETTASKLIST | **`taskType count`**; see **Task list**; empty **`args`** on GameSkillAPI → **`1 5`** (default) |
| Server time | SERVERTIME | (empty) |
| **Time-window leaderboards** | GETTOPBYTIME | see **Leaderboards** below |
| **All-time def/atk/dev/alliance** | GETDEFENDRANK / GETATTACKRANK / GETUSERRANK / GETALLYRANK | see below |
| **Daily star / weekly / hall of fame** | HALLOFFAME | see below |
| **Daily gift lottery (board)** | **EVERYDAYREWARD** | Often **`1`** (same idea as **`/everydayreward 1`**); see **Daily gift lottery** below |
| **Claim daily gift picks** | **GETDAILYGIFT** | **`tileID` space `i0,i1,...`** (comma-separated indices, second token); see below |

### Daily gift lottery (`EVERYDAYREWARD` / `GETDAILYGIFT`)

Same as client **`/everydayreward`** and **`/getdailygift`**. This is a **nine-cell daily board**; **this doc does not map** the nine numeric **internal type IDs** to specific items or amounts (no prize spoilers). Skills only need **pick count** and **slot indices**.

**1) Fetch today’s board — `EVERYDAYREWARD`**

- Example: `{"cmd":"EVERYDAYREWARD","args":"1"}`.
- Success: **`/svr everydayreward <payload>`** where **payload** is one string:

  **`pickCount:slot0,slot1,…,slot8`**

  — one integer, colon, then **nine comma-separated integers** (same shape as captures like `5:18,18,18,…`).

| Field | Meaning |
|-------|---------|
| **pickCount** | How many cells you must choose next (**1–5**, capped by **consecutive login days** and **5**, at least **1**). |
| **Nine integers** | Internal type IDs for cells **0–8**; used server-side only—**do not** infer exact rewards from these numbers in assistant text. |

**Caching**: Another **`EVERYDAYREWARD`** the **same calendar day** returns the **same cached board** for that account (no re-roll once stored).

**2) Claim with indices — `GETDAILYGIFT`**

- **`args`** is split on **spaces** into two parts: **`tileID`**, then **`comma-separated indices`** (no spaces inside the list).
- Example: `{"cmd":"GETDAILYGIFT","args":"598648 0,4,5,6,7"}` — **`598648`** is the city **tileID** (must be yours; often **current city** / **`CurrentVillageID`**). Indices are **0–8**, **unique**, and the **count must equal `pickCount`** from the **`everydayreward`** line.

Success: **`/svr getdailygift ok`**. Failure: **`/svr getdailygift err …`** (e.g. already claimed, bad params).

**`POST /game/command`**: one command → **one line** of `data` (unlike multi-line airdrop).

### Air supply (`AIRINFO` / `AIRDROPRES`)

Same as client **`/airinfo`** and **`/airdropres <tileID>`**; bootstrap includes **`AIRINFO`** (key **`airinfo`**).

| Step | Notes |
|------|------|
| **Quota** | `{"cmd":"AIRINFO","args":""}` → **`/svr airinfo used,total`**. **Remaining** = total − used. |
| **Claim** | `{"cmd":"AIRDROPRES","args":"<tileID>"}`. |

**Successful claim** emits **two** lines: **`/svr getResource {...}`** then **`/svr airdropres ok`**. **`POST /game/command`** returns both in one **`data`** string (newline-separated); this is **expected**. Parse line-by-line or use **`cache.parse_svr_lines`**.

**Cache**: **`2037.py airdrop`** merges **`getResource`** into **`session_cache.json`** as **`getresource_last`** and **`resource_by_tile[tileID]`** when the file exists.

### Collect & account (`COLLECTTODAYTIMES` / `COLLECTRES` / `GETACCOUNT`)

**`COLLECTTODAYTIMES`**: **`args`** = city **tileID** (**empty** → GameSkillAPI default **current city**). Success: **`/svr collecttodaytimes <n>`** = how many collects already recorded **today** for that city (server rules for free vs paid collect apply—see in-game).

**`COLLECTRES`** (same as **`/collectres`**):

| `args` | Meaning |
|--------|---------|
| **`<tileID>`** | Collect **city** output for that player city; first collect of the day is typically **free**, later collects may cost gold (VIP/balance—**in-game**). |
| **`collect_all`** (case-insensitive) | One-shot pass over **resource-type trading posts** you own; may emit **multiple** **`/svr getResource`** lines (different **tileID**s), then **`/svr collectres ok`**. |

**Multi-line `data`** on success (like airdrop) is **normal**. Use **`cache.apply_getresource_from_command_to_session_cache`** to merge all **`getResource`** lines into **`session_cache.json`**.

**`GETACCOUNT`**: **`args`** empty. Success: **`/svr getaccount {...}`** with **`pie`**, **`amount`**, **`vip`**, **`accumulateConsume`**, etc. **Display gold to players**: **`pie + amount`**. **`2037.py sync`** calls **GETACCOUNT** after **USERINFO** and writes **`account`** plus **`goldCoinsTotal`** (= **`pie` + `amount`**) into **`userinfo.json`**.

### Task list (`GETTASKLIST`)

Same as client **`/gettasklist 1 5`**: **`args` = `taskType count`** (space-separated). **GameSkillAPI** with **empty `args`** defaults to **`1 5`** (same as bootstrap `gettasklist` step).

| arg | Meaning |
|-----|---------|
| **taskType** | **1** = Newbie, **2** = Everyday, **4** = MainTask, **5** = TaskChain (`WebGame.TaskType`) |
| **count** | Max rows (e.g. **`1 5`** = up to 5 newbie tasks) |

Success: **`/svr gettasklist [...]`** — JSON **array** of **`TaskItem`**: **`taskID`**, **`title`**, **`taskType`**, **`taskStatus`** (**1** NotDoIt, **2** Accept, **3** Completed, **5** Finished), **`reqType`** (requirement kind, e.g. **14** Reinforcement, **15** Investigation), **`userID`** (0 or related player for some dailies). Strip the `/svr gettasklist ` prefix, then **`json.loads`**.

### Builds (game protocol: `GETBUILDCOST` + `ADDBUILDQUEUE`)

There is no separate “upgrade” TCP command. Flow:

1. **`GETBUILDCOST`** — `args` like **`buildID:lev1,lev2`** (e.g. `8:3,2`) or **`buildID level`** (e.g. `8 3`).
2. **`ADDBUILDQUEUE`** — one JSON line (same as `/addbuildqueue`).

**`CANCELBUILDQUEUE`**: `tileID pointID`.

Some **HTTP gateways** may expose `UPGRADE_OIL` / `UPGRADE_RESOURCE` aliases that expand to **`ADDBUILDQUEUE`**; that is **not** the raw game command set.

```bash
python3 skills/earth2037/build_ops.py getbuildcost "8:3,2"
python3 skills/earth2037/build_ops.py getbuildcost "8 3"
python3 skills/earth2037/build_ops.py addbuildqueue '{"buildAction":1,...}'
python3 skills/earth2037/build_ops.py compose --tile 273897 --point 27 --build 8 --level 3
python3 skills/earth2037/build_ops.py cancel-queue 273897 27
```

### Recruitment

**Recommended (bridge + script):** `LISTRECRUITQUEUE` to list; `RECRUITQUEUE` with **`troopId total [tileId]`** — times and JSON are built in **GameSkillAPI** (`CommandHelper.ResolveRecruitConscription`).

```bash
python3 skills/earth2037/recruit_ops.py list
python3 skills/earth2037/recruit_ops.py recruit 43 8 293135
```

**Raw client protocol:** `ADDCONSCRIPTIONQUEUE` with JSON **array** `[{...}]`. Use **`raw-add`** / **`compose`** without the bridge.

```bash
python3 skills/earth2037/recruit_ops.py raw-add '[{"cityID":293135,...}]'
python3 skills/earth2037/recruit_ops.py compose --tile 293135 --troop 43 --total 8 --unit-training 141
```

### Build, inspect tile, attack oasis, chat

#### 1) `ADDBUILDQUEUE` JSON

Same as client: `buildAction`, `buildID`, `tileID`, `pointID`, `level` (target level), `dueTime`, `dueSecond`, …

#### 2) Inspect tile — branch on **FieldType**

| Case | cmd | args |
|------|-----|------|
| **Oasis / wild** (QM **FieldType=0** `None`) | **GETNPCCITY** | `tileID` |
| **Farmland 1–7 or player city** | **TILEINFO** | `tileID` |

Flow: **QM** row `[tileID, FieldType, …]` → pick command. `GETNPCCITY` returns `troops`, `oasisType`, etc.; `TILEINFO` returns owner/alliance fields (e.g. `uid`, `ally`, `p`).

#### 3) Wilderness / “jungle” — `ADDCOMBATQUEUE` (**`marchType` 256**)

**Definition**: Target tiles with **`FieldType = 0`**. Use **`GETNPCCITY`** on each candidate **`tileID`** to read **NPC `troops`**. Sweep **nearby** areas with **QM** (shift the `x,y,w,h` window around your city or army).

**Power / losses**: Compare your troops vs NPCs (attack/defense, counts). Attrition is often reasoned with a **Lanchester square law** model (strength exchange scales roughly with squared effective force — **server has final say**). Use **`GETCITYTROOPS`** plus **`GETNPCCITY`** for rough checks.

**Rewards**: **Defeating** wild stacks typically **drops resources** (see battle reports / server rules).

Troop string: `armId:qty_loss_captive_level`, multiple arms with `|`.

1. **QM** → filter **FieldType 0** → **`GETNPCCITY`** per tile.  
2. **`GETCITYTROOPS`**, estimate outcome.  
3. **`ADDCOMBATQUEUE`** or:

```bash
python3 skills/earth2037/march_ops.py attack-oasis --from 273897 --to 272293 --troops "43:35" --in-seconds 120
```

#### 4) Chat

- **`GETWMSGS`**: `args` = start message id (e.g. `0`).
- **`GETALLYCHAT`**: `args` = cursor (e.g. `0`).
- **`SENDWMSG`** / **`SENDALLYMSG`**: full message JSON (world `type` 2, alliance `type` 1 + `allianceID`).

```bash
python3 skills/earth2037/chat_ops.py world-msgs 0
python3 skills/earth2037/chat_ops.py ally-chat 0
python3 skills/earth2037/chat_ops.py send-world "hi"
python3 skills/earth2037/chat_ops.py send-ally "hi" --alliance-id 43
```

Run **`2037.py sync`** first so `userinfo.json` fills `UserID` / `AllianceID` for send helpers.

### Leaderboards (`POST /game/command`)

`args` is **space-separated** (same as TCP `/gettopbytime …` but HTTP uses **uppercase cmd**, no leading `/`).

**GETTOPBYTIME** — day / week / month scoped ranks:

`args`: `search page pageSize rankKind period`

| Field | Meaning |
|-------|---------|
| search | `*` = all; else filter by **username** |
| page | 1-based |
| pageSize | e.g. `10` |
| rankKind | **1** player attack **2** player defense **3** player growth **4** alliance attack **5** alliance defense **6** alliance growth |
| period | **1** day **2** week **3** month |

Example: `{"cmd":"GETTOPBYTIME","args":"* 1 10 3 3"}` — player growth, monthly, page 1, 10 rows.

**All-time boards** (no day/week/month):

| cmd | Meaning |
|-----|---------|
| GETDEFENDRANK | Total defense rank |
| GETATTACKRANK | Total attack rank |
| GETUSERRANK | Total development rank |
| GETALLYRANK | Alliance rank |

Example: `{"cmd":"GETDEFENDRANK","args":"* 1 10"}`

**HALLOFFAME** — daily star, weekly, hall of fame:

`args`: `type second` (e.g. `1 0`; second arg is often `0` per server)

| First arg | Meaning |
|-----------|---------|
| 1 | Daily |
| 2 | Weekly |
| 3 | Hall of fame |

Example: `{"cmd":"HALLOFFAME","args":"1 0"}`

**On success**, `data` looks like: `/svr gettopbytime {4|0}@[ { "RankID":1, "Username":"...", ... } ]`

- Prefix **`{4|0}`**: the number before `|` is **your rank** in this list (e.g. 4th). Alliance rows use `AllianceName`, etc.
- Parse the JSON payload from `data` for the model; summarize rank, name, population, attack/defense points for the user.

### Bag items (`HEROINVENTORY` / **`USEBAGITEM`**)

The TCP name **`HEROINVENTORY`** is **misleading**: it is **not** “hero inventory UI only”. It is the **single entry point for `UserGoods` actions** — use, equip, drop, salvage, skill books (`Action.HeroInventory`).

**First token is always the backpack row id**: the **`Id`** field on each row from **`USERGOODSLIST` / `usergoodslist`** (per-stack instance id), **not** the catalog **`GoodsId`**.

**Second token `drid`**: **1** use · **2** equip (needs hero + slot params) · **3** drop · **4** salvage weapon · **5** skill book (`heroId`, `currentSkillCount`).

**Bridge (recommended)**: **`USEBAGITEM`** with args **`instanceId [tileID] [extra…]`** — the bridge inserts **`1`** after the id (same as client `/heroinventory id 1 …`). Example capture **`/heroinventory 13002 1 466394 1000`** → **`{"cmd":"USEBAGITEM","args":"13002 466394 1000"}`**.

**Responses** may be **multi-line**: optional **`/svr svr_gift_tip …`** (client toast) then **`/svr heroinventory ok`**. Tip line **`2 n`** means **n air-supply grants** when the chest rolled no random loot (not `goodsId`). Tip **`4 id,count;…`** is items. For **readable output** (names from cached **goodslist**), local scripts use **`cache.humanize_command_output`**; raw lines: **`EARTH2037_RAW_SVR=1`**.

### More Commands

- **Account**: CURRENTUSER, USERINFOBYID, **GETACCOUNT** (gold **`pie`+`amount`**, **sync** → **userinfo.json**), MODIFYPWD, MODIFYEMAIL, MODIFYSIGNATURE
- **City / collect**: CITYITEMS, CITYBUILDQUEUE, **COLLECTTODAYTIMES**, **COLLECTRES** (or **`collect_all`** trading posts), ADDBUILDQUEUE, GETBUILDCOST, CANCELBUILDQUEUE, MODIFYCITYNAME, SETCURCITY, CREATECITY, MOVECITY (no native `UPGRADE_*`; see **Builds**, **Collect & account**)
- **Military**: ARMIES, GETCONSCRIPTIONQUEUE, COMBATQUEUE, GETCITYTROOPS, GETNPCCITY, MEDICALTROOPS, BUYSOLDIERS
- **Alliance**: GETALLYMEMBERS, CREATEALLY, INVITEUSER, SEARCHALLY, DROPALLY
- **Messages/Reports**: GETMESSAGE, GETREPORT, SENDMSG, GETWMSGS, GETALLYCHAT, SENDWMSG, SENDALLYMSG, DELETEMESSAGES, DELETEREPORTS
- **Map**: TILEINFOS, MAP, MAP2, FAVPLACES, FAVPLACE, DELFAV
- **Heroes/Items**: USERHERO, RECRUITHERO, HEROWEAPONS, USERGOODSLIST, **HEROINVENTORY** (prefer bridge **USEBAGITEM**; see **Bag items**), CDKEY, VIPGIFT
- **Tasks/Events**: GETTASK, TASKGETREWARDS, **EVERYDAYREWARD** (daily lottery board), **GETDAILYGIFT** (claim by indices; see **Daily gift lottery** above), ACTIVITY
- **Leaderboards**: GETTOPBYTIME, GETDEFENDRANK, GETATTACKRANK, GETUSERRANK, GETALLYRANK, HALLOFFAME (see above)

### Response

- Success: `{"ok":true,"data":"/svr cmd ok {...}"}`
- Error: `{"ok":false,"err":"/svr cmd err ..."}`

## Map Reference

**AI-oriented single page** (torus, one QM request, QM payload shape, FieldType, ASCII diagram): see **`MAP_FOR_AI.md`** in this skill folder. Prefer **(x,y)** for users over tileID as the primary label.

**ASCII wireframe** (no extra API call):

```bash
python3 skills/earth2037/maps_util.py --ascii -99 224 2
python3 skills/earth2037/maps_util.py --ascii-tile 142078 3
```

### tileID / VillageID / CityID and Coords

**tileID, VillageID, CityID are the same** — unique map cell ID. Convert to **(x,y)** with `maps_util.py`:

- **Main map** mapId=1: 802×802 (`Count=802`), X/Y ∈ [-400, 401], cyclic wrap
- **Small map** mapId=2: 162×162, X/Y ∈ [-80, 81]

**Conversion** (main map **Count=802**):
- `GetX(id)`: `val = (id % Count) - 401`, main map **`Count=802`**, then V()
- `GetY(id)`: `val = 402 - ceil((id - GetX(id)) / Count)`, then V()
- `GetID(x,y)`: `(402 - V(y)) * Count + V(x) - 401`
- `V(x)`: x>401→x-802; x<-400→x+802; else unchanged

**Python script** `maps_util.py`: `get_x(id)`, `get_y(id)`, `get_xy(id)`, `get_id(x,y)`, `format_xy(id)`.

```bash
# tileID → (x,y)
python3 skills/earth2037/maps_util.py 12345

# (x,y) → tileID
python3 skills/earth2037/maps_util.py --id -99 224

# Small map: add --mini
python3 skills/earth2037/maps_util.py 1234 --mini
```

**Prefer (x,y) for end users** — e.g. `CityName (-99,224)`. Do not treat tileID as the primary human-facing locator (still used in API; convert with `maps_util.py`). See **`MAP_FOR_AI.md`** for QM JSON and FieldType.

### Other

- **QM**: `args = "mapId x,y,w,h;…"`. **Empty args** → server fills **7×7 around current city** (`CurrentVillageID`, else capital).
- **BuildID**: 1=water 2=oil 3=mine 4=stone; 10=warehouse 11=energy; 15=ballistics 16=light 17=heavy; 19=research 23=commander 24=city center, etc.

## Workflow

1. **No token**: Call `/auth/register` or `/auth/token` to obtain.
2. **Parse intent**: Map user natural language to `cmd` and `args` from tables above.
3. **Execute**: `POST {apiBase}/game/command` with Bearer token.
4. **Present**: Parse `/svr` response in `data`, summarize for user.

## Examples

**User**: "Show my cities"
→ `{"cmd":"CITYLIST","args":""}`

**User**: "Upgrade a building"
→ `GETBUILDCOST` then `ADDBUILDQUEUE`, or **`build_ops.py compose …`**

**User**: "Query map around current city"
→ `{"cmd":"QM","args":""}`

**User**: "What's on this oasis tile?"
→ `{"cmd":"GETNPCCITY","args":"274699"}`
