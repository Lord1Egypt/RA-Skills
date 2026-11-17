#!/usr/bin/env python3
"""hr-calculator CLI：HR 税费计算器（8 个子命令，JSON 输出）。

用法：python3 hr_calc.py <command> [args...]
子命令：salary / reverse-salary / labor / reverse-labor /
        author / privilege / reverse-privilege / compensation
"""
import argparse
import json
from decimal import Decimal, InvalidOperation

from calc.salary import salary_calculation, reverse_salary_calculation
from calc.remuneration import (labor_calculate, reverse_labor_calculate,
                               author_calculate, privilege_calculate,
                               reverse_privilege_calculate, compensation_calculate)


def amount(value: str, name: str) -> Decimal:
    """解析金额参数；非法或为负 → 退出码 1 + stderr 中文报错"""
    try:
        d = Decimal(value)
    except (InvalidOperation, ValueError):
        raise SystemExit(f"参数错误：{name} 不是合法数字：{value}")
    if d < 0:
        raise SystemExit(f"参数错误：{name} 不能为负数：{value}")
    return d


def periods_value(value: str) -> int:
    try:
        n = int(value)
    except ValueError:
        raise SystemExit(f"参数错误：--periods 必须是正整数：{value}")
    if n < 1:
        raise SystemExit(f"参数错误：--periods 必须 ≥ 1：{value}")
    return n


def add_salary_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--periods", default="1", help="缴纳期数(月)，累计预扣用，默认 1")
    p.add_argument("--social-ee", default="0", help="社保个人月缴总额，默认 0")
    p.add_argument("--fund-ee", default="0", help="公积金个人月缴额，默认 0（0=不缴纳）")
    p.add_argument("--deduction-child-edu", default="0", help="专项附加:子女教育(月)")
    p.add_argument("--deduction-continue-edu", default="0", help="专项附加:继续教育(月)")
    p.add_argument("--deduction-medical", default="0", help="专项附加:大病医疗(月)")
    p.add_argument("--deduction-house", default="0", help="专项附加:住房(月)")
    p.add_argument("--deduction-elder", default="0", help="专项附加:赡养老人(月)")
    p.add_argument("--deduction-infant", default="0", help="专项附加:3岁以下婴幼儿照护(月)")
    p.add_argument("--personal-pension", default="0", help="个人养老金(月)")


def salary_kwargs(args) -> dict:
    return dict(
        periods=periods_value(args.periods),
        social_ee=amount(args.social_ee, "--social-ee"),
        fund_ee=amount(args.fund_ee, "--fund-ee"),
        child_edu=amount(args.deduction_child_edu, "--deduction-child-edu"),
        continue_edu=amount(args.deduction_continue_edu, "--deduction-continue-edu"),
        serious_medical=amount(args.deduction_medical, "--deduction-medical"),
        house=amount(args.deduction_house, "--deduction-house"),
        elder=amount(args.deduction_elder, "--deduction-elder"),
        infant_care=amount(args.deduction_infant, "--deduction-infant"),
        personal_pension=amount(args.personal_pension, "--personal-pension"),
    )


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(prog="hr_calc.py", description="HR 税费计算器")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("salary", help="工资个税正算")
    p.add_argument("--before-tax", required=True, help="税前月收入")
    add_salary_args(p)

    p = sub.add_parser("reverse-salary", help="工资个税反推（税后→税前）")
    p.add_argument("--after-tax", required=True, help="到手月收入")
    add_salary_args(p)

    p = sub.add_parser("labor", help="劳务报酬正算")
    p.add_argument("--before-tax", required=True)
    p = sub.add_parser("reverse-labor", help="劳务报酬反推")
    p.add_argument("--after-tax", required=True)
    p = sub.add_parser("author", help="稿酬正算")
    p.add_argument("--before-tax", required=True)
    p = sub.add_parser("privilege", help="特许权使用费正算")
    p.add_argument("--before-tax", required=True)
    p = sub.add_parser("reverse-privilege", help="特许权使用费反推")
    p.add_argument("--after-tax", required=True)
    p = sub.add_parser("compensation", help="解除劳动合同一次性补偿金")
    p.add_argument("--before-tax", required=True, help="补偿金总额")
    p.add_argument("--avg-salary", required=True, help="当地上年职工月平均工资")

    args = parser.parse_args(argv)

    try:
        if args.command == "salary":
            result = salary_calculation(amount(args.before_tax, "--before-tax"),
                                        **salary_kwargs(args))
        elif args.command == "reverse-salary":
            result = reverse_salary_calculation(amount(args.after_tax, "--after-tax"),
                                                **salary_kwargs(args))
        elif args.command == "labor":
            result = labor_calculate(amount(args.before_tax, "--before-tax"))
        elif args.command == "reverse-labor":
            result = reverse_labor_calculate(amount(args.after_tax, "--after-tax"))
        elif args.command == "author":
            result = author_calculate(amount(args.before_tax, "--before-tax"))
        elif args.command == "privilege":
            result = privilege_calculate(amount(args.before_tax, "--before-tax"))
        elif args.command == "reverse-privilege":
            result = reverse_privilege_calculate(amount(args.after_tax, "--after-tax"))
        elif args.command == "compensation":
            result = compensation_calculate(amount(args.before_tax, "--before-tax"),
                                            amount(args.avg_salary, "--avg-salary"))
    except ValueError as e:
        raise SystemExit(f"参数错误：{e}")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
