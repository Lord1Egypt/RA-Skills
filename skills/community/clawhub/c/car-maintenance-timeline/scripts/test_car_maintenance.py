#!/usr/bin/env python3
"""Self-tests for car_maintenance.py — stdlib only, deterministic.

Run:  python3 scripts/test_car_maintenance.py
"""
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

SCRIPT = Path(__file__).parent / "car_maintenance.py"

spec = __import__("importlib.util").util.spec_from_file_location(
    "car_maintenance", SCRIPT)
cm = __import__("importlib.util").util.module_from_spec(spec)
spec.loader.exec_module(cm)

PASS = 0
FAIL = 0


def check(name, cond):
    global PASS, FAIL
    tag = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    print(f"[{tag}] {name}")


def run(args, expect_rc=0):
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)] + args,
        capture_output=True, text=True,
    )
    assert proc.returncode == expect_rc, (
        f"rc={proc.returncode} expected {expect_rc}\n{proc.stderr}"
    )
    return proc


def status(km, in_service, **kw):
    """Thin wrapper around build_status with sensible test defaults."""
    today = kw.pop("today", date(2026, 8, 27))
    severe = kw.pop("severe", False)
    annual = kw.pop("annual_km", 15000)
    history = kw.pop("history", [])
    done = cm.resolve_history(json.dumps(history), today) \
        if history else {}
    return cm.build_status(int(km), in_service, annual, severe, done, today)


def pick(results, fragment):
    return next(t for t in results if fragment in t["task"])


TODAY = date(2026, 8, 27)

# ---------------------------------------------------------------------------
# 1. Task library integrity
# ---------------------------------------------------------------------------
check("task library has >= 10 tasks", len(cm.TASK_LIBRARY) >= 10)

for t in cm.TASK_LIBRARY:
    tid = t["id"]
    check(f"{tid}: has km or month interval",
          t.get("km") is not None or t.get("mo") is not None)
    check(f"{tid}: has priority class",
          t["priority"] in ("safety-critical", "wear-item", "standard"))

ids = {t["id"] for t in cm.TASK_LIBRARY}
check("library contains oil change", any("oil" in i for i in ids))
check("library contains brake fluid", any("brake" in i for i in ids))

# ---------------------------------------------------------------------------
# 2. Dual-interval: whichever comes FIRST
# ---------------------------------------------------------------------------
# Oil 10,000 km / 12 mo (normal). 12,000 km in 6 months -> overdue by km.
res = status(12000, date(2026, 2, 27), annual_km=24000)
oil = pick(res, "oil")
check("dual interval: km event fires before time event",
      oil["km_due_at"] == 10000 and oil["status"] == "OVERDUE")

# Low-mileage car: 4,000 km but 14 months -> overdue by TIME.
res3 = status(4000, date(2025, 6, 1), annual_km=4000)
oil3 = pick(res3, "oil")
check("time overdue on low-mileage car", oil3["status"] == "OVERDUE")
check("time-due date = in-service + 12 months",
      oil3["date_due_at"] == "2026-06-01")

# ---------------------------------------------------------------------------
# 3. Due-soon thresholds
# ---------------------------------------------------------------------------
# Oil at 9,700 of 10,000 km -> within 20% -> DUE SOON.
res4 = status(9700, date(2026, 8, 1), annual_km=30000)
oil4 = pick(res4, "oil")
check("due soon when within 20% of km interval", oil4["status"] == "DUE SOON")

# Brand-new car: nothing overdue.
res5 = status(500, date(2026, 8, 20), annual_km=10000)
check("fresh vehicle has no OVERDUE items",
      all(t["status"] != "OVERDUE" for t in res5))

