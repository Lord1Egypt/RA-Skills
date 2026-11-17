# Workflow Reference — 24 Tasks, 4 Gates, 3 Routes

Load this file when planning a project, sequencing work, or deciding where to roll back to.

## 1. Task Cards

Six columns per card: action · deliverable · acceptance · days · owner. Cards marked `AI 草稿` require human rewrite before completion.

### P0 立项 — 10 days

| ID | Task | Action | Deliverable | Acceptance | Days | Owner |
|---|---|---|---|---|---|---|
| W01 | 题材筛选 | List 5 candidate 母体, score each 1–5 on market heat / manufacturability / narrative room | 3 candidates + score table | ≥1 candidate scores ≥4 on two axes | 3 | 主理人 |
| W02 | 竞品扫描 | Find 10 in-category products (include 3 that flopped); record scale, price, recognition-point count, top complaint keywords | competitor table | complaints cluster into ≥3 groups | 4 | AI 草稿 |
| W03 | 商业假设 | Fix ratio, height, target price, volume, channel, mold route; cross-check against the detail budget | one-page brief (asset 01) | four numbers are mutually consistent | 2 | 主理人 |
| W04 | 立项评审 G0 | Answer "build it or not"; refute three reasons not to build | Go/No-Go record | all three objections answered | 1 | 主理人 |

### P1 设定 — 8 days

| ID | Task | Action | Deliverable | Acceptance | Days | Owner |
|---|---|---|---|---|---|---|
| W05 | 人设三问 | What is it doing right now / where is it looking / what is it hiding, plus a one-line claim for the box back | character card | the sentence is specific and contains an action | 2 | 主理人 |
| W06 | 姿势三方案 | Fix pose before face; each option states gaze target and hand action; the three must differ in strategy, not costume | 3 pose sketches | gaze targets all differ | 3 | AI 草稿 |
| W07 | 仕様書 v1 | Fill every field: accessories, expressions, materials, dimensions, base, paint method | spec sheet (asset 02) | no line substitutes "参考图" for a requirement | 2 | AI 草稿 |
| W08 | 授权核对 | Licensed IP only: list approval nodes, asset rights, review-round budget | submission pack + schedule | three review nodes are on the Gantt | 2 | 主理人 |

### P2 造型 — 12 days

| ID | Task | Action | Deliverable | Acceptance | Days | Owner |
|---|---|---|---|---|---|---|
| W09 | 剪影测试 | Fill three options solid black, shrink to thumbnail, place beside category top-10 | silhouette comparison | ≥1 outline does not repeat a competitor | 3 | 主理人 |
| W10 | 三视图与动势 | Front / side / back + one line of action + non-parallel shoulder and hip lines | three-view v1 | silhouettes consistent across views, no instability when flipped | 5 | AI 草稿 |
| W11 | 表面与材质采样 | List 5–8 details; assign each a **real sampling source** (fruit skin, fabric, rust, bone) | detail list + reference photos | count within the detail budget | 4 | 主理人 |
| W12 | 配色 | ≤4 blocks, 60/25/15, lock color codes; verify at thumbnail size and in low light | color sheet + codes | main blocks still separable at 1 cm | 2 | 主理人 |
| W13 | 造型评审 G1 | Record all three tests, issue a frozen version number | Design Freeze record | all three tests passed and archived | 1 | 主理人 |

### P3 建模工程 — 18 days

| ID | Task | Action | Deliverable | Acceptance | Days | Owner |
|---|---|---|---|---|---|---|
| W14 | 数字雕刻 | Dynamesh for mass → TrimDynamic / Polish for hard edges → ZRemesher + Project to keep detail | high-poly model | form matches the frozen three-view | 7 | 建模师 |
| W15 | 拆件方案 | Cut on natural boundaries (hairline, collar, cuff, belt, boot top); write a reason per seam | part-split sheet (asset 03) | every seam has a reason, none on the face | 3 | 建模师 |
| W16 | 结构工程 | Draft 1–3°, wall 2.5–4 mm, pegs 0.25–0.3 mm, magnet holes +0.2–0.3, counterweight cavity, section drawing | engineering model + section | all values inside the rule table | 5 | 建模师 |
| W17 | 手板打印 | Resin print → remove supports → 800/1500 wet sand → filler → grey primer | 5–10 grey masters | form problems are visible on the master | 3 | 打印方 |
| W18 | 工程评审 G2 | Factory DFM review with **written sign-back**: buildable / must change what | DFM report + signature | written confirmation, not verbal | 2 | 工厂 |

### P4 打样 — 12 days

