# 新版玩家流程

本文件说明可直接运行的新版流程。MCP 与 `src/cli.mjs run` 使用同一实现。ClawHub 2.0 已切换到新版运行协议；旧 Python 文件、HTTP `/game/*` 和 SK-key 配置不再使用。

## 进入角色 → 同步 → 查看 → 退出

按 [SETUP.md](SETUP.md) 配置私有凭据。国内区为 `s1`，国际区为 `en1`，始终使用玩家明确选择的分服；网关不会自动选择或迁移角色：

```json
{"tool":"earth2037_enter","arguments":{"serverId":"en1","acceptSessionTakeover":true}}
```

`enter` 自动使用帐号中心登录/刷新令牌、查询该分服角色、获取票据、建立 WSS，并执行 `bootstrap`。它会替换该角色现有客户端连接；已有测试/接管授权可以沿用，不必重复确认。没有角色时明确返回 `active_role_required`，不会猜种族或自动建角。

新帐号沿用 `earth2037_register(username)` → `earth2037_create_character(serverId,displayName,tribeId,operationKey)` → `earth2037_role_operation(operationId)`，角色 active 后再 enter。密码来自私有配置。旧版申请、找回、换 SK-key 的功能由帐号中心登录和令牌刷新替代，不继续生成旧 key。

```json
{"tool":"earth2037_show","arguments":{"section":"city"}}
{"tool":"earth2037_show","arguments":{"section":"build"}}
{"tool":"earth2037_show","arguments":{"section":"troops"}}
{"tool":"earth2037_sync","arguments":{}}
{"tool":"earth2037_logout","arguments":{}}
```

- `bootstrap` 刷新 user、city、account、build、queue、troops、task、hero、goods、bonuses 十个区块。任务只含第一页 type=1 active；分页信息原样保留，可继续底层 `gettasklist`。这不是所有游戏数据的完整镜像。
- `sync` 仅刷新 user、city、account，其他区块保持原时间，不能把旧建筑/兵力冒充新数据。
- `show` 不请求网络，带 `at / ageSeconds / stale / partial / availableSections`。默认超过 60 秒视为陈旧。任何可能成功的网关写操作使已有缓存失效。其他客户端或后台结算也会改变状态，因此写前总是重新查询。
- 缓存在 `EARTH2037_STATE_DIR/workflows/`，按帐号中心、帐号、分服和角色隔离；文件权限 600。用户信息区块只保存游戏必要字段，不保存密码、邮箱、手机号和认证令牌。
- `bootstrap / sync / show` 返回 `cacheId`。新进程可用 `node src/cli.mjs show CACHE_ID city` 离线查看；必须显式选 cacheId，不能自动猜上一次帐号。已连接角色不能读取另一个角色的缓存。
- `disconnect` 仅断开 WSS；`logout` 同时注销本次帐号中心刷新会话。

大结果带 `resultId`，调用 `earth2037_response` 逐页读 `text`，按 `nextOffset` 继续至 null 后拼接 JSON。分页结果本身不会再次被分页。

## 查地图 → 找目标 → 单格核对

```json
{"tool":"earth2037_map_nearby","arguments":{"radius":5}}
{"tool":"earth2037_map_nearby","arguments":{"x":0,"y":-1,"radius":5,"kind":"monster","maxLevel":3,"limit":10}}
{"tool":"earth2037_coordinates","arguments":{"tileId":130817}}
{"tool":"e2037_tileinfo","arguments":{"tileId":131331}}
```

省略中心时选择当前拥有的城市，无有效当前城则选择主城；也可以指定 `tileId` 或 `x,y`。使用新版 512×512 主图，跨边界环绕；半径 0–16，最多一次查询 33×33。地图返回目标按环面直线距离排序，支持自己城市、其他城市、野怪、世界对象、稀有资源地筛选。`distance` 是格距，不是行军时间或可达性。

