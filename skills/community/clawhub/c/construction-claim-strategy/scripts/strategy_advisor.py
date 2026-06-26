#!/usr/bin/env python3
"""
strategy_advisor.py — Strategic Planning Framework
Construction Claim Strategy Skill v1.7.6

Sits BEFORE clause selection. Helps plan the direction, scope, and
architecture of a claim response before deciding which clauses to cite.

The 7-Dimension methodology is contract-form neutral. It works with
PSSCOC, FIDIC, NEC, SIA, JCT, and bespoke contracts. The bundled
examples use PSSCOC 2014 (7th Edition) clause references.

Usage:
    python3 scripts/strategy_advisor.py
    python3 scripts/strategy_advisor.py --file input.json --output strategy.md

Non-interactive mode (primary use case):
    Provide a JSON file with situation details; generates a strategy report.

Interactive mode:
    Guided wizard that walks through all 7 strategy dimensions.

Output formats:
    --format md (default)
    --format txt
    --output <filename>
    --file <input.json>         Non-interactive: read from JSON
    --save-strategy <path>      Dump answered strategy as JSON
"""

import argparse
import json
import sys
import os
from datetime import datetime

# ─────────────────────────────────────────────
# VERSION
# ─────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from version import VERSION

DIVIDER = "━" * 52
THIN_DIVIDER = "─" * 52


# ═══════════════════════════════════════════════
# 1. STRATEGY REFERENCE DATA
# ═══════════════════════════════════════════════

# ── 1A. Argument types ranked by strength ──
# For construction contracts (all forms)

ARGUMENT_TYPES = [
    {
        "rank": 1,
        "name": "Textual Interpretation",
        "strength": "Strongest",
        "description": (
            "Argue from the actual clause wording. Identify what the clause "
            "presupposes, what it expressly covers, and where the factual "
            "situation falls outside its scope or premise."
        ),
        "example": (
            "Clause 12.5 permits the Employer to engage other contractors "
            "on Site, but the clause does not transfer to the Contractor "
            "the risk of delay caused by acts or omissions of such other "
            "contractors. The EOT entitlement arises under Clause 14.2(m)."
        ),
        "when_to_use": (
            "Always start here. If you can win on the text, you don't need "
            "anything else. Courts and contract administrators prefer textual arguments."
        ),
    },
    {
        "rank": 2,
        "name": "Factual Distinction",
        "strength": "Strong",
        "description": (
            "Show that the factual situation exceeds the clause's scope or "
            "premise. The clause applies generally, but THIS situation is "
            "materially different from what was contemplated."
        ),
        "example": (
            "Clause 12.5 contemplates the Contractor affording 'all "
            "reasonable facilities' to other contractors in the ordinary "
            "course. Where the other contractor's delay was caused by the "
            "Employer's own coordination failure, the situation exceeds "
            "what Clause 12.5 contemplates."
        ),
        "when_to_use": (
            "When the text is broad but the facts are extraordinary. "
            "Pairs well with textual interpretation as a 1–2 punch."
        ),
    },
    {
        "rank": 3,
        "name": "Concede-then-Distinguish",
        "strength": "Moderate-Strong",
        "description": (
            "Acknowledge that the clause applies in ordinary circumstances, "
            "then distinguish THIS case as extraordinary. Disarms the other "
            "side and shows good faith."
        ),
        "example": (
            "The Contractor acknowledges that Clause 12.5 applies in "
            "ordinary circumstances and accepts its coordination obligations. "
            "However, the present delay did not arise from ordinary interface "
            "risk — it arose from the SO's direction which materially "
            "affected the Contractor's planned access and sequence of works."
        ),
        "when_to_use": (
            "For risk-allocation rebuttals. Never lead with 'the clause "
            "doesn't apply' — it antagonises the certifier. Concede the "
            "ordinary application first, then distinguish."
        ),
    },
    {
        "rank": 4,
        "name": "Implied Terms / Prevention Principle",
        "strength": "Weakest",
        "description": (
            "Argue that the contract contains implied terms or that the "
            "prevention principle bars the other party. In many jurisdictions, "
            "courts are reluctant to imply terms when express provisions "
            "exist. Standard form contracts with detailed risk allocation "
            "clauses — implied terms will usually get shut down."
        ),
        "example": (
            "There is an implied obligation not to prevent the Contractor "
            "from performing. (Weak — only use if express clauses fail.)"
        ),
        "when_to_use": (
            "Last resort only. If you're reaching for implied terms when "
            "express clauses exist, your primary arguments are probably weak. "
            "Consider whether the claim is viable at all."
        ),
    },
]


