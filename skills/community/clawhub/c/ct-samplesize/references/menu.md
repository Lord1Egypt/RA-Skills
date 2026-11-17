# ct-samplesize — Test Menu (Navigation Aid)

> **What this file is:** the authoritative map of all 65 `--test` types. The agent reads it
> to help a user **pick the right test** when they need to choose. It is a *navigation aid*, not
> a strict taxonomy — the same test may appear under several headings on purpose.
>
> **Triage gate (SKILL.md 4-level) — read before opening this menu:**
> - **Simple** (the user already named a specific test, e.g. "two-sample t-test") → compute directly, **do not show this menu**.
> - **Middle** (single-point but deep — ICH guidance detail, statistical parameter, compliance gray zone) → same path as Simple: answer **directly, no menu**, with a richer multi-point answer.
> - **Vague** (the user is unsure what test to use, e.g. "help me figure out the sample size") → enter **bounded grill-me** branch-by-branch probing (**hard cap 3 rounds**, accumulate a question profile, then echo a needs-portrait + recommended test summary); **do not dump this menu**. Clarify the endpoint type, design and goal first, then compute. 注：此 3-round cap 针对「Vague 深挖锁定 test」；参数缺失澄清的全局上限另为 2 轮（AGENTS.md §6.1），不冲突。
> - **Complex** (the user knows the design but hesitates between test types / design families) → use this menu **two-level**: first the level-1 categories (SKILL.md Quick Menu), then this file's **Part 1** for the picked category. When they waver on a choice, offer the **③ explain-differences** option (see below) instead of deciding for them.
>
> **③ Can't decide?** → say *"explain the differences between these choices in detail"*, and I'll clarify the clinical/statistical meaning before you choose. This entry is required on every Complex routing menu — **wording must match the family standard verbatim**: 中文 `③ 还拿不准？→ 说「详细解释这些选择之间的差异」，我先讲清临床与统计含义再让你决定`.

**Total: 65 test types** — a primary tree of 7 endpoint categories, plus a design-family cross-index.

---

## Part 0 — Find your test by *research question* (start here if unsure)

You do not need to know statistical jargon. Pick the question closest to what you want to find out;
the right `--test` is on the right.

| You want to find out… | Typical design | `--test` |
|---|---|---|
| Does drug A change a **continuous** outcome (BP, HbA1c, score) more than B? | Parallel 2-group | `ttest_ind` |
| Same, but **paired / 2×2 crossover** (each subject their own control)? | Crossover / paired | `ttest_paired` |
| Is a single group's mean different from a known standard? | One-sample | `ttest_one` |
| Do **3+ groups** differ on a continuous outcome? | k-group | `anova` |
| Are two **response rates** (e.g. 20% vs 35%) different? | Parallel 2-group | `proportion_two` |
| Is a single group's rate different from a target? | One-group | `proportion_one` |
| Are two **paired** rates (before/after) different? | Paired | `proportion_paired` |
| How much **more/less likely** is an event with treatment (OR / RR)? | 2-group | `odds_ratio` / `risk_ratio` |
| Is the new treatment **not worse** than control (within a margin)? | Non-inferiority | `non_inferiority` / `ni_survival` |
| Are two treatments **equivalent** (means / HR)? | Equivalence | `equivalence` / `survival_equivalence` |
| Is a generic **bioequivalent** to the reference? | 2×2 crossover BE | `be_tost` |
| Does treatment improve **survival / delay event** (HR)? | Time-to-event | `survival` |
| How well does a **diagnostic test** discriminate (AUC)? | Diagnostic | `roc` |
| Do two measurement methods **agree** (Bland-Altman)? | Method comparison | `bland_altman` |
| How many **events / rate** differ between groups? | Count | `poisson` |
| I want **interim analyses / early stopping** built in. | Group-sequential | `group_sequential` / `gsd_survival` |
| I want the design to **adapt** mid-trial. | Adaptive | `adaptive` |
| I want a **Bayesian** design / assurance. | Bayesian | `bayesian` / `assurance` |
| I'm doing a **Phase I dose-escalation**. | Dose-finding | `dose_escalation` |
| I have **multiple arms / endpoints / clusters**. | Complex design | `mams` / `multiple_endpoints` / `cluster` |

