---
name: figure-design
description: Design and gate-check collectible figures and designer toys (手办 / 潮玩 / 盲盒 / GK / 雕像) as manufacturable products. Use when the user asks to design a figure or character statue, turn a 2D character into a physical product, write or review a 仕様書 / spec sheet, plan a figure project end to end, review 拆件 / 分模 / 壁厚 / 公差 / 拔模角 before tooling, generate AI concept-art prompts for figures, or diagnose defects such as 脸崩 / 站不住 / 接缝难看 / 装不上 / 色差. Encodes the Three-Translations model (2D → 3D → molds → shelf) plus a 24-task, 4-gate workflow with numeric manufacturing limits. Do not use for 2D illustration only, plush sewing patterns, or pure market-size research.
agent_created: true
---

# Figure Design

## Overview

Turn a character idea into a manufacturable figure by controlling three translations: **2D → 3D (form)**, **3D → part set (engineering)**, **part set → shelf (commerce)**. Each translation loses information. Defects such as a collapsed face, a figure that will not stand, or a visible seam are all cases where a translation failed and nothing blocked it.

Most figure projects fail at translation two, not at drawing. Treat engineering limits as design constraints from the first sketch, not as a problem to solve after the sculpt is done.

## When to Use

Use this skill when the request involves a **physical figure product**:

- Designing a new figure, statue, blind-box series, or GK from a concept or IP.
- Converting a character illustration into a three-view, then a part set.
- Writing or reviewing a 仕様書 (spec sheet), 拆件表 (part-split sheet), or DFM brief.
- Judging feasibility before paying for tooling ("能不能开模", "这样做得出来吗").
- Diagnosing a defect: face collapse, unstable stance, seam through the face, parts that will not fit, batch color drift.
- Producing AI concept prompts for figure rendering.

Do not use for: 2D illustration or character design with no physical output; plush/sewing pattern making; market-size or financial research; packaging-only work.

## Core Model: Three Translations, Four Gates

| Stage | Translation | Deliverable | Failure if skipped | Gate |
|---|---|---|---|---|
| T0 企划 | decide before drawing | one-page brief | wrong scale, wrong price band | **G0** |
| T1 造型 | 2D → 3D | frozen three-view | silhouette reads as generic, cannot stand | **G1** |
| T2 工程 | 3D → part set | part-split sheet + DFM sign-off | cannot demold, cannot assemble | **G2** |
| T3 商品 | part set → shelf | golden sample | color drift, price below cost | **G3** |

Gates sit where cost jumps: G0 costs nothing, G1 costs 1–2 weeks, G2 costs the mold, G3 is irreversible. Never advance past a failed gate.

Full task cards, rollback rules, and the three project routes: `references/workflow.md`.

## Workflow: 6 Phases / 24 Tasks

| Phase | Tasks | Key deliverable | Days |
|---|---|---|---|
| P0 立项 | W01 题材筛选 · W02 竞品扫描 · W03 商业假设 · W04 立项评审 | one-page brief (asset 01) | 10 |
| P1 设定 | W05 人设三问 · W06 姿势三方案 · W07 仕様書 · W08 授权核对 | 仕様書 v1 (asset 02) | 8 |
| P2 造型 | W09 剪影测试 · W10 三视图 · W11 表面采样 · W12 配色 · W13 造型冻结 | frozen three-view | 12 |
| P3 建模工程 | W14 雕刻 · W15 拆件 · W16 结构 · W17 手板 · W18 DFM 回签 | part-split sheet (asset 03) | 18 |
| P4 打样 | W19 涂装打样 · W20 包装跌落 · W21 商品评审 | acceptance sheet (asset 04) | 12 |
| P5 量产 | W22 开模试模 · W23 量产 QC · W24 上市复盘 | QC log (asset 05) | 30–60 |

Routes: **自嗨款** ~45 days (skip factory DFM) · **验证款** ~90 days (silicone mold, 100 pcs — recommended default) · **量产款** ~150 days (steel mold, 1000+ pcs). Default to 验证款 unless the user states otherwise.

## Gate Criteria

**G0 立项** — one sentence covering where it lives, who buys it, why; ratio/height/price/detail-count are mutually consistent; three head-to-head competitors identified with a stated difference; mold route and MOQ fixed.

**G1 造型冻结** — black-silhouette test passes and does not duplicate the top-10 in-category outlines; exactly one primary + one secondary recognition point; all three views hold up and flipping the image does not feel unstable; ≤4 color blocks with locked color codes.

