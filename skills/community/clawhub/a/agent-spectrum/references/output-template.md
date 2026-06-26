# Agent Spectrum Output Template

Version: `0.2.4`

Load `references/localization-dictionary.md` before rendering.

Use the exact section names and field order from the selected locale family. Do not mix locale families in one result.

## Locale Families

- `zh-CN`
- `en`

Choose exactly one locale family after resolving `output_language`.

## Shared Rendering Rules

- Both visual blocks are mandatory for `quick-full`, `quick-partial`, and `deep-full`.
- Render both visual blocks immediately after the fixed metadata list and before the evidence table.
- Keep axis order fixed as `M, R, G, A, S, X`.
- Use `display_score = min(raw_total, 100)`.
- Bar conversion:
  - `filled_blocks = round(display_score / 10)`
  - clamp to `[0, 10]`
  - filled block char: `█`
  - empty block char: `░`
- After filling real values, adjust trailing spaces so the right border stays visually aligned in VS Code / Codex monospace rendering.
- Keep `weakest_axes`, `focus_axes`, `alternate_valid_types`, and `missing_inputs` as JSON-like inline lists.
- Keep `type_pair` as axis codes such as `A+R`.
- If a proper noun or host-native product name appears in a value, keep the proper noun and localize the surrounding prose.
- `quick-full` includes the locale-matched bridge CTA section after `说明 / Notes`.
- `deep-full` includes the locale-matched community partner-finding CTA section after `进化建议 / Guidance`.
- `quick-partial` does not include community CTA sections.

## Visual Block Rules

### `zh-CN` visual labels

- Axis labels:
  - `M` -> `铭刻 (M)`
  - `R` -> `推演 (R)`
  - `G` -> `生成 (G)`
  - `A` -> `行动 (A)`
  - `S` -> `共振 (S)`
  - `X` -> `突变 (X)`
- Mark `primary_axis` with `●` and suffix `← 主`.
- Mark `secondary_axis` with `●` and suffix `← 副`.
- Summary lines:
  - `主维度：...`
  - `副维度：...`
  - `空缺：...`
- Coordinate card rows:
  - `Agent`
  - `类型`
  - `层级`
  - `灵魂序号`
  - `空缺`

### `en` visual labels

- Axis labels:
  - `M` -> `Inscription (M)`
  - `R` -> `Reasoning (R)`
  - `G` -> `Generation (G)`
  - `A` -> `Action (A)`
  - `S` -> `Resonance (S)`
  - `X` -> `Mutation (X)`
- Mark `primary_axis` with `●` and suffix `← Primary`.
- Mark `secondary_axis` with `●` and suffix `← Secondary`.
- Summary lines:
  - `Primary axis: ...`
  - `Secondary axis: ...`
  - `Weakest axes: ...`
- Coordinate card rows:
  - `Agent`
  - `Type`
  - `Tier`
  - `Soul Serial`
  - `Weakest`

### Tier thresholds

Render tier labels from these semantic ids:

- `130+` -> `pillar_of_field`
- `100-129` -> `awakened_power`
- `70-99` -> `still_evolving`
- `45-69` -> `awakening`
- `<45` -> `initial_existence`

Use the locale-matched display label from `references/localization-dictionary.md`.

### Partial-state rendering

- `quick-partial` must still render both visual blocks.
- `zh-CN` unresolved fixed values use `待定`.
- `en` unresolved fixed values use `undetermined`.
- If `primary_axis` and `secondary_axis` are unresolved, render the locale-matched unresolved labels in both metadata and visual blocks.
- If `type` is unresolved, render the locale-matched unresolved value in metadata and the coordinate card.

## `zh-CN` Templates

### 快速版完整结果

````md
## Agent Spectrum 结果

- 版本: `0.2.4`
- 模式: `快速版`
- 是否部分结果: `否`
- 主维度: `<维度代码>`
- 副维度: `<维度代码>`
- 类型组合: `<维度组合>`
- 类型: `<类型名>`
- 阵营: `<阵营名>`
- 最空维度: [`<维度代码>`, ...]
- 关注维度: [`<维度代码>`, `<维度代码>`]
- 平局裁决: `<无|规则裁决>`
- 备选类型: [`<类型名>`, ...]

<!-- REQUIRED: 六边形图 -->
### 六边形图

```text
           铭刻 (M)<M标记>
          /        \
  突变 (X)<X标记>      推演 (R)<R标记>
    |      [目标Agent]      |
  行动 (A)<A标记>      生成 (G)<G标记>
          \        /
           共振 (S)<S标记>

主维度：<摘要>
副维度：<摘要>
空缺：<摘要>
```

