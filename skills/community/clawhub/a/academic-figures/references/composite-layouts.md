# Composite Figure Layout Patterns

> **何时读我**：多面板排版：panel_labels/span/占位。
> **最短路径**：先看版式库，抄最接近的布局 JSON。
> **回 INDEX**：SKILL.md「文件索引与 30 秒路由」。

Proven multi-panel layouts for journal submission figures. Each layout combines
chart types that tell a coherent clinical story.

## Layout Conventions

- Panel labels: **A, B, C...** (bold, top-left of each panel)
- Use `composite` type with JSON data specifying `layout: [rows, cols]`
- Each panel gets its own `data` object matching its chart type schema
- Per-panel flags: `legend`, `show_values`, `trend`, `hatch`, `horizontal`, `show_ratio`

## All Proven Layouts (23 total)

### Layout Grid Shapes

| Shape | Count | Use case |
|-------|-------|----------|
| 1×2 vertical | 6 | Paired analyses (mechanism + outcome, diagnostic + performance) |
| 1×3 horizontal | 4 | Disease profiling across 3 dimensions |
| 1×4 horizontal | 1 | Full pipeline (presentation → diagnosis → kinetics → outcome) |
| 2×2 mixed | 3 | Comprehensive 4-panel figures (efficacy, immunology) |
| 2×3 six-panel | 2 | Full multi-subtype comparison (JIA, biologics) |
| 3×1 vertical | 1 | Deep-dive on one disease (APS: diagnostic → clinical → survival) |

### By Clinical Theme

#### RA / Biologics Efficacy
- **comp_01** `2×2` — A:bar(DAS28 remission) + B:line(CRP dynamics) + C:box(Wk24 CRP distribution) + D:scatter(baseline vs ΔDAS28)
- **comp_05** `1×2` — A:ROC(3-model diagnostic) + B:bar(sensitivity/PPV/NPV)
- **c23** `2×3` — A:bar(ACR50) + B:bar(DAS28 remission) + C:box(ΔDAS28 distribution) + D:scatter(CRP vs response) + E:KM(drug retention) + F:stacked_bar(SAE distribution)

#### GCA / PMR
- **comp_02** `1×2` — A:KM(relapse-free) + B:forest(pooled HR)
- **c17** `2×2` — A:stacked_bar(symptom spectrum) + B:box(ESR) + C:KM(relapse-free) + D:bar(GC taper success)

#### SLE / Lupus Nephritis
- **comp_03** `1×3` — A:violin(dsDNA by activity) + B:bar(organ response) + C:scatter(complement vs SLEDAI)
- **c10** `1×2` — A:stacked_bar(renal response by ISN/RPS class) + B:dual_axis(proteinuria + C3 dynamics)

#### AAV / Vasculitis
- **comp_06** `1×3` — A:hbar(ANCA specificity) + B:box(BVAS) + C:line(BVAS reduction)
- **comp_08** `1×3` — A:hbar(study quality NOS) + B:forest(individual HR) + C:bar(subgroup analysis)
- **c18** `1×2` — A:forest(7 prognostic factors HR) + B:ROC(FVSG+BVAS 1yr mortality prediction)

#### sJIA / Pediatric
- **comp_07** `1×2` — A:dual_axis(IL-6 + ferritin dynamics) + B:KM(time to ACR-Pedi50)
- **c13** `2×3` — A:bar(ACR-Pedi70) + B:box(ΔJADAS27) + C:line(active joints) + D:violin(baseline CRP) + E:scatter(duration vs JADAS) + F:bar(erosion rate)

#### IgA Nephropathy
- **c09** `2×2` — A:box(baseline proteinuria) + B:scatter(eGFR vs UACR) + C:bar(remission rate) + D:KM(50% eGFR decline-free)

#### TAK (Takayasu Arteritis)
- **c11** `1×3` — A:box(vessel wall thickness change) + B:bar(PET-CT response) + C:line(ESR+CRP dynamics)

#### APS (Antiphospholipid Syndrome)
- **c12** `3×1` — A:ROC(aCL/anti-β2GP1/LA diagnostic) + B:bar(thrombotic events by antibody profile) + C:KM(thrombosis-free survival)

#### Behçet's Disease
- **c14** `1×2` — A:hbar(manifestations by region: Turkey/Japan/China) + B:forest(treatment Meta-analysis OR)

#### Sjögren's (pSS)
- **c15** `2×2` — A:heatmap(autoantibody correlation) + B:bar(salivary flow rate) + C:scatter(focus score vs ESSDAI) + D:violin(IgG by subtype)

#### AIH (Autoimmune Hepatitis)
- **c16** `1×3` — A:bar(biochemical response AIH-1/2/overlap) + B:dual_axis(ALT + albumin) + C:KM(transplant-free survival)

