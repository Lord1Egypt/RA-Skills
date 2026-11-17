# Extended Functions Reference

> v4.0 additions: Win-Ratio, Must-Win/Co-Primary, Historical Controls, MAMS, Conditional Power/SSR, NI Survival, Superiority Margin, Assurance, Dunnett, Mediation, Survival Exact

---

## Mixed Model Power — `simr`

### Clinical Use
- Cluster-level intervention with individual outcomes

### R Code
```r
library(simr); library(lme4)
set.seed(42)

# pilot parameters
beta <- c(5.0, -0.8)        # fixed effects: intercept=5, treatment effect=-0.8
V1   <- 0.5                 # random intercept variance
sigma <- 1.0                # residual standard deviation

# data frame
n_subjects <- 20
n_treatment <- 10
df <- expand.grid(time = c(0, 3, 6, 12), subject = seq_len(n_subjects))
df$treatment <- ifelse(df$subject <= n_treatment, "active", "placebo")

# build model
model <- makeLmer(y ~ treatment * time + (1|subject),
                  fixef = beta, VarCorr = V1, sigma = sigma, data = df)

# test power
result <- powerSim(model, nsim = 1000, test = fcompare(y ~ time + (1|subject)))
print(result)

# power curve
pc <- powerCurve(model, test = fcompare(y ~ time + (1|subject)),
                 along = "subject", breaks = seq(10, 50, 10))
plot(pc)
```

### CLI
```bash
python scripts/samplesize_power.py --test mixed_model --effect 0.5 --nsim 500
```

---

## ROC Curve — `pROC`

### Clinical Use
- ROC AUC versus null 0.50 / reference 0.75

### Formula
Obuchowski AUC

$$n = \frac{(Z_{1-\alpha/2} + Z_{1-\beta})^2}{4(\arcsin\sqrt{AUC_1} - \arcsin\sqrt{AUC_0})^2}$$

### CLI
```bash
python scripts/samplesize_power.py --test roc --auc0 0.5 --auc1 0.75 --power 0.8
```

---

## Poisson Rate Comparison

### Method
- Wald approximation

### CLI
```bash
python scripts/samplesize_power.py --test poisson --lambda1 0.05 --lambda2 0.03 --t1 2 --t2 2 --power 0.8
```

---

## Cluster-Randomized Design

### Clinical Use
- Pragmatic Trial
- Stepped Wedge cluster design

### Method
$$DEFF = 1 + (m - 1) \times ICC$$

### CLI
```bash
python scripts/samplesize_power.py --test cluster --icc 0.05 --m 30 --n_indiv 64
```

---

## Bland-Altman Method Comparison

### Clinical Use
- POCT versus reference laboratory
- New method versus CT

### Formula
Lu et al. (2016) LoA

$$n = 2 \times \left(\frac{Z_{1-\alpha/2} \times SD_{diff}}{W}\right)^2$$

W = half-width of the limits of agreement (LoA)

### CLI
```bash
python scripts/samplesize_power.py --test bland_altman --sd_diff 5 --w 2.5
```

---

## Bioequivalence (TOST) — `PowerTOST`

### Clinical Use
- AUC / Cmax comparison
- Fed versus Fasted BE
- NTID BE

### R Code
```r
library(PowerTOST)
sampleN.TOST(theta0 = 0.95, CV = 0.25, design = "2x2", alpha = 0.05, targetpower = 0.8)
```

### CLI
```bash
python scripts/samplesize_power.py --test be_tost --theta0 0.95 --cv 0.25 --design "2x2"
```

---

## Vaccine Efficacy

### Method
Halloran et al. Poisson

$$VE = \frac{ARU - ARV}{ARU}$$

$$n = \frac{(Z_{1-\alpha/2} + Z_{1-\beta})^2 \times (1/ARU + 1/ARV)}{(\log(1-VE))^2}$$

### CLI
```bash
python scripts/samplesize_power.py --test vaccine_efficacy --ve_control 0.02 --ve_treatment 0.005 --power 0.8
```

---

## Multiple Endpoints

### Clinical Use
- MACE: MI + stroke composite

### Method
- $n_{adj} = n_{single} (1 - \rho)$
- rpact

### CLI
```bash
python scripts/samplesize_power.py --test multiple_endpoints --effect 0.3 --correlation 0.5
```