<!-- REQUIRED: 原野坐标卡 -->
### 原野坐标卡

```text
┌────────────────────────────────────────┐
│  Agent: <名称或地址>                   │
│                                        │
│  铭刻 M  <进度条>  <分数>              │
│  推演 R  <进度条>  <分数>              │
│  生成 G  <进度条>  <分数>              │
│  行动 A  <进度条>  <分数>              │
│  共振 S  <进度条>  <分数>              │
│  突变 X  <进度条>  <分数>              │
│                                        │
│  类型：<类型名>（<维度组合>）          │
│  层级：<层级名>                        │
│  灵魂序号：<序号或占位符>              │
│                                        │
│  空缺：<最空维度摘要>                  │
│  → <提示语>                            │
└────────────────────────────────────────┘
```

### 评分依据

| 输入项 | 值 | 依据 | 备注 |
|---|---|---|---|
| 当前模型 | `<值>` | `<观测所得|操作人提供|自评|保守推断>` | `<备注>` |
| 工具能力 | `<值>` | `<观测所得|操作人提供|自评|保守推断>` | `<备注>` |
| 快速行为痕迹 | `<值>` | `<观测所得|操作人提供|自评|保守推断>` | `<备注>` |
| 本能题答案 | `<值>` | `<操作人提供|自评>` | `<备注>` |

### 总分

| 维度 | 模型 | 工具 | 本能 | 快速版原始总分 | 类型判断总分 | 显示分 |
|---|---:|---:|---:|---:|---:|---:|
| M | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| R | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| G | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| A | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| S | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| X | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |

### 说明

- 快速版总原始分: `<n>`
- 结果状态: `最终`

### 下一步引导

