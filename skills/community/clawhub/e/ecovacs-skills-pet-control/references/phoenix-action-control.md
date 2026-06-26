# Phoenix 编排（`action_sequence`）

**适用**：多步表演、声+动合并、设备端定时 —— `display` → **`cmd=action_sequence`**，或 `playSound` 带 `actions`/`conditions` 时由网关合成。

单步动作 → [phoenix-single-action.md](./phoenix-single-action.md)（`play_action`）。  
**编排怎么排时间、定时场景、脚本 helper** → [action-sequence.md](./action-sequence.md)（本文件只写字段）。

> **勿混用协议**：本文件字段仅用于 `action_sequence` / `playSound.actions[]` / 编舞。  
> 不要把 `play_action` 的载荷（头部 `angle`×100、摆尾 `angle`、叫声 `angle`=文件名、`moveTimeMs=-1`）原样塞进 `actions[]`。

---

## 序列结构

```json
{
  "variables": {},
  "conditions": {
    "scheduled": "0",
    "repeat_type": "0",
    "repeat_count": "0"
  },
  "actions": []
}
```

| 块 | 说明 |
|----|------|
| `variables` | 通常 `{}` |
| `conditions` | 见 [action-sequence.md §conditions](./action-sequence.md#conditions) |
| `actions` | 基础动作数组；每项含 **`delay`（ms）** |

---

## `actions[]` 字段

### 头部 `nod_head` / `shake_head` / `cock_head`

| 字段 | 说明 |
|------|------|
| `angle` | **角度制**（如 `"15"`、`"-14"`），非 ×100 |
| `moveTimeMs` | **>0**（与 `moveSpeed` 二选一） |
| `moveSpeed` | 20–200（`moveTimeMs=0` 且已设 `delay` 时可用） |
| `count` | **>0**；编排建议 `"1"` |
| `delay` | ≥0，相对序列起点 **毫秒** |
| `ctrlpoint` | 编排中留 `""` |

**角度范围**：点头 -14~+22，摇头 -60~+60，扭头 -20~+20。

### 摆尾 `wag_tail`

| 字段 | 说明 |
|------|------|
| `percent` | 0–100 |
| `moveTimeMs` | **>0** |
| `delay` | ms |

### 叫声 `play_sound`

| 字段 | 说明 |
|------|------|
| `file` | 音效文件名 |
| `moveTimeMs` | **>0** |
| `count` | 播放次数 |
| `delay` | ms |

文件名规则 → [phoenix-single-action.md §2.2](./phoenix-single-action.md)。

### 眼睛 `eye_control`

| 字段 | 说明 |
|------|------|
| `eyetype` | `1` 左 / `2` 右 / `3` 双眼 |
| `narrow` | `1` 眯眼 / `0` 睁眼 |
| `percent` | 1–100 |
| `moveTimeMs` | **>0** |
| `count` | 眨眼次数 |
| `delay` | ms |

编舞中作节奏补充 → [dance-routines.md](./dance-routines.md)。

---

## 与单动作字段对照（禁止混写）

| 动作 | 单动作 `play_action` | 本文件 `action_sequence` | 范围 / 备注 |
|------|----------------------|----------------------------|-------------|
| 点头 | `angle` ×100 | `angle` 角度制 | **−14 ~ +22** |
| 摇头 | `angle` ×100 | `angle` 角度制 | **−60 ~ +60** |
| 扭头 | `angle` ×100 | `angle` 角度制 | **−20 ~ +20** |
| 摆尾 | `angle` = 速度×100 | **`percent`** 0–100 | 编排 **`moveTimeMs>0`** |
| 叫声 | `angle` = 文件名 | **`file`** | 见 phoenix-single-action §2.2 |
| 时间 | 无 `delay`；`moveTimeMs` 可 `-1` | 每项 **`delay`**；`moveTimeMs>0` | 默认：头 800 · 尾 1200 · 叫 3000 ms |

**反例（会导致动作异常或不执行）**：

```json
{"type": "shake_head", "angle": "3000", "moveTimeMs": "-1", "count": "3", "delay": "0"}
```

应为（角度制、正时长、范围内）：

```json
{"type": "shake_head", "angle": "30", "moveTimeMs": "800", "count": "3", "delay": "0", "ctrlpoint": ""}
```

脚本示例见 [action-sequence.md §脚本](./action-sequence.md#脚本)。
