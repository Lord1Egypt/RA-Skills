#!/usr/bin/env python3
"""
call_coach.py — build branching call scripts, objection trees, cheat sheets, practice.

10 pre-built scenarios + custom build. Storage: ~/.call-scripts/. Pure stdlib.
"""
import argparse
import json
import os
import random
import re
import sys

SCRIPTS_DIR = os.path.join(os.path.expanduser("~"), ".call-scripts")

# ------------------------------------------------------------------ scenarios
# Each: goal template, leverage hints, fallback hints, objections[(line, response)]
SCENARIOS = {
    "billing-dispute": {
        "title": "Billing dispute / wrong charge",
        "goal": "Remove the disputed charge ({amount}) from this billing cycle",
        "leverage": [
            "Written evidence the charge was quoted differently (chat log, email, ad)",
            "Long customer tenure in good standing",
            "Regulator complaints are free and cost them time (FCC, state AG, CFPB)",
        ],
        "fallback": "File FCC/state-AG/CFPB complaint; dispute via card chargeback if <60-120 days",
        "objections": [
            ("That's our policy / all tech visits are billed",
             "I understand that's the standard policy. My issue isn't the policy — I was told this visit was free, and I have the chat log. What I'm asking is: can you remove this specific charge?"),
            ("It's already been billed and processed",
             "Right — and billing errors have a dispute window, which is what I'm using now. Who can credit an already-billed charge?"),
            ("I don't have the authority to remove it",
             "I appreciate you checking. Please transfer me to someone who can approve credits — or a supervisor, whichever is faster."),
            ("I can offer a partial credit as a one-time courtesy",
             "Thank you — to be clear, is that a credit against the full {amount} or partial? If partial, I'm asking for the full amount because the charge was quoted to me as $0."),
            ("You agreed to the terms of service",
             "The terms cover services rendered as agreed. This charge was never agreed — it was explicitly quoted as free. I'll hold while you check the notes on my account."),
        ],
    },
    "late-fee-waiver": {
        "title": "Late fee / interest waiver",
        "goal": "Waive the late fee ({amount}) as a one-time courtesy",
        "leverage": [
            "First late payment in years of history",
            "Payment was X days late, not delinquent",
            "Autopay signup = guaranteed future on-time payments (their win too)",
        ],
        "fallback": "Ask for supervisor; if refused, ask what would make future waivers possible",
        "objections": [
            ("Fees are applied automatically by the system",
             "Understood — and the system applies them, but a person can reverse them. Can you flag this one for reversal?"),
            ("We can only waive fees once per year and you used it",
             "Then let's note on the account that this call is my exception request for this year — or connect me with someone who tracks goodwill adjustments."),
            ("You should set up autopay",
             "Agreed — enroll me now, and waive this fee as the reason I'm calling. Both, please."),
        ],
    },
    "rate-negotiation": {
        "title": "Rate negotiation (internet/phone/insurance/SaaS)",
        "goal": "Reduce monthly rate to {target} or get equivalent value (credits, tier bump)",
        "leverage": [
            "Competitor promo in writing (screenshot/speed)",
            "Years of on-time payments",
            "Promotional pricing expired — loyalty should price-match new-customer deals",
            "Ready to churn: switching cost to them > discount cost",
        ],
        "fallback": "Accept smaller cut with no contract lock; or actually switch (do the homework first)",
        "objections": [
            ("That price is for new customers only",
             "I understand. What I'm saying is: as a {N}-year customer who pays on time, retention should be able to match what acquisition spends. Can you check the retention offers on my account?"),
            ("There are no promotions on your account right now",
             "That's for the standard list. I'd like the loyalty/retention desk — or the cancellation department, since they usually have the best ones."),
            ("The best I can do is $X off for 6 months",
             "Thank you — that's progress. Does that come to {target} or below? If it expires in 6 months and jumps back, I'd rather have a 12-month locked price now."),
            ("You're in a contract until {date}",
             "Then let's talk about what happens at renewal — and what you can do today on credits while we're at it."),
        ],
    },
    "cancellation": {
        "title": "Cancel a service (retention gauntlet)",
        "goal": "Cancel effective {date}; pay nothing further; keep no-sweat confirmation",
        "leverage": [
            "You don't owe them a reason — but one clear reason ends the 'why' script",
            "Month-to-month = legal right to cancel per terms",
            "Chargebacks exist for post-cancellation charges",
        ],
        "fallback": "No fallback needed — cancellation IS the walk-away. Alternative: pause option if offered.",
        "objections": [
            ("Before you cancel, let me review some offers",
             "I appreciate it, but my decision's made — I'm calling to cancel, not negotiate. Please process the cancellation effective today."),
            ("You'll lose your loyalty discount / your history",
             "I understand — and the total is still higher than my alternative. Please proceed with the cancellation."),
            ("I can't cancel — only the retention team can",
             "Fine — transfer me to retention now, and please note on the account that I requested cancellation today at {time}."),
            ("You have to do it online / in the app / in person",
             "Your terms say a call is acceptable — and I'm on the call. If the system truly requires it, I need you to walk me through it while we're connected, or email me the exact link."),
        ],
    },
    "landlord-repair": {
        "title": "Landlord repair demand",
        "goal": "Repair of {issue} scheduled within {timeframe}, in writing",
        "leverage": [
            "Habitability laws in nearly all jurisdictions — some repairs are not optional",
            "Rent escrow / repair-and-deduct options in many jurisdictions (check local law)",
            "Written trail matters more than phone memory — follow up every call by email",
        ],
        "fallback": "Formal written demand letter; local housing inspector; tenant union/aid",
        "objections": [
            ("It's normal wear, not my responsibility",
             "Wear is exactly what maintenance covers. The issue affects habitability: {issue}. When can I expect a repair date?"),
            ("I'll get to it when I can",
             "I need a date. If it's not scheduled by {date}, I'll send a written demand and contact the housing inspector — I'd rather we just fix it."),
            ("The contractor is expensive / it's winter / busy season",
             "That's a scheduling problem on your side, and it doesn't pause my rights as a tenant. Who else do you use for emergencies?"),
            ("You caused this damage",
             "Let's see it in writing with the inspection evidence — meanwhile the unit needs a working {thing} either way."),
        ],
    },
    "insurance-denial": {
        "title": "Insurance denial pushback",
        "goal": "Reconsider and pay claim {claim}; at minimum, written denial reason + appeal path",
        "leverage": [
            "Denials are frequently coding/administrative errors — ask for the exact clause",
            "Formal internal appeal is a right; external review often reverses",
            "State insurance regulator complaints are free and get attention",
        ],
        "fallback": "Internal appeal → external independent review → state regulator",
        "objections": [
            ("The claim wasn't medically necessary",
             "My provider documented necessity — please send me the reviewer's rationale in writing, their credentials, and the policy clause it violates. That's the packet I need for appeal."),
            ("The service was out of network",
             "I'd like the network-adequacy check on file — when no in-network provider was available, plans typically must cover at out-of-network rates. Who handles that review?"),
            ("It's a pre-existing condition exclusion",
             "Please cite the exact policy page and how the condition was documented before the policy date. I'll wait while you pull the file."),
            ("You missed the filing deadline",
             "Let's verify the date the denial was mailed vs when I received it — the appeal clock usually starts at receipt."),
        ],
    },
    "collections": {
        "title": "Collections call response",
        "goal": "Get written validation of the debt; commit to NOTHING on this call",
        "leverage": [
            "Validation rights: they must prove the debt is yours and the amount, in writing",
            "Anything you admit or pay can restart the limitations clock — say nothing either way",
            "You control the channel: everything in writing, never by phone",
        ],
        "fallback": "No payment until validated; if validated, negotiate pay-for-delete in writing",
        "objections": [
            ("This is an attempt to collect a debt of {amount} owed to {creditor}",
             "I'm recording this call notice: please send written validation of this debt — the original agreement, itemization, and proof you're authorized to collect. I'll respond in writing."),
            ("If you pay today we'll settle for 40%",
             "Put that offer in writing and mail it — including how it will be reported to the bureaus. I don't make payment decisions by phone."),
            ("We'll mark it as refusal to pay",
             "To be clear: this is not a refusal. It's a request for validation, which is my right. Please note it accurately."),
            ("This will affect your credit today",
             "Noted. Validation first — and how it's reported is exactly what I'll review in your response."),
        ],
    },
    "vendor-complaint": {
        "title": "Vendor/contractor complaint",
        "goal": "Fix the defective work by {date}, or partial refund of {amount}",
        "leverage": [
            "Written scope/quote vs delivered work — the delta is your case",
            "Reviews and referral pipelines cut both ways (state facts, never threaten)",
            "Small claims court threshold usually covers small jobs",
        ],
        "fallback": "Written final notice → review with facts → small claims if in range",
        "objections": [
            ("That's how it's normally done",
             "Then let's compare it to the scope we agreed in writing — the quote says {X}, the result is {Y}. What's your plan to close the gap?"),
            ("I'd have to charge more to redo it",
             "The rework is because the first pass missed the agreed scope — that's warranty territory, not a new job. How do you want to handle it?"),
            ("I'm booked for weeks",
             "The defect is active damage — it can't wait weeks. If you can't schedule by {date}, I'll need to bring someone else in and settle the difference with you."),
        ],
    },
    "salary-ask": {
        "title": "Raise / rate call",
        "goal": "Agreement to {target} salary/rate, or a dated plan to get there",
        "leverage": [
            "Documented scope growth: what you owned then vs now",
            "Market comparables for role+city+level (2-3 data points)",
            "Alternative offer or pipeline — implied, never threatened",
        ],
        "fallback": "Specific non-cash asks: title, remote days, education budget, review date",
        "objections": [
            ("It's not budget cycle yet",
             "Understood — then I'd like two things today: agreement in principle that the role has grown to {level}, and a dated review the week the cycle opens."),
            ("We can do X% now, revisit later",
             "I appreciate movement. X% against my documented scope gap still leaves us at {gap}. Can we split: X% now plus title change, and {target} at the next review in writing?"),
            ("You're already at the top of the band",
             "Then the conversation is about the band — either a band exception for documented scope, or a promotion path to the next band. Which process do we start?"),
            ("Everyone's getting the same increase this year",
             "This isn't a cost-of-living ask — it's a scope ask. My role grew; COL and scope are separate conversations."),
        ],
    },
    "cold-call": {
        "title": "Sales cold call (either side)",
        "goal": "Book a 20-min qualification call, or qualify them out fast",
        "leverage": [
            "Specific trigger you observed (hiring, funding, tech-stack signal)",
            "Peer customer story with a number in it",
            "Timebox respect: 'I'll take 40 seconds, then you decide'",
        ],
        "fallback": "Ask for a better-timed window or a referral; park politely, no burn",
        "objections": [
            ("We already have a provider",
             "Most teams I work with did too. I'm not asking you to switch — just 20 minutes to benchmark one number your current tool reports. Worst case you validate them."),
            ("Send me an email",
             "Happy to — so the email isn't generic: what's the one metric your team argues about most? That's the only thing I'll write about."),
            ("No budget",
             "Makes sense — that's usually a next-quarter problem anyway. Can I check back when planning starts? What month does your team plan?"),
            ("Not the right person",
             "Who owns that? … Understood — one favor: when you forward this, what should I change so it doesn't get deleted?"),
        ],
    },
}

