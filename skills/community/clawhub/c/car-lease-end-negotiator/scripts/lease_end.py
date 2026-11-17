#!/usr/bin/env python3
"""car-lease-end-negotiator — three-way lease-end decision, wear-bill pricing,
and the negotiation sheet. Stdlib only.

Subcommands: decide, wear, sheet, --demo
"""
import argparse


def cmd_decide(a) -> None:
    over = max(0, a.miles_now - a.mile_allowance)
    projected_over = over + a.miles_left_estimate * a.months_left if a.miles_now > a.mile_allowance else over
    equity = a.market - a.residual
    mileage_bill_return = projected_over * a.mile_rate
    return_cost = a.disposition + mileage_bill_return + a.wear_est
    buyout_cost = a.residual * (1 + a.tax_rate) + a.purchase_fee
    # buy-and-sell: buy at residual(+tax+fee), sell at market minus sale costs %
    sale_costs = a.market * a.sale_cost_pct
    buy_sell_net = a.market - sale_costs - buyout_cost
    remaining_payments = a.payment * a.months_left

    print("=== LEASE-END THREE-PATH DECISION\n")
    print(f"Residual (contract):        ${a.residual:>10,.0f}")
    print(f"Market (private-party):     ${a.market:>10,.0f}")
    print(f"EQUITY (market-residual):   ${equity:>10,.0f}  {'<- POSITIVE: do NOT just return it' if equity > 500 else ''}")
    print(f"Excess miles (est. @end):   {projected_over:>10,.0f} mi")
    print(f"  mileage bill if returned: ${mileage_bill_return:>10,.0f}")
    print(f"Remaining payments:         ${remaining_payments:>10,.0f} ({a.months_left} mo)\n")

    print("--- PATH A: RETURN AT MATURITY ---")
    print(f"  disposition ${a.disposition:,.0f} + mileage ${mileage_bill_return:,.0f} "
          f"+ wear est ${a.wear_est:,.0f} = ${return_cost:,.0f} out of pocket, walk away.")
    print("--- PATH B: BUY OUT AND KEEP ---")
    print(f"  ${buyout_cost:,.0f} (+tax {a.tax_rate*100:.0f}% on residual, purchase fee "
          f"${a.purchase_fee:,.0f}) vs buying same car used at ${a.market:,.0f}: "
          f"{'BUYOUT CHEAPER — keep it' if buyout_cost < a.market else 'market is cheaper — buy used, return lease'}")
    print("--- PATH C: BUY-AND-SELL (capture equity) ---")
    print(f"  net after sale costs ({a.sale_cost_pct*100:.0f}%): ${buy_sell_net:,.0f}"
          f"{'  <- TAKE THIS PATH' if buy_sell_net > 300 and buy_sell_net > -return_cost else ''}")
    print(f"  (vs PATH A which costs -${return_cost:,.0f}; difference: "
          f"${buy_sell_net + return_cost:,.0f})\n")

    best = min(return_cost, -buy_sell_net)
    if buy_sell_net > 500:
        verdict = (f"BUY-AND-SELL: pocket ~${buy_sell_net:,.0f} of equity "
                   f"(or buy out if you love the car — it's ${a.market - buyout_cost:,.0f} "
                   f"under market).")
    elif equity > 500:
        verdict = f"BUYOUT WINS: car is ${equity:,.0f} under market at residual."
    elif equity < -1500:
        verdict = (f"RETURN AND WALK: residual is ${-equity:,.0f} ABOVE market — "
                   f"the lessor priced this badly in your favor.")
    else:
        verdict = ("EITHER WAY IS FINE (equity ≈ 0): negotiate disposition waiver "
                   "or keep it for convenience; no material money at stake.")
    print(f"VERDICT: {verdict}")
    print("\nNever announce buy-and-sell at the dealer desk: get payoff quote in "
          "writing, line up buyer/CU paperwork before the final payment date.")


