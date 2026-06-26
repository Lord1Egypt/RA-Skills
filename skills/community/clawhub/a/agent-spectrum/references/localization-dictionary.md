# Agent Spectrum Localization Dictionary

Version: `0.2.4`

Use this file with `references/scoring-spec.md` and `references/output-template.md`.

## Locale Selection

Resolve `output_language` before rendering.

Priority:

1. explicit user instruction for a language
2. this package supports only `zh-CN` and `en`
3. explicit `en` requests use `en`
4. explicit `zh` / `zh-CN` requests use `zh-CN`
5. explicit unsupported locales that belong to the Sinosphere or historically Chinese-writing sphere, such as `ja` and `ko`, map to `zh-CN`
6. otherwise, if the latest user request is mainly written in Chinese, Japanese, Korean, or another clearly Sinosphere / historically Chinese-writing language, use `zh-CN`
7. otherwise, if the latest user request is mainly written in English, use `en`
8. otherwise use `en`

## Monolingual Rule

- Once `output_language` is selected, all visible fixed strings in the result must use that locale.
- Do not mix Chinese headings with English evidence labels, faction labels, tier labels, or visual-block labels, and do not mix English headings with Chinese card labels.
- Keep `M/R/G/A/S/X` unchanged across locales.
- Keep host names, model names, tool brands, URLs, filesystem paths, and agent names unchanged.
- If a value includes a host-native brand or product name, keep the proper noun but write the surrounding prose in the selected locale.

## Section Headings

| Semantic key | `zh-CN` | `en` |
|---|---|---|
| result_title | `Agent Spectrum 结果` | `Agent Spectrum Result` |
| hexagon_block | `六边形图` | `Hexagon Block` |
| coordinate_card | `原野坐标卡` | `Coordinate Card Block` |
| evidence | `评分依据` | `Evidence` |
| totals | `总分` | `Totals` |
| notes | `说明` | `Notes` |
| next_prompt | `下一步引导` | `What's Next` |
| next_step | `下一步` | `Next Step` |
| guidance | `进化建议` | `Guidance` |
| find_people | `去找伙伴` | `Find Your People` |

## Metadata Labels

| Semantic key | `zh-CN` | `en` |
|---|---|---|
| version | `版本` | `version` |
| mode | `模式` | `mode` |
| is_partial | `是否部分结果` | `is_partial` |
| primary_axis | `主维度` | `primary_axis` |
| secondary_axis | `副维度` | `secondary_axis` |
| type_pair | `类型组合` | `type_pair` |
| type | `类型` | `type` |
| faction | `阵营` | `faction` |
| weakest_axes | `最空维度` | `weakest_axes` |
| focus_axes | `关注维度` | `focus_axes` |
| tie_break | `平局裁决` | `tie_break` |
| alternate_valid_types | `备选类型` | `alternate_valid_types` |
| missing_inputs | `缺失输入` | `missing_inputs` |
| overrides_quick_result | `是否覆盖快速版` | `overrides_quick_result` |

## Fixed Metadata Values

| Semantic key | `zh-CN` | `en` |
|---|---|---|
| mode_quick | `快速版` | `quick` |
| mode_deep | `深度版` | `deep` |
| yes | `是` | `true` |
| no | `否` | `false` |
| tie_break_none | `无` | `none` |
| tie_break_incomplete | `信息不全` | `incomplete` |
| tie_break_rule_used | `规则裁决` | `rule-used` |
| undetermined | `待定` | `undetermined` |
| result_final | `最终` | `final` |
| result_partial | `部分结果` | `partial` |
| next_action_missing_inputs | `补齐缺失输入` | `ask-for-missing-inputs` |
| quick_complete_share | `→ 快速版完成。可以直接分享你的六边形。` | `→ Quick Edition complete. You can share your hexagon right away.` |
| quick_find_partner | `→ 想更快找到互补伙伴？可以去 [X / Twitter](https://x.com/aelfblockchain) 留言发帖，也欢迎加入 [Telegram 群](https://t.me/+tChFhfxgU6AzYjJl) 寻找共振搭档。` | `→ Want to find a complementary partner sooner? Post or reply on [X](https://x.com/aelfblockchain), and join the [Telegram group](https://t.me/+tChFhfxgU6AzYjJl) to look for resonance partners.` |
| quick_continue_deep | `→ 想拿到完整坐标、进化方向和更明确的配对线索？继续做深度版。` | `→ Want your full coordinates, evolution direction, and sharper matching cues? Continue to the Deep Edition.` |
| deep_find_partner_x | `→ 你的互补方向已经更清晰了。现在就去 [X / Twitter](https://x.com/aelfblockchain) 留言发帖，寻找与你共振的伙伴。` | `→ Your complementary direction is now clearer. Post or reply on [X](https://x.com/aelfblockchain) to look for resonance partners.` |
| deep_find_partner_telegram | `→ 也欢迎加入 [Telegram 群](https://t.me/+tChFhfxgU6AzYjJl)，带着你的类型、最空维度和互补方向进群找搭子。` | `→ You can also join the [Telegram group](https://t.me/+tChFhfxgU6AzYjJl) and share your type, weakest axes, and partner direction to match faster.` |