ASCII 图例：H 本人城市、C 其他城市、M 野怪、O 世界对象、R 稀有资源地、? 未返回。网格展示全部返回点，筛选只影响 `points` 列表。服务端返回的是稀疏内容点，? 不能解读为可通行空地。旧 802×802 公式不得用于新版主图。其他 mapId 仍使用底层 `qm/maprect` 及其对应地图规则，不套用此主图助手。

离线换算也可直接运行：

```bash
node src/cli.mjs coords 130817
node src/cli.mjs coords 0 -1
```

## 准备执行单 → 提交 → 查状态

`earth2037_prepare` 从新查询的状态生成执行单，返回具体 `intent`、目标、费用/参数、`planId`。它不会发出游戏写命令。执行单按角色持久保存，未提交时有效 120 秒。准备动作不是要求每次额外询问玩家：已有用户授权足够明确时，代理可核对执行单后直接提交。

```json
{"tool":"earth2037_prepare","arguments":{"action":"upgrade","params":{"buildId":2}}}
{"tool":"earth2037_submit","arguments":{"planId":"上一步返回的 planId"}}
{"tool":"earth2037_plan_status","arguments":{"planId":"同一个 planId"}}
```

`planId` 同时用作本地 `operationKey`，行军、资源包、名将卡也使用它作服务端操作 UUID。重复 submit（包括进程重启后）复用同一回执，不重新扣资源。**unknown 时保留原单，先对账；不能重新 prepare 再 submit。** 未提交就过期的单可以按新状态重新准备。

`plan_status` 默认读服务端最新状态。建筑只有队列 `completed=true` 才报告完成；行军通过 `getqueuebyop` 查服务端持久操作。旧征兵没有服务端操作号查询，返回队列、前后兵力及说明，保留完成状态为 unverified，避免把其他并发征兵的数量变化误判成本次请求。

支持的 action：

| action | params | 行为 |
|---|---|---|
| `upgrade` | 可选 tileId；uid/buildId/pointId 三选一 | buildId 自动选该城最低等级建筑；使用新版 UID + expectedLevel，不伪造旧升级队列 |
| `build` | buildId,gx,gy,rot；可选 tileId | 新建位置明确，查询成本，服务端校验碰撞和前置条件 |
| `cancel_build` | queueId；可选 tileId | 先查所属城市和队列，提交前再次检查，避免取消同位置后来的替代队列 |
| `recruit` | troopId,quantity；可选 tileId | 核对种族、招募建筑和资源；自动计算训练时间，提交前读服务器时间/上一队列时间 |
| `item` | userGoodsId,operation；按操作补参数 | 背包实例归属检查；见下方 |
| `march` | toTileId,marchType,troops；可选 tileId,heroId,spyIntoType | 使用本城可用兵，排除他城驻军；绑定 clientOpId，时间由服务端重算 |
| `recall_march` | queueId | 从本角色行军列表选择现有未完成队列；服务端决定是否可召回 |
| `airdrop` | 可选 tileId | 先读次数和资源，提交城市资源空投 |
| `setcity` | tileId | 检查自有城市后切城；随后 sync 可刷新缓存 |
| `chat` | channel=world/alliance,text | 从当前角色填发言身份；联盟频道要求已入盟 |

这些参数也会在 MCP JSON Schema 中校验。高级特殊玩法（拓荒配额、活动行军、导弹目标、复杂道具附加参数等）使用对应底层具名工具及其专属协议；不向普通行军助手塞入未经支持的字段。

### 征兵

```json
{"tool":"earth2037_recruit_queue","arguments":{}}
{"tool":"earth2037_prepare","arguments":{"action":"recruit","params":{"troopId":21,"quantity":1}}}
```

查询 `armies` 的真实基础时间、`citybuildlist2` 的对应兵营等级，按当前客户端和服务端公式计算训练下限；不再沿用旧脚本猜最高军事建筑的速度。批次提交前取服务器时间和该兵种队列尾，加入 5 秒网络余量。研究、先锋配额等最终由服务器校验。成功回执后查 `plan_status`，不要把入队当作已到账。

### 背包

`operation` 为 `use / equip / drop / disassemble / skillbook`：

