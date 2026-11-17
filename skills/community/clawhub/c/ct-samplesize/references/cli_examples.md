# Command-Line Examples

> This file collects all common CLI examples for `scripts/samplesize_power.py`, referenced by `SKILL.md`.
> By default the skill runs in SAFE PREVIEW: the exact coze request envelope is shown but NOT sent/computed. On the coze engine the natural-language trigger ("please compute directly" / 请直接计算) fires the compute — **no `--yes` needed**; the legacy `--yes`/`-y` flag applies only to the optional local-R dev backend (`adapters/local-r/`). `--show-code` displays the coze request JSON (no send); `--dry-run` is the default preview mode (envelope shown, not sent).
> Sequences support two formats: comma list `"20,40,200"` or auto-generated `"20:20:200"` (start:step:stop).

---

## Quick Menu

| Test Type | Clinical Scenario | R Package(s) |
|:---|:---|:---|

### ① Continuous
| `ttest_ind` | Two-means comparison (parallel) | `pwr`, `TrialSize` |
| `ttest_paired` | Paired t-test (2×2 crossover) | `pwr`, `TrialSize` |
| `ttest_one` | One-sample vs known mean | `pwr` |
| `anova` | Multi-group comparison (k groups) | `pwr`, `TrialSize` |
| `equivalence` | Equivalence test (means) | `TrialSize` |
| `mixed_model` | Repeated measures longitudinal | `simr` |

### ② Binary Proportions
| `proportion_one` | Single-group rate | `pwr` |
| `proportion_two` | Two-group rate (chi-square) | `pwr`, `TrialSize` |
| `proportion_paired` | Paired rate (McNemar) | `TrialSize` |
| `odds_ratio` | Odds ratio | `pwr`, `TrialSize` |
| `risk_ratio` | Risk ratio (RR) | `pwr`, `TrialSize` |
| `non_inferiority` | Non-inferiority (rate) | `TrialSize` |
| `superiority_margin` | Superiority (margin) | `TrialSize` |
| `be_tost` | Bioequivalence (TOST) | `PowerTOST` |
| `vaccine_efficacy` | Vaccine efficacy | Halloran formula |
| `gsd_proportion` | Group-sequential two proportions | `rpact` |

### ③ Count Rates
| `poisson` | Poisson rate (recurrent events) | Wald test |
| `recurrent_events` | Recurrent events (Andersen-Gill) | Poisson (base R) |
| `gsd_poisson` | Group-sequential two Poisson rates | `rpact` |

### ④ Survival Time-to-event
| `survival` | Survival (simplified) | Schoenfeld formula |
| `survival_exact` | Survival (exact) | `rpact` |
| `ni_survival` | Non-inferiority survival | `powerSurvEpi` |
| `survival_equivalence` | Survival equivalence (TOST log-HR) | closed-form (base R) |
| `survival_superiority` | Survival superiority w/ margin | closed-form (base R) |
| `cox_covariate` | Cox regression w/ covariate (R²) | Vittinghoff (base R) |
| `survival_one_sample` | One-sample exponential survival | closed-form (base R) |
| `competing_risks` | Competing risks (cum. incidence) | 2-sample proportion (base R) |
| `survival_historical` | Historical-control logrank | closed-form (base R) |
| `gsd_survival` | Group-sequential logrank (two survival curves) | `rpact` |
| `gsd_hazard` | Group-sequential hazard ratio (HR) | `rpact` |
| `gsd_survival_sim` | Group-sequential logrank — Monte-Carlo SIMULATION | `rpact` |
| `gsd_hazard_sim` | Group-sequential hazard ratio — Monte-Carlo SIMULATION | `rpact` |

### ⑤ Diagnostic Method comparison
| `roc` | ROC curve diagnostic trial | `pROC` |
| `bland_altman` | Bland-Altman method comparison | Lu et al. formula |