#### SSc (Systemic Sclerosis)
- **c19** `2×2` — A:bar(ΔFVC by subtype) + B:violin(ΔmRSS) + C:line(mRSS trajectory) + D:KM(SSc-ILD survival)

#### AOSD (Adult-onset Still's)
- **c20** `1×4` — A:bar(systemic manifestations) → B:box(ferritin) → C:dual_axis(ferritin + CRP) → D:KM(remission maintenance)

#### ANCA Testing Performance
- **c21** `1×3` — A:hbar(sensitivity/specificity by assay) + B:ROC(combined vs IIF alone) + C:bar(inter-assay κ agreement)

#### Mastocytosis
- **c22** `1×2` — A:bar(symptom control rate 5 domains) + B:line(serum tryptase dynamics)

## Design Tips

- **Consistent theme** across all panels (use same `--theme`)
- **Panel titles** should be descriptive but concise (≤15 words)
- **Axis labels** can be shared if panels have same Y-axis
- **Legend placement**: set `legend: false` on inner panels, keep on outer panel only
- **Sizing**: 2×2 panels benefit from `--width 12 --height 10`; 1×3 from `--width 14 --height 5`
- **3×1 vertical** is rare but effective for deep single-disease figures (APS pattern)

## Data Source Guidelines

All demo figures use real published clinical data:
- GiACTA (NEJM 2017, Stone et al.) — GCA/TCZ trial
- BLISS-52/76 — belimumab SLE trials
- ADACTA — TCZ vs ADA RA monotherapy
- Nishimura 2007 — Anti-CCP2 diagnostic performance
- Polish AAV Registry (Susol et al. 2020) — AAV organ involvement

## 反冗余审计（多面板动笔前先过这一节）

组合图的每一面板必须回答**唯一问题**。三层正交递进，每层只编码一个维度：

| 层 | 回答的问题 | 典型编码 |
|---|---|---|
| Overview（总体） | 整体模式是什么 | 堆叠柱/构成比/总计数 |
| Deviation（偏离） | 各组独特点是什么 | Z-score 热图/背离色/倍数变化 |
| Relationship（共变） | 变量间如何共变 | 散点/相关矩阵/网络边权 |

**5 个常见冗余陷阱**（命中即重构）：

1. 绝对值 + 绝对值并排 → 第二面板改画偏差（差值/倍数）
2. 父集 + 子集两面板 → 改一张散点（子集点叠在父集分布上）
3. 两个排序视角展示同一组数 → 合并成一张火山式图（x=效应 y=显著性）
4. 同数据换视觉（饼图 + 堆叠柱各来一张）→ 二选一
5. 两个高相关轴（r≥0.9 的两张散点）→ 留一张散点 + 相关矩阵一格

**排版前 4 问**：同数据？→ 并。同问题？→ 重构。可互相推导？→ 删导出方。删掉后结论不削弱？→ 删。
**判据**：3 个信息致密不冗余的面板 > 6 个面板里 3 个在复读。

## 主面板（Hero Panel）规格

多面板叙事需要视觉锚点时，指定一个主面板承接核心结论：

- **面积**：主面板 = 1.2–1.5× 单个辅面板面积（引擎实现取 1.35:1 双列）；
- **位置**：左上或居中（左上=阅读动线起点，居中=强调对称）；
- **色彩**：全图最高饱和的强调色**只允许出现在主面板**（辅面板一律降饱和/中性）；
- **内容**：主面板必须承载 3 秒结论——读者只看它也能复述核心发现。

引擎支持随 v7.8.0 引擎批启用：composite 面板 JSON 增 `hero_panel: <面板序号>` 字段——
启用 1.35:1 双列布局（`width_ratios=[1.35, 1.0]`）且主面板列纵向跨全部行，辅面板右列纵排；
支持 3–6 面板，>6 面板打 WARNING 回退均等网格。与既有 span/overlap 机制的优先级关系见该版 changelog。

## 叙事排序 5 规则 + 出口检查

1. **数据先于示意图**——示意/模型图放 (a) 等于自报"这是推测"；数据面板开路，机制示意收尾；
2. 发现先于验证——先给主发现，再给稳健性/验证面板；
3. 简单先于复杂——读者逐面板建立视觉素养后再进高密度面板；
4. 共享轴面板相邻——同 y 轴的系列放一起，减少视线往返；
5. 自洽分组——上排=发现组，下排=验证组，组间留白/分隔线明示。

**出口检查**：只读面板标签，每格扫 2 秒——能复述该格主信息吗？有一个格子不能→重排或删格。

Always use real data ranges from published studies, not arbitrary numbers.
