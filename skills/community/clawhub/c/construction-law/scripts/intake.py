#!/usr/bin/env python3
"""
intake.py — Matter Intake Mode
Construction Law Skill v2.8.1

Usage:
    python3 scripts/intake.py
    python3 scripts/construction_law.py intake

Output formats:
    --format md (default)
    --format txt
    --output <filename>
    --file <input.json>      Non-interactive: read answers from JSON
    --save-matter <path>     Dump answered matter as JSON
"""

import argparse
import json
import sys
from datetime import datetime, date, timedelta


# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────

VERSION = "2.3.0"
DIVIDER = "━" * 44

CONTRACT_FORMS = {
    "1":  ("fidic-red",     "FIDIC Red (Measurement)"),
    "2":  ("fidic-yellow",  "FIDIC Yellow (Design & Build)"),
    "3":  ("fidic-silver",  "FIDIC Silver (EPC / Turnkey)"),
    "4":  ("fidic-gold",    "FIDIC Gold (DBO)"),
    "5":  ("fidic-emerald", "FIDIC Emerald (Underground)"),
    "6":  ("nec4-a",        "NEC4 Option A (Lump Sum)"),
    "7":  ("nec4-c",        "NEC4 Option C (Target Cost)"),
    "8":  ("psscoc",        "PSSCOC"),
    "9":  ("psscoc-db",     "PSSCOC D&B"),
    "10": ("sia",           "SIA Conditions"),
    "11": ("jct",           "JCT"),
    "12": ("bespoke",       "Bespoke / Other"),
}

# Display name when shown in output (form_label + edition rendered together)
FORM_DISPLAY = {
    "fidic-red":     "FIDIC Red",
    "fidic-yellow":  "FIDIC Yellow",
    "fidic-silver":  "FIDIC Silver",
    "fidic-gold":    "FIDIC Gold",
    "fidic-emerald": "FIDIC Emerald",
    "nec4-a":        "NEC4 Option A (Lump Sum)",
    "nec4-c":        "NEC4 Option C (Target Cost)",
    "psscoc":        "PSSCOC",
    "psscoc-db":     "PSSCOC D&B",
    "sia":           "SIA Conditions",
    "jct":           "JCT",
    "bespoke":       "Bespoke / Other",
}

COMMON_EDITIONS = {
    "fidic-red":     ["1999", "2017"],
    "fidic-yellow":  ["1999", "2017"],
    "fidic-silver":  ["1999", "2017"],
    "fidic-gold":    ["2008"],
    "fidic-emerald": ["2019"],
    "nec4-a":        ["NEC3", "NEC4"],
    "nec4-c":        ["NEC3", "NEC4"],
    "psscoc":        ["2017 (7th Ed)", "2020 (8th Ed)"],
    "psscoc-db":     ["2014 (6th Ed)", "2020 (7th Ed)"],
    "sia":           ["9th Ed (2010)", "11th Ed"],
    "jct":           ["2016", "2024"],
    "bespoke":       [],
}

GOVERNING_LAWS = {
    "1": "Singapore",
    "2": "England & Wales",
    "3": "Hong Kong",
    "4": "UAE / DIFC",
    "5": "Other",
}

PROCUREMENT_TYPES = {
    "1": "Measure & Pay",
    "2": "Lump Sum",
    "3": "Design & Build",
    "4": "EPC / Turnkey",
    "5": "DBO (Design, Build, Operate)",
    "6": "Unknown / Not applicable",
}

AMENDMENT_STATUS = {
    "1": "yes",
    "2": "no",
    "3": "unknown",
}

ISSUE_TYPES = {
    "1": "Delay / Extension of Time (EOT)",
    "2": "Disruption / Loss of Productivity",
    "3": "Variation / Change Order",
    "4": "Payment / Certification",
    "5": "Termination",
    "6": "Defect / Design Liability",
    "7": "Dispute / Enforcement",
    "8": "Other",
}

PARTIES = {
    "1": "Contractor",
    "2": "Employer / Owner",
    "3": "Subcontractor",
    "4": "Consultant / Engineer",
    "5": "Other / Neutral",
}

OBJECTIVES = {
    "1": "Extension of Time (EOT)",
    "2": "Additional payment / prolongation costs",
    "3": "Both EOT and additional payment",
    "4": "Defend a claim made against us",
    "5": "Assess risk and exposure",
    "6": "Prepare for dispute / adjudication / arbitration",
    "7": "General contract review",
}

URGENCY = {
    "1": "Immediate — deadline within 7 days",
    "2": "Short-term — within 30 days",
    "3": "Medium-term — within 3 months",
    "4": "Planning ahead — no immediate deadline",
}

CONFIDENCE_ICONS = {
    "high":   "✅ High confidence",
    "medium": "⚠️ Medium confidence",
    "review": "❗ Needs review",
}


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def divider():
    print(DIVIDER)


def header(title):
    print()
    divider()
    print(f" {title}")
    divider()
    print()


def prompt_choice(options, allow_skip=False):
    for key, label in options.items():
        print(f" {key:>2}. {label}")
    print()
    while True:
        raw = input("Enter number: ").strip()
        if allow_skip and raw == "":
            return ""
        if raw in options:
            return raw
        print(f" ⚠️ Invalid choice. Enter one of: {', '.join(options.keys())}")


def prompt_date(label, allow_skip=False):
    hint = " (or press Enter to skip)" if allow_skip else ""
    while True:
        raw = input(f"{label}{hint}: ").strip()
        if allow_skip and raw == "":
            return None
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            print(" ⚠️ Invalid date. Use YYYY-MM-DD format (e.g. 2026-05-04).")


def prompt_text(label, allow_skip=False):
    hint = " (or press Enter to skip)" if allow_skip else ""
    return input(f"{label}{hint}: ").strip()


def days_from(start, days):
    return start + timedelta(days=days)


def format_date(d):
    return d.strftime("%Y-%m-%d") if d else "Not provided"


def parse_date_safe(s):
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def form_label_full(form_id, edition):
    """Render 'FIDIC Red 1999' or 'PSSCOC 2020 (8th Ed)' style display."""
    base = FORM_DISPLAY.get(form_id, form_id)
    if not edition or edition == "Unknown":
        return base
    # Avoid duplication for NEC ("NEC4 Option C" + "NEC4")
    if edition.lower() in base.lower():
        return base
    return f"{base} {edition}"


# ─────────────────────────────────────────────
# DATA TABLES
# ─────────────────────────────────────────────