### ⑥ Special Advanced designs
| `group_sequential` | Group sequential interim analysis (rpact **exact**, two-sample means) | `rpact` |
| `adaptive` | Adaptive design | `rpact` |
| `adaptive_simulate` | Adaptive design — Monte-Carlo SIMULATION | `rpact` |
| `bayesian` | Bayesian design | `BayesCTDesign` |
| `dose_escalation` | Dose escalation (Phase I) | `escalation` |
| `mams` | Multi-arm multi-stage (MAMS) | `rpact` |
| `dunnett` | Dunnett multiple comparison | Custom formula |
| `win_ratio` | Win-Ratio composite | `BuyseTest` simulation |
| `must_win` | Must-Win co-primary | Correlation method |
| `historical_controls` | Historical control borrowing | `RBesT` MAP prior |
| `conditional_power` | Conditional power SSR | `rpact` |
| `assurance` | Bayesian assurance | Monte Carlo |
| `multiple_endpoints` | Multi-endpoint composite | Correlation method |
| `mediation` | Mediation effect | `powerMediation` |
| `cluster` | Cluster randomized | DEFF formula |

### ⑦ Correlation / Variance / Precision / Regression / Meta / Rates (PASS-coverage)
| `--test` | Meaning | Engine |
|:---|:---|:---|
| `correlation` | Correlation test H0:ρ=0 | `pwr.r.test` |
| `variance_one` | One-sample variance σ²=σ0² | χ² closed form |
| `variance_two` | Two-variance ratio F test | F closed form |
| `cv_one` | Coefficient-of-variation relative error | closed form |
| `ci_mean` | CI precision for a mean | `presize::prec_mean` |
| `ci_prop` | CI precision for a proportion | `presize::prec_prop` |
| `ci_or` | CI precision for an odds ratio | `presize::prec_or` |
| `ci_rr` | CI precision for a risk ratio | `presize::prec_riskratio` |
| `ci_cor` | CI precision for a correlation | `presize::prec_cor` |
| `ci_icc` | CI precision for an ICC | `presize::prec_icc` |
| `regression_linear` | Multiple linear regression R² test | `pwr.f2.test` |
| `regression_logistic` | Logistic regression (continuous / binary X) | Hsieh 1998/1989 |
| `regression_poisson` | Poisson regression (normal X, over-dispersion) | Signorini 1991 |
| `cluster_ext` | Cluster randomized — generalized DEFF (unequal cluster sizes) | Eldridge 2006 |
| `rates_ext` | Rate / rate-ratio (over-dispersed, or CI precision) | closed form + `presize` |
| `meta_planning` | Meta-analysis prospective power / number of studies | Hedges & Pigott 2001 |

---

## Common Flags

| Flag | Meaning |
|:---|:---|
| `--test <type>` | Test type (required) |
| `--power 0.8` | Target power (forward: solve n given power) |
| `--nobs N` | Given sample size (reverse: solve power; mutually exclusive with `--power`, `--nobs` wins) |
| `--n_seq "20:20:200"` | Sample-size sequence → Power curve (x=n, y=power) |
| `--power_seq "0.6:0.05:0.95"` | Power sequence → sample-size curve (x=power, y=n) |
| `--plot_effects "0.3,0.5,0.8"` | Overlay multiple effect-size curves (sensitivity; some types) |
| `--effect_seq "0.1:0.05:0.9"` | **Effect-size as continuous X axis** → effect-axis curve; y = Power with `--nobs`/`--n_seq`, y = sample size (n) with `--power_seq`. Supported by the 9 curve tests (ttest×3 / anova / proportion×2 / survival / equivalence / be_tost). |
| `--dist_plot` | **① H0/H1 distribution-overlap plot**: standardized-effect space, two normal densities, α/β regions shaded. Supported: `ttest_ind` `ttest_paired` `ttest_one` `proportion_two` `proportion_one` `survival`. |
| `--power_time_seq "1:0.5:4"` | **③ Survival follow-up–power curve (survival only)**: x = study duration, y = power; needs `--event_rate` (per-unit hazard) + `--accrual_time` in the same time unit. Marks time-to-target-power. |
| `--heatmap` | **④ Power heatmap**: needs `--n_seq` (sample size) × `--effect_seq` (effect size); fills power over the 2-D grid. Supported by the 9 curve tests. |
| `--out path.png` | Curve PNG output path (default: system temp) |
| `-y/--yes` | Explicitly execute R code and compute (legacy local-R dev backend only; coze engine needs no `--yes` — the natural-language trigger fires the compute) |
| `--dry-run` | Show the exact coze request envelope only, nothing sent (safe preview, default) |

---

## Implementation Examples