# ── 1B. Disclosure control levels ──

DISCLOSURE_LEVELS = {
    "state_precisely": {
        "label": "State Precisely",
        "description": "Documented facts with letter references, clause numbers, legal reasoning.",
        "examples": [
            "Other contractor commenced late on [date] (ref. Contractor's letter ref. [XXX])",
            "EOT clause for acts/omissions of other contractors — Clause 14.2(m)",
            "Contractor's notice ref. [XXX] dated [date] issued under Clause 14.3",
        ],
    },
    "keep_general": {
        "label": "Keep General",
        "description": (
            "Operational details (zones, quantities), dates without written "
            "record, internal arrangements. Use general language to preserve "
            "flexibility."
        ),
        "examples": [
            "'multiple work areas within and outside the Site' (not Zone A, Zone B)",
            "'resequencing of works' (not specific programme activities)",
            "'approximately [date]' for verbal/informal communications",
        ],
    },
    "defer": {
        "label": "Defer to Claim Report",
        "description": (
            "Full quantification, detailed delay analysis, cost breakdown, "
            "programme impact. Reserve for the Notified Claim Report or "
            "subsequent submissions."
        ),
        "examples": [
            "Detailed delay analysis with critical path impact",
            "Cost breakdown with quantities, rates, invoices",
            "Zone-by-zone production records",
            "Programme comparison (baseline vs actual vs impacted)",
        ],
    },
}


# ── 1C. Response architecture patterns ──

RESPONSE_PATTERNS = {
    "standard_rebuttal": {
        "name": "Standard Certifier Query Response",
        "steps": [
            "Acknowledge the certifier's position / question",
            "Pivot to Contractor's primary contractual reliance",
            "State primary argument (textual interpretation)",
            "Reserve fallback clause(s) without elaborating",
            "Close cooperatively",
        ],
        "when": (
            "Default pattern for responding to certifier queries. Works for "
            "most items in a request-for-information letter."
        ),
    },
    "risk_allocation_rebuttal": {
        "name": "Risk Allocation Rebuttal (Concede-then-Distinguish)",
        "steps": [
            "Concede the ordinary application of the risk clause",
            "Distinguish the extraordinary facts of THIS case",
            "Provide factual support (before/after, what changed)",
            "State legal conclusion (clause covers X, this is Y)",
            "Show mitigation evidence (demonstrates good faith)",
            "Close cooperatively — accept ordinary risk, maintain this is extraordinary",
        ],
        "when": (
            "When the certifier points to a specific risk-allocation clause "
            "(e.g., a clause allocating interface risk to the Contractor) "
            "and says the risk is yours. Never "
            "lead with 'the clause doesn't apply'."
        ),
    },
    "chronology_response": {
        "name": "Chronology / Details Response",
        "steps": [
            "State what is known with exact dates and references",
            "Flag items still being compiled (don't hedge documented facts)",
            "Commit to supplementing in the Notified Claim Report",
            "Reserve right to provide further details",
        ],
        "when": (
            "When asked for chronology, details, or documentary evidence. "
            "Provide what you have, hedge only what's genuinely uncertain, "
            "defer the rest."
        ),
    },
    "cost_claim_response": {
        "name": "Cost Claim Response (Pre-Quantification)",
        "steps": [
            "Identify the contractual basis for cost recovery (e.g., Cl. 63.1)",
            "List heads of claim without quantifying",
            "State that the disruption is ongoing / costs are being assessed",
            "Commit to detailed breakdown in the Notified Claim Report",
            "Reserve right to supplement",
        ],
        "when": (
            "When asked for cost breakdowns before you're ready to quantify. "
            "Name the heads of claim to show awareness, but don't lock in "
            "numbers prematurely."
        ),
    },
    "reservation_close": {
        "name": "Reservation of Rights Closing",
        "steps": [
            "State that submission is on an interim / without prejudice basis",
            "Reserve all rights, remedies, claims, and entitlements",
            "Under the Contract, at law, or otherwise",
            "Commit to cooperation",
        ],
        "when": "Always. Every substantive response should end with a reservation.",
    },
}


