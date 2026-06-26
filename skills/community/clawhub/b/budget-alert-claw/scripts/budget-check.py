#!/usr/bin/env python3
"""
budget-check.sh 的 Python 实现
支持单笔校验、批量校验、报告生成

用法：
  python3 budget-check.py check --amount 50000 --department 市场部 --category 广告费 --budget-file budget.csv --expense-file expenses.csv
  python3 budget-check.py batch --input expenses.csv --budget-file budget.csv --output result.csv
  python3 budget-check.py report --budget-file budget.csv --expense-file expenses.csv --month 2026-03
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from collections import defaultdict


def load_budget(budget_file):
    """加载预算配置表"""
    budgets = {}
    with open(budget_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row.get('部门', ''), row.get('项目', ''), row.get('费用类别', ''))
            budgets[key] = {
                'total': float(row.get('预算总额', 0)),
                'threshold': float(row.get('预警阈值', 80)),
                'period': row.get('时间周期', '月度')
            }
    return budgets


def load_expenses(expense_file, month=None):
    """加载支出流水，可按月份过滤"""
    expenses = defaultdict(float)
    with open(expense_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_str = row.get('日期', '')
            if month and not date_str.startswith(month):
                continue
            key = (row.get('部门', ''), row.get('项目', ''), row.get('费用类别', ''))
            expenses[key] += float(row.get('金额', 0))
    return expenses


def check_single(amount, department, category, project, budgets, expenses):
    """单笔预算校验"""
    key = (department, project, category)
    # 尝试匹配（部门+项目+类别 → 部门+类别 → 全局兜底）
    budget_info = budgets.get(key) or budgets.get((department, '', category))
    
    if not budget_info:
        return {
            'status': 'no_budget',
            'message': f'未找到 {department}/{category} 的预算配置，默认放行并记录',
            'action': '放行（无预算配置）'
        }
    
    total = budget_info['total']
    threshold = budget_info['threshold']
    used = expenses.get(key, 0) or expenses.get((department, '', category), 0)
    available = total - used
    new_usage_rate = (used + amount) / total * 100 if total > 0 else 0
    
    if new_usage_rate >= 100:
        status = 'red'
        action = '🔴 拦截，需升级审批'
    elif new_usage_rate >= threshold:
        status = 'yellow'
        action = '🟡 通知负责人，允许通过'
    else:
        status = 'green'
        action = '🟢 自动通过'
    
    return {
        'status': status,
        'department': department,
        'category': category,
        'amount': amount,
        'budget_total': total,
        'used': used,
        'available': available,
        'usage_rate': round(new_usage_rate, 1),
        'action': action
    }


def cmd_check(args):
    budgets = load_budget(args.budget_file)
    expenses = load_expenses(args.expense_file) if args.expense_file else {}
    result = check_single(
        float(args.amount),
        args.department,
        args.category,
        getattr(args, 'project', ''),
        budgets,
        expenses
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_batch(args):
    budgets = load_budget(args.budget_file)
    expenses = load_expenses(args.expense_file) if args.expense_file else {}
    results = []
    with open(args.input, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            result = check_single(
                float(row.get('金额', 0)),
                row.get('部门', ''),
                row.get('费用类别', ''),
                row.get('项目', ''),
                budgets,
                expenses
            )
            result['申请人'] = row.get('申请人', '')
            result['日期'] = row.get('日期', '')
            results.append(result)
    
    # 输出结果
    if args.output:
        fieldnames = ['申请人', '日期', 'department', 'category', 'amount', 'usage_rate', 'status', 'action']
        with open(args.output, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(results)
        print(f'批量校验完成，结果已写入 {args.output}')
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))


def cmd_report(args):
    budgets = load_budget(args.budget_file)
    expenses = load_expenses(args.expense_file, month=args.month)
    
    report = []
    for key, budget_info in budgets.items():
        dept, proj, cat = key
        used = expenses.get(key, 0)
        total = budget_info['total']
        usage_rate = used / total * 100 if total > 0 else 0
        threshold = budget_info['threshold']
        
        if usage_rate >= 100:
            status = '🔴 超支'
        elif usage_rate >= threshold:
            status = '🟡 预警'
        else:
            status = '🟢 正常'
        
        report.append({
            '部门': dept, '项目': proj, '费用类别': cat,
            '预算总额': total, '已使用': used,
            '使用率': f'{usage_rate:.1f}%', '状态': status
        })
    
    # 按使用率降序排列
    report.sort(key=lambda x: float(x['使用率'].rstrip('%')), reverse=True)
    
    print(f"\n{'='*50}")
    print(f"预算执行报告 - {args.month or '全部'}")
    print(f"{'='*50}")
    for item in report:
        print(f"{item['状态']} {item['部门']}/{item['费用类别']}: {item['使用率']} (已用 {item['已使用']}元 / 总额 {item['预算总额']}元)")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='预算校验工具')
    subparsers = parser.add_subparsers(dest='command')
    
    # check 子命令
    p_check = subparsers.add_parser('check', help='单笔校验')
    p_check.add_argument('--amount', required=True)
    p_check.add_argument('--department', required=True)
    p_check.add_argument('--category', required=True)
    p_check.add_argument('--project', default='')
    p_check.add_argument('--budget-file', required=True)
    p_check.add_argument('--expense-file', default=None)
    
    # batch 子命令
    p_batch = subparsers.add_parser('batch', help='批量校验')
    p_batch.add_argument('--input', required=True)
    p_batch.add_argument('--budget-file', required=True)
    p_batch.add_argument('--expense-file', default=None)
    p_batch.add_argument('--output', default=None)
    
    # report 子命令
    p_report = subparsers.add_parser('report', help='生成报告')
    p_report.add_argument('--budget-file', required=True)
    p_report.add_argument('--expense-file', required=True)
    p_report.add_argument('--month', default=None, help='格式: 2026-03')
    
    args = parser.parse_args()
    
    if args.command == 'check':
        cmd_check(args)
    elif args.command == 'batch':
        cmd_batch(args)
    elif args.command == 'report':
        cmd_report(args)
    else:
        parser.print_help()