```bash
# === Continuous ===
python scripts/samplesize_power.py --test ttest_ind --effect 0.5 --power 0.8
python scripts/samplesize_power.py --test ttest_paired --effect 0.5 --power 0.8
python scripts/samplesize_power.py --test anova --effect 0.25 --k_groups 3 --power 0.8
python scripts/samplesize_power.py --test equivalence --margin 2.0 --effect 3.0 --power 0.8

# === Binary ===
# proportion_* convention: --p1 = control/original, --p2 = experimental/new
python scripts/samplesize_power.py --test proportion_two --p1 0.15 --p2 0.30 --power 0.8
python scripts/samplesize_power.py --test proportion_two --p1 0.15 --p2 0.30 --power 0.8 --side one
python scripts/samplesize_power.py --test proportion_one --p1 0.40 --p2 0.50 --power 0.8
python scripts/samplesize_power.py --test proportion_paired --p1 0.15 --p2 0.30 --power 0.8
python scripts/samplesize_power.py --test odds_ratio --p1 0.30 --p2 0.50 --power 0.8
python scripts/samplesize_power.py --test risk_ratio --p1 0.30 --p2 0.50 --power 0.8
python scripts/samplesize_power.py --test non_inferiority --margin 0.1 --p1 0.85 --p2 0.80 --power 0.8
python scripts/samplesize_power.py --test superiority_margin --sup_margin 0.05 --p_control_sup 0.3 --delta_sup 0.15

# === Count ===
python scripts/samplesize_power.py --test poisson --lambda1 0.05 --lambda2 0.03 --t1 2 --t2 2 --power 0.8

# === Survival ===
# 2026-10-28：补 event_rate/入组/随访，否则只回所需事件数（不给样本量）
python scripts/samplesize_power.py --test survival --hazard_ratio 0.75 --event_rate 0.7 --accrual_time 12 --followup_time 12 --power 0.85

# === Survival — PASS extensions (v3.5) ===
python scripts/samplesize_power.py --test survival_equivalence --eq_margin_surv 1.25 --hr_expected 1.0 --accrual_time 12 --followup_time 12 --event_rate 0.7 --power 0.8
python scripts/samplesize_power.py --test survival_superiority --sup_margin_surv 0.8 --sup_hr 0.67 --accrual_time 12 --followup_time 12 --event_rate 0.7 --power 0.8
python scripts/samplesize_power.py --test cox_covariate --cox_hr 2.0 --cox_r2 0.3 --cox_prev 0.5 --cox_event_prop 0.3 --power 0.8
python scripts/samplesize_power.py --test survival_one_sample --median0 12 --median1 18 --accrual_time 12 --followup_time 12 --power 0.8
python scripts/samplesize_power.py --test competing_risks --ci_control 0.2 --ci_treatment 0.1 --power 0.8
python scripts/samplesize_power.py --test recurrent_events --rate_control 1.0 --rate_ratio 0.6 --recur_followup 2 --power 0.8
# 2026-10-28：参数名修正 --hist_median → --median0（原写法 argparse 直接报 unrecognized arguments）
python scripts/samplesize_power.py --test survival_historical --median0 12 --new_median 18 --hist_n 100 --accrual_time 12 --followup_time 12 --power 0.8

# === Special Designs ===
python scripts/samplesize_power.py --test cluster --icc 0.05 --m 30 --n_indiv 64
python scripts/samplesize_power.py --test group_sequential --n_interim 1 --effect_gs 0.4
# === Group-sequential (PASS, rpact-backed) — v3.6 ===
python scripts/samplesize_power.py --test gsd_proportion --n_interim 1 --p1 0.7 --p2 0.5 --power 0.8     # -> n~=75/arm
python scripts/samplesize_power.py --test gsd_survival  --n_interim 1 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --power 0.8   # -> n~=178/arm (198 events)
python scripts/samplesize_power.py --test gsd_hazard    --n_interim 1 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --power 0.8   # -> n~=178/arm
python scripts/samplesize_power.py --test gsd_survival_sim --n_interim 2 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --power 0.8 --n_simulations 2000 --sim_seed 1   # Monte-Carlo: empirical power ~0.78
python scripts/samplesize_power.py --test gsd_hazard_sim    --n_interim 2 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --nobs 180
python scripts/samplesize_power.py --test gsd_poisson   --n_interim 1 --gs_rate1 0.6 --gs_rate2 1.0 --gs_poisson_time 2 --power 0.8   # -> n~=33/arm
# Spending functions + futility (shared by 5 types)
python scripts/samplesize_power.py --test group_sequential --n_interim 2 --effect_gs 0.4 --spending_func Pocock --futility --power 0.8
python scripts/samplesize_power.py --test group_sequential --n_interim 1 --effect_gs 0.4 --spending_func WT --wt_delta 0.25 --power 0.8   # Wang-Tsiatis Delta=0.25; cannot combine with --futility
# Reverse: given n -> power (consistent with forward n)
python scripts/samplesize_power.py --test gsd_proportion --n_interim 1 --p1 0.7 --p2 0.5 --nobs 75        # -> power~=0.80
python scripts/samplesize_power.py --test gsd_survival  --n_interim 1 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --nobs 178   # -> power~=0.82
```

