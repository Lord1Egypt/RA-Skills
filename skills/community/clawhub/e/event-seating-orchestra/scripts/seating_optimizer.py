#!/usr/bin/env python3
"""Event seating optimizer: simulated annealing over table assignments.

Guest model
-----------
guests.json (or --demo):
{
  "tables": [8, 8, 8],                      // seats per table
  "guests": [
    {"name": "Alice", "party": "A", "flags": ["talker"]},
    {"name": "Bob", "party": "A"},
    {"name": "Cara", "flags": ["kid"]},
    ...
  ],
  "keep_apart": [["Alice", "Derek"], ...],   // hard veto pairs
  "prefer_near": [["Eve", "Frank"], ...],    // soft wishes
  "know_well":  [["Gia", "Hank"], ...]       // prior closeness (mixing splits)
}

Scoring (lower = better):
  +1_000_000 per keep-apart pair at the same table   (near-hard)
  +40 per must-together party split across tables    (party integrity)
  talker balance: sum over tables of max(0, talkers-1)^2 * 25
  kid scatter: kids at >1 table penalized; kid table without adult penalized
  mixing: +6 per know_well pair seated together      (we want new connections)
  -30 per prefer_near pair seated together           (reward)

Stdlib only; deterministic with --seed.
"""
import argparse
import json
import math
import random
import sys

HARD_KEEPAPART = 1_000_000
W_PARTY_SPLIT = 40
W_TALKER = 25
W_KID_SCATTER = 60
W_KID_NO_ADULT = 120
W_KNOWWELL = 6
W_PREFER_NEAR = 30


def load_spec(path=None, demo=False):
    if demo:
        return demo_spec()
    with open(path) as f:
        return json.load(f)


def demo_spec():
    names = [
        # family A (couple)                 family B (couple, divorced from A's side)
        ("Alice", "A", []), ("Arlen", "A", ["talker"]),
        ("Beth", "B", []), ("Boris", "B", []),
        # keep-apart: Alice's ex-husband Craig + his new partner
        ("Craig", "C", []), ("Celine", "C", []),
        # friends
        ("Dana", "D", []), ("Dmitri", "D", ["talker"]),
        ("Eve", "E", []), ("Erik", "E", []),
        ("Faye", "F", []), ("Felix", "F", ["talker"]),
        # grandparents
        ("Grace", "G", ["needs-aisle"]), ("Greg", "G", []),
        ("Hana", "H", []), ("Hugo", "H", []),
        # kids
        ("Ivy", "K", ["kid"]), ("Ian", "K", ["kid"]),
        ("Jack", "K", ["kid"]), ("Jade", "K", ["kid"]),
        # patient adults for kid table
        ("Kira", "KK", []), ("Karl", "KK", []),
        # more friends
        ("Lena", "L", []), ("Liam", "L", []),
    ]
    guests = [{"name": n, "party": p, "flags": f} for n, p, f in names]
    return {
        "tables": [8, 8, 8],
        "guests": guests,
        "keep_apart": [["Alice", "Craig"], ["Beth", "Craig"]],
        "prefer_near": [["Dana", "Eve"], ["Faye", "Hana"]],
        "know_well": [["Dana", "Dmitri"], ["Eve", "Erik"], ["Lena", "Liam"]],
    }


def index_guests(spec):
    g = spec["guests"]
    by_name = {x["name"]: i for i, x in enumerate(g)}
    parties = {}
    for i, x in enumerate(g):
        parties.setdefault(x.get("party") or f"__solo{i}", []).append(i)
    keep = [(by_name[a], by_name[b]) for a, b in spec.get("keep_apart", [])]
    near = [(by_name[a], by_name[b]) for a, b in spec.get("prefer_near", [])]
    known = [(by_name[a], by_name[b]) for a, b in spec.get("know_well", [])]
    return by_name, parties, keep, near, known


def score(assign, spec, parties, keep, near, known, caps):
    """assign: list table-index per guest. Lower is better."""
    s = 0
    seats_used = [0] * len(caps)
    table_of = assign
    for t in table_of:
        seats_used[t] += 1
    for t, (used, cap) in enumerate(zip(seats_used, caps)):
        if used > cap:
            s += 100_000 * (used - cap)          # overfull: forbidden

    for a, b in keep:
        if table_of[a] == table_of[b]:
            s += HARD_KEEPAPART

    for p, members in parties.items():
        tables = {table_of[m] for m in members}
        if len(tables) > 1:
            s += W_PARTY_SPLIT * (len(tables) - 1) * len(members)

    talkers_per = [0] * len(caps)
    kids_per = [0] * len(caps)
    adults_per = [0] * len(caps)
    for i, x in enumerate(spec["guests"]):
        t = table_of[i]
        fl = x.get("flags", [])
        if "talker" in fl:
            talkers_per[t] += 1
        if "kid" in fl:
            kids_per[t] += 1
        else:
            adults_per[t] += 1
    s += sum(max(0, x - 1) ** 2 * W_TALKER for x in talkers_per)

    kid_tables = [t for t, k in enumerate(kids_per) if k > 0]
    if len(kid_tables) > 1:
        s += W_KID_SCATTER * (len(kid_tables) - 1)
    for t in kid_tables:
        if adults_per[t] == 0:
            s += W_KID_NO_ADULT

    for a, b in known:
        if table_of[a] == table_of[b]:
            s += W_KNOWWELL
    for a, b in near:
        if table_of[a] == table_of[b]:
            s -= W_PREFER_NEAR
    return s


