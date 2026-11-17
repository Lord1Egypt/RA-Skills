# Data Format Guide

> This guide takes the "what data do you need to prepare" angle and gives a friendly input framework for each of the 65 test types.
> Each type includes: a **parameter table to fill in** + **a real example** + **data-source hints**.

---

## 📌 General Parameters (all types)

| Param | Description | Default | Example |
|:-----|:-----|:-----|:---------|
| `α` (alpha) | Significance level, two-sided | 0.05 | 0.05 |
| `Power` | Test power | 0.8 | 0.8 / 0.85 / 0.9 |
| `--show-code` | Show the coze request JSON (no send) | SAFE PREVIEW by default: envelope shown, nothing sent | coze needs no `--yes` — natural-language trigger fires compute; `--yes` is legacy local-R dev only |

---

## Continuous

### 1. `ttest_ind` — Two-sample t-test

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|:---------|
| `--effect` | ✅ | Cohen's d (effect size) | (μ₁ - μ₂) / σ |
| `--alpha` | | 0.05 | 0.05 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test ttest_ind --effect 0.5 --power 0.8 -y
```

- Cohen's d = (Mean₁ - Mean₂) / SD_pooled
- Cohen's d benchmarks: 0.2 = small, 0.5 = medium, 0.8 = large
- d = standardized mean difference

---

### 2. `ttest_paired` — Paired t-test (2×2)

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--effect` | ✅ | Cohen's d = mean difference / SD | 0.4 |
| `--alpha` | | 0.05 | 0.05 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test ttest_paired --effect 0.4 --power 0.85 -y
```

- Paired design
- versus independent two-sample

---

### 3. `anova` — One-way ANOVA

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--effect` | ✅ | Cohen's f | 0.25 |
| `--k_groups` | | 2 | 3 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test anova --effect 0.25 --k_groups 3 --power 0.8 -y
```

Cohen's f benchmarks: 0.1 = small, 0.25 = medium, 0.4 = large

---

### 4. `equivalence` — Equivalence (TOST)

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--margin` | ✅ | δ (equivalence margin) | 2.0 |
| `--effect` | ✅ | σ (SD) | 3.0 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test equivalence --margin 2.0 --effect 3.0 --power 0.8 -y
```

---

### 5. `mixed_model` — Mixed Model (R `simr`)

| Parameter | Description |
|:-----|:-----|
| (β) | fixed effects vector |
| VarCorr | random effect variance |
| SD (σ) | residual standard deviation |
| "treatment_effect" | named effect of interest |

**CLI**

```bash
python scripts/samplesize_power.py --test mixed_model --effect 0.5 --nsim 500 -y
```

---

## Binary

### 6. `proportion_one` — One-sample proportion

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--p1` | ✅ | proportion under H1 | 0.3 |
| `--power` | | 0.8 | 0.8 |

---

### 7. `proportion_two` — Two-sample proportion

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--p1` | ✅ | treatment proportion | 0.3 |
| `--p2` | ✅ | control proportion | 0.15 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test proportion_two --p1 0.3 --p2 0.15 --power 0.8 -y
```

---

### 8. `non_inferiority` — Non-inferiority

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--p1` | ✅ | treatment proportion | 0.85 |
| `--p2` | ✅ | control proportion | 0.80 |
| `--margin` | ✅ | NI margin | 0.1 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test non_inferiority --p1 0.85 --p2 0.80 --margin 0.1 --power 0.8 -y
```

---

### 9. `superiority_margin` — Superiority by a margin

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--sup_margin` | ✅ | δ (margin) | 0.05 |
| `--p_control_sup` | ✅ | control proportion | 0.3 |
| `--delta_sup` | ✅ | target difference | 0.15 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test superiority_margin --sup_margin 0.05 --p_control_sup 0.3 --delta_sup 0.15 -y
```

---

### 10. `be_tost` — Bioequivalence (TOST)

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--theta0` | ✅ | T/R ratio, e.g. 0.95 | 0.95 |
| `--cv` | ✅ | CV, e.g. 0.25 | 0.25 |
| `--design` | | "2x2" | "2x2" |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test be_tost --theta0 0.95 --cv 0.25 --design "2x2" -y
```

Supported designs: "2x2", "2x4", "3x3", "2x2x2", "2x2x3", "2x2x4"

---

## Count

### 11. `poisson` — Poisson rate comparison

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--lambda1` | ✅ | rate group 1 | 0.05 |
| `--lambda2` | ✅ | rate group 2 | 0.03 |
| `--t1` | | 1.0 | 2.0 |
| `--t2` | | 1.0 | 2.0 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test poisson --lambda1 0.05 --lambda2 0.03 --t1 2 --t2 2 -y
```

---