# ---------------------------------------------------------------------------
# 4. Severe service shortens intervals
# ---------------------------------------------------------------------------
res_norm = status(8000, date(2026, 1, 1), annual_km=16000, severe=False)
res_sev = status(8000, date(2026, 1, 1), annual_km=16000, severe=True)
oil_n = pick(res_norm, "oil")
oil_s = pick(res_sev, "oil")
check("severe service halves oil km interval",
      oil_s["interval_km"] == oil_n["interval_km"] // 2)
check("severe service flags OVERDUE earlier",
      oil_s["status"] == "OVERDUE" and oil_n["status"] in ("OK", "DUE SOON"))

# ---------------------------------------------------------------------------
# 5. History resets the interval
# ---------------------------------------------------------------------------
res_h = status(84500, date(2021, 3, 10), annual_km=15000, severe=True,
               history=[{"task": "oil", "km": 63000, "date": "2026-01-15"}])
oil_h = pick(res_h, "oil")
check("history: oil km due at 63,000 + 5,000 (severe)",
      oil_h["km_due_at"] == 68000)
check("history: oil time due 2026-01-15 + 6 months",
      oil_h["date_due_at"] == "2026-07-15")
check("history: last-done recorded",
      oil_h["last_done_km"] == 63000 and oil_h["last_done_date"] == "2026-01-15")

# ---------------------------------------------------------------------------
# 6. Annual-km fallback derivation
# ---------------------------------------------------------------------------
derived = cm.compute_annual_km(84500, date(2021, 3, 10), TODAY, None)
check("annual km derived from odometer and age", 14000 < derived < 17000)
explicit = cm.compute_annual_km(84500, date(2021, 3, 10), TODAY, 12000)
check("explicit annual km wins over derivation", explicit == 12000)

# ---------------------------------------------------------------------------
# 7. Timeline projection
# ---------------------------------------------------------------------------
done = cm.resolve_history("[]", TODAY)
events = cm.build_timeline(84500, date(2021, 3, 10), 15000, False, done, TODAY,
                           months=24)
check("timeline produces events", len(events) >= 5)
check("timeline entries carry date and task",
      all("date" in e and "task" in e for e in events))
check("timeline sorted by date",
      all(events[i]["date"] <= events[i + 1]["date"]
          for i in range(len(events) - 1)))
check("timeline horizon <= 24 months out",
      all(e["date"] <= "2028-08-31" for e in events))

# ---------------------------------------------------------------------------
# 8. CLI end-to-end
# ---------------------------------------------------------------------------
proc = run(["tasks"])
check("CLI tasks lists oil change", "oil" in proc.stdout.lower())

proc = run(["status", "--km", "84500", "--in-service", "2021-03-10"])
check("CLI status prints OVERDUE", "OVERDUE" in proc.stdout)
check("CLI status prints summary line", "Summary" in proc.stdout)

proc = run([
    "status", "--km", "84500", "--in-service", "2021-03-10",
    "--history", '[{"task":"oil","km":63000,"date":"2026-01-15"}]',
    "--severe", "--json",
])
payload = json.loads(proc.stdout)
check("CLI status --json parses", "meta" in payload and "tasks" in payload)
check("CLI status --json meta carries severe flag",
      payload["meta"]["severe"] is True)
sample = payload["tasks"][0]
required = {"task", "status", "km_due_at", "date_due_at", "interval_km",
            "interval_months", "priority", "reason"}
check("CLI status --json task keys complete",
      required.issubset(sample.keys()))

proc = run(["timeline", "--km", "84500", "--in-service", "2021-03-10",
            "--annual-km", "15000"])
check("CLI timeline prints month groups", "2026-" in proc.stdout)
check("CLI timeline prints cost ranges", "$" in proc.stdout)

proc = run(["timeline", "--km", "84500", "--in-service", "2021-03-10",
            "--annual-km", "15000", "--json"])
tl = json.loads(proc.stdout)
check("CLI timeline --json parses", isinstance(tl, dict) or isinstance(tl, list))

# ---------------------------------------------------------------------------
# 9. Input validation
# ---------------------------------------------------------------------------
proc = run(["status", "--km", "abc", "--in-service", "2021-03-10"], expect_rc=2)
check("CLI rejects non-numeric km", "error" in proc.stderr.lower())

proc = run(["status", "--km", "1000", "--in-service", "not-a-date"], expect_rc=2)
check("CLI rejects malformed date", "error" in proc.stderr.lower())

proc = run(["status", "--km", "1000", "--in-service", "2031-01-01"], expect_rc=2)
check("CLI rejects future in-service date", "error" in proc.stderr.lower())

proc = run([
    "status", "--km", "1000", "--in-service", "2020-01-01",
    "--history", "not-json",
], expect_rc=2)
check("CLI rejects malformed history JSON", "error" in proc.stderr.lower())

print()
if FAIL == 0:
    print(f"ALL TESTS PASSED ({PASS} assertions)")
    sys.exit(0)
print(f"FAILED: {FAIL} of {PASS + FAIL} assertions")
sys.exit(1)
