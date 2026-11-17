# ct-samplesize Advanced Reference (for developers / debugging)

> The following is for users who need to debug, reproduce, or extend the tool. Ordinary chat users don't need it; see Sections 1-4 of README.md for daily use.

### 5.1 CLI Examples (full 65 tests)

Under the hood the skill uses `scripts/samplesize_power.py` to generate and run R code. If you want to reproduce, debug, or batch-run yourself, call the CLI directly (normal chat users don't need this step):

```bash
# === Continuous ===
python scripts/samplesize_power.py --test ttest_ind --effect 0.5 --power 0.8
python scripts/samplesize_power.py --test ttest_paired --effect 0.5 --power 0.8
python scripts/samplesize_power.py --test anova --effect 0.25 --k_groups 3 --power 0.8
python scripts/samplesize_power.py --test equivalence --margin 2.0 --effect 3.0 --power 0.8
python scripts/samplesize_power.py --test mixed_model --effect 0.5 --nsim 500

# === Binary ===
python scripts/samplesize_power.py --test proportion_two --p1 0.3 --p2 0.15 --power 0.8
python scripts/samplesize_power.py --test non_inferiority --margin 0.1 --p1 0.85 --p2 0.80 --power 0.8
python scripts/samplesize_power.py --test be_tost --theta0 0.95 --cv 0.25 --design "2x2"
python scripts/samplesize_power.py --test superiority_margin --sup_margin 0.05 --p_control_sup 0.3 --delta_sup 0.15

# === Count ===
python scripts/samplesize_power.py --test poisson --lambda1 0.05 --lambda2 0.03 --t1 2 --t2 2 --power 0.8
python scripts/samplesize_power.py --test vaccine_efficacy --ve_control 0.02 --ve_treatment 0.005 --power 0.8

# === Survival ===
python scripts/samplesize_power.py --test survival --hazard_ratio 0.75 --power 0.85
python scripts/samplesize_power.py --test survival_exact --hr_exact 0.75 --accrual_exact 12 --followup_exact 0.85
python scripts/samplesize_power.py --test ni_survival --ni_margin_surv 1.25 --accrual_time 12 --followup_time 12

# === Survival — PASS extensions (v3.5) ===
python scripts/samplesize_power.py --test survival_equivalence --eq_margin_surv 1.25 --hr_expected 1.0 --accrual_time 12 --followup_time 12 --event_rate 0.7 --power 0.8
python scripts/samplesize_power.py --test survival_superiority --sup_margin_surv 0.8 --sup_hr 0.67 --accrual_time 12 --followup_time 12 --event_rate 0.7 --power 0.8
python scripts/samplesize_power.py --test cox_covariate --cox_hr 2.0 --cox_r2 0.3 --cox_prev 0.5 --cox_event_prop 0.3 --power 0.8
python scripts/samplesize_power.py --test survival_one_sample --median0 12 --median1 18 --accrual_time 12 --followup_time 12 --power 0.8
python scripts/samplesize_power.py --test competing_risks --ci_control 0.2 --ci_treatment 0.1 --power 0.8
python scripts/samplesize_power.py --test recurrent_events --rate_control 1.0 --rate_ratio 0.6 --recur_followup 2 --power 0.8
python scripts/samplesize_power.py --test survival_historical --hist_median 12 --new_median 18 --hist_n 100 --accrual_time 12 --followup_time 12 --power 0.8

# === Diagnostic / Method Comparison ===
python scripts/samplesize_power.py --test roc --auc0 0.5 --auc1 0.75 --power 0.8
python scripts/samplesize_power.py --test bland_altman --sd_diff 5 --w 2.5

# === Special Designs ===
python scripts/samplesize_power.py --test cluster --icc 0.05 --m 30 --n_indiv 64
python scripts/samplesize_power.py --test multiple_endpoints --effect 0.3 --correlation 0.5
python scripts/samplesize_power.py --test bayesian --prob_control 0.3 --prob_treatment 0.15 --prior_a0 0.5
python scripts/samplesize_power.py --test dose_escalation --n_doses 5 --target_dlt 0.33

# === Advanced Endpoints (v3.3) ===
python scripts/samplesize_power.py --test win_ratio --win_ratio_theta 1.5 --n_sim 1000
python scripts/samplesize_power.py --test must_win --n_endpoints_must 3 --effect_must 0.3 --correlation_must 0.5
python scripts/samplesize_power.py --test historical_controls --historical_response 15 --historical_n 100 --a0_borrowing 0.5
python scripts/samplesize_power.py --test mams --n_arms_mams 3 --n_stages_mams 2 --delta_effect 0.3
python scripts/samplesize_power.py --test conditional_power --timing 0.5 --observed_effect 0.2 --planned_effect 0.3
python scripts/samplesize_power.py --test assurance --n_assurance 100 --n_sim_assurance 5000
python scripts/samplesize_power.py --test dunnett --n_groups_dunnett 3 --n_control_dunnett 50 --effect_dunnett 0.4
python scripts/samplesize_power.py --test mediation --a_path 0.3 --b_path 0.3
python scripts/samplesize_power.py --test group_sequential --n_interim 1 --effect_gs 0.4
python scripts/samplesize_power.py --test adaptive --n_stages_adapt 2 --effect_adaptive 0.4

# === Group-sequential SIMULATION (v3.7) — Monte-Carlo validation ===
python scripts/samplesize_power.py --test gsd_survival_sim --n_interim 2 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --power 0.8 --n_simulations 2000 --sim_seed 1
python scripts/samplesize_power.py --test gsd_hazard_sim --n_interim 2 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --nobs 180

# === Group-sequential (PASS, rpact-backed) — v3.6 ===
python scripts/samplesize_power.py --test gsd_proportion --n_interim 1 --p1 0.7 --p2 0.5 --power 0.8     # -> n~=75/arm
python scripts/samplesize_power.py --test gsd_survival  --n_interim 1 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --power 0.8   # -> n~=178/arm (198 events)
python scripts/samplesize_power.py --test gsd_hazard    --n_interim 1 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --power 0.8   # -> n~=178/arm
python scripts/samplesize_power.py --test gsd_poisson   --n_interim 1 --gs_rate1 0.6 --gs_rate2 1.0 --gs_poisson_time 2 --power 0.8   # -> n~=33/arm

# Spending functions + futility (all 5 GSD types share these flags)
python scripts/samplesize_power.py --test group_sequential --n_interim 2 --effect_gs 0.4 --spending_func Pocock --futility --power 0.8
python scripts/samplesize_power.py --test group_sequential --n_interim 1 --effect_gs 0.4 --spending_func WT --wt_delta 0.25 --power 0.8   # Wang-Tsiatis Δ=0.25; cannot combine with --futility

# Reverse: given n -> achieved power (self-consistent with forward n)
python scripts/samplesize_power.py --test gsd_proportion --n_interim 1 --p1 0.7 --p2 0.5 --nobs 75        # -> power~=0.80
python scripts/samplesize_power.py --test gsd_survival  --n_interim 1 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --nobs 178   # -> power~=0.82
```

### 5.2 Reverse Calculation: Power given Sample Size

By default (`--power` or omitted) the tool solves for **n** given a target power.
Pass `--nobs N` to reverse the direction: solve for **achieved power** given a fixed sample size.
`--power` and `--nobs` are mutually exclusive.

```bash
# n=50 per group → achieved power for two-sample t-test
python scripts/samplesize_power.py --test ttest_ind --effect 0.5 --nobs 50

# n=20 per sequence → achieved power for bioequivalence TOST
python scripts/samplesize_power.py --test be_tost --nobs 20

# n=100 per group → achieved power for MAMS design
python scripts/samplesize_power.py --test mams --nobs 100
```

All 65 test types support this bidirectional solving. Native reverse functions
(`pwr.*`, `PowerTOST::power.TOST`, `rpact::getPowerMeans/getPowerSurvival`) are used
where available; analytic inverse formulas cover self-written tests; precision-style
tests (`bland_altman`) report achievable CI half-width instead of power.

### 5.3 Curve Mode: Power / Sample-size Curves

Batch-plot curves to visualize the sample-size ↔ power relationship.

- `--n_seq "20,40,200"` → **Power curve** (x = sample size, y = power)
- `--n_seq "20:20:200"` → same, but auto-expanded start:step:stop
- `--power_seq "0.6:0.05:0.95"` → **Sample-size curve** (x = power, y = n)
- `--plot_effects "0.3,0.5,0.8"` → overlay multiple effect-size curves (sensitivity)
- `--out path.png` → PNG output (defaults to system temp dir)

```bash
# Power curve with 3 overlaid effect sizes
python scripts/samplesize_power.py --test ttest_ind --n_seq "20:20:200" --plot_effects "0.3,0.5,0.8" --out power_curve.png

# Sample-size curve across power 0.6–0.95
python scripts/samplesize_power.py --test ttest_ind --power_seq "0.6:0.05:0.95" --out n_curve.png
```

Supported for 9 core test types (`ttest_ind`, `ttest_paired`, `ttest_one`, `anova`,
`proportion_one`, `proportion_two`, `survival`, `equivalence`, `be_tost`) — matching
the R engine's `.curve_solvers`. Curves reuse the same validated formulas as
single-point solving. All other test types (incl. `odds_ratio`, `risk_ratio`, `roc`,
`poisson`, `non_inferiority`, `superiority_margin`, `ni_survival`, `vaccine_efficacy`,
`group_sequential`, `survival_exact`, `mams`, `dunnett`, …) support single-point
solving only; a curve request returns a clear "curve not supported" notice.

### 5.4 Core Formulas

| Scenario | Formula |
|:---|:---|
| Independent t (equal n) | $n_1 = 2(\frac{Z_{1-\alpha/2} + Z_{1-\beta}}{d})^2$ |
| Proportion (arcsin) | $n = 2(\frac{Z_{1-\alpha/2} + Z_{1-\beta}}{h})^2$ |
| Survival (Schoenfeld) | $d = \frac{(Z_{1-\alpha/2} + Z_{1-\beta})^2}{(\log HR)^2}$ |
| Survival Equivalence (TOST/log-HR) | $D = \frac{[2(Z_{1-\alpha} + Z_{1-\beta})]^2}{(\log\delta_E)^2},\ n_{pg}=\frac{D/2}{e}$ |
| Survival Superiority w/ margin | $\delta=\log\delta_S-\log HR;\ D = \frac{[2(Z_{1-\alpha} + Z_{1-\beta})]^2}{\delta^2}$ |
| Cox w/ covariate (Vittinghoff) | $d = \frac{(Z_{1-\alpha/2} + Z_{1-\beta})^2}{(1-R^2)\,p(1-p)\,(\log HR)^2}$ |
| One-sample exponential | $\lambda_j=\frac{\log2}{m_j},\ e_j=1-e^{-\lambda_j\bar t},\ n=\lceil\frac{\mu_1}{e_1}\rceil$ |
| Competing risks (CIF) | $n_{pg}=\lceil\frac{(Z_{1-\alpha/2}+Z_{1-\beta})^2[\pi_C(1-\pi_C)+\pi_T(1-\pi_T)]}{(\pi_C-\pi_T)^2}\rceil$ |
| Recurrent events (Poisson) | $n_{pg}=\lceil\frac{(Z_{1-\alpha/2}+Z_{1-\beta})^2(\lambda_1+\lambda_2)}{t(\lambda_1-\lambda_2)^2}\rceil$ |
| Historical-control logrank | single-arm vs historical median $m_H$; same one-sample exponential structure |
| ROC (Obuchowski) | $n = \frac{(Z_{1-\alpha/2} + Z_{1-\beta})^2}{4(\arcsin\sqrt{AUC_1} - \arcsin\sqrt{AUC_0})^2}$ |
| Cluster DEFF | $DEFF = 1 + (m - 1) \times ICC$ |
| Bland-Altman | $n = 2(\frac{Z_{1-\alpha/2} \times SD_{diff}}{W})^2$ |
| Win-Ratio (approx) | $n = \frac{(Z_{1-\alpha/2} + Z_{1-\beta})^2}{(\ln WR)^2 / SE_{approx}^2}$ |
| Must-Win inflation | $n = n_{single} \times [1 + (k-1)\rho \times 0.5]$ |
| MAMS (Bonferroni) | $n = \frac{(Z_{1-\alpha/(2k)} + Z_{1-\beta})^2}{\delta^2}$ |
| Assurance | $P(\text{success}) = \frac{1}{N}\sum_{i=1}^N I(\text{trial}_i \text{ significant})$ |

**Full formulas:** `references/formulas.md` | **Extended functions:** `references/extended_functions.md`

### 5.5 System Requirements

| Component | Requirement |
|:----------|:------------|
| Python | ≥ 3.8, **standard library only** — no third-party runtime deps |
| R | ≥ 4.1.0 — **server-side on coze only**; the published skill needs no local R (dev-only backend: `adapters/local-r/`) |
| OS | Windows / macOS / Linux |

R packages are **not pre-installed**; in the published skill all R runs **server-side on coze** (no local install ever needed). Note: the one-click flag `--install-all-packages` was **removed in v5.0.2**. For the optional local-R dev backend (`adapters/local-r/`, not shipped), use the printed `install.packages()` snippet instead.
**No R package needed for:** `poisson`, `cluster`, `bland_altman`, `vaccine_efficacy`, `bayesian`, `dose_escalation`, `survival` (Schoenfeld only), `must_win`, `multiple_endpoints`, `assurance`, `dunnett`, `mediation`, `win_ratio`

### 5.6 Common Errors

| Error | Fix |
|:----------|:--------|
| "Rscript not found" | Install R or specify path (dev backend only) |
| "package not found" | install.packages("xxx") (dev backend only) |
| coze unreachable | Check network/proxy; retry (serverless cold start can take >15s) |
| simr timeout | Reduce --nsim or simplify model |
| BuyseTest convergence | Increase n_sim, check prior specification |
| rpact error | Update rpact to latest version |

### 5.7 File Structure

```
ct-samplesize/
├── SKILL.md                  ← Skill definition (output in Chinese or English per OS setting; prompt can force-switch)
├── README.md                 ← This file (English)
├── README_zh-CN.md           ← Chinese version
├── ADVANCED.md               ← Advanced reference (this file)
├── ADVANCED_zh-CN.md         ← Advanced reference (Chinese)
├── AGENTS.md                 ← Self-improvement conventions (EN/ZH bilingual)
├── CHANGELOG.md              ← Version / remediation log
├── requirements.txt
├── .gitignore
├── assets/
│   ├── icon.svg              ← A-tier green logo (104×104, three-elements template)
│   ├── icon_4x.png / icon_8x.png
│   └── ct-samplesize_4x.png / ct-samplesize_8x.png
├── scripts/
│   ├── samplesize_power.py   ← CLI: 65-test calculator (coze backend; v5, stdlib only)
│   ├── compute_backend.py    ← Backend abstraction: CozeBackend (unique, no local fallback)
│   ├── i18n.py               ← EN/ZH switch helper (copied from ct-base)
│   └── office_to_md.py       ← User-uploaded docx/pptx → md (ct-base §6.7)
├── adapters/
│   ├── coze_client.py        ← Outbound coze compute client (trial-design params only)
│   ├── coze_token_embedded.py← Public credential store (XOR+base64, §5)
│   ├── bug_report.py         ← Skill bug-report client (11-key envelope, §20.3)
│   └── rendering.py          ← Figure rendering pipeline (SVG inline / PNG fallback)
└── references/
    ├── language_policy.md    ← Bilingual policy (copied from ct-base)
    ├── report_template.md    ← Report skeleton (copied from ct-base)
    ├── units.md              ← Atomic task-unit index (BASE.md §6)
    ├── menu.md               ← Authoritative layered test menu
    ├── cli_examples.md       ← Full 65-test CLI examples + bidirectional solve
    ├── operation_sop.md      ← End-to-end operation SOP + troubleshooting
    ├── data_format_guide.md  ← 65-test data format + examples
    ├── formulas.md        ← Formula derivations
    ├── extended_functions.md ← Extended function catalogue
    ├── r_packages.md      ← R package reference (20+ pkgs)
    ├── python_usage.md       ← Python quick ref
    ├── r_usage.md            ← R quick ref
    ├── effect_size.md        ← Effect size standards (d/f/h + Z table)
    ├── examples.md           ← 3 full walkthroughs (proportion / GS / non-inferiority)
    └── adaptive_simulator.md ← Adaptive Monte-Carlo simulator guide
```

### 5.8 References (R packages)

- rpact: https://www.rpact.org/
- gsDesign: https://keaven.github.io/gsDesign/
- TrialSize: https://cran.r-project.org/web/packages/TrialSize/
- PowerTOST: https://cran.r-project.org/web/packages/PowerTOST/
- simr: https://github.com/pitakakariki/simr/
- powerSurvEpi: https://cran.r-project.org/web/packages/powerSurvEpi/
- BayesCTDesign: https://cran.r-project.org/web/packages/BayesCTDesign/
- BuyseTest: https://cran.r-project.org/web/packages/BuyseTest/
- RBesT: https://cran.r-project.org/web/packages/RBesT/
- MCPAN: https://cran.r-project.org/web/packages/MCPAN/
- powerMediation: https://cran.r-project.org/web/packages/powerMediation/
- CRAN ClinicalTrials View: https://cran.r-project.org/web/views/ClinicalTrials.html


## Effect-size benchmark library: CLI entry points (moved from README 3.5/4.14, 2026-10-22 v5.13.27 spec alignment)

Show mode (never silently substitutes):

```bash
python scripts/samplesize_power.py --test ttest_ind     --effect-ref references/effect_size_benchmarks/hcc__OS.json     --ta "HCC" --endpoint "OS" --show-assumptions
```

Explicit adoption (auditable source):

```bash
python scripts/samplesize_power.py --test ttest_ind     --effect-ref references/effect_size_benchmarks/hcc__OS.json     --adopt-ref conservative --sd 10 --side two --power 0.8
```

- After adoption the source and `basis` print to stdout, are written into the assumptions block, and the reproducible R code comments cite the source.
- `--adopt-ref low|high` runs a three-point sensitivity (CI lower / median / upper); `--adopt-ref <index>` pins one single source.
- Adoptable types (`param`/`scale`): `effect` (d/MD/SMD — ttest / anova / meta_planning), `hazard_ratio` (HR — survival), `odds_ratio` (OR — ci_or / regression_logistic), `risk_ratio` (RR — ci_rr / regression_poisson / rates_ext; OR/RR land on `--effect`).
- Candidate ingestion: `adapters/ma_extractor.py --confirm candidates.json --into references/effect_size_benchmarks/<name>.json`.


## Workbench: startup & feature overview (collapsed from README section 7, 2026-10-22)

- **Online portal (no install)**: https://ct.medstatstar.com — same features and 65-test catalog as the local Workbench.
- **Local startup**: `cd workbench && python server.py 8790` (talks to the real coze R engine by default; `CTSS_COZE_MOCK=1` for the offline demo; `CTSS_BACKEND=local_r` for the local-R dev backend, dev/regression only).
- **Core features**: one-shot natural-language recognition (zero-LLM deterministic routing + LLM fallback), dynamic forms for all 65 tests, effect-size helper, curve / allocation-ratio plots, current analysis setting card, key-number cards, inline SVG figures (PNG switchable), reproducible R code, coze request-envelope preview (nothing sent), session-thread diffs (inherited / overridden / missing), multi-group comparison table, one-click single-file HTML report export, two-stage sanitized feedback.
- Consulting-style phrasing ("what does this test mean") never triggers a cloud computation — the result area shows a hint instead, so idle chatter doesn't burn compute quota.
