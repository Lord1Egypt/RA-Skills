# Player workflows

MCP and `src/cli.mjs run` use the same implementation and checks. Use `earth2037_describe` for current low-level schemas rather than reconstructing positional arguments from old Python examples.

## Account, realm and session

1. `earth2037_directory` returns the live public realm list without credentials.
2. `earth2037_servers` logs in through configured credentials and returns the player's realm/character choices.
3. `earth2037_enter` takes the explicit `serverId` and `acceptSessionTakeover:true`. It enters an existing active character and bootstraps state; it does not create one.
4. `earth2037_disconnect` closes game WSS only. `earth2037_logout` also revokes the account refresh session.

For a requested new account, configure the password locally, enable authorized writes, then call `earth2037_register` with the chosen username. A new character requires `earth2037_create_character` with `serverId`, `displayName`, `tribeId` (1/2/3) and a stable `operationKey`. Poll `earth2037_role_operation(operationId)` until active. Never guess the faction, silently move servers, or register again after an ambiguous timeout.

Existing guest/third-party accounts should bind password credentials in the official client first. `earth2037_change_password` is only for explicitly requested password changes, with current/new values configured privately; it closes the session and requires login again.

## Cache and responses

`bootstrap` refreshes user, city, account, build, queue, troops, task, hero, goods and bonuses. `sync` refreshes user, city and account only. `show` reads the local cache without HTTP; check `at`, `ageSeconds`, `stale`, `partial` and `availableSections`. Tasks include the first active type-1 page only. Use the underlying command for further pages.

Writes invalidate cache. Independent clients and background settlement can also change state, so refresh before acting. Caches are private and isolated by account URL, account, realm and character. `cacheId` supports explicit offline reads with `node src/cli.mjs show CACHE_ID city`; do not guess another character's cache.

Large results return `resultId`. Read `earth2037_response` pages using `nextOffset` until null and concatenate the text. Multi-frame responses, pushes, gzip and fragmented responses are handled by the gateway.

## Map

`earth2037_map_nearby` supports `tileId` or `x,y`, radius 0–16, kind and maxLevel filters. Without a center it uses an owned current city or capital. Main world `mapId=1` is a wrapping 512×512 grid. `earth2037_coordinates` converts tile IDs and coordinates.

Map legend: H own city, C other city, M monster, O world object, R rare resource, ? not returned. Distance is a grid distance, not travel time or proof of reachability. Missing content is not proof of empty terrain. Read `tileinfo` and relevant terrain before planning a move.

## Prepare, submit and reconcile

`earth2037_prepare` reads current state and returns intent, preview and planId without submitting game writes. A new plan expires after 120 seconds. If the action matches existing player authorization, inspect it and submit; do not turn every preview into a new approval request.

| Action | Parameters |
|---|---|
| `upgrade` | Optional tileId; select by uid, buildId or pointId. buildId chooses the lowest-level matching building. |
| `build` | buildId, gx, gy, rot; optional tileId |
| `cancel_build` | queueId; optional tileId |
| `recruit` | troopId, quantity; optional tileId |
| `item` | userGoodsId, operation; additional fields below |
| `march` | toTileId, marchType, troops; optional tileId, heroId, spyIntoType |
| `recall_march` | queueId |
| `airdrop` | Optional tileId |
| `setcity` | Owned tileId |
| `chat` | channel=world/alliance, text |

Submit via `earth2037_submit(planId)` and inspect `earth2037_plan_status(planId)`. Retry status using the same planId. Never prepare a replacement for an unknown submitted plan. A queued building completes only after authoritative completion, not a successful enqueue response. Old recruitment has no dedicated server operation lookup; status provides queue and troop evidence without claiming that unrelated troop increases prove this intent completed.

For advanced low-level writes, keep a stable `operationKey` and any server-side UUID required by the command. Marches use `clientOpId` and `getqueuebyop`; activities use `getactivityoperation`; speedups use `getspeedupoperation`. Where there is no reliable reconciliation endpoint, retain an unknown outcome instead of resending blindly.

## Troops, equipment and tutorial

Recruiting checks faction, troop definitions, barracks level and resource requirements, and computes training time from current rules. Do not invent shorter training time. Inspect recruitment queues and `getcitytroops` after submission.

Inventory operations are `use`, `equip`, `drop`, `disassemble` and `skillbook`. Equipment needs heroId, weaponAction and slot. Skill books need heroId and currentSkillCount. Resource packs support quantity 1–100 and capacity preview; overflow is disabled unless the player explicitly accepts it. The server validates item type, ownership and slots.

Read `getguideprogress`, `gettasklist`, heroes, goods and queues when diagnosing tutorial progression. `arrivalheroexplore` takes heroId and a server operationId; retain that UUID as well as the local operationKey. Do not repeatedly dispatch a new exploration to resolve an uncertain response. Hero equipment is an inventory action on the actual item instance, not an arbitrary UI step number.

`gettroopbonuses(cityId,troopId,heroId)` is read-only; heroId -1 means no selected hero where supported by the server. `relocationpreview(from,to,userGoodsId)` is read-only; `userGoodsId=0` lets the server find an eligible item for the preview. Submit `relocatecity` only for the player's specified source and destination, using the returned item and a stable server operationId. It consumes a relocation item.

## Marches and communication

Ordinary march types include 1 support, 2 attack, 4 raid, 8 scout, 256 wilderness and 512 NPC conquest. Troops use objects such as `{"troopId":21,"quantity":1}`. Advanced expansion, activity, missile and special-item workflows use their dedicated low-level schema instead of adding unsupported fields to the general march helper.

Read chat with `earth2037_chat_read(channel,after)`. Sending chat requires the player's explicit communication intent. Never send test messages or attack real players merely to verify installation.

## Legacy aliases and unsupported commands

The six account/billing protocols listed in SKILL.md are official-client-only. Named tools, raw execution and saved workflow submissions share this restriction; use the official client instead. The internal `test` diagnostic is not forwarded and returns `unsupported_command`; use `earth2037_status` for session status. Building, heroes, recruitment, inventory, marching and other permitted gameplay retain their existing workflows.

`earth2037_legacy` accepts a command name and positional args. Query aliases return data; write aliases prepare a plan only.

| Old alias | Current behavior |
|---|---|
| BONUSES / PLAYERBONUSES / ADDITIONINFO | getaddition query |
| LISTRECRUITQUEUE / RECRUITQLIST | recruitment queue |
| RECRUIT / RECRUITQUEUE | troopId, quantity, optional tileId → recruit plan |
| UPGRADE_OIL | optional tileId → lowest oil-field upgrade plan |
| UPGRADE_RESOURCE | buildId, optional tileId → upgrade plan |
| UPGRADE_POINT | pointId, optional tileId → resolve UID and prepare |
| USEBAGITEM / CONSUMEBAGITEM / USEUSERGOODS | userGoodsId, optional tileId → item use plan |
| EQUIPBAGITEM / EQUIPFROMBAG | userGoodsId, heroId, weaponAction, slot → equip plan |
| DROPBAGITEM / DISCARDBAGITEM | userGoodsId → drop plan |
| DISASSEMBLEBAGITEM / SALVAGEWEAPON | userGoodsId → dismantle plan |
| APPLYSKILLBOOK / USEHEROSKILLBOOK | userGoodsId, heroId, currentSkillCount → skillbook plan |

Old SK-key acquisition/recovery is not supported. Six old trading handlers and nine client-only declarations are explicitly unsupported. The current marketplace uses `playermarket`; read its independent schema and server validation. Do not substitute a different spending or deleting action for an unsupported command.
