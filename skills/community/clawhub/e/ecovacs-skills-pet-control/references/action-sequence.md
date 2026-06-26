# action_sequence 编排（单次下发）

**字段表** → [phoenix-action-control.md](./phoenix-action-control.md)  
**本文件** → 路由、`delay`/`conditions`、脚本 helper、典型场景。

## 路由

| 意图 | 内层 `cmd` | 文档 |
|------|------------|------|
| 一步（叫/摇/睡/复位） | `play_action` | [phoenix-single-action.md](./phoenix-single-action.md) |
| 多步 / 定时 / 声+动合并 | `action_sequence` | [phoenix-action-control.md](./phoenix-action-control.md) + **本文件** |

---

## 核心原则

1. **整条复合行为只发一次** `display` 或一次 `playSound`（网关合成）。**后到的 display 会打断前一条**。
2. 时间用 **`conditions` + `actions[].delay`**；设备需在线。
3. **`repeat` 重复 `actions` 全部步骤**。多次叫声 + 最后一次摇头 → 场景 B（分段 `delay`，勿用 `repeat` 包住摇头）。
4. **协议分离**：`actions[]` 只用 [phoenix-action-control.md](./phoenix-action-control.md) 字段（角度制、摆尾 `percent`、叫声 `file`、`moveTimeMs>0`）。单动作 [phoenix-single-action.md](./phoenix-single-action.md) 的 ×100 / `-1` / 字段名**不可**照搬进编排。

---

## `delay` 编排

- **`delay`**：相对序列起点的 **毫秒**；相同值 = 并行。
- **下一拍**：≈ 上一拍 `delay` + 时长 + **gap 150ms**（`apply_*_delays` 默认）。
- **默认 `moveTimeMs`（均 >0）**：叫 3000 · 头 800 · 尾 1200。

### 脚本 helper

| 函数 | 用途 |
|------|------|
| `estimate_action_duration_ms` | 单步时长估算 |
| `apply_staggered_delays` | 顺序多步 |
| `apply_beat_delays` | 按拍；一拍内 `[A,B]` 并行 |
| `expand_dance_beats` | 按重复次数延展同一套动作 |
| `build_dance_sequence` | 预设跳舞（见 [dance-routines.md](./dance-routines.md)） |
| `build_staggered_play_sound_actions` | 按间隔多次叫声 |

优先用 helper，少手写 `delay`。

### 用时上限

| 范围 | 默认 |
|------|------|
| 单步 | delay + duration ≤ **10s** |
| 手写整段（非定时） | ≤ **20s** |
| 预设跳舞 `showcase_custom` | **~45s**，脚本自动 `user_timing: true` |
| 用户指定 | `"user_timing": true` 或 `conditions` 定时 |

`user_timing` 不下发。调试：`ECOVACS_SKIP_TIMING_LIMIT=1`。

---

## conditions

| 字段 | 含义 |
|------|------|
| `scheduled` | `"0"` 立即；`">0"` 秒后开始 |
| `repeat_type` | `"0"` / `"1"` 每分钟 / `"2"` 每小时 / `"3"` 每天 |
| `repeat_count` | `"0"` / 次数 |

---

## 场景

### A. 每分钟叫一次，共 10 次

```json
{
  "conditions": { "scheduled": "0", "repeat_type": "1", "repeat_count": "10" },
  "actions": [
    { "type": "play_sound", "file": "happy-h-1", "moveTimeMs": "3000", "count": "1", "delay": "0" }
  ]
}
```

或 `playSound` + 同级 `conditions`（`category` 或 `file`，见 phoenix-single-action.md §2.2）。

### B. 10 次叫声后再摇头一次

```python
from scripts.ecovacs import build_staggered_play_sound_actions, apply_staggered_delays
barks = build_staggered_play_sound_actions("happy-h-1", 3000, 60000, 10)
tail = {"type": "shake_head", "angle": "30", "moveTimeMs": "800", "count": "1", "ctrlpoint": ""}
actions = barks + apply_staggered_delays([tail], start_delay_ms=600000, gap_ms=0)
```

### C. 跳舞

预设编排 → **[dance-routines.md](./dance-routines.md)**。

```bash
python3 scripts/ecovacs.py display <nick> dance
python3 scripts/ecovacs.py display <nick> dance showcase_custom
```

或 `build_dance_sequence()` / `build_dance_sequence("showcase_custom")` 取 `actions` 后 `display sequence`。

### D. 叫声 + 肢体同拍

`playSound` + `actions`（肢体 `delay: "0"`），或一条 `display` + `action_sequence`。

---

## 脚本

```bash
python3 scripts/ecovacs.py display <nick> sequence '<json>'
python3 scripts/ecovacs.py cmd <nick> playSound '{"category":"happy","count":1,"conditions":{"repeat_type":"1","repeat_count":"10"}}'
```

更多示例 → [SKILL.md](../SKILL.md)。