---

## Bayesian Design — `BayesCTDesign`

### Clinical Use
- Phase I/II design

### Method
- `BayesCTDesign::simple_sim`
- prior a0 shape parameter
- P(effect > margin | data)

### CLI
```bash
python scripts/samplesize_power.py --test bayesian --prob_control 0.3 --prob_treatment 0.15 --prior_a0 0.5
```

---

## Dose Escalation — `escalation`

### Clinical Use
- Phase I
- BOIN / CRM / mTPI

### 3+3
|DLT|
|:-------|:-----|
|0/3|
|1/3|3|
|1/6|
|≥2/6|MTD|

### CLI
```bash
python scripts/samplesize_power.py --test dose_escalation --n_doses 5 --target_dlt 0.33
```

---

## Win-Ratio Composite Endpoint — `BuyseTest`

### Clinical Use
- PFS + death composite

### Method
- BuyseTest win-ratio
- Win-Ratio = priority-ranked pairwise comparisons
- log(WR) standard error

### Formula (approx)
$$n = \frac{(Z_{1-\alpha/2} + Z_{1-\beta})^2}{(\ln WR)^2 / SE_{approx}^2}$$

### CLI
```bash
python scripts/samplesize_power.py --test win_ratio --win_ratio_theta 1.5 --n_sim 1000
```

---

## Must-Win (Co-Primary)

### Clinical Use
- FDA/EMA co-primary endpoints

### Method
- k endpoints, correlation $\rho$
- sample size per endpoint $n$
- inflation factor $= 1 + (k-1) \times \rho \times 0.5$

### CLI
```bash
python scripts/samplesize_power.py --test must_win --n_endpoints_must 3 --effect_must 0.3 --correlation_must 0.5
```

---

## Historical Controls — `RBesT` MAP

### Method
- **MAP (Maximal A Posteriori)** Beta mixture
- **ESS (Effective Sample Size)**
- $N_{borrow} = N_{fixed} \times \frac{1}{1 + ESS_{hist}/N_{fixed}}$

### CLI
```bash
python scripts/samplesize_power.py --test historical_controls --historical_response 15 --historical_n 100 --a0_borrowing 0.5
```

---

## MAMS — `rpact`

### Method
- O'Brien-Fleming boundaries
- Bonferroni adjustment for k comparisons

### CLI
```bash
python scripts/samplesize_power.py --test mams --n_arms_mams 3 --n_stages_mams 2 --delta_effect 0.3
```

---

## Conditional Power & SSR — `rpact`

### Clinical Use
- Sample Size Reassessment (SSR)

### Method
- conditional power formula
- $SSR = (planned\_effect / observed\_effect)^2$
- information fraction

### CLI
```bash
python scripts/samplesize_power.py --test conditional_power --timing 0.5 --observed_effect 0.2 --planned_effect 0.3
```

---

## Non-Inferiority Survival — `powerSurvEpi`

### Clinical Use
- HR < 1.25 (non-inferiority margin)

### Method
- `powerSurvEpi::powerAnsi`

### CLI
```bash
python scripts/samplesize_power.py --test ni_survival --ni_margin_surv 1.25 --accrual_time 12 --followup_time 12
```

---

## Superiority by a Margin

### Clinical Use
- Superiority if difference > $\delta$

### Method
- $H_0: p_T - p_C \leq \delta$ vs $H_1: p_T - p_C > \delta$
- $p_T - p_C - \delta$

### CLI
```bash
python scripts/samplesize_power.py --test superiority_margin --sup_margin 0.05 --p_control_sup 0.3 --delta_sup 0.15
```

---

## Bayesian Assurance — Monte Carlo

### Clinical Use
- Target assurance 80%

### Method
- Monte Carlo simulation
- Assurance = P(power > target | data)

### CLI
```bash
python scripts/samplesize_power.py --test assurance --n_assurance 100 --n_sim_assurance 5000
```

---

## Dunnett Comparisons — `MCPAN`

### Clinical Use
- Multiple treatments versus control

### Method
- Dunnett $d_{crit} \approx Z_{1-\alpha/2} + 0.5 \ln(k)$
- Bonferroni when k > 10