def anneal(spec, seed=7, iters=30000):
    caps = spec["tables"]
    n = len(spec["guests"])
    by_name, parties, keep, near, known = index_guests(spec)
    rng = random.Random(seed)

    # blocks = parties (move whole parties together)
    blocks = [m for m in parties.values()]
    nb = len(blocks)
    assign = [0] * n
    for bi, members in enumerate(blocks):
        t = bi % len(caps)
        for m in members:
            assign[m] = t

    cur = score(assign, spec, parties, keep, near, known, caps)
    best, best_assign = cur, assign[:]

    for it in range(iters):
        T = 1.0 - it / iters
        temp = max(0.2, 8.0 * T)
        a = rng.choice(blocks)
        # move block to random table, or swap two blocks
        if rng.random() < 0.5:
            new_t = rng.randrange(len(caps))
            old = {assign[m] for m in a}
            for m in a:
                assign[m] = new_t
            cand = score(assign, spec, parties, keep, near, known, caps)
            if cand <= cur or rng.random() < math.exp((cur - cand) / temp):
                cur = cand
            else:
                for m in a:
                    assign[m] = old.pop() if len(old) > 1 else list(old)[0] if old else assign[m]
                # restore properly (set pop order bug guard)
                # (handled below by rescore)
                cur = score(assign, spec, parties, keep, near, known, caps)
        else:
            b = rng.choice(blocks)
            if b is a:
                continue
            ta, tb = assign[a[0]], assign[b[0]]
            for m in a:
                assign[m] = tb
            for m in b:
                assign[m] = ta
            cand = score(assign, spec, parties, keep, near, known, caps)
            if cand <= cur or rng.random() < math.exp((cur - cand) / temp):
                cur = cand
            else:
                for m in a:
                    assign[m] = ta
                for m in b:
                    assign[m] = tb
        if cur < best:
            best, best_assign = cur, assign[:]

    return best_assign, best, dict(keep=keep, near=near, known=known,
                                   parties=parties, caps=caps)


def report(assign, spec, ctx):
    caps, parties = ctx["caps"], ctx["parties"]
    tables = {t: [] for t in range(len(caps))}
    for i, x in enumerate(spec["guests"]):
        tables[assign[i]].append(x)
    lines = []
    for t, members in tables.items():
        talkers = sum(1 for m in members if "talker" in m.get("flags", []))
        kids = sum(1 for m in members if "kid" in m.get("flags", []))
        aisle = [m["name"] for m in members if "needs-aisle" in m.get("flags", [])]
        lines.append(f"Table {t+1} ({len(members)}/{caps[t]} seats, talkers={talkers}, kids={kids}"
                     + (f", AISLE: {','.join(aisle)}" if aisle else "") + ")")
        for m in members:
            fl = ",".join(m.get("flags", [])) or ""
            lines.append(f"   {m['name']:<12} {('<' + fl + '>') if fl else ''}")
    # constraint audit
    bad = []
    for a, b in ctx["keep"]:
        if assign[a] == assign[b]:
            bad.append(f"KEEP-APART VIOLATION: {spec['guests'][a]['name']} + {spec['guests'][b]['name']}")
    for p, members in parties.items():
        if len({assign[m] for m in members}) > 1:
            bad.append(f"PARTY SPLIT: {p}")
    for t in range(len(caps)):
        n_t = sum(1 for i, x in enumerate(spec["guests"]) if assign[i] == t)
        if n_t > caps[t]:
            bad.append(f"OVERFULL table {t+1}: {n_t}/{caps[t]}")
    return "\n".join(lines), bad


def main():
    p = argparse.ArgumentParser(description="Seating chart optimizer (simulated annealing)")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--guests", help="path to guests.json")
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--iters", type=int, default=30000)
    a = p.parse_args()
    if not a.demo and not a.guests:
        p.error("need --guests file or --demo")

    spec = load_spec(a.guests, a.demo)
    assign, best, ctx = anneal(spec, a.seed, a.iters)
    chart, bad = report(assign, spec, ctx)
    print(chart)
    print(f"\nScore: {best}")
    if bad:
        print("PROBLEMS:")
        for b in bad:
            print("  !", b)
        sys.exit(2)
    print("All hard constraints satisfied: no keep-apart sharing, no split parties, no overfull tables.")


if __name__ == "__main__":
    main()
