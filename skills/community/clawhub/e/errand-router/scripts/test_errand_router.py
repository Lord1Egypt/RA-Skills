#!/usr/bin/env python3
"""Tests for errand_router.py — run with: python3 scripts/test_errand_router.py"""
import subprocess
import sys
import os
import json
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "errand_router.py")

FAILED = []


def check(name, cond, extra=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {extra}" if extra and not cond else ""))
    if not cond:
        FAILED.append(name)


def run(args):
    r = subprocess.run([sys.executable, SCRIPT] + args,
                       capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout, r.stderr


# 1. haversine sanity: 1 degree of latitude ~ 111 km
sys.path.insert(0, HERE)
import errand_router as er  # noqa: E402

d = er.haversine_km(52.0, 13.0, 53.0, 13.0)
check("haversine 1° lat ≈ 111 km", abs(d - 111.2) < 1.0, f"got {d:.2f}")

d2 = er.haversine_km(52.52, 13.405, 52.52, 13.405)
check("haversine same point = 0", d2 == 0.0)

# 2. quick mode with 3 stops, no return
code, out, err = run(["quick", "--start", "home,52.52,13.405",
                      "--stop", "post,52.51,13.39,10,09:00,18:00",
                      "--stop", "pharm,52.54,13.42,15,09:00,20:00",
                      "--depart", "17:00", "--no-return"])
check("quick mode exits 0", code == 0, err)
check("quick mode mentions both stops", "post" in out and "pharm" in out)
check("quick mode shows ORDER", "ORDER" in out)

# 3. violation detection: stop closes before arrival
code, out, err = run(["quick", "--start", "home,52.52,13.405",
                      "--stop", "closing,52.60,13.50,10,09:00,17:05",
                      "--depart", "17:00", "--no-return"])
check("late arrival flagged (exit 1)", code == 1)
check("violation printed", "VIOLATION" in out.upper())

# 4. JSON output parses
code, out, err = run(["quick", "--start", "home,52.52,13.405",
                      "--stop", "a,52.53,13.41,10",
                      "--stop", "b,52.51,13.44,5",
                      "--depart", "10:00", "--no-return", "--json"])
try:
    data = json.loads(out)
    check("JSON parses", True)
    check("JSON has totals", "totals" in data and "km" in data["totals"])
    names = data["order"]
    check("all stops present exactly once",
          sorted(names) == ["a", "b", "home"], str(names))
except Exception as e:
    check("JSON parses", False, str(e))

# 5. plan mode from a JSON file with a time window forcing wait
problem = {
    "start": {"name": "home", "lat": 52.52, "lon": 13.405},
    "depart": "08:00",
    "speed_kmh": 30,
    "stops": [
        {"name": "bank", "lat": 52.53, "lon": 13.42, "dwell_min": 10,
         "open": "09:00", "close": "16:00"},
        {"name": "bakery", "lat": 52.525, "lon": 13.41, "dwell_min": 5},
        {"name": "gym", "lat": 52.535, "lon": 13.435, "dwell_min": 60,
         "open": "07:00", "close": "22:00"},
    ],
}
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    json.dump(problem, f)
    tmp = f.name

code, out, err = run(["plan", tmp, "--json"])
try:
    data = json.loads(out)
    legs = data["legs"]
    bank_leg = [l for l in legs if l["to"] == "bank"][0]
    check("wait-for-open simulated", bank_leg["wait_min"] > 0,
          f"wait={bank_leg['wait_min']}")
    check("totals elapsed = drive+dwell+wait",
          abs(data["totals"]["elapsed_min"]
              - (data["totals"]["drive_min"] + data["totals"]["dwell_min"]
                 + data["totals"]["wait_min"])) < 0.5)
except Exception as e:
    check("plan JSON parses", False, str(e))
os.unlink(tmp)

# 6. totals math consistency on the JSON output
code, out, err = run(["quick", "--start", "home,52.52,13.405",
                      "--stop", "x1,52.60,13.50,10",
                      "--stop", "x2,52.45,13.30,10",
                      "--stop", "x3,52.55,13.60,10",
                      "--depart", "09:00", "--no-return", "--json"])
data = json.loads(out)
leg_sum = round(sum(l["km"] for l in data["legs"]), 2)
check("leg km sums to total km", abs(leg_sum - data["totals"]["km"]) < 0.05,
      f"{leg_sum} vs {data['totals']['km']}")

# 7. 2-opt improvement beats a bad fixed order (drive time)
p = er.Problem(
    start=er.Stop("home", x=0, y=0, dwell_min=0),
    stops=[
        er.Stop("far", x=10, y=0, dwell_min=1),
        er.Stop("mid", x=5, y=0, dwell_min=1),
        er.Stop("near", x=1, y=0, dwell_min=1),
    ],
    depart_min=9 * 60,
)
route = er.solve(p)
res = er.simulate(p, route)
names = [n for n in res["order"] if n != "home"]
check("solver orders collinear stops near→mid→far", names == ["near", "mid", "far"],
      str(names))

print()
if FAILED:
    print(f"{len(FAILED)} FAILED: {FAILED}")
    sys.exit(1)
print("ALL TESTS PASSED")
