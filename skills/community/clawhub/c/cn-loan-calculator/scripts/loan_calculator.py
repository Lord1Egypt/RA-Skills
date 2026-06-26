#!/usr/bin/env python3
"""Loan Calculator - Calculate loan payments."""
import argparse
import json
import sys

def calc_equal_installment(principal, annual_rate, months):
    """等额本息"""
    monthly_rate = annual_rate / 100 / 12
    if monthly_rate == 0:
        monthly = principal / months
    else:
        monthly = principal * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)
    
    total = monthly * months
    interest = total - principal
    return {
        "method": "等额本息",
        "monthly_payment": round(monthly, 2),
        "total_payment": round(total, 2),
        "total_interest": round(interest, 2),
    }

def calc_equal_principal(principal, annual_rate, months):
    """等额本金"""
    monthly_rate = annual_rate / 100 / 12
    principal_part = principal / months
    
    total_interest = 0
    schedule = []
    for m in range(1, months + 1):
        remaining = principal - principal_part * (m - 1)
        interest_part = remaining * monthly_rate
        total = principal_part + interest_part
        total_interest += interest_part
        if m <= 3 or m == months:
            schedule.append({
                "month": m,
                "principal": round(principal_part, 2),
                "interest": round(interest_part, 2),
                "total": round(total, 2),
            })
    
    first_month = schedule[0]["total"]
    last_month = schedule[-1]["total"] if schedule else 0
    
    return {
        "method": "等额本金",
        "first_month_payment": round(first_month, 2),
        "last_month_payment": round(last_month, 2),
        "total_payment": round(principal + total_interest, 2),
        "total_interest": round(total_interest, 2),
    }

def main():
    parser = argparse.ArgumentParser(description="Loan Calculator")
    parser.add_argument("--amount", type=float, required=True, help="Loan amount")
    parser.add_argument("--rate", type=float, required=True, help="Annual interest rate (%)")
    parser.add_argument("--years", type=int, help="Loan term in years")
    parser.add_argument("--months", type=int, help="Loan term in months")
    parser.add_argument("--method", choices=["equal_installment", "equal_principal", "both"], default="both", help="Repayment method")
    args = parser.parse_args()
    
    months = args.months or (args.years * 12)
    if months <= 0:
        print(json.dumps({"error": "Loan term must be positive"}))
        sys.exit(1)
    
    result = {"amount": args.amount, "rate": args.rate, "term_months": months}
    
    if args.method in ["equal_installment", "both"]:
        result["equal_installment"] = calc_equal_installment(args.amount, args.rate, months)
    if args.method in ["equal_principal", "both"]:
        result["equal_principal"] = calc_equal_principal(args.amount, args.rate, months)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