| ID | Task | Action | Deliverable | Acceptance | Days | Owner |
|---|---|---|---|---|---|---|
| W19 | 涂装打样 | Six-layer process: primer → shadow → base ×3 → highlight → panel line → clear coat; face by hand or water-slide decal | golden sample 2–3 pcs | color codes verified, face acceptable | 7 | 涂装方 |
| W20 | 包装与跌落 | Window box / blister / gift box; 1 m drop test; shoot photos in parallel | packaging sample + test log | 1 m drop, six faces, no breakage | 3 | 包装厂 |
| W21 | 商品评审 G3 | Cost build-up (incl. mold amortization, returns), price, margin; decide batch size | release sheet | margin ≥3× total cost | 2 | 主理人 |

### P5 量产 — 30–60 days

| ID | Task | Action | Deliverable | Acceptance | Days | Owner |
|---|---|---|---|---|---|---|
| W22 | 开模与试模 | Steel 15–30 d / silicone 2–5 d; compare T1 shot line-by-line with the golden sample | mold acceptance + T1 | T1 matches sample within color tolerance | 5–30 | 工厂 |
| W23 | 量产与 QC | Three gates: incoming / first-article + patrol / final AQL 2.5; log defect types | QC report (asset 05) | defect rate within agreed range, no batch color drift | 15–20 | 工厂 |
| W24 | 上市与复盘 | Launch data, complaint clustering, secondary share rate; decide what the second SKU changes | review report + SKU-2 decision | can name three changes for the next model | 7 | 主理人 |

## 2. Gate Checklists

Each gate needs a one-page record: criteria ticked individually, conclusion, date. No record = not passed.

### G0 立项
1. One sentence states where it lives, who buys it, why they buy it.
2. Ratio, height, price, detail count are mutually consistent.
3. Three competitors that would sit beside it are named, with the difference stated.
4. Mold route fixed (silicone / steel) with MOQ and lead time confirmed.

### G1 造型冻结
1. Black-silhouette test passed; outline does not duplicate the category top-10.
2. Exactly one primary + one secondary recognition point.
3. Front / side / back silhouettes all hold; flipping the image produces no falling sensation.
4. ≤4 color blocks, color codes locked.
5. After freeze, no form changes without returning to W09 and issuing a new version number.

### G2 结构冻结
1. Every part demolds, no undercuts, draft 1–3°.
2. No parting line crosses the face.
3. Wall thickness in range, max/min ≤1.3.
4. Every fit has a numeric clearance.
5. Factory has signed DFM in writing.

### G3 量产放行
1. Golden sample approved in writing; physical + photos + color codes archived.
2. Margin ≥3× cost including amortization; otherwise return to W03 and re-fix the scale.
3. Packaging passes drop test; paint line slot booked.
4. Blind-box probabilities, age limits, and compliance marks confirmed.

## 3. Rollback Rules

Rolling back to the wrong stage is the most expensive mistake in the process.

| Symptom | Return to | Why here | Forbidden |
|---|---|---|---|
| G0 rejected | W01 | The subject itself fails; no amount of spec polish saves it | "Build a rough version first" |
| Silhouette fails | W09 | Silhouette is the foundation; added detail makes the error more expensive | Entering W14 |
| Cannot split parts | W11 | The form itself created unsplittable geometry (floating ribbons, fused fingers, unsupported thin parts) | Forcing cuts at the engineering stage |
| Wall / tolerance problem | W16 | Pure structure issue; the form is innocent | Changing the form to accommodate structure |
| Price cannot hold | W03 | Not a cost problem — the scale was chosen wrong (too large, too many accessories) | Silently cutting accessories to lower price |
| Mold already cut | — | Only color, packaging, accessories may change | Any form change (= new mold) |

## 4. Three Routes

| Route | Goal | Trimming | Duration | Volume |
|---|---|---|---|---|
| 自嗨款 | Portfolio piece / make it real once | Simplify P0, drop factory DFM in P3, skip P5; print in-house | ~45 d | 1–5 pcs |
| 验证款 (default) | Test whether it sells | All 24 tasks, silicone mold, 100 pcs | ~90 d | 50–100 pcs |
| 量产款 | Retail / licensing | Full process + steel mold + AQL full inspection + engineered packaging | ~150 d | 1000+ pcs |

Default to 验证款: it buys the "does it sell" answer for roughly one tenth of the mold cost.

## 5. File Layout and Naming

```
<CODE>/
├── 00_brief/       brief, competitor table, G0 record
├── 01_spec/        character card, spec sheet, licensing pack
├── 02_form/        silhouette tests, three-view, color sheet, G1 freeze record
├── 03_engineer/    high-poly, part-split sheet, sections, STL, DFM sign-back
├── 04_sample/      master photos, golden sample, packaging, drop-test log
├── 05_production/  mold acceptance, QC reports, shipping
└── 06_launch/      launch data, review report
```

Naming: `<CODE>_v<NN>_<content>_<YYYYMMDD>.<ext>` — e.g. `MOCHI_v03_三视图_20261102.png`.

Frozen versions carry `FREEZE` and are never overwritten: `MOCHI_v05_三视图_FREEZE_20261110.png`. Every later edit opens a new version number.