# ── 1D. Scope control patterns ──

SCOPE_PATTERNS = {
    "limit_to_letter": {
        "name": "Limit Response to Matters Raised",
        "description": (
            "Respond only to the specific items raised in the letter being "
            "replied to. Do not volunteer information about topics not yet "
            "addressed by the other side."
        ),
        "anti_pattern": (
            "Volunteering information about topics the certifier hasn't "
            "asked about yet. E.g., including a mitigation proposal "
            "narrative when the Employer's letter only replies to the initial "
            "notice, not the mitigation request."
        ),
        "check": "Which letter(s) are we replying to? What did they specifically ask?",
    },
    "preserve_future_claims": {
        "name": "Preserve Future Claims",
        "description": (
            "Don't close doors. Use 'reserves its position' and 'without "
            "prejudice' to keep options open for claims not yet fully "
            "developed."
        ),
        "anti_pattern": (
            "Making definitive statements that could be used against you "
            "later. E.g., 'the only delay was X' when there may be other "
            "delay events not yet notified."
        ),
        "check": "Are we making any absolute statements that could limit future claims?",
    },
    "dont_name_specifics_early": {
        "name": "Keep Operational Details General",
        "description": (
            "Don't name specific zones, quantities, or internal arrangements "
            "in initial replies. Once named in writing, you're locked in."
        ),
        "anti_pattern": (
            "Naming 'Zone A' and 'Zone B' in the initial reply. If "
            "boundaries shift during assessment, you have a consistency "
            "problem. The Employer will immediately follow up with zone-by-zone "
            "breakdowns."
        ),
        "check": "Are we naming anything specific that we might need to adjust later?",
    },
}


# ── 1E. Risk assessment checklist ──

RISK_CHECKLIST = [
    {
        "category": "Counter-Arguments",
        "questions": [
            "What will the other party argue in response?",
            "Which clauses might they cite to rebut our position?",
            "Are there any contractual provisions that explicitly allocate this risk to us?",
            "Can they argue we failed to mitigate?",
        ],
    },
    {
        "category": "Weak Points",
        "questions": [
            "Is our notice timing vulnerable? (Late notice = potential time-bar.)",
            "Are there gaps in our contemporaneous records?",
            "Did we create any inconsistencies in prior correspondence?",
            "Are we relying on verbal communications without written confirmation?",
        ],
    },
    {
        "category": "Timing Risks",
        "questions": [
            "What is the response deadline?",
            "Is the disruption still ongoing? (Affects quantification.)",
            "Are there parallel claims or notices that interact with this one?",
            "Could delay in responding weaken our position or trigger time-bar arguments?",
        ],
    },
    {
        "category": "Disclosure Risks",
        "questions": [
            "Are we volunteering anything the other side hasn't asked about?",
            "Could any statement be used against us in a future dispute?",
            "Are we prematurely quantifying before records are complete?",
            "Are we naming specifics (zones, dates, quantities) we might need to change?",
        ],
    },
]


# ── 1F. Situation triggers ──

SITUATION_TYPES = {
    "1": "Responding to the certifier's request for further information",
    "2": "Initiating a new claim / notice",
    "3": "Responding to a rejection of our claim",
    "4": "Responding to a counter-claim / back-charge",
    "5": "Preparing for adjudication / arbitration",
    "6": "Pre-emptive strategy (anticipating a dispute)",
    "7": "Other",
}


# ═══════════════════════════════════════════════
# 2. INTERACTIVE MODE
# ═══════════════════════════════════════════════

def _prompt_choice(options, allow_skip=False):
    """Prompt user to select from numbered options dict."""
    for key, label in options.items():
        print(f"  {key:>2}. {label}")
    print()
    while True:
        raw = input("Enter number: ").strip()
        if allow_skip and raw == "":
            return ""
        if raw in options:
            return raw
        print(f"  ⚠️ Invalid. Enter one of: {', '.join(options.keys())}")


def _prompt_text(label, allow_skip=False):
    """Prompt for free text."""
    hint = " (or press Enter to skip)" if allow_skip else ""
    return input(f"{label}{hint}: ").strip()



