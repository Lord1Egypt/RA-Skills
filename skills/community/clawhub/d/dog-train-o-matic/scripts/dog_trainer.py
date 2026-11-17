#!/usr/bin/env python3
"""
dog-train-o-matic — personalized, breed-and-age-aware dog training plans.

Subcommands: plan | breed | log | today | demo

Positive reinforcement / force-free only. Flags red-flag presentations
(aggression, severe anxiety) for professional referral instead of planning.
"""
import argparse
import json
import os
import sys

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".trainlog.json")

# ── Breed group drive profiles ──────────────────────────────────────────────
# name, exercise floor (min/day), intensity note, outlets, predispositions
BREED_GROUPS = {
    "herding": {
        "label": "HERDING",
        "exercise": 75,
        "note": "mental work tires them more than distance; needs a 'job'",
        "outlets": ["treibball / pushing balls", "directional fetch (left/right/away)",
                    "grouping games with family", "advanced obedience chains", "heelwork to music"],
        "predispositions": ["nipping heels of running children", "chasing cars/bikes/joggers",
                            "shadow-chasing (light fixation) if under-stimulated", "herding other pets"],
        "members": ["border collie", "aussie", "australian shepherd", "kelpie", "corgi",
                    " Pembroke welsh corgi", "cardigan", "heeler", "australian cattle dog",
                    "sheltie", "shetland sheepdog", "german shepherd", "belgian malinois",
                    "collie", "rough collie", "smooth collie", "tervuren"],
    },
    "scent_hound": {
        "label": "SCENT HOUND",
        "exercise": 60,
        "note": "the nose is the dog; sniffing is fulfilling exercise, not a bonus",
        "outlets": ["nose-work / scent games (hidden treats)", "snuffle mats",
                    "'find it' scatter feeding", "tracking long lines", "food puzzles"],
        "predispositions": ["pulling nose-to-ground on walks", "deaf to recall mid-trail",
                            "baying/howling when bored", "digging"],
        "members": ["beagle", "basset hound", "bloodhound", "coonhound", "dachshund",
                    "harrier", "otterhound", "plott"],
    },
    "sighthound": {
        "label": "SIGHT HOUND",
        "exercise": 45,
        "note": "sprinters, not marathoners; 2 short hard chases beat an hour of walking",
        "outlets": ["flirt pole", "lure coursing", "fetch sprints", "racing games with a cue"],
        "predispositions": ["chasing small running animals (cats!)", "counter-surfing",
                            "couch-potato indoors; zoomies when rested"],
        "members": ["greyhound", "whippet", "saluki", "borzoi", "afghan hound",
                    "italian greyhound", "lurcher"],
    },
    "retriever": {
        "label": "RETRIEVER",
        "exercise": 60,
        "note": "mouth-oriented and people-oriented; carrying things is joy",
        "outlets": ["structured fetch with obedience cues", "water retrieval/swimming",
                    "carrying games (fetch the leash/slipper)", "dock diving"],
        "predispositions": ["mouthing/nipping when excited", "jumping on guests",
                            "counter-surfing", "selective recall mid-fetch"],
        "members": ["labrador", "labrador retriever", "golden retriever", "chesapeake",
                    "chesapeake bay retriever", "flat-coated retriever", "nova scotia duck tolling retriever"],
    },
    "sled": {
        "label": "SLED/WORKING",
        "exercise": 90,
        "note": "engineered for endurance; under-exercised = howling and demolition",
        "outlets": ["bikejoring / canicross", "flirt pole", "hiking with a weighted dog pack (adults)",
                    "backyard digging pit (sanctioned)", "skijoring"],
        "predispositions": ["howling", "escape artistry (digging, climbing)", "pulling on leash",
                            "prey drive toward small animals"],
        "members": ["siberian husky", "husky", "alaskan malamute", "samoyed",
                    "alaskan husky", "greenland dog"],
    },
    "guardian": {
        "label": "GUARDIAN/PROTECTIVE",
        "exercise": 60,
        "note": "watchful and territorial; socialization matters more than for other groups",
        "outlets": ["patrol-style walks (structured sniff circuits)", "weight pull (adults, conditioned)",
                    "advanced obedience as 'work'", "carrier/service roles"],
        "predispositions": ["barking at strangers/noise", "wariness of new people",
                            "leash reactivity toward other dogs", "territorial guarding of home/car"],
        "members": ["rottweiler", "doberman", "german shepherd dog", "boxer", "bullmastiff",
                    "great dane", "cane corso", "kangal", "anatolian shepherd", "tibetan mastiff"],
    },
    "terrier": {
        "label": "TERRIER",
        "exercise": 60,
        "note": "bred to kill vermin; high prey drive and tenacity are features",
        "outlets": ["digging pit (sanctioned digging spot)", "flirt pole", "earthdog-style games",
                    "shake-toy time", "puzzle feeders"],
        "predispositions": ["digging", "barking", "small-animal chase", "tenacious grip on toys/pant legs"],
        "members": ["jack russell", "jack russell terrier", "parson russell", "rat terrier",
                    "fox terrier", "westie", "west highland white terrier", "scottish terrier",
                    "cairn terrier", "yorkie", "yorkshire terrier", "airedale", "pit bull terrier-type"],
    },
    "companion": {
        "label": "COMPANION",
        "exercise": 30,
        "note": "bred to sit on laps; still needs enrichment but lower floor",
        "outlets": ["trick training", "sniffy walks", "puzzle toys", "agility-for-fun (low bars)"],
        "predispositions": ["separation distress when alone", "barking for attention",
                            "house-soiling regressions", "guarding laps/beds"],
        "members": ["pug", "french bulldog", "bichon frise", "maltese", "shih tzu",
                    "cavalier king charles spaniel", "pekingese", "chihuahua", "havanese"],
    },
    "bully": {
        "label": "BULLY/MIXED",
        "exercise": 50,
        "note": "athletic, people-social; find the individual's drives by observation",
        "outlets": ["flirt pole", "spring pole (adults)", "tug with rules", "hiking"],
        "predispositions": ["pulling", "jumping", "dog-selectivity in adolescence"],
        "members": ["staffordshire bull terrier", "american bully", "boston terrier",
                    "bulldog", "english bulldog", "pit mix", "mixed breed", "mix", "mutt", "rescue mix"],
    },
    "gundog": {
        "label": "GUNDOG/POINTING",
        "exercise": 60,
        "note": "stamina + soft mouth + biddable; thrives on structure",
        "outlets": ["field-style marked retrieves", "hunt-water-retrieve games", "steady-to-wing drills (fun version)"],
        "predispositions": ["pulling", "mouthiness", "bird/small-animal interest"],
        "members": ["pointer", "german shorthaired pointer", "english setter", "irish setter",
                    "vizsla", "weimaraner", "brittany", "spaniel", "english springer spaniel",
                    "cocker spaniel"],
    },
}