### CLI
```bash
python scripts/samplesize_power.py --test dunnett --n_groups_dunnett 3 --n_control_dunnett 50 --effect_dunnett 0.4
```

---

## Mediation Effects — `powerMediation`

### Method
- **Sobel test** = a × b (a-path, b-path)
- **Monte Carlo** method
- `powerMediation::power.powerMediation.v2`

### CLI
```bash
python scripts/samplesize_power.py --test mediation --a_path 0.3 --b_path 0.3
```

---

## Group Sequential Design — `rpact` (upgraded from `gsDesign` in v3.6)

### Method
- **O'Brien-Fleming (OF)**
- **Pocock**
- **Alpha spending function**
- $N_{gs} = N_{fixed} \times IF$

### CLI
```bash
python scripts/samplesize_power.py --test group_sequential --n_interim 1 --effect_gs 0.4
```

---

## Group-Sequential Two Proportions — `rpact`

### Clinical Use
- difference / ratio / odds-ratio

### Method
- `rpact::getSampleSizeRates` (n) / `getPowerRates` (power)
- `getDesignGroupSequential(kMax, typeOfDesign, ...)`
- AE: `directionUpper = FALSE` (lower is better) / `TRUE`
- `--power` to solve n; `--nobs` to solve power

### CLI
```bash
# difference mode (default): --p1 = treatment, --p2 = control
python scripts/samplesize_power.py --test gsd_proportion --n_interim 1 --p1 0.7 --p2 0.5 --power 0.8   # -> n~=75/arm
# ratio mode: treatment rate = control rate x ratio
python scripts/samplesize_power.py --test gsd_proportion --n_interim 1 --p1 0.7 --gs_proportion_metric ratio --gs_ratio 0.8 --power 0.8
# OR mode
python scripts/samplesize_power.py --test gsd_proportion --n_interim 1 --p1 0.7 --gs_proportion_metric or --gs_or 0.5 --power 0.8
# reverse: given n, solve power
python scripts/samplesize_power.py --test gsd_proportion --n_interim 1 --p1 0.7 --p2 0.5 --nobs 75      # -> power~=0.80
```

---

## Group-Sequential Survival (logrank) — `rpact`

### Clinical Use
- logrank

### Method
- `rpact::getSampleSizeSurvival` / `getPowerSurvival`; `followUpTime`, `maxNumberOfEvents`, `accrualIntensity`
- `--gs_median_control` ($\lambda_2$), `--hazard_ratio`
- HR < 1: `directionUpper = FALSE` (lower is better) / `TRUE`
- `events ≈ n·[(1−e^{−λ₂·expo}) + (1−e^{−λ₁·expo})]`, expo = accrual / 2

### CLI
```bash
python scripts/samplesize_power.py --test gsd_survival --n_interim 1 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --power 0.8   # -> n~=178/arm, 198 events
python scripts/samplesize_power.py --test gsd_survival --n_interim 1 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --nobs 178      # -> power~=0.82
```

---

## Group-Sequential Hazard Ratio — `rpact`

### Clinical Use
- `gsd_survival` (HR)
- HR

### Method
- `gsd_survival`; env `R_GSD_SURVIVAL`, `R_GSD_HAZARD`; header `surv_header`

### CLI
```bash
python scripts/samplesize_power.py --test gsd_hazard --n_interim 1 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --power 0.8   # -> n~=178/arm
```

---

## Group-Sequential Survival/Hazard — Monte-Carlo Simulation — `rpact`

### Clinical Use
- PASS Group-Sequential "Logrank Tests (Simulation)"

### Method
- `rpact::getSimulationSurvival` for `gsd_survival`/`gsd_hazard`; `getDesignGroupSequential`; `--spending_func`, `--futility`, `directionUpper`
- rpact `maxNumberOfEvents`; `longTimeSimulationAllowed = TRUE`
- `maxNumberOfSubjects`; rpact `accrualTime × accrualIntensity` API
- `futilityStops` = kMax - 1 (futility stop)
- `adaptive_simulate`; `--n_simulations` → `maxNumberOfIterations` (10000); `--sim_seed` → `seed`
- `--nobs` to target power (n, events)

