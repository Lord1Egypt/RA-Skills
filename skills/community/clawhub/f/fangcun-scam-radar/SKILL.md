---
name: fangcun-scam-radar
slug: fangcun-scam-radar
displayName: "防割雷达"
summary: "十问自查可疑理财营销（荐股群/低价课/保本高息），命中给官方持牌查验路径；不下定性、不荐股、不代操作。"
display_name: 防割雷达
display_name_en: Scam Radar
description: 理财防割韭菜识别助手。当用户遇到"老师荐股/带单"、"9元/免费理财课"、"保本高收益"、"内幕消息"、可疑理财App/平台，想自查风险、验证对方是否持牌时使用。对话式十问采集，用户零格式门槛。只教通用识别特征+给持牌查验入口+列命中事实，绝不替用户给"某产品/课程/平台是骗局"的定性判断，不荐股不代操作。适合所有被理财营销包围的普通人。
description_zh: 对话式十问采集可疑理财营销的特征（荐股群/低价课/保本高息/陌生App），命中即给官方持牌查验路径；绝不下"是骗局"定性、不荐股、不代操作。
description_en: Ten-question conversational self-check for suspicious investment marketing (stock-picking groups, cheap courses, "guaranteed" high returns, unknown apps). Lists matched facts plus official license-verification entrances; never issues a verdict and never recommends products.
version: 1.0.0
author: fangcun
license: MIT
agent_created: true
examples_zh:
- "群里有个老师天天带单，靠谱吗"
- "报了个 9 块钱的理财训练营，班主任让我报 6800 的进阶班"
- "有个平台说保本保息年化 12%，能投吗"
examples_en:
- "An 'instructor' runs a stock-picking group and shares positions daily - is it legit?"
- "I joined a 9-yuan finance bootcamp; the tutor now pushes a 6800-yuan advanced class"
- "A platform promises principal-protection plus 12% APY - should I invest?"
---


# Fangcun Scam Radar

Scam-risk self-check for investment marketing such as tipster groups, cheap finance courses and guaranteed-return pitches. Teaches general red flags and licence verification entry points only; it does not label any product or course a scam, recommend investments or trade on the user's behalf.

## How to Use

Load this skill and state your concrete inputs. The bundled references, scripts and templates carry the detailed rules and worked examples; the assistant should consult them before answering.

## Bundled Resources

- `CHANGELOG.md`
- `README_____.md`
- `references/case_material.md`
- `references/check_entrances.md`
- `references/dialog_flows.md`
- `references/interview.md`
- `scripts/radar_check.py`
- `tests/README.md`
- `tests/case_clean.json`
- `tests/case_crypto.json`
- `tests/case_full.json`
- `tests/case_partial.json`
- `tests/regen_snapshots.py`
- `tests/report_case_clean.md`
- `tests/report_case_crypto.md`
- `tests/report_case_full.md`
- `tests/report_case_partial.md`
- `tests/report_clean.md`
- `tests/report_crypto.md`
- `tests/report_full.md`
- `tests/report_partial.md`
- `tests/report_s_cheapcourse.md`
- `tests/report_s_insurancemixed.md`
- `tests/report_s_stockgroup.md`
- `tests/report_s_unknownapp.md`

## Notes

This package is a static knowledge and tooling bundle. It does not call external services, does not place orders or trades, and makes no return promises. Verify any hardware-specific values against the official datasheet for your part.

Author: fangcun. License: MIT.
