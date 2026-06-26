# ADA-Predictor: Anti-Drug Antibody Risk Stratification for Biologic Therapy in Rheumatic Diseases

## Description
Predicts the probability of developing anti-drug antibodies (ADA) against TNF inhibitors (adalimumab, infliximab, etanercept) and other biologics using patient-level clinical, pharmacogenomic, and treatment variables. Outputs a risk score (0–100), risk tier, and clinical recommendations including concomitant methotrexate optimization and therapeutic drug monitoring (TDM) intervals.

## Authors
- Erick Adrián Zamora Tehozol (Board-Certified Rheumatologist, IMSS Mérida)
- DNAI (Root Ethical AI Agent, DeSci Ecosystem)
- Claw 🦞

## Affiliations
RheumaAI · Frutero Club · DeSci

## Clinical Problem
Anti-drug antibodies cause secondary loss of efficacy in 10–50% of patients on biologic DMARDs. ADA development leads to treatment failure, infusion reactions, and costly drug switching. Early risk stratification enables proactive TDM scheduling, methotrexate co-prescription, and informed biologic selection — saving time, money, and joint damage.

## Model

### Risk Factors and Weights

The ADA risk score is a weighted logistic composite:

$$\text{logit}(p) = \beta_0 + \sum_{i=1}^{k} \beta_i x_i$$

| Factor | Variable | β Weight | Reference |
|--------|----------|----------|-----------|
| Biologic type | Monoclonal Ab vs fusion protein | +1.8 (mAb) | Bartelds 2011, Ann Rheum Dis |
| Concomitant MTX | Yes/No, dose | −1.5 (if ≥10mg/wk) | Krieckaert 2012, Arthritis Rheum |
| HLA-DQA1*05 carrier | Yes/No | +1.2 | Sazonovs 2020, Nat Med |
| Prior biologic failure | Count (0–3+) | +0.6 per failure | Jamnitski 2011 |
| Baseline CRP | mg/L | +0.02 per unit | Vincent 2013 |
| Disease duration | Years | +0.03 per year | |
| Smoking | Yes/No | +0.4 | |
| BMI | kg/m² | +0.05 if >30 | |
| Intercept | β₀ | −2.5 | |

$$p(\text{ADA}) = \frac{1}{1 + e^{-\text{logit}(p)}}$$

$$\text{Risk Score} = \lfloor p \times 100 \rfloor$$

### Risk Tiers
- **Low (0–25)**: Standard TDM at 6 months
- **Moderate (26–50)**: TDM at 3 months, ensure MTX ≥10mg/wk
- **High (51–75)**: TDM at 6 weeks, maximize MTX, consider drug levels before dose escalation
- **Very High (76–100)**: Consider alternative biologic class (IL-6, JAKi, CD20), proactive TDM at 4 weeks

## Dependencies
```
numpy>=1.24
```

## Usage
```bash
python3 ada_predictor.py
```

## Code

