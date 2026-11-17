#!/usr/bin/env python3
"""Tests for border_buddy.py — run: python3 scripts/test_border_buddy.py"""
import importlib.util
import json
import subprocess
import sys
import tempfile
import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("bb", os.path.join(HERE, "border_buddy.py"))
bb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bb)

PASS, FAIL = 0, 0


def check(name, cond, extra=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ok  {name}")
    else:
        FAIL += 1
        print(f" FAIL {name} {extra}")


# ── Schengen math ────────────────────────────────────────────────────────────
print("schengen 90/180:")
d = bb.parse_date
# Convention: entry day counts, exit day does not.
# A 90-day stay entered 2026-01-10 therefore exits 2026-04-10 (Jan10..Apr9 = 90 days).
v1 = [{"entry": d("2026-01-10"), "exit": d("2026-04-10")}]
used, rem, det = bb.schengen_report(v1, d("2026-04-09"))
check("90-day trip: final night is the 90th day", used == 90, f"got {used}")
used, rem, det = bb.schengen_report(v1, d("2026-04-10"))
check("90-day stay on exit day uses exactly 90", used == 90, f"got {used}")
check("overstay is zero", det["overstay"] == 0)
check("remaining is 0", rem == 0)

# one day later the oldest day is still inside the window
used, _, _ = bb.schengen_report(v1, d("2026-04-11"))
check("day after exit still 90 (old days not yet dropped)", used == 90, f"got {used}")

# last presence day (Apr 9) stops counting when window start passes it:
# ref - 179 > 2026-04-09  =>  ref >= 2026-10-07
used, _, _ = bb.schengen_report(v1, d("2026-10-07"))
check("window after trip expiry returns to 0", used == 0, f"got {used}")

# overstay scenario: 90 + 19 presence days within one window
v2 = [{"entry": d("2026-01-10"), "exit": d("2026-04-10")},
      {"entry": d("2026-06-01"), "exit": d("2026-06-20")}]
used, _, det = bb.schengen_report(v2, d("2026-06-20"))
check("109/90 overstay detected", det["overstay"] == 19, f"got {det['overstay']}")

# single day visit counts entry, not exit
v3 = [{"entry": d("2026-06-01"), "exit": d("2026-06-02")}]
used, _, _ = bb.schengen_report(v3, d("2026-06-01"))
check("single-day visit = 1 presence day", used == 1, f"got {used}")

# next safe entry
v4 = [{"entry": d("2026-01-10"), "exit": d("2026-04-09")}]
safe, u = bb.next_safe_entry(v4, 20, d("2026-08-18"))
check("next safe entry found after heavy usage", safe == "2026-08-18", f"got {safe}")
# if window already full, must wait
v5 = [{"entry": d("2026-05-01"), "exit": d("2026-07-30")}]
safe5, _ = bb.next_safe_entry(v5, 20, d("2026-08-18"))
check("safe entry deferred when window full", safe5 and safe5 > "2026-08-18", f"got {safe5}")

# ── Passport rules ───────────────────────────────────────────────────────────
print("passport rules:")
msgs = bb.passport_check("six_months", d("2027-03-02"), d("2026-09-01"), d("2026-10-01"))
check("six-month rule pass (entry+6mo exactly)", msgs[0][0] is True)
msgs = bb.passport_check("six_months", d("2026-10-01"), d("2026-09-01"), d("2026-10-01"))
check("six-month rule fail (3 months left)", msgs[0][0] is False)
msgs = bb.passport_check("schengen_3mo", d("2026-12-10"), d("2026-09-01"), d("2026-09-10"))
check("schengen 3mo beyond departure pass", msgs[0][0] is True)
msgs = bb.passport_check("schengen_3mo", d("2026-09-30"), d("2026-09-01"), d("2026-09-10"))
check("schengen 3mo fail (1 month buffer)", msgs[0][0] is False)
msgs = bb.passport_check("valid_for_stay", d("2026-09-20"), d("2026-09-01"), d("2026-09-10"))
check("valid-for-stay pass", msgs[0][0] is True)

# ── Yellow fever ─────────────────────────────────────────────────────────────
print("yellow fever:")
check("endemic origin triggers requirement",
      "REQUIRED" in bb.yellow_fever_check("if_from_endemic", "NG"))
check("clean origin no requirement",
      "REQUIRED" not in bb.yellow_fever_check("if_from_endemic", "DE"))
check("domestic risk wording",
      "recommended" in bb.yellow_fever_check("domestic_risk", None))

# ── CLI end-to-end ───────────────────────────────────────────────────────────
print("cli:")
r = subprocess.run([sys.executable, os.path.join(HERE, "border_buddy.py"), "check",
                    "--nationality", "BR", "--destination", "PT", "--transit", "DE",
                    "--stay-days", "42", "--passport-expiry", "2027-03-01",
                    "--entry-date", "2026-09-01"], capture_output=True, text=True)
check("check exits 0", r.returncode == 0, r.stderr)
check("check mentions Schengen pool", "90/180" in r.stdout)
check("check flags nothing fatal for BR->PT", "FAIL" not in r.stdout)

visits = [{"entry": "2026-01-10", "exit": "2026-04-09", "country": "PT"}]
tf = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
json.dump(visits, tf)
tf.close()
r = subprocess.run([sys.executable, os.path.join(HERE, "border_buddy.py"), "schengen",
                    "--visits", tf.name, "--on", "2026-06-20", "--plan-days", "20"],
                   capture_output=True, text=True)
os.unlink(tf.name)
check("schengen cmd exits 0", r.returncode == 0, r.stderr)
check("schengen cmd reports remaining days", "remaining" in r.stdout)
check("schengen cmd gives safe entry", "safe entry" in r.stdout)

r = subprocess.run([sys.executable, os.path.join(HERE, "border_buddy.py"), "rules",
                    "--destination", "JP"], capture_output=True, text=True)
check("rules cmd dumps JSON", r.returncode == 0 and '"Japan"' in r.stdout)

r = subprocess.run([sys.executable, os.path.join(HERE, "border_buddy.py"), "demo"],
                   capture_output=True, text=True)
check("demo runs clean", r.returncode == 0 and "DEMO 4" in r.stdout)

print(f"\n{PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
