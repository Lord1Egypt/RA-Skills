#!/usr/bin/env python3
"""
Enterprise Change Management Lead — Diagnostic CLI.
No dependencies beyond stdlib.

Usage:
  python3 cm_assess.py <command> [args]

Commands:
  readiness <initiative> [--impacted-groups "A,B,C"] [--timeline "Q2 2026"]
  sponsor <initiative> [--sponsor "Title"] [--phase Prepare|Manage|Sustain]
  adoption <initiative> [--weeks-since-launch N]
  impact <initiative> [--stakeholders "A,B,C"] [--risk high|med|low]
  resistance <initiative> [--friction-points "A,B,C"]
"""

import json
import sys
import os
from datetime import datetime

# --- Framework Constants ---

ADOPTION_STAGES = [
    ("Awareness", "Understanding why the change is necessary"),
    ("Commitment", "Willingness to support and participate"),
    ("Knowledge", "Understanding what to do and how"),
    ("Ability", "Demonstrated capability in live conditions"),
    ("Reinforcement", "Mechanisms sustaining the change over time")
]

SUCCESS_TRIANGLE = [
    ("Leadership & Sponsorship", "Active, visible, consistent executive support"),
    ("Delivery Execution", "Technical delivery aligned with business readiness"),
    ("Change Readiness & Adoption", "People prepared to operate in the future state")
]

PHASES = [
    ("Prepare", "Define success, assess risk, align leadership"),
    ("Manage", "Execute through sponsorship, comms, training, readiness"),
    ("Sustain", "Measure adoption, reinforce, transfer to BAU")
]

RESISTANCE_SOURCES = [
    "unclear value",
    "loss of autonomy",
    "increased workload",
    "confusion about roles or controls",
    "distrust in leadership intent",
    "previous change fatigue",
    "weak manager support",
    "insufficient training or practice",
    "fear of compliance or audit exposure"
]

IMPACT_DIMENSIONS = [
    "processes",
    "systems and tools",
    "controls and approvals",
    "decision rights",
    "workload",
    "service model",
    "team interactions",
    "required knowledge",
    "performance expectations",
    "mindset and behaviours"
]

ESCALATION_TRIGGERS = [
    "sponsor engagement is weak or inconsistent",
    "impacted groups do not understand the reason for change",
    "manager readiness is low",
    "training exists but live task performance is weak",
    "legacy workarounds remain attractive or easier",
    "launch timing exceeds the organization's absorption capacity",
    "critical controls are implemented technically but not behaviourally"
]

MEASURE_CATEGORIES = {
    "Adoption": [
        "percentage of impacted users using the new process, tool, or control",
        "usage consistency by role, function, or business unit",
        "completion of key behaviour changes"
    ],
    "Proficiency": [
        "demonstrated ability to perform critical tasks correctly",
        "error rates, exceptions, or rework",
        "evidence of reduced dependence on legacy workarounds",
        "manager validation of role readiness"
    ],
    "Readiness": [
        "sponsor visibility and effectiveness",
        "manager preparedness",
        "communication reach and understanding",
        "learning completion and confidence indicators",
        "operational support readiness"
    ],
    "Sustainment": [
        "continued use after launch",
        "reduced workarounds over time",
        "reinforcement actions completed",
        "ownership embedded into ongoing governance and operations"
    ]
}

# --- Commands ---

