#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
disproportionality.py /  disproportionate analysis (signal detection)

Computes three standard pharmacovigilance measures from a 2x2 contingency table
of (drug, event) co-occurrence in FAERS:
  - ROR   (Reporting Odds Ratio)        ROR = a*d / (b*c)
  - PRR   (Proportional Reporting Ratio) PRR = [a/(a+b)] / [c/(c+d)]
  - IC    (Information Component, UMC/VigiBase method) IC = log2( N*a / ((a+b)(a+c)) )

Each with 95% confidence intervals (log method) and a binary signal flag.
Signal conventions (EMA / WHO):
  - ROR:  lower 95% CI of ROR > 1
  - PRR:  PRR >= 2 AND chi-square >= 4
  - IC:   lower 95% CI (IC025) > 0
  - EBGM: FDA MGPS Bayesian shrinkage (gamma-Poisson mixture); signal when EB05 >= 2
No network call. Pure math on the 2x2 table. / 纯本地统计，不联网。

Extensions added (v0.1.8, inspired by upstream scan):
  - PRR p-value (1-df chi-square upper tail, via math.erfc — no scipy dependency)
  - benjamini_hochberg(): FDR control for multi-event sweeps
  - map_soc(): limited MedDRA PT -> System Organ Class mapping (curated dictionary)
