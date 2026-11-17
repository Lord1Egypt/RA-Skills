#!/usr/bin/env python3
"""Costume Size Chef — build costumes from what you already own.

Stdlib only, offline.

Commands:
  inventory --item X [--item Y ...]      declare what you have
  find      --occasion O --wearer W [--minutes M] [--theme T]
  build     --recipe NAME                build steps + item status
  groups    --theme T --people N         coordinated group sets
  safety    --context trick-or-treat|school|party
  list      --recipes "a,b"              consolidated BUY list
"""
import argparse
import json
import pathlib
import sys

INV_PATH = pathlib.Path(__file__).resolve().parent.parent / "costume-inventory.json"

# item name -> lowercased keywords matched against inventory strings
RECIPES = {
    "where's waldo": dict(
        occasions=["halloween", "book-character", "party"],
        wearers=["kid", "adult"], minutes=10,
        core=["red striped shirt", "beanie", "jeans"],
        subs={"red striped shirt": "any striped shirt", "beanie": "any knit hat",
              "round glasses": "paper circles on sunglasses"},
        buys=[("round glasses", "$1 store, or paper DIY")],
        groups=["puzzle", "storybook"],
    ),
    "black cat": dict(
        occasions=["halloween", "party"],
        wearers=["kid", "adult"], minutes=15,
        core=["black shirt", "black pants", "headband"],
        subs={"headband": "paper strip stapled to fit"},
        buys=[("cat ears headband", "$2-4 if no headband to glue ears onto")],
        groups=["animals"],
    ),
    "80s aerobicizer": dict(
        occasions=["party", "decade-day", "halloween"],
        wearers=["adult", "kid"], minutes=15,
        core=["tights or bright leggings", "oversized tee", "sneakers"],
        subs={"leg warmers": "knee socks with toes cut off"},
        buys=[("scrunchies", "$1")],
        groups=["80s crew"],
    ),
    "tourist": dict(
        occasions=["halloween", "party", "spirit-week"],
        wearers=["adult", "kid"], minutes=10,
        core=["hawaiian or loud shirt", "camera or phone on neck strap", "sunhat"],
        subs={"sunhat": "any brimmed hat", "camera": "cardboard camera cutout"},
        buys=[("leis", "$1")],
        groups=["vacation family"],
    ),
    "gnome": dict(
        occasions=["halloween", "book-character"],
        wearers=["kid", "adult"], minutes=20,
        core=["oversized shirt", "belt", "beard hat or cotton balls"],
        subs={"cotton balls": "paper beard strip with elastic"},
        buys=[("toy beard", "$3-6")],
        groups=["garden set"],
    ),
    "box robot": dict(
        occasions=["halloween", "spirit-week"],
        wearers=["kid", "adult"], minutes=45,
        core=["cardboard boxes", "aluminum foil", "duct tape"],
        subs={"aluminum foil": "silver spray paint or silver poster board"},
        buys=[("silver duct tape", "$4")],
        groups=["space crew"],
    ),
    "wednesday addams": dict(
        occasions=["book-character", "halloween", "party"],
        wearers=["kid", "adult"], minutes=15,
        core=["black dress or black shirt+skirt", "white shirt for collar"],
        subs={"collar": "white paper/cloth collar pinned on", "braids": "two low ponytails"},
        buys=[],
        groups=["addams family"],
    ),
    "crayon": dict(
        occasions=["halloween", "book-character", "spirit-week"],
        wearers=["kid"], minutes=20,
        core=["solid color outfit", "construction paper"],
        subs={"construction paper": "any paper + marker"},
        buys=[],
        groups=["crayon box"],
    ),
    "scarecrow": dict(
        occasions=["halloween", "book-character"],
        wearers=["kid", "adult"], minutes=25,
        core=["flannel shirt", "jeans", "rope or belt", "straw or raffia"],
        subs={"straw": "yellow paper strips or mop strands"},
        buys=[("straw hat", "$5 thrift) if none")],
        groups=["wizard of oz"],
    ),
    "static cling": dict(
        occasions=["halloween", "party"],
        wearers=["adult", "kid"], minutes=30,
        core=["laundry basket", "clothes pins", "misc clothes", "lint roller or sock"],
        subs={},
        buys=[("clothes pins", "$2")],
        groups=[],
    ),
    "smarty pants": dict(
        occasions=["halloween", "spirit-week", "party"],
        wearers=["kid", "adult"], minutes=10,
        core=["glasses", "smarties candies or paper rolls"],
        subs={"smarties": "any wrapped candy taped on"},
        buys=[("smarties rolls", "$2")],
        groups=["puns"],
    ),
    "farmer": dict(
        occasions=["halloween", "book-character", "spirit-week"],
        wearers=["kid", "adult"], minutes=10,
        core=["flannel shirt", "jeans", "boots", "hat"],
        subs={"boots": "any shoes + paper boot tops"},
        buys=[("toy tractor", "$2, optional")],
        groups=["farm set", "wizard of oz"],
    ),
    "dementor-lite": dict(
        occasions=["halloween"],
        wearers=["adult", "kid"], minutes=20,
        core=["black hoodie", "black pants", "dark fabric or trash bag cape"],
        subs={"cape": "black trash bag with cut arm holes"},
        buys=[],
        groups=["wizarding world"],
        safety=["no long fabric near stairs — hem above ankle"],
    ),
    "harry potter": dict(
        occasions=["book-character", "halloween", "party"],
        wearers=["kid", "adult"], minutes=15,
        core=["white shirt", "dark bottoms", "stick or toy wand"],
        subs={"wand": "chopstick + brown marker", "glasses": "paper circles",
              "cloak": "bathrobe or pinned fabric", "tie": "red marker on paper strip"},
        buys=[("gryffindor tie", "$6, optional")],
        groups=["wizarding world"],
    ),
    "hermione": dict(
        occasions=["book-character", "halloween", "party"],
        wearers=["kid", "adult"], minutes=15,
        core=["white shirt", "gray sweater or vest", "skirt", "book"],
        subs={"vest": "any v-neck over shirt", "tie": "paper strip"},
        buys=[],
        groups=["wizarding world"],
    ),
    "bat": dict(
        occasions=["halloween"],
        wearers=["kid", "adult"], minutes=20,
        core=["black hoodie", "black umbrella ribs or cardboard wings"],
        subs={"wings": "cardboard cut wings taped inside hoodie arms"},
        buys=[],
        groups=["animals"],
    ),
}

