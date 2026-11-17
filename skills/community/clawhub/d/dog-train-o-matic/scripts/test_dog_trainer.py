#!/usr/bin/env python3
"""Tests for dog_trainer.py — run: python3 scripts/test_dog_trainer.py"""
import importlib.util
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("dt", os.path.join(HERE, "dog_trainer.py"))
dt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dt)

PASS, FAIL = 0, 0


def check(name, cond, extra=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ok  {name}")
    else:
        FAIL += 1
        print(f" FAIL {name} {extra}")


# ── Breed group mapping ──────────────────────────────────────────────────────
print("breed mapping:")
gid, g = dt.find_group("siberian husky")
check("husky → sled", gid == "sled", gid)
gid, g = dt.find_group("Border Collie")
check("border collie (case) → herding", gid == "herding", gid)
gid, g = dt.find_group("beagle")
check("beagle → scent_hound", gid == "scent_hound", gid)
gid, g = dt.find_group("golden retriever")
check("golden retriever → retriever", gid == "retriever", gid)
gid, g = dt.find_group("jack russell terrier")
check("jack russell → terrier", gid == "terrier", gid)
gid, g = dt.find_group("german shepherd")
check("german shepherd → herding", gid == "herding", gid)
gid, g = dt.find_group("totally-unknown-mix")
check("unknown → falls back to bully/mixed", gid == "bully", gid)
check("every group has exercise floor >= 20", all(g["exercise"] >= 20 for g in dt.BREED_GROUPS.values()))
check("every group has >=3 outlets", all(len(g["outlets"]) >= 3 for g in dt.BREED_GROUPS.values()))

# ── Age staging ──────────────────────────────────────────────────────────────
print("age staging:")
check("3mo → puppy", dt.age_stage(3) == "puppy")
check("10mo → adolescent", dt.age_stage(10) == "adolescent")
check("24mo → adult", dt.age_stage(24) == "adult")
check("96mo → senior", dt.age_stage(96) == "senior")

# ── Protocols ────────────────────────────────────────────────────────────────
print("protocols:")
check("12+ protocols defined", len(dt.PROTOCOLS) >= 12, str(len(dt.PROTOCOLS)))
check("every protocol has >=4 steps", all(len(p["steps"]) >= 4 for p in dt.PROTOCOLS.values()))
check("every protocol has management", all(p.get("management") for p in dt.PROTOCOLS.values()))
check("key problems covered", all(k in dt.PROTOCOLS for k in
      ["leash-pulling", "jumping", "recall", "barking", "digging", "crate", "separation", "house-soiling"]))

# ── Red flags ────────────────────────────────────────────────────────────────
print("red flags:")
hits = dt.screen_red_flags(["leash-pulling"])
check("known protocol does not red-flag", hits == [])
hits = dt.screen_red_flags(["biting history with children"])
check("bite history red-flags", len(hits) == 1 and "behaviorist" in hits[0][1])
hits = dt.screen_red_flags(["aggression toward strangers"])
check("aggression red-flags", len(hits) == 1 and "behaviorist" in hits[0][1])
hits = dt.screen_red_flags(["random made-up issue"])
check("unknown problem flagged for clarification", len(hits) == 1)

# ── Plan building ────────────────────────────────────────────────────────────
print("plan building:")
plan, flagged = dt.build_plan("siberian husky", 10, ["leash-pulling", "barking"], 30)
check("plan mentions breed profile", "SLED/WORKING" in plan)
check("plan contains session structure", "Session A" in plan)
check("plan has management section", "MANAGEMENT" in plan)
check("plan includes adjust rules", "ADJUST RULES" in plan)
check("plan not flagged", flagged == [])
check("puppy note for young pup", "socialization window" in dt.build_plan("labrador", 2.5, ["puppy"], 20)[0])
check("adolescent note present", "regression" in plan)
check("red-flagged plan still returns plan", "REFER OUT" in dt.build_plan("labrador", 36, ["biting history"], 20)[0])

# minute budgeting
plan40, _ = dt.build_plan("beagle", 24, ["digging"], 40)
check("outlets fill remainder", "16 min" in plan40)

# ── CLI ──────────────────────────────────────────────────────────────────────
print("cli:")
r = subprocess.run([sys.executable, os.path.join(HERE, "dog_trainer.py"), "plan",
                    "--breed", "corgi", "--age-months", "8", "--problems", "nipping", "--minutes", "25"],
                   capture_output=True, text=True)
check("plan cmd exits 0", r.returncode == 0, r.stderr)
check("corgi → herding profile", "HERDING" in r.stdout)
check("nipping protocol engaged", "Gentle mouth" in r.stdout)

r = subprocess.run([sys.executable, os.path.join(HERE, "dog_trainer.py"), "breed", "greyhound"],
                   capture_output=True, text=True)
check("breed cmd works", r.returncode == 0 and "SIGHT HOUND" in r.stdout)

# log + today roundtrip (uses scripts/.trainlog.json)
r = subprocess.run([sys.executable, os.path.join(HERE, "dog_trainer.py"), "log",
                    "--step", "1", "--result", "success", "--note", "test"],
                   capture_output=True, text=True)
check("log cmd exits 0", r.returncode == 0, r.stderr)
r = subprocess.run([sys.executable, os.path.join(HERE, "dog_trainer.py"), "today"],
                   capture_output=True, text=True)
check("today shows logged entry", "success" in r.stdout and "test" in r.stdout)
os.remove(dt.STATE_FILE)

r = subprocess.run([sys.executable, os.path.join(HERE, "dog_trainer.py"), "demo"],
                   capture_output=True, text=True)
check("demo runs clean", r.returncode == 0 and "DEMO 4" in r.stdout)

print(f"\n{PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