### ⑦ Correlation / Variance / Precision / Regression / Meta / Rates (v5.9.0 + v5.10.0)
```bash
# --- Tier 1 (v5.9.0) ---
python scripts/samplesize_power.py --test correlation     --effect 0.3 --power 0.8
python scripts/samplesize_power.py --test variance_one    --sd 1 --effect 1.5 --power 0.8
python scripts/samplesize_power.py --test variance_two    --effect 2 --power 0.8
python scripts/samplesize_power.py --test cv_one          --effect 0.2 --rel_error 0.1
python scripts/samplesize_power.py --test ci_mean         --sd 1 --half_width 0.5
python scripts/samplesize_power.py --test ci_prop         --p1 0.5 --half_width 0.1
python scripts/samplesize_power.py --test ci_or           --p0 0.3 --effect 2 --half_width 0.5
python scripts/samplesize_power.py --test ci_rr           --p0 0.3 --effect 1.5 --half_width 0.3
python scripts/samplesize_power.py --test ci_cor          --effect 0.5 --half_width 0.1
python scripts/samplesize_power.py --test ci_icc          --icc 0.3 --m 2 --half_width 0.15
python scripts/samplesize_power.py --test regression_linear --u_pred 3 --f2 0.15 --power 0.8
python scripts/samplesize_power.py --test meta_planning   --effect_type smd --effect 0.3 --n_per_study 100 --i2 0.3 --power 0.8

# --- Tier 2 (v5.10.0) ---
# Logistic regression, continuous covariate (PASS validation: P0=.5, OR=1.5 -> N=317)
python scripts/samplesize_power.py --test regression_logistic --x_type continuous --p0 0.5 --effect 1.5 --power 0.95
# Logistic regression, binary covariate (q = P(X=1))
python scripts/samplesize_power.py --test regression_logistic --x_type binary --p0 0.07 --effect 1.5 --q 0.5 --power 0.9
# Poisson regression (baseline rate=1, RR=1.3, normal X mean 3.2 sd 2.1, over-dispersion 1)
python scripts/samplesize_power.py --test regression_poisson --lambda1 1 --effect 1.3 --mu_x 3.2 --sd 2.1 --phi 1 --power 0.8
# Cluster randomized — generalized DEFF with unequal cluster sizes (CV)
python scripts/samplesize_power.py --test cluster_ext --n_indiv 100 --m 20 --icc 0.05 --cv_cluster 0.5 --ratio 1
python scripts/samplesize_power.py --test cluster_ext --nobs 20 --m 20 --icc 0.05          # reverse: clusters -> effective individual n
# Rates — over-dispersed rate ratio (phi=1 degenerates to Poisson)
python scripts/samplesize_power.py --test rates_ext --rate_mode ratio --lambda1 0.5 --lambda2 0.25 --phi 2 --power 0.8
# Rates — single-rate CI (person-time) / rate-ratio CI
python scripts/samplesize_power.py --test rates_ext --rate_mode single_ci --lambda1 0.5 --half_width 0.2
python scripts/samplesize_power.py --test rates_ext --rate_mode ratio_ci  --lambda1 0.5 --lambda2 0.25 --half_width 0.5
```

---

## Reverse Examples

```bash
# Reverse: n=50 per group → achieved power for two-sample t-test
python scripts/samplesize_power.py --test ttest_ind --effect 0.5 --nobs 50

# Reverse: n=20 per sequence → achieved power for bioequivalence TOST
python scripts/samplesize_power.py --test be_tost --nobs 20

# BE with custom equivalence limits (theta0=1, CV=30%, limits 0.5~2, power 0.8) — 2026-08-20
python scripts/samplesize_power.py --test be_tost --theta0 1 --cv 0.3 --theta1 0.5 --theta2 2 --power 0.8
# Same via --margin (margin=2 → limits 1/2 ~ 2)
python scripts/samplesize_power.py --test be_tost --theta0 1 --cv 0.3 --margin 2 --power 0.8

# Reverse: n=100 per group → achieved power for MAMS design
python scripts/samplesize_power.py --test mams --nobs 100

# Reverse: the 7 new PASS-survival tests also accept --nobs (solve power)
python scripts/samplesize_power.py --test survival_equivalence --eq_margin_surv 1.25 --hr_expected 1.0 --accrual_time 12 --followup_time 12 --event_rate 0.7 --nobs 350
```