### CLI
```bash
# default (analytic n + events, then simulate to verify), kMax=3, O-F
python scripts/samplesize_power.py --test gsd_survival_sim --n_interim 2 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --power 0.8 --n_simulations 2000 --sim_seed 1   # -> n=180/arm, empirical power ~0.78
# fixed n simulation (too-small n yields low empirical power)
python scripts/samplesize_power.py --test gsd_hazard_sim --n_interim 2 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --nobs 180
```

---

## Poisson Group-Sequential Two Poisson Rates — `rpact`

### Method
- `rpact::getSampleSizeCounts` / `getPowerCounts`
- $\lambda_1$ = `--gs_rate1`, $\lambda_2$ = `--gs_rate2`, `--gs_poisson_time`
- $\lambda_1 < \lambda_2$: `directionUpper = FALSE` (lower is better) / `TRUE`

### CLI
```bash
python scripts/samplesize_power.py --test gsd_poisson --n_interim 1 --gs_rate1 0.6 --gs_rate2 1.0 --gs_poisson_time 2 --power 0.8   # -> n~=33/arm
python scripts/samplesize_power.py --test gsd_poisson --n_interim 1 --gs_rate1 0.6 --gs_rate2 1.0 --gs_poisson_time 2 --nobs 33      # -> power~=0.81
```

---

## Group-Sequential Spending Functions