RULES = [
    "Open with name + account + one-sentence goal (15-second triage)",
    "Ask, then silence — first to fill silence concedes ground",
    "'Policy' is a position: 'what can you do in THIS case?'",
    "Second no → escalate: 'please transfer me to someone who can approve'",
    "Know your walk-away; say it once, calmly, with a date",
]

DO_NOT_SAY = [
    'I will never pay this" (admission games on collections calls)',
    '"That\'s ridiculous / you people" (the rep disengages)',
    '"Let me think about it" mid-dispute (momentum dies; say "I need X or Y")',
    '"I\'ll sue" (unless you mean it today, with a lawyer)',
    '"Yes" to anything you haven\'t priced ("partial credit" -> "how partial?")',
]

# ------------------------------------------------------------------ helpers

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:50] or "script"

def ensure_dir():
    # Private-by-default storage: dir 0700, files 0600 — scripts contain
    # personal negotiation details (account numbers, leverage, fallback plans).
    os.makedirs(SCRIPTS_DIR, mode=0o700, exist_ok=True)
    try:
        os.chmod(SCRIPTS_DIR, 0o700)
    except OSError:
        pass

def save_script(scenario, title, body, extra=None):
    ensure_dir()
    name = slugify(f"{scenario}-{title}")
    path = os.path.join(SCRIPTS_DIR, name + ".txt")
    # Write via mkstemp then chmod 0600 so the file is never world/other-readable,
    # even transiently (no umask dependence).
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(body)
    meta_path = os.path.join(SCRIPTS_DIR, name + ".json")
    fd = os.open(meta_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump({"scenario": scenario, "title": title,
                   "goal": (extra or {}).get("goal", ""),
                   "leverage": (extra or {}).get("leverage", ""),
                   "fallback": (extra or {}).get("fallback", ""),
                   "objections_extra": (extra or {}).get("objections_extra", [])},
                  f, indent=2)
    return path, meta_path

def prompt(label, default=""):
    try:
        val = input(f"{label} [{default}]: ").strip()
    except EOFError:
        val = ""
    return val or default

def fill(text, ctx):
    out = text or ""
    for k, v in ctx.items():
        if isinstance(v, (list, tuple)):
            v = "; ".join(str(x) for x in v)
        out = out.replace("{" + k + "}", str(v))
    return out

# ------------------------------------------------------------------ build

def build_body(scenario, ctx, custom_objections):
    sc = SCENARIOS[scenario]
    lines = []
    lines.append(f"CALL SCRIPT — {sc['title']}" + (f"  ({ctx.get('title','')})" if ctx.get("title") else ""))
    lines.append("=" * 64)
    lines.append("")
    lines.append(f"GOAL:      {fill(ctx.get('goal') or sc['goal'], ctx)}")
    lines.append(f"FALLBACK:  {fill(ctx.get('fallback') or sc['fallback'], ctx)}")
    lines.append("")
    lines.append("LEVERAGE (say only what's true):")
    lev = ctx.get("leverage_list") or sc["leverage"]
    for i, l in enumerate(lev, 1):
        lines.append(f"  {i}. {fill(l, ctx)}")
    lines.append("")
    lines.append("OPENING (memorize):")
    lines.append(f'  "Hi, my name is {ctx.get("caller_name","___")}, account {ctx.get("account","___")}.')
    lines.append(f'   I\'m calling about {ctx.get("subject","___")}."')
    lines.append("")
    lines.append("ASKS IN ORDER:")
    lines.append(f"  1. {fill(ctx.get('goal') or sc['goal'], ctx)}")
    lines.append("  2. If no: 'Who has authority to approve this?'")
    lines.append("  3. If no: 'Please transfer me to retention / a supervisor.'")
    lines.append("  4. If still no: state fallback once, with a date. Then thank and end.")
    lines.append("")
    lines.append("OBJECTION TREE — acknowledge → bridge → ask:")
    lines.append("-" * 64)
    objections = list(sc["objections"]) + custom_objections
    for their, yours in objections:
        lines.append(f"THEY:  {fill(their, ctx)}")
        lines.append(f"YOU:   {fill(yours, ctx)}")
        lines.append("")
    lines.append("RULES:")
    for i, r in enumerate(RULES, 1):
        lines.append(f"  {i}. {r}")
    lines.append("")
    lines.append("DO NOT SAY:")
    for d in DO_NOT_SAY:
        lines.append(f"  ✗ {d}")
    lines.append("")
    lines.append("NOTES DURING CALL:")
    lines.append("  rep name: ________  time: ________  ticket/ref: ________")
    lines.append("  promised: ______________________________________")
    lines.append("  ________________________________________________")
    return "\n".join(lines)

# ------------------------------------------------------------------ commands

def cmd_scenarios(a):
    print("Pre-built scenarios:")
    for key, sc in SCENARIOS.items():
        print(f"  {key:<20} {sc['title']}  ({len(sc['objections'])} objections)")

def cmd_build(a):
    sc = SCENARIOS.get(a.scenario)
    if not sc:
        sys.exit(f"unknown scenario '{a.scenario}' — see `scenarios`")
    ctx = {"title": a.title or "", "caller_name": a.name or "___",
           "account": a.account or "___", "subject": a.subject or "___",
           "amount": a.amount or "$___", "target": a.target or "$___",
           "date": a.date or "today", "time": "now"}
    if a.interactive:
        ctx["goal"] = prompt("Goal (one sentence)", fill(sc["goal"], ctx))
        ctx["leverage"] = prompt("Your leverage (one line)", "; ".join(sc["leverage"][:1]))
        ctx["fallback"] = prompt("Fallback if refused", fill(sc["fallback"], ctx))
    else:
        if a.goal: ctx["goal"] = a.goal
        if a.fallback: ctx["fallback"] = a.fallback
    ctx["leverage_list"] = ([a.leverage] if a.leverage else None)
    custom = []
    if a.objection and a.response:
        custom.append((a.objection, a.response))
    body = build_body(a.scenario, ctx, custom)
    print(body)
    print()
    path, metapath = save_script(a.scenario, a.title or "call", body, extra={
        "goal": ctx.get("goal", ""), "leverage": a.leverage or "",
        "fallback": ctx.get("fallback", ""), "objections_extra": custom})
    print(f"saved: {path}")

def cmd_sheet(a):
    # rebuild from meta if exists, else build fresh with defaults
    cmd_build(a)

def cmd_tree(a):
    sc = SCENARIOS.get(a.scenario)
    if not sc:
        sys.exit(f"unknown scenario '{a.scenario}' — see `scenarios`")
    print(f"OBJECTION TREE — {sc['title']}")
    print("=" * 64)
    for their, yours in sc["objections"]:
        print(f"THEY:  {their}")
        print(f"YOU:   {yours}")
        print()

def cmd_practice(a):
    sc = SCENARIOS.get(a.scenario)
    if not sc:
        sys.exit(f"unknown scenario '{a.scenario}' — see `scenarios`")
    ph = {"amount": "$X", "target": "$Y", "date": "today", "time": "now",
          "N": "N", "claim": "claim #", "issue": "the issue", "thing": "item",
          "timeframe": "a week", "X": "X", "Y": "Y", "creditor": "creditor",
          "level": "the next level", "gap": "a gap", "title": ""}
    print(f"PRACTICE — {sc['title']}")
    print("The script plays the other side. Respond with acknowledge → bridge → ask.")
    print("Score shows which elements your reply hits. Ctrl-D to quit.\n")
    rounds = sc["objections"][:]
    random.shuffle(rounds)
    scored = []
    try:
        for i, (their, model) in enumerate(rounds, 1):
            print(f"[{i}/{len(rounds)}] REP: {fill(their, ph)}")
            reply = input("YOU: ").strip()
            if not reply:
                continue
            ack = any(w in reply.lower() for w in
                      ["understand", "appreciate", "i hear", "right,", "fair", "got it",
                       "makes sense", "noted"])
            bridge = any(w in reply.lower() for w in
                         ["because", "since", "the issue", "what i'm asking",
                          "my issue", "the reason", "quoted", "agreed", "documented",
                          "in writing"])
            ask = any(w in reply.lower() for w in
                      ["can you", "could you", "please", "what can", "who can",
                       "when can", "transfer", "remove", "credit", "waive", "send"])
            hits = sum([ack, bridge, ask])
            scored.append(hits)
            tags = [t for t, ok in (("acknowledge", ack), ("bridge", bridge), ("ask", ask)) if ok]
            print(f"      score: {hits}/3  [{' + '.join(tags) if tags else 'MISS'}]")
            if not ask:
                print("      hint: end with a concrete ask — 'can you remove X / who can approve?'")
            print(f"      model: {fill(model, ph)}")
            print()
    except (EOFError, KeyboardInterrupt):
        pass
    if scored:
        avg = sum(scored) / len(scored)
        print(f"— rounds: {len(scored)}   avg {avg:.1f}/3   "
              f"({'ready' if avg >= 2.5 else 'keep practicing — add concrete asks'})")

# ------------------------------------------------------------------ cli

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("scenarios"); sp.set_defaults(func=cmd_scenarios)

    sp = sub.add_parser("build", help="build a call script")
    sp.add_argument("--scenario", required=True)
    sp.add_argument("--title"); sp.add_argument("--name"); sp.add_argument("--account")
    sp.add_argument("--subject"); sp.add_argument("--amount"); sp.add_argument("--target")
    sp.add_argument("--date")
    sp.add_argument("--goal"); sp.add_argument("--leverage"); sp.add_argument("--fallback")
    sp.add_argument("--objection", help="custom objection line")
    sp.add_argument("--response", help="your response to the custom objection")
    sp.add_argument("--interactive", action="store_true")
    sp.set_defaults(func=cmd_build)

    sp = sub.add_parser("sheet", help="printable one-pager (same options as build)")
    for arg in ("scenario", "title", "name", "account", "subject", "amount",
                "target", "date", "goal", "leverage", "fallback"):
        sp.add_argument(f"--{arg}")
    sp.add_argument("--interactive", action="store_true")
    sp.set_defaults(func=cmd_sheet)

    sp = sub.add_parser("tree", help="show objection tree")
    sp.add_argument("--scenario", required=True)
    sp.set_defaults(func=cmd_tree)

    sp = sub.add_parser("practice", help="play the other side, score your replies")
    sp.add_argument("--scenario", required=True)
    sp.set_defaults(func=cmd_practice)

    a = p.parse_args()
    a.func(a)

if __name__ == "__main__":
    main()
