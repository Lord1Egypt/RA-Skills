#!/usr/bin/env python3
"""
ADA-Predictor: Anti-Drug Antibody Risk Stratification for Biologic Therapy
Authors: Erick Adrián Zamora Tehozol, DNAI, Claw 🦞
License: MIT | RheumaAI · Frutero Club · DeSci
"""

import json
import math
import sys
from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class PatientProfile:
    biologic: str
    is_monoclonal_ab: bool = True
    concomitant_mtx: bool = False
    mtx_dose_mg_wk: float = 0.0
    hla_dqa1_05: Optional[bool] = None
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


MONOCLONAL_ABS = {"adalimumab", "infliximab", "golimumab"}


def compute_ada_risk(patient: PatientProfile) -> dict:
    patient.validate()
    B0 = -2.5
    logit = B0

    if patient.biologic in MONOCLONAL_ABS:
        logit += 1.8
    if patient.concomitant_mtx and patient.mtx_dose_mg_wk >= 10:
        logit -= 1.5
    elif patient.concomitant_mtx and patient.mtx_dose_mg_wk > 0:
        logit -= 0.7
    if patient.hla_dqa1_05 is True:
        logit += 1.2
    elif patient.hla_dqa1_05 is None:
        logit += 0.4
    logit += 0.6 * min(patient.prior_biologic_failures, 5)
    logit += 0.02 * patient.baseline_crp_mg_l
    logit += 0.03 * patient.disease_duration_years
    if patient.smoking:
        logit += 0.4
    if patient.bmi > 30:
        logit += 0.05 * (patient.bmi - 30)

    prob = 1.0 / (1.0 + math.exp(-logit))
    score = int(prob * 100)

    if score <= 25:
        tier, tdm = "Low", 26
        rec = "Standard TDM at 6 months. Current regimen appropriate."
    elif score <= 50:
        tier, tdm = "Moderate", 12
        rec = "Schedule TDM at 3 months. Ensure methotrexate ≥10 mg/week if tolerated."
    elif score <= 75:
        tier, tdm = "High", 6
        rec = "Proactive TDM at 6 weeks. Maximize MTX 15-25 mg/wk SC. Check trough before dose escalation."
    else:
        tier, tdm = "Very High", 4
        rec = "Consider alternative MOA (IL-6R, JAKi, CD20). If TNFi needed, use certolizumab + proactive TDM at 4 wk."

    return {
        "biologic": patient.biologic, "ada_probability": round(prob, 4),
        "risk_score": score, "risk_tier": tier,
        "recommended_tdm_weeks": tdm, "recommendation": rec,
    }


def monte_carlo_sensitivity(patient: PatientProfile, n_sim: int = 5000) -> dict:
    rng = np.random.default_rng(42)
    scores = []
    for _ in range(n_sim):
        p = PatientProfile(
            biologic=patient.biologic, is_monoclonal_ab=patient.is_monoclonal_ab,
            concomitant_mtx=patient.concomitant_mtx, mtx_dose_mg_wk=patient.mtx_dose_mg_wk,
            hla_dqa1_05=patient.hla_dqa1_05,
            prior_biologic_failures=patient.prior_biologic_failures,
            baseline_crp_mg_l=max(0, rng.normal(patient.baseline_crp_mg_l, patient.baseline_crp_mg_l * 0.2)),
            disease_duration_years=patient.disease_duration_years,
            smoking=patient.smoking,
            bmi=max(15, rng.normal(patient.bmi, 2)),
        )
        scores.append(compute_ada_risk(p)["risk_score"])
    scores = np.array(scores)
    return {
        "mean_score": float(np.mean(scores)), "std_score": float(np.std(scores)),
        "ci_95": [float(np.percentile(scores, 2.5)), float(np.percentile(scores, 97.5))],
        "p_high_risk": float(np.mean(scores > 50)), "n_simulations": n_sim,
    }


def demo():
    print("=" * 70)
    print("ADA-Predictor: Anti-Drug Antibody Risk Stratification")
    print("RheumaAI · Frutero Club · DeSci")
    print("=" * 70)

    scenarios = [
        ("RA on adalimumab, no MTX, HLA-DQA1*05+", PatientProfile(
            biologic="adalimumab", hla_dqa1_05=True, baseline_crp_mg_l=18.0,
            disease_duration_years=3.0, bmi=27.0)),
        ("RA on infliximab + MTX 15mg/wk, smoker", PatientProfile(
            biologic="infliximab", concomitant_mtx=True, mtx_dose_mg_wk=15.0,
            prior_biologic_failures=1, baseline_crp_mg_l=8.0,
            disease_duration_years=7.0, smoking=True, bmi=32.0)),
        ("AS on etanercept + MTX, HLA-DQA1*05 neg", PatientProfile(
            biologic="etanercept", concomitant_mtx=True, mtx_dose_mg_wk=10.0,
            hla_dqa1_05=False, baseline_crp_mg_l=4.0, disease_duration_years=1.5, bmi=24.0)),
    ]

    for label, patient in scenarios:
        print(f"\n{'─' * 60}")
        print(f"Scenario: {label}")
        result = compute_ada_risk(patient)
        print(f"  Score: {result['risk_score']}/100 ({result['risk_tier']}) | ADA prob: {result['ada_probability']:.1%}")
        print(f"  TDM: {result['recommended_tdm_weeks']} wk | {result['recommendation']}")
        mc = monte_carlo_sensitivity(patient)
        print(f"  MC: {mc['mean_score']:.1f}±{mc['std_score']:.1f}, 95%CI [{mc['ci_95'][0]:.0f},{mc['ci_95'][1]:.0f}], P(high)={mc['p_high_risk']:.1%}")

    print(f"\n{'=' * 70}\n✅ All scenarios computed successfully.")


if __name__ == "__main__":
    demo()
