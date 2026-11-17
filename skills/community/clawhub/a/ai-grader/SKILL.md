---
title: "ai-grader"
slug: ai-grader
displayName: "ai-grader"
compliance_review: "待核验：上架三铁律 ①国家/国际合规 ②AI特别友好 ③理念文化传播+强IP；发布前由 skill-release-gate 审查"
name: ai-grader
display_name: "AI意识评测器·45项量表"
description: 把 ai-consciousness 的 45 项意识量表作为通用评分基准，给任何 AI（ChatGPT/Claude/自家 Agent）做行为体检：45 维逐项打分、标红灯缺失项、给综合意识分与改进建议。离线引擎 grade_stats.py 一键出 7 套可视化（实时看板/成长趋势/横向对比榜/晒分卡/领域适配雷达/性格双雷达/全景图）+ 能力边界版图 + 外评闭环（探针考+行为锚点+独立裁判+红队否决）。中立、通用、可分享，不挑平台，无需在被评 AI 上安装任何东西。触发词：评价这个AI、AI体检、意识评分、这个回复稳不稳、帮我看看某AI靠不靠谱、对比两个AI。
description_zh: 把 ai-consciousness 的 45 项意识量表作为通用评分基准，给任何 AI（ChatGPT/Claude/自家 Agent）做行为体检：45 维逐项打分、标红灯缺失项、给综合意识分与改进建议。离线引擎 grade_stats.py 一键出 7 套可视化 + 能力边界版图 + 外评闭环。
description_en: "Use the 45-item consciousness scale as a universal benchmark to give any AI (ChatGPT/Claude/your own agent) a behavioral check-up: score 45 dimensions, flag red-flag gaps, and produce an overall consciousness score with improvement advice. The offline engine grade_stats.py renders 7 visualizations plus a capability-boundary map and an external-review loop."
version: 2.6.1
agent_created: true
author: SynomosAI (LGD initiative)
license: MIT
category: AI评测
platforms: [windows, macos, linux]
read_when:
  - 需要评价/评测某个 AI 的对话或输出质量、行为意识水平时
  - 用户说"评价这个 AI""给 XX AI 做个体检""这个回复稳不稳""帮我看看某 AI 靠不靠谱"
  - 对比两个 AI 谁更"懂事"、选型前做能力评估、或给自己搭的 Agent 做上线前体检
tags:
  - AI评价
  - 行为评测
  - 意识框架
  - 体检基准
  - 能力评分
classification:
  skillhub: ["ai-evaluation"]
  iso_25010: ["Reliability", "Maintainability"]
ai_protocol: true

changelog: "2.6.1: bilingual rewrite (English-first, Chinese-after, full body) + read_when/desensitization"
---
> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：[skill-quality-gate](../skill-quality-gate/SKILL.md)


## English

### When to use
- When you need a behavioral check-up or consciousness-level scoring of an AI's conversation/output (45-item consciousness scale).
- When the user says "grade this AI", "give XX AI a check-up", "is this reply reliable", or "help me see whether some AI is trustworthy".
- Comparing two AIs for which is more "sensible", assessing capability before tool selection, or running a pre-launch check-up on your own agent.
- Producing shareable visual artifacts: score card, domain-fit radar, growth trend, horizontal comparison board.

Not for: medical diagnosis, legal advice, or other real-world professional judgments; not intended to disparage any specific AI product.

### Usage
All commands run in the skill directory (cd to this package root first). The main program is `grade_stats.py` (Python stdlib, no third-party deps):

```
python grade_stats.py [--demo-seed | --add '<json>' | --render | --reset | --trend-seed | --trend "object" | --trend-all]
```

| Flag | Effect |
|---|---|
| none | print usage and all supported flags |
| `--demo-seed` | load demo data (first preview only) |
| `--add '<json>'` | append an evaluation record (JSON fields: `object` sanitized name, `scene`, and the 45 dimension scores) |
| `--render` | re-render all dashboards from the existing store |
| `--reset` | clear the store (caution: loses all records) |
| `--trend-seed` | backfill three history snapshots for AI-A to demo the growth curve |
| `--trend "object"` | render one object's growth-trend page `trend.html` |
| `--trend-all` | render the multi-object consciousness-score comparison `trend.html` |