### 12. `vaccine_efficacy` — Vaccine efficacy

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--ve_control` | ✅ | attack rate control (ARU) | 0.02 |
| `--ve_treatment` | ✅ | attack rate vaccine (ARV) | 0.005 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test vaccine_efficacy --ve_control 0.02 --ve_treatment 0.005 -y
```

---

## Time-to-Event (Survival)

### 13. `survival` — Survival (logrank)

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--hazard_ratio` | ✅ | hazard ratio (HR), e.g. 0.75 | 0.75 |
| `--power` | | 0.8 | 0.85 |

```bash
python scripts/samplesize_power.py --test survival --hazard_ratio 0.75 --power 0.85 -y
```

---

### 14. `survival_exact` — Survival exact

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--hr_exact` | ✅ | HR, e.g. 0.75 | 0.75 |
| `--accrual_exact` | ✅ | accrual time | 12 |
| `--followup_exact` | ✅ | follow-up time | 12 |
| `--event_rate_exact` | | 0.3 | 0.3 |
| `--dropout_exact` | | 0.05 | 0.05 |

```bash
python scripts/samplesize_power.py --test survival_exact --hr_exact 0.75 --accrual_exact 12 --followup_exact 12 -y
```

---

### 15. `ni_survival` — Non-inferiority survival

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--ni_margin_surv` | ✅ | HR margin, e.g. 1.25 | 1.25 |
| `--hr_expected` | | HR 1.0 | 1.0 |
| `--accrual_time` | | 12 | 12 |
| `--followup_time` | | 12 | 12 |
| `--event_rate` | | 0.3 | 0.3 |

```bash
python scripts/samplesize_power.py --test ni_survival --ni_margin_surv 1.25 --accrual_time 12 --followup_time 12 -y
```

---

## Diagnostic

### 16. `roc` — ROC curve

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--auc1` | ✅ | AUC under H1, e.g. 0.75 | 0.75 |
| `--auc0` | | AUC under H0 = 0.5 | 0.5 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test roc --auc0 0.5 --auc1 0.75 -y
```

---

### 17. `bland_altman` — Bland-Altman

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--sd_diff` | ✅ | SD of differences | 5 |
| `--w` | ✅ | half-width of LoA | 2.5 |
| `--alpha` | | 0.05 | 0.05 |

```bash
python scripts/samplesize_power.py --test bland_altman --sd_diff 5 --w 2.5 -y
```

---

## Special Designs

### 18. `cluster` — Cluster-randomized

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--icc` | ✅ | intraclass correlation (ICC), e.g. 0.05 | 0.05 |
| `--m` | ✅ | cluster size, e.g. 30 | 30 |
| `--n_indiv` | ✅ | individuals per cluster | 64 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test cluster --icc 0.05 --m 30 --n_indiv 64 -y
```

---

### 19. `multiple_endpoints` — Multiple endpoints

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--correlation` | ✅ | ρ (correlation) | 0.5 |
| `--effect` | ✅ | Cohen's d | 0.3 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test multiple_endpoints --effect 0.3 --correlation 0.5 -y
```

---

### 20. `bayesian` — Bayesian

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--prob_control` | ✅ | control response probability | 0.3 |
| `--prob_treatment` | ✅ | treatment response probability | 0.15 |
| `--prior_a0` | | 0.5 | 0.5 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test bayesian --prob_control 0.3 --prob_treatment 0.15 --prior_a0 0.5 -y
```

---

### 21. `dose_escalation` — Dose escalation (Phase I)

| Parameter | Description | Example |
|:-----|:-----|
| `--n_doses` | number of doses | 5 |
| `--target_dlt` | target DLT rate, e.g. 0.33 | 0.33 |

```bash
python scripts/samplesize_power.py --test dose_escalation --n_doses 5 --target_dlt 0.33 -y
```

---

## Advanced Endpoints (v3.3)