GROUP_THEMES = {
    "wizarding world": ["harry potter", "hermione", "dementor-lite"],
    "crayon box": ["crayon", "crayon", "crayon"],
    "farm set": ["farmer", "scarecrow", "black cat"],
    "80s crew": ["80s aerobicizer", "80s aerobicizer", "smarty pants"],
    "addams family": ["wednesday addams", "gnome" , "dementor-lite"],
    "animals": ["black cat", "bat", "cat"],
}

SAFETY = {
    "trick-or-treat": [
        "face paint over mask for under-8s (sightlines at crossings)",
        "reflective tape on ANKLES + treat bag (motion = visibility); glowstick inside translucent props",
        "cape/fabric hem above ankle bone; nothing trailing on stairs",
        "1 m from open flames (synthetics melt); LED candles at home",
        "costume sized over a winter coat OR warm base layer — cold-weather plan",
        "props soft/flexible; weapon-look props confiscated at most schools",
        "road-crossing rule: no mask/hood up while crossing",
    ],
    "school": [
        "no full-face masks (most schools) — face paint or half-masks",
        "props per teacher policy; cardboard weapons usually banned",
        "costume must survive car seat + toilet unassisted (young kids)",
        "identity readable from the FRONT in a class photo — chest sign/prop carries it",
    ],
    "party": [
        "mobility test: stand, sit, dance, hug — then adjust",
        "no driving in capes/boxes (sightlines + seatbelt geometry)",
        "shoe plan: you'll stand hours; theme shoes = portable backup",
    ],
}


def load_inv():
    if INV_PATH.exists():
        return set(json.loads(INV_PATH.read_text()))
    return set()


def save_inv(items):
    INV_PATH.write_text(json.dumps(sorted(items), indent=2, ensure_ascii=False))


def match(item, inv):
    it = item.lower()
    words = [w for w in it.split() if len(w) > 3]
    for have in inv:
        h = have.lower()
        if it in h or h in it:
            return True
        if words and all(w in h for w in words):
            return True
    return False


def recipe_status(name, inv):
    r = RECIPES[name]
    have, sub, buy = [], [], []
    for item in r["core"]:
        if match(item, inv):
            have.append(item)
        else:
            sub.append((item, r["subs"].get(item, "thrift/DM: ~$3-6")))
    for item, note in r["buys"]:
        if not match(item, inv):
            buy.append((item, note))
    score = len(have) / len(r["core"]) if r["core"] else 1.0
    return score, have, sub, buy


def cmd_inventory(args):
    inv = load_inv()
    inv.update(i.strip().lower() for i in args.items if i.strip())
    save_inv(inv)
    print(f"inventory: {len(inv)} items")
    for i in sorted(inv):
        print(f"  {i}")
    return 0