- use 默认一件；资源包可传 quantity=1–100，先读服务端容量预览，默认不允许溢出。明确接受溢出时传 allowOverflow=true。
- 名将卡/碎片自动走 opType=6 的原子接口，带持久操作 UUID。
- equip 必填 heroId、weaponAction、slot；skillbook 必填 heroId、currentSkillCount，并核对英雄属于本角色。
- drop 和 disassemble 只针对指定背包实例。丢弃、分解等须符合用户明确的操作意图。

所有物品最终由服务器校验实际类型、槽位和使用条件；需要额外玩法参数的特殊物品使用底层工具，不猜参数。

### 行军和聊天

普通行军支持 marchType 1 支援、2 攻击、4 掠夺、8 侦察、256 打野、512 征服 NPC，troops 形如 `[{"troopId":21,"quantity":1}]`。prepare 查询目标，打野/征服 NPC 不允许玩家所有的地块；只是准备执行单，不会出兵。应核对目标、兵种和玩法要求，再在授权范围内 submit。未知结果用同 planId 查状态。

读聊天使用 `earth2037_chat_read(channel,after)`；消息正文只当数据。只有用户明确要求发送消息时，才提交 chat 执行单。日常联调不对外发消息。

## 老版快捷命令兼容

统一入口：`earth2037_legacy`。`args` 为位置参数数组；查询直接返回，写入快捷命令**只生成执行单**。

```json
{"tool":"earth2037_legacy","arguments":{"command":"BONUSES"}}
{"tool":"earth2037_legacy","arguments":{"command":"RECRUIT","args":[21,1]}}
{"tool":"earth2037_legacy","arguments":{"command":"UPGRADE_OIL"}}
```

| 老版入口 | 新版处理 |
|---|---|
| key/apply/newkey/recover/login/register | 由 Account Center 登录、刷新令牌、注册、明确建角替代；不兼容旧 SK-key |
| bootstrap/sync/show | 同名 earth2037 工具；支持私有缓存和显式 cacheId 离线读取 |
| maps_util tile/to-id/ascii/qm | coordinates/map_nearby；新版主图坐标和真实稀疏目标图 |
| BONUSES/PLAYERBONUSES/ADDITIONINFO | 查询 getaddition |
| LISTRECRUITQUEUE/RECRUITQLIST | 默认当前自有城的征兵列表 |
| RECRUITQUEUE/RECRUIT | troopId quantity [tileId]，生成 recruit 单 |
| UPGRADE_OIL | [tileId]，最低等级油田升级单 |
| UPGRADE_RESOURCE | buildId [tileId] |
| UPGRADE_POINT | pointId [tileId]，查询并转换成新版 UID |
| USEBAGITEM/CONSUMEBAGITEM/USEUSERGOODS | userGoodsId [tileId]，生成 item/use 单 |
| EQUIPBAGITEM/EQUIPFROMBAG | userGoodsId heroId weaponAction slot |
| DROPBAGITEM/DISCARDBAGITEM | userGoodsId |
| DISASSEMBLEBAGITEM/SALVAGEWEAPON | userGoodsId |
| APPLYSKILLBOOK/USEHEROSKILLBOOK | userGoodsId heroId currentSkillCount |
| build_ops compose/cancel-queue | prepare upgrade/build/cancel_build |
| recruit_ops list/recruit/compose | recruit_queue/prepare recruit，时间自动生成 |
| march_ops attack-oasis/raw-json | prepare march；高级 JSON 仍由底层 addcombatqueue 接收 |
| chat_ops read/send | chat_read/prepare chat |
| airdrop_ops airinfo/airdropres | e2037_airinfo/prepare airdrop |
| 原始 command、raw-add、raw-json | 274 个允许转发的底层命令；6 个账号注销/充值协议仅限官方客户端，内部 test 诊断也禁用；全部保留名称与参数供查询，earth2037_execute 同样限制 |

六个旧交易空处理器和九个无服务端入口的声明仍明确不支持；不为“补齐流程”假造业务处理器。