# Key: (form_id_prefix, issue_key)
# form_id_prefix: matches start of form_id (e.g. "fidic-red" matches fidic-red for any edition)
# issue_key: "1"=delay, "2"=disruption, "3"=variation, "4"=payment, "5"=termination, "6"=defect, "7"=dispute

def _form_prefix(form_id):
    """Normalize form_id to a lookup prefix."""
    # nec4-a and nec4-c → nec4
    if form_id.startswith("nec4"):
        return "nec4"
    # psscoc-db → psscoc
    if form_id.startswith("psscoc"):
        return "psscoc"
    return form_id


CLAUSE_BUCKETS = {
    # FIDIC 1999
    ("fidic-red", "1999", "1"): {  # delay
        "primary": [
            ("2.1", "Right of Access to Site"),
            ("8.4", "Extension of Time for Completion"),
            ("20.1", "Contractor's Claims"),
        ],
        "supporting": [
            ("1.9", "Delayed Drawings or Instructions"),
            ("8.3", "Programme"),
            ("17.4", "Consequences of Employer's Risks"),
        ],
    },
    ("fidic-red", "1999", "2"): {  # disruption
        "primary": [
            ("8.4", "Extension of Time for Completion"),
            ("20.1", "Contractor's Claims"),
        ],
        "supporting": [
            ("8.3", "Programme"),
            ("13.7", "Adjustments for Changes in Legislation"),
            ("17.4", "Consequences of Employer's Risks"),
        ],
    },
    ("fidic-red", "1999", "3"): {  # variation
        "primary": [
            ("13.1", "Right to Vary"),
            ("13.3", "Variation Procedure"),
            ("12.3", "Evaluation"),
        ],
        "supporting": [
            ("3.3", "Instructions of the Engineer"),
            ("20.1", "Contractor's Claims"),
        ],
    },
    ("fidic-red", "1999", "4"): {  # payment
        "primary": [
            ("14.3", "Application for Interim Payment Certificates"),
            ("14.6", "Issue of Interim Payment Certificates"),
            ("14.7", "Payment"),
        ],
        "supporting": [
            ("14.8", "Delayed Payment"),
            ("16.1", "Contractor's Entitlement to Suspend Work"),
            ("20.1", "Contractor's Claims"),
        ],
    },
    ("fidic-red", "1999", "5"): {  # termination
        "primary": [
            ("15.2", "Termination by Employer"),
            ("16.2", "Termination by Contractor"),
        ],
        "supporting": [
            ("15.1", "Notice to Correct"),
            ("16.1", "Contractor's Entitlement to Suspend Work"),
            ("19.6", "Optional Termination, Payment and Release"),
        ],
    },
    ("fidic-red", "1999", "6"): {  # defect
        "primary": [
            ("11.1", "Completion of Outstanding Work and Remedying Defects"),
            ("11.2", "Cost of Remedying Defects"),
        ],
        "supporting": [
            ("7.5", "Rejection"),
            ("7.6", "Remedial Work"),
            ("11.4", "Failure to Remedy Defects"),
        ],
    },
    ("fidic-red", "1999", "7"): {  # dispute
        "primary": [
            ("20.2", "Appointment of the Dispute Adjudication Board"),
            ("20.4", "Obtaining Dispute Adjudication Board's Decision"),
            ("20.6", "Arbitration"),
        ],
        "supporting": [
            ("20.5", "Amicable Settlement"),
        ],
    },
    # FIDIC 2017
    ("fidic-red", "2017", "1"): {  # delay
        "primary": [
            ("2.1", "Right of Access to and Possession of the Site"),
            ("8.5", "Extension of Time for Completion"),
            ("20.2.1", "Notice of Claim"),
        ],
        "supporting": [
            ("1.9", "Delayed Drawings or Instructions"),
            ("8.3", "Programme"),
            ("20.2.4", "Fully Detailed Claim"),
        ],
    },
    ("fidic-red", "2017", "3"): {  # variation
        "primary": [
            ("13.1", "Right to Vary"),
            ("13.3", "Variation Procedure"),
            ("13.6", "Adjustments for Changes in Laws"),
        ],
        "supporting": [
            ("3.5", "Instructions of the Engineer"),
            ("20.2.1", "Notice of Claim"),
        ],
    },
    ("fidic-red", "2017", "4"): {  # payment
        "primary": [
            ("14.3", "Application for Interim Payment Certificates"),
            ("14.6", "Interim Payment"),
            ("14.7", "Payment of Retained Amount"),
        ],
        "supporting": [
            ("14.8", "Delayed Payment"),
            ("16.1", "Contractor's Entitlement to Suspend Work"),
            ("20.2.1", "Notice of Claim"),
        ],
    },
    ("fidic-red", "2017", "7"): {  # dispute
        "primary": [
            ("21.1", "Constitution of the DAAB"),
            ("21.4", "Obtaining DAAB's Decision"),
            ("21.6", "Arbitration"),
        ],
        "supporting": [
            ("21.5", "Amicable Settlement"),
        ],
    },
    # PSSCOC (both editions share same clause structure)
    ("psscoc", "any", "1"): {  # delay
        "primary": [
            ("14", "Delay and Extension of Time"),
            ("23", "Notices"),
        ],
        "supporting": [
            ("32", "Payment"),
            ("37", "Final Certificate"),
        ],
    },
    ("psscoc", "any", "3"): {  # variation
        "primary": [
            ("12", "Variation of Works"),
            ("23", "Notices"),
        ],
        "supporting": [
            ("31", "Interim Certificates"),
            ("32", "Payment"),
        ],
    },
    ("psscoc", "any", "4"): {  # payment
        "primary": [
            ("31", "Interim Certificates"),
            ("32", "Payment"),
            ("37", "Final Certificate"),
        ],
        "supporting": [
            ("SOP Act s.10", "Payment Claim"),
            ("SOP Act s.11", "Payment Response"),
            ("SOP Act s.12", "Entitlement to Adjudicate"),
        ],
    },
    ("psscoc", "any", "5"): {  # termination
        "primary": [
            ("33", "Termination by Employer"),
            ("34", "Termination by Contractor"),
        ],
        "supporting": [
            ("23", "Notices"),
        ],
    },
    # NEC4 (both options share clause numbering)
    ("nec4", "any", "1"): {  # delay
        "primary": [
            ("60.1(2)", "Compensation Events — access delay"),
            ("61", "Notifying Compensation Events"),
            ("62", "Quotations for Compensation Events"),
            ("63", "Assessing Compensation Events"),
        ],
        "supporting": [
            ("15", "Early Warning"),
            ("10.1", "Mutual Trust and Cooperation"),
            ("64", "Project Manager's Assessment"),
        ],
    },
    ("nec4", "any", "3"): {  # variation
        "primary": [
            ("60.1(1)", "Compensation Events — PM instruction changing scope"),
            ("61", "Notifying Compensation Events"),
            ("62", "Quotations for Compensation Events"),
            ("63", "Assessing Compensation Events"),
            ("64", "Project Manager's Assessment"),
        ],
        "supporting": [
            ("10.1", "Mutual Trust and Cooperation"),
            ("15", "Early Warning"),
            ("54", "Activity Schedule / Bill of Quantities"),
            ("53", "Pain / Gain Share"),
        ],
    },
    ("nec4", "any", "4"): {  # payment
        "primary": [
            ("50", "Assessing the Amount Due"),
            ("51", "Payment"),
        ],
        "supporting": [
            ("60.1", "Compensation Events"),
            ("53", "Pain / Gain Share"),
        ],
    },
    ("nec4", "any", "7"): {  # dispute
        "primary": [
            ("W1", "Dispute Resolution — Adjudication"),
            ("W2", "Dispute Resolution — Tribunal"),
        ],
        "supporting": [
            ("15", "Early Warning"),
        ],
    },
    # SIA
    ("sia", "any", "1"): {  # delay
        "primary": [
            ("23", "Extension of Time"),
            ("24", "Damages for Non-Completion"),
        ],
        "supporting": [
            ("11", "Instructions of Architect"),
            ("23", "Notices"),
        ],
    },
    ("sia", "any", "3"): {  # variation
        "primary": [
            ("12", "Variations"),
            ("13", "Valuation of Variations"),
        ],
        "supporting": [
            ("11", "Instructions of Architect"),
            ("23", "Extension of Time"),
        ],
    },
    ("sia", "any", "4"): {  # payment
        "primary": [
            ("31", "Interim Certificates"),
            ("32", "Payment"),
        ],
        "supporting": [
            ("SOP Act s.10", "Payment Claim"),
            ("SOP Act s.11", "Payment Response"),
        ],
    },
    ("sia", "any", "5"): {  # termination
        "primary": [
            ("33", "Determination by Employer"),
            ("34", "Determination by Contractor"),
        ],
        "supporting": [
            ("24", "Damages for Non-Completion"),
            ("23", "Extension of Time"),
            ("32", "Payment on Determination"),
        ],
    },
}

