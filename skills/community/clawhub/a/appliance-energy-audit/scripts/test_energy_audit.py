#!/usr/bin/env python3
"""Tests for energy_audit.py — plain asserts, no pytest. Run: python3 test_energy_audit.py"""

import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "energy_audit.py")

sys.path.insert(0, HERE)
import energy_audit as ea  # noqa: E402


def run_cli(args):
    return subprocess.run([sys.executable, ENGINE] + args,
                          capture_output=True, text=True)


def check(label, cond):
    assert cond, label
    print("[PASS] %s" % label)


# ---- resolve_appliance ----
a = ea.resolve_appliance({"name": "f", "preset": "fridge"})
check("fridge preset: watts 150", a["watts"] == 150)
check("fridge preset: duty 0.35", abs(a["duty"] - 0.35) < 1e-9)
check("fridge preset: hours 24 (24h appliance)", a["hours_day"] == 24)

a = ea.resolve_appliance({"name": "x", "watts": 100})
check("custom: default duty 1.0", a["duty"] == 1.0)
check("custom: default hours 4.0", a["hours_day"] == 4.0)

a = ea.resolve_appliance({"name": "x", "preset": "tv-led-55", "hours_day": 2})
check("preset override: hours_day wins", a["hours_day"] == 2)
check("preset override: watts kept from preset", a["watts"] == 100)

try:
    ea.resolve_appliance({"name": "x", "watts": 100, "duty": 0})
    raise SystemExit("FAIL: duty=0 accepted")
except ValueError:
    check("duty=0 rejected", True)

try:
    ea.resolve_appliance({"name": "x"})
    raise SystemExit("FAIL: missing watts accepted")
except ValueError:
    check("missing watts+preset rejected", True)

try:
    ea.resolve_appliance({"name": "x", "preset": "nope"})
    raise SystemExit("FAIL: bad preset accepted")
except ValueError:
    check("unknown preset rejected", True)

a = ea.resolve_appliance({"name": "x", "watts": 60, "qty": 5})
check("qty normalized to int", a["qty"] == 5)

# ---- monthly_kwh ----
a = ea.resolve_appliance({"name": "x", "watts": 1000, "hours_day": 2, "duty": 1.0, "standby_w": 0})
# 1000W * 2h * 30d = 60 kWh
check("1000W @2h/day = 60 kWh/mo", abs(ea.monthly_kwh(a) - 60.0) < 1e-9)

a = ea.resolve_appliance({"name": "x", "watts": 100, "hours_day": 24, "duty": 0.5, "standby_w": 0})
# 100W * 24h * 30d * 0.5 = 36 kWh
check("duty cycle halves consumption", abs(ea.monthly_kwh(a) - 36.0) < 1e-9)

a = ea.resolve_appliance({"name": "x", "watts": 100, "hours_day": 4, "duty": 1.0, "standby_w": 5})
# active 100*4*30 = 12 kWh; idle 5W * 20h * 30 = 3 kWh → 15 kWh
check("standby added on idle hours", abs(ea.monthly_kwh(a) - 15.0) < 1e-9)

a = ea.resolve_appliance({"name": "x", "watts": 60, "hours_day": 5, "qty": 4})
check("qty multiplies kWh", abs(ea.monthly_kwh(a) - 4 * 60 * 5 * 30 / 1000) < 1e-9)

a = ea.resolve_appliance({"name": "x", "watts": 100, "hours_day": 4, "standby_w": 5})
check("standby_kwh = 5W*20h*30d", abs(ea.standby_kwh(a) - 3.0) < 1e-9)

# ---- tiered_cost ----
check("tiered: within first tier", abs(ea.tiered_cost(300, [(500, 0.12), (None, 0.20)]) - 36.0) < 1e-9)
check("tiered: spans two tiers", abs(ea.tiered_cost(700, [(500, 0.12), (None, 0.20)]) - (60.0 + 40.0)) < 1e-9)
check("tiered: three tiers", abs(ea.tiered_cost(
    1500, [(500, 0.12), (1000, 0.15), (None, 0.20)]) - (60.0 + 75.0 + 100.0)) < 1e-9)
check("tiered: zero usage zero cost", ea.tiered_cost(0, [(500, 0.12), (None, 0.20)]) == 0.0)

# ---- build_audit ----
specs = [
    {"name": "fridge", "preset": "fridge"},
    {"name": "lamp", "preset": "led-bulb", "qty": 5, "hours_day": 4},
    {"name": "dryer", "preset": "electric-dryer", "hours_day": 0.5},
]
audit = ea.build_audit(specs, rate=0.20)
check("audit has 3 rows", len(audit["rows"]) == 3)
check("rows sorted by cost desc", audit["rows"][0]["cost_month"] >= audit["rows"][1]["cost_month"]
      >= audit["rows"][2]["cost_month"])
check("total = sum of rows", abs(audit["total_kwh_month"] - sum(r["kwh_month"] for r in audit["rows"])) < 0.05)
check("share sums ~100%", abs(sum(r["share_pct"] for r in audit["rows"]) - 100.0) < 0.5)
check("cost_year = 12x month", abs(audit["total_cost_year"] - audit["total_cost_month"] * 12) < 0.05)

audit_t = ea.build_audit(specs, tiers=[(500, 0.12), (None, 0.20)])
check("tiered audit computes cost", audit_t["total_cost_month"] > 0)
check("tiered effective rate between rates", 0.12 <= audit_t["effective_rate"] <= 0.20)

