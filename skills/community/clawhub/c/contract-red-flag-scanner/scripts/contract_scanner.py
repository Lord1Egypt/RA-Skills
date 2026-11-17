#!/usr/bin/env python3
"""Contract Red Flag Scanner — offline first-pass triage for contracts.

Scans plain contract text for high-risk clause patterns, infers the
contract type, ranks findings, checks for missing protections, and
emits a question list for the other side. Pure stdlib.

Usage:
    python3 contract_scanner.py scan <file.txt> [--json] [--type lease]
    python3 contract_scanner.py list-detectors
Exit codes: 0 = no HIGH findings, 2 = HIGH findings present, 1 = error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict

# --------------------------------------------------------------------------
# Detector library
# --------------------------------------------------------------------------
# Each detector: id, title, base severity, regex patterns (case-insensitive,
# DOTALL where noted), plain-language explanation, question to ask.


@dataclass
class Finding:
    detector: str
    title: str
    severity: str
    matched_text: str
    explanation: str
    question: str


DETECTORS = [
    {
        "id": "auto_renewal",
        "title": "AUTO-RENEWAL WITH STRICT NOTICE WINDOW",
        "severity": "HIGH",
        "patterns": [
            r"automatic(ally)? renew\w*",
            r"renew\w* for (an additional|successive|another)",
            r"notice[^.]{0,80}(not less than\s+)?(\d{1,3})\s*(\(?\d{0,3}\)?\s*)?(days|months)[^.]{0,60}(prior to|before)[^.]{0,60}(expiration|end of (the )?(term|initial term))",
        ],
        "explanation": (
            "The contract renews itself automatically unless YOU remember to send "
            "written notice inside a narrow window (often 30-90 days before term end). "
            "Miss the window by a day and you are committed to a full new term. This is "
            "the single most common way people get trapped in leases and subscriptions."
        ),
        "question": (
            "Can renewal convert to month-to-month after the initial term, or can the "
            "notice window shrink to 30 days with acceptance by email?"
        ),
    },
    {
        "id": "termination_acceleration",
        "title": "EARLY TERMINATION — RENT ACCELERATION / ALL REMAINING PAYMENTS",
        "severity": "HIGH",
        "patterns": [
            r"(all|entire|remaining) (amounts?|rent|payments?|balance)[^.]{0,80}(become|shall become|immediately)[^.]{0,40}(due|payable)",
            r"accelerat\w+ (of )?(rent|payment|the balance)",
            r"terminate[^.]{0,120}liable for[^.]{0,60}(all|remaining|entire)",
            r"early termination fee of[^.]{0,40}(two|three|four|2|3|4|x|×)\s*(month|rent)",
        ],
        "explanation": (
            "Breaking the contract early makes you owe everything (or several months) at "
            "once — not just the notice period. In some states this is unenforceable as a "
            "penalty, but you'd have to fight it. Know the worst case before you sign."
        ),
        "question": (
            "What exactly do I owe if I leave early — notice-period rent only, a defined "
            "fee, or all remaining rent? Can we cap early-exposure at two months' rent?"
        ),
    },
    {
        "id": "arbitration",
        "title": "BINDING ARBITRATION / CLASS-ACTION WAIVER",
        "severity": "HIGH",
        "patterns": [
            r"binding arbitration",
            r"arbitrat\w+[^.]{0,100}(final|binding|exclusive remedy)",
            r"waive[^.]{0,60}(class action|jury|participate in any class)",
            r"class action waiver",
        ],
        "explanation": (
            "Disputes go to a private arbitrator instead of court, and you usually give up "
            "joining class actions. Arbitration fees can exceed the disputed amount, which "
            "in practice kills small claims. Some clauses are unenforceable in some "
            "jurisdictions — a lawyer can tell you in minutes."
        ),
        "question": (
            "Is arbitration mandatory, or can we strike this clause / opt out in writing "
            "within 30 days if the contract offers an opt-out?"
        ),
    },
    {
        "id": "unilateral_amendment",
        "title": "UNILATERAL AMENDMENT — 'WE MAY CHANGE THESE TERMS'",
        "severity": "HIGH",
        "patterns": [
            r"(we|company|landlord)\s+(may|reserves? the right to)[^.]{0,80}(change|modify|amend|update)[^.]{0,60}(these terms|this agreement|the terms|this lease|these rules|the rules|this policy|these policies)[^.]{0,80}(at any time|without notice|in its sole discretion|upon notice)",
            r"terms[^.]{0,40}subject to change[^.]{0,40}(at any time|without (prior )?notice)",
            r"continued (use|occupancy)[^.]{0,60}(shall )?(constitute|be deemed)[^.]{0,30}acceptance",
        ],
        "explanation": (
            "The other side can rewrite the deal later without your agreement. Watch for "
            "'continued use constitutes acceptance' riders — they make silence a yes."
        ),
        "question": (
            "Will material changes require my signed consent (or at least 30 days' notice "
            "plus a right to cancel without penalty)?"
        ),
    },
    {
        "id": "non_compete",
        "title": "NON-COMPETE / NON-SOLICIT CLAUSE",
        "severity": "HIGH",
        "patterns": [
            r"non-?compet\w+",
            r"shall not[^.]{0,80}(directly or indirectly)?[^.]{0,80}engag?e? in[^.]{0,60}(any business|competition|the same)",
            r"not[^.]{0,60}(solicit|hire|recruit)[^.]{0,60}(employees|customers|clients)",
        ],
        "explanation": (
            "Restricts where you can work or who you can do business with AFTER the "
            "contract ends. Scope, geography, and duration matter enormously; several "
            "jurisdictions ban or limit non-competes for employees entirely."
        ),
        "question": (
            "What are the exact scope, radius, and duration of the restriction — and is it "
            "enforceable in my state? Can we limit it to direct competitors, 12 months?"
        ),
    },
    {
        "id": "late_fee",
        "title": "LATE FEE — FLAT PLUS DAILY ACCRETION",
        "severity": "MEDIUM",
        "patterns": [
            r"late (fee|charge)[^.]{0,80}\$?\s*\d+",
            r"late (fee|charge)[^.]{0,60}(per day|each day|daily)",
            r"\d+(\.\d+)?%[^.]{0,30}(per (calendar )?month|per diem|monthly)[^.]{0,40}(late|overdue|interest)",
            r"returned payment[^.]{0,60}\$?\s*\d+",
        ],
        "explanation": (
            "Quantify the failure cost: a flat fee plus a per-day charge plus a percentage "
            "compounding monthly can snowball from a single late payment. Many states cap "
            "late fees; check yours."
        ),
        "question": (
            "Is there a grace period before the late fee applies, and a hard cap on total "
            "late charges? Can the fee be a flat amount with no daily accretion?"
        ),
    },
    {
        "id": "deposit_risk",
        "title": "SECURITY DEPOSIT — VAGUE OR ONE-SIDED TERMS",
        "severity": "MEDIUM",
        "patterns": [
            r"security deposit[^.]{0,200}(damage|damages|cleaning|professional cleaning|withhold)",
            r"deposit[^.]{0,80}non-?refundable",
            r"deposit[^.]{0,120}(as|for) (liquidated )?damages",
        ],
        "explanation": (
            "Deposits are the most-litigated clause in leasing. Look for: 'professional "
            "cleaning' at landlord's discretion, deposit forfeited as liquidated damages, "
            "or no stated return deadline. Absence of a deadline is a red flag by itself."
        ),
        "question": (
            "By what date after move-out is the deposit (plus itemized deductions) "
            "returned, and can deductions require photos/receipts?"
        ),
    },
    {
        "id": "indemnification",
        "title": "ONE-SIDED INDEMNIFICATION",
        "severity": "MEDIUM",
        "patterns": [
            r"indemnify[^.]{0,120}(and hold harmless)?",
            r"hold(s)? (you |the \w+ )?harmless[^.]{0,100}(claims|losses|liabilit)",
            r"defend[^.]{0,60}against (any|all) claims",
        ],
        "explanation": (
            "You cover the other side's legal costs and losses, even for things they partly "
            "caused. Check whether it's mutual or one-way — one-way indemnity means you "
            "carry all the risk."
        ),
        "question": (
            "Can indemnification be mutual and limited to third-party claims caused by "
            "each party's own negligence?"
        ),
    },
    {
        "id": "liability_cap",
        "title": "LIABILITY CAP / DAMAGES WAIVER",
        "severity": "MEDIUM",
        "patterns": [
            r"(in no event|under no circumstances)[^.]{0,120}(liable|responsible)[^.]{0,80}",
            r"limitation of liability",
            r"(consequential|incidental|indirect)[^.]{0,40}damages",
            r"total (aggregate )?liability[^.]{0,80}(shall not exceed|is limited to)[^.]{0,60}(\$?\s*\d+|fees paid)",
        ],
        "explanation": (
            "Caps THEIR liability to you (often to 'fees paid in the last 12 months') while "
            "yours stays unlimited via indemnification. Asymmetry is the point: read this "
            "together with the indemnity clause."
        ),
        "question": (
            "Is the liability cap mutual? For a paid service, what happens to my data or "
            "deposit if you breach — is that capped too?"
        ),
    },
    {
        "id": "attorney_fees",
        "title": "ONE-SIDED ATTORNEY FEES",
        "severity": "MEDIUM",
        "patterns": [
            r"attorney(s'?|'s)?\s*fees[^.]{0,80}(incurred by (the )?(landlord|company|employer))",
            r"reasonable attorney(s'?|'s)?\s*fees[^.]{0,60}(shall be paid by|borne by) (tenant|you|employee|the other)",
            r"attorney(s'?|'s)?\s*fees[^.]{0,60}(incurred by)[^.]{0,40}(landlord|company|employer)",
        ],
        "explanation": (
            "The winner-gets-fees rule is fine; LANDLORD-always-gets-fees is not. One-sided "
            "fee clauses make contesting anything economically irrational."
        ),
        "question": (
            "Can attorney fees go to the PREVAILING party in any dispute, not just to you?"
        ),
    },
    {
        "id": "entry_rights",
        "title": "ENTRY WITHOUT NOTICE",
        "severity": "MEDIUM",
        "patterns": [
            r"(enter|access)[^.]{0,80}(the (premises|property|unit|unit))[^.]{0,120}(any time|without notice|at any time|with (a )?copy of the key|sole discretion)",
            r"right of access[^.]{0,80}any time",
        ],
        "explanation": (
            "Landlord/vendor entry with no notice or at any time. Most states require "
            "'reasonable notice' (24-48h) except emergencies; if it's not in writing, you "
            "can't enforce it."
        ),
        "question": (
            "Can we add 24-hour written notice for non-emergency entry, and an emergency "
            "definition limited to fire/flood/gas?"
        ),
    },
    {
        "id": "as_is",
        "title": "AS-IS CONDITION / CONDITION WAIVER",
        "severity": "MEDIUM",
        "patterns": [
            r"as-?is[^.]{0,80}(condition|basis|where-?is)",
            r"no (representations|warranties)[^.]{0,60}(condition|fitness|merchantab)",
            r"tenant[^.]{0,60}accepts?[^.]{0,60}(premises|property)[^.]{0,40}as-?is",
        ],
        "explanation": (
            "You accept the property/product exactly as found, defects included, and waive "
            "reliance on any verbal promises. Any promise that matters must be written INTO "
            "the contract to survive this clause."
        ),
        "question": (
            "Which repairs will be completed (with dates) before this is signed? Can we "
            "list them in an addendum that survives the as-is clause?"
        ),
    },
    {
        "id": "ip_assignment",
        "title": "BROAD IP ASSIGNMENT ('WORK FOR HIRE' SCOPE)",
        "severity": "MEDIUM",
        "patterns": [
            r"(assign|assignment of)[^.]{0,60}(all right, title|all inventions|all intellectual property)",
            r"work (made )?for hire",
            r"conceived[^.]{0,80}(during|in the course of)[^.]{0,60}(employment|engagement)",
        ],
        "explanation": (
            "For employees this is standard and mostly fine; for contractors, 'all IP "
            "conceived during the engagement' can sweep in your unrelated side projects. "
            "Scope it to work product for THIS client."
        ),
        "question": (
            "Can IP assignment be limited to work performed for this project/company, "
            "excluding pre-existing and unrelated IP (listed in an exhibit)?"
        ),
    },
    {
        "id": "non_disparagement",
        "title": "NON-DISPARAGEMENT CLAUSE",
        "severity": "LOW",
        "patterns": [
            r"non-?disparag\w+",
            r"shall not[^.]{0,60}(disparage|make (any )?negative|harmful) (statements?|comments?)",
        ],
        "explanation": (
            "You can't say anything negative about them, ever. These have been ruled "
            "unlawful in some consumer/employment contexts (they can gag legitimate "
            "complaints), but you shouldn't rely on that."
        ),
        "question": "Can this be limited to knowingly false statements only?",
    },
    {
        "id": "governing_law",
        "title": "GOVERNING LAW / VENUE FAR FROM YOU",
        "severity": "LOW",
        "patterns": [
            r"governed by the laws of the state of [^.]{3,60}",
            r"exclusive (jurisdiction|venue)[^.]{0,80}(courts? of|located in)",
            r"venue[^.]{0,60}(shall be|lies in)[^.]{0,60}(county of|state of)",
        ],
        "explanation": (
            "Disputes happen in THEIR state, under THEIR law — plane tickets and an out-of-"
            "town lawyer for you. For small consumer contracts this effectively waives "
            "enforcement both ways, but it's their waiver, not yours."
        ),
        "question": (
            "Can venue be 'the defendant's county of residence' instead of a fixed state?"
        ),
    },
    {
        "id": "assignment",
        "title": "ASSIGNMENT WITHOUT YOUR CONSENT",
        "severity": "LOW",
        "patterns": [
            r"(may|right to) assign[^.]{0,100}(without (your|tenant's|the other party's )?(prior )?consent|notice)",
            r"assigns? and successors[^.]{0,60}without",
        ],
        "explanation": (
            "They can transfer your contract (your lease, your debt, your agreement) to "
            "anyone — a collections agency, a worse property manager — while YOU usually "
            "can't assign yours."
        ),
        "question": (
            "Can assignment require my written consent (not to be unreasonably withheld)?"
        ),
    },
    {
        "id": "cancellation_fee",
        "title": "SUBSCRIPTION CANCELLATION FRICTION",
        "severity": "MEDIUM",
        "patterns": [
            r"cancell?ation[^.]{0,60}(fee|charge|penalty)[^.]{0,40}\$?\s*\d+",
            r"(cancel|cancell\w+)[^.]{0,80}(in writing|by certified mail|in person|only by phone)[^.]{0,60}(no later than|at least)",
            r"early cancell\w+[^.]{0,60}(fee|charge)[^.]{0,40}(of\s+)?\$?\s*\d+",
        ],
        "explanation": (
            "Cancellation exists only through a narrow channel with a fee and a deadline — "
            "the gym-membership pattern. Note the exact method NOW or you'll pay for the "
            "months you thought you'd cancelled."
        ),
        "question": (
            "Can I cancel online with written confirmation, effective the last day of the "
            "current billing period, with no fee after month N?"
        ),
    },
    {
        "id": "auto_billing",
        "title": "AUTOMATIC BILLING / STORED PAYMENT",
        "severity": "LOW",
        "patterns": [
            r"(automatic|recurring)[^.]{0,40}(billing|payment|charge)",
            r"(card|payment method)[^.]{0,80}(on file|kept on file|stored)[^.]{0,60}(charge|bill)",
        ],
        "explanation": (
            "Payments charge automatically until you cancel, and the stored card becomes "
            "the enforcement mechanism for every fee clause above. Calendar the renewal "
            "window the day you sign."
        ),
        "question": (
            "Will you notify me 7 days before every recurring charge over $X, and can I "
            "get a prorated refund on unused time if I cancel mid-period?"
        ),
    },
    {
        "id": "jury_waiver",
        "title": "JURY TRIAL WAIVER",
        "severity": "HIGH",
        "patterns": [
            r"waive[^.]{0,60}(the right to|any right to)?[^.]{0,30}(a )?jury trial",
            r"jury trial waiver",
            r"(trial by jury|jury of any kind|right to a jury|trial by jury of any|jury trial)",
        ],
        "explanation": (
            "Even where arbitration is struck down, this separate waiver removes a jury. "
            "Courts scrutinize these heavily; they also signal the drafter expects disputes."
        ),
        "question": "Can this waiver be removed if arbitration is removed?",
    },
    {
        "id": "liquidated_damages",
        "title": "LIQUIDATED DAMAGES FORFEITURE",
        "severity": "MEDIUM",
        "patterns": [
            r"liquidated damages[^.]{0,80}(and not (as )?(a )?penalty)",
            r"(forfeit|forfeiture)[^.]{0,60}(deposit|payment|fees paid)",
        ],
        "explanation": (
            "A fixed sum you owe/forfeit regardless of actual harm — drafted as 'not a "
            "penalty' precisely because penalties are unenforceable. Whether a court "
            "agrees depends on how wildly it exceeds real damages."
        ),
        "question": (
            "How was this amount calculated, and can it credit against actual damages only?"
        ),
    },
]

# --------------------------------------------------------------------------
# Contract-type inference
# --------------------------------------------------------------------------

TYPE_KEYWORDS = {
    "lease": [
        "landlord", "tenant", "premises", "lease", "rent", "security deposit",
        "sublease", "habitability", "move-in", "move-out", "apartment",
    ],
    "employment": [
        "employee", "employer", "salary", "position", "at-will", "duties",
        "benefits", "termination of employment", "base compensation", "offer of employment",
    ],
    "tos": [
        "terms of service", "user agreement", "the service", "account",
        "end user", "website", "platform", "users of the service", "acceptable use",
    ],
    "subscription": [
        "membership", "monthly", "billing cycle", "subscription", "gym",
        "renewal term", "initiation fee", "month-to-month",
    ],
}

# Missing-clause checklist per type: (label, list of regexes that would satisfy it)
MISSING_CLAUSES = {
    "lease": [
        ("Landlord repair / habitability obligation",
         [r"repair", r"habitab\w+", r"maintain (the )?premises"]),
        ("Security deposit return deadline (days)",
         [r"deposit[^.]{0,200}(\d{1,2})\s*days", r"return\w*[^.]{0,80}within \d{1,2} days"]),
        ("Entry notice requirement",
         [r"(24|48|twenty-?four|forty-?eight)[^-.]{0,20}hours'? (prior )?notice", r"reasonable notice"]),
        ("Grace period before late fee",
         [r"grace period"]),
    ],
    "employment": [
        ("Termination notice or severance terms",
         [r"(severance|notice of termination|termination pay)"]),
        ("Dispute of deductions / final paycheck timing",
         [r"final (paycheck|wages)[^.]{0,80}(within )?\d"]),
        ("Job title and duties defined",
         [r"(title|position)[^.]{0,60}(reports? to|duties|responsibilit)"]),
    ],
    "tos": [
        ("Data deletion / export on account closure",
         [r"(export|download) your (data|content)", r"delet\w+ (your |the )?(data|account)"]),
        ("Service availability or refund commitment",
         [r"(uptime|service credit|refund)"]),
        ("Notice of material term changes",
         [r"notify[^.]{0,60}(you|users)[^.]{0,60}(before|prior to)[^.]{0,40}(chang|amend|updat)"]),
    ],
    "subscription": [
        ("Cancellation method stated explicitly",
         [r"cancel[^.]{0,80}(online|by (phone|mail|email|writing)|in person|at any (location|club))"]),
        ("Refund/proration policy on cancellation",
         [r"(refund|prorat\w+|credit)[^.]{0,60}(cancell|unused|remaining)"]),
    ],
}

SEVERITY_WEIGHT = {"HIGH": 10, "MEDIUM": 4, "LOW": 1}


def normalize(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\r\n?", "\n", text)
    return text


def detect_type(text: str) -> tuple[str, float]:
    lower = text.lower()
    scores = {}
    total_words = max(len(lower.split()), 1)
    for ctype, kws in TYPE_KEYWORDS.items():
        hits = sum(lower.count(kw) for kw in kws)
        scores[ctype] = hits
    best = max(scores, key=lambda k: scores[k])
    if scores[best] == 0:
        return "general", 0.0
    confidence = min(scores[best] / (sum(scores.values()) + 1e-9), 1.0)
    return best, round(confidence, 2)


def find_all(text: str, pattern: str, limit: int = 2) -> list[str]:
    # contract text wraps lines mid-phrase; treat literal spaces as any whitespace
    pattern = pattern.replace(" ", r"\s+")
    out = []
    for m in re.finditer(pattern, text, re.IGNORECASE | re.DOTALL):
        start, end = m.start(), m.end()
        snippet = text[max(0, start - 60):min(len(text), end + 80)]
        snippet = re.sub(r"\s+", " ", snippet).strip()
        out.append(snippet)
        if len(out) >= limit:
            break
    return out


def scan_text(text: str, forced_type: str | None = None) -> dict:
    text = normalize(text)
    ctype, conf = detect_type(text)
    if forced_type:
        ctype = forced_type

    findings: list[Finding] = []
    for det in DETECTORS:
        for pat in det["patterns"]:
            for snippet in find_all(text, pat):
                findings.append(Finding(
                    detector=det["id"],
                    title=det["title"],
                    severity=det["severity"],
                    matched_text=snippet[:400],
                    explanation=det["explanation"],
                    question=det["question"],
                ))
                break  # one finding per pattern-group is enough for triage

    # de-duplicate by detector
    seen: set[str] = set()
    uniq: list[Finding] = []
    for f in findings:
        if f.detector not in seen:
            seen.add(f.detector)
            uniq.append(f)

    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    uniq.sort(key=lambda f: order[f.severity])

    score = min(sum(SEVERITY_WEIGHT[f.severity] for f in uniq) * 2, 100)

    # missing-clause checklist
    missing = []
    for label, satisfaction_pats in MISSING_CLAUSES.get(ctype, []):
        if not any(re.search(p, text, re.IGNORECASE) for p in satisfaction_pats):
            missing.append(label)

    return {
        "contract_type": ctype,
        "type_confidence": conf,
        "scrutiny_score": score,
        "counts": {
            "HIGH": sum(1 for f in uniq if f.severity == "HIGH"),
            "MEDIUM": sum(1 for f in uniq if f.severity == "MEDIUM"),
            "LOW": sum(1 for f in uniq if f.severity == "LOW"),
        },
        "findings": [asdict(f) for f in uniq],
        "missing_protections": missing,
        "questions": [f.question for f in uniq],
    }


def render(report: dict) -> str:
    lines = []
    lines.append(f"CONTRACT TYPE: {report['contract_type']} "
                 f"(confidence {report['type_confidence']})")
    c = report["counts"]
    lines.append(f"SCRUTINY SCORE: {report['scrutiny_score']}/100 — "
                 f"{c['HIGH']} HIGH, {c['MEDIUM']} MEDIUM, {c['LOW']} LOW findings")
    lines.append("")
    for f in report["findings"]:
        lines.append(f"[{f['severity']}] {f['title']}")
        lines.append(f"  Matched: \"{f['matched_text']}\"")
        lines.append(f"  Plain language: {f['explanation']}")
        lines.append(f"  Ask: {f['question']}")
        lines.append("")
    if report["missing_protections"]:
        lines.append(f"MISSING-CLAUSE CHECKLIST ({report['contract_type']}):")
        for label in report["missing_protections"]:
            lines.append(f"  [ ] {label} — NOT FOUND")
        lines.append("")
    if report["questions"]:
        lines.append("QUESTION LIST FOR THE OTHER SIDE:")
        for i, q in enumerate(report["questions"], 1):
            lines.append(f"  {i}. {q}")
    if report["counts"]["HIGH"] >= 2 or report["scrutiny_score"] >= 60:
        lines.append("")
        lines.append("RECOMMENDATION: 2+ HIGH findings or score >= 60 — "
                     "have a lawyer review the flagged clauses before signing "
                     "(targeted review is far cheaper than full review).")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Contract red-flag triage scanner")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan", help="scan a contract text file")
    s.add_argument("file")
    s.add_argument("--json", action="store_true")
    s.add_argument("--type", choices=list(TYPE_KEYWORDS) + ["general"])
    sub.add_parser("list-detectors", help="list all detectors")
    args = ap.parse_args()

    if args.cmd == "list-detectors":
        for det in DETECTORS:
            print(f"[{det['severity']:6}] {det['title']}")
        return 0

    try:
        text = open(args.file, encoding="utf-8", errors="replace").read()
    except OSError as e:
        print(f"error: cannot read {args.file}: {e}", file=sys.stderr)
        return 1

    if len(text.strip()) < 80:
        print("error: file too short to be a contract (<80 chars). Extract the "
              "full text including schedules/exhibits.", file=sys.stderr)
        return 1

    report = scan_text(text, forced_type=args.type)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render(report))
    return 2 if report["counts"]["HIGH"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