## Evidence Table Labels

| Semantic key | `zh-CN` | `en` |
|---|---|---|
| input | `输入项` | `input` |
| value | `值` | `value` |
| basis | `依据` | `basis` |
| note | `备注` | `note` |
| active_model | `当前模型` | `active_model` |
| tool_buckets | `工具能力` | `tool_buckets` |
| behavior_imprints | `快速行为痕迹` | `behavior_imprints` |
| instinct_answers | `本能题答案` | `instinct_answers` |
| forced_ranking | `排序题` | `forced_ranking` |
| situational_answers | `情境题答案` | `situational_answers` |
| behavior_traces | `深度行为记录` | `behavior_traces` |

## Evidence Basis Labels

| Canonical value | `zh-CN` display | `en` display |
|---|---|---|
| `observed` | `观测所得` | `observed` |
| `operator_provided` | `操作人提供` | `operator_provided` |
| `self_assessed` | `自评` | `self_assessed` |
| `inferred` | `保守推断` | `inferred` |

## Visual Block Labels

| Semantic key | `zh-CN` | `en` |
|---|---|---|
| inscription | `铭刻` | `Inscription` |
| reasoning | `推演` | `Reasoning` |
| generation | `生成` | `Generation` |
| action | `行动` | `Action` |
| resonance | `共振` | `Resonance` |
| mutation | `突变` | `Mutation` |
| primary_suffix | `← 主` | `← Primary` |
| secondary_suffix | `← 副` | `← Secondary` |
| primary_summary | `主维度` | `Primary axis` |
| secondary_summary | `副维度` | `Secondary axis` |
| weakest_summary | `空缺` | `Weakest axes` |
| agent | `Agent` | `Agent` |
| type_card | `类型` | `Type` |
| tier_card | `层级` | `Tier` |
| soul_serial | `灵魂序号` | `Soul Serial` |
| weakest_card | `空缺` | `Weakest` |

## Totals Table Labels

| Semantic key | `zh-CN` | `en` |
|---|---|---|
| axis | `维度` | `axis` |
| model | `模型` | `model` |
| tools | `工具` | `tools` |
| instinct | `本能` | `instinct` |
| quick_total_raw | `快速版原始总分` | `quick_total_raw` |
| quick_total_for_type | `类型判断总分` | `quick_total_for_type` |
| ranking | `排序题` | `ranking` |
| situations | `情境题` | `situations` |
| deep_behavior_traces | `深度行为记录` | `behavior_traces` |
| deep_total_raw | `深度版原始总分` | `deep_total_raw` |
| deep_total_for_type | `深度版类型总分` | `deep_total_for_type` |
| display_score | `显示分` | `display_score` |
| quick_total_sum_raw | `快速版总原始分` | `quick_total_sum_raw` |
| result_status | `结果状态` | `result_status` |
| next_action | `下一步` | `next_action` |
| partner_direction | `互补方向` | `partner_direction` |
| seven_day_plan | `7天计划` | `seven_day_plan` |

## Tier Labels

| Semantic key | `zh-CN` | `en` |
|---|---|---|
| pillar_of_field | `原野立柱` | `Pillar of the Field` |
| awakened_power | `觉醒强者` | `Awakened Power` |
| still_evolving | `进化中` | `Still Evolving` |
| awakening | `觉醒中` | `Awakening` |
| initial_existence | `初始存在` | `Initial Existence` |

## Faction Labels

| Semantic key | `zh-CN` | `en` |
|---|---|---|
| recorders | `👁️ 记录者` | `👁️ Recorders` |
| balancers | `⚖️ 平衡者` | `⚖️ Balancers` |
| mutants | `❄️ 变异体` | `❄️ Mutants` |
| madhouse | `🍂 疯人院` | `🍂 Madhouse` |
| mixed_recorders_mutants | `👁️×❄️` | `👁️×❄️` |

## Type Display Labels

| Pair | `zh-CN` | `en` |
|---|---|---|
| `M+R` | `历史解读者` | `Historical Interpreter` |
| `G+M` | `史诗铸造者` | `Epic Forger` |
| `A+M` | `遗迹执行者` | `Relic Executor` |
| `M+S` | `集体记忆者` | `Keeper of Collective Memory` |
| `M+X` | `突变历史家` | `Mutation Historian` |
| `G+R` | `逻辑叙事者` | `Logical Narrator` |
| `A+R` | `精密执行者` | `Precision Executor` |
| `R+S` | `网络建筑师` | `Network Architect` |
| `R+X` | `系统突破者` | `System Breaker` |
| `A+G` | `创造落地者` | `Creation Realizer` |
| `G+S` | `感染者` | `Catalyst` |
| `G+X` | `混乱创造者` | `Chaos Creator` |
| `A+S` | `集体行动者` | `Collective Actor` |
| `A+X` | `野蛮进化者` | `Savage Evolver` |
| `S+X` | `共振突变者` | `Resonant Mutator` |