def cmd_readiness(initiative, options):
    """Full readiness diagnostic with success triangle."""
    groups = [g.strip() for g in options.get("impacted-groups", "Key Stakeholders").split(",")]
    timeline = options.get("timeline", "TBD")
    
    print(f"\n{'━' * 60}")
    print(f"  ENTERPRISE CHANGE READINESS ASSESSMENT")
    print(f"  {initiative}")
    print(f"{'━' * 60}")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"  Timeline: {timeline}")
    print(f"  Impacted Groups: {', '.join(groups)}")
    print()
    
    # Change Success Triangle
    print(f"{'━' * 60}")
    print(f"  CHANGE SUCCESS TRIANGLE")
    print(f"{'━' * 60}")
    for name, desc in SUCCESS_TRIANGLE:
        print(f"  ▸ {name}")
        print(f"    {desc}")
        print(f"    Status: [  ] Strong  [  ] Adequate  [  ] At Risk  [  ] Critical")
        print()
    
    # Five-Part Adoption Model
    print(f"{'━' * 60}")
    print(f"  FIVE-PART ADOPTION MODEL — STAKEHOLDER DIAGNOSIS")
    print(f"{'━' * 60}")
    for group in groups:
        print(f"\n  Group: {group}")
        print(f"  {'─' * 50}")
        for i, (stage, desc) in enumerate(ADOPTION_STAGES, 1):
            print(f"  {i}. {stage}: {desc}")
            print(f"     Status: [  ] Complete  [  ] In Progress  [  ] At Risk  [  ] Not Started")
        print()
    
    # Escalation Triggers
    print(f"{'━' * 60}")
    print(f"  ESCALATION TRIGGERS — CHECK FOR")
    print(f"{'━' * 60}")
    for trigger in ESCALATION_TRIGGERS:
        print(f"  [  ] {trigger}")
    print()
    
    # Recommended Next Actions
    print(f"{'━' * 60}")
    print(f"  RECOMMENDED NEXT ACTIONS")
    print(f"{'━' * 60}")
    print(f"  1. Confirm sponsor engagement and visibility level")
    print(f"  2. Validate adoption model stage for each impacted group")
    print(f"  3. Identify top 3 adoption risks with evidence")
    print(f"  4. Align change activities with delivery milestones")
    print(f"  5. Define minimum viable readiness criteria for go-live")
    print()

def cmd_sponsor(initiative, options):
    """Generate sponsor action plan."""
    sponsor = options.get("sponsor", "Executive Sponsor")
    phase = options.get("phase", "Manage")
    
    print(f"\n{'━' * 60}")
    print(f"  SPONSOR ACTION PLAN")
    print(f"  {initiative}")
    print(f"{'━' * 60}")
    print(f"  Sponsor: {sponsor}")
    print(f"  Phase: {phase}")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d')}")
    print()
    
    print(f"  SPONSOR EXPECTATIONS")
    print(f"  {'─' * 50}")
    expectations = [
        "Explain why the change matters — connect to strategy, risk, and business priorities",
        "Remove barriers and resolve escalations promptly",
        "Align senior leaders and maintain visible, consistent support",
        "Reinforce the future state after implementation"
    ]
    for i, exp in enumerate(expectations, 1):
        print(f"  {i}. {exp}")
    print()
    
    print(f"  SPONSOR ACTIONS BY PHASE")
    print(f"  {'─' * 50}")
    
    if phase == "Prepare":
        actions = [
            "Confirm business case and strategic alignment",
            "Identify and engage other senior leaders",
            "Define success criteria and risk tolerance",
            "Approve change investment and resource allocation",
            "Communicate personal commitment to the initiative"
        ]
    elif phase == "Sustain":
        actions = [
            "Review adoption and proficiency metrics",
            "Reinforce new behaviours in leadership communications",
            "Recognize teams demonstrating strong adoption",
            "Address areas where reversion is occurring",
            "Confirm BAU ownership transfer is complete"
        ]
    else:  # Manage
        actions = [
            "Deliver key messages at town halls and leadership meetings",
            "Conduct skip-level conversations with impacted teams",
            "Remove escalated barriers within 48 hours",
            "Hold peers accountable for visible sponsorship",
            "Review adoption dashboard weekly and intervene on risks"
        ]
    
    for i, action in enumerate(actions, 1):
        print(f"  {i}. {action}")
        print(f"     Target Date: ____________")
        print(f"     Status: [  ] Not Started  [  ] In Progress  [  ] Complete")
        print()
    
    # Health Check
    print(f"  SPONSOR HEALTH CHECK")
    print(f"  {'─' * 50}")
    checks = [
        "Sponsor can articulate why the change matters in one sentence",
        "Sponsor has been visibly active in the last 30 days",
        "Sponsor has removed at least one barrier",
        "Other senior leaders are aligned and consistent",
        "Sponsor engagement is increasing, not decreasing as launch approaches"
    ]
    for check in checks:
        print(f"  [  ] {check}")
    print()