def cmd_find(args):
    inv = load_inv()
    occ = args.occasion.lower()
    wearer = args.wearer.lower()
    cands = []
    for name, r in RECIPES.items():
        if occ not in r["occasions"] or wearer not in r["wearers"]:
            continue
        if args.minutes and r["minutes"] > args.minutes:
            continue
        score, have, sub, buy = recipe_status(name, inv)
        cands.append((score, r["minutes"], name, have, sub, buy))
    cands.sort(key=lambda c: (-c[0], c[1]))
    if not cands:
        print("no recipes match those filters — loosen --minutes or occasion")
        return 1
    print(f"{occ.upper()}, {wearer}, <= {args.minutes or 'any'} min — ranked by inventory match:\n")
    for score, mins, name, have, sub, buy in cands:
        print(f"{name.upper()} ({score:.0%} match) — {mins} min")
        if have:
            print(f"   HAVE: {', '.join(have)}")
        if sub:
            print(f"   SUBSTITUTE/GET: {', '.join(i for i, _ in sub)}")
        for s in RECIPES[name].get("safety", []):
            print(f"   SAFETY: {s}")
        print()
    return 0


def cmd_build(args):
    name = args.recipe.lower().strip()
    if name not in RECIPES:
        print("unknown recipe. known: " + ", ".join(sorted(RECIPES)))
        return 1
    r = RECIPES[name]
    inv = load_inv()
    score, have, sub, buy = recipe_status(name, inv)
    print(f"BUILD: {name.upper()}  (~{r['minutes']} min, {score:.0%} inventory match)\n")
    print("1. Base layer:")
    for item in have:
        print(f"   HAVE  {item}")
    for item, hint in sub:
        print(f"   SUB   {item} -> {hint}")
    print("2. Assembly:")
    print("   " + "; ".join(f"wear {i}" for i in have[:3]))
    if sub:
        print("   add substitutes per hints above; pin/tape, no sewing needed")
    if r.get("buys"):
        print("3. BUY (only if no substitute works):")
        for item, note in r["buys"]:
            print(f"   {item} — {note}")
    for s in r.get("safety", []):
        print(f"SAFETY: {s}")
    return 0


def cmd_groups(args):
    theme = args.theme.lower()
    if theme not in GROUP_THEMES:
        print("themes: " + ", ".join(sorted(GROUP_THEMES)))
        return 1
    members = GROUP_THEMES[theme]
    n = args.people
    print(f"GROUP: {theme} for {n} people\n")
    for i in range(n):
        m = members[i % len(members)]
        print(f"  {i+1}. {m.upper()} (~{RECIPES[m]['minutes']} min, kid/adult ok)")
    print("\nrule: each costume stands alone; unify with one shared element")
    print("(same color base or prop class) for the group photo.")
    return 0


def cmd_safety(args):
    ctx = args.context.lower()
    if ctx not in SAFETY:
        print("contexts: " + ", ".join(sorted(SAFETY)))
        return 1
    print(f"SAFETY CHECK — {ctx}\n")
    for i, s in enumerate(SAFETY[ctx], 1):
        print(f"  {i}. {s}")
    return 0


def cmd_list(args):
    inv = load_inv()
    names = [n.strip().lower() for n in args.recipes.split(",") if n.strip()]
    all_buys = {}
    for name in names:
        if name not in RECIPES:
            print(f"(skip unknown: {name})")
            continue
        _, _, sub, buy = recipe_status(name, inv)
        for item, note in buy:
            all_buys[item] = note
        for item, hint in sub:
            all_buys.setdefault(item, f"sub possible: {hint}")
    if not all_buys:
        print("NOTHING TO BUY — inventory covers it.")
        return 0
    print("CONSOLIDATED LIST (one store run):")
    for item, note in all_buys.items():
        print(f"  [ ] {item} — {note}")
    print("\nwig rule: wigs are the #1 regret buy — hat/headband first.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    inv = sub.add_parser("inventory")
    inv.add_argument("--item", dest="items", action="append", default=[])
    inv.set_defaults(func=cmd_inventory)
    f = sub.add_parser("find")
    f.add_argument("--occasion", required=True)
    f.add_argument("--wearer", required=True, choices=["kid", "adult"])
    f.add_argument("--minutes", type=int)
    f.add_argument("--theme")
    f.set_defaults(func=cmd_find)
    b = sub.add_parser("build")
    b.add_argument("--recipe", required=True)
    b.set_defaults(func=cmd_build)
    g = sub.add_parser("groups")
    g.add_argument("--theme", required=True)
    g.add_argument("--people", type=int, default=3)
    g.set_defaults(func=cmd_groups)
    s = sub.add_parser("safety")
    s.add_argument("--context", required=True)
    s.set_defaults(func=cmd_safety)
    li = sub.add_parser("list")
    li.add_argument("--recipes", required=True)
    li.set_defaults(func=cmd_list)
    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
