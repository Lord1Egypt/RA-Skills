#!/usr/bin/env python3
"""
Car Lease & Buy Calculator
Usage: python3 calc.py [cap] [residual] [mf] [term] [down]
Example: python3 calc.py 45000 0.55 0.00125 36 3000
"""

import sys

def calc_lease(cap_cost, residual_pct, money_factor, term_months, down_payment=0, tax_rate=0.06):
    residual_value = cap_cost * residual_pct
    adjusted_cap = cap_cost - down_payment
    depreciation = (adjusted_cap - residual_value) / term_months
    finance_charge = (adjusted_cap + residual_value) * money_factor
    base_payment = depreciation + finance_charge
    total_payment = base_payment * (1 + tax_rate)
    total_cost = (total_payment * term_months) + down_payment
    apr_equiv = money_factor * 2400

    print("\n========== LEASE CALCULATOR ==========")
    print(f"  Cap Cost (MSRP/Negotiated): ${cap_cost:,.0f}")
    print(f"  Down Payment:               ${down_payment:,.0f}")
    print(f"  Adjusted Cap Cost:          ${adjusted_cap:,.0f}")
    print(f"  Residual Value ({residual_pct*100:.0f}%):      ${residual_value:,.0f}")
    print(f"  Money Factor:               {money_factor:.5f}  (~{apr_equiv:.1f}% APR)")
    print(f"  Term:                       {term_months} months")
    print(f"  Depreciation/mo:            ${depreciation:,.2f}")
    print(f"  Finance Charge/mo:          ${finance_charge:,.2f}")
    print(f"  Base Payment/mo:            ${base_payment:,.2f}")
    print(f"  Payment w/ Tax ({tax_rate*100:.0f}%):     ${total_payment:,.2f}/mo")
    print(f"  Total Cost of Lease:        ${total_cost:,.0f}")
    print("=======================================\n")
    return total_payment

def calc_buy(price, down, rate_pct, term_months, tax_rate=0.06):
    loan_amount = (price * (1 + tax_rate)) - down
    monthly_rate = rate_pct / 100 / 12
    if monthly_rate > 0:
        payment = loan_amount * (monthly_rate * (1 + monthly_rate)**term_months) / ((1 + monthly_rate)**term_months - 1)
    else:
        payment = loan_amount / term_months
    total_cost = (payment * term_months) + down

    print("\n========== BUY CALCULATOR ==========")
    print(f"  Vehicle Price:              ${price:,.0f}")
    print(f"  Down Payment:               ${down:,.0f}")
    print(f"  Loan Amount (w/ tax):       ${loan_amount:,.0f}")
    print(f"  APR:                        {rate_pct:.2f}%")
    print(f"  Term:                       {term_months} months")
    print(f"  Monthly Payment:            ${payment:,.2f}/mo")
    print(f"  Total Cost:                 ${total_cost:,.0f}")
    print("=====================================\n")
    return payment

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) >= 4:
        cap = float(args[0])
        residual = float(args[1])
        mf = float(args[2])
        term = int(args[3])
        down = float(args[4]) if len(args) > 4 else 0
        calc_lease(cap, residual, mf, term, down)
    else:
        print("Demo mode — running sample deal:")
        print("Scenario: $45,000 vehicle, 55% residual, MF 0.00125, 36mo, $3k down")
        calc_lease(45000, 0.55, 0.00125, 36, 3000)
        print("Scenario: $45,000 purchase, $5k down, 6.9% APR, 60mo")
        calc_buy(45000, 5000, 6.9, 60)