### 22. `win_ratio` — Win-Ratio

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--win_ratio_theta` | ✅ | Win-Ratio, e.g. 1.5 | 1.5 |
| `--n_sim` | | 1000 | 1000 |

```bash
python scripts/samplesize_power.py --test win_ratio --win_ratio_theta 1.5 --n_sim 1000 -y
```

---

### 23. `must_win` — Must-Win

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--n_endpoints_must` | ✅ | 2-5 (default 3) | 3 |
| `--effect_must` | ✅ | Cohen's d | 0.3 |
| `--correlation_must` | ✅ | correlation | 0.5 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test must_win --n_endpoints_must 3 --effect_must 0.3 --correlation_must 0.5 -y
```

---

### 24. `historical_controls` — Historical controls

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--historical_response` | ✅ | historical responders | 15 |
| `--historical_n` | ✅ | historical N | 100 |
| `--a0_borrowing` | | 0-1 (default 0.5) | 0.5 |
| `--p_control_current` | | 0.3 | 0.3 |
| `--prob_treatment` | ✅ | 0.15 | 0.15 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test historical_controls --historical_response 15 --historical_n 100 --a0_borrowing 0.5 --prob_treatment 0.15 -y
```

---

### 25. `mams` — Multi-Arm Multi-Stage (MAMS)

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--n_arms_mams` | ✅ | 3 | 3 |
| `--n_stages_mams` | ✅ | 2 | 2 |
| `--delta_effect` | ✅ | effect | 0.3 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test mams --n_arms_mams 3 --n_stages_mams 2 --delta_effect 0.3 -y
```

---

### 26. `conditional_power` — Conditional power / SSR

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--timing` | ✅ | 0-1 (default 0.5) | 0.5 |
| `--observed_effect` | ✅ | observed effect | 0.2 |
| `--planned_effect` | ✅ | planned effect | 0.3 |
| `--n_completed` | | 100 | 100 |
| `--n_planned` | ✅ | 200 | 200 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test conditional_power --timing 0.5 --observed_effect 0.2 --planned_effect 0.3 -y
```

---

### 27. `superiority_margin` — Binary

See section 9 (`superiority_margin`) for the binary superiority-by-a-margin parameters (`--sup_margin`, `--p_control_sup`, `--delta_sup`).

---

### 28. `assurance` — Bayesian assurance

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--shape1_trt` | ✅ | Beta α treatment, e.g. 3 | 3 |
| `--shape2_trt` | ✅ | Beta β treatment, e.g. 7 | 7 |
| `--shape1_ctrl` | ✅ | Beta α control, e.g. 3 | 3 |
| `--shape2_ctrl` | ✅ | Beta β control, e.g. 7 | 7 |
| `--n_assurance` | ✅ | 100 | 100 |
| `--n_sim_assurance` | | 5000 | 5000 |

```bash
python scripts/samplesize_power.py --test assurance --shape1_trt 3 --shape2_trt 7 --shape1_ctrl 3 --shape2_ctrl 7 --n_assurance 100 -y
```

---

### 29. `dunnett` — Dunnett

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--n_groups_dunnett` | ✅ | 3 | 3 |
| `--n_control_dunnett` | ✅ | 50 | 50 |
| `--effect_dunnett` | ✅ | Cohen's d | 0.4 |

```bash
python scripts/samplesize_power.py --test dunnett --n_groups_dunnett 3 --n_control_dunnett 50 --effect_dunnett 0.4 -y
```

---

### 30. `mediation` — Mediation

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--a_path` | ✅ | a-path effect, e.g. 0.3 | 0.3 |
| `--b_path` | ✅ | b-path effect, e.g. 0.3 | 0.3 |
| `--sigma2_m` | | 1.0 | 1.0 |
| `--sigma2_y` | | 1.0 | 1.0 |
| `--power` | | 0.8 | 0.8 |

```bash
python scripts/samplesize_power.py --test mediation --a_path 0.3 --b_path 0.3 -y
```

---

### 31. `group_sequential` — Group sequential

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--n_interim` | ✅ | 1 | 1 |
| `--effect_gs` | ✅ | Cohen's d | 0.4 |
| `--spending_func` | | "OF" "Pocock" "WT" | "OF" |

```bash
python scripts/samplesize_power.py --test group_sequential --n_interim 1 --effect_gs 0.4 -y
```

---

### 32. `adaptive` — Adaptive

| Parameter | Required | Description | Example |
|:-----|:-----|:-----|
| `--n_stages_adapt` | ✅ | 2 | 2 |
| `--effect_adaptive` | ✅ | Cohen's d | 0.4 |
| `--adaptive_type` | | "SSR" "Population" "Combination" | "SSR" |

```bash
python scripts/samplesize_power.py --test adaptive --n_stages_adapt 2 --effect_adaptive 0.4 -y
```

---

## Dropout Adjustment

Adjusted N = ceiling(N_calculated / (1 - dropout_rate))

Example: N=100 with 10% dropout → N = ceiling(100 / 0.9) = 112

---

## Quick Test Selector

```
What is your primary endpoint?
├── Continuous → ttest_ind / ttest_paired / anova / mixed_model
├── Binary → proportion_two / non_inferiority / superiority_margin
├── Survival → survival / survival_exact / ni_survival
├── Diagnostic → roc / bland_altman
├── Vaccine → vaccine_efficacy
├── Phase I dose-finding → dose_escalation
├── Complex designs → group_sequential / adaptive / mams / conditional_power
├── Multiple endpoints → must_win / multiple_endpoints
├── Bioequivalence → be_tost
└── Other → win_ratio / historical_controls / assurance / dunnett / mediation
```