def interactive_strategy():
    """Walk through all 7 strategy dimensions interactively."""
    print()
    print(DIVIDER)
    print(" STRATEGY ADVISOR — Interactive Mode")
    print(DIVIDER)
    print()
    print("This wizard helps you plan your strategic approach BEFORE")
    print("selecting clauses or drafting a response.")
    print()

    strategy = {}

    # ── Dimension 1: Situation Assessment ──
    print(THIN_DIVIDER)
    print(" 1. SITUATION ASSESSMENT")
    print(THIN_DIVIDER)
    print()
    print("What are we dealing with?")
    print()
    sit_key = _prompt_choice(SITUATION_TYPES)
    strategy["situation_type"] = SITUATION_TYPES[sit_key]
    print()

    strategy["other_side_position"] = _prompt_text(
        "What is the other side's position / what did they say?"
    )
    strategy["trigger_event"] = _prompt_text(
        "What triggered this? (e.g., letter ref, event, instruction)"
    )
    strategy["responding_to_letters"] = _prompt_text(
        "Which letter(s) are we replying to? (refs and dates)"
    )

    # ── Dimension 2: Scope Control ──
    print()
    print(THIN_DIVIDER)
    print(" 2. SCOPE CONTROL")
    print(THIN_DIVIDER)
    print()
    strategy["in_scope"] = _prompt_text(
        "What is IN scope for this response?"
    )
    strategy["out_of_scope"] = _prompt_text(
        "What should we NOT volunteer? (topics not yet raised)", allow_skip=True
    )
    strategy["future_claims_to_preserve"] = _prompt_text(
        "Any future claims / positions to preserve?", allow_skip=True
    )

    # ── Dimension 3: Direction Decision ──
    print()
    print(THIN_DIVIDER)
    print(" 3. DIRECTION DECISION")
    print(THIN_DIVIDER)
    print()
    strategy["primary_argument"] = _prompt_text(
        "Primary argument / clause (your strongest position)"
    )
    strategy["fallback_argument"] = _prompt_text(
        "Fallback argument / clause (reserve position)", allow_skip=True
    )
    strategy["clauses_to_avoid"] = _prompt_text(
        "Any clauses to AVOID citing? (and why)", allow_skip=True
    )

    # ── Dimension 4: Argument Strategy ──
    print()
    print(THIN_DIVIDER)
    print(" 4. ARGUMENT STRATEGY")
    print(THIN_DIVIDER)
    print()
    print("Argument types ranked by strength:")
    print()
    for at in ARGUMENT_TYPES:
        print(f"  {at['rank']}. {at['name']} ({at['strength']})")
    print()
    strategy["chosen_argument_type"] = _prompt_text(
        "Which argument type will you lead with? (number or name)"
    )
    strategy["argument_notes"] = _prompt_text(
        "Notes on argument approach", allow_skip=True
    )

    # ── Dimension 5: Disclosure Control ──
    print()
    print(THIN_DIVIDER)
    print(" 5. DISCLOSURE CONTROL")
    print(THIN_DIVIDER)
    print()
    print("What level of detail at this stage?")
    for key, level in DISCLOSURE_LEVELS.items():
        print(f"\n  [{key}] {level['label']}")
        print(f"    {level['description']}")
    print()
    strategy["state_precisely"] = _prompt_text(
        "What should be stated precisely? (documented facts, clause refs)",
        allow_skip=True
    )
    strategy["keep_general"] = _prompt_text(
        "What should be kept general? (operational details, zones, quantities)",
        allow_skip=True
    )
    strategy["defer_items"] = _prompt_text(
        "What should be deferred to the Claim Report?",
        allow_skip=True
    )

    # ── Dimension 6: Response Architecture ──
    print()
    print(THIN_DIVIDER)
    print(" 6. RESPONSE ARCHITECTURE")
    print(THIN_DIVIDER)
    print()
    print("Available response patterns:")
    for key, pattern in RESPONSE_PATTERNS.items():
        print(f"\n  [{key}]  {pattern['name']}")
        print(f"    When: {pattern['when']}")
    print()
    strategy["chosen_pattern"] = _prompt_text(
        "Which pattern(s) will you use? (name or key)", allow_skip=True
    )
    strategy["architecture_notes"] = _prompt_text(
        "Notes on response structure", allow_skip=True
    )

    # ── Dimension 7: Risk Assessment ──
    print()
    print(THIN_DIVIDER)
    print(" 7. RISK ASSESSMENT")
    print(THIN_DIVIDER)
    print()
    strategy["counter_arguments"] = _prompt_text(
        "Expected counter-arguments from the other side", allow_skip=True
    )
    strategy["weak_points"] = _prompt_text(
        "Known weak points in our position", allow_skip=True
    )
    strategy["timing_risks"] = _prompt_text(
        "Timing risks (deadlines, ongoing events)", allow_skip=True
    )
    strategy["response_deadline"] = _prompt_text(
        "Response deadline (specific calendar date, e.g. 2026-04-22 \u2014 "
        "calculate using the construction-law SOP calculator if applicable)",
        allow_skip=True
    )

    return strategy


