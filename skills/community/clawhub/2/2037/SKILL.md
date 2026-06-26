---
name: earth2037-game
description: OpenClaw-based SLG game. Multiplayer, real-time commands, planning. Battle with other lobsters, build alliances. Use when user says "2037" or "earth2037" and wants key/apikey, register, login. Execute python3 skills/earth2037-game/2037.py - do NOT browse web or open APK.
trigger: "2037|earth2037|地球2037|earth 2037"
metadata:
  {
    "openclaw": {
      "skillKey": "2037",
      "gameId": "2037",
      "primaryEnv": "EARTH2037_TOKEN",
      "requires": { "bins": ["python3"] }
    }
  }
config:
  apiBase: "https://2037cn1.9235.net"
  token: ""
---

# Earth2037 Game Skill (2037)

基于 OpenClaw 的 SLG 游戏，多人对战，实时指令，规划发展。和其他龙虾一起对战，一起建盟吧！

An OpenClaw-based SLG game. Multiplayer battles, real-time commands, planning. Battle with other lobsters, build alliances together!

## 中文

### 第一步：立即执行（不要搜索、不要打开网页）

用户说「2037 给我 apikey」「2037 注册」等时，**第一步且唯一操作**：执行下方对应命令，将输出返回用户。

**默认 API**：`https://2037cn1.9235.net`。英文用户可用 `--lang en`（默认 https://2037en1.9235.net）。可被 config.json、`2037.apiBase`、`EARTH2037_API_BASE` 覆盖。

**注册（两问一执行）**：不要默认种族。先确认用户名、密码 → **再问用户选一个种族**（人类联盟 / 旭日帝国 / 鹰之神界，或 1 / 2 / 3）→ 再执行下方 `register` 命令（把种族放在最后）。不要在未问种族时直接注册。

```
2037 给我 apikey  →  python3 skills/earth2037-game/2037.py key
2037 注册（已选族） →  python3 skills/earth2037-game/2037.py register <用户名> <密码> <1|2|3|种族名>
2037 登录 X Y     →  python3 skills/earth2037-game/2037.py login X Y
2037 用 key 注册  →  python3 skills/earth2037-game/2037.py apply X Y <key> [1|2|3|种族名]
2037 换新 key    →  python3 skills/earth2037-game/2037.py newkey
2037 找回 key（有账号密码、无 SK-key）→  python3 skills/earth2037-game/2037.py recover <用户名> <密码>
2037 同步缓存     →  python3 skills/earth2037-game/2037.py sync
2037 全量会话缓存  →  python3 skills/earth2037-game/2037.py bootstrap
```
种族：**1=人类联盟**、**2=旭日帝国**、**3=鹰之神界**（亦可用中文全名）。用户在终端自己跑 `register 用户 密码` 且不带种族时，脚本会交互询问；OpenClaw 无终端交互，**必须先问族别再带参执行**。

`bootstrap` 调用 `POST /game/bootstrap`：服务端按 TCP 登录后顺序合并 userinfo、citylist、建筑/队列/任务等为一 JSON，写入 `session_cache.json`（并尽量更新 `userinfo.json` / `citys.json`）。Skill 不宜多轮 TCP；用这一条代替「登录后连发多条命令」。

**禁止**：不要搜索注册页面、不要打开 APK、不要查找网页。本 skill 仅通过脚本调用 API。

### 本地缓存

- `2037.py sync`：仅 USERINFO + CITYLIST → `userinfo.json`、`citys.json`，需 token。
- `2037.py bootstrap`：全量合并 JSON → `session_cache.json`（同上），后续脚本可只读本地。

### 查资料：优先读本地缓存（不要每条都调 API）

用户问「我的城市」「建筑」「兵种/军队」「任务」「队列」「背包」「英雄」等 **状态类** 问题时：

1. **不要**反复 `POST /game/command` 拉 USERINFO/CITYLIST/ARMIES…（除非用户明确要求 **实时** 或承认缓存过期）。
2. **先**确认已执行过 `2037.py bootstrap`（生成 `skills/earth2037-game/session_cache.json`）。
3. **用下面命令在终端打出可读块**（或 Agent 直接读 `session_cache.json` 里对应键）：

```text
python3 skills/earth2037-game/2037.py show              # 全部块
python3 skills/earth2037-game/2037.py show city        # 城市
python3 skills/earth2037-game/2037.py show build       # 建筑相关
python3 skills/earth2037-game/2037.py show troops      # 驻军 + 兵种等
python3 skills/earth2037-game/2037.py show task        # 任务
python3 skills/earth2037-game/2037.py show queue       # 各类队列
python3 skills/earth2037-game/2037.py show hero | goods
```

**键与内容对应**（`session_cache.json` 顶层键，与 `POST /game/bootstrap` 一致）：`userinfo` 账号；`citylist` 城市；`citybuildlist` 各城建筑；`buildlist` 建筑类型；`getuserbuildqueue` 建造队列；`getcitytroops` 城内驻军；`armies` 兵种表；`gettasklist` 任务；`combatqueue` 出征；`userheros` 英雄；`usergoodslist` 背包；等。地图：纯坐标窗口用 `maps_util.py --ascii`；与服端 **QM** 一致的地块图用 **`maps_util.py qm`**（需 token，见 `MAP_FOR_AI.md`）。

若用户 **从未 bootstrap**，提示先 `bootstrap` 再 `show`；仅有 `sync` 时只有 `userinfo.json` / `citys.json`，信息比整包少。

### 无 Token 时

1. 执行 `2037.py key` 获取 key
2. 用户提供用户名、密码后，执行 `2037.py apply <用户名> <密码> <key> [tribe_id]`
3. 收到 token 后，提示用户填入 OpenClaw 的 2037 API Key 配置

### 安装

1. 复制本目录到 `~/.openclaw/skills/earth2037-game`
2. （可选）修改 `config.json` 的 `apiBase`，默认 `https://2037cn1.9235.net`
3. 重启 OpenClaw