# ---- calibrate ----
audit2 = ea.build_audit([{"name": "f", "preset": "fridge"}], rate=0.17)
cal = ea.calibrate(audit2, ea.monthly_kwh(ea.resolve_appliance({"name": "f", "preset": "fridge"})))
check("calibrate matched when equal", cal["verdict"] == "matched")
cal = ea.calibrate(audit2, 1000.0)
check("calibrate undercounted verdict", cal["verdict"] == "undercounted")
check("calibrate gap positive", cal["gap_kwh"] > 0)
cal = ea.calibrate(audit2, 30.0)
check("calibrate overcounted verdict", cal["verdict"] == "overcounted")

# ---- replace_analysis ----
rep = ea.replace_analysis(
    {"name": "old-fridge", "preset": "fridge"},
    {"name": "new-fridge", "watts": 100, "duty": 0.30, "hours_day": 24},
    800.0, rate=0.17)
check("replace: new uses less", rep["kwh_saved_month"] > 0)
check("replace: savings positive", rep["money_saved_month"] > 0)
check("replace: payback = price/monthly savings",
      abs(rep["payback_months"] - 800.0 / rep["money_saved_month"]) < 1.0)
check("replace: worth_it bool", isinstance(rep["worth_it"], bool))

rep2 = ea.replace_analysis(
    {"name": "new", "preset": "fridge"},
    {"name": "old-guzzler", "watts": 400, "duty": 0.6, "hours_day": 24},
    500.0, rate=0.17)
check("replace: negative savings detected", rep2["kwh_saved_month"] < 0)

# ---- parse_appliance_arg ----
s = ea.parse_appliance_arg("fridge")
check("parse: name only", s["name"] == "fridge" and "watts" not in s)

s = ea.parse_appliance_arg("my tv,tv-led-55")
check("parse: preset form", s.get("preset") == "tv-led-55")

s = ea.parse_appliance_arg("heater,1500")
check("parse: watts number", s["watts"] == 1500)

s = ea.parse_appliance_arg("bulbs,led-bulb,6,8")
check("parse: preset+hours+qty", s["preset"] == "led-bulb" and s["hours_day"] == 6 and s["qty"] == 8)

s = ea.parse_appliance_arg("box,1200,3,2,4")
check("parse: watts+hours+qty+standby", s["watts"] == 1200 and s["hours_day"] == 3
      and s["qty"] == 2 and s["standby_w"] == 4)

try:
    ea.parse_appliance_arg("x,abc,def")
    raise SystemExit("FAIL: garbage numbers accepted")
except ValueError:
    check("parse: non-numeric rejected", True)

# ---- _parse_tiers ----
t = ea._parse_tiers("0.12:500,0.20:")
check("tiers: unlimited tail", t == [(500, 0.12), (None, 0.20)])
t = ea._parse_tiers("0.10:200,0.15:800,0.30:*")
check("tiers: * means unlimited", t[-1][0] is None)

for bad in ["0.12", "0.30:200,0.12:", "0.12:500,0.10:", "-0.5:"]:
    try:
        ea._parse_tiers(bad)
        raise SystemExit("FAIL: bad tiers accepted: %s" % bad)
    except ValueError:
        pass
check("tiers: malformed strings rejected", True)

# ---- CLI ----
r = run_cli(["library"])
check("cli library exits 0", r.returncode == 0)
check("cli library lists fridge", "fridge" in r.stdout)

r = run_cli(["estimate", "dryer,electric-dryer,0.5", "--rate", "0.25"])
check("cli estimate exits 0", r.returncode == 0)
check("cli estimate shows kWh", "kWh/month" in r.stdout)

r = run_cli(["audit", "-a", "fridge,fridge", "-a", "tv,tv-led-55,5", "--rate", "0.20", "--json"])
check("cli audit json exits 0", r.returncode == 0)
data = json.loads(r.stdout)
check("cli audit json parses with rows", isinstance(data.get("rows"), list) and len(data["rows"]) == 2)
check("cli audit json has totals", "total_cost_month" in data)

r = run_cli(["audit", "-a", "fridge,fridge", "--tiers", "0.12:500,0.20:"])
check("cli audit tiers exits 0", r.returncode == 0 and "TOTAL" in r.stdout)

r = run_cli(["calibrate", "-a", "fridge,fridge", "--bill-kwh", "900"])
check("cli calibrate exits 0", r.returncode == 0 and "undercounted" in r.stdout)

r = run_cli(["replace", "--old", "lamp,halogen-floor", "--new", "led lamp,22,4",
             "--price", "45", "--rate", "0.17"])
check("cli replace exits 0", r.returncode == 0)
check("cli replace shows payback", "PAYS BACK" in r.stdout or "payback" in r.stdout.lower())

r = run_cli(["example"])
check("cli example exits 0", r.returncode == 0 and "TOTAL" in r.stdout)

r = run_cli(["audit"])
check("cli audit with no appliances exits 2", r.returncode == 2)

r = run_cli(["audit", "-a", "thing,nosuchpreset"])
check("cli bad preset exits 2", r.returncode == 2)

r = run_cli(["audit", "-a", "fridge,fridge", "--tiers", "0.12"])
check("cli bad tiers exits 2", r.returncode == 2)

# file input
tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
json.dump([{"name": "f", "preset": "fridge"},
           {"name": "t", "preset": "tv-led-55", "hours_day": 3}], tmp)
tmp.close()
r = run_cli(["audit", "-f", tmp.name, "--json"])
check("cli audit from file exits 0", r.returncode == 0)
d = json.loads(r.stdout)
check("cli audit from file 2 rows", len(d["rows"]) == 2)
os.unlink(tmp.name)

r = run_cli(["audit", "-f", "/nonexistent/x.json"])
check("cli missing file exits 2", r.returncode == 2)

print("\nALL TESTS PASSED")