# Notice rules: keyed by (form_prefix, issue_key)
# period_days: number of days (or weeks*7)
# clause: clause reference
# trigger: "awareness" | "event" | "instruction"
NOTICE_RULES = {
    ("fidic-red", "1999"): {
        "clause": "20.1",
        "clause_name": "Contractor's Claims",
        "period_days": 28,
        "trigger": "awareness",
        "consequence": "Engineer may reject claim as time-barred",
        "note": "Time-bar under FIDIC 1999 Clause 20.1 is strict.",
    },
    ("fidic-red", "2017"): {
        "clause": "20.2.1",
        "clause_name": "Notice of Claim",
        "period_days": 28,
        "trigger": "awareness",
        "consequence": "Potential time-bar — claim lost if notice not given",
        "note": "FIDIC 2017 Clause 20.2.7 provides Engineer late-notice safeguard.",
    },
    ("fidic-yellow", "1999"): {
        "clause": "20.1",
        "clause_name": "Contractor's Claims",
        "period_days": 28,
        "trigger": "awareness",
        "consequence": "Engineer may reject claim as time-barred",
        "note": "Same time-bar regime as Red Book 1999.",
    },
    ("fidic-yellow", "2017"): {
        "clause": "20.2.1",
        "clause_name": "Notice of Claim",
        "period_days": 28,
        "trigger": "awareness",
        "consequence": "Potential time-bar — claim lost if notice not given",
        "note": "Same regime as Red Book 2017.",
    },
    ("fidic-silver", "1999"): {
        "clause": "20.1",
        "clause_name": "Contractor's Claims",
        "period_days": 28,
        "trigger": "awareness",
        "consequence": "Claim time-barred",
        "note": "Silver Book 1999 follows same Clause 20.1 regime.",
    },
    ("fidic-silver", "2017"): {
        "clause": "20.2.1",
        "clause_name": "Notice of Claim",
        "period_days": 28,
        "trigger": "awareness",
        "consequence": "Potential time-bar",
        "note": "Silver Book 2017 follows same Clause 20.2.1 regime.",
    },
    ("nec4", "any"): {
        "clause": "61.3",
        "clause_name": "Contractor Notification of Compensation Event",
        "period_days": 56,  # 8 weeks
        "trigger": "awareness",
        "consequence": "Failure to notify bars Contractor from claiming change to Prices or Completion Date",
        "note": "NEC4 also requires early warning under Clause 15 as soon as aware.",
    },
    ("psscoc", "any"): {
        "clause": "23",
        "clause_name": "Notices",
        "period_days": 28,
        "trigger": "event",
        "consequence": "Delay weakens contractual position",
        "note": "SOP Act provides parallel statutory route — claim/response/adjudication.",
    },
    ("sia", "any"): {
        "clause": "23",
        "clause_name": "Extension of Time Notice",
        "period_days": 28,
        "trigger": "event",
        "consequence": "Late notice may prejudice entitlement",
        "note": "SOP Act provides parallel statutory route.",
    },
}

# Amendment sensitivity per form prefix
AMENDMENT_FLAGS_DB = {
    "fidic-red": [
        "Notice period (Clause 20.1/20.2.1) — often shortened",
        "EOT entitlement grounds (Clause 8.4/8.5) — often narrowed",
        "Engineer's certification powers — sometimes replaced by Employer's Representative",
        "Prolongation cost recovery — sometimes excluded or capped",
        "DAAB composition and appointment — sometimes removed",
        "Limitation of liability — sometimes capped",
    ],
    "fidic-yellow": [
        "Notice period (Clause 20.1/20.2.1) — often shortened",
        "Design liability standard — fitness for purpose vs skill and care",
        "Employer's Requirements definition — scope creep risk",
        "Engineer's certification powers — sometimes replaced",
        "Performance guarantees — sometimes added or expanded",
    ],
    "fidic-silver": [
        "Risk allocation — further loading onto Contractor",
        "Unforeseeable conditions — sometimes entirely excluded",
        "Employer's Requirements — definition scope",
        "Force majeure — sometimes narrowed",
        "Time-bar periods — sometimes shortened",
    ],
    "nec4": [
        "Shortened notification periods (Clause 61.3)",
        "Modified pain/gain share percentages",
        "Additional compensation event categories added or removed",
        "Changed PM assessment timescales",
        "Z-clauses overriding standard allocation",
        "W-clause dispute resolution modifications",
    ],
    "psscoc": [
        "EOT entitlement grounds — sometimes narrowed",
        "Superintending Officer powers — sometimes modified",
        "LD cap — sometimes increased",
        "Defects liability period — sometimes extended",
        "Payment terms — sometimes modified from standard 21/35 days",
    ],
    "sia": [
        "Architect's certification powers — sometimes curtailed",
        "EOT grounds — sometimes narrowed",
        "LD regime — sometimes modified",
        "Arbitration clause — sometimes replaced with litigation",
        "Retention percentage — sometimes increased",
    ],
    "jct": [
        "Relevant Events list — sometimes restricted",
        "Relevant Matters for loss/expense — sometimes restricted",
        "Determination provisions — sometimes modified",
        "Insurance provisions — sometimes enhanced",
    ],
}