# ── Behavior protocols (force-free, criterion-laddered) ─────────────────────
PROTOCOLS = {
    "leash-pulling": {
        "name": "Loose-leash walking",
        "steps": [
            "Silence check: at the door, wait for all-four-paws calm before the leash goes on. Open door only on calm.",
            "Inside walk: 2 min of walking indoors, reward every 3 steps at your left seam.",
            "Garden/driveway laps: reward at your seam every 5 steps; if leash goes tight, stop and be a tree.",
            "Quiet street: same rules; one about-turn per block when the dog surges.",
            "Real walk: reward every 10-15 steps; a tight leash = stop + call to seam + restart.",
            "Maintenance: random rewards; front-clip harness fades once 90% loose.",
        ],
        "management": "front-clip harness; hands-free waist leash; higher-value treats than the sidewalk",
        "weeks": 4,
    },
    "jumping": {
        "name": "Four-on-the-floor greetings",
        "steps": [
            "Install the alternative: heavily reward a sit at a distance from the door.",
            "Fake arrivals: ring your own bell, enter, reward sit; leave if paws leave the floor.",
            "Real guest #1 (dog-savvy): guest approaches only while sit holds; resets when it breaks.",
            "Real guests: tether or baby-gate; dog earns approach by holding the sit.",
            "Public greetings: 'say hi' cue means approach allowed while sitting; no sit, no greet.",
        ],
        "management": "gate between dog and door; guests ignore dog until calm; no pushing/off yelling (attention feeds it)",
        "weeks": 3,
    },
    "recall": {
        "name": "Rocket recall",
        "steps": [
            "Name game: say name, mark, feed — 20 reps/day for 3 days, everywhere.",
            "Recall on long line (5m): whistle/cue, reel gently if needed, jackpot reward.",
            "Long line 10m with distractions (food on ground first, then a calm dog at distance).",
            "Free play with 8-of-10 recalls ending in release back to play (never punish after coming).",
            "Proofing: woods, dog park edges, squirrels at distance; jackpot those.",
        ],
        "management": "long line until 95% reliable; never call for baths/nails/leaving the park — go get the dog instead",
        "weeks": 6,
    },
    "barking": {
        "name": "Bark budget & trigger work",
        "steps": [
            "Log 3 days of barking: trigger, time, what happened after (barking works?).",
            "Remove the payoff: window film for passers-by, deliver nothing when demand-barking.",
            "Thank-you protocol: cue 'enough' + treat at 1s silence; extend silence gradually.",
            "Alternative: send to mat on the trigger at distance; reward heavily there.",
            "Close the distance gradually over weeks; bark budget shrinks naturally.",
        ],
        "management": "block window sightlines; white noise; do not shout (dog reads it as joining in)",
        "weeks": 4,
    },
    "digging": {
        "name": "Sanctioned digging",
        "steps": [
            "Build a digging pit (sandbox + loose soil); bury 3 treasures half-visible.",
            "Dig WITH the dog at the pit once; celebrate unearthed treasure.",
            "Interrupt garden digging calmly, redirect to pit, reward there.",
            "Supervise yard time 2 weeks; every garden dig redirects to pit.",
            "Fade supervision once 80% of digs choose the pit.",
        ],
        "management": "pit in a shady spot; some breeds need this forever — it is the outlet, not a failure",
        "weeks": 3,
    },
    "nipping": {
        "name": "Gentle mouth",
        "steps": [
            "Toy-as-answer: every excited mouth contact → toy inserted, praise for biting IT.",
            "Kids become feeding robots: all child-dog interactions = treat delivery for calm, no running-chase games.",
            "Withdrawal consequence: mouth on skin = play stops 20s (no yelling; leaving is the message).",
            "Rehearse greetings calmly on-leash; reward four-on-floor.",
            "Proof with real excitement levels; drop back a step if skin contact returns.",
        ],
        "management": "no unsupervised child play for 3 weeks; chase games banned until bite inhibition is reliable",
        "weeks": 3,
    },
    "chewing": {
        "name": "Right thing in the mouth",
        "steps": [
            "Inventory chewed items; replace access with edible chews + frozen KONGs daily.",
            "Trade game: swap stolen item for a high-value treat, return the item sometimes.",
            "'Drop' cue trained with paired treats (drop item, get treat, get item back).",
            "Supervise; interrupt wrong chewing, redirect, reward right object.",
            "Freedom expands room-by-room as choices improve.",
        ],
        "management": "puppy-proof; bitter spray on furniture edges; chews BEFORE boredom, on a schedule",
        "weeks": 3,
    },
    "counter-surfing": {
        "name": "Counters are boring",
        "steps": [
            "Make counters never pay: food never left out, trash secured (management does 80% here).",
            "Floor feeding station: the magic food spot is a mat away from the counter.",
            "Mat cue with duration; reward calm mat-time during cooking.",
            "Booby-trap-free proofing: staged temptations the dog can never reach anyway.",
            "Maintenance: counters stay clean forever; mat stays during cooking.",
        ],
        "management": "ABSOLUTE: one successful counter steal = weeks of training setback",
        "weeks": 2,
    },
    "crate": {
        "name": "Crate as bedroom",
        "steps": [
            "Door open, best chews inside only; dog chooses to enter.",
            "Eat meals just inside the door; move the bowl deeper over days.",
            "Close the door 1s while licking a stuffed KONG; open before fussing.",
            "Duration with you in the room; then out of sight 10s, 30s, minutes.",
            "Overnight and departures: frozen KONG every time; crate predicts good things.",
        ],
        "management": "never use the crate for punishment; no forcing; listen to genuine distress",
        "weeks": 3,
    },
    "separation": {
        "name": "Alone-time confidence (mild cases)",
        "steps": [
            "Baseline film 20 min alone; note the latency to first stress sign.",
            "Departure cues de-linked: pick up keys, sit back down 10x/day.",
            "Micro-departures below stress latency: out the door 2s, return before worry.",
            "Grow duration 10-20% per success; frozen KONG at each departure.",
            "Return is boring: ignore first 2 min home so arrivals deflate.",
        ],
        "management": "leave something to do; exercise BEFORE alone-time; film sessions weekly (data beats anecdotes)",
        "weeks": 6,
    },
    "leash-reactivity": {
        "name": "Distance before drama (reactivity)",
        "steps": [
            "Find the threshold distance: the farthest the dog notices a dog and can still eat.",
            "Look-at-that (LAT): dog glances at trigger, mark, feed; trigger predicts chicken.",
            "Hold distance while latency to look-back-at-you drops over a week.",
            "Shrink distance 10% per week; retreat instantly if the dog stiffens.",
            "Pattern games (1-2-3 walking) through moderate passes.",
        ],
        "management": "never correct the lunging (it adds stress); use space proactively; amber-colored dogs need more warm-up",
        "weeks": 8,
    },
    "house-soiling": {
        "name": "Potty protocol",
        "steps": [
            "Vet check first (rule out UTI); then log every accident with time and context.",
            "Schedule: out after sleep/eat/play, every 30-60 min for pups; huge rewards outdoors.",
            "Interrupt (no scare) + redirect outside; clean enzymatically (ammonia products fail).",
            "Freedom expands as log shows 2 clean weeks; bell-training optional add-on.",
            "Marking (intact males) may need neutering conversation with the vet.",
        ],
        "management": "enzyme cleaner; supervision or confinement — no unsupervised access to accident zones",
        "weeks": 4,
    },
    "puppy": {
        "name": "Puppy foundations + socialization",
        "steps": [
            "Name game + hand targeting (week 1; 5 min x2 daily).",
            "Socialization checklist: 5 new exposures/week (surfaces, sounds, handling, kind strangers, calm dogs) — window closes ~14 weeks.",
            "Crate foundations (see crate protocol) + potty protocol from day one.",
            "Bite-inhibition games: toys-as-answer, withdrawal on tooth contact.",
            "Loose-leash foundations indoors; recall name game everywhere.",
        ],
        "management": "carry in public until fully vaccinated; socialize with safe dogs; do NOT wait for shots to socialize (use safe protocols)",
        "weeks": 8,
    },
}

