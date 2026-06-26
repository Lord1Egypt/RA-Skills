#!/usr/bin/env python3
"""Calculate monthly principal & interest for a fixed-rate mortgage."""

import argparse
import math


def monthly_payment(principal: float, annual_rate: float, years: int) -> float:
    """Return monthly P&I payment."""
    if annual_rate == 0:
        return principal / (years * 12)
    r = annual_rate / 100 / 12
    n = years * 12
    return principal * (r * math.pow(1 + r, n)) / (math.pow(1 + r, n) - 1)


def main():
    parser = argparse.ArgumentParser(description="Mortgage payment calculator")
    parser.add_argument("--principal", "-p", type=float, required=True, help="Loan amount in dollars")
    parser.add_argument("--rate", "-r", type=float, required=True, help="Annual interest rate (e.g. 6.5)")
    parser.add_argument("--years", "-y", type=int, default=30, help="Loan term in years (default: 30)")
    parser.add_argument("--compare-rate", "-c", type=float, help="Compare against a second rate")
    args = parser.parse_args()

    pmt = monthly_payment(args.principal, args.rate, args.years)
    total = pmt * args.years * 12
    interest = total - args.principal

    print(f"Loan: ${args.principal:,.0f} at {args.rate:.2f}% for {args.years} years")
    print(f"Monthly P&I: ${pmt:,.2f}")
    print(f"Total paid: ${total:,.0f}")
    print(f"Total interest: ${interest:,.0f}")

    if args.compare_rate is not None:
        pmt2 = monthly_payment(args.principal, args.compare_rate, args.years)
        diff = pmt2 - pmt
        print(f"\nAt {args.compare_rate:.2f}%: ${pmt2:,.2f}/mo ({'+' if diff >= 0 else ''}{diff:,.2f}/mo)")
        print(f"Difference over {args.years} years: ${abs(diff) * args.years * 12:,.0f}")


if __name__ == "__main__":
    main()