# Governing law cautions
GOVERNING_LAW_CAUTIONS = {
    "Singapore": [
        "Time-bars are generally strictly enforced",
        "No general duty of good faith in Singapore contract law unless express",
        "Prevention principle may apply if Employer caused delay without EOT mechanism",
        "SOP Act may provide parallel payment rights independent of contract",
    ],
    "England & Wales": [
        "NEC4 Clause 10.1 imposes express mutual trust and cooperation obligation",
        "No general good faith duty beyond express terms",
        "Compensation event regime is exhaustive — claims outside Clause 60.1 list are generally not recoverable",
        "UK Housing Grants Act adjudication rights apply independently of contract",
        "Prevention principle recognised under English law",
    ],
    "Hong Kong": [
        "Time-bars are generally strictly enforced under Hong Kong law",
        "No general duty of good faith unless express",
        "Prevention principle applies (similar to English law)",
        "Arbitration is the predominant dispute mechanism (HKIAC)",
        "Security of Payment Legislation introduced 2024 — check applicability",
    ],
    "UAE / DIFC": [
        "UAE Civil Code may imply good faith obligations",
        "Time-bar provisions may be subject to court interpretation",
        "DIFC courts provide common-law-style jurisdiction",
        "Expert determination increasingly used in construction disputes",
        "Statutory limitation periods may override contractual time-bars",
    ],
}

# Evidence checklists per issue_key
EVIDENCE_CHECKLISTS = {
    "1": [  # delay
        "Notice(s) issued and acknowledged",
        "Baseline programme (approved)",
        "Updated programme showing delay impact",
        "Delay event records (site diary, photos, weather)",
        "Correspondence confirming cause of delay",
        "Contemporaneous records of impact",
        "Cost records (if claiming prolongation)",
        "As-built programme or delay analysis",
    ],
    "2": [  # disruption
        "Notice(s) issued and acknowledged",
        "Productivity records (planned vs actual)",
        "Measured mile comparison data",
        "Labour and plant records",
        "Site instructions causing disruption",
        "Programme showing concurrent activities",
        "Cost records (labour, plant, preliminaries)",
    ],
    "3": [  # variation
        "Written instruction or direction (VO/SI/AI)",
        "Scope change clearly documented",
        "Original scope / specification for comparison",
        "Quotation or daywork records",
        "Programme impact assessment",
        "Cost build-up (rates, quantities, resources)",
        "Correspondence trail confirming instruction",
    ],
    "4": [  # payment
        "Payment claim submitted — date, amount, contents",
        "Certificate issued or withheld — confirm",
        "Payment response received — if any",
        "Valuation records supporting claim amount",
        "Correspondence with certifier",
        "Contract payment schedule / milestone dates",
        "Proof of service of payment claim (for SOP Act)",
    ],
    "5": [  # termination
        "All contractual notices served in sequence",
        "Cure period compliance documented",
        "Records of default / breach",
        "Valuation of work done to termination date",
        "Plant and materials on site — inventory",
        "Handover arrangements and documentation",
    ],
    "6": [  # defect
        "Defect notification and response records",
        "Inspection reports (joint and independent)",
        "Design documents and specifications",
        "Testing and commissioning records",
        "Remedial work proposals and costs",
        "Correspondence on liability",
    ],
    "7": [  # dispute
        "Complete notice and correspondence trail",
        "Claim submissions (all versions)",
        "Engineer/Architect determinations",
        "Settlement correspondence (without prejudice)",
        "Expert reports (if any)",
        "Witness statements / factual chronology",
    ],
}

# Missing info checklists per issue_key (what users often forget)
MISSING_INFO_DB = {
    "1": [  # delay
        "Exact clause wording (amended?)",
        "Baseline programme (approved version)",
        "Programme updates showing delay impact",
        "Correspondence confirming cause of delay",
        "Site records confirming access denial / delay",
        "Prolongation cost records (if claiming money)",
    ],
    "2": [  # disruption
        "Productivity baseline records",
        "Measured mile or comparison data",
        "Site instructions causing disruption",
        "Labour allocation records",
        "Cost records (labour, plant, preliminaries)",
    ],
    "3": [  # variation
        "Written instruction (VO/SI/AI) — dated",
        "Original scope/specification for comparison",
        "Cost build-up for quotation",
        "Programme impact on Completion Date",
        "Correspondence confirming instruction",
    ],
    "4": [  # payment
        "Payment claim — date, amount, contents",
        "Certificate issued or withheld",
        "Payment response — if any",
        "Valuation records supporting amount",
        "SOP Act payment claim — served correctly?",
    ],
    "5": [  # termination
        "Sequence of contractual notices",
        "Cure period documentation",
        "Records of breach/default",
        "Valuation of work to termination date",
    ],
    "6": [  # defect
        "Defect notification records",
        "Inspection reports",
        "Design documents and specifications",
        "Remedial work cost estimates",
    ],
    "7": [  # dispute
        "Complete notice trail",
        "All claim submissions (versions)",
        "Engineer/Architect determinations",
        "Legal advice received (if any)",
    ],
}