"""
import argparse
import json
import math
import os
import re
import sys
from ebgm import ebgm  # FDA MGPS EBGM (gamma-Poisson mixture shrinkage)


def _safe(x):
    return x if x is not None and x > 0 else 1e-9


def prr_pvalue_from_chi2(chi2):
    """Upper-tail p-value of a 1-degree-of-freedom chi-square statistic.

    For 1 df, P(X >= x) = erfc(sqrt(x/2)). Pure stdlib (math.erfc), so no
    scipy required. Returns 1.0 for non-positive chi2.
    """
    if chi2 is None or chi2 <= 0:
        return 1.0
    return math.erfc(math.sqrt(chi2 / 2.0))


def compute(a, b, c, d, continuity=False):
    """Disproportionality from a 2x2 table.

    `continuity` (default False) applies the Haldane-Anscombe correction: add 0.5
    to every cell so a zero cell (which would collapse ROR/PRR to 0 or inf) yields
    a finite, conservative estimate. Standard for sparse 2x2 tables. When enabled,
    the returned `table` reflects the corrected counts and `raw_counts` preserves
    the originals for audit.
    """
    raw = {"a": a, "b": b, "c": c, "d": d}
    # Negative cell counts are invalid (counts cannot be negative). Clamp to a
    # conservative null and never signal, to avoid OverflowError / NaN in the math
    # below (and in ebgm). Mirrors the structural-zero (a==0) guard.
    if raw["a"] < 0 or raw["b"] < 0 or raw["c"] < 0 or raw["d"] < 0:
        _a, _b, _c, _d = (max(v, 0) for v in (raw["a"], raw["b"], raw["c"], raw["d"]))
        _eb = ebgm(_a, _b, _c, _d)
        return {
            "table": {"a": _a, "b": _b, "c": _c, "d": _d, "N": _b + _c + _d},
            "ROR": {"value": 0.0, "ci_low": 0.0, "ci_high": 0.0, "signal": False},
            "PRR": {"value": 0.0, "ci_low": 0.0, "ci_high": 0.0,
                    "chi2": 0.0, "p_value": 1.0, "signal": False},
            "IC": {"value": -10.0, "ci_low": -10.0, "ci_high": -10.0, "signal": False},
            "EBGM": _eb,
            "continuity": False, "raw_counts": None, "signal_overall": False,
            "note": "negative cell count detected: clamped to conservative null (no signal)",
        }
    # EBGM (FDA MGPS) from RAW counts -- independent of the Haldane correction
    # applied to ROR/PRR below; Bayesian shrinkage is the right behaviour on a==0.
    eb = ebgm(raw["a"], raw["b"], raw["c"], raw["d"])
    # Structural zero: NO observed co-occurrence (a==0). Return a conservative
    # null and NEVER a signal, regardless of `continuity`. Applying Haldane here
    # would fabricate a (often huge) OR from a zero cell -- e.g. (0.5*d)/(0.5*b)
    # collapses to d/b and spuriously flags an event that was never reported with
    # the drug. Unsafe for signal detection; EBGM already returns ~1 (no signal)
    # on a==0, so this keeps ROR/PRR consistent with it.
    if raw["a"] == 0:
        return {
            "table": {"a": 0, "b": b, "c": c, "d": d, "N": b + c + d},
            "ROR": {"value": 0.0, "ci_low": 0.0, "ci_high": 0.0, "signal": False},
            "PRR": {"value": 0.0, "ci_low": 0.0, "ci_high": 0.0,
                    "chi2": 0.0, "p_value": 1.0, "signal": False},
            "IC": {"value": -10.0, "ci_low": -10.0, "ci_high": -10.0, "signal": False},
            "EBGM": eb,
            "continuity": False, "raw_counts": None, "signal_overall": False,
            "note": "a==0: zero co-occurrence, conservative null "
                    "(continuity overridden)",
        }
    # Zero cell in a non-a margin (b/c/d == 0) without continuity correction:
    # 1/0 in the SE terms would overflow. Return a conservative null (no signal)
    # rather than crash — real FAERS slices can yield empty margins for rare
    # drug-event pairs. Continuity correction handles this gracefully, so only
    # guard the no-correction path.
    if (not continuity) and (b == 0 or c == 0 or d == 0):
        return {
            "table": {"a": a, "b": b, "c": c, "d": d, "N": b + c + d},
            "ROR": {"value": 0.0, "ci_low": 0.0, "ci_high": 0.0, "signal": False},
            "PRR": {"value": 0.0, "ci_low": 0.0, "ci_high": 0.0,
                    "chi2": 0.0, "p_value": 1.0, "signal": False},
            "IC": {"value": -10.0, "ci_low": -10.0, "ci_high": -10.0, "signal": False},
            "EBGM": eb,
            "continuity": False, "raw_counts": None, "signal_overall": False,
            "note": "zero margin cell (b/c/d==0) without continuity: "
                    "conservative null (no signal)",
        }
    if continuity:
        a = a + 0.5; b = b + 0.5; c = c + 0.5; d = d + 0.5
    N = a + b + c + d
    a = _safe(a); b = _safe(b); c = _safe(c); d = _safe(d)
    # ROR
    ror = (a * d) / (b * c)
    se_log_ror = math.sqrt(1.0 / a + 1.0 / b + 1.0 / c + 1.0 / d)
    ror_lo = math.exp(math.log(ror) - 1.96 * se_log_ror)
    ror_hi = math.exp(math.log(ror) + 1.96 * se_log_ror)
    # PRR
    p1 = a / (a + b)
    p0 = c / (c + d)
    prr = p1 / p0
    se_log_prr = math.sqrt(1.0 / a - 1.0 / (a + b) + 1.0 / c - 1.0 / (c + d))
    prr_lo = math.exp(math.log(prr) - 1.96 * se_log_prr)
    prr_hi = math.exp(math.log(prr) + 1.96 * se_log_prr)
    # PRR chi-square (Mantel-Haenszel, no continuity correction)
    denom = (a + b) * (c + d) * (a + c) * (b + d)
    chi2 = (a * d - b * c) ** 2 * N / denom if denom > 0 else 0.0
    prr_p = prr_pvalue_from_chi2(chi2)
    # IC (EBGM)
    ic = math.log2((N * a) / ((a + b) * (a + c)))
    var_ic = 1.0 / a - 1.0 / (a + b) - 1.0 / (a + c) + 1.0 / N
    ic_lo = ic - 1.96 * math.sqrt(max(var_ic, 1e-9))
    ic_hi = ic + 1.96 * math.sqrt(max(var_ic, 1e-9))

    # IC 信号判定：需点估计与下限均有实质余量（ic>0.1 且 ic_lo>0.1），
    # 避免 IC025 仅略大于 0 的边际噪声（如 IC=0.126/ci_low=0.024）误判信号。
    signals = {
        "ROR": ror_lo > 1,
        "PRR": (prr >= 2) and (chi2 >= 4),
        "IC": (ic > 0.1) and (ic_lo > 0.1),
        "EBGM": eb["signal"],
    }
    overall = any(signals.values())

    return {
        "table": {"a": a, "b": b, "c": c, "d": d, "N": N},
        "ROR": {"value": round(ror, 3), "ci_low": round(ror_lo, 3),
                "ci_high": round(ror_hi, 3), "signal": signals["ROR"]},
        "PRR": {"value": round(prr, 3), "ci_low": round(prr_lo, 3),
                "ci_high": round(prr_hi, 3), "chi2": round(chi2, 2),
                "p_value": round(prr_p, 6), "signal": signals["PRR"]},
        "IC": {"value": round(ic, 3), "ci_low": round(ic_lo, 3),
               "ci_high": round(ic_hi, 3), "signal": signals["IC"]},
        "EBGM": {"value": eb["value"], "eb05": eb["eb05"], "eb95": eb["eb95"],
                 "signal": eb["signal"], "weights": eb["weights"]},
        "continuity": continuity,
        "raw_counts": raw if continuity else None,
        "signal_overall": overall,
    }


def benjamini_hochberg(pvals):
    """Benjamini-Hochberg FDR control.

    Input: list of p-values (None / non-numeric treated as 1.0 — i.e. not
    significant). Output: list of BH-adjusted q-values in the SAME order as the
    input. Monotonicity is enforced (step-up from the largest rank).

    Use after a multi-event sweep to flag which signals survive FDR < 0.05,
    preventing false discoveries when many drug-event pairs are tested at once.
    """
    m = len(pvals)
    if m == 0:
        return []
    idx_p = []
    for i, p in enumerate(pvals):
        try:
            p = float(p)
        except (TypeError, ValueError):
            p = 1.0
        if p is None or math.isnan(p):
            p = 1.0
        if p < 0.0:
            p = 0.0
        if p > 1.0:
            p = 1.0
        idx_p.append([i, p])
    ordered = sorted(idx_p, key=lambda x: x[1])  # ascending by p
    q = [1.0] * m
    prev = 1.0
    # step from largest rank down to enforce monotonic non-increasing q
    for rank in range(m, 0, -1):
        i, p = ordered[rank - 1]
        val = p * m / rank
        val = min(val, prev)
        q[i] = val
        prev = val
    return q


# ----------------------------------------------------------------------------
# Limited MedDRA PT -> System Organ Class (SOC) mapping.
#
# NOTE: MedDRA is a licensed dictionary; this is a CURATED, INCOMPLETE mapping
# of high-frequency PTs only (covering the common AEs seen in oncology / cardio
# / metabolic / general PV work). Terms not present fall back to
# "Unmapped / 未归类". It is intended for REPORT READABILITY (grouping signals
# by organ system), NOT as a certified MedDRA lookup. For full SOC coverage,
# license MedDRA and replace this dict with an official lookup.
# ----------------------------------------------------------------------------
PT_TO_SOC = {
    # Gastrointestinal
    "NAUSEA": "Gastrointestinal disorders",
    "VOMITING": "Gastrointestinal disorders",
    "DIARRHOEA": "Gastrointestinal disorders",
    "DIARRHEA": "Gastrointestinal disorders",
    "CONSTIPATION": "Gastrointestinal disorders",
    "ABDOMINAL PAIN": "Gastrointestinal disorders",
    "ABDOMINAL PAIN UPPER": "Gastrointestinal disorders",
    "DYSPEPSIA": "Gastrointestinal disorders",
    "GASTRITIS": "Gastrointestinal disorders",
    "GASTROINTESTINAL HAEMORRHAGE": "Gastrointestinal disorders",
    "STOMATITIS": "Gastrointestinal disorders",
    "COLITIS": "Gastrointestinal disorders",
    # Hepatobiliary
    "HEPATIC FAILURE": "Hepatobiliary disorders",
    "HEPATITIS": "Hepatobiliary disorders",
    "JAUNDICE": "Hepatobiliary disorders",
    "ALT INCREASED": "Hepatobiliary disorders",
    "AST INCREASED": "Hepatobiliary disorders",
    "BLOOD ALKALINE PHOSPHATASE INCREASED": "Hepatobiliary disorders",
    "HEPATIC ENZYME INCREASED": "Hepatobiliary disorders",
    "LIVER FUNCTION TEST ABNORMAL": "Hepatobiliary disorders",
    "HYPERBILIRUBINAEMIA": "Hepatobiliary disorders",
    "IMMUNE-MEDIATED HEPATITIS": "Hepatobiliary disorders",
    # Skin & subcutaneous
    "RASH": "Skin and subcutaneous tissue disorders",
    "PRURITUS": "Skin and subcutaneous tissue disorders",
    "ERYTHEMA": "Skin and subcutaneous tissue disorders",
    "DRY SKIN": "Skin and subcutaneous tissue disorders",
    "ALOPECIA": "Skin and subcutaneous tissue disorders",
    "ACNE": "Skin and subcutaneous tissue disorders",
    "STEVENS JOHNSON SYNDROME": "Skin and subcutaneous tissue disorders",
    "TOXIC EPIDERMAL NECROLYSIS": "Skin and subcutaneous tissue disorders",
    "DERMATITIS": "Skin and subcutaneous tissue disorders",
    "HYPERSENSITIVITY": "Skin and subcutaneous tissue disorders",
    "DRUG ERUPTION": "Skin and subcutaneous tissue disorders",
    # Nervous
    "HEADACHE": "Nervous system disorders",
    "DIZZINESS": "Nervous system disorders",
    "INSOMNIA": "Nervous system disorders",
    "FATIGUE": "General disorders and administration site conditions",
    "SEIZURE": "Nervous system disorders",
    "PERIPHERAL NEUROPATHY": "Nervous system disorders",
    "PARESTHESIA": "Nervous system disorders",
    "TREMOR": "Nervous system disorders",
    "SOMNOLENCE": "Nervous system disorders",
    "DYSAESTHESIA": "Nervous system disorders",
    "ENCEPHALOPATHY": "Nervous system disorders",
    "DEPRESSED LEVEL OF CONSCIOUSNESS": "Nervous system disorders",
    # Psychiatric
    "DEPRESSION": "Psychiatric disorders",
    "ANXIETY": "Psychiatric disorders",
    "INSOMNIA": "Psychiatric disorders",
    "CONFUSIONAL STATE": "Psychiatric disorders",
    "SLEEP DISORDER": "Psychiatric disorders",
    # Cardiac
    "CARDIAC FAILURE": "Cardiac disorders",
    "MYOCARDIAL INFARCTION": "Cardiac disorders",
    "ARRHYTHMIA": "Cardiac disorders",
    "TACHYCARDIA": "Cardiac disorders",
    "BRADYCARDIA": "Cardiac disorders",
    "ATRIAL FIBRILLATION": "Cardiac disorders",
    "QT PROLONGATION": "Cardiac disorders",
    "CARDIOMYOPATHY": "Cardiac disorders",
    "PERICARDIAL EFFUSION": "Cardiac disorders",
    "CARDIAC TAMPONADE": "Cardiac disorders",
    "PERICARDITIS": "Cardiac disorders",
    "ANGINA PECTORIS": "Cardiac disorders",
    # Vascular
    "HYPOTENSION": "Vascular disorders",
    "HYPERTENSION": "Vascular disorders",
    "THROMBOSIS": "Vascular disorders",
    "VENOUS THROMBOEMBOLISM": "Vascular disorders",
    "PULMONARY EMBOLISM": "Vascular disorders",
    "DEEP VEIN THROMBOSIS": "Vascular disorders",
    "HAEMORRHAGE": "Vascular disorders",
    "FLUSHING": "Vascular disorders",
    "HYPERTENSIVE CRISIS": "Vascular disorders",
    # Respiratory
    "PNEUMONITIS": "Respiratory, thoracic and mediastinal disorders",
    "DYSPNOEA": "Respiratory, thoracic and mediastinal disorders",
    "COUGH": "Respiratory, thoracic and mediastinal disorders",
    "PNEUMONIA": "Respiratory, thoracic and mediastinal disorders",
    "RESPIRATORY FAILURE": "Respiratory, thoracic and mediastinal disorders",
    "INTERSTITIAL LUNG DISEASE": "Respiratory, thoracic and mediastinal disorders",
    "HYPOXIA": "Respiratory, thoracic and mediastinal disorders",
    "UPPER RESPIRATORY TRACT INFECTION": "Respiratory, thoracic and mediastinal disorders",
    "EPISTAXIS": "Respiratory, thoracic and mediastinal disorders",
    "PLEURAL EFFUSION": "Respiratory, thoracic and mediastinal disorders",
    "RESPIRATORY DISTRESS": "Respiratory, thoracic and mediastinal disorders",
    "BRONCHOSPASM": "Respiratory, thoracic and mediastinal disorders",
    # Renal & urinary
    "RENAL FAILURE": "Renal and urinary disorders",
    "ACUTE KIDNEY INJURY": "Renal and urinary disorders",
    "NEPHRITIS": "Renal and urinary disorders",
    "PROTEINURIA": "Renal and urinary disorders",
    "HAEMATURIA": "Renal and urinary disorders",
    "OLIGURIA": "Renal and urinary disorders",
    "RENAL IMPAIRMENT": "Renal and urinary disorders",
    "NEPHROGENIC DIABETES INSIPIDUS": "Renal and urinary disorders",
    # Endocrine
    "HYPOTHYROIDISM": "Endocrine disorders",
    "HYPERTHYROIDISM": "Endocrine disorders",
    "THYROID FUNCTION TEST ABNORMAL": "Endocrine disorders",
    "THYROIDITIS": "Endocrine disorders",
    "HYPERGLYCAEMIA": "Endocrine disorders",
    "DIABETIC KETOACIDOSIS": "Endocrine disorders",
    "ADRENAL INSUFFICIENCY": "Endocrine disorders",
    # Metabolism & nutrition
    "HYPOKALAEMIA": "Metabolism and nutrition disorders",
    "HYPONATRAEMIA": "Metabolism and nutrition disorders",
    "HYPERCALCAEMIA": "Metabolism and nutrition disorders",
    "DEHYDRATION": "Metabolism and nutrition disorders",
    "ANOREXIA": "Metabolism and nutrition disorders",
    "WEIGHT LOSS": "Metabolism and nutrition disorders",
    "WEIGHT INCREASED": "Metabolism and nutrition disorders",
    "APPETITE DECREASED": "Metabolism and nutrition disorders",
    "HYPOALBUMINAEMIA": "Metabolism and nutrition disorders",
    # Musculoskeletal
    "ARTHRALGIA": "Musculoskeletal and connective tissue disorders",
    "MYALGIA": "Musculoskeletal and connective tissue disorders",
    "MUSCLE WEAKNESS": "Musculoskeletal and connective tissue disorders",
    "RABDOMYOLYSIS": "Musculoskeletal and connective tissue disorders",
    "OSTEONECROSIS": "Musculoskeletal and connective tissue disorders",
    "BONE PAIN": "Musculoskeletal and connective tissue disorders",
    "MYOPATHY": "Musculoskeletal and connective tissue disorders",
    "ARTHRITIS": "Musculoskeletal and connective tissue disorders",
    # Blood & lymphatic
    "ANAEMIA": "Blood and lymphatic system disorders",
    "THROMBOCYTOPENIA": "Blood and lymphatic system disorders",
    "LEUKOPENIA": "Blood and lymphatic system disorders",
    "NEUTROPENIA": "Blood and lymphatic system disorders",
    "PANCYTOPENIA": "Blood and lymphatic system disorders",
    "LYMPHOPENIA": "Blood and lymphatic system disorders",
    "FEBRILE NEUTROPENIA": "Blood and lymphatic system disorders",
    "COAGULOPATHY": "Blood and lymphatic system disorders",
    # Infections
    "INFECTION": "Infections and infestations",
    "SEPSIS": "Infections and infestations",
    "PYREXIA": "Infections and infestations",
    "NEUTROPENIC SEPSIS": "Infections and infestations",
    "URINARY TRACT INFECTION": "Infections and infestations",
    "CELLULITIS": "Infections and infestations",
    "PNEUMONIA": "Infections and infestations",
    "OPPORTUNISTIC INFECTION": "Infections and infestations",
    # Eye
    "VISION BLURRED": "Eye disorders",
    "CONJUNCTIVITIS": "Eye disorders",
    "DRY EYE": "Eye disorders",
    "EYE PAIN": "Eye disorders",
    "UVEITIS": "Eye disorders",
    "VISUAL ACUITY REDUCED": "Eye disorders",
    # Immune
    "ANAPHYLACTIC REACTION": "Immune system disorders",
    "CYTOKINE RELEASE SYNDROME": "Immune system disorders",
    "IMMUNE-MEDIATED MYOCARDITIS": "Immune system disorders",
    "INFLAMMATORY BOWEL DISEASE": "Gastrointestinal disorders",
    # General / administration
    "PYREXIA": "General disorders and administration site conditions",
    "ASTHENIA": "General disorders and administration site conditions",
    "OEDEMA": "General disorders and administration site conditions",
    "MALAISE": "General disorders and administration site conditions",
    "CHILLS": "General disorders and administration site conditions",
    "INJECTION SITE REACTION": "General disorders and administration site conditions",
    "FATIGUE": "General disorders and administration site conditions",
    "PAIN": "General disorders and administration site conditions",
    # ---- EGFR-TKI / NSCLC class-effect & general oncology expansion (v0.1.11) ----
    # EGFR-TKI hallmark cutaneous / appendageal toxicities
    "ANGIOEDEMA": "Skin and subcutaneous tissue disorders",
    "PARONYCHIA": "Skin and subcutaneous tissue disorders",
    "TRICHOMEGALY": "Skin and subcutaneous tissue disorders",
    "FOLLICULITIS": "Skin and subcutaneous tissue disorders",
    # EGFR-TKI ocular toxicities
    "KERATITIS": "Eye disorders",
    "EYE IRRITATION": "Eye disorders",
    "VISUAL IMPAIRMENT": "Eye disorders",
    "CORNEAL EPITHELIAL DEFECT": "Eye disorders",
    # Mucosal / GI
    "MUCOSITIS": "Gastrointestinal disorders",
    "ORAL MUCOSITIS": "Gastrointestinal disorders",
    "XEROSTOMIA": "Gastrointestinal disorders",
    "ASCITES": "Gastrointestinal disorders",
    # Metabolic (EGFR-TKI diarrhoea-driven electrolyte loss, appetite/weight)
    "HYPOMAGNESAEMIA": "Metabolism and nutrition disorders",
    "HYPOMAGNESEMIA": "Metabolism and nutrition disorders",
    "DECREASED APPETITE": "Metabolism and nutrition disorders",
    "WEIGHT DECREASED": "Metabolism and nutrition disorders",
    # Immune / hypersensitivity (broad-spectrum, also ICPI-related)
    "ANAPHYLAXIS": "Immune system disorders",
    "ANAPHYLACTIC SHOCK": "Immune system disorders",
    # Hepato / cardiac (label-relevant across targeted & ICPI therapies)
    "HEPATOTOXICITY": "Hepatobiliary disorders",
    "MYOCARDITIS": "Cardiac disorders",
    # General / respiratory adjacent
    "PERIPHERAL OEDEMA": "General disorders and administration site conditions",
    "BRONCHITIS": "Respiratory, thoracic and mediastinal disorders",
    "RESPIRATORY TRACT INFECTION": "Infections and infestations",
    # ---- explicit compound PTs (v0.1.14): keep high-frequency ambiguous terms
    #      precise so the conservative multi-word-only substring fallback (see
    #      map_soc) never collapses them onto a generic single-word bucket. ----
    "CHEST PAIN": "Cardiac disorders",
    "ANGINA": "Cardiac disorders",
    "BACK PAIN": "Musculoskeletal and connective tissue disorders",
    "JOINT PAIN": "Musculoskeletal and connective tissue disorders",
    "MUSCLE PAIN": "Musculoskeletal and connective tissue disorders",
    "NECK PAIN": "Musculoskeletal and connective tissue disorders",
    "FLANK PAIN": "Renal and urinary disorders",
    "KIDNEY FAILURE": "Renal and urinary disorders",
    "KIDNEY INJURY": "Renal and urinary disorders",
    "RENAL PAIN": "Renal and urinary disorders",
}


def map_soc(pt):
    """Map a MedDRA Preferred Term to its System Organ Class (limited dict).

    Exact dictionary match first. For unmapped compound PTs, a CONSERVATIVE
    substring fallback is applied over MULTI-WORD dictionary keys only (longest
    match wins) — generic single-word keys (e.g. "PAIN", "KIDNEY") are
    deliberately excluded from the fallback so they cannot hijack the SOC of a
    compound term (e.g. "CHEST PAIN" must NOT collapse onto bare "PAIN" ->
    General bucket; it is now an explicit Cardiac entry above). Returns
    "Unmapped / 未归类" when nothing matches.

    User-supplied extension (upgrade E, 2026-09-29): if the env var
    ``CT_SAFETY_SOC_MAP`` points to a JSON/CSV file (or ``--soc-map`` was
    passed on the CLI and loaded via :func:`load_user_soc_map`), those PT→SOC
    pairs are merged OVER the built-in dictionary at lookup time. The user file
    is never bundled — MedDRA is license-restricted, so we only accept the
    sponsor's own licensed mapping.
    """
    if not pt:
        return "Unmapped / 未归类"
    key = re.sub(r"[^A-Za-z ]", "", str(pt)).strip().upper()
    if not key:
        return "Unmapped / 未归类"
    user = _USER_SOC_MAP.get(key)
    if user:
        return user
    soc = PT_TO_SOC.get(key)
    if soc:
        return soc
    # Substring fallback: multi-word dictionary keys only, longest match wins.
    # Also consult user map multi-word keys first (user takes precedence).
    best = None
    best_len = 0
    for k, v in list(_USER_SOC_MAP.items()) + list(PT_TO_SOC.items()):
        if len(k.split()) < 2:
            continue  # skip generic single-word keys in fallback
        if k in key or key in k:
            if len(k) > best_len:
                best = v
                best_len = len(k)
    return best if best else "Unmapped / 未归类"


# ---------------------------------------------------------------------------
# User-supplied PT→SOC extension map (upgrade E). Loaded lazily from the env
# var CT_SAFETY_SOC_MAP or explicitly via load_user_soc_map(path). Never
# bundled (MedDRA license stays with the sponsor's own copy).
# ---------------------------------------------------------------------------
_USER_SOC_MAP = {}


def load_user_soc_map(path):
    """Load a user PT→SOC mapping file (JSON {PT: SOC} or CSV/TSV two columns).

    Keys are normalized the same way as :func:`map_soc` (strip non-letters,
    upper). Returns the number of entries loaded. Safe to call repeatedly;
    later loads merge/overwrite earlier ones."""
    global _USER_SOC_MAP
    if not path:
        return 0
    loaded = 0
    try:
        if path.lower().endswith(".json"):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            items = data.items() if isinstance(data, dict) else [
                (d.get("pt") or d.get("PT"), d.get("soc") or d.get("SOC"))
                for d in data]
        else:
            import csv
            items = []
            with open(path, encoding="utf-8-sig", newline="") as f:
                delim = "\t" if "\t" in open(path, encoding="utf-8").read(4096) else ","
                for row in csv.reader(f, delimiter=delim):
                    if len(row) >= 2 and row[0].strip():
                        items.append((row[0].strip(), row[1].strip()))
        for pt, soc in items:
            if not pt or not soc:
                continue
            key = re.sub(r"[^A-Za-z ]", "", str(pt)).strip().upper()
            if key:
                _USER_SOC_MAP[key] = str(soc).strip()
                loaded += 1
    except Exception as e:  # noqa: BLE001 - extension is best-effort
        print("[WARN] user SOC map not loaded (%s): %s" % (path, e), file=sys.stderr)
    return loaded


def init_soc_map_from_env():
    """Auto-load CT_SAFETY_SOC_MAP if set. Call once at CLI start."""
    p = os.environ.get("CT_SAFETY_SOC_MAP", "")
    return load_user_soc_map(p) if p else 0


# ----------------------------------------------------------------------------
# Known signal reference pairs for pipeline self-validation (--validate-controls).
#
# Positive controls = drug-event pairs with an ESTABLISHED adverse-drug association
# (e.g. cerivastatin/rhabdomyolysis led to market withdrawal). A well-behaved
# detection pipeline should flag these (expected signal = True).
#
# Negative controls = drug-event pairs with NO established association (a safe,
# ubiquitous drug paired with an unrelated serious event). The pipeline should
# NOT flag these (expected signal = False).
#
# Drug names use the openFDA `patient.drug.medicinalproduct` form. These pairs are
# reference anchors only; they are NOT a validation of any specific drug's safety.
# ----------------------------------------------------------------------------
CONTROL_DRUGS = {
    "positive": [
        ("cerivastatin", "RABDOMYOLYSIS"),
        ("troglitazone", "HEPATITIS"),
        ("rosiglitazone", "MYOCARDIAL INFARCTION"),
        ("leflunomide", "HEPATIC FAILURE"),
        ("fluoroquinolone", "TENDON RUPTURE"),
    ],
    "negative": [
        ("paracetamol", "RABDOMYOLYSIS"),
        ("ibuprofen", "PNEUMONITIS"),
        ("amoxicillin", "MYOCARDIAL INFARCTION"),
        ("salbutamol", "HEPATIC FAILURE"),
    ],
}


def load_control_pairs(path):
    """Merge external benchmark control pairs into CONTROL_DRUGS (upgrade E).

    File forms:
      JSON: {"positive": [["drug","event"], ...] or [{"drug":..,"event":..}],
             "negative": [...]}
      CSV/TSV: three columns group,drug,event (header optional).
    Lets a sponsor validate the pipeline against THEIR OWN published known-
    positive/negative benchmark set (e.g. WHO VigiBase case studies, FDA
    safety communications) instead of only the 9 built-in anchors.
    Returns counts {positive, negative} added.
    """
    added = {"positive": 0, "negative": 0}
    if not path:
        return added
    try:
        if path.lower().endswith(".json"):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            for grp in ("positive", "negative"):
                for item in data.get(grp, []):
                    if isinstance(item, dict):
                        pair = (item.get("drug", ""), item.get("event", ""))
                    else:
                        pair = (item[0], item[1])
                    if pair[0] and pair[1]:
                        CONTROL_DRUGS[grp].append(pair)
                        added[grp] += 1
        else:
            import csv
            with open(path, encoding="utf-8-sig", newline="") as f:
                delim = "\t" if "\t" in open(path, encoding="utf-8").read(4096) else ","
                for row in csv.reader(f, delimiter=delim):
                    if len(row) >= 3 and row[0].strip() in ("positive", "negative"):
                        CONTROL_DRUGS[row[0].strip()].append(
                            (row[1].strip(), row[2].strip()))
                        added[row[0].strip()] += 1
    except Exception as e:  # noqa: BLE001 - extension best-effort
        print("[WARN] control pairs not loaded (%s): %s" % (path, e), file=sys.stderr)
    return added


def summarize_control_validation(records):
    """Aggregate the outcome of a --validate-controls run.

    `records`: list of dicts with keys
        drug, event, group ("positive"|"negative"),
        expected (bool), signal (bool, from compute().signal_overall).
    Returns agreement rates (proportion of pairs whose `signal` matches
    `expected`) for positive and negative controls, plus the raw records.
    """
    def _agree(rs):
        if not rs:
            return {"n": 0, "agree": 0, "rate": None}
        n = len(rs)
        hit = sum(1 for r in rs if bool(r.get("signal")) == bool(r.get("expected")))
        return {"n": n, "agree": hit, "rate": hit / n}

    pos = _agree([r for r in records if r.get("group") == "positive"])
    neg = _agree([r for r in records if r.get("group") == "negative"])
    return {
        "positive": pos,
        "negative": neg,
        "n_total": len(records),
        "records": records,
    }


def main():
    ap = argparse.ArgumentParser(description="Disproportionality from 2x2 table.")
    ap.add_argument("--a", type=float, default=None)
    ap.add_argument("--b", type=float, default=None)
    ap.add_argument("--c", type=float, default=None)
    ap.add_argument("--d", type=float, default=None)
    ap.add_argument("--in", dest="infile", help="read counts from fetch_faers JSON")
    ap.add_argument("--out", help="output JSON path")
    ap.add_argument("--soc", help="map a MedDRA PT to SOC (no 2x2 needed)")
    ap.add_argument("--bh", nargs="*", type=float, help="run Benjamini-Hochberg on p-values")
    ap.add_argument("--soc-map", help="user PT→SOC extension file (JSON/CSV); also "
                    "honors env CT_SAFETY_SOC_MAP (upgrade E)")
    args = ap.parse_args()

    # upgrade E: load user-supplied SOC map (explicit path wins, then env)
    _n = load_user_soc_map(args.soc_map) if args.soc_map else init_soc_map_from_env()
    if _n:
        print("[OK] user SOC map loaded: %d entries" % _n, file=sys.stderr)

    if args.soc:
        print(json.dumps({"pt": args.soc, "soc": map_soc(args.soc)},
                          ensure_ascii=False, indent=2))
        return
    if args.bh is not None:
        print(json.dumps({"q_values": benjamini_hochberg(args.bh)},
                         ensure_ascii=False, indent=2))
        return

    if args.infile:
        data = json.load(open(args.infile, encoding="utf-8"))
        cnt = data["counts"]
        a, b, c, d = cnt["a"], cnt["b"], cnt["c"], cnt["d"]
        drug, event = data.get("drug"), data.get("event")
    elif None not in (args.a, args.b, args.c, args.d):
        a, b, c, d = args.a, args.b, args.c, args.d
        drug = event = None
    else:
        ap.error("provide --a/--b/--c/--d, or --in, or use --soc/--bh (no 2x2 needed)")

    res = compute(a, b, c, d)
    if drug:
        res["drug"] = drug
    if event:
        res["event"] = event
        res["soc"] = map_soc(event)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
        print("[OK] wrote", args.out)
    else:
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