RED_FLAGS = {
    "bite": "history of breaking skin on a human — work with a certified behaviorist, not a plan",
    "biting history": "history of biting a human — work with a certified behaviorist, not a plan",
    "aggression": "human-directed aggression — refer to CAAB/ACVB veterinary behaviorist",
    "severe separation": "self-injury, escape injuries, hours of distress — CSAT or veterinary behaviorist (medication may be indicated)",
    "fear": "deep fear presentations (shutdown, trembling beyond mild startle) — certified behaviorist",
}

AGES = {
    "puppy": (0, 18),        # in months, socialization sub-window < 14 wks
    "adolescent": (6, 18),
    "adult": (18, 84),
    "senior": (84, 300),
}


def find_group(breed):
    b = breed.lower().strip()
    for gid, g in BREED_GROUPS.items():
        for m in g["members"]:
            if m == b or (m in b and len(m) > 4):
                return gid, g
    return "bully", BREED_GROUPS["bully"]


def age_stage(months):
    if months < 6:
        return "puppy"
    if months < 18:
        return "adolescent"
    if months < 84:
        return "adult"
    return "senior"


def screen_red_flags(problems):
    hits = []
    for p in problems:
        if p in PROTOCOLS:
            continue
        low = p.lower()
        for key, msg in RED_FLAGS.items():
            if key in low:
                hits.append((p, msg))
                break
        else:
            # free-text problem not matching any protocol or red flag
            hits.append((p, "unrecognized problem — ask for details; if fear or aggression is involved, refer to a certified behaviorist"))
    return hits


