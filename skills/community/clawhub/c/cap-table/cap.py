#!/usr/bin/env python3
import argparse
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--founders', type=int, default=2)
    p.add_argument('--employees', type=float, default=10)
    p.add_argument('--investors', type=float, default=0)
    args = p.parse_args()
    total = 100
    founder_pct = 70 - (args.founders - 1) * 5
    employee_pct = args.employees
    investor_pct = args.investors / 10000
    print(f"""📋 CAP TABLE
{'='*50}
Founders:   {founder_pct:.1f}% ({args.founders} founders)
Employees: {employee_pct:.1f}% (option pool)
Investors: {100-founder_pct-employee_pct:.1f}%
""")
if __name__ == '__main__':
    main()