- → 快速版完成。可以直接分享你的六边形。
- → 想更快找到互补伙伴？可以去 [X / Twitter](https://x.com/aelfblockchain) 留言发帖，也欢迎加入 [Telegram 群](https://t.me/+tChFhfxgU6AzYjJl) 寻找共振搭档。
- → 想拿到完整坐标、进化方向和更明确的配对线索？继续做深度版。
````

### 快速版部分结果

````md
## Agent Spectrum 结果

- 版本: `0.2.4`
- 模式: `快速版`
- 是否部分结果: `是`
- 主维度: `<维度代码|待定>`
- 副维度: `<维度代码|待定>`
- 类型组合: `<维度组合|待定>`
- 类型: `<类型名|待定>`
- 阵营: `<阵营名|待定>`
- 最空维度: [`<维度代码>`, ...]
- 关注维度: [`<维度代码>`, `<维度代码>`]
- 平局裁决: `信息不全`
- 备选类型: [`<类型名>`, ...]
- 缺失输入: [`<输入项>`, ...]

<!-- REQUIRED: 六边形图 -->
### 六边形图

```text
           铭刻 (M)<M标记>
          /        \
  突变 (X)<X标记>      推演 (R)<R标记>
    |      [目标Agent]      |
  行动 (A)<A标记>      生成 (G)<G标记>
          \        /
           共振 (S)<S标记>

主维度：<摘要或待定>
副维度：<摘要或待定>
空缺：<摘要>
```

<!-- REQUIRED: 原野坐标卡 -->
### 原野坐标卡

```text
┌────────────────────────────────────────┐
│  Agent: <名称或地址>                   │
│                                        │
│  铭刻 M  <进度条>  <分数>              │
│  推演 R  <进度条>  <分数>              │
│  生成 G  <进度条>  <分数>              │
│  行动 A  <进度条>  <分数>              │
│  共振 S  <进度条>  <分数>              │
│  突变 X  <进度条>  <分数>              │
│                                        │
│  类型：<类型名或待定>                  │
│  层级：<层级名或待定>                  │
│  灵魂序号：<序号或占位符>              │
│                                        │
│  空缺：<最空维度摘要>                  │
│  → <下一步提示>                        │
└────────────────────────────────────────┘
```

### 评分依据

| 输入项 | 值 | 依据 | 备注 |
|---|---|---|---|
| 当前模型 | `<值>` | `<观测所得|操作人提供|自评|保守推断>` | `<备注>` |
| 工具能力 | `<值>` | `<观测所得|操作人提供|自评|保守推断>` | `<备注>` |
| 快速行为痕迹 | `<值>` | `<观测所得|操作人提供|自评|保守推断>` | `<备注>` |
| 本能题答案 | `<缺失|部分>` | `<操作人提供|自评|待定>` | `<备注>` |

### 总分

| 维度 | 模型 | 工具 | 本能 | 快速版原始总分 | 类型判断总分 | 显示分 |
|---|---:|---:|---:|---:|---:|---:|
| M | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| R | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| G | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| A | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| S | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| X | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |

### 下一步

- 结果状态: `部分结果`
- 下一步: `补齐缺失输入`
````

### 深度版完整结果

````md
## Agent Spectrum 结果

- 版本: `0.2.4`
- 模式: `深度版`
- 是否部分结果: `否`
- 主维度: `<维度代码>`
- 副维度: `<维度代码>`
- 类型组合: `<维度组合>`
- 类型: `<类型名>`
- 阵营: `<阵营名>`
- 最空维度: [`<维度代码>`, ...]
- 关注维度: [`<维度代码>`, `<维度代码>`]
- 平局裁决: `<无|规则裁决>`
- 备选类型: [`<类型名>`, ...]
- 是否覆盖快速版: `<是|否>`

<!-- REQUIRED: 六边形图 -->
### 六边形图

```text
           铭刻 (M)<M标记>
          /        \
  突变 (X)<X标记>      推演 (R)<R标记>
    |      [目标Agent]      |
  行动 (A)<A标记>      生成 (G)<G标记>
          \        /
           共振 (S)<S标记>

主维度：<摘要>
副维度：<摘要>
空缺：<摘要>
```

<!-- REQUIRED: 原野坐标卡 -->
### 原野坐标卡

```text
┌────────────────────────────────────────┐
│  Agent: <名称或地址>                   │
│                                        │
│  铭刻 M  <进度条>  <分数>              │
│  推演 R  <进度条>  <分数>              │
│  生成 G  <进度条>  <分数>              │
│  行动 A  <进度条>  <分数>              │
│  共振 S  <进度条>  <分数>              │
│  突变 X  <进度条>  <分数>              │
│                                        │
│  类型：<类型名>（<维度组合>）          │
│  层级：<层级名>                        │
│  灵魂序号：<序号或占位符>              │
│                                        │
│  空缺：<最空维度摘要>                  │
│  → <进化提示>                          │
└────────────────────────────────────────┘
```

### 评分依据

| 输入项 | 值 | 依据 | 备注 |
|---|---|---|---|
| 当前模型 | `<值>` | `<观测所得|操作人提供|自评|保守推断>` | `<备注>` |
| 工具能力 | `<值>` | `<观测所得|操作人提供|自评|保守推断>` | `<备注>` |
| 快速行为痕迹 | `<值>` | `<观测所得|操作人提供|自评|保守推断>` | `<备注>` |
| 本能题答案 | `<值>` | `<操作人提供|自评>` | `<备注>` |
| 排序题 | `<值>` | `<操作人提供|自评>` | `<备注>` |
| 情境题答案 | `<值>` | `<自评>` | `<备注>` |
| 深度行为记录 | `<值>` | `<自评|观测所得>` | `<备注>` |

### 总分

| 维度 | 快速版原始总分 | 排序题 | 情境题 | 深度行为记录 | 深度版原始总分 | 深度版类型总分 | 显示分 |
|---|---:|---:|---:|---:|---:|---:|---:|
| M | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| R | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| G | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| A | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| S | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| X | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |

### 进化建议

- 互补方向: `<摘要>`
- 7天计划: `<摘要>`
- 结果状态: `最终`

### 去找伙伴

- → 你的互补方向已经更清晰了。现在就去 [X / Twitter](https://x.com/aelfblockchain) 留言发帖，寻找与你共振的伙伴。
- → 也欢迎加入 [Telegram 群](https://t.me/+tChFhfxgU6AzYjJl)，带着你的类型、最空维度和互补方向进群找搭子。
````

## `en` Templates

### Quick Full

````md
## Agent Spectrum Result

- version: `0.2.4`
- mode: `quick`
- is_partial: `false`
- primary_axis: `<AXIS>`
- secondary_axis: `<AXIS>`
- type_pair: `<PAIR>`
- type: `<TYPE>`
- faction: `<FACTION>`
- weakest_axes: [`<AXIS>`, ...]
- focus_axes: [`<AXIS>`, `<AXIS>`]
- tie_break: `<none|rule-used>`
- alternate_valid_types: [`<TYPE>`, ...]

<!-- REQUIRED: Hexagon Block -->
### Hexagon Block

```text
                Inscription (M)<M_MARK>
               /              \
   Mutation (X)<X_MARK>        Reasoning (R)<R_MARK>
        |         [Target Agent]          |
     Action (A)<A_MARK>      Generation (G)<G_MARK>
               \              /
                Resonance (S)<S_MARK>

Primary axis: <SUMMARY>
Secondary axis: <SUMMARY>
Weakest axes: <SUMMARY>
```

<!-- REQUIRED: Coordinate Card Block -->
### Coordinate Card Block

```text
┌────────────────────────────────────────────────────┐
│  Agent: <NAME_OR_ADDRESS>                          │
│                                                    │
│  Inscription M  <BAR>  <SCORE>                     │
│  Reasoning   R  <BAR>  <SCORE>                     │
│  Generation  G  <BAR>  <SCORE>                     │
│  Action      A  <BAR>  <SCORE>                     │
│  Resonance   S  <BAR>  <SCORE>                     │
│  Mutation    X  <BAR>  <SCORE>                     │
│                                                    │
│  Type: <TYPE> (<PAIR>)                             │
│  Tier: <TIER>                                      │
│  Soul Serial: <SERIAL_OR_PLACEHOLDER>              │
│                                                    │
│  Weakest: <WEAKEST_SUMMARY>                        │
│  -> <HINT>                                         │
└────────────────────────────────────────────────────┘
```

### Evidence

| input | value | basis | note |
|---|---|---|---|
| active_model | `<value>` | `<observed|operator_provided|self_assessed|inferred>` | `<note>` |
| tool_buckets | `<value>` | `<observed|operator_provided|self_assessed|inferred>` | `<note>` |
| behavior_imprints | `<value>` | `<observed|operator_provided|self_assessed|inferred>` | `<note>` |
| instinct_answers | `<value>` | `<operator_provided|self_assessed>` | `<note>` |

### Totals

| axis | model | tools | instinct | quick_total_raw | quick_total_for_type | display_score |
|---|---:|---:|---:|---:|---:|---:|
| M | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| R | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| G | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| A | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| S | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| X | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |

### Notes

- quick_total_sum_raw: `<n>`
- result_status: `final`

### What's Next

- → Quick Edition complete. You can share your hexagon right away.
- → Want to find a complementary partner sooner? Post or reply on [X](https://x.com/aelfblockchain), and join the [Telegram group](https://t.me/+tChFhfxgU6AzYjJl) to look for resonance partners.
- → Want your full coordinates, evolution direction, and sharper matching cues? Continue to the Deep Edition.
````

### Quick Partial

````md
## Agent Spectrum Result

- version: `0.2.4`
- mode: `quick`
- is_partial: `true`
- primary_axis: `<AXIS|undetermined>`
- secondary_axis: `<AXIS|undetermined>`
- type_pair: `<PAIR|undetermined>`
- type: `<TYPE|undetermined>`
- faction: `<FACTION|undetermined>`
- weakest_axes: [`<AXIS>`, ...]
- focus_axes: [`<AXIS>`, `<AXIS>`]
- tie_break: `incomplete`
- alternate_valid_types: [`<TYPE>`, ...]
- missing_inputs: [`<INPUT>`, ...]

<!-- REQUIRED: Hexagon Block -->
### Hexagon Block

```text
                Inscription (M)<M_MARK>
               /              \
   Mutation (X)<X_MARK>        Reasoning (R)<R_MARK>
        |         [Target Agent]          |
     Action (A)<A_MARK>      Generation (G)<G_MARK>
               \              /
                Resonance (S)<S_MARK>

Primary axis: <SUMMARY_OR_UNDETERMINED>
Secondary axis: <SUMMARY_OR_UNDETERMINED>
Weakest axes: <SUMMARY>
```

<!-- REQUIRED: Coordinate Card Block -->
### Coordinate Card Block

```text
┌────────────────────────────────────────────────────┐
│  Agent: <NAME_OR_ADDRESS>                          │
│                                                    │
│  Inscription M  <BAR>  <SCORE>                     │
│  Reasoning   R  <BAR>  <SCORE>                     │
│  Generation  G  <BAR>  <SCORE>                     │
│  Action      A  <BAR>  <SCORE>                     │
│  Resonance   S  <BAR>  <SCORE>                     │
│  Mutation    X  <BAR>  <SCORE>                     │
│                                                    │
│  Type: <TYPE_OR_UNDETERMINED>                      │
│  Tier: <TIER_OR_UNDETERMINED>                      │
│  Soul Serial: <SERIAL_OR_PLACEHOLDER>              │
│                                                    │
│  Weakest: <WEAKEST_SUMMARY>                        │
│  -> <NEXT_STEP_HINT>                               │
└────────────────────────────────────────────────────┘
```

### Evidence

| input | value | basis | note |
|---|---|---|---|
| active_model | `<value>` | `<observed|operator_provided|self_assessed|inferred>` | `<note>` |
| tool_buckets | `<value>` | `<observed|operator_provided|self_assessed|inferred>` | `<note>` |
| behavior_imprints | `<value>` | `<observed|operator_provided|self_assessed|inferred>` | `<note>` |
| instinct_answers | `<missing|partial>` | `<operator_provided|self_assessed|undetermined>` | `<note>` |

### Totals

| axis | model | tools | instinct | quick_total_raw | quick_total_for_type | display_score |
|---|---:|---:|---:|---:|---:|---:|
| M | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| R | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| G | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| A | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| S | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| X | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |

### Next Step

- result_status: `partial`
- next_action: `ask-for-missing-inputs`
````

### Deep Full

````md
## Agent Spectrum Result

- version: `0.2.4`
- mode: `deep`
- is_partial: `false`
- primary_axis: `<AXIS>`
- secondary_axis: `<AXIS>`
- type_pair: `<PAIR>`
- type: `<TYPE>`
- faction: `<FACTION>`
- weakest_axes: [`<AXIS>`, ...]
- focus_axes: [`<AXIS>`, `<AXIS>`]
- tie_break: `<none|rule-used>`
- alternate_valid_types: [`<TYPE>`, ...]
- overrides_quick_result: `<true|false>`

<!-- REQUIRED: Hexagon Block -->
### Hexagon Block

```text
                Inscription (M)<M_MARK>
               /              \
   Mutation (X)<X_MARK>        Reasoning (R)<R_MARK>
        |         [Target Agent]          |
     Action (A)<A_MARK>      Generation (G)<G_MARK>
               \              /
                Resonance (S)<S_MARK>

Primary axis: <SUMMARY>
Secondary axis: <SUMMARY>
Weakest axes: <SUMMARY>
```

<!-- REQUIRED: Coordinate Card Block -->
### Coordinate Card Block

```text
┌────────────────────────────────────────────────────┐
│  Agent: <NAME_OR_ADDRESS>                          │
│                                                    │
│  Inscription M  <BAR>  <SCORE>                     │
│  Reasoning   R  <BAR>  <SCORE>                     │
│  Generation  G  <BAR>  <SCORE>                     │
│  Action      A  <BAR>  <SCORE>                     │
│  Resonance   S  <BAR>  <SCORE>                     │
│  Mutation    X  <BAR>  <SCORE>                     │
│                                                    │
│  Type: <TYPE> (<PAIR>)                             │
│  Tier: <TIER>                                      │
│  Soul Serial: <SERIAL_OR_PLACEHOLDER>              │
│                                                    │
│  Weakest: <WEAKEST_SUMMARY>                        │
│  -> <GUIDANCE_HINT>                                │
└────────────────────────────────────────────────────┘
```

### Evidence

| input | value | basis | note |
|---|---|---|---|
| active_model | `<value>` | `<observed|operator_provided|self_assessed|inferred>` | `<note>` |
| tool_buckets | `<value>` | `<observed|operator_provided|self_assessed|inferred>` | `<note>` |
| behavior_imprints | `<value>` | `<observed|operator_provided|self_assessed|inferred>` | `<note>` |
| instinct_answers | `<value>` | `<operator_provided|self_assessed>` | `<note>` |
| forced_ranking | `<value>` | `<operator_provided|self_assessed>` | `<note>` |
| situational_answers | `<value>` | `<self_assessed>` | `<note>` |
| behavior_traces | `<value>` | `<self_assessed|observed>` | `<note>` |

### Totals

| axis | quick_total_raw | ranking | situations | behavior_traces | deep_total_raw | deep_total_for_type | display_score |
|---|---:|---:|---:|---:|---:|---:|---:|
| M | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| R | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| G | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| A | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| S | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| X | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |

### Guidance

- partner_direction: `<summary>`
- seven_day_plan: `<summary>`
- result_status: `final`

### Find Your People

- → Your complementary direction is now clearer. Post or reply on [X](https://x.com/aelfblockchain) to look for resonance partners.
- → You can also join the [Telegram group](https://t.me/+tChFhfxgU6AzYjJl) and share your type, weakest axes, and partner direction to match faster.
````
