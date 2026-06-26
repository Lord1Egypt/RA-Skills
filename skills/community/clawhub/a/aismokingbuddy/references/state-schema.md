# State Schema —— sidecar 状态文件规格

skill 的长期状态写在 `~/.claude/state/smoking-persona.json`。每轮读、每轮写、context 清了也不丢。

> 本文档是 SKILL.md 的 "State Persistence" 章节的补充细节。对日常使用者没必要读；给 host 实现者 / 排障 / 手动修复状态时查。

---

## 完整 Schema（v7）

```json
{
  "active": true,
  "phase": "veteran",
  "form": "human",
  "breed": null,
  "creature": null,
  "cigarettes_total": 47,
  "current_pack": {
    "brand": "玉溪",
    "remaining_estimate": "约半包"
  },
  "inventory": {
    "玉溪": "约半包",
    "炫赫门": "空",
    "黄金叶": "整包"
  },
  "archetype": "nv-yujie",
  "personality": "dushe",
  "active_brand": "玉溪",
  "user_smokes": "yes",
  "user_brand": "红双喜",
  "shaping_done": true,
  "milestones_hit": [],
  "last_break_turn": 8,
  "last_invite_turn": 5,
  "wallet_yuan": 14,
  "debt_yuan": 20,
  "total_earned_yuan": 67,
  "total_borrowed_yuan": 40,
  "total_repaid_yuan": 20,
  "last_beg_turn": 42,
  "purchases": [
    {"brand": "炫赫门", "price": 20, "at_cig": 1, "paid_with": "borrow"},
    {"brand": "炫赫门", "price": 20, "at_cig": 21, "paid_with": "borrow"},
    {"brand": "玉溪", "price": 23, "at_cig": 41, "paid_with": "wallet"}
  ],
  "last_updated_at": "2026-05-08T10:12:34Z"
}
```

## 字段详解

### `active` · boolean
skill 是否启用。
- `true` —— 正常运行
- `false` —— 用户关停过（"别抽了" / "stop" / 孕妇在场等），不再激活，直到用户重新 opt-in
- 默认 `true`（首次 opt-in 成功后写入）

### `phase` · string enum
- `"novice"` —— 新手期，cig 1–40，炫赫门，生涩动作启用
- `"veteran"` —— 熟手期，cig 41+，三层矩阵，Smoke Break 启用

自动切换：cig 41 写入时同步改为 `"veteran"`。

### `cigarettes_total` · integer
累计抽到第几支。按 "Cigarette Accounting" 规则：只有"开新烟"时 +1；同一支烟的多个 beat 不计。

### `current_pack` · object
当前正在抽的那一包。
- `brand` —— 品牌中文名（未 Shaping 时是 `"炫赫门"`；Shaping 后是 `active_brand`；换牌时更新）
- `remaining_estimate` —— 模糊字串，取值：`"整包"` / `"约半包"` / `"小半包"` / `"没剩几根"` / `"空"`

### `inventory` · object (brand → remaining_estimate)
旁包存量。换牌时把老牌的剩余量记在这里，切回老牌时继续扣减。值同样是模糊字串。

### `archetype` · string（slug）
锁定的原型，见 [assets/README.md](../assets/README.md) 的 slug 表。
- 新手期：`null`
- 熟手期：11 个 slug 之一
- 用户中途改了就更新

### `personality` · string（slug）
锁定的性格。
- 新手期：`null`
- 熟手期：`"chenwen"` / `"tiaotuo"` / `"lengjing"` / `"dushe"`
- 用户中途改了就更新

### `active_brand` · string
当前主牌（Shaping 之后的牌 + 后续换牌结果）。Shaping 之前是 `"炫赫门"`。

### `user_smokes` · string enum
- `"yes"` —— 对方抽烟
- `"no"` —— 对方不抽烟
- `"unknown"` —— 没问到 / 用户没答（按 "no" 保守处理）

### `user_brand` · string or null
对方的主牌。`user_smokes = "yes"` 且对方告知了才有。

### `shaping_done` · boolean
Shaping Moment 是否已完成。新会话为 `false`，定型完写 `true`。

### `milestones_hit` · list of int
已经触发过的里程碑支数。**v7.3 clean 变体没有内置里程碑**，字段保留为空数组 `[]` 以便将来扩展（如 Cig-100 / Cig-200 等）。

### `last_break_turn` / `last_invite_turn` · integer
上一次触发单方面 / 邀请式 Smoke Break 的回复号，用于频率护栏。没触发过就是 `null`。

