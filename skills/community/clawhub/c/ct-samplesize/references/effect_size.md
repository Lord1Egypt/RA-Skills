# Effect Size Reference

> **English:** Cohen's d f h standards for judging effect size magnitude. Cohen's d f h

## Cohen's d Cohen's d

|Size|d|Clinical Example|
|:---------:|:--:|:-----------------------------|
|Small|0.2|Blood pressure ↓ 5 mmHg|
|Medium|0.5|Blood pressure ↓ 10-15 mmHg|
|Large|0.8|Blood pressure ↓ >20 mmHg|

## Cohen's f Cohen's f

|Size|f|ANOVA Interpretation|
|:---------:|:--:|:---------------------|
|Small|0.10|Groups slightly different|
|Medium|0.25|Clinically relevant|
|Large|0.40|Clearly separated|

## h Effect Size (arcsin-transformed rates) h

|Size|h|arcsin Rate Difference|
|:---------:|:--:|:----------------------|
|Small|0.20|~0.10 (rate diff)|
|Medium|0.50|~0.25 (rate diff)|
|Large|0.80|~0.40 (rate diff)|

## Conversion Formulas

|Conversion|Formula|
|:----------------|:-------------|
| Cohen's d → f | $f = d/2$ |
| Cohen's d → r | $r = d/\sqrt{d^2+4}$ |
| r → Cohen's d | $d = 2r/\sqrt{1-r^2}$ |
| OR → Cohen's d | $d = \log(OR) \times \sqrt{3}/\pi$ |
| η² → Cohen's f | $f = \sqrt{\eta^2/(1-\eta^2)}$ |

## Z-Value Quick Reference Z

| $\alpha$ | One-sided $Z_{1-\alpha}$ | Two-sided $Z_{1-\alpha/2}$ |
|:--------:|:------------------------:|:--------------------------:|
| 0.10 | 1.282 | 1.645 |
| 0.05 | 1.645 | 1.960 |
| 0.025 | 1.960 | 2.242 |
| 0.01 | 2.326 | 2.576 |
| 0.001 | 3.090 | 3.291 |

| $\beta$ | $Z_{1-\beta}$ |
|:-------:|:------------:|
| 0.20 | 0.842 |
| 0.10 | 1.282 |
| 0.05 | 1.645 |
| 0.01 | 2.326 |