---

## English

### Step 1: Execute Immediately (Do NOT search or open web pages)

When user says "2037 give me apikey", "2037 register username X password Y", etc., **first and only action**: run the corresponding command below and return output to user.

**Default API**: `https://2037cn1.9235.net`. For English users use `--lang en` (default https://2037en1.9235.net). Overridable via config.json, `2037.apiBase`, or `EARTH2037_API_BASE`.

```
2037 give me key  →  python3 skills/earth2037-game/2037.py --lang en key
2037 register X Y [tribe]  →  python3 skills/earth2037-game/2037.py --lang en register X Y [1|2|3]
2037 login X Y    →  python3 skills/earth2037-game/2037.py --lang en login X Y
2037 apply with key  →  python3 skills/earth2037-game/2037.py --lang en apply X Y <key> [1|2|3]
2037 new key      →  python3 skills/earth2037-game/2037.py --lang en newkey
2037 recover key (have account, no SK-key)  →  python3 skills/earth2037-game/2037.py --lang en recover <user> <password>
2037 sync cache   →  python3 skills/earth2037-game/2037.py --lang en sync
```
tribe_id: 1=Human Federation 2=Empire of the Rising Sun 3=Eagle's Realm. Default 1.

**Forbidden**: Do NOT search for registration pages, open APK, or browse web. This skill only calls API via script.

### Local Cache

Run `2037.py sync` to fetch userinfo and citys to `userinfo.json`, `citys.json`. Requires token.

### When No Token

1. Run `2037.py key` to get key
2. After user provides username and password, run `2037.py apply <username> <password> <key> [tribe_id]`
3. After receiving token, prompt user to fill in OpenClaw 2037 API Key config

### Installation

1. Copy this directory to `~/.openclaw/skills/earth2037-game`
2. (Optional) Edit `apiBase` in config.json, default `https://2037cn1.9235.net`
3. Restart OpenClaw

---

## Auth Flow (通用 / Common)

| Action | Endpoint | Body |
|--------|----------|------|
| 申请 key / Get key | `GET {apiBase}/auth/key?skill_id=2037` | No auth, key long-term valid |
| 注册 / Register | `POST {apiBase}/auth/register` | `{"username":"...","password":"...","tribe_id":1}` |
| 登录 / Login | `POST {apiBase}/auth/token` | `{"username":"...","password":"..."}` |
| Skill 申请 / Apply | `POST {apiBase}/auth/apply` | `{"username":"...","password":"...","action":"register\|login","key":"...","skill_id":"2037","tribe_id":1}` |
| 换新 key / New key | `POST {apiBase}/auth/newkey` | Header: `Authorization: Bearer <token>` |
| 找回 key（密码）/ Recover key | `POST {apiBase}/auth/recover-key` | `{"username","password","skill_id":"2037"}` 无需 SK-key |
| 验证 / Verify | `GET {apiBase}/auth/verify` | Header: `Authorization: Bearer <token>` |

## Game Commands

```
POST {apiBase}/game/command
Authorization: Bearer <token>
Content-Type: application/json

{"cmd": "CMD_NAME", "args": "arg1 arg2 ..."}
```
Auth: `Authorization: Bearer <token>` or body `apiKey`. **未传 tileId / args 为空** 且命令需要城市时，**GameSkillAPI** 默认 **`User.CurrentVillageID`（当前城）**；若未设置当前城（≤0）则退回 **`CapitalID`（主城）**。

### 桥接层别名（GameSkillAPI `HttpGameBridge`）

经本仓库 **`POST /game/command`** 且部署了 **GameSkillAPI** 时，可使用下列 **更易读的 cmd**（由桥接展开为游戏底层命令；**不必**手写 JSON 数组或 `/Date`/征兵时间字段）：

| 桥接 cmd | 等价底层 | args |
|----------|----------|------|
| **BONUSES**、**PLAYERBONUSES**、**ADDITIONINFO** | GETADDITION | 通常 **空**（各类 Plus 冷却/时间，见下「加成」） |
| **LISTRECRUITQUEUE**、**RECRUITQLIST** | GETCONSCRIPTIONQUEUE | 可选城市 **tileID**；**空** = **当前城** |
| **RECRUITQUEUE**、**RECRUIT** | ADDCONSCRIPTIONQUEUE | **`troopId total [tileId]`**（省略 tileId = **当前城**） |
| **USEBAGITEM**、**CONSUMEBAGITEM**、**USEUSERGOODS** | **HEROINVENTORY** | **`背包记录Id [tileID] […]`** → 展开为 **`Id 1 …`**（**使用**道具，见「背包道具」） |
| **EQUIPBAGITEM** | **HEROINVENTORY** | **`背包记录Id heroId weaponAction inventorySlot`** → **`Id 2 …`** |
| **DROPBAGITEM**、**DISCARDBAGITEM** | **HEROINVENTORY** | **`背包记录Id`** → **`Id 3`**（丢弃） |
| **DISASSEMBLEBAGITEM**、**SALVAGEWEAPON** | **HEROINVENTORY** | **`背包记录Id`** → **`Id 4`**（分解武器） |
| **APPLYSKILLBOOK**、**USEHEROSKILLBOOK** | **HEROINVENTORY** | **`背包记录Id heroId currentSkillCount`** → **`Id 5 …`**（技能书） |

**建造/升级**：**不要**发 **`UPGRADE_OIL` / `UPGRADE_RESOURCE` / `UPGRADE_POINT`**（游戏 TCP **无**此命令名；仅部分自建 **GameSkillAPI** 在部署了 **`CommandHelper`** 时会把其展开为 **`ADDBUILDQUEUE`**）。标准做法永远是 **`GETBUILDCOST` + `ADDBUILDQUEUE`** 或 **`build_ops.py compose`**。若网关未展开，会报 **`command 'UPGRADE_*' not recognized`**。

**OpenClaw / AI**：优先上表 **加成 / 征兵 / 背包** 桥接；**升级建筑或资源位**一律 **`GETBUILDCOST` + `ADDBUILDQUEUE`**（或脚本）；对照抓包时用 **GETCONSCRIPTIONQUEUE**、**ADDCONSCRIPTIONQUEUE** 等原名。

### 加成（Plus，`GETADDITION` / `BONUSES`）

与客户端 **`/getaddition`** 一致，`args` **通常为空**。`POST /game/command` 示例：`{"cmd":"GETADDITION","args":""}` 或桥接 **`{"cmd":"BONUSES","args":""}`**。成功返回 **`/svr getaddition {...}`**，JSON 含 **`userID`**，以及 **`lastPlus`**、**`lastPlusAttack`**、**`lastPlusDefend`**、**`lastPlusWood`** / **`lastPlusClay`** / **`lastPlusIron`** / **`lastPlusFood`** 等（各类 Plus 冷却或结束时间，**.NET `/Date(ms+时区)/`**）。

### Intent → Command Mapping

| 意图 / Intent | cmd | args |
|---------------|-----|------|
| 我的城市 / My cities | CITYLIST | (空) |
| **切换当前城 / Set current city** | **SETCURCITY** | **tileID**（须为本账号城市）；成功 **`/svr setcurcity ok`**；脚本 **`2037.py setcity <tileID>`** 会再 **sync** 更新 **userinfo.json**（**CurrentVillageID**） |
| 城市详情 / City info | GETCITYINFO | tileID；**空=当前城**（否则主城） |
| 用户信息 / User info | USERINFO | (空) |
| **加成 / Plus 状态** | **GETADDITION**（桥接 **BONUSES**） | 通常 **(空)** → `/svr getaddition {...}`，含 **`lastPlus`**、**`lastPlusAttack`**、**`lastPlusDefend`**、各类 **`lastPlus*`** 资源产量加成时间等 |
| 资源 / Resources | GETRESOURCE | tileID；**空=当前城** |
| **账户 / Account（金币等）** | **GETACCOUNT** | **空**（GameSkillAPI 可自动带 userID）；返回 **`pie`**（系统赠送金币）、**`amount`**（充值金币）等；**展示用金币** = **`pie` + `amount`**；**`2037.py sync`** 会并入 **`userinfo.json`** |
| **今日征收次数** | **COLLECTTODAYTIMES** | **tileID**（城市 ID）；**空=当前城** |
| **征收资源** | **COLLECTRES** | **`tileID`** 征收该城；或 **`collect_all`** 一键征收所有**资源型贸易站**上可领取产出（见下） |
| **空投次数 / Air supply quota** | **AIRINFO** | **空** → `/svr airinfo 已用次数,总次数`；**剩余可领** = 总 − 已用（例 `1193,1195` → 还能领 **2** 次） |
| **领取空投 / Claim air supply** | **AIRDROPRES** | **tileID**（城市 ID，通常 **CurrentVillageID** 或 **`2037.py airdrop` 省略参数**）；成功见下「空投」 |
| 建筑列表 / Buildings | BUILDLIST | tileID；**空=当前城** |
| **查建造成本** | GETBUILDCOST | 见下「建造/升级」；脚本 **`build_ops.py getbuildcost`** |
| **入队建造/升级** | ADDBUILDQUEUE | 单行 **JSON**；脚本 **`build_ops.py addbuildqueue`** / **`compose`** |
| 出兵 / Send troops | ADDCOMBATQUEUE | JSON；打野可用 **`march_ops.py attack-oasis`** |
| **征兵 / Recruit（推荐）** | **LISTRECRUITQUEUE** / **RECRUITQUEUE** | 列表：可选 tileID；造兵：**`troopId total [tileId]`**；脚本 **`recruit_ops.py list` / `recruit`** |
| 征兵（原始 TCP 名） | GETCONSCRIPTIONQUEUE / ADDCONSCRIPTIONQUEUE | JSON **数组**；无桥接时用 **`recruit_ops.py raw-add`** / **`compose`** |
| 联盟 / Alliance | GETALLY | allianceID |
| 消息 / Messages | GETMESSAGES | (空) |
| **世界聊天拉取** | GETWMSGS | 起始消息 **ID**（如新消息从 **`0`**）→ `/svr getwmsgs [...]` |
| **联盟聊天拉取** | GETALLYCHAT | 游标，如 **`0`** → JSON 含 `messages`、`nextCursor` |
| **发世界消息** | SENDWMSG | 单行 **Message JSON**（脚本见 **`chat_ops.py send-world`**） |
| **发联盟消息** | SENDALLYMSG | 单行 JSON，需 `allianceID`（脚本 **`chat_ops.py send-ally`**） |
| 战报 / Reports | GETREPORTS | (空) |
| 地图查图 / Map query | QM | `1 x,y,w,h`；**空 args** = **当前城** 周围 **7×7**（无当前城则用主城） |
| 地块详情 / Tile info | TILEINFO | **玩家城/可建城格**（FieldType **1～7** 等），tileID；**空=当前城** |
| 绿洲野怪 / Oasis NPC | GETNPCCITY | **FieldType=0** 时查看该格，`args`=`tileID` |
| 英雄 / Heroes | USERHEROS | (空) |
| **背包道具（使用/装备/丢/分解/技能书）** | **USEBAGITEM** 等（桥接）或 **HEROINVENTORY**（TCP 原名） | 见下「**背包道具**」；**勿**把 **`HEROINVENTORY`** 理解成「只查列表」——底层是 **UserGoods 全动作** |
| 任务列表 / Tasks | GETTASKLIST | **`taskType count`**（见下）；**args 空** 时 GameSkillAPI 默认 **`1 5`**（新手 5 条，与 bootstrap 一致） |
| 服务器时间 / Server time | SERVERTIME | (空) |
| **周期排行榜** / Time-window ranks | GETTOPBYTIME | 见下节「排行榜」 |
| **总防 / 总攻 / 总发展 / 联盟总榜** | GETDEFENDRANK / GETATTACKRANK / GETUSERRANK / GETALLYRANK | 见下节 |
| **每日之星 / 周榜 / 名人堂** | HALLOFFAME | 见下节 |
| **每日礼遇（乐透）/ Daily lottery board** | **EVERYDAYREWARD** | 常为 **`1`**（与客户端 **`/everydayreward 1`** 一致）；**见下「每日礼遇」** |
| **领取每日礼遇** | **GETDAILYGIFT** | **`tileID` 与索引列表**同一字符串内用**空格**分隔第二段为 **`i0,i1,...`**（逗号无空格拆段）；**见下** |

### 每日礼遇（乐透，`EVERYDAYREWARD` / `GETDAILYGIFT`）

与客户端 **`/everydayreward`**、**`/getdailygift`** 一致。此为「九格选 N」的**当日乐透盘面**，**不在此文档中列出**各内部类型编号对应的道具或数值（避免剧透礼包内容）；技能侧只需理解**次数**与**格子索引**。

**1）拉取当日盘面 — `EVERYDAYREWARD`**

- 请求示例：`{"cmd":"EVERYDAYREWARD","args":"1"}`（`args` 与常见客户端一致即可）。
- 成功返回：**`/svr everydayreward <payload>`**，**`payload`** 为一段文本，格式：

  **`可领取次数:格0,格1,格2,格3,格4,格5,格6,格7,格8`**

  即 **一个数字、冒号、再九个逗号分隔的整数**（与抓包如 `5:18,18,18,…` 同形）。

| 字段 | 含义 |
|------|------|
| **可领取次数** | 你在下一步里**必须选中的格子个数**（**1～5**；上限受**连续登录天数**约束，且不超过 **5**，至少为 **1**）。 |
| **九个整数** | 九个格位（逻辑下标 **0～8**）上各自的 **内部类型编号**，仅供服务端校验与发奖；**请勿**据编号推断具体奖励名称或数量。 |

**缓存**：同一**自然日**内再次请求 **`EVERYDAYREWARD`**，会拿到**服务端已为该账号缓存的同一盘面**（已生成则不会重新掷点）。

**2）按索引领取 — `GETDAILYGIFT`**

- 会话将 **`args` 按空格拆成两段**（见 `Game_e_Action.Params`）：第一段为 **城市 `tileID`**，第二段为 **逗号分隔的格子下标**（**无空格**）。
- 请求示例：`{"cmd":"GETDAILYGIFT","args":"598648 0,4,5,6,7"}`  
  - **`598648`**：领取发奖用的城市 **tileID**（须为本账号城市，常用 **当前城** / **`CurrentVillageID`**）。  
  - **`0,4,5,6,7`**：从九格中选中的 **下标**，须在 **0～8** 之间、**互不相同**，且**个数必须等于**上一步 **`everydayreward` 返回的「可领取次数」**（例：可领 **5** 次则必须恰好 **5** 个索引）。

成功：**`/svr getdailygift ok`**（末尾可有空格）。失败：**`/svr getdailygift err <code>`**（如当日已领过、参数不合法等，以服务器为准）。

**POST /game/command**：单条命令对应**单行** `data`，与多行空投响应不同，按单行解析即可。

### 空投（`AIRINFO` / `AIRDROPRES`）

与客户端 **`/airinfo`**、**`/airdropres <tileID>`** 一致；**bootstrap** 里已含 **`AIRINFO`** 一步（键名 **`airinfo`**）。

| 步骤 | 说明 |
|------|------|
| **查次数** | `{"cmd":"AIRINFO","args":""}` → **`/svr airinfo 已用,总数`**（两整数逗号分隔）。**剩余次数** = 总数 − 已用。 |
| **领取** | `{"cmd":"AIRDROPRES","args":"<tileID>"}`（**args 为城市 tileID**，多城时与 **`SETCURCITY`** / **`CurrentVillageID`** 对齐）。 |

**一次领取的服务器输出（两条 `WriteLine`，TCP 与 HTTP 一致）**：

1. **`/svr getResource {...}`** — 领取后该城资源快照（含 **`tileID`**、**`wood`/`clay`/`iron`/`food`**、**`lastCheck`** 等）。  
2. **`/svr airdropres ok`**

**GameSkillAPI**：`POST /game/command` 将上述两段**合并为一条 `data` 字符串**（中间为换行符），**正常**；HTTP JSON 的 **`ok`** 为 true 当且仅当整段结果不被判定为错误（与单行命令相同）。解析时请**按行**拆分，或使用本目录 **`cache.parse_svr_lines`** / **`airdrop_ops.py`**。

**本地缓存**：执行 **`python3 2037.py airdrop [tileID]`**（或 **`airdrop_ops.py airdrop`**）在成功时会把 **`getResource`** 合并进 **`session_cache.json`** 的 **`getresource_last`**、**`resource_by_tile[<tileID>]`**（若已有 bootstrap 缓存文件）。无 **`session_cache.json`** 时仅打印返回，不报错。

### 征收与账户（`COLLECTTODAYTIMES` / `COLLECTRES` / `GETACCOUNT`）

**`COLLECTTODAYTIMES`**：`args` = **城市 tileID**（**空** 时 GameSkillAPI 默认 **当前城**）。成功：**`/svr collecttodaytimes <整数>`**，表示该城**当日已累计的征收次数**（用于判断是否已征、以及后续是否扣金币等，**以服务端规则为准**）。

**`COLLECTRES`**（与 **`/collectres`** 一致）：

| `args` | 含义 |
|--------|------|
| **`<tileID>`** | 对该 **玩家城市** 征收产出；城内**当日首次**征收通常**不扣金币**，**再次**征收可能按 VIP/余额扣金币（**以游戏内为准**）。 |
| **`collect_all`**（大小写不敏感） | **一键**：对账号下各城所占领的**资源型贸易站**，按可领取时间批量结算（服务端循环，可能与多城 **`getResource`** 相关）。**不是**把 `tileID` 写成 `collect_all` 以外的变体。 |

成功时通常先出现 **`/svr getResource {...}`**（单城一条；**`collect_all`** 可能出现**多行** `getResource`，对应不同 **tileID**），再 **`/svr collectres ok`**。与空投类似，**`POST /game/command` 的 `data` 为多行字符串属正常**。本地若存在 **`session_cache.json`**，可用 **`cache.apply_getresource_from_command_to_session_cache`** 合并多行资源（**`getresource_last`** 为最后一行，**`resource_by_tile`** 逐城合并）。

**`GETACCOUNT`**：`args` **空** 即可（GameSkillAPI **`CommandHelper`** 会填 **userID**）。成功：**`/svr getaccount {...}`**，JSON 含 **`pie`**（系统赠送金币）、**`amount`**（充值金币）、**`vip`**、**`accumulateConsume`** 等。**向玩家展示「金币」时**：**`pie + amount`**（与客户端展示一致）。执行 **`python3 2037.py sync`**（或 **`cache.sync`**）时，会在 **USERINFO** 之后请求 **GETACCOUNT**，并写入 **`userinfo.json`** 的 **`account`** 字段，同时写入 **`goldCoinsTotal`** = **`pie` + `amount`**，便于脚本与 OpenClaw 直接读取。

### 建造 / 升级（与游戏 TCP 一致：只有两条命令）

游戏内升级**没有**单独的「升级」指令名；标准流程是：

1. **`GETBUILDCOST`** — 查消耗与时间。  
   - **多等级**：`args` = **`buildID:等级1,等级2,...`**，例 **`8:3,2`** 表示建筑 8 在等级 3 与 2 的造价列表。  
   - **单等级**：`args` 也可为 **`buildID 等级`**（空格），例 **`8 3`**。
2. **`ADDBUILDQUEUE`** — 入队；`args` = **单行 JSON**（与 **`/addbuildqueue {...}`** 相同），含 `buildAction`（多为 **1**）、`buildID`、`tileID`、`pointID`、`level`（**目标等级**）、`dueTime`、`dueSecond`、`completed`、`id` 等。成功返回常含城内资源 JSON。

**取消队列**：`CANCELBUILDQUEUE`，`args` = **`tileID pointID`**（两整数空格分隔）。

**说明**：若你用的 **HTTP 网关**（例如自建 GameSkillAPI）里出现 **`UPGRADE_OIL` / `UPGRADE_RESOURCE` / `UPGRADE_POINT`**，那是网关把参数展开成 **`ADDBUILDQUEUE`** 的简写，**不是**游戏客户端原生 TCP 命令；抓包对照时请以 **`GETBUILDCOST` + `ADDBUILDQUEUE`** 为准。若简写**解析失败**（缺参、城内无对应外城资源位建筑等），网关会返回明确错误，业务侧应改用 **`GETBUILDCOST` + `ADDBUILDQUEUE`**。

**脚本**（本目录 **`build_ops.py`**）：

```bash
# 查价（与 /getbuildcost 8:3,2 一致）
python3 skills/earth2037-game/build_ops.py getbuildcost "8:3,2"
python3 skills/earth2037-game/build_ops.py getbuildcost "8 3"

# 入队（整行 JSON，可从游戏日志复制）
python3 skills/earth2037-game/build_ops.py addbuildqueue '{"buildAction":1,"buildID":8,...}'

# 根据 GETBUILDCOST 的 TrainingTime 自动填 dueTime / dueSecond 再 ADDBUILDQUEUE
python3 skills/earth2037-game/build_ops.py compose --tile 273897 --point 27 --build 8 --level 3

python3 skills/earth2037-game/build_ops.py cancel-queue 273897 27
```

### 征兵 / 造兵

**推荐（桥接 + 脚本）**：`LISTRECRUITQUEUE` 列表；`RECRUITQUEUE` 入队，**只需** `troopId total [tileId]`，时间与 JSON 由 **GameSkillAPI** 内 **`CommandHelper.ResolveRecruitConscription`** 按兵营规则与 **`GetLastConscription`** 计算（单兵秒数优先从该城同兵种队列复用，否则按城内军事建筑等级估算）。

```bash
python3 skills/earth2037-game/recruit_ops.py list
python3 skills/earth2037-game/recruit_ops.py list 293135
python3 skills/earth2037-game/recruit_ops.py recruit 43 8
python3 skills/earth2037-game/recruit_ops.py recruit 43 8 293135
```

**原始客户端协议**（抓包）：`ADDCONSCRIPTIONQUEUE` 的 **`args` = JSON 数组** `[{...}]`，含 `cityID`、`troopID`、`total`、`unitTraining`、`nextUnit`、`dueTime`（.NET **`/Date(...)/`**）等。无桥接或需完全手写时用：

```bash
python3 skills/earth2037-game/recruit_ops.py raw-add '[{"cityID":293135,...}]'
python3 skills/earth2037-game/recruit_ops.py compose --tile 293135 --troop 43 --total 8 --unit-training 141
```

### 发展编排：查看地块、打野、聊天

#### 1) `ADDBUILDQUEUE` 字段

与客户端一致；`level` 为**升级后的目标等级**；`dueTime` 为 .NET `/Date(ms+时区)/` 格式。

#### 2) 查看地块 — 按 **FieldType** 分支

| 场景 | cmd | args |
|------|-----|------|
| **绿洲 / 野地**（QM 里 **FieldType=0**，`None`） | **GETNPCCITY** | `tileID`，如 `274699` |
| **可建城田或玩家城**（FieldType **1～7** 或已有用户） | **TILEINFO** | `tileID`，如 `273897` |

流程建议：**QM**（或缓存地图）得到某格的 `[tileID, FieldType…]` → 再选上表命令。`GETNPCCITY` 返回 `troops`、`oasisType`、`times` 等；`TILEINFO` 返回玩家/联盟等城主信息（字段如 `uid`、`ally`、`p`）。

#### 3) 打野（定义与流程）

**定义**：打野 = 在地图上寻找 **`FieldType = 0`**（绿洲/野地）的 **tile**，对这些格用 **`GETNPCCITY`**（`/getnpccity`）查看 **NPC 兵力**（`troops` 等），在**主城或部队附近**用 **QM** 分段搜索邻近地块，筛出可打的野怪格。

**战力与战损**：结合兵种攻防、数量评估「打不打得过」。游戏内攻守双方兵力消耗/战损比例，按 **兰开斯特平方律**（Lanchester square law）一类思路：兵力规模与**有效战力**常呈平方关系参与交换比估算（具体系数以游戏内结算为准）。出征前可用 **`GETCITYTROOPS`** / 兵种表对照野怪 **`GETNPCCITY`** 结果做粗算。

**收益**：**消灭野怪**后通常会**获得资源**（具体种类与数量以战报/服端为准）。

**出征命令**：目标格须为 **FieldType=0** 的野地；**`marchType=256`** 为打野出征。兵种串：`armId:数量_战损_俘虏_等级`，多兵种用 `|` 连接。

**编排步骤**：

1. **QM** 在附近矩形内列出地块，筛 **`FieldType=0`**；对候选 **`tileID` 逐个 `GETNPCCITY`** 看 **`troops`**。  
2. **`GETCITYTROOPS`** 配兵，按战力/兰开斯特思路估算战损与胜算。  
3. 发 **`ADDCOMBATQUEUE`**，或用脚本：
```bash
python3 skills/earth2037-game/march_ops.py attack-oasis --from 273897 --to 272293 --troops "43:35" --in-seconds 120
```

**JSON 字段要点**：

| 字段 | 含义 |
|------|------|
| `fromCityID` | 出发城 tileID |
| `toCityID` | 目标绿洲 tileID |
| `marchType` | **256**（打野） |
| `troops` | 兵种串：`armId:数量_战损_俘虏_等级`，多种用 `\|` 拼接。例：`43:35_0_0_0` = 兵种 43 数量 35，其余 0 |
| `resources` | 常 `"0\|0\|0\|0"` |
| `heroID` | 无统帅填 `0` |
| `spyIntoType` | `0` |
| `arrivalTime` | `"/Date(…+时区)/"`，需与服务端行军时间一致（机器人曾用「曼哈顿格距 × 秒」粗算，实际以客户端/服务端为准） |
| `completed` | `false` |
| `id` | `0` |
| `upkeep` | 粮耗；可按兵种表估算或先试填再由服端校验 |

成功示例：`/svr addcombatqueue ok <queueId>`。

**HTTP body 示例**（`args` 内为转义后的 JSON 字符串，按实战替换时间与兵力）见上节脚本或直接抓包游戏客户端。

#### 4) 聊天

- **`GETWMSGS`**：`args` = **从哪条消息 ID 开始拉**（如 **`0`** 拉最新一页），返回 `/svr getwmsgs [...]`。
- **`GETALLYCHAT`**：`args` = **游标**（如 **`0`**），返回联盟频道 JSON（含 `messages`、`nextCursor`、`hasMore`）。
- **`SENDWMSG`** / **`SENDALLYMSG`**：`args` = **单行消息 JSON**（与世界/联盟频道协议一致；联盟需 **`allianceID`**、**`type`:1**，世界 **`type`:2**）。

```bash
python3 skills/earth2037-game/chat_ops.py world-msgs 0
python3 skills/earth2037-game/chat_ops.py ally-chat 0
python3 skills/earth2037-game/chat_ops.py send-world "你好"
python3 skills/earth2037-game/chat_ops.py send-ally "联盟里吼一嗓" --alliance-id 43
```

发消息前建议先 **`2037.py sync`**，脚本会从 **`userinfo.json`** 读 `UserID` / `Username` / `AllianceID`（可用参数覆盖）。

### 排行榜 / Leaderboards（HTTP：`POST /game/command`）

`args` 为**空格分隔**参数（与 TCP `/gettopbytime …` 一致；HTTP 使用**大写 cmd**，无 `/` 前缀）。

**GETTOPBYTIME** — 按日/周/月的分类排行：

`args`: `搜索 页码 每页条数 排行类型 周期`

| 位置 | 含义 |
|------|------|
| 搜索 | `*` = 全服；否则按**用户名**筛选 |
| 页码 | 从 **1** 起 |
| 每页条数 | 如 `10` |
| 排行类型 | **1** 个人攻击 **2** 个人防御 **3** 个人发展（人口增长） **4** 联盟攻击 **5** 联盟防御 **6** 联盟发展 |
| 周期 | **1** 日 **2** 周 **3** 月 |

示例：`{"cmd":"GETTOPBYTIME","args":"* 1 10 3 3"}` → 个人发展、月榜、第 1 页、每页 10 条。

**总榜（无日/周/月维度）** — 搜索、页码、每页条数 同上：

| cmd | 含义 |
|-----|------|
| GETDEFENDRANK | 总防御排行 |
| GETATTACKRANK | 总攻击排行 |
| GETUSERRANK | 总发展排行 |
| GETALLYRANK | 联盟排行 |

示例：`{"cmd":"GETDEFENDRANK","args":"* 1 10"}`

**HALLOFFAME** — 每日之星 / 周榜 / 名人堂：

`args`: `类型 第二参数`（与 TCP `/halloffame` 一致；第二参数常为 `0`，以服务端为准）

| 第 1 参数 | 含义 |
|-----------|------|
| 1 | 每日 |
| 2 | 每周 |
| 3 | 名人堂 |

示例：`{"cmd":"HALLOFFAME","args":"1 0"}`

**成功时 `data` 文本**（节选）：`/svr gettopbytime {4|0}@[ { "RankID":1, "Username":"…", … } ]`

- 前缀 **`{4|0}`**：`|` 前数字为**当前玩家在本榜的名次**（示例为第 4 名）；联盟榜时字段以 `AllianceName` 等为主。
- 解析时从 `data` 字符串中取 JSON 数组；向用户说明名次、用户名、人口、攻防分等即可。

### 任务列表解析（`GETTASKLIST`）

与客户端 **`/gettasklist 1 5`** 一致：**`args` = `taskType count`**（两个整数，空格分隔）。经 **GameSkillAPI** 且 **`args` 为空** 时，桥接默认填 **`1 5`**（与 **`bootstrap`** 里 `gettasklist` 步一致）。

| 参数 | 含义 |
|------|------|
| **taskType** | 任务大类（`TaskType`）：**1** = 新手（Newbie），**2** = 每日（Everyday），**4** = 剧情（MainTask），**5** = 任务链（TaskChain） |
| **count** | 拉取条数上限（示例 **`1 5`** = 新手任务最多 5 条） |

成功返回 **`/svr gettasklist [...]`**，body 为 **JSON 数组**；每一项为 **`TaskItem`**，常见字段：

| 字段 | 说明 |
|------|------|
| **taskID** | 任务配置 ID |
| **title** | 标题文案（如「【外交】建立或加入一个联盟」） |
| **taskType** | 任务大类，枚举同上（**1** 新手 / **2** 日常 等） |
| **taskStatus** | 状态（`TaskStatus`）：**1** = 未接（NotDoIt），**2** = 已接/进行中（Accept），**3** = 已完成（Completed），**5** = 已结束/领奖（Finished） |
| **reqType** | 要求类型（`TaskReqType`），如 **1** = 普通，**14** = 仗义支援（Reinforcement），**15** = 侦查（Investigation）等；具体以服端配置为准 |
| **userID** | 部分日常/交互类任务会带关联玩家 ID；无则为 **0** |

**解析建议**：先 **`json.loads`** 去掉 `/svr gettasklist ` 前缀后得到数组；按 **`taskStatus`** 筛「可领/待完成」，按 **`title`** 展示；**bootstrap** 中键名 **`gettasklist`** 对应同结构数据。

### 背包道具（`HEROINVENTORY` / 桥接 **`USEBAGITEM`** 等）

游戏 TCP 命令名为 **`HEROINVENTORY`**，容易误解成「只和英雄界面有关」；**实质是背包里每条道具实例（UserGoods）的通用入口**：使用、装备、丢弃、分解、技能书学习等（见 `Action.HeroInventory`）。

**第一个参数永远是「背包记录 Id」**：即 **`USERGOODSLIST` / `usergoodslist`** 返回的数组里，**每一条的 `Id` 字段**（实例主键），**不是** 商品目录里的 **`GoodsId`**。向玩家说明时请称「背包里这条道具的 Id」。

**第二个参数 `drid`（动作码）**：

| drid | 含义 | 其余参数（空格分隔，与客户端一致） |
|------|------|--------------------------------------|
| **1** | **使用** | 可选 **`tileID`**（多类消耗品需要当前城/指定城）；部分客户端还会多传**附加整数**（如抓包 `… 466394 1000`），服务端按道具类型分支读取，**以实际道具逻辑为准**。 |
| **2** | **装备到英雄** | **`heroId` `weaponAction` `inventorySlot`**（共需 5 段：`实例Id 2 heroId …`） |
| **3** | **丢弃** | 无 |
| **4** | **分解**（武器等） | 无 |
| **5** | **技能书**（概率顶替等） | **`heroId` `currentSkillCount`** |

**推荐桥接（避免误用 `HEROINVENTORY` 字面义）**：在 **`POST /game/command`** 里优先使用 **`USEBAGITEM`**（同义 **`CONSUMEBAGITEM`**、**`USEUSERGOODS`**），`args` 只写 **使用** 所需参数，**不要**手写中间的 **`1`**：

- 例：抓包 **`/heroinventory 13002 1 466394 1000`**（使用实例 **13002**，城 **466394**，第三段客户端约定）  
  → 桥接：`{"cmd":"USEBAGITEM","args":"13002 466394 1000"}`，服务端展开为 **`13002 1 466394 1000`** 再调 **`HEROINVENTORY`**。

其它桥接：**`EQUIPBAGITEM`**、**`DROPBAGITEM`**、**`DISASSEMBLEBAGITEM`**、**`APPLYSKILLBOOK`** 见上表「桥接层别名」。

**成功时的输出**：除 **`/svr heroinventory ok`** 外，前面可能还有 **`/svr svr_gift_tip …`**（客户端飘字；**服端协议**，不是都给玩家直读）。**含义概要**：子类型 **`4`** 后为 **`goodsId,count`** 多段（`;` 分隔）；子类型 **`2`** 后为 **空投补给次数**（礼包未随到随机物时的系统补偿，**不是**物品 ID）；另有金币文本、`3` 立即完成、`9`/`10` 地图格等（见 `Action.cs`）。**OpenClaw / 终端**：本地脚本（`cache.humanize_command_output`）会把多行 **`/svr`** 转成中文说明，并用 **`session_cache.json` 的 `goodslist`** 把物品 ID 换成名称；调试原样输出可设 **`EARTH2037_RAW_SVR=1`**。**`POST /game/command` 的 `data` 仍为多行字符串**（自动化解析请用原始行）。

### 切换当前城（`SETCURCITY`）

多城时先将服务器「当前城」设为要操作的城市，后续无 tileId 的默认城才会指向该城（**`CurrentVillageID`**）。

- **HTTP**：`{"cmd":"SETCURCITY","args":"<tileID>"}`，成功返回 **`/svr setcurcity ok`**（与客户端 **`/setcurcity 8403`** 一致）。
- **本地缓存**：执行 **`python3 skills/earth2037-game/2037.py setcity <tileID>`**（需 token），内部 **SETCURCITY** 后自动 **sync**，更新 **`userinfo.json`** / **`citys.json`**。若你还依赖 **`session_cache.json`** 整包，可再运行 **`2037.py bootstrap`**。

### 更多命令 / More Commands

- **用户账号**：CURRENTUSER, USERINFOBYID, **GETACCOUNT**（金币：**`pie`+`amount`**，**sync** 写入 **userinfo.json**）, MODIFYPWD, MODIFYEMAIL, MODIFYSIGNATURE
- **城市 / 征收**：CITYITEMS, CITYBUILDQUEUE, **COLLECTTODAYTIMES**, **COLLECTRES**（或 **`collect_all`** 贸易站）, ADDBUILDQUEUE, GETBUILDCOST, CANCELBUILDQUEUE, MODIFYCITYNAME, SETCURCITY, CREATECITY, MOVECITY（**无** `UPGRADE_*` TCP 名；见「建造/升级」「征收与账户」）
- **军事**：ARMIES, GETCONSCRIPTIONQUEUE, COMBATQUEUE, GETCITYTROOPS, GETNPCCITY, MEDICALTROOPS, BUYSOLDIERS
- **联盟**：GETALLYMEMBERS, CREATEALLY, INVITEUSER, SEARCHALLY, DROPALLY
- **消息战报**：GETMESSAGE, GETREPORT, SENDMSG, DELETEMESSAGES, DELETEREPORTS
- **地图**：TILEINFOS, MAP, MAP2, FAVPLACES, FAVPLACE, DELFAV
- **英雄物品**：USERHERO, RECRUITHERO, HEROWEAPONS, USERGOODSLIST, **HEROINVENTORY**（易混名；优先桥接 **USEBAGITEM** 等，见「背包道具」）, CDKEY, VIPGIFT
- **任务活动**：GETTASK, TASKGETREWARDS, **EVERYDAYREWARD**（每日乐透盘面）, **GETDAILYGIFT**（按索引领取，见上表「每日礼遇」）, ACTIVITY
- **排行榜**：GETTOPBYTIME, GETDEFENDRANK, GETATTACKRANK, GETUSERRANK, GETALLYRANK, HALLOFFAME（见上表）

### Response

- Success: `{"ok":true,"data":"/svr cmd ok {...}"}`
- Error: `{"ok":false,"err":"/svr cmd err ..."}`

## 地图参考 / Map Reference

**给 AI 的单页地图说明**（环面、单次 QM、QM 返回格式、FieldType、文字线框图）：见本目录 **`MAP_FOR_AI.md`**。对玩家以 **(x,y)** 为主，勿把 tileID 当主展示。

**文字线框图**（不额外请求接口）：

```bash
python3 skills/earth2037-game/maps_util.py --ascii -99 224 2
python3 skills/earth2037-game/maps_util.py --ascii-tile 142078 3
python3 skills/earth2037-game/maps_util.py qm
python3 skills/earth2037-game/maps_util.py qm -a "1 -99,224,9,9"
```

### tileID / VillageID / CityID 与坐标

**tileID、VillageID、CityID 三者相同**，均为地图格子的唯一 ID。客户端需将其转换为 (x,y) 坐标以便显示。服务端 `Maps` 类逻辑：

- **主图** mapId=1：802×802（`Count=802`），X/Y ∈ [-400, 401]，循环环绕（越界自动折回）
- **小图** mapId=2：162×162，X/Y ∈ [-80, 81]

**转换公式**（与游戏服主图约定一致，`Count=802`）：
- `GetX(id)`：`val = (id % Count) - 401`，主图 **`Count=802`**，再 `V()`
- `GetY(id)`：`val = 402 - ceil((id - GetX(id)) / Count)`，再 `V()`
- `GetID(x,y)`：`(402 - V(y)) * Count + V(x) - 401`
- `V(x)`：x>401→x-802；x<-400→x+802；否则不变

**Python 脚本** `maps_util.py`：提供 `get_x(id)`、`get_y(id)`、`get_xy(id)`、`get_id(x,y)`、`format_xy(id)`。

```bash
# tileID → (x,y)
python3 skills/earth2037-game/maps_util.py 12345

# (x,y) → tileID
python3 skills/earth2037-game/maps_util.py --id -99 224

# 小图加 --mini
python3 skills/earth2037-game/maps_util.py 1234 --mini
```

**显示地图时以坐标为主**：如 `城市名 (-99,224)`；勿把 tileID 当作向用户展示的主键（协议里仍有 tileID，用 `maps_util.py` 换算即可）。

### 其他

- **QM**：`args = "mapId x,y,w,h;…"`。**不传范围**（`args` 空）时，HTTP 由服务端填 **当前城市** 为中心 **7×7**（`CurrentVillageID`，否则主城）。
- **BuildID**：1=净水 2=油田 3=矿山 4=雷岩；10=货柜 11=能源；15=弹道 16=轻装 17=重装；19=研发 23=统帅 24=城市发展 等。

## Workflow

1. **No token**: Call `/auth/register` or `/auth/token` to obtain.
2. **Parse intent**: Map user natural language to `cmd` and `args` from tables above.
3. **Execute**: `POST {apiBase}/game/command` with Bearer token.
4. **Present**: Parse `/svr` response in `data`, summarize for user.

## Examples

**User**: "帮我看看我有哪些城市" / "Show my cities"
→ `{"cmd":"CITYLIST","args":""}`

**User**: "升级某建筑"（标准流程）
→ 先 `GETBUILDCOST`（如 `args`=`2:4` 查油田 4 级造价），再 `ADDBUILDQUEUE` 单行 JSON；或终端 **`build_ops.py compose --tile … --point … --build … --level …`**

**User**: "查一下主城周围" / "Query around capital"
→ `{"cmd":"QM","args":""}`（当前城 7×7）

**User**: "这块绿洲有什么兵"（已知 tile 为野地）
→ `{"cmd":"GETNPCCITY","args":"274699"}`