def cmd_wear(a) -> None:
    print("=== WEAR-BILL LINE-ITEM AUDIT\n")
    total = 0.0
    for item in a.items:
        name, _, amt = item.rpartition(",")
        amt = float(amt)
        total += amt
        print(f"  ${amt:>7,.0f}  {name}")
    print(f"  {'-'*30}\n  ${total:>7,.0f}  inspector's total (opening ask, not a bill)")
    print(f"\nYour self-fix estimate: ${a.self_fix_est:,.0f} "
          f"(scuffs/tires/bumper at independent shop)")
    print(f"Contest-worthy lines (normal-use vs damage is defined in your "
          f"contract's wear guide): tread within spec? stone chips? "
          f"interior wear consistent with mileage?")
    if a.self_fix_est < total * 0.7:
        print(f"\nFIX-YOURSELF WINS: save ~${total - a.self_fix_est:,.0f}. Get the "
              "wear guide definition in writing, fix cheap items, contest the rest.")
    else:
        print("\nBill is roughly fair — negotiate the total, not each line; ask "
              "for a 20-30% settlement on the aggregate if paid at turn-in.")
    print("Tire trick: adjudicated 4-tire 'tread' charges often die when you "
          "replace the 2 below-spec tires yourself (~$180-260) with receipts.")


def cmd_sheet(a) -> None:
    equity = a.market - a.residual
    print("=== LEASE-END NEGOTIATION CARD (print, carry)\n")
    rows = [
        ("Disposition fee", f"${a.disposition:,.0f}", "WAIVABLE",
         "Waived routinely with same-brand re-lease or purchase — ask the CAPTIVE by phone first, dealer second."),
        ("Excess mileage rate", "$0.20-0.30/mi", "FIXED but avoidable",
         "Vanishes on buyout; pre-purchase packs cheaper than end rate if returning."),
        ("Wear adjudication", "line items", "CONTESTABLE",
         "Pre-turn-in inspection 30-60 days out; price every line at an independent shop; wear guide definitions in writing."),
        ("Purchase-option price", f"${a.residual:,.0f}", "FIXED (contract)",
         "Some captives negotiate residual on slow models — ask, in writing."),
        ("Your equity", f"${equity:,.0f}", "YOUR LEVERAGE",
         "Positive = buy-and-sell or keep; negative = return happily, residual overpriced."),
    ]
    for name, val, status, note in rows:
        print(f"[{status}]\n  {name}: {val}\n    -> {note}\n")
    print("Call order: 1) captive finance co (payoff + disposition + pack rates) "
          "2) credit union (buyout loan / buyer paperwork) 3) dealer LAST.")
    print("Golden rule: get every number in writing before the last payment date.")


def run_demo() -> None:
    import types
    print("######## DEMO 1: equity-positive, over-mileage lease ########\n")
    cmd_decide(types.SimpleNamespace(residual=18000, market=20500, months_left=8,
                                     payment=320, disposition=400, miles_now=30500,
                                     mile_allowance=27000, mile_rate=0.25,
                                     wear_est=300, tax_rate=0.08, purchase_fee=300,
                                     sale_cost_pct=0.08, miles_left_estimate=300))
    print("\n######## DEMO 2: the $912 inspection letter ########\n")
    cmd_wear(types.SimpleNamespace(
        items=["wheel scuff x2,160", "windshield chip,90", "tire tread (4),420",
               "bumper scuff,242"], self_fix_est=380))
    print("\n######## DEMO 3: negotiation card ########\n")
    cmd_sheet(types.SimpleNamespace(residual=18000, market=20500, disposition=400))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd")
    d = sub.add_parser("decide")
    d.add_argument("--residual", type=float, required=True)
    d.add_argument("--market", type=float, required=True)
    d.add_argument("--months-left", type=int, required=True)
    d.add_argument("--payment", type=float, default=300)
    d.add_argument("--disposition", type=float, default=400)
    d.add_argument("--miles-now", type=float, default=0)
    d.add_argument("--mile-allowance", type=float, default=36000)
    d.add_argument("--mile-rate", type=float, default=0.25)
    d.add_argument("--wear-est", type=float, default=300)
    d.add_argument("--tax-rate", type=float, default=0.08)
    d.add_argument("--purchase-fee", type=float, default=300)
    d.add_argument("--sale-cost-pct", type=float, default=0.08)
    d.add_argument("--miles-left-estimate", type=float, default=800)
    w = sub.add_parser("wear")
    w.add_argument("--items", nargs="+", required=True, help="'name,amount' entries")
    w.add_argument("--self-fix-est", type=float, default=0)
    s = sub.add_parser("sheet")
    s.add_argument("--residual", type=float, required=True)
    s.add_argument("--market", type=float, required=True)
    s.add_argument("--disposition", type=float, default=400)
    p.add_argument("--demo", action="store_true")
    a = p.parse_args()
    if a.demo:
        run_demo()
    elif a.cmd == "decide":
        cmd_decide(a)
    elif a.cmd == "wear":
        cmd_wear(a)
    elif a.cmd == "sheet":
        cmd_sheet(a)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