> Any test above is reachable from the full tree in Parts 1–2. If your question isn't listed, jump to the
> endpoint category that matches your outcome type.

---

## Part 1 — Primary Tree by Endpoint Type (authoritative)

### ① Continuous
> 常见参数：`--effect`（Cohen's d，或 `--effect Δ` + `--sd`）· `--alpha` · `--power` / `--nobs` · `--side`

- `ttest_ind` — Two-means comparison (parallel)
- `ttest_paired` — Paired t / 2×2 crossover
- `ttest_one` — One-sample vs known mean
- `anova` — Multi-group (k groups)
- `equivalence` — Equivalence (means)
- `mixed_model` — Repeated measures / longitudinal
- `wilcoxon` — Wilcoxon rank-sum, two independent samples (nonparametric, Noether 1987; `--superiority` φ or `--median_diff`+`--sd`+`--shape`)
- `wilcoxon_signed_rank` — Wilcoxon signed-rank, paired/one-sample (nonparametric; same effect inputs as `wilcoxon`)

### ② Binary / Proportions
> 常见参数：`--p1`/`--p2`（率差场景）或 `--effect OR/RR` · `--margin`（非劣效/BE）· `--sup_margin`/`--p_control_sup`/`--delta_sup`（优效）· `--alpha` · `--power`

- `proportion_one` — Single-group rate
- `proportion_two` — Two-group rate (chi-square)
- `proportion_paired` — Paired rate (McNemar)
- `odds_ratio` — Odds ratio
- `risk_ratio` — Risk ratio (RR)
- `non_inferiority` — Non-inferiority (rate)
- `superiority_margin` — Superiority by margin
- `be_tost` — Bioequivalence (TOST)
- `vaccine_efficacy` — Vaccine efficacy
- `gsd_proportion` — Group-sequential two proportions

### ③ Count / Rates
> 常见参数：`--lambda1`/`--lambda2`（率）· `--t1`/`--t2`（暴露时间）· `--alpha` · `--power`

- `poisson` — Poisson rate
- `recurrent_events` — Recurrent events (Andersen-Gill)
- `gsd_poisson` — Group-sequential two Poisson rates

### ④ Survival / Time-to-event
> 常见参数：`--hazard_ratio`（或 `--median0`/`--median1` 单样本）· `--accrual_time`/`--followup_time`（可选）· `--alpha` · `--power`

- `survival` — Survival (simplified logrank)
- `survival_exact` — Survival (exact)
- `ni_survival` — Non-inferiority survival
- `survival_equivalence` — Survival equivalence (TOST log-HR)
- `survival_superiority` — Survival superiority w/ margin
- `cox_covariate` — Cox regression w/ covariate R²
- `survival_one_sample` — One-sample exponential survival
- `competing_risks` — Competing risks (cum. incidence)
- `survival_historical` — Historical-control logrank
- `gsd_survival` — Group-sequential logrank
- `gsd_hazard` — Group-sequential hazard ratio (HR)
- `gsd_survival_sim` — Group-sequential logrank — Monte-Carlo SIM
- `gsd_hazard_sim` — Group-sequential HR — Monte-Carlo SIM

### ⑤ Diagnostic / Method comparison
> 常见参数：按检验定（AUC / 灵敏度特异度 / 一致性界值等）· `--alpha` · `--power`，详见 `cli_examples.md`

- `roc` — ROC curve diagnostic trial
- `bland_altman` — Bland-Altman method comparison

### ⑥ Special / Advanced designs
> 常见参数：按设计族定——`--n_interim`/`--spending_func`/`--futility`（期中）、`--margin`/`--effect`（BE/等效）、`--icc`/`--m`/`--n_indiv`（聚类）等，详见 `cli_examples.md`