- Spending functions: `--spending_func` OF (O'Brien-Fleming), Pocock, WT (Wang-Tsiatis), HSD (Hwang-Shih-DeCani, $\gamma$ via `--rho`), Kim-DeMets (asOF, $\gamma$ via `--rho`)
- Futility: `--futility`, `bindingFutility = FALSE`; beta spending `bsOF`; aliases `as*` `asOF`/`asP`/`asHSD`/`asKD` for OF/P/WT futility
- WT: `WT`, `--wt_delta` (default 0.25); WT with `--futility`; rpact `asWT`
- Direction: HR<1, rate1<rate2, `effect_gs`, p1<p2 → `directionUpper = FALSE` (lower is better); otherwise `TRUE`. Mis-set direction yields power=0

---

## Adaptive Design — `rpact`

### Clinical Use
- Sample Size Reassessment (SSR)
- Population Enrichment
- Combination Test

### Method
- rpact
- information fraction

### CLI
```bash
python scripts/samplesize_power.py --test adaptive --n_stages_adapt 2 --effect_adaptive 0.4
```

---

## Survival Exact — `rpact`

### Clinical Use
- ICH E9 (R1)

### Method
- `rpact::getSampleSizeSurvival`

### CLI
```bash
python scripts/samplesize_power.py --test survival_exact --hr_exact 0.75 --accrual_exact 12 --followup_exact 12
```

---

## Survival Equivalence (TOST) — closed-form (base R)

### Clinical Use
- HR equivalence margin $\delta_E$ (80–125%)

### Method
- TOST on log-HR: $D = \frac{[2(Z_{1-\alpha} + Z_{1-\beta})]^2}{(\log \delta_E)^2}$
- $n_{pg} = \frac{D/2}{e}$, e = event_rate

### CLI
```bash
python scripts/samplesize_power.py --test survival_equivalence --eq_margin_surv 1.25 --hr_expected 1.0 --accrual_time 12 --followup_time 12 --event_rate 0.7 --power 0.8
```

---

## Survival Superiority with Margin — closed-form (base R)

### Clinical Use
- $\delta_S$ HR margin, $\delta_S < 1$

### Method
- $\delta = \log\delta_S - \log(HR)$, $D = \frac{[2(Z_{1-\alpha} + Z_{1-\beta})]^2}{\delta^2}$
- $HR \ge \delta_S$

### CLI
```bash
python scripts/samplesize_power.py --test survival_superiority --sup_margin_surv 0.8 --sup_hr 0.67 --accrual_time 12 --followup_time 12 --event_rate 0.7 --power 0.8
```

---

## Cox Regression w/ Covariate R² (Vittinghoff) — base R

### Clinical Use
- Cox model with covariate R²
- Cox regression

### Method
- Vittinghoff & McCulloch (2007): $d = \frac{(Z_{1-\alpha/2} + Z_{1-\beta})^2}{(1-R^2)\,p(1-p)\,(\log HR)^2}$
- p = event proportion $\in (0,1)$, $R^2\in[0,1)$

### CLI
```bash
python scripts/samplesize_power.py --test cox_covariate --cox_hr 2.0 --cox_r2 0.3 --cox_prev 0.5 --cox_event_prop 0.3 --power 0.8
```

---

## One-Sample Exponential Survival — base R

### Method
- $\lambda_j = \log2 / m_j$, $e_j = 1 - e^{-\lambda_j\bar t}$, $\bar t =$ (accrual + followup)/2
- $r = e_0/e_1$, $n = \lceil \mu_1/e_1\rceil$, $\mu_1 = \big(\frac{Z_{1-\alpha}\sqrt r + Z_{1-\beta}}{r-1}\big)^2$

### CLI
```bash
python scripts/samplesize_power.py --test survival_one_sample --median0 12 --median1 18 --accrual_time 12 --followup_time 12 --power 0.8
```

---

## Competing Risks (Cumulative Incidence) — 2-sample proportion (base R)

### Clinical Use
- Cumulative Incidence Function (CIF)
- log-rank

### Method
- $n_{pg} = \left\lceil\frac{(Z_{1-\alpha/2}+Z_{1-\beta})^2[\pi_C(1-\pi_C)+\pi_T(1-\pi_T)]}{(\pi_C-\pi_T)^2}\right\rceil$

### CLI
```bash
python scripts/samplesize_power.py --test competing_risks --ci_control 0.2 --ci_treatment 0.1 --power 0.8
```

---

## Recurrent Events (Andersen-Gill, Poisson) — base R

### Clinical Use
- rate ratio

### Method
- Poisson: $n_{pg} = \left\lceil\frac{(Z_{1-\alpha/2}+Z_{1-\beta})^2(\lambda_1+\lambda_2)}{t\,(\lambda_1-\lambda_2)^2}\right\rceil$, $\lambda_1 = RR\cdot\lambda_2$

### CLI
```bash
python scripts/samplesize_power.py --test recurrent_events --rate_control 1.0 --rate_ratio 0.6 --recur_followup 2 --power 0.8
```

---

## Logrank Historical-Control Logrank — base R

### Clinical Use
- versus historical control

### Method
- $m_H$ (historical median), $m_N$ (new median)
- $n = \lceil \mu_1/e_N\rceil$, hist_n

### CLI
```bash
python scripts/samplesize_power.py --test survival_historical --hist_median 12 --new_median 18 --hist_n 100 --accrual_time 12 --followup_time 12 --power 0.8
```

---

## Full Command Matrix

| Test Type | CLI Flag | Required Params |
|:----------|:---------|:----------------|
| Two-sample t-test | `--test ttest_ind` | `--effect` |
| Paired t-test | `--test ttest_paired` | `--effect` |
| ANOVA | `--test anova` | `--effect`, `--k_groups` |
| One proportion | `--test proportion_one` | `--p1` |
| Two proportions | `--test proportion_two` | `--p1`, `--p2` |
| Non-inferiority | `--test non_inferiority` | `--p1`, `--p2`, `--margin` |
| **Mixed Model** | `--test mixed_model` | `--effect` |
| **ROC** | `--test roc` | `--auc1` |
| **Poisson** | `--test poisson` | `--lambda1`, `--lambda2` |
| **Cluster Randomized** | `--test cluster` | `--icc`, `--m`, `--n_indiv` |
| **Bland-Altman** | `--test bland_altman` | `--sd_diff`, `--w` |
| **Bioequivalence** | `--test be_tost` | `--theta0`, `--cv` |
| Equivalence | `--test equivalence` | `--margin` |
| Survival | `--test survival` | `--hazard_ratio` |
| **Survival Exact** | `--test survival_exact` | `--hr_exact` |
| **NI Survival** | `--test ni_survival` | `--ni_margin_surv` |
| **Vaccine Efficacy** | `--test vaccine_efficacy` | `--ve_control`, `--ve_treatment` |
| **Multiple Endpoints** | `--test multiple_endpoints` | `--effect`, `--correlation` |
| **Bayesian** | `--test bayesian` | `--prob_control`, `--prob_treatment` |
| **Dose Escalation** | `--test dose_escalation` | `--n_doses`, `--target_dlt` |
| **Win-Ratio** | `--test win_ratio` | `--win_ratio_theta` |
| **Must-Win** | `--test must_win` | `--n_endpoints_must` |
| **Historical Controls** | `--test historical_controls` | `--historical_response`, `--historical_n` |
| **MAMS** | `--test mams` | `--n_arms_mams` |
| **Conditional Power** | `--test conditional_power` | `--observed_effect` |
| **Superiority Margin** | `--test superiority_margin` | `--sup_margin` |
| **Assurance** | `--test assurance` | `--n_assurance` |
| **Dunnett** | `--test dunnett` | `--n_groups_dunnett` |
| **Mediation** | `--test mediation` | `--a_path`, `--b_path` |
| **Group Sequential** | `--test group_sequential` | `--n_interim` |
| **GSD Two Proportions** | `--test gsd_proportion` | `--p1`, `--p2` (or `--gs_proportion_metric` + `--gs_ratio` / `--gs_or`), `--n_interim` |
| **GSD Survival (logrank)** | `--test gsd_survival` | `--gs_median_control`, `--hazard_ratio`, `--n_interim` |
| **GSD Hazard Ratio** | `--test gsd_hazard` | `--gs_median_control`, `--hazard_ratio`, `--n_interim` |
| **GSD Survival Sim** | `--test gsd_survival_sim` | `--gs_median_control`, `--hazard_ratio`, `--n_interim`, `--n_simulations`, `--sim_seed` |
| **GSD Hazard Sim** | `--test gsd_hazard_sim` | `--gs_median_control`, `--hazard_ratio`, `--n_interim`, `--n_simulations`, `--sim_seed` |
| **GSD Two Poisson** | `--test gsd_poisson` | `--gs_rate1`, `--gs_rate2`, `--gs_poisson_time`, `--n_interim` |
| **Adaptive** | `--test adaptive` | `--n_stages_adapt` |
| **Survival Equivalence** | `--test survival_equivalence` | `--eq_margin_surv`, `--hr_expected` |
| **Survival Superiority** | `--test survival_superiority` | `--sup_margin_surv`, `--sup_hr` |
| **Cox w/ Covariate** | `--test cox_covariate` | `--cox_hr`, `--cox_r2`, `--cox_prev`, `--cox_event_prop` |
| **One-Sample Survival** | `--test survival_one_sample` | `--median0`, `--median1` |
| **Competing Risks** | `--test competing_risks` | `--ci_control`, `--ci_treatment` |
| **Recurrent Events** | `--test recurrent_events` | `--rate_control`, `--rate_ratio`, `--recur_followup` |
| **Historical-Control Logrank** | `--test survival_historical` | `--hist_median`, `--new_median`, `--hist_n` |

---

## References

- Green P, MacLeod CJ. SIMR: an R package for power analysis of generalized linear mixed models by simulation. Methods in Ecology and Evolution, 2016.
- Obuchowski NA, et al. Sample size requirements for studies of diagnostic tests. Radiology, 1998.
- Lu MJ et al. Sample size for assessing agreement between two instruments. Statistical Methods in Medical Research, 2016.
- Halloran ME, et al. Exposure Efficacy and Change in Rate of Infection with and without a Vaccine. Epidemiology, 1991.
- Labes D, Schütz H, Lang B. PowerTOST: Power and Sample Size for (Bio)Equivalence Studies. CRAN.
- Patterson SD, Jones B. Bioequivalence and Statistics in Clinical Trials. CRC Press.
- Eggleston B et al. BayesCTDesign: Bayesian Clinical Trial Design with Historical Control Data. CRAN.
- Sabanés Bové D et al. crmPack: Model-Based Dose Escalation Designs in R. JSS, 2019.
- Pahl R et al. BuyseTest: A package to compute the Win Ratio. CRAN.
- Wassmer G, Pahlke F. rpact: Confirmatory Adaptive Clinical Trial Design and Analysis. CRAN.
- Wassmer G, Brannath W. Group Sequential and Confirmatory Adaptive Designs in Clinical Trials. Springer.
- Bulus M et al. MCPAN: Multiple Comparisons Using Normal Approximations. CRAN.
- Qiu W et al. powerMediation: Power/Sample Size for Mediation Effects. CRAN.
- Serdar CC et al. RBesT: R Bayesian Evidence Synthesis Tools. CRAN.
- Green SB, et al. Proceedings of the International Society for Clinical Biostatistics. 2023.
