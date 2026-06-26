#!/usr/bin/env bash
set -euo pipefail
DATA_DIR="${HOME}/.local/share/bytesagain-medical-scribe"
mkdir -p "$DATA_DIR"
_log() { echo "[$(date '+%H:%M:%S')] $*" >&2; }
_err() { echo "ERROR: $*" >&2; exit 1; }

cmd_soap() {
    local patient="" chief="" findings="" plan=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --patient) patient="$2"; shift 2 ;;
            --chief)   chief="$2";   shift 2 ;;
            --findings) findings="$2"; shift 2 ;;
            --plan)    plan="$2";    shift 2 ;;
            *) shift ;;
        esac
    done
    [[ -z "$patient" ]] && _err "Usage: soap --patient NAME --chief COMPLAINT --findings EXAM_FINDINGS [--plan PLAN]"
    local date_str; date_str=$(date '+%Y-%m-%d %H:%M')
    cat << EOF

═══════════════════════════════════════════════
SOAP NOTE
Date: $date_str
═══════════════════════════════════════════════

PATIENT: $patient

SUBJECTIVE:
  Chief Complaint: $chief
  History of Present Illness:
    Patient presents with $chief.
    Onset, duration, and associated symptoms require further documentation.
  Review of Systems: As per chief complaint. Full ROS to be completed.

OBJECTIVE:
  Vital Signs: To be documented
  Physical Examination:
    $findings
  Investigations: Pending / As ordered

ASSESSMENT:
  Working Diagnosis: Based on clinical presentation of "$chief" with findings: $chief
  Differential Diagnoses:
    1. [Primary diagnosis — document here]
    2. [Secondary differential — document here]
    3. [Tertiary differential — document here]

PLAN:
${plan:-  1. Further investigations as clinically indicated
  2. Treatment as per clinical guidelines
  3. Patient education and counseling
  4. Follow-up in [X] days / weeks
  5. Return precautions discussed}

───────────────────────────────────────────────
⚠️  DRAFT ONLY — Review and approve before use.
Powered by BytesAgain | bytesagain.com
EOF
}

cmd_discharge() {
    local patient="" diagnosis="" stay="" treatment="" followup=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --patient)   patient="$2";   shift 2 ;;
            --diagnosis) diagnosis="$2"; shift 2 ;;
            --stay)      stay="$2";      shift 2 ;;
            --treatment) treatment="$2"; shift 2 ;;
            --followup)  followup="$2";  shift 2 ;;
            *) shift ;;
        esac
    done
    [[ -z "$patient" ]] && _err "Usage: discharge --patient NAME --diagnosis DX --stay DURATION --treatment TX"
    cat << EOF

═══════════════════════════════════════════════
DISCHARGE SUMMARY
Date: $(date '+%Y-%m-%d')
═══════════════════════════════════════════════

PATIENT: $patient
ADMISSION DIAGNOSIS: $diagnosis
LENGTH OF STAY: $stay

HOSPITAL COURSE:
  Patient was admitted with $diagnosis.
  During the admission of $stay, the patient received:
  $treatment

DISCHARGE CONDITION: Stable / Improved (update as appropriate)

DISCHARGE MEDICATIONS:
  [Document all medications, doses, frequency, and duration]

DISCHARGE INSTRUCTIONS:
  1. Activity: As tolerated / Restricted (specify)
  2. Diet: Regular / Modified (specify)
  3. Wound care: N/A / As instructed
  4. Warning signs: Return to ED if worsening symptoms, fever >38.5°C, or any concerns

FOLLOW-UP:
  ${followup:-GP in 1–2 weeks / Specialist as arranged}

REFERRING PHYSICIAN: [Name, Clinic]
DISCHARGING PHYSICIAN: [Name, Signature]

───────────────────────────────────────────────
⚠️  DRAFT ONLY — Review and sign before release.
Powered by BytesAgain | bytesagain.com
EOF
}

cmd_referral() {
    local patient="" from="" to="" reason=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --patient) patient="$2"; shift 2 ;;
            --from)    from="$2";    shift 2 ;;
            --to)      to="$2";      shift 2 ;;
            --reason)  reason="$2";  shift 2 ;;
            *) shift ;;
        esac
    done
    [[ -z "$patient" || -z "$to" || -z "$reason" ]] && \
        _err "Usage: referral --patient NAME --from DEPT --to SPECIALIST --reason REASON"
    cat << EOF

═══════════════════════════════════════════════
REFERRAL LETTER
Date: $(date '+%Y-%m-%d')
═══════════════════════════════════════════════

To: $to
From: ${from:-General Practitioner}
Re: $patient

Dear Colleague,