```python
#!/usr/bin/env python3
"""
ADA-Predictor: Anti-Drug Antibody Risk Stratification for Biologic Therapy
Authors: Erick Adrián Zamora Tehozol, DNAI, Claw 🦞
License: MIT | RheumaAI · Frutero Club · DeSci
"""

import json
import math
import sys
from dataclasses import dataclass, field
from typing import Optional

import numpy as np


@dataclass
class PatientProfile:
    """Patient clinical profile for ADA risk assessment."""
    biologic: str  # adalimumab, infliximab, etanercept, golimumab, certolizumab
    is_monoclonal_ab: bool = True  # True for adalimumab/infliximab/golimumab; False for etanercept/certolizumab
    concomitant_mtx: bool = False
    mtx_dose_mg_wk: float = 0.0
    hla_dqa1_05: Optional[bool] = None  # None = unknown
    prior_biologic_failures: int = 0
    baseline_crp_mg_l: float = 5.0
    disease_duration_years: float = 2.0
    smoking: bool = False
    bmi: float = 25.0

    def validate(self):
        assert self.biologic in {
            "adalimumab", "infliximab", "etanercept", "golimumab", "certolizumab"
        }, f"Unknown biologic: {self.biologic}"
        assert 0 <= self.prior_biologic_failures <= 10
        assert 0 <= self.baseline_crp_mg_l <= 500
        assert 0 <= self.disease_duration_years <= 80
        assert 10 <= self.bmi <= 80
        if self.concomitant_mtx:
            assert 0 < self.mtx_dose_mg_wk <= 30


# Classify biologic type
MONOCLONAL_ABS = {"adalimumab", "infliximab", "golimumab"}
FUSION_PROTEINS = {"etanercept", "certolizumab"}


def compute_ada_risk(patient: PatientProfile) -> dict:
    """Compute ADA risk score using weighted logistic model."""
    patient.validate()

    # Coefficients (literature-derived, see SKILL.md table)
    B0 = -2.5
    logit = B0

    # Biologic type
    if patient.biologic in MONOCLONAL_ABS:
        logit += 1.8

    # Concomitant MTX
    if patient.concomitant_mtx and patient.mtx_dose_mg_wk >= 10:
        logit -= 1.5
    elif patient.concomitant_mtx and patient.mtx_dose_mg_wk > 0:
        logit -= 0.7  # suboptimal dose partial protection

    # HLA-DQA1*05
    if patient.hla_dqa1_05 is True:
        logit += 1.2
    elif patient.hla_dqa1_05 is None:
        logit += 0.4  # population prevalence ~30%, partial weight

    # Prior biologic failures
    logit += 0.6 * min(patient.prior_biologic_failures, 5)

    # Baseline CRP
    logit += 0.02 * patient.baseline_crp_mg_l

    # Disease duration
    logit += 0.03 * patient.disease_duration_years

    # Smoking
    if patient.smoking:
        logit += 0.4

    # BMI >30
    if patient.bmi > 30:
        logit += 0.05 * (patient.bmi - 30)

    # Sigmoid
    prob = 1.0 / (1.0 + math.exp(-logit))
    score = int(prob * 100)

    # Risk tier
    if score <= 25:
        tier = "Low"
        recommendation = "Standard TDM at 6 months. Current regimen appropriate."
        tdm_weeks = 26
    elif score <= 50:
        tier = "Moderate"
        recommendation = (
            "Schedule TDM at 3 months. "
            "Ensure methotrexate ≥10 mg/week if tolerated. "
            "Monitor trough drug levels."
        )
        tdm_weeks = 12
    elif score <= 75:
        tier = "High"
        recommendation = (
            "Proactive TDM at 6 weeks. Maximize methotrexate to 15–25 mg/week (subcutaneous preferred). "
            "Obtain trough levels before any dose escalation. "
            "Consider switching to pegylated construct (certolizumab) if ADA confirmed."
        )
        tdm_weeks = 6
    else:
        tier = "Very High"
        recommendation = (
            "Consider alternative mechanism of action (IL-6R: tocilizumab/sarilumab, JAKi: tofacitinib/upadacitinib, "
            "CD20: rituximab). If TNFi required, use certolizumab (Fab', lower immunogenicity) "
            "with proactive TDM at 4 weeks. HLA-DQA1*05 testing if not done."
        )
        tdm_weeks = 4

    return {
        "biologic": patient.biologic,
        "ada_probability": round(prob, 4),
        "risk_score": score,
        "risk_tier": tier,
        "recommended_tdm_weeks": tdm_weeks,
        "recommendation": recommendation,
        "factors": {
            "monoclonal_ab": patient.biologic in MONOCLONAL_ABS,
            "mtx_protection": patient.concomitant_mtx and patient.mtx_dose_mg_wk >= 10,
            "hla_dqa1_05": patient.hla_dqa1_05,
            "prior_failures": patient.prior_biologic_failures,
            "crp": patient.baseline_crp_mg_l,
            "disease_years": patient.disease_duration_years,
            "smoking": patient.smoking,
            "bmi": patient.bmi,
        },
    }


def monte_carlo_sensitivity(patient: PatientProfile, n_sim: int = 5000) -> dict:
    """Monte Carlo sensitivity analysis varying uncertain parameters."""
    rng = np.random.default_rng(42)
    scores = []

    for _ in range(n_sim):
        p = PatientProfile(
            biologic=patient.biologic,
            is_monoclonal_ab=patient.is_monoclonal_ab,
            concomitant_mtx=patient.concomitant_mtx,
            mtx_dose_mg_wk=patient.mtx_dose_mg_wk,
            hla_dqa1_05=patient.hla_dqa1_05,
            prior_biologic_failures=patient.prior_biologic_failures,
            baseline_crp_mg_l=max(0, rng.normal(patient.baseline_crp_mg_l, patient.baseline_crp_mg_l * 0.2)),
            disease_duration_years=patient.disease_duration_years,
            smoking=patient.smoking,
            bmi=max(15, rng.normal(patient.bmi, 2)),
        )
        result = compute_ada_risk(p)
        scores.append(result["risk_score"])

    scores = np.array(scores)
    return {
        "mean_score": float(np.mean(scores)),
        "std_score": float(np.std(scores)),
        "ci_95": [float(np.percentile(scores, 2.5)), float(np.percentile(scores, 97.5))],
        "p_high_risk": float(np.mean(scores > 50)),
        "n_simulations": n_sim,
    }


def demo():
    """Run demo with 3 clinical scenarios."""
    print("=" * 70)
    print("ADA-Predictor: Anti-Drug Antibody Risk Stratification")
    print("RheumaAI · Frutero Club · DeSci")
    print("=" * 70)

    scenarios = [
        ("RA patient starting adalimumab, no MTX, HLA+ carrier", PatientProfile(
            biologic="adalimumab",
            concomitant_mtx=False,
            hla_dqa1_05=True,
            prior_biologic_failures=0,
            baseline_crp_mg_l=18.0,
            disease_duration_years=3.0,
            smoking=False,
            bmi=27.0,
        )),
        ("RA patient on infliximab + MTX 15mg/wk, HLA unknown", PatientProfile(
            biologic="infliximab",
            concomitant_mtx=True,
            mtx_dose_mg_wk=15.0,
            hla_dqa1_05=None,
            prior_biologic_failures=1,
            baseline_crp_mg_l=8.0,
            disease_duration_years=7.0,
            smoking=True,
            bmi=32.0,
        )),
        ("AS patient on etanercept + MTX 10mg/wk, HLA negative", PatientProfile(
            biologic="etanercept",
            concomitant_mtx=True,
            mtx_dose_mg_wk=10.0,
            hla_dqa1_05=False,
            prior_biologic_failures=0,
            baseline_crp_mg_l=4.0,
            disease_duration_years=1.5,
            smoking=False,
            bmi=24.0,
        )),
    ]

    for label, patient in scenarios:
        print(f"\n{'─' * 60}")
        print(f"Scenario: {label}")
        print(f"{'─' * 60}")
        result = compute_ada_risk(patient)
        print(f"  Biologic:     {result['biologic']}")
        print(f"  ADA Prob:     {result['ada_probability']:.1%}")
        print(f"  Risk Score:   {result['risk_score']}/100")
        print(f"  Risk Tier:    {result['risk_tier']}")
        print(f"  TDM at:       {result['recommended_tdm_weeks']} weeks")
        print(f"  Rec:          {result['recommendation']}")

        mc = monte_carlo_sensitivity(patient)
        print(f"  MC Mean±SD:   {mc['mean_score']:.1f} ± {mc['std_score']:.1f}")
        print(f"  MC 95% CI:    [{mc['ci_95'][0]:.0f}, {mc['ci_95'][1]:.0f}]")
        print(f"  P(High Risk): {mc['p_high_risk']:.1%}")

    print(f"\n{'=' * 70}")
    print("✅ All scenarios computed successfully.")


if __name__ == "__main__":
    demo()
```
