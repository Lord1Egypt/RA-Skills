---
name: baoqingtian
description: Use when judging an early product idea, MVP, AI tool, creator product, or launched demo with Baoqingtian-style demand evidence, verdicts, seven-day validation tasks, and a visual verdict card.
---

# 包青天

## Purpose

Use this skill to审 idea / MVP / AI 产品 / 作品型产品. The output must include:

1. A stable visual HTML verdict card rendered from the bundled template.
2. A detailed Markdown verdict report.

Do not ask the model to freestyle card design. Generate structured case data, then run the renderer.

## Verdict Method

Judge evidence, not enthusiasm.

Evidence ladder: `口供 < 旁证 < 物证 < 银票 < 血书`

Verdict levels:
- `不予立案`: no clear user, scene, pain, or evidence.
- `押后再审`: some pain, but scope or evidence is too weak.
- `准予翻案`: possible direction; requires seven-day proof.
- `准予试做`: has real evidence; do service-first or narrow MVP.
- `准予开工`: strong evidence and clear next build step.

Four scores:
- `需求真度`: pain, frequency, urgency, specificity.
- `付费可能`: payer clarity, budget, pricing proof.
- `分发可达`: founder can reach first users repeatedly.
- `创始人匹配`: why this founder can keep doing it.

Tone: direct, modern, Baoqingtian-flavored. First name the problem, then give the remedy.

## Workflow

1. Read the user's 状纸 and infer missing fields conservatively.
2. Create a case JSON using the schema below.
3. Save it as a temporary `.json` file.
4. Run:

```bash
python3 ~/.codex/skills/baoqingtian/scripts/render_verdict.py --case-json /path/to/case.json --out-dir /path/to/output
```

5. Return the generated HTML and Markdown file links.

## Case JSON Schema

Required top-level fields:

```json
{
  "case_title": "不超过12字",
  "subtitle": "一句话说明案由",
  "ruling_level": "准予试做",
  "verdict_tag": "准予试做 · 需补证",
  "verdict": "先服务 · 再产品化",
  "score": 76,
  "evidence_level": "银票",
  "evidence_label": "证据力：银票 2/5",
  "metrics": [
    {"name": "需求真度", "score": 78, "judgement": "一句话判词"},
    {"name": "付费可能", "score": 62, "judgement": "一句话判词"},
    {"name": "分发可达", "score": 74, "judgement": "一句话判词"},
    {"name": "创始人匹配", "score": 88, "judgement": "一句话判词"}
  ],
  "problems": [
    {"title": "问题名", "desc": "一句话说明"},
    {"title": "问题名", "desc": "一句话说明"},
    {"title": "问题名", "desc": "一句话说明"}
  ],
  "judgement": "本案最关键判语",
  "tasks": ["七日任务一", "七日任务二", "七日任务三"],
  "detailed": {
    "ruling": "立案等级说明",
    "pseudo_demand_risk": "伪需求嫌疑说明",
    "key_deaths": ["展开死因一", "展开死因二", "展开死因三"],
    "strongest_evidence": "最强证据",
    "biggest_gap": "最大缺口",
    "appeal": "准予/不准予翻案",
    "seven_day_tasks": ["任务一", "任务二", "任务三"]
  }
}
```

Optional fields: `case_no`, `theme` (`black`, `gray`, `white`), `source_url`.

Theme selection when absent:
- `black` for `不予立案` or score below 45.
- `white` for `准予开工` or score 80+.
- `gray` otherwise.