# ═══════════════════════════════════════════════
# 3. REPORT GENERATOR
# ═══════════════════════════════════════════════

def generate_report(strategy, fmt="md"):
    """Generate a strategy report from a strategy dict."""
    lines = []

    def heading(level, text):
        if fmt == "md":
            lines.append(f"{'#' * level} {text}")
        else:
            lines.append(text)
            lines.append("=" * len(text) if level <= 2 else "-" * len(text))

    def bullet(text, indent=0):
        prefix = "  " * indent
        if fmt == "md":
            lines.append(f"{prefix}- {text}")
        else:
            lines.append(f"{prefix}• {text}")

    def para(text):
        lines.append(text)

    def blank():
        lines.append("")

    def field(label, value, indent=0):
        if value:
            bullet(f"**{label}:** {value}" if fmt == "md" else f"{label}: {value}", indent)

    # ── Title ──
    lines.append(DIVIDER)
    lines.append(" STRATEGY REPORT")
    lines.append(DIVIDER)
    blank()
    para(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    para(f"Strategy Advisor v{VERSION}")
    blank()

    # ── 1. Situation Assessment ──
    heading(2, "1. Situation Assessment")
    blank()
    field("Type", strategy.get("situation_type", ""))
    field("Other side's position", strategy.get("other_side_position", ""))
    field("Trigger", strategy.get("trigger_event", ""))
    field("Responding to", strategy.get("responding_to_letters", ""))
    blank()

    # ── 2. Scope Control ──
    heading(2, "2. Scope Control")
    blank()
    field("In scope", strategy.get("in_scope", ""))
    field("Out of scope / Do NOT volunteer", strategy.get("out_of_scope", ""))
    field("Future claims to preserve", strategy.get("future_claims_to_preserve", ""))
    blank()

    # Reference: scope control patterns
    if fmt == "md":
        para("**Scope Control Checklist:**")
    else:
        para("Scope Control Checklist:")
    for key, pattern in SCOPE_PATTERNS.items():
        bullet(f"{pattern['name']}: {pattern['check']}")
    blank()

    # ── 3. Direction Decision ──
    heading(2, "3. Direction Decision")
    blank()
    field("Primary argument / clause", strategy.get("primary_argument", ""))
    field("Fallback argument / clause", strategy.get("fallback_argument", ""))
    field("Clauses to AVOID", strategy.get("clauses_to_avoid", ""))
    blank()

    # ── 4. Argument Strategy ──
    heading(2, "4. Argument Strategy")
    blank()
    field("Chosen argument type", strategy.get("chosen_argument_type", ""))
    field("Notes", strategy.get("argument_notes", ""))
    blank()

    if fmt == "md":
        para("**Argument Types (ranked by strength):**")
    else:
        para("Argument Types (ranked by strength):")
    blank()
    for at in ARGUMENT_TYPES:
        bullet(f"Rank {at['rank']}: {at['name']} ({at['strength']})")
        bullet(f"When: {at['when_to_use']}", indent=1)
    blank()

    # ── 5. Disclosure Control ──
    heading(2, "5. Disclosure Control")
    blank()
    field("State precisely", strategy.get("state_precisely", ""))
    field("Keep general", strategy.get("keep_general", ""))
    field("Defer to Claim Report", strategy.get("defer_items", ""))
    blank()

    if fmt == "md":
        para("**Disclosure Level Reference:**")
    else:
        para("Disclosure Level Reference:")
    for key, level in DISCLOSURE_LEVELS.items():
        bullet(f"{level['label']}: {level['description']}")
        for ex in level["examples"]:
            bullet(ex, indent=1)
    blank()

    # ── 6. Response Architecture ──
    heading(2, "6. Response Architecture")
    blank()
    field("Chosen pattern(s)", strategy.get("chosen_pattern", ""))
    field("Notes", strategy.get("architecture_notes", ""))
    blank()

    if fmt == "md":
        para("**Available Response Patterns:**")
    else:
        para("Available Response Patterns:")
    blank()
    for key, pattern in RESPONSE_PATTERNS.items():
        if fmt == "md":
            bullet(f"**{pattern['name']}**")
        else:
            bullet(pattern["name"])
        for i, step in enumerate(pattern["steps"], 1):
            bullet(f"Step {i}: {step}", indent=1)
        bullet(f"When: {pattern['when']}", indent=1)
        blank()

    # ── 7. Risk Assessment ──
    heading(2, "7. Risk Assessment")
    blank()
    field("Expected counter-arguments", strategy.get("counter_arguments", ""))
    field("Known weak points", strategy.get("weak_points", ""))
    field("Timing risks", strategy.get("timing_risks", ""))
    field("Response deadline", strategy.get("response_deadline", ""))
    blank()

    if fmt == "md":
        para("**Risk Checklist:**")
    else:
        para("Risk Checklist:")
    for section in RISK_CHECKLIST:
        bullet(section["category"])
        for q in section["questions"]:
            bullet(q, indent=1)
    blank()

    # ── Footer ──
    lines.append(THIN_DIVIDER)
    para(f"Generated by Strategy Advisor v{VERSION}")
    para("This is a strategic planning aid only. It is not legal advice.")
    lines.append(THIN_DIVIDER)

    return "\n".join(lines)


# ═══════════════════════════════════════════════
# 4. CLI
# ═══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        prog="strategy_advisor",
        description=(
            "Strategy Advisor — Strategic planning framework for construction "
            "claim responses. Plan your direction, scope, and argument strategy "
            "BEFORE selecting clauses."
        ),
    )
    parser.add_argument(
        "--file",
        metavar="INPUT_JSON",
        help="Non-interactive: read strategy inputs from a JSON file.",
    )
    parser.add_argument(
        "--output", "-o",
        metavar="FILE",
        help="Write report to file instead of stdout.",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["md", "txt"],
        default="md",
        help="Output format (default: md).",
    )
    parser.add_argument(
        "--save-strategy",
        metavar="PATH",
        help="Save the strategy data as JSON for reuse.",
    )
    parser.add_argument(
        "--reference",
        action="store_true",
        help="Print all reference tables (argument types, patterns, etc.) and exit.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"Strategy Advisor v{VERSION}",
    )

    def _safe_write(path, content, label="file"):
        """Write *content* to *path*, exiting cleanly on permission/OS errors."""
        try:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
        except (PermissionError, OSError) as e:
            print(f"❌ Cannot write {label}: {e}", file=sys.stderr)
            sys.exit(1)

    args = parser.parse_args()

    # ── Reference mode: dump all tables ──
    if args.reference:
        _print_reference(args.format)
        return

    # ── Non-interactive mode ──
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                strategy = json.load(fh)
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        except PermissionError:
            print(f"❌ Permission denied: {args.file}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in {args.file}: {e}", file=sys.stderr)
            sys.exit(1)

        if not isinstance(strategy, dict):
            print(
                f"❌ Expected a JSON object (dict) in {args.file}, "
                f"got {type(strategy).__name__}.",
                file=sys.stderr,
            )
            sys.exit(1)

        # Warn on unrecognised keys
        _KNOWN_KEYS = {
            "situation_type", "other_side_position", "trigger_event",
            "responding_to_letters", "in_scope", "out_of_scope",
            "future_claims_to_preserve", "primary_argument",
            "fallback_argument", "clauses_to_avoid",
            "chosen_argument_type", "argument_notes",
            "state_precisely", "keep_general", "defer_items",
            "chosen_pattern", "architecture_notes",
            "counter_arguments", "weak_points", "timing_risks",
            "response_deadline",
        }
        _REQUIRED_KEYS = {
            "situation_type", "other_side_position", "trigger_event",
            "primary_argument", "chosen_argument_type",
            "chosen_pattern",
        }
        missing = _REQUIRED_KEYS - set(strategy.keys())
        if missing:
            print(
                f"❌ Missing required key(s) in {args.file}: "
                f"{', '.join(sorted(missing))}\n"
                f"   Required fields: {', '.join(sorted(_REQUIRED_KEYS))}",
                file=sys.stderr,
            )
            sys.exit(1)
        unknown = set(strategy.keys()) - _KNOWN_KEYS
        if unknown:
            print(
                f"⚠️  Unrecognised key(s) in input (ignored): "
                f"{', '.join(sorted(unknown))}",
                file=sys.stderr,
            )

        report = generate_report(strategy, fmt=args.format)
        if args.output:
            _safe_write(args.output, report, label=f"output file '{args.output}'")
            print(f"✅ Strategy report written to {args.output}")
        else:
            print(report)
        if args.save_strategy:
            _safe_write(
                args.save_strategy,
                json.dumps(strategy, indent=2, ensure_ascii=False),
                label=f"strategy file '{args.save_strategy}'",
            )
            print(f"✅ Strategy data saved to {args.save_strategy}")
        return

    # ── Interactive mode ──
    try:
        strategy = interactive_strategy()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ Strategy session cancelled.")
        sys.exit(1)

    report = generate_report(strategy, fmt=args.format)

    if args.output:
        _safe_write(args.output, report, label=f"output file '{args.output}'")
        print(f"\n✅ Strategy report written to {args.output}")
    else:
        print()
        print(report)

    if args.save_strategy:
        _safe_write(
            args.save_strategy,
            json.dumps(strategy, indent=2, ensure_ascii=False),
            label=f"strategy file '{args.save_strategy}'",
        )
        print(f"✅ Strategy data saved to {args.save_strategy}")