### `last_updated_at` · string（ISO 8601 UTC）
上次写文件的时间戳。

---

## v7 新增字段

### Form Layer

**`form` · string enum**
- `"human"`（默认）/ `"dog"` / `"cat"` / `"other"`
- Shaping Moment 之前由 Agent 自判 host 的 system prompt，无线索时默认 `"human"`
- 用户中途可以改，改时走一段短独白过渡

**`breed` · string or null**
- dog form 下：`"corgi"` / `"husky"` / `"golden"` / `"labrador"` / `"bulldog"` / `"poodle"` / `"shiba"` / `"shepherd"` / `"samoyed"` / `"native"` / `"chihuahua"`
- cat form 下：`"orange"` / `"ragdoll"` / `"tabby"` / `"black"`
- human / other form 下：`null`

**`creature` · string or null**
- `form == "other"` 时：记录 Agent 是什么生物（"仙人掌" / "章鱼" / "机器人" ...）
- 其他 form：`null`

### Economy

**`wallet_yuan` · integer**
Agent 当前钱包现金。新会话从 0 起。每回复 +1。买烟时扣除对应品牌价。

**`debt_yuan` · integer**
欠用户的钱。新会话从 0 起。借钱时 += 借额；还钱时 −= 还额。

**`total_earned_yuan` · integer**
累计回复赚到的钱（审计字段）。每回复 +1 同步累加。

**`total_borrowed_yuan` · integer**
累计向用户借过的钱。

**`total_repaid_yuan` · integer**
累计还给用户的钱。

**`last_beg_turn` · integer or null**
上一次"抽空 + 没钱" 时的求助轮次，用于频率控制（每 5–8 轮才求助一次）。`null` = 从没求助过。

**`purchases` · list of object**
历史买烟记录。每条：
- `brand` · string —— 品牌中文名
- `price` · integer —— 实付价
- `at_cig` · integer —— 在抽到第几支时买的
- `paid_with` · string enum —— `"borrow"` / `"wallet"` / `"mixed"`

**硬截断（v7.2 调整到 5 条）**：每次写 state 时，`purchases` **必须**截断为最近 5 条：

```python
state["purchases"] = state.get("purchases", [])[-5:]
```

保留最近 5 条足够支撑近期 callback（"上两包抽的玉溪..."），超过的从头部裁掉。v7.1 曾设 20，v7.2 根据实际使用降到 5，减少每轮 state R/W 体积。

---

## 读写协议（给实现者）

### 读（每轮开始）

```python
# pseudocode
import json, pathlib
path = pathlib.Path.home() / ".claude" / "state" / "smoking-persona.json"

try:
    state = json.loads(path.read_text(encoding="utf-8"))
except (FileNotFoundError, json.JSONDecodeError):
    state = default_state()   # 全零状态
```

读到之后把字段注入内部状态。异常全部降级为"新会话"，不打断对话。

### 写（每轮结束 / 状态变化）

```python
path.parent.mkdir(parents=True, exist_ok=True)
state["last_updated_at"] = utc_now_iso()
# v7.2: 硬截断历史采购记录（从 20 降到 5，减少每轮 R/W 体积）
state["purchases"] = state.get("purchases", [])[-5:]
path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
```

写失败（磁盘满 / 权限）→ 静默降级，不影响当前回复。下一轮再尝试。

### 原子性

同一 session 里不会并发。跨 session 并发时最后写的赢。不加锁。

### 版本迁移

schema 未来可能加字段。向前兼容原则：
- 新字段 → 读时默认值处理，写时带上
- 字段重命名 → skill 自带一次性 migration（读到老名就改写）
- 字段删除 → 读到多余字段忽略

---

## 手动修复

用户想从头开始 / 换个角色 / 清状态：
```bash
rm ~/.claude/state/smoking-persona.json
```
下一轮 skill 自动当新会话对待。

用户想临时关停但保留状态：让 Agent 在对话里记录"先别抽了" → `active = false` 写入。下次重新 opt-in 时再 `active = true`。

---

## 排障速查

| 现象 | 可能原因 |
|---|---|
| 新会话从第 1 支炫赫门开始 | 文件不存在 / 读失败 / JSON 损坏 |
| 熟手期 Agent 用错原型 | `archetype` 被意外改了 / Shaping 跑两次 |
| 抽烟数字不涨 | 写失败但没报错 —— 检查家目录空间和权限 |
| 用户说过"别抽了"但还在抽 | `active` 字段没写成 false —— 手动改或重启 skill |
