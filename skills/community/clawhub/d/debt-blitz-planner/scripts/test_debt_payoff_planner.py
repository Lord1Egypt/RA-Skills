#!/usr/bin/env python3
"""Self-test for debt_payoff_planner.py — no pytest needed, plain asserts."""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from debt_payoff_planner import parse_debt, simulate, run_all, fmt

SCRIPT = Path(__file__).parent / "debt_payoff_planner.py"


def test_parse():
    d = parse_debt("Visa,4200,22.9,105")
    assert d["name"] == "Visa" and d["balance"] == 420000 and d["apr"] == 22.9
    assert d["min"] == 10500
    try:
        parse_debt("bad-spec")
        assert False, "should reject"
    except ValueError:
        pass
    print("ok parse")


def test_single_debt_payoff():
    # $1200 @ 12% min $106, extra 0 -> roughly a year
    r = simulate([parse_debt("X,1200,12,106")], "avalanche", extra_c=0)
    assert r["ok"] and 10 <= r["months"] <= 13, r
    print(f"ok single debt: {r['months']} months")


def test_invariants():
    debts = [parse_debt(s) for s in ("Visa,4200,22.9,105", "MC,1800,19.9,56", "Car,9500,6.5,290")]
    results = {r["strategy"]: r for r in run_all(debts, extra_c=15000, budget_c=None)}
    assert results["avalanche"]["total_interest"] <= results["snowball"]["total_interest"]
    assert results["snowball"]["total_interest"] <= results["min-only"]["total_interest"] + 1
    assert results["avalanche"]["months"] <= results["snowball"]["months"]
    # payoff orders
    assert results["avalanche"]["payoff_order"][0] == "Visa"  # highest APR
    assert results["snowball"]["payoff_order"][0] == "MC"     # smallest balance
    print(f"ok invariants: av={results['avalanche']['months']}mo/{fmt(results['avalanche']['total_interest'])} "
          f"sb={results['snowball']['months']}mo/{fmt(results['snowball']['total_interest'])} "
          f"base={results['min-only']['months']}mo/{fmt(results['min-only']['total_interest'])}")


def test_negative_amortization():
    # $5000 @ 29.9% with $100 min: interest ≈ $124 > min -> never paid off
    debts = [parse_debt("Trap,5000,29.9,100")]
    r = simulate(debts, "min-only", extra_c=0)
    assert not r["ok"] and "survivable" in r["error"], r
    print("ok negative amortization detected")


def test_budget_mode():
    debts = [parse_debt("A,2000,20,60"), parse_debt("B,1000,10,30")]
    r = simulate(debts, "avalanche", budget_c=round(200 * 100))
    assert r["ok"]
    try:
        simulate(debts, "avalanche", budget_c=round(50 * 100))
        assert False
    except ValueError as e:
        assert "minimums" in str(e)
    print("ok budget mode")


def test_cli():
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--debt", "Visa,4200,22.9,105",
         "--debt", "MC,1800,19.9,56", "--extra", "150"],
        capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "avalanche" in r.stdout and "snowball" in r.stdout
    assert "payoff order" in r.stdout
    print("ok cli")


if __name__ == "__main__":
    test_parse()
    test_single_debt_payoff()
    test_invariants()
    test_negative_amortization()
    test_budget_mode()
    test_cli()
    print("\nALL TESTS PASSED ✅")
