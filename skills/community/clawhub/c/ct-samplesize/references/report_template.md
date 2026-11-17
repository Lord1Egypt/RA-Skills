# Report Template

> **🌐 Output language (configurable, opt-in):**
> Output language follows the user's stated preference and is **not mandated**.
> - Default recommendation: bilingual output (English + Chinese, both shown side by side), since this skill is published bilingually.
> - Single-language output (English-only or Chinese-only) is fully supported — just set the user's requested language.
> - In regulated clinical workflows where output language must be tightly controlled, use the user's single requested language only.
>
> **English:** By default, end every analysis with this structure + results; include the standalone R code block ONLY when the user explicitly asks for it.

---

## Structure

### 1. Title
```
## 📊 Sample Size / Power Report
```

### 2. Trial Design
```
- **Design Type**: [Parallel/Crossover/Group Sequential/Adaptive]
- **Primary Endpoint**: [Continuous/Binary/Time-to-Event]
- **Hypothesis**: [Superiority/Non-inferiority/Equivalence]
- **Direction**: [One-sided/Two-sided]
```

### 3. Input Parameters
```
- **Significance (α)**: [value, one/two-sided]
- **Power (1-β)**: [value]
- **Effect Size**: [Cohen's d / HR / OR / rate diff]
- **Allocation**: [1:1 / 2:1 / ...]
- **Dropout Rate**: [X%] → adjustment factor 1/(1-X%)
```

### 4. Results
```
- **Per-group N**: [N1, N2]
- **Total N**: [N]
- **Adjusted for Dropout**: [N_adjusted]
- **[Adaptive/GS] Interim Analyses**: [K]
- **[Survival] Events Needed**: [D]
```

### 5. Interpretation
```
[Plain-language explanation of what the sample size means]
```

### 6. Assumptions
```
[Normality, equal variance, independence, etc.]
```

### 7. Methodological Limits
```
[R exact engine (server-side coze): approximation conditions]
```

### 8. Sensitivity
```
[If effect size decreases by 20%, how does N change?]
```

---

## ⚠️ On Request: Reproducible R Code

> **Note:** Include this block ONLY when the user explicitly asks for the reproducible R code; it is hidden by default.

```markdown
---

## 📋 Reproducible R Code

> Copy to R Studio or save as `.R` and run with `Rscript` to reproduce.

```r
# ============================================================
# Sample Size Calculation — Standalone R Script
# Generated: [YYYY-MM-DD]
# Path: [R exact — engine runs server-side on coze]
# ============================================================

# ---- 0. Setup (uncomment first run) ----
# install.packages(c("TrialSize", "pwr", "rpact", "gsDesign"))

# ---- 1. Load packages ----
library(TrialSize)
library(pwr)
# library(rpact)     # Enable for Adaptive/GS
# library(gsDesign)  # Enable for Group Sequential

# ---- 2. Parameters ----
alpha <- [value]
power <- [value]
effect_size <- [value]

# ---- 3. Calculate ----
[core function calls with hardcoded values]

# ---- 4. Output ----
cat("\n===== Result =====\n")

# ---- 5. Dropout adjustment ----
dropout_rate <- [value]
n_adj <- ceiling(n / (1 - dropout_rate))
cat(sprintf("Adjusted for %.0f%% dropout: %d\n", dropout_rate*100, n_adj))
```

**Run**:
- R Studio: paste into script window
- CLI: `Rscript clin_calc.R`
```

---

## R Code Generation Rules

| Rule | Description |
|:---------|:----------------|
| **Complete** | install.packages / library / calc / output |
| **Hardcoded** | Actual values, no placeholders |
| **Runnable** | Copy-paste executable in R |
| **Multi-method** | Key scenarios: ≥2 packages |
| **Dropout** | Include clinical utility code |