# Confidence labels per issue_key
CONFIDENCE_MAP = {
    "1": [  # delay
        ("Deadline calculation", "high"),
        ("Clause identification", "high"),
        ("Time-bar risk assessment", "high"),
        ("EOT entitlement", "medium"),
        ("Prolongation recovery", "review"),
        ("Amendment impact", "review"),
    ],
    "2": [  # disruption
        ("Deadline calculation", "high"),
        ("Clause identification", "high"),
        ("Disruption entitlement", "medium"),
        ("Quantum / productivity loss", "review"),
        ("Causation", "review"),
    ],
    "3": [  # variation
        ("Deadline calculation", "high"),
        ("Clause identification", "high"),
        ("Compensation event status", "medium"),
        ("Quotation assessment", "review"),
        ("Programme impact", "review"),
    ],
    "4": [  # payment
        ("SOP Act timeline", "high"),
        ("Contractual clause mapping", "high"),
        ("Adjudication entitlement", "medium"),
        ("Quantum / valuation", "review"),
        ("Smash-and-grab risk", "medium"),
    ],
    "5": [  # termination
        ("Notice sequence", "high"),
        ("Clause identification", "high"),
        ("Validity of termination", "medium"),
        ("Quantum / final account", "review"),
    ],
    "6": [  # defect
        ("Clause identification", "high"),
        ("Defect liability period", "high"),
        ("Design responsibility", "medium"),
        ("Remedial cost allocation", "review"),
    ],
    "7": [  # dispute
        ("Procedural requirements", "high"),
        ("Clause identification", "high"),
        ("Dispute route options", "medium"),
        ("Merits assessment", "review"),
        ("Quantum", "review"),
    ],
}

# Next steps per issue_key (templates with placeholders)
NEXT_STEPS_DB = {
    "1": [  # delay
        "Review Particular Conditions for amendments to notice/EOT clauses",
        "Secure site access records and correspondence",
        "Update programme to show delay impact",
        "Begin prolongation cost records immediately",
        "Prepare full EOT application using claims template",
    ],
    "2": [  # disruption
        "Quantify productivity loss using measured mile or comparison",
        "Document all site instructions causing disruption",
        "Prepare disruption claim using claims template",
        "Review contract for global claims restrictions",
    ],
    "3": [  # variation
        "Confirm written instruction exists and is dated",
        "Prepare cost build-up for quotation",
        "Update programme to show impact on Completion",
        "Submit quotation within contractual timeframe",
    ],
    "4": [  # payment
        "Confirm whether valid SOP Act payment claim has been served",
        "If not — serve a compliant payment claim immediately",
        "Run SOP calculator to map all deadlines",
        "Write formally to certifier requesting certification",
        "Preserve all valuation records and correspondence",
        "If payment response is inadequate — consider adjudication",
    ],
    "5": [  # termination
        "Verify all contractual pre-conditions met",
        "Check cure period has expired without remedy",
        "Secure valuation of work done to date",
        "Plan handover logistics and documentation",
    ],
    "6": [  # defect
        "Confirm defect is notified within DLP",
        "Obtain independent inspection report",
        "Review design responsibility allocation",
        "Prepare cost estimate for remedial work",
    ],
    "7": [  # dispute
        "Confirm all pre-arbitration/adjudication steps completed",
        "Review contractual dispute escalation mechanism",
        "Gather all notices, claims, and determinations",
        "Seek legal advice on merits and procedure",
    ],
}


# ─────────────────────────────────────────────
# ANALYSIS ENGINE
# ─────────────────────────────────────────────

def _lookup_clause_buckets(form_id, edition, issue_key):
    """Look up clause buckets with fallback: exact → any edition → generic."""
    prefix = _form_prefix(form_id)
    # Try exact form + edition + issue
    key = (form_id, edition, issue_key)
    if key in CLAUSE_BUCKETS:
        return CLAUSE_BUCKETS[key]
    # Try form + "any" + issue
    key = (prefix, "any", issue_key)
    if key in CLAUSE_BUCKETS:
        return CLAUSE_BUCKETS[key]
    # Try fidic-red editions as fallback for other fidic forms
    if form_id.startswith("fidic"):
        for ed in ("1999", "2017", "any"):
            key = ("fidic-red", ed, issue_key)
            if key in CLAUSE_BUCKETS:
                return CLAUSE_BUCKETS[key]
    return None


def _lookup_notice_rule(form_id, edition):
    """Look up notice rules with fallback."""
    prefix = _form_prefix(form_id)
    # Exact form + edition
    key = (form_id, edition)
    if key in NOTICE_RULES:
        return NOTICE_RULES[key]
    # Prefix + edition
    key = (prefix, edition)
    if key in NOTICE_RULES:
        return NOTICE_RULES[key]
    # Prefix + "any"
    key = (prefix, "any")
    if key in NOTICE_RULES:
        return NOTICE_RULES[key]
    return None


def build_issue_summary(a, b, c, d):
    """Generate 2-3 sentence issue summary."""
    form_display = form_label_full(a["form_id"], a["edition"])
    issue = b["issue_type"].lower()
    party = b["party"].lower()
    gov = a["governing_law"]
    desc = b.get("description", "")

    summary = (
        f"This appears to be a {issue} issue under "
        f"{form_display} (governed by {gov})"
    )
    if desc:
        summary += f", arising from {desc.lower().rstrip('.')}"
    summary += f". Acting for the {party}."

    # Add objective context
    obj = d["objective"]
    if "EOT" in obj and "payment" in obj.lower():
        summary += (
            " The party may have entitlement to both an extension of time "
            "and additional costs, subject to notice compliance and "
            "causation evidence."
        )
    elif "EOT" in obj:
        summary += (
            " The party may have entitlement to an extension of time, "
            "subject to notice compliance."
        )
    elif "payment" in obj.lower():
        summary += (
            " Additional payment may be recoverable, subject to "
            "proper substantiation."
        )

    # Amendment caveat
    if a["amendment_status"] in ("yes", "unknown"):
        summary += (
            f"\n\n⚠️ Amendment status is {a['amendment_status']}. "
            "All conclusions below are provisional pending review of "
            "Particular Conditions."
        )

    return summary


def build_clause_buckets(a, b):
    """Return formatted clause bucket lines."""
    data = _lookup_clause_buckets(a["form_id"], a["edition"], b["issue_key"])
    if not data:
        return [
            "Primary:",
            "  - [No clause data available for this form/issue combination]",
            "",
            "Supporting:",
            "  - [Consult the contract directly]",
        ]

    lines = ["Primary:"]
    for ref, name in data["primary"]:
        lines.append(f"  - Clause {ref:<8} {name}")
    lines.append("")
    lines.append("Supporting:")
    for ref, name in data["supporting"]:
        lines.append(f"  - Clause {ref:<8} {name}")
    return lines