def cmd_adoption(initiative, options):
    """Post-launch adoption assessment."""
    weeks = int(options.get("weeks-since-launch", 0))
    
    print(f"\n{'━' * 60}")
    print(f"  POST-LAUNCH ADOPTION ASSESSMENT")
    print(f"  {initiative}")
    print(f"{'━' * 60}")
    print(f"  Weeks Since Launch: {weeks}")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d')}")
    print()
    
    # Adoption Measures
    print(f"  ADOPTION MEASURES")
    print(f"  {'─' * 50}")
    for item in MEASURE_CATEGORIES["Adoption"]:
        print(f"  [  ] {item}")
        print(f"     Current: ________  Target: ________")
    print()
    
    print(f"  PROFICIENCY MEASURES")
    print(f"  {'─' * 50}")
    for item in MEASURE_CATEGORIES["Proficiency"]:
        print(f"  [  ] {item}")
        print(f"     Current: ________  Target: ________")
    print()
    
    print(f"  SUSTAINMENT MEASURES")
    print(f"  {'─' * 50}")
    for item in MEASURE_CATEGORIES["Sustainment"]:
        print(f"  [  ] {item}")
        print(f"     Current: ________  Target: ________")
    print()
    
    # Common post-launch issues
    print(f"  COMMON POST-LAUNCH ISSUES — CHECK FOR")
    print(f"  {'─' * 50}")
    issues = [
        "Technical completion mistaken for business readiness",
        "Training completion mistaken for proficiency",
        "Initial adoption declining after week 2-3",
        "Legacy workarounds re-emerging under pressure",
        "Managers not coaching new behaviours",
        "Escalation channels not functioning for adoption issues",
        "Reinforcement mechanisms not activated"
    ]
    for issue in issues:
        print(f"  [  ] {issue}")
    print()

def cmd_impact(initiative, options):
    """Stakeholder impact analysis."""
    stakeholders = [s.strip() for s in options.get("stakeholders", "").split(",") if s.strip()]
    risk = options.get("risk", "medium")
    
    print(f"\n{'━' * 60}")
    print(f"  STAKEHOLDER IMPACT ANALYSIS")
    print(f"  {initiative}")
    print(f"{'━' * 60}")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"  Overall Risk: {risk.upper()}")
    print()
    
    # Impact Dimensions
    print(f"  IMPACT DIMENSIONS — ASSESS PER GROUP")
    print(f"  {'─' * 50}")
    for dim in IMPACT_DIMENSIONS:
        print(f"  • {dim}")
    print()
    
    # Per-group assessment
    if stakeholders:
        for group in stakeholders:
            print(f"  {'━' * 50}")
            print(f"  GROUP: {group}")
            print(f"  {'━' * 50}")
            print(f"  Impact Level: [  ] High  [  ] Medium  [  ] Low")
            print(f"  Current Adoption Stage: [  ] Awareness  [  ] Commitment  [  ] Knowledge  [  ] Ability  [  ] Reinforcement")
            print(f"  Key Impacts:")
            for dim in IMPACT_DIMENSIONS[:5]:
                print(f"    • {dim}: ____________________________")
            print(f"  Top Risks:")
            print(f"    1. ____________________________")
            print(f"    2. ____________________________")
            print(f"    3. ____________________________")
            print(f"  Recommended Actions:")
            print(f"    1. ____________________________")
            print(f"    2. ____________________________")
            print()
    
    # Risk Matrix
    print(f"  RISK RATING GUIDE")
    print(f"  {'─' * 50}")
    print(f"  HIGH:    Critical role changes, heavy training, compliance exposure")
    print(f"  MEDIUM:  Moderate process changes, some new tools, role adjustments")
    print(f"  LOW:     Minor changes, awareness-level updates, minimal disruption")
    print()

