#!/usr/bin/env python3
"""
fence_deal.py — boundary fence cost splits, damage routing, notice letters, de-escalation.

Subcommands:
  cost      fair split: baseline shared, premium delta to the wanter
  damage    who-pays router by cause x boundary status
  notice    statutory-style cost-sharing notice letter (ready to send)
  ladder    5-rung dispute de-escalation for a specific issue

Stdlib only. Not legal advice; state doctrines vary — SKILL.md has the map.
"""
import argparse
import sys
from datetime import date, timedelta

DOCTRINES = {
    # sharing statutes / partition fence family (notice usually required first)
    "share": ["CA", "OR", "WA", "NV", "AZ", "ID", "MT", "NM", "ND", "SD", "NE", "KS",
              "OK", "MN", "IA", "MO", "AR", "LA", "WI", "MI", "IN", "KY", "TN", "NC",
              "VA", "WV", "PA", "NY", "ME", "NH", "VT", "MA", "CT", "RI", "MD", "DE", "NJ"],
    # agreement-only common interpretation for residential fences
    "agreement": ["TX", "FL", "GA", "AL", "MS", "SC", "UT", "CO", "WY", "AK", "HI", "IL", "OH"],
}
# NOTE: classifications are practical guidance bands, not legal citation;
# rural "line fence / fence viewer" statutes (WI MI OH IA etc.) can assign
# shares by township officials. Always check the current state statute.

DAMAGE_ROUTER = [
    ("neighbor tree fell", "boundary", "Tree owner pays (negligence if visibly dead — photograph before clearing)"),
    ("neighbor tree fell", "own", "Tree owner pays: their tree, your fence"),
    ("my tree fell", "any", "You pay; offer before being asked"),
    ("storm", "boundary", "Shared repair in sharing states; otherwise fence owner (check policy for acts of god)"),
    ("storm", "own", "Your fence, your repair; homeowner's policy if large loss (deductible math first)"),
    ("rot", "boundary", "Owners share (it served both); split baseline cost"),
    ("rot", "own", "Fence owner replaces; good moment to propose a boundary agreement if replacing on the line"),
    ("contractor", "any", "Contractor's liability — capture company name + insurance same day"),
    ("kids guests", "any", "You pay if your people did it; offer cash not argument"),
]

LADDER = [
    ("Rung 1 — Coffee, not counsel",
     "In person, neutral time (not the moment you're angry). One sentence of problem, one of proposal:\n"
     "     'The fence on our line is failing — I got two quotes, want to split it fairly?'\n"
     "     Bring the printed quotes. Most fence disputes actually end here."),
    ("Rung 2 — The letter",
     "Short friendly written summary of what was agreed/proposed + deadline (14-21 days).\n"
     "     Certified mail + email. This creates the record WITHOUT hostility."),
    ("Rung 3 — Facts hired, not lawyers",
     "Boundary question -> licensed surveyor ($500-1500) settles feet-and-inches.\n"
     "     Cost question -> 3rd quote. Most 'legal' fence fights are actually survey fights."),
    ("Rung 4 — Mediation",
     "Community dispute resolution / county mediation services (often free or <$100).\n"
     "     Mediated fence agreements can be recorded and bind future owners."),
    ("Rung 5 — Attorney demand letter",
     "Only after 1-4 documented. A demand letter citing the state fence statute runs\n"
     "     $250-500 and lands very differently than a neighbor's note. Litigation is\n"
     "     the failure mode: it costs more than any residential fence."),
]


def cmd_cost(args):
    n = args.length
    base = n * args.price_base
    up = n * args.price_upgrade if args.price_upgrade else None
    print(f"\n  FENCE COST — {n:.0f} ft")
    print(f"  Baseline installed: ${base:.0f}  (${args.price_base}/ft)")
    if up is not None:
        print(f"  Premium option:     ${up:.0f}  (${args.price_upgrade}/ft)")
        print(f"  Upgrade delta:      ${up-base:.0f}  <- belongs to whoever WANTS premium")
    print()
    my_share = base * args.share
    their_share = base - my_share
    print(f"  Fair split (share={args.share:.0%} you):")
    print(f"    you:   ${my_share:>8,.0f}  (baseline portion)")
    print(f"    them:  ${their_share:>8,.0f}  (baseline portion)")
    if up is not None:
        print(f"    + premium delta ${up-base:,.0f} to the wanter")
        print(f"\n  If YOU want premium: your total ${my_share + (up-base):,.0f}, their ${their_share:,.0f}")
        print(f"  If THEY want premium: your total ${my_share:,.0f}, their ${their_share + (up-base):,.0f}")
    print("\n  Sharing states: this split is the statutory norm AFTER written notice.")
    print("  Agreement states: this is the fair-opening proposal that most neighbors accept.")
    print("  One signed page beats any handshake — see SKILL.md pitfalls #5.")
    return 0


