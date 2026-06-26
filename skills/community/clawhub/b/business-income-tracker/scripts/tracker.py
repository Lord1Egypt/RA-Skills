#!/usr/bin/env python3
# Income Tracker

def track_income(incomes, expenses):
    total_income = sum(i['amount'] for i in incomes)
    total_expense = sum(e['amount'] for e in expenses)
    roi = (total_income - total_expense) / total_expense if total_expense > 0 else 0
    return total_income, total_expense, roi

if __name__ == '__main__':
    incomes = [{'amount': 350}, {'amount': 499}]
    expenses = [{'amount': 100}]
    inc, exp, roi = track_income(incomes, expenses)
    print(f"收入：¥{inc}, 支出：¥{exp}, ROI: {roi:.1f}x")
