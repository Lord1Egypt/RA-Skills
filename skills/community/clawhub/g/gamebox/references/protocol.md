# gamebox 接口协议

## 通用约定

- 输入：JSON 字符串（CLI argv[1] 或 stdin）
- 输出：JSON stdout，`{"status":"ok"} | {"status":"error","code":N,"message":"..."}`
- Exit code：0=成功，1=参数错误，2=执行失败，3=状态错误
- 共享目录：`game_dir` 参数，默认 `.gamebox/`

---

## 1. manager.py — 游戏管理

### create — 创建游戏

```json
{"action":"create","game_type":"rpg|werewolf|story_relay|ctf|civilization","user":"alice","game_name":"可选","config":{}}
```

**config 按游戏类型：**
- rpg: `{"setting":"fantasy|scifi|modern|horror"}`
- werewolf: `{"roles":{"werewolf":2,"seer":1,"witch":1,...}}`
- story_relay: `{"genre":"奇幻","max_rounds":50,"words_per_turn":200}`
- ctf: `{"challenge_count":5,"difficulty":"mixed","time_limit":60}`
- civilization: `{"max_rounds":30}`

**返回：** `{meta: {id, type, name, creator, players, status, ...}}`

### join — 加入游戏

```json
{"action":"join","game_id":"xxx","user":"bob"}
```

### start — 启动游戏

```json
{"action":"start","game_id":"xxx","user":"alice"}
```

仅创建者可启动，需满足最低人数。

### end — 结束游戏

```json
{"action":"end","game_id":"xxx","user":"alice","reason":"可选"}
```

仅创建者可结束。

### leave — 退出游戏

```json
{"action":"leave","game_id":"xxx","user":"bob"}
```

仅 waiting 状态可退出。最后一人退出则删除游戏。

### list — 列出游戏

```json
{"action":"list"}
{"action":"list","status":"waiting"}
{"action":"list","type":"rpg"}
```

### info — 查看详情

```json
{"action":"info","game_id":"xxx"}
```

返回 meta + state。

---

## 2. turn.py — 回合控制

### next — 推进回合

```json
{"action":"next","game_id":"xxx","user":"alice"}
```

轮到下一位玩家。

### phase — 设置阶段

```json
{"action":"phase","game_id":"xxx","phase":"night"}
```

用于狼人杀等需要阶段切换的游戏。

### skip — 跳过当前回合

```json
{"action":"skip","game_id":"xxx","user":"alice"}
```

### status — 查看回合状态

```json
{"action":"status","game_id":"xxx"}
```

返回 turn, round, current_player, turn_order。

---

## 3. action.py — 统一动作接口

### do — 执行动作

```json
{"action":"do","game_id":"xxx","user":"alice","action_name":"move","params":{"target":"幽暗森林"}}
```

**action_name 按游戏类型：**

| 游戏 | 可用动作 | 参数 |
|------|---------|------|
| rpg | move, look, take, use, talk, fight, rest | target/item/npc/enemy/skill |
| werewolf | kill, check, save, poison, protect, vote, speak, reveal_role | target/content/role |
| story_relay | write, add_character, add_plot_thread, resolve_thread, revise, finish, read | content/name/description/index |
| ctf | submit, hint, challenges, scoreboard, finish, dynamic_challenge | challenge_id/flag/category |
| civilization | build, research, propose_trade, respond_trade, declare_war, make_peace, attack, status, world_status | building/tech/target/offer/request |

### history — 查看动作历史

```json
{"action":"history","game_id":"xxx"}
{"action":"history","game_id":"xxx","user":"alice","limit":20}
```

### undo — 撤销最近动作

```json
{"action":"undo","game_id":"xxx","user":"alice"}
```

仅创建者可撤销。

---

## 4. message.py — 消息系统

### send — 发送消息

```json
{"action":"send","game_id":"xxx","user":"alice","msg_type":"public","content":"大家好"}
{"action":"send","game_id":"xxx","user":"alice","msg_type":"private","to":"bob","content":"密谈"}
{"action":"send","game_id":"xxx","user":"alice","msg_type":"role","to":"werewolf","content":"今晚杀谁"}
```

msg_type: `public` | `private` | `role` | `system`

### receive — 接收消息

```json
{"action":"receive","game_id":"xxx","user":"bob"}
{"action":"receive","game_id":"xxx","user":"bob","channel":"public"}
{"action":"receive","game_id":"xxx","user":"bob","channel":"role","role":"werewolf"}
{"action":"receive","game_id":"xxx","user":"bob","since":"2026-04-13T22:00:00Z","limit":50}
```

channel: `public` | `private` | `role` | `system` | `all`

### channels — 列出可用频道

```json
{"action":"channels","game_id":"xxx","user":"bob"}
```

---

## 5. 游戏状态结构

### RPG state

```json
{
  "game_type": "rpg",
  "setting": "fantasy",
  "world_name": "艾尔德兰大陆",
  "locations": ["新手村", "幽暗森林", ...],
  "players": {
    "alice": {"hp": 100, "mp": 50, "location": "新手村", "inventory": [], "level": 1, ...}
  },
  "world": {"time": 1, "weather": "晴朗", "npcs": {}, ...},
  "phase": "exploration"
}
```

### 狼人杀 state

```json
{
  "game_type": "werewolf",
  "phase": "night",
  "round": 1,
  "player_roles": {"alice": "werewolf", "bob": "seer", ...},
  "player_alive": {"alice": true, "bob": true, ...},
  "role_revealed": {"alice": false, ...},
  "night_actions": {},
  "vote_record": {},
  "witch": {"antidote": true, "poison": true},
  "winner": null
}
```

### 小说接龙 state

```json
{
  "game_type": "story_relay",
  "genre": "奇幻",
  "write_order": ["alice", "bob", "charlie"],
  "current_writer_idx": 0,
  "segments": [{"writer": "alice", "content": "...", "word_count": 150, "round": 1}],
  "total_words": 150,
  "round": 1,
  "phase": "writing",
  "characters": {},
  "finished": false
}
```

### CTF state

```json
{
  "game_type": "ctf",
  "phase": "playing",
  "challenges": [{"id": 1, "category": "crypto", "title": "凯撒密码", "flag": "FLAG{...}", ...}],
  "scores": {"alice": {"score": 300, "solved": [1, 2], "attempts": 5}}
}
```

### 文明模拟 state

```json
{
  "game_type": "civilization",
  "phase": "play",
  "round": 1,
  "civs": {
    "alice": {"population": 3, "resources": {"food": 50, "gold": 50, ...}, "buildings": [], "techs": [], ...}
  },
  "diplomacy": {},
  "trade_deals": [],
  "events_log": []
}
```
