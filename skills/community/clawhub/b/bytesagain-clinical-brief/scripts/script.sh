#!/usr/bin/env bash
set -euo pipefail
DATA_DIR="${HOME}/.local/share/bytesagain-clinical-brief"
mkdir -p "$DATA_DIR"
_log() { echo "[$(date '+%H:%M:%S')] $*" >&2; }
_err() { echo "ERROR: $*" >&2; exit 1; }

cmd_summarize() {
    local notes=""
    while [[ $# -gt 0 ]]; do
        case "$1" in --notes) notes="$2"; shift 2 ;; *) shift ;; esac
    done
    [[ -z "$notes" ]] && _err "Usage: summarize --notes 'clinical notes text'"
    cat << EOF

═══════════════════════════════════════════════
CLINICAL BRIEF SUMMARY
Date: $(date '+%Y-%m-%d %H:%M')
═══════════════════════════════════════════════

RAW INPUT:
  $notes

STRUCTURED SUMMARY:

  PRESENTATION:
    $(echo "$notes" | grep -oiE "(presents|presenting|complaint|pain|fever|cough|dyspnea|nausea|vomiting|dizziness)[^,\.]*" | head -3 | sed 's/^/    /' || echo "    See raw notes above")

  KEY FINDINGS:
    Symptoms identified: $(echo "$notes" | grep -oiE "[0-9]+\.?[0-9]*\s*(°C|°F|mmHg|bpm|kg|mg|mmol)" | tr '\n' ' ' | head -c 200 || echo "Refer to raw notes")
    Abnormal values: To be flagged by clinician review

  CLINICAL PRIORITY:
    $(echo "$notes" | grep -iqE "severe|acute|emergency|critical|unstable" && echo "⚠️  HIGH — Urgent review indicated" || echo "Routine — Standard assessment")

  SUGGESTED NEXT STEPS:
    1. Complete history and physical examination
    2. Order investigations as clinically indicated
    3. Review differential diagnoses
    4. Initiate appropriate management

───────────────────────────────────────────────
⚠️  AI-generated summary. Clinical judgment required.
Powered by BytesAgain | bytesagain.com
EOF
}

cmd_differential() {
    local symptoms="" age="" sex=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --symptoms) symptoms="$2"; shift 2 ;;
            --age)      age="$2";      shift 2 ;;
            --sex)      sex="$2";      shift 2 ;;
            *) shift ;;
        esac
    done
    [[ -z "$symptoms" ]] && _err "Usage: differential --symptoms 'symptom1, symptom2' [--age N] [--sex M/F]"

    local patient_info="${age:-?}${sex:+$sex}"
    cat << EOF

═══════════════════════════════════════════════
DIFFERENTIAL DIAGNOSIS
Patient: ${patient_info:-Not specified}
═══════════════════════════════════════════════

PRESENTING SYMPTOMS: $symptoms

DIFFERENTIAL DIAGNOSES (consider in order of likelihood):

  1. [Most likely diagnosis based on symptom pattern]
     Supporting: Key features that fit
     Against: Features that don't fit

  2. [Second differential]
     Supporting: Key features
     Against: Key features

  3. [Third differential]
     Supporting: Key features
     Against: Key features

  4. [Must-not-miss diagnosis — even if less likely]
     Why consider: Serious if missed

SUGGESTED INVESTIGATIONS:
  Blood: FBC, CMP, LFT, CRP/ESR, Blood cultures (if febrile)
  Imaging: As clinically indicated
  Specific: Based on leading differential

SYMPTOM-SPECIFIC POINTERS:
$(echo "$symptoms" | tr ',' '\n' | while IFS= read -r s; do
    s=$(echo "$s" | xargs)
    case "${s,,}" in
        *fever*) echo "  → Fever: Consider infection, malignancy, autoimmune, drug fever" ;;
        *chest*pain*) echo "  → Chest pain: Exclude ACS, PE, aortic dissection first" ;;
        *dyspnea*|*breath*) echo "  → Dyspnea: Consider cardiac (HF, PE) vs pulmonary (pneumonia, asthma)" ;;
        *headache*) echo "  → Headache: Red flags — thunderclap, worst-ever, meningism" ;;
        *weight*loss*) echo "  → Weight loss: Malignancy screen, thyroid, diabetes, TB" ;;
        *) echo "  → $s: Clinical assessment required" ;;
    esac