def build_deadline_check(a, b, c):
    """Calculate notice deadlines and produce formatted output."""
    rule = _lookup_notice_rule(a["form_id"], a["edition"])
    lines = []

    if not rule:
        lines.append("No specific notice rule data for this form/edition.")
        lines.append("Consult the contract for notice requirements.")
        return lines

    clause = rule["clause"]
    clause_name = rule["clause_name"]
    period = rule["period_days"]
    trigger = rule["trigger"]
    consequence = rule["consequence"]
    note = rule["note"]

    lines.append(f"Clause {clause} — {clause_name}")

    if c["awareness_date"]:
        trigger_date = c["awareness_date"] if trigger == "awareness" else c.get("event_date") or c["awareness_date"]
        deadline = days_from(trigger_date, period)
        today = date.today()

        trigger_label = "Awareness" if trigger == "awareness" else "Occurrence"
        lines.append(f"  Trigger:   {trigger_label} of event ({format_date(trigger_date)})")
        lines.append(f"  Deadline:  {period} days → {format_date(deadline)}")

        if c["notice_served"]:
            if c["notice_date"] and c["notice_date"] <= deadline:
                lines.append(f"  Status:    ✅ Notice served on time ({format_date(c['notice_date'])})")
            elif c["notice_date"] and c["notice_date"] > deadline:
                lines.append(f"  Status:    ❗ Notice served LATE ({format_date(c['notice_date'])})")
                lines.append(f"  Risk:      {consequence}")
            else:
                lines.append(f"  Status:    ✅ Notice served (date unconfirmed)")
        else:
            if today > deadline:
                days_late = (today - deadline).days
                lines.append(f"  Status:    ❗ OVERDUE — notice not yet served ({days_late} days past deadline)")
                lines.append(f"  Risk:      {consequence}")
                lines.append(f"  Action:    Serve notice immediately and seek")
                lines.append(f"             agreement to accept late notice")
            elif (deadline - today).days <= 7:
                days_left = (deadline - today).days
                lines.append(f"  Status:    ⚠️ At risk — {days_left} days remaining")
                lines.append(f"  Risk:      {consequence}")
                lines.append(f"  Action:    Serve notice urgently")
            else:
                days_left = (deadline - today).days
                lines.append(f"  Status:    ✅ Within window — {days_left} days remaining")
                lines.append(f"  Action:    Serve notice promptly — do not wait")

        if note:
            lines.append("")
            lines.append(f"⚠️ {note}")
    else:
        lines.append(f"  Period:    {period} days from {trigger}")
        lines.append(f"  Risk:      {consequence}")
        lines.append("")
        lines.append("  ⚠️ No awareness/event date provided — cannot calculate deadline.")
        lines.append("     Provide dates to enable time-bar assessment.")

    return lines


def build_amendment_flags(a):
    """Return amendment sensitivity warnings."""
    if a["amendment_status"] == "no":
        prefix = _form_prefix(a["form_id"])
        note = ""
        if prefix == "psscoc":
            note = "\n   Note: PSSCOC is a Singapore public sector form.\n   Amendments are less common but do occur. Verify if in doubt."
        elif prefix == "nec4":
            note = "\n   Note: NEC4 Option C contracts are frequently\n   amended in practice. Verify W-clauses and Z-clauses."
        return [f"✅ No amendments reported — standard form applies.{note}"]

    prefix = _form_prefix(a["form_id"])
    flags = AMENDMENT_FLAGS_DB.get(prefix, AMENDMENT_FLAGS_DB.get(a["form_id"], []))

    status_word = a["amendment_status"].upper()
    lines = [
        f"⚠️ Amendment status is {status_word}. The following areas",
        "   are commonly modified and may change the standard",
        "   position:",
        "",
    ]
    for flag in flags:
        lines.append(f"   - {flag}")

    lines.append("")
    lines.append("   Verify Particular Conditions before relying on")
    lines.append("   standard-form positions.")

    if a["amendment_notes"]:
        lines.append("")
        lines.append(f"   User notes: {a['amendment_notes']}")

    return lines


def build_missing_info(a, b, c):
    """Return checklist of missing/unconfirmed information."""
    checklist = []

    if a["amendment_status"] in ("yes", "unknown"):
        checklist.append("□ Particular Conditions — review for amendments")

    if not c["notice_served"]:
        checklist.append("□ Notice of Claim — draft and serve immediately")

    # Issue-specific items
    items = MISSING_INFO_DB.get(b["issue_key"], [])
    for item in items:
        checklist.append(f"□ {item}")

    if not c.get("event_date"):
        checklist.append("□ Key event date — required for deadline calculation")

    return checklist


def build_next_steps(a, b, c, d):
    """Return ordered list of recommended next steps."""
    steps = []
    step_num = 1

    # Urgent notice action
    if not c["notice_served"] and c.get("awareness_date"):
        rule = _lookup_notice_rule(a["form_id"], a["edition"])
        if rule:
            steps.append(f"{step_num}. Serve Clause {rule['clause']} notice today — do not delay further")
            step_num += 1

    # Issue-specific steps
    issue_steps = NEXT_STEPS_DB.get(b["issue_key"], [])
    for step in issue_steps:
        steps.append(f"{step_num}. {step}")
        step_num += 1

    # Relevant CLI command
    cli_map = {
        "1": "python3 scripts/claims_template.py \\\n        --form {form} --type notice-of-claim \\\n        --output notice.md",
        "3": "python3 scripts/claims_template.py \\\n        --form {form} --type variation-claim \\\n        --output variation.md",
        "4": "python3 scripts/sop_calculator.py \\\n        --claim-date {date} \\\n        --format md --output sop_timeline.md",
    }
    cli_template = cli_map.get(b["issue_key"])
    if cli_template:
        form_arg = a["form_id"]
        if form_arg.startswith("nec4"):
            form_arg = "nec4"
        date_arg = format_date(c.get("event_date"))
        cmd = cli_template.format(form=form_arg, date=date_arg)
        steps.append("")
        steps.append("  Run:")
        steps.append(f"    {cmd}")

    return steps


def build_confidence_labels(a, b, c):
    """Return list of (label, confidence) tuples."""
    labels = CONFIDENCE_MAP.get(b["issue_key"], [
        ("Clause identification", "medium"),
        ("Entitlement position", "review"),
    ])
    # If amendments unknown/yes, downgrade amendment-related
    result = list(labels)
    if a["amendment_status"] in ("yes", "unknown"):
        # Ensure amendment impact is flagged
        has_amend = any("mendment" in l[0].lower() for l in result)
        if not has_amend:
            result.append(("Amendment impact", "review"))
    return result


def build_governing_law_cautions(governing_law):
    """Return jurisdiction-specific caution list."""
    cautions = GOVERNING_LAW_CAUTIONS.get(governing_law)
    if cautions:
        return [f"- {c}" for c in cautions]
    return [f"- [No specific cautions available for {governing_law}]",
            "- Verify local statutory requirements and limitation periods",
            "- Check whether statutory adjudication rights exist"]