def build_plan(breed, age_months, problems, minutes):
    gid, group = find_group(breed)
    stage = age_stage(age_months)
    flagged = screen_red_flags(problems)
    prots = []
    for p in problems:
        if p in PROTOCOLS:
            prots.append((p, PROTOCOLS[p]))
    # split minutes: 60% protocols, 40% outlets
    prot_min = max(10, int(minutes * 0.6))
    out_min = minutes - prot_min
    lines = []
    add = lines.append
    dog = f"{breed} ({stage}, {age_months:g} months)"
    add(f"TRAINING PLAN — {dog}")
    add(f"Problems: {', '.join(problems)}   |   Budget: {minutes} min/day")
    add("")
    if flagged:
        add("!! RED-FLAG SCREEN: REFER OUT !!")
        for p, msg in flagged:
            add(f"   {p}: {msg}")
        add("")
    add(f"RED-FLAG SCREEN: {'FLAGGED — see above; plan below covers the safe parts only' if flagged else 'CLEAR'}")
    add("")
    add(f"BREED PROFILE: {group['label']}")
    add(f"  Exercise floor: {group['exercise']}+ min/day — {group['note']}")
    add(f"  Instinct outlets: {'; '.join(group['outlets'][:4])}")
    add(f"  Predispositions (expect these, manage them): {'; '.join(group['predispositions'][:3])}")
    add("")
    if stage == "puppy" and age_months <= 3.5:
        add("PUPPY NOTE: socialization window closes ~14 weeks — exposures OUTRANK drills now.")
        add("")
    if stage == "adolescent":
        add("ADOLESCENT NOTE: regression is developmental and temporary; hold criteria, don't punish.")
        add("")
    add(f"WEEK 1 — two {max(5, prot_min // 2)}-min protocol sessions + outlets to fill {minutes} min")
    day = 1
    for pname, prot in prots:
        add(f"  Session A (day {day}): {prot['name']} — step 1")
        add(f"      · {prot['steps'][0]}")
        add(f"      Advance when: {advance_rule()}")
        day = 2 if day == 1 else 3
    add(f"  Outlets ({out_min} min): choose from profile above; flirt pole and sniff work are highest-yield.")
    add("")
    add("MANAGEMENT (start today — not training, environment):")
    for pname, prot in prots:
        add(f"  · {pname}: {prot['management']}")
    if not prots:
        add("  (no specific protocols requested — foundations: name game, hand target, mat)")
    add("")
    add("ADJUST RULES: 2 green sessions → next step; 3 failed sessions → drop back one step, double reps.")
    return "\n".join(lines), flagged