def cmd_resistance(initiative, options):
    """Resistance and friction response plan."""
    friction = [f.strip() for f in options.get("friction-points", "").split(",") if f.strip()]
    
    print(f"\n{'━' * 60}")
    print(f"  RESISTANCE & FRICTION RESPONSE PLAN")
    print(f"  {initiative}")
    print(f"{'━' * 60}")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d')}")
    print()
    
    print(f"  RESISTANCE IS OPERATIONAL INFORMATION")
    print(f"  It signals where intervention is required, not where employees are failing.")
    print()
    
    # Common sources
    print(f"  COMMON SOURCES OF RESISTANCE")
    print(f"  {'─' * 50}")
    for source in RESISTANCE_SOURCES:
        marker = "▸ " if source in friction else "  "
        print(f"  {marker}{source}")
    print()
    
    # Response actions
    print(f"  RESPONSE ACTIONS")
    print(f"  {'─' * 50}")
    responses = {
        "unclear value": "Connect the change to business outcomes the group cares about. Use specific examples.",
        "loss of autonomy": "Give groups input on how they implement within the new framework.",
        "increased workload": "Show the long-term efficiency gain. Remove low-value legacy tasks.",
        "confusion about roles or controls": "Provide clear, role-specific guidance. Test understanding.",
        "distrust in leadership intent": "Increase sponsor visibility. Address concerns directly.",
        "previous change fatigue": "Acknowledge the volume. Sequence changes. Show what's being de-prioritized.",
        "weak manager support": "Equip managers with conversation guides. Coach them directly.",
        "insufficient training or practice": "Add hands-on practice. Extend support window. Add coaching.",
        "fear of compliance or audit exposure": "Clarify what's expected vs what's penalized. Provide safety nets."
    }
    
    if friction:
        for point in friction:
            resp = responses.get(point, "Assess root cause and tailor response.")
            print(f"  ▸ {point}")
            print(f"    Response: {resp}")
            print(f"    Owner: ____________")
            print(f"    Target Date: ____________")
            print()
    else:
        for source, resp in responses.items():
            print(f"  • {source}")
            print(f"    → {resp}")
            print()
    
    # Escalation guidance
    print(f"  ESCALATION GUIDANCE")
    print(f"  {'─' * 50}")
    print(f"  Escalate to sponsor when:")
    print(f"    • Resistance is spreading across multiple groups")
    print(f"    • Manager interventions are not working")
    print(f"    • Resistance is impacting delivery timelines")
    print(f"    • Executive messaging is being questioned or discounted")
    print()

# --- CLI ---

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    cmd = sys.argv[1]
    options = {}
    args = sys.argv[2:]
    
    # First positional arg is the initiative name
    initiative = args[0] if args else "Initiative"
    remaining = args[1:] if len(args) > 1 else []
    
    i = 0
    while i < len(remaining):
        if remaining[i] == "--impacted-groups" and i + 1 < len(remaining):
            options["impacted-groups"] = remaining[i + 1]; i += 2
        elif remaining[i] == "--timeline" and i + 1 < len(remaining):
            options["timeline"] = remaining[i + 1]; i += 2
        elif remaining[i] == "--sponsor" and i + 1 < len(remaining):
            options["sponsor"] = remaining[i + 1]; i += 2
        elif remaining[i] == "--phase" and i + 1 < len(remaining):
            options["phase"] = remaining[i + 1]; i += 2
        elif remaining[i] == "--weeks-since-launch" and i + 1 < len(remaining):
            options["weeks-since-launch"] = remaining[i + 1]; i += 2
        elif remaining[i] == "--stakeholders" and i + 1 < len(remaining):
            options["stakeholders"] = remaining[i + 1]; i += 2
        elif remaining[i] == "--risk" and i + 1 < len(remaining):
            options["risk"] = remaining[i + 1]; i += 2
        elif remaining[i] == "--friction-points" and i + 1 < len(remaining):
            options["friction-points"] = remaining[i + 1]; i += 2
        else:
            i += 1
    
    if cmd == "readiness":
        cmd_readiness(initiative, options)
    elif cmd == "sponsor":
        cmd_sponsor(initiative, options)
    elif cmd == "adoption":
        cmd_adoption(initiative, options)
    elif cmd == "impact":
        cmd_impact(initiative, options)
    elif cmd == "resistance":
        cmd_resistance(initiative, options)
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