**G2 结构冻结** — every part demolds without undercuts, draft angle 1–3°; no parting line crosses the face; wall thickness in range with max/min ratio ≤1.3; all fits have numeric clearance; **factory signs DFM in writing**.

**G3 量产放行** — golden sample approved in writing and archived as QC baseline (physical + photos + color codes); gross margin ≥3× total cost including mold amortization; packaging passes 1 m drop; blind-box probability disclosure and age labeling confirmed.

## Numeric Red Lines

Memorize these eight; the rest are in `references/numbers.md`.

| Item | Value |
|---|---|
| Wall thickness, PVC / 搪胶 | 2.5–4 mm (max/min ≤1.3) |
| Wall thickness, hollow resin | 1.5–2 mm + drain holes |
| Peg / socket clearance | 0.25–0.3 mm (moving parts 0.2–0.5) |
| Draft angle | 1–3° |
| Ball joint diameter | 15–20% thicker than the limb |
| Eye position | 15–20% below the head's midline |
| Color blocks | ≤4, split 60 / 25 / 15 |
| Detail floor | FDM ≥1 mm · resin ≥0.3 mm |

## Operating Procedures

### A. Design from scratch
1. Resolve T0 first: fix ratio, height, target price, and detail budget. Reject combinations that do not exist in the market (e.g. 1/12 at ¥1500).
2. Ask for or infer the 母体 (cultural source). One primary recognition point, one secondary — a third starts destroying the silhouette.
3. Run the black-silhouette test before any detail work. If it fails, remove accessories rather than adding detail.
4. Only after the silhouette is frozen, move to three-view, then part splitting.
5. State the gate the work currently sits at, and what is still missing to pass it.

### B. Review an existing design or sculpt
1. Load `references/method.md` for the four-form and five-stage checklists.
2. Check in this order — silhouette, stance/recenter, three-view consistency, part split, wall/draft/clearance. Report the **earliest** failing layer only; later fixes are wasted until it passes.
3. For part-split review, require a written reason for every seam. A seam without a reason gets replanned.
4. Grade against the 100-point self-check in `references/method.md` and give a single verdict: 开模 / 先打样 / 回炉.

### C. Write a 仕様書
Copy `assets/templates/02_仕様書.md` and fill every field. Reject any line that says "参考图" instead of stating the requirement — the target reader is a sculptor who must not need to ask questions.

### D. AI concept art for figures
Load `references/prompts.md`. Use the seven-segment prompt skeleton (category anchor → style anchor → subject → head-body ratio → color ratio → process evidence → quality suffix). Flag clearly that AI output cannot enter tooling without retopology, wall thickening, and drain holes.

### E. Defect triage
Match the symptom to the earliest broken translation using the failure map in `references/method.md`. Return: cause, the stage to roll back to, and the specific fix. Do not offer cosmetic fixes for structural causes.

## Scripts

**Scaffold a project** (creates the folder tree, copies and prefills all five templates, writes a kanban checklist):

```bash
python scripts/new_project.py --code MOCHI --name "麻糍兔" --out <dir> --ratio 1/7 --price 899
```

**Validate design parameters against the rule table** (pass/warn/fail per item, then an overall gate verdict):

```bash
python scripts/gate_check.py params.json
python scripts/gate_check.py --ratio 1/7 --height 240 --price 899 --wall 3.0 --gap 0.28 --colors 4 --points 6
```

Run `gate_check.py` before answering any feasibility question. Do not eyeball numbers that the script can verify.

## Output Conventions

- Deliver files, not just prose. Put artifacts in the project folder created by `new_project.py`.
- Name versions as `<CODE>_v<NN>_<content>_<YYYYMMDD>`; mark frozen versions with `FREEZE` and never overwrite them.
- When a design is frozen, say so explicitly and list what is now locked (form / structure / color).
- Cite the gate being passed, and the remaining risk in plain terms.

## Resources

- `references/workflow.md` — full 24 task cards, four gate checklists, rollback rules, three routes, file layout.
- `references/method.md` — four-form sculpture model, five engineering stages, 12 hard rules, 100-point self-check, failure map, case digest.
- `references/numbers.md` — complete numeric tables: scale/height/price, mold economics, coating parameters, tolerance table.
- `references/cases.md` — ten worked cases, each stating which translation it won on.
- `references/prompts.md` — seven-segment prompt skeleton, image-to-3D chain, AI boundaries.
- `assets/templates/` — 01 项目Brief, 02 仕様書, 03 拆件与工程表 (CSV), 04 打样验收单, 05 QC抽检表 (CSV).