def build_evidence_checklist(issue_key):
    """Return evidence checklist for claims-related issues, or None."""
    items = EVIDENCE_CHECKLISTS.get(issue_key)
    if not items:
        return None
    return [f"□ {item}" for item in items]


# ─────────────────────────────────────────────
# INTERACTIVE SECTIONS
# ─────────────────────────────────────────────

def section_a():
    header("MATTER INTAKE — Section A: Contract")

    print("[A1] Which contract form applies?\n")
    form_choices = {k: v[1] for k, v in CONTRACT_FORMS.items()}
    form_key = prompt_choice(form_choices)
    form_id, form_label = CONTRACT_FORMS[form_key]

    print()
    print("[A2] Which edition or year applies?\n")
    editions = COMMON_EDITIONS.get(form_id, [])
    if editions:
        print("    Common editions still in active use:")
        for e in editions:
            print(f"    - {e}")
        print()
    print("    ⚠️ Do not assume the latest edition applies.")
    print("       Check the contract documents.\n")
    edition = prompt_text("Enter edition (e.g. 1999, 2017, 2020)")
    if not edition:
        print("    ⚠️ Edition is required. Defaulting to 'Unknown'.")
        edition = "Unknown"

    print()
    print("[A3] What is the governing law?\n")
    law_key = prompt_choice(GOVERNING_LAWS)
    governing_law = GOVERNING_LAWS[law_key]
    if law_key == "5":
        governing_law = prompt_text("Specify governing law")

    print()
    print("[A4] What is the procurement type?\n")
    proc_key = prompt_choice(PROCUREMENT_TYPES)
    procurement = PROCUREMENT_TYPES[proc_key]

    print()
    print("[A5] Are there amendments or Particular Conditions?\n")
    amend_choices = {"1": "Yes — known amendments", "2": "No — using standard form unamended", "3": "Unknown — not yet reviewed"}
    print("    ⚠️ If yes or unknown, all conclusions will be")
    print("       flagged as provisional pending amendment review.\n")
    amend_key = prompt_choice(amend_choices)
    amendment_status = AMENDMENT_STATUS[amend_key]
    amendment_notes = ""
    if amend_key == "1":
        print()
        amendment_notes = prompt_text("Briefly note key amendments (optional)", allow_skip=True)

    return {
        "form_id": form_id,
        "form_label": form_label,
        "edition": edition,
        "governing_law": governing_law,
        "procurement": procurement,
        "amendment_status": amendment_status,
        "amendment_notes": amendment_notes,
    }


def section_b():
    header("MATTER INTAKE — Section B: Issue")

    print("[B1] What is the primary issue type?\n")
    issue_key = prompt_choice(ISSUE_TYPES)
    issue_type = ISSUE_TYPES[issue_key]

    print()
    print("[B2] Briefly describe the issue.\n")
    print("    (One or two sentences. Focus on what happened,")
    print("     not the legal argument.)\n")
    description = prompt_text("> ")

    print()
    print("[B3] Which party are you acting for?\n")
    party_key = prompt_choice(PARTIES)
    party = PARTIES[party_key]

    return {
        "issue_key": issue_key,
        "issue_type": issue_type,
        "description": description,
        "party": party,
    }


def section_c():
    header("MATTER INTAKE — Section C: Timeline")

    print("[C1] When did the key event occur?\n")
    print("    (The event that gives rise to the claim or issue.)\n")
    event_date = prompt_date("Enter date (YYYY-MM-DD)", allow_skip=True)

    print()
    print("[C2] When did you first become aware of the event?\n")
    print("    ⚠️ Notice periods typically run from awareness,")
    print("       not from the event itself. Check your clause.\n")
    awareness_date = prompt_date("Enter date (YYYY-MM-DD) or press Enter if same as above", allow_skip=True)
    if awareness_date is None and event_date is not None:
        awareness_date = event_date

    print()
    print("[C3] Has a notice been served?\n")
    notice_choices = {"1": "Yes", "2": "No", "3": "Not sure"}
    notice_key = prompt_choice(notice_choices)
    notice_served = notice_key == "1"
    notice_date = None
    notice_acknowledged = None

    if notice_key == "1":
        print()
        notice_date = prompt_date("When was the notice served? (YYYY-MM-DD)")
        print()
        print("Was the notice acknowledged or accepted?\n")
        ack_key = prompt_choice({"1": "Yes", "2": "No", "3": "Not sure"})
        notice_acknowledged = ack_key

    print()
    print("[C4] What is the current contract completion date?\n")
    completion_date = prompt_date("Enter date (YYYY-MM-DD)", allow_skip=True)

    return {
        "event_date": event_date,
        "awareness_date": awareness_date,
        "notice_served": notice_served,
        "notice_date": notice_date,
        "notice_acknowledged": notice_acknowledged,
        "completion_date": completion_date,
    }


def section_d():
    header("MATTER INTAKE — Section D: Objective")

    print("[D1] What outcome are you seeking?\n")
    obj_key = prompt_choice(OBJECTIVES)
    objective = OBJECTIVES[obj_key]

    print()
    print("[D2] How urgent is this matter?\n")
    urg_key = prompt_choice(URGENCY)
    urgency = URGENCY[urg_key]

    return {
        "objective": objective,
        "urgency": urgency,
    }


# ─────────────────────────────────────────────
# OUTPUT RENDERER
# ─────────────────────────────────────────────