def advance_rule():
    return "criterion met in 2 consecutive sessions"


def cmd_plan(args):
    problems = [p.strip() for p in args.problems.split(",") if p.strip()]
    plan, flagged = build_plan(args.breed, args.age_months, problems, args.minutes)
    print(plan)
    return 0


def cmd_breed(args):
    gid, group = find_group(args.breed)
    print(f"BREED PROFILE — {args.breed} → {group['label']}")
    print("=" * 60)
    print(f"Exercise floor: {group['exercise']}+ min/day")
    print(f"Philosophy: {group['note']}")
    print("Outlets:")
    for o in group["outlets"]:
        print(f"  · {o}")
    print("Predispositions (features, not bugs):")
    for p in group["predispositions"]:
        print(f"  · {p}")
    print(f"Similar breeds: {', '.join(group['members'][:8])}")
    return 0


def cmd_log(args):
    entry = {"step": args.step, "result": args.result, "note": args.note or "", "ts": args.when or "now"}
    data = []
    if os.path.exists(STATE_FILE):
        try:
            data = json.loads(open(STATE_FILE).read())
        except Exception:
            data = []
    data.append(entry)
    open(STATE_FILE, "w").write(json.dumps(data, indent=1))
    # simple plateau hint
    recent = [e["result"] for e in data[-6:]]
    if recent.count("fail") >= 3:
        print("Logged. ⚠ 3+ fails in the last 6 sessions — drop back one step and double reps (use --adjust next plan).")
    elif recent[-5:] and len(set(recent[-5:])) == 1 and recent[-1] == "success":
        print("Logged. 5 straight successes — advance to the next step.")
    else:
        print(f"Logged session: step {args.step} = {args.result}.")
    return 0


