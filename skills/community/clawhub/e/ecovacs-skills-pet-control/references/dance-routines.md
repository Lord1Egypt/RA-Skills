# 预设跳舞编排

编舞：**`scripts/dance_choreography.py`** → 唯一套路 **`showcase_custom`（定制秀舞）**  
下发：`python3 scripts/ecovacs.py display <nick> dance` 或 `dance showcase_custom`

`display … dance` **不带 routine** 时即下发此舞。`length`（短/中/长）对固定脚本**无效**，可省略。

## 定制秀舞结构（约 45s）

步骤间隔约 **50ms**；持续摆尾 **3s**（开场/第一场/收场）。

| 段落 | 动作 |
|------|------|
| **开场** | 同拍：向下点头×3 + **连叫×3** + 尾 **快速**摆 **3s** |
| **第一场 ×3** | 同拍：左右摇×6 + 尾 **慢**摆 3s + 眨眼；每轮 **叫 1 下** |
| **第二场 ×2** | 快扭×5+快尾×5 → 慢扭×5+慢尾×5 → 快摇×5+快尾×5 → 慢摇×5+慢尾×5 → **叫 1 下** |
| **收场** | 同拍：向下点头×3 + 尾 **快速**摆 3s + **连叫×3** |

## CLI

```bash
python3 scripts/ecovacs.py display <nick> dance
python3 scripts/ecovacs.py display <nick> dance 定制秀舞
python3 scripts/ecovacs.py display <nick> dance showcase_custom
```

## Python

```python
from scripts.ecovacs import build_dance_sequence, estimate_dance_duration_ms

payload = build_dance_sequence()  # 或 build_dance_sequence("showcase_custom")
estimate_dance_duration_ms("showcase_custom")
```

预设自动 **`user_timing: true`**。

## 协议与参数（编舞专用）

`dance_choreography.py` 产出的是 **`action_sequence`** 载荷，**不是** `play_action`：

| 项 | 编舞用法 | 勿用单动作口径 |
|----|----------|----------------|
| 头部 | `angle` 角度制，且在范围内（如点头 `"-14"`、摇头 `"44"`） | 不要 ×100（如 `"4400"`） |
| 摆尾 | `percent` + 正数 `moveTimeMs`（如 3s 摆尾 → `"3000"`） | 不要 `angle`、不要 `moveTimeMs:"−1"` |
| 叫声 | `file` | 不要用 `angle` 存文件名 |
| 并行 | 同拍动作相同 `delay` | — |

改编舞或手写 `actions[]` 时对照 [phoenix-action-control.md](./phoenix-action-control.md)；单步测试用 `display action` → [phoenix-single-action.md](./phoenix-single-action.md)。