- `group_sequential` — Group sequential interim (rpact exact two-sample means)
- `adaptive` — Adaptive design
- `adaptive_simulate` — Adaptive design — Monte-Carlo SIM
- `bayesian` — Bayesian design
- `dose_escalation` — Dose escalation (Phase I)
- `mams` — Multi-arm multi-stage (MAMS)
- `dunnett` — Dunnett multiple comparison
- `win_ratio` — Win-Ratio composite endpoint
- `must_win` — Must-Win co-primary endpoints
- `historical_controls` — Historical control borrowing
- `conditional_power` — Conditional power / sample-size re-estimation
- `assurance` — Bayesian assurance
- `multiple_endpoints` — Multiple / compound endpoints
- `mediation` — Mediation effects
- `cluster` — Cluster-randomized

### ⑦ Correlation / Dispersion / Precision / Regression / Meta planning
> 常见参数：`--effect`（按测试：r / 方差比 / CV / OR / RR / SMD / 率比）· `--half_width`（CI 类目标半宽）· `--sd`·`--p0`·`--f2`·`--u_pred`·`--i2`·`--k_studies`·`--x_type`·`--q`·`--r2`·`--mu_x`·`--phi`·`--cv_cluster`·`--rate_mode`·`--alpha`·`--power`（或 `--nobs` 反向）

- `correlation` — 相关检验 H0:ρ=0（Fisher-z 精确）
- `variance_one` — 单样本方差 σ²=σ0² 检验（χ²）
- `variance_two` — 两独立方差之比 F 检验
- `cv_one` — 变异系数估计的相对误差精度
- `ci_mean` — 均值置信区间精度（半宽→n）
- `ci_prop` — 比例置信区间精度
- `ci_or` — 优势比置信区间精度
- `ci_rr` — 风险比置信区间精度
- `ci_cor` — 相关系数置信区间精度
- `ci_icc` — 组内相关系数置信区间精度
- `regression_linear` — 多重线性回归 R² 检验（Cohen's f²）
- `regression_logistic` — 逻辑回归样本量（Hsieh 1998/1989；`--x_type=continuous|binary`，`--r2` 校正）
- `regression_poisson` — 泊松回归样本量（Signorini 1991 正态 X；`--phi` 过离散，`--t1` 暴露时间）
- `cluster_ext` — 整群随机化**广义设计效应**（`--cv_cluster` 不等群；由个体 n 推簇数，或反向）
- `rates_ext` — 率扩展（`--rate_mode=ratio` 过离散率比 / `single_ci` 单率 CI / `ratio_ci` 率比 CI）
- `meta_planning` — Meta 分析前瞻效能/研究数规划（Hedges & Pigott 随机效应；smd/paired/or/rr/cor/cluster；异质性双参数 `--i2`/`--R`，cluster 支持 `--cluster_cv`；默认输出 I²∈{0,.25,.5,.75,.9} 扫描表 + K–I² 图，对标 PASS Plots）

---

## Part 2 — Design-Family Cross-Index

The same tests, regrouped by **study design** — an additional (non-exclusive) entry point for users
who think in design terms rather than endpoint type.

### Group-Sequential / Interim analysis
`group_sequential` · `gsd_proportion` · `gsd_survival` · `gsd_hazard` · `gsd_poisson` · `gsd_survival_sim` · `gsd_hazard_sim`
> Also reachable from ① (means), ② (proportions), ③ (rates), ④ (survival HR).

### Adaptive
`adaptive` · `adaptive_simulate`

### Equivalence / Non-inferiority / Superiority-margin
`equivalence` · `be_tost` · `non_inferiority` · `superiority_margin` · `ni_survival` · `survival_equivalence` · `survival_superiority`

### Bayesian
`bayesian` · `assurance`

### Dose Escalation
`dose_escalation`

### Multi-arm / Multiplicity
`mams` · `dunnett`

### Historical Control
`historical_controls` · `survival_historical`

### Vaccine
`vaccine_efficacy`

### Conditional Power / Sample-size Re-estimation
`conditional_power` · (re-estimation also in `adaptive`)

### Win Statistics
`win_ratio` · `must_win`

### Multiple / Composite Endpoints
`multiple_endpoints`

### Cluster-randomized
`cluster`

### Mediation
`mediation`

### Longitudinal / Mixed-model
`mixed_model`

### Diagnostic / Method comparison
`roc` · `bland_altman`