done)

───────────────────────────────────────────────
⚠️  AI-generated list. Clinical judgment required.
Powered by BytesAgain | bytesagain.com
EOF
}

cmd_lab() {
    local results=""
    while [[ $# -gt 0 ]]; do
        case "$1" in --results) results="$2"; shift 2 ;; *) shift ;; esac
    done
    [[ -z "$results" ]] && _err "Usage: lab --results 'WBC 14.5, Hb 9.2, ...'"

    echo ""
    echo "═══════════════════════════════════════════════"
    echo "LAB RESULT INTERPRETATION"
    echo "Date: $(date '+%Y-%m-%d %H:%M')"
    echo "═══════════════════════════════════════════════"
    echo ""
    echo "INPUT: $results"
    echo ""
    echo "FLAGGED VALUES:"

    python3 - "$results" << 'PYEOF'
import sys, re

results_str = sys.argv[1]

# Reference ranges (adult)
RANGES = {
    "wbc": (4.0, 11.0, "×10⁹/L", "leukocytosis/leukopenia"),
    "hb": (12.0, 17.5, "g/dL", "anemia/polycythemia"),
    "hgb": (12.0, 17.5, "g/dL", "anemia/polycythemia"),
    "plt": (150, 400, "×10⁹/L", "thrombocytopenia/thrombocytosis"),
    "crp": (0, 10, "mg/L", "inflammation marker"),
    "esr": (0, 20, "mm/hr", "inflammation marker"),
    "creatinine": (0.6, 1.2, "mg/dL", "renal function"),
    "sodium": (136, 145, "mmol/L", "sodium imbalance"),
    "potassium": (3.5, 5.0, "mmol/L", "potassium imbalance"),
    "glucose": (70, 100, "mg/dL", "glycemia"),
    "tsh": (0.4, 4.0, "mIU/L", "thyroid function"),
    "troponin": (0, 0.04, "ng/mL", "cardiac injury"),
    "alt": (0, 40, "U/L", "liver function"),
    "ast": (0, 40, "U/L", "liver function"),
}

tokens = re.findall(r'([A-Za-z\-]+)\s*([\d\.]+)', results_str)
found_any = False
for name, val_str in tokens:
    key = name.lower()
    val = float(val_str)
    if key in RANGES:
        lo, hi, unit, context = RANGES[key]
        found_any = True
        if val < lo:
            print(f"  ⬇️  LOW  {name}: {val} {unit} (ref: {lo}–{hi}) — {context}")
        elif val > hi:
            print(f"  ⬆️  HIGH {name}: {val} {unit} (ref: {lo}–{hi}) — {context}")
        else:
            print(f"  ✅ NORMAL {name}: {val} {unit}")

if not found_any:
    print("  No recognized lab values found. Verify format: 'WBC 14.5, Hb 9.2, ...'")
PYEOF

    echo ""
    echo "CLINICAL INTERPRETATION:"
    echo "  Review flagged values in clinical context."
    echo "  Trend comparison with prior results recommended."
    echo ""
    echo "───────────────────────────────────────────────"
    echo "⚠️  Reference ranges are approximate adults. Adjust for age/sex/lab."
    echo "Powered by BytesAgain | bytesagain.com"
}

cmd_case_present() {
    local patient="" chief="" hx="" findings=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --patient)  patient="$2";  shift 2 ;;
            --chief)    chief="$2";    shift 2 ;;
            --hx)       hx="$2";       shift 2 ;;
            --findings) findings="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    cat << EOF

═══════════════════════════════════════════════
CASE PRESENTATION
Date: $(date '+%Y-%m-%d')
═══════════════════════════════════════════════

"$patient presenting with $chief"

HISTORY:
  $patient presents with a complaint of $chief.
  Past Medical History: ${hx:-Not documented}
  Medications: [Document current medications]
  Allergies: [NKDA / document allergies]
  Social History: [Smoking, alcohol, occupation]
  Family History: [Relevant family history]

EXAMINATION:
  General: [Patient appearance, distress level]
  Vital Signs: [T, HR, BP, RR, O2Sat, Weight]
  Systems Review:
    $findings

INVESTIGATIONS:
  [Bloods, imaging, ECG, other]

IMPRESSION:
  $patient with $chief — differential includes:
  1. [Primary diagnosis]
  2. [Secondary differential]

