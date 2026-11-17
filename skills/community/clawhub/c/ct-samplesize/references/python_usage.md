# Python Implementation Reference

> **English:** Python path is the fallback when the user refuses R installation. Supports simple, fixed designs only.

---

## Quick Usage

```bash
# Two-sample t-test
python scripts/samplesize_power.py --test ttest_ind --effect 0.5 --alpha 0.05 --power 0.9

# Given n, find power
python scripts/samplesize_power.py --test ttest_ind --effect 0.5 --alpha 0.05 --nobs1 44

# One-sample / Paired t
python scripts/samplesize_power.py --test ttest_one --effect 0.625 --alpha 0.05 --power 0.9

# ANOVA (3 groups)
python scripts/samplesize_power.py --test anova --effect 0.25 --k_groups 3 --power 0.9

# Two proportions (arcsin)
python scripts/samplesize_power.py --test proportion_two --p1 0.3 --p2 0.15 --power 0.8

# Non-inferiority
python scripts/samplesize_power.py --test non_inferiority --margin 0.1 --p1 0.85 --p2 0.80

# Survival (simplified)
python scripts/samplesize_power.py --test survival --hazard_ratio 0.7 --power 0.8
```

---

## Parameters

| Parameter | Description | Applicable Tests |
|:----------|:-----------------|:------------------------|
| `--test` | Test type (required) | all |
| `--effect` | Effect size (Cohen's d or f) | ttest_one/ttest_ind/anova |
| `--alpha` | Significance level | all |
| `--power` | Desired power | all |
| `--nobs1` | Sample size (when solving for power) | ttest_one/ttest_ind |
| `--k_groups` | Number of groups | anova |
| `--p1`, `--p2` | Two rates | proportion_two/non_inferiority |
| `--margin` | Non-inferiority margin | non_inferiority |
| `--hazard_ratio` | Hazard ratio | survival |

---

## Supported Test Types

| test value | Description | Method |
|:--------------|:-----------------|:------------|
| `ttest_one` | One-sample / Paired t | statsmodels.TTestPower |
| `ttest_ind` | Two independent samples t | statsmodels.TTestIndPower |
| `anova` | One-way ANOVA | statsmodels.FTestAnovaPower |
| `proportion_one` | One-sample rate | Normal approx |
| `proportion_two` | Two-sample rate | arcsin + independent t |
| `non_inferiority` | Non-inferiority (rate) | Standard formula |
| `survival` | Survival (simplified) | Schoenfeld formula |

---

## Auto R Code Generation

**English:** The Python script is the orchestrator for the remote coze R engine. Default mode is SAFE PREVIEW — it prints the exact coze request envelope without sending. On coze, computing is fired by the natural-language trigger ("please compute directly"), **no `-y`/`--yes` needed**; the legacy `--yes` confirmation applies only to the optional local-R dev backend.

---

## Anaconda Execution

```python
import subprocess
result = subprocess.run(
    [r"%USERPROFILE%\AppData\Local\Programs\Python\313\python.exe",
     r"%USERPROFILE%\.workbuddy\skills\ct-samplesize\scripts\samplesize_power.py",
     "--test", "ttest_ind", "--effect", "0.5", "--alpha", "0.05", "--power", "0.9"],
    capture_output=True, text=True, timeout=30
)
print(result.stdout)
```

---

## Limitations

- **English:** Simple, fixed designs only; survival uses simplified Schoenfeld formula.
- **English:** Does NOT support group sequential, adaptive, or platform designs.
- **English:** For precise/complex results, R is mandatory.