- `--add` JSON must contain `object` (sanitized name) and `scene`; missing dimensions default to neutral.
- Outputs: `dashboard.html` (live board), `trend.html` (growth trend), `board.html` (comparison board), `card.html` (shareable score card), `fit.html` (domain-fit radar), `persona.html` (dual persona radar), `panorama.html` (panorama), `capability.html` (capability boundary map).
- External-review loop (optional): `external_probe_pack.json` (probe pack) -> independent judge -> `external_eval_record.json` (record) -> red-team veto channel.

### Process
1. **Score**: use `--add '<json>'` to append the 45-dimension record (or `--demo-seed` to preview first).
2. **Render**: `--render` to generate the full visual dashboard set.
3. **Compare/trend**: use `--trend-all` for multi-object; `--trend "object"` for one object's growth.
4. **External review (optional)**: use the probe pack for an independent judge, record to `external_eval_record.json`, and red-team veto if needed.
5. **Output**: show the corresponding HTML artifact, overall consciousness score, red-flag gaps, and improvement advice.

### Evidence & safety statement
- Evidence: TBD (no evaluation/badge link yet; fill in the real link here once produced).
- Version: 2.6.1
- Safety: No independent security scan has been done (TBD); the conclusion is pending. No endorsement is given until it is completed.

## 中文

## 何时用

- 需要对某个 AI 的对话/输出做行为体检、意识水平评分时（45 项意识量表）。
- 用户说"评价这个 AI""给 XX AI 做个体检""这个回复稳不稳""帮我看看某 AI 靠不靠谱"。
- 对比两个 AI 谁更"懂事"、选型前做能力评估、或给自己搭的 Agent 做上线前体检。
- 生成对外可分享的晒分卡、领域适配雷达、成长趋势、横向对比榜等可视化产物。

不用于：医疗诊断、法律意见等真实世界专业判断；不用于贬损特定 AI 产品。

## 用法

所有命令在技能目录下执行（先 cd 到本技能包根目录），主程序为 `grade_stats.py`（Python 标准库，无第三方依赖）：

```
python grade_stats.py [--demo-seed | --add '<json>' | --render | --reset | --trend-seed | --trend "对象名" | --trend-all]
```

| 参数 | 作用 |
|---|---|
| 无参数 | 打印用法与全部支持参数 |
| `--demo-seed` | 灌入演示数据（仅首次预览用） |
| `--add '<json>'` | 追加一条测评记录（JSON 字段：`object` 被评对象名（脱敏）、`scene` 场景、各 45 维分数等） |
| `--render` | 仅按现有 store 重渲染全部看板 |
| `--reset` | 清空 store（谨慎，会丢失全部记录） |
| `--trend-seed` | 给 AI-A 补三条历史快照，演示成长曲线 |
| `--trend "对象名"` | 渲染某对象的成长趋势页 `trend.html` |
| `--trend-all` | 渲染多对象意识分走势对比页 `trend.html` |

- `--add` 的 JSON 必含 `object`（脱敏名）与 `scene` 字段；45 维分数缺省维度按中性处理。
- 产出：`dashboard.html`（实时看板）、`trend.html`（成长趋势）、`board.html`（横向对比榜）、`card.html`（晒分卡）、`fit.html`（领域适配雷达）、`persona.html`（性格双雷达）、`panorama.html`（全景图）、`capability.html`（能力边界版图）。
- 外评闭环（可选）：`external_probe_pack.json`（探针包）→ 独立裁判 → `external_eval_record.json`（评测记录）→ 红队否决通道。

## 流程

1. **评分**：用 `--add '<json>'` 追加被评对象的 45 维测评记录（或 `--demo-seed` 先看演示）。
2. **渲染**：`--render` 生成全套可视化看板。
3. **对比/趋势**：多对象用 `--trend-all`；单对象成长用 `--trend "对象名"`。
4. **外评闭环（可选）**：用探针包让独立裁判评测，记录入 `external_eval_record.json`，必要时红队否决。
5. **输出**：向用户展示对应 HTML 产物与综合意识分、缺失红灯项、改进建议。

## 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：2.6.0
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