### Correlation / Association
`correlation` · `ci_cor`

### Variance / Dispersion
`variance_one` · `variance_two` · `cv_one`

### Confidence-Interval Precision
`ci_mean` · `ci_prop` · `ci_or` · `ci_rr` · `ci_cor` · `ci_icc`

### Regression
`regression_linear` · `regression_logistic` · `regression_poisson` · `cox_covariate`

### Cluster-randomized
`cluster` · `cluster_ext`

### Rates / Counts
`poisson` · `rates_ext`

### Meta-analysis planning
`meta_planning`

---

## How the agent should use this menu

1. **Identify the user's endpoint type** → jump to the matching primary-tree category (①–⑥).
2. If the user thinks in **design terms** (e.g. "I want a group-sequential trial"), use the **Design-Family Cross-Index** to locate the test, then confirm the endpoint.
3. The same test may appear in both views — that is intentional (non-exclusive).
4. After picking a test, see [`cli_examples.md`](cli_examples.md) for the exact CLI flags.
5. On any hesitation between choices, offer **③ explain-differences** before deciding.

---

## Conversation Examples（对话示例 · 对齐 Type-Compute 范式）

> 三个真实对话骨架，覆盖 Simple / Complex / Vague 三分支（Middle 走 Simple 同路径、答案加深）。
> 范式参照：`meta-analysis/references/interactive_menu.md`（Type-Compute 家族范式实现）。

### Example 1 · Simple：点名检验 + 参数齐 → 直接自动执行（不弹菜单）

**You say:**
> 帮我算一下两样本 t 检验的样本量：效应量 d=0.5，α=0.05，power=0.8，双侧。

**Assistant replies (sketch):**
> ✅ `ttest_ind`（双侧），每组 n ≈ 64（总 128），10% 脱落调整后每组 71。
> 完整 R 代码可随时索要。
> `## 当前分析设定： test=ttest_ind | effect(d)=0.5 | alpha=0.05 | power=0.8 | solve=n | side=two | sd=— | n=64 | ratio=1.0`

**📌 说明：** Simple 直接算，不弹菜单；末尾回显设定块供后续追问继承。

### Example 2 · Complex：卡在"非劣效 vs 优效"选型 → 能力路由菜单 + 解释差异入口

**You say:**
> 我这个三期试验是跟阳性对照比，主要终点是 6 个月 PFS 差异，但我还没想好该按非劣效设计还是优效设计。

**Assistant replies (sketch):**
> 已识别：生存终点、阳性对照。还有 1 个关键选择，我来帮你理清：
>
> **① 你倾向哪种设计假设？**
> - (a) **非劣效** — 证明新药不比对照差（预设 margin），适合"安全性/依从性更优但疗效相当"的定位（推荐，若新药无显著疗效优势预期）
> - (b) **优效** — 证明新药优于对照，需更大的样本量和更长的随访
>
> **② 还拿不准？** → 说「详细解释这些选择之间的差异」，我先讲清临床与统计含义再让你决定

**📌 说明：** 已点名能力但卡在选型时，弹**能力路由菜单**逐步确认（(a)/(b) + rationale + 推荐默认 + ③ 解释差异入口），不替用户拍板、不甩全量 65 项菜单。

### Example 3 · Vague：不确定用哪种检验 → grill-me 逐分支追问（不甩菜单）

**You say:**
> 我想算样本量，但不确定该用什么检验方法，能帮我梳理一下吗？

**Assistant replies (sketch):**
> 好的，我们先把需求理清楚，每轮问 1–3 个聚焦问题，每个带推荐默认：
>
> **第 1 轮（3 题）：**
> 1. 主要终点类型？— 连续变量(均值) / 二分类(率) / 生存(时间) / 计数(率)
> 2. 几组比较？— 两组 / 三组以上 / 单组 vs 已知标准
> 3. 有没有特殊设计？— 期中分析 / 自适应 / 非劣效 / 都没有
>
> （回答后继续追问，直到锁定检验类型 — 不会甩全量菜单）

**📌 说明：** 用户自述"不确定"时用 **grill-me 逐分支追问**理清需求，而非甩全量菜单或替用户选。
