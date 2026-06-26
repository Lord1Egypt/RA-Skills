#!/usr/bin/env python3
"""
Get monthly financial summary from AccountantPriv databases.

Usage:
    uv run python monthly_summary.py --month 03/2026
    uv run python monthly_summary.py --month 03/2026 --json
"""

import argparse
import sqlite3
import json
from pathlib import Path
from datetime import datetime

# Database paths
BASE_DIR = Path("/Users/sharontourjeman/accountantpriv/output")
DB_PATHS = {
    "hapoalim": BASE_DIR / "hapoalim.db",
    "isracard": BASE_DIR / "isracard.db",
    "max": BASE_DIR / "max.db",
}

# Card bill descriptions in Hapoalim (to exclude from expenses)
CARD_BILL_DESCRIPTIONS = ["ישראכרט", "מסטרקרד", "מקס"]


def parse_month(month_str: str) -> tuple[str, str]:
    """Parse MM/YYYY to YYYY-MM format."""
    parts = month_str.split("/")
    return f"{parts[1]}-{parts[0]}", f"{parts[1]}-{parts[0].zfill(2)}"


def get_hapoalim_summary(db_path: Path, year: str, month: str) -> dict:
    """Get Hapoalim bank summary for a month."""
    if not db_path.exists():
        return {"income": 0, "expenses": 0, "card_bills": 0, "transactions_count": 0}
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    month_pattern = f"{year}-{month.zfill(2)}%"
    
    # Income (positive amounts)
    cursor.execute("""
        SELECT SUM(charged_amount) as total
        FROM hapoalim_transactions
        WHERE date LIKE ? AND charged_amount > 0
    """, (month_pattern,))
    income = cursor.fetchone()[0] or 0
    
    # Expenses excluding card bills
    placeholders = ",".join("?" * len(CARD_BILL_DESCRIPTIONS))
    cursor.execute(f"""
        SELECT SUM(charged_amount) as total
        FROM hapoalim_transactions
        WHERE date LIKE ? 
          AND charged_amount < 0
          AND description NOT LIKE '%ישראכרט%'
          AND description NOT LIKE '%מסטרקרד%'
          AND description NOT LIKE '%מקס%'
    """, (month_pattern,))
    expenses = cursor.fetchone()[0] or 0
    
    # Card bills only
    cursor.execute(f"""
        SELECT SUM(charged_amount) as total
        FROM hapoalim_transactions
        WHERE date LIKE ?
          AND (description LIKE '%ישראכרט%' 
               OR description LIKE '%מסטרקרד%' 
               OR description LIKE '%מקס%')
    """, (month_pattern,))
    card_bills = cursor.fetchone()[0] or 0
    
    # Transaction count
    cursor.execute("""
        SELECT COUNT(*) FROM hapoalim_transactions WHERE date LIKE ?
    """, (month_pattern,))
    count = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "income": round(income, 2),
        "expenses": round(expenses, 2),
        "card_bills": round(card_bills, 2),
        "transactions_count": count,
    }


def get_isracard_summary(db_path: Path, billing_month: str) -> dict:
    """Get Isracard summary for a billing month."""
    if not db_path.exists():
        return {"total": 0, "by_category": {}, "transactions_count": 0}
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Total spending
    cursor.execute("""
        SELECT SUM(billed_amount) as total
        FROM isracard_transactions
        WHERE billing_month = ?
    """, (billing_month,))
    total = cursor.fetchone()[0] or 0
    
    # By category
    cursor.execute("""
        SELECT category, SUM(billed_amount) as total
        FROM isracard_transactions
        WHERE billing_month = ?
        GROUP BY category
        ORDER BY total DESC
    """, (billing_month,))
    by_category = {row[0]: round(row[1], 2) for row in cursor.fetchall()}
    
    # Transaction count
    cursor.execute("""
        SELECT COUNT(*) FROM isracard_transactions WHERE billing_month = ?
    """, (billing_month,))
    count = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total": round(total, 2),
        "by_category": by_category,
        "transactions_count": count,
    }


def get_max_summary(db_path: Path, year: str, month: str) -> dict:
    """Get Max card summary for a month."""
    if not db_path.exists():
        return {"total": 0, "transactions_count": 0}
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    month_pattern = f"{year}-{month.zfill(2)}%"
    
    # Total spending
    cursor.execute("""
        SELECT SUM(charged_amount) as total
        FROM max_transactions
        WHERE date LIKE ?
    """, (month_pattern,))
    total = cursor.fetchone()[0] or 0
    
    # Transaction count
    cursor.execute("""
        SELECT COUNT(*) FROM max_transactions WHERE date LIKE ?
    """, (month_pattern,))
    count = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total": round(total, 2),
        "transactions_count": count,
    }


def monthly_summary(month_str: str) -> dict:
    """Get complete monthly summary."""
    billing_month, _ = parse_month(month_str)
    year, month = month_str.split("/")
    
    summary = {
        "month": month_str,
        "billing_month": billing_month,
        "hapoalim": get_hapoalim_summary(DB_PATHS["hapoalim"], year, month),
        "isracard": get_isracard_summary(DB_PATHS["isracard"], billing_month),
        "max": get_max_summary(DB_PATHS["max"], year, month),
    }
    
    # Calculate totals
    summary["total_income"] = summary["hapoalim"]["income"]
    summary["total_bank_expenses"] = abs(summary["hapoalim"]["expenses"])
    summary["total_card_bills"] = abs(summary["hapoalim"]["card_bills"])
    summary["total_isracard"] = abs(summary["isracard"]["total"])
    summary["total_max"] = abs(summary["max"]["total"])
    
    # Net = income + expenses (negative) + card_bills (negative)
    summary["net"] = (
        summary["total_income"]
        + summary["hapoalim"]["expenses"]
        + summary["hapoalim"]["card_bills"]
    )
    
    return summary


def format_summary(summary: dict) -> str:
    """Format summary as human-readable text."""
    lines = [
        f"📊 **סיכום חודשי: {summary['month']}**",
        "",
        f"**הכנסות:** ₪{summary['total_income']:,.2f}",
        f"**הוצאות בנק (לא כולל כרטיסים):** ₪{summary['total_bank_expenses']:,.2f}",
        f"**תשלומי כרטיסים (ביחד):** ₪{summary['total_card_bills']:,.2f}",
        f"  - ישראכרט: ₪{summary['total_isracard']:,.2f}",
        f"  - מקס: ₪{summary['total_max']:,.2f}",
        "",
        f"**סה״כ הוצאות:** ₪{summary['total_bank_expenses'] + summary['total_card_bills']:,.2f}",
        f"**נטו:** ₪{summary['net']:,.2f}",
    ]
    
    if summary["isracard"]["by_category"]:
        lines.append("")
        lines.append("**הוצאות ישראכרט לפי קטגוריה:**")
        for cat, amount in list(summary["isracard"]["by_category"].items())[:5]:
            lines.append(f"  • {cat}: ₪{amount:,.2f}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Monthly financial summary")
    parser.add_argument("--month", required=True, help="Month in MM/YYYY format")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    summary = monthly_summary(args.month)
    
    if args.json:
        print(json.dumps(summary, indent=2, default=str))
    else:
        print(format_summary(summary))


if __name__ == "__main__":
    main()