def render_output(a, b, c, d, fmt="md"):
    """Assemble and render the full intake output report."""
    issue_summary = build_issue_summary(a, b, c, d)
    clause_buckets = build_clause_buckets(a, b)
    deadline_check = build_deadline_check(a, b, c)
    amendment_flags = build_amendment_flags(a)
    missing_info = build_missing_info(a, b, c)
    next_steps = build_next_steps(a, b, c, d)
    confidence = build_confidence_labels(a, b, c)
    law_cautions = build_governing_law_cautions(a["governing_law"])
    evidence = build_evidence_checklist(b["issue_key"])

    lines = []

    def ln(text=""):
        lines.append(text)

    def div():
        ln(DIVIDER)

    # Header
    div()
    ln(" MATTER INTAKE — OUTPUT REPORT")
    ln(f" Construction Law Skill v{VERSION}")
    div()
    ln()
    ln(f"Contract:   {form_label_full(a['form_id'], a['edition'])}")
    ln(f"Governing:  {a['governing_law']}")
    ln(f"Party:      {b['party']}")
    ln(f"Issue:      {b['issue_type']}")
    ln(f"Objective:  {d['objective']}")
    ln(f"Generated:  {date.today().strftime('%Y-%m-%d')}")

    # 1. Issue Summary
    ln()
    div()
    ln(" 1. ISSUE SUMMARY")
    div()
    ln()
    ln(issue_summary)

    # 2. Clause Buckets
    ln()
    div()
    ln(" 2. LIKELY CLAUSE BUCKETS")
    div()
    ln()
    for line in clause_buckets:
        ln(f"  {line}")

    # 3. Deadline Check
    ln()
    div()
    ln(" 3. DEADLINE / TIME-BAR CHECK")
    div()
    ln()
    for line in deadline_check:
        ln(f"  {line}")

    # 4. Amendment Flags
    ln()
    div()
    ln(" 4. AMENDMENT SENSITIVITY FLAGS")
    div()
    ln()
    for line in amendment_flags:
        ln(f"  {line}")

    # 5. Missing Information
    ln()
    div()
    ln(" 5. MISSING INFORMATION CHECKLIST")
    div()
    ln()
    for item in missing_info:
        ln(f"  {item}")

    # 6. Evidence Checklist (claims only)
    if evidence:
        ln()
        div()
        ln(" 📎 EVIDENCE CHECKLIST")
        div()
        ln()
        for item in evidence:
            ln(f"  {item}")

    # 7. Next Steps
    ln()
    div()
    ln(" 6. RECOMMENDED NEXT STEPS")
    div()
    ln()
    for step in next_steps:
        ln(f"  {step}")

    # 8. Confidence Labels
    ln()
    div()
    ln(" 7. CONFIDENCE LABELS")
    div()
    ln()
    for label, level in confidence:
        icon = CONFIDENCE_ICONS.get(level, level)
        ln(f"  {label:<35} {icon}")

    # 9. Governing Law Cautions
    ln()
    div()
    ln(f" ⚖️ GOVERNING LAW CAUTIONS — {a['governing_law']}")
    div()
    ln()
    for caution in law_cautions:
        ln(f"  {caution}")

    # Footer
    ln()
    div()
    ln(" ⚠️ IMPORTANT")
    div()
    ln()
    ln("This output is a workflow and analysis aid only.")
    ln("It is not legal advice. Verify all conclusions")
    ln("against the actual contract, amendments, and")
    ln("applicable law before acting.")
    div()
    ln()

    return "\n".join(lines)


# ─────────────────────────────────────────────
# FILE-BASED (NON-INTERACTIVE) INPUT
# ─────────────────────────────────────────────

def load_matter_from_file(path):
    """Load matter answers from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Section A
    a = {
        "form_id": data.get("form_id", "bespoke"),
        "form_label": FORM_DISPLAY.get(data.get("form_id", "bespoke"), "Bespoke / Other"),
        "edition": data.get("edition", "Unknown"),
        "governing_law": data.get("governing_law", "Other"),
        "procurement": data.get("procurement", "Unknown / Not applicable"),
        "amendment_status": data.get("amendment_status", "unknown"),
        "amendment_notes": data.get("amendment_notes", ""),
    }
    # Section B
    b = {
        "issue_key": data.get("issue_key", "8"),
        "issue_type": ISSUE_TYPES.get(data.get("issue_key", "8"), "Other"),
        "description": data.get("description", ""),
        "party": data.get("party", "Contractor"),
    }
    # Section C
    c = {
        "event_date": parse_date_safe(data.get("event_date")),
        "awareness_date": parse_date_safe(data.get("awareness_date")) or parse_date_safe(data.get("event_date")),
        "notice_served": data.get("notice_served", False),
        "notice_date": parse_date_safe(data.get("notice_date")),
        "notice_acknowledged": data.get("notice_acknowledged"),
        "completion_date": parse_date_safe(data.get("completion_date")),
    }
    # Section D
    d = {
        "objective": data.get("objective", "General contract review"),
        "urgency": data.get("urgency", "Planning ahead — no immediate deadline"),
    }
    return a, b, c, d


# ─────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────

def run_intake(fmt="md", output_path=None, file_path=None, save_matter=None):
    if file_path:
        a, b, c, d = load_matter_from_file(file_path)
    else:
        print()
        divider()
        print(f" CONSTRUCTION LAW SKILL — MATTER INTAKE v{VERSION}")
        divider()
        print()
        print("    This wizard will guide you through a structured")
        print("    matter intake and produce a triage report.")
        print()
        print("    Press Ctrl+C at any time to exit.")
        print()
        try:
            a = section_a()
            b = section_b()
            c = section_c()
            d = section_d()
        except KeyboardInterrupt:
            print("\n\n    Intake cancelled.")
            sys.exit(0)

    # Save matter JSON if requested
    if save_matter:
        matter_data = {
            "form_id": a["form_id"],
            "edition": a["edition"],
            "governing_law": a["governing_law"],
            "procurement": a["procurement"],
            "amendment_status": a["amendment_status"],
            "amendment_notes": a["amendment_notes"],
            "issue_key": b["issue_key"],
            "description": b["description"],
            "party": b["party"],
            "event_date": format_date(c["event_date"]) if c["event_date"] else None,
            "awareness_date": format_date(c["awareness_date"]) if c["awareness_date"] else None,
            "notice_served": c["notice_served"],
            "notice_date": format_date(c["notice_date"]) if c["notice_date"] else None,
            "notice_acknowledged": c["notice_acknowledged"],
            "completion_date": format_date(c["completion_date"]) if c["completion_date"] else None,
            "objective": d["objective"],
            "urgency": d["urgency"],
        }
        with open(save_matter, "w", encoding="utf-8") as f:
            json.dump(matter_data, f, indent=2, ensure_ascii=False)
        print(f"\n    Matter saved to: {save_matter}")

    # Generate report
    if not file_path:
        print()
        divider()
        print(" Generating report...")
        divider()
        print()

    report = render_output(a, b, c, d, fmt=fmt)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"    Report saved to: {output_path}")
    else:
        print(report)


def main():
    parser = argparse.ArgumentParser(
        description="Matter Intake Mode — Construction Law Skill v2.8.1"
    )
    parser.add_argument("--format", "-f", choices=["md", "txt"], default="md",
                        help="Output format (default: md)")
    parser.add_argument("--output", "-o", metavar="FILE",
                        help="Save report to file")
    parser.add_argument("--file", metavar="JSON",
                        help="Non-interactive: load answers from JSON file")
    parser.add_argument("--save-matter", metavar="FILE",
                        help="Save matter answers as JSON for reuse")
    args = parser.parse_args()
    run_intake(fmt=args.format, output_path=args.output,
               file_path=args.file, save_matter=args.save_matter)


if __name__ == "__main__":
    main()