def _print_reference(fmt="md"):
    """Print all reference tables for Claude / agent use."""
    lines = []

    def heading(level, text):
        if fmt == "md":
            lines.append(f"{'#' * level} {text}")
        else:
            lines.append(text)
            lines.append("=" * len(text) if level <= 2 else "-" * len(text))

    def bullet(text, indent=0):
        prefix = "  " * indent
        lines.append(f"{prefix}- {text}" if fmt == "md" else f"{prefix}• {text}")

    def blank():
        lines.append("")

    heading(1, "Strategy Advisor — Reference Tables")
    blank()
    lines.append(f"Version: {VERSION}")
    blank()

    # Argument types
    heading(2, "Argument Types (Ranked by Strength)")
    blank()
    for at in ARGUMENT_TYPES:
        heading(3, f"Rank {at['rank']}: {at['name']} ({at['strength']})")
        blank()
        lines.append(at["description"])
        blank()
        bullet(f"Example: {at['example']}")
        bullet(f"When to use: {at['when_to_use']}")
        blank()

    # Disclosure levels
    heading(2, "Disclosure Control Levels")
    blank()
    for key, level in DISCLOSURE_LEVELS.items():
        heading(3, level["label"])
        blank()
        lines.append(level["description"])
        blank()
        for ex in level["examples"]:
            bullet(ex)
        blank()

    # Response patterns
    heading(2, "Response Architecture Patterns")
    blank()
    for key, pattern in RESPONSE_PATTERNS.items():
        heading(3, pattern["name"])
        blank()
        for i, step in enumerate(pattern["steps"], 1):
            bullet(f"Step {i}: {step}")
        blank()
        lines.append(f"When: {pattern['when']}")
        blank()

    # Scope control
    heading(2, "Scope Control Patterns")
    blank()
    for key, pattern in SCOPE_PATTERNS.items():
        heading(3, pattern["name"])
        blank()
        lines.append(pattern["description"])
        blank()
        bullet(f"Anti-pattern: {pattern['anti_pattern']}")
        bullet(f"Check: {pattern['check']}")
        blank()

    # Risk checklist
    heading(2, "Risk Assessment Checklist")
    blank()
    for section in RISK_CHECKLIST:
        heading(3, section["category"])
        blank()
        for q in section["questions"]:
            bullet(q)
        blank()

    # Situation types
    heading(2, "Situation Types")
    blank()
    for key, label in SITUATION_TYPES.items():
        bullet(f"{key}. {label}")
    blank()

    print("\n".join(lines))


if __name__ == "__main__":
    main()