MANAGEMENT PLAN:
  [Investigations, treatment, disposition]

───────────────────────────────────────────────
⚠️  Draft for presentation. Review before presenting.
Powered by BytesAgain | bytesagain.com
EOF
}

cmd_specialty() {
    local type="general" notes=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --type)  type="$2";  shift 2 ;;
            --notes) notes="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    echo ""
    echo "═══════════════════════════════════════════════"
    echo "SPECIALTY BRIEF: $(echo "$type" | tr '[:lower:]' '[:upper:]')"
    echo "Date: $(date '+%Y-%m-%d %H:%M')"
    echo "═══════════════════════════════════════════════"
    echo ""
    echo "CLINICAL NOTES: $notes"
    echo ""
    case "${type,,}" in
        cardiology)
            echo "CARDIOLOGY FOCUS:"
            echo "  Rhythm: [ECG interpretation]"
            echo "  Function: [Echo/EF if available]"
            echo "  Vasculature: [Coronary/peripheral]"
            echo "  Key labs: Troponin, BNP, CK-MB, lipids"
            echo "  Risk scores: TIMI / GRACE / CHA2DS2-VASc as applicable"
            ;;
        neurology)
            echo "NEUROLOGY FOCUS:"
            echo "  GCS: [Score]"
            echo "  Focal deficits: [Motor, sensory, speech, vision]"
            echo "  Stroke scale: NIHSS if applicable"
            echo "  Key imaging: CT head, MRI brain"
            echo "  Consider: Seizure, stroke, meningitis, raised ICP"
            ;;
        oncology)
            echo "ONCOLOGY FOCUS:"
            echo "  Primary site: [Known/suspected]"
            echo "  Stage: [TNM staging if known]"
            echo "  Performance status: ECOG [0-4]"
            echo "  Current regimen: [Chemo/radiation/immunotherapy]"
            echo "  Key concerns: Neutropenia, pain, disease progression"
            ;;
        pulmonology)
            echo "PULMONOLOGY FOCUS:"
            echo "  Spirometry: FEV1/FVC ratio"
            echo "  O2 requirements: [Room air vs supplemental]"
            echo "  CXR/CT findings: [Document]"
            echo "  Consider: PNA, COPD exacerbation, PE, malignancy"
            ;;
        *)
            echo "GENERAL SPECIALTY BRIEF:"
            echo "  System involved: $type"
            echo "  Key findings: $notes"
            echo "  Suggested investigations: As clinically indicated"
            echo "  Referral considerations: Specialist review recommended"
            ;;
    esac
    echo ""
    echo "───────────────────────────────────────────────"
    echo "⚠️  AI-generated brief. Clinical judgment required."
    echo "Powered by BytesAgain | bytesagain.com"
}

cmd_help() {
    cat << 'EOF'
Clinical Brief — Summarize clinical cases into structured specialty briefs
Powered by BytesAgain | bytesagain.com

Commands:
  summarize      Summarize raw clinical notes into a structured brief
  differential   Generate differential diagnosis list from symptoms
  lab            Interpret lab results and flag abnormal values
  case-present   Format case for clinical presentation / handover
  specialty      Generate specialty-specific brief
  help           Show this help

Usage:
  bash scripts/script.sh summarize --notes "fever 39.2, productive cough, consolidation on CXR"
  bash scripts/script.sh differential --symptoms "fever, night sweats, weight loss" --age 35 --sex M
  bash scripts/script.sh lab --results "WBC 14.5, Hb 9.2, CRP 87, Creatinine 1.8"
  bash scripts/script.sh case-present --patient "55F" --chief "dyspnea" --hx "HTN, DM2" --findings "bilateral crackles"
  bash scripts/script.sh specialty --type cardiology --notes "STEMI, troponin 8.4"

Specialties: cardiology, neurology, oncology, pulmonology, gastroenterology
More: https://bytesagain.com/skills
Feedback: https://bytesagain.com/feedback/
EOF
}

case "${1:-help}" in
    summarize)     shift; cmd_summarize "$@" ;;
    differential)  shift; cmd_differential "$@" ;;
    lab)           shift; cmd_lab "$@" ;;
    case-present)  shift; cmd_case_present "$@" ;;
    specialty)     shift; cmd_specialty "$@" ;;
    help|*)        cmd_help ;;
esac