I am writing to refer $patient for your expert assessment and management.

REASON FOR REFERRAL:
  $reason

CLINICAL BACKGROUND:
  [Document relevant history, investigations, and current medications]

CURRENT MANAGEMENT:
  [Document treatments initiated and response to date]

SPECIFIC REQUEST:
  I would appreciate your assessment, further investigation, and management
  recommendations regarding $reason.

Please do not hesitate to contact me if further information is required.

Yours sincerely,

[Referring Physician Name]
[Practice / Hospital]
[Contact details]

───────────────────────────────────────────────
⚠️  DRAFT ONLY — Review before sending.
Powered by BytesAgain | bytesagain.com
EOF
}

cmd_prescription() {
    local patient="" drug="" dose="" freq="" duration="" route="oral"
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --patient)  patient="$2";  shift 2 ;;
            --drug)     drug="$2";     shift 2 ;;
            --dose)     dose="$2";     shift 2 ;;
            --frequency) freq="$2";   shift 2 ;;
            --duration) duration="$2"; shift 2 ;;
            --route)    route="$2";    shift 2 ;;
            *) shift ;;
        esac
    done
    [[ -z "$patient" || -z "$drug" ]] && \
        _err "Usage: prescription --patient NAME --drug DRUG --dose DOSE --frequency FREQ --duration DUR"
    cat << EOF

═══════════════════════════════════════════════
PRESCRIPTION DRAFT
Date: $(date '+%Y-%m-%d')
═══════════════════════════════════════════════

PATIENT: $patient
DATE: $(date '+%Y-%m-%d')

Rx: $drug $dose
Route: $route
Frequency: ${freq:-as directed}
Duration: ${duration:-as directed}
Quantity: [Calculate based on dose × frequency × duration]

INSTRUCTIONS TO PATIENT:
  Take $drug $dose ${freq:-as directed} for ${duration:-the prescribed duration}.
  Complete the full course even if feeling better.
  Do not share this medication with others.

PRESCRIBER:
  Name: [Physician Name]
  License No: [License Number]
  Signature: ________________

───────────────────────────────────────────────
⚠️  DRAFT ONLY — Verify drug, dose, interactions before dispensing.
Powered by BytesAgain | bytesagain.com
EOF
}

cmd_template() {
    local list=false
    while [[ $# -gt 0 ]]; do
        case "$1" in --list) list=true; shift ;; *) shift ;; esac
    done
    cat << 'EOF'
Available Templates:
  soap         — SOAP note (Subjective/Objective/Assessment/Plan)
  discharge    — Discharge summary
  referral     — Specialist referral letter
  prescription — Prescription draft

Usage examples:
  bash scripts/script.sh soap --patient "John Doe, 45M" --chief "chest pain" --findings "BP 140/90"
  bash scripts/script.sh discharge --patient "Jane, 62F" --diagnosis "T2DM" --stay "3 days" --treatment "Metformin"
  bash scripts/script.sh referral --patient "Bob, 38M" --to "Cardiologist" --reason "arrhythmia"
  bash scripts/script.sh prescription --patient "Alice, 29F" --drug "Amoxicillin" --dose "500mg" --frequency "3x daily" --duration "7 days"
EOF
}

cmd_help() {
    cat << 'EOF'
Medical Scribe — Generate structured medical documents from clinical notes
Powered by BytesAgain | bytesagain.com

Commands:
  soap         Generate SOAP note
  discharge    Generate discharge summary
  referral     Generate specialist referral letter
  prescription Generate prescription draft
  template     List available templates
  help         Show this help

Usage:
  bash scripts/script.sh soap --patient "John Doe, 45M" --chief "chest pain 2 days" --findings "BP 140/90"
  bash scripts/script.sh discharge --patient "Jane, 62F" --diagnosis "Type 2 Diabetes" --stay "3 days" --treatment "Metformin 500mg"
  bash scripts/script.sh referral --patient "Bob, 38M" --from "GP" --to "Cardiologist" --reason "arrhythmia"
  bash scripts/script.sh prescription --patient "Alice, 29F" --drug "Amoxicillin" --dose "500mg" --frequency "3x daily" --duration "7 days"

⚠️  All output is AI-generated draft. Review by licensed professional required.
More AI skills: https://bytesagain.com/skills
Feedback: https://bytesagain.com/feedback/
EOF
}

case "${1:-help}" in
    soap)         shift; cmd_soap "$@" ;;
    discharge)    shift; cmd_discharge "$@" ;;
    referral)     shift; cmd_referral "$@" ;;
    prescription) shift; cmd_prescription "$@" ;;
    template)     shift; cmd_template "$@" ;;
    help|*)       cmd_help ;;
esac