**Covers all 67 test types.** Reverse-solve strategy:
- **Native package reverse (priority):** `pwr.*` (`pwr.t.test(n=)` auto-reverses), `PowerTOST::power.TOST(n=)`, `rpact::getPowerMeans/getPowerSurvival(n=)` — exact.
- **Analytic inverse:** self-written tests (ROC, Poisson, vaccine efficacy, multi-endpoint, Bayesian, Win Ratio, MAMS etc.) back-solve `z_b` via non-centrality, then `power = pnorm(z_b)`.
- **Approx/precision:** `bland_altman` returns achievable CI half-width (precision, not power); `dose_escalation` is heuristic design (power N/A); `conditional_power`/`assurance` `--nobs` maps directly to planned/assurance sample size.

*Note: `roc` uses `--auc1`/`--effect`; `mixed_model` uses `--effect_name`.*

---

## Curve Mode Examples

```bash
# Power curve: n = 20,40,...,200, overlaying 3 effect-size curves
python scripts/samplesize_power.py --test ttest_ind --n_seq "20:20:200" --plot_effects "0.3,0.5,0.8" --out power_curve.png

# Sample-size curve: power = 0.6,0.65,...,0.95
python scripts/samplesize_power.py --test ttest_ind --power_seq "0.6:0.05:0.95" --out n_curve.png

# Effect-axis curve (Power vs Cohen's d, fixed n=100): x = effect size, y = power
python scripts/samplesize_power.py --test ttest_ind --effect_seq "0.1:0.05:0.9" --nobs 100 --out effect_power_curve.png

# Effect-axis curve (required n vs Hazard ratio, fixed target power=0.8): x = HR, y = events
python scripts/samplesize_power.py --test survival --effect_seq "0.5:0.05:0.9" --power_seq "0.8" --out effect_n_curve.png

# ① Distribution-overlap plot (ttest_ind, d=0.5, n=100): shades α/β regions
python scripts/samplesize_power.py --test ttest_ind --nobs 100 --effect 0.5 --dist_plot --out dist_overlap.png

# ③ Survival follow-up–power curve: x = years, y = power; event_rate=0.1/yr, accrual=1yr
python scripts/samplesize_power.py --test survival --nobs 200 --hazard_ratio 0.7 \
    --event_rate 0.1 --accrual_time 1 --power_time_seq "1:0.5:4" --out surv_power_time.png

# ④ Power heatmap: n_seq (sample size) × effect_seq (Cohen's d), fill = power
python scripts/samplesize_power.py --test ttest_ind --heatmap \
    --n_seq "30:30:150" --effect_seq "0.2:0.2:1.0" --out power_heatmap.png
```

**Curve mode supports 9 core test types:** ttest_ind, ttest_paired, ttest_one, anova, proportion_one, proportion_two, survival, equivalence, be_tost.

Curve mode reuses the same validated formulas as single-point solving (pwr, PowerTOST, analytic inverse) — numerically identical.

All other test types (incl. odds_ratio, risk_ratio, roc, poisson, non_inferiority, superiority_margin, ni_survival, vaccine_efficacy, group_sequential, survival_exact, mams, dunnett, mixed_model, bayesian, win_ratio, …) support single-point solving only; a curve request returns a clear "curve not supported" notice at runtime.

---

## R Package Install

> v5: R packages run **server-side on coze** — the published skill never installs R locally. The legacy CLI flags (`--install-all-packages` / `--run-install`) were **removed in v5.0.2**. The notes below apply only to the optional local-R dev backend (`adapters/local-r/`, not shipped).

- **Install on demand (dev backend):** when the skill prints `Warning: 'xxx' package not found.`, run `install.packages("xxx")`.
- **No R package needed:** `poisson`, `cluster`, `bland_altman`, `survival` (Schoenfeld only), `vaccine_efficacy`, `bayesian`, `dose_escalation` etc.

Full R package list: `references/r_packages.md`.