def cmd_today(args):
    if not os.path.exists(STATE_FILE):
        print("No sessions logged yet. Run a plan, do session A, then `log`.")
        return 0
    data = json.loads(open(STATE_FILE).read())
    print(f"SESSION LOG ({len(data)} entries)")
    for e in data[-8:]:
        print(f"  {e['ts']:<6} step {e['step']}: {e['result']}" + (f" — {e['note']}" if e['note'] else ""))
    return 0


def cmd_demo(args):
    print("=== DEMO 1: adolescent husky — pulling + barking ===")
    cmd_plan(argparse.Namespace(breed="siberian husky", age_months=10,
                                problems="leash-pulling,barking", minutes=30))
    print()
    print("=== DEMO 2: corgi puppy nipping ===")
    cmd_plan(argparse.Namespace(breed="corgi", age_months=3,
                                problems="nipping,puppy", minutes=25))
    print()
    print("=== DEMO 3: breed insight ===")
    cmd_breed(argparse.Namespace(breed="border collie"))
    print()
    print("=== DEMO 4: red-flag screen ===")
    cmd_plan(argparse.Namespace(breed="labrador", age_months=36,
                                problems="recall,biting history with children", minutes=20))


def main():
    p = argparse.ArgumentParser(description="dog-train-o-matic: personalized force-free dog training plans")
    sub = p.add_subparsers(dest="cmd")
    pl = sub.add_parser("plan", help="build a training week")
    pl.add_argument("--breed", required=True)
    pl.add_argument("--age-months", type=float, required=True)
    pl.add_argument("--problems", required=True, help="comma list: leash-pulling,barking,recall,...")
    pl.add_argument("--minutes", type=int, default=30, help="owner minutes/day")
    b = sub.add_parser("breed", help="breed drive profile")
    b.add_argument("breed")
    lg = sub.add_parser("log", help="log a session result")
    lg.add_argument("--step", type=int, required=True)
    lg.add_argument("--result", required=True, choices=["success", "partial", "fail"])
    lg.add_argument("--note")
    lg.add_argument("--when", help="date tag, e.g. 2026-08-18")
    t = sub.add_parser("today", help="show recent session log")
    sub.add_parser("demo", help="run sample scenarios")
    args = p.parse_args()
    if args.cmd == "plan":
        return cmd_plan(args)
    if args.cmd == "breed":
        return cmd_breed(args)
    if args.cmd == "log":
        return cmd_log(args)
    if args.cmd == "today":
        return cmd_today(args)
    if args.cmd == "demo":
        return cmd_demo(args)
    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