def cmd_damage(args):
    cause = args.cause.lower()
    bkey = "boundary" if args.boundary == "yes" else "own"
    for c, b, verdict in DAMAGE_ROUTER:
        if c.split()[0] in cause and (b == bkey or b == "any"):
            print(f"\n  DAMAGE ROUTER — cause: {args.cause} | boundary fence: {args.boundary}")
            print(f"\n  -> {verdict}")
            break
    else:
        print(f"\n  DAMAGE ROUTER — no exact match for '{args.cause}'.")
        print("  Known causes: neighbor tree fell / my tree fell / storm / rot / contractor / kids guests")
        return 1
    print("\n  Same-day actions: photograph from both sides BEFORE any cleanup,")
    print("  note weather date, save contractor/company names if any equipment involved.")
    return 0


def cmd_notice(args):
    today = date.today()
    deadline = today + timedelta(days=args.deadline)
    you = args.you or "[your name, address, phone, email]"
    them = args.neighbor
    total = args.cost
    their = total * (1 - args.share)
    letter = f"""Date: {today.strftime('%B %d, %Y')}

From: {you}
To: {them}

Re: Notice regarding repair/replacement of the boundary fence between our properties

Dear Neighbor,

The fence along our shared boundary ({args.length:.0f} ft) needs {args.work}. I have obtained
written quotes; the reasonable baseline cost is ${total:,.0f}.

Under the equitable cost-sharing principles that apply to boundary fences in our state,
I am proposing we split this cost: my share ${total - their:,.0f}, your share ${their:,.0f}.
(If you obtain a lower comparable quote, I'm glad to consider it.)

I propose work to begin after {deadline.strftime('%B %d, %Y')}, and I'm happy to meet and
discuss any aspect — materials, timing, contractor choice — before then. Please respond by
that date so we can proceed as neighbors should.

Sincerely,
{you.split(',')[0] if args.you else '[your name]'}

---
Send: certified mail + email. Keep the certified receipt. This letter is the
statutory-style notice required before cost-sharing obligations arise in
good-neighbor-fence states (e.g., California Civil Code 841).
"""
    print(letter)
    return 0


def cmd_ladder(args):
    print(f"\n  DE-ESCALATION LADDER — issue: {args.issue}\n  " + "=" * 56)
    for title, body in LADDER:
        print(f"\n  {title}\n{body}")
    print("\n  STOP conditions: any threat, any property damage in progress, any survey")
    print("  tampering -> document and go straight to rung 5 / police non-emergency line.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Boundary fence economics + de-escalation")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("cost")
    p.add_argument("--length", type=float, required=True)
    p.add_argument("--price-base", type=float, required=True)
    p.add_argument("--price-upgrade", type=float)
    p.add_argument("--share", type=float, default=0.5)
    p.set_defaults(fn=cmd_cost)
    p = sub.add_parser("damage")
    p.add_argument("--cause", required=True)
    p.add_argument("--boundary", required=True, choices=["yes", "no"])
    p.set_defaults(fn=cmd_damage)
    p = sub.add_parser("notice")
    p.add_argument("--length", type=float, required=True)
    p.add_argument("--cost", type=float, required=True)
    p.add_argument("--share", type=float, default=0.5)
    p.add_argument("--neighbor", required=True)
    p.add_argument("--you", help="your name/address block")
    p.add_argument("--work", default="replacement")
    p.add_argument("--deadline", type=int, default=21)
    p.set_defaults(fn=cmd_notice)
    p = sub.add_parser("ladder")
    p.add_argument("--issue", required=True)
    p.set_defaults(fn=cmd_ladder)
    args = ap.parse_args()
    if not args.cmd:
        ap.print_help(); sys.exit(1)
    sys.exit(args.fn(args) or 0)


if __name__ == "__main__":
    main()
