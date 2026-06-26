#!/usr/bin/env python3
"""
Find a merchant/subscription across all AccountantPriv databases.

Usage:
    uv run python find_merchant.py "נטפליקס"
    uv run python find_merchant.py "netflix"
    uv run python find_merchant.py "ארומה"
"""

import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime

# Database paths
BASE_DIR = Path("/Users/sharontourjeman/accountantpriv/output")
DB_PATHS = {
    "hapoalim": BASE_DIR / "hapoalim.db",
    "isracard": BASE_DIR / "isracard.db",
    "max": BASE_DIR / "max.db",
}


def search_in_db(db_name: str, db_path: Path, search_term: str) -> list[dict]:
    """Search for a merchant in a specific database."""
    if not db_path.exists():
        return []
    
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    results = []
    
    try:
        if db_name == "hapoalim":
            # Search in hapoalim_transactions
            cursor.execute("""
                SELECT date, description, charged_amount, account_number, category
                FROM hapoalim_transactions
                WHERE description LIKE ? OR description LIKE ?
                ORDER BY date DESC
                LIMIT 10
            """, (f"%{search_term}%", f"%{search_term.lower()}%"))
            
            for row in cursor.fetchall():
                results.append({
                    "source": "hapoalim",
                    "account": row["account_number"],
                    "date": row["date"],
                    "description": row["description"],
                    "amount": row["charged_amount"],
                    "category": row.get("category", ""),
                })
        
        elif db_name == "isracard":
            # Search in isracard_transactions
            cursor.execute("""
                SELECT card_name, date, description, billed_amount, category, billing_month
                FROM isracard_transactions
                WHERE description LIKE ? OR description LIKE ?
                ORDER BY date DESC
                LIMIT 10
            """, (f"%{search_term}%", f"%{search_term.lower()}%"))
            
            for row in cursor.fetchall():
                results.append({
                    "source": "isracard",
                    "card": row["card_name"],
                    "date": row["date"],
                    "description": row["description"],
                    "amount": row["billed_amount"],
                    "category": row.get("category", ""),
                    "billing_month": row.get("billing_month", ""),
                })
        
        elif db_name == "max":
            # Search in max_transactions
            cursor.execute("""
                SELECT account_number, date, description, charged_amount, category
                FROM max_transactions
                WHERE description LIKE ? OR description LIKE ?
                ORDER BY date DESC
                LIMIT 10
            """, (f"%{search_term}%", f"%{search_term.lower()}%"))
            
            for row in cursor.fetchall():
                results.append({
                    "source": "max",
                    "account": row["account_number"],
                    "date": row["date"],
                    "description": row["description"],
                    "amount": row["charged_amount"],
                    "category": row.get("category", ""),
                })
    
    except sqlite3.Error:
        pass  # Table might not exist
    
    conn.close()
    return results


def find_merchant(search_term: str) -> dict:
    """Search for a merchant across all databases."""
    all_results = {}
    
    for db_name, db_path in DB_PATHS.items():
        results = search_in_db(db_name, db_path, search_term)
        if results:
            all_results[db_name] = results
    
    return all_results


def format_results(results: dict) -> str:
    """Format search results as human-readable text."""
    if not results:
        return "לא נמצאו תוצאות."
    
    output = []
    
    for db_name, transactions in results.items():
        output.append(f"\n**{db_name.upper()}** ({len(transactions)} תוצאות):")
        
        for tx in transactions[:5]:  # Show top 5 per DB
            date = tx.get("date", "N/A")
            desc = tx.get("description", "N/A")
            amount = tx.get("amount", "N/A")
            
            if db_name == "isracard":
                card = tx.get("card", "N/A")
                category = tx.get("category", "")
                output.append(f"  • {date} | {card} | {desc} | ₪{amount} | {category}")
            elif db_name == "hapoalim":
                account = tx.get("account", "N/A")
                output.append(f"  • {date} | חשבון {account} | {desc} | ₪{amount}")
            else:  # max
                account = tx.get("account", "N/A")
                output.append(f"  • {date} | {account} | {desc} | ₪{amount}")
    
    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run python find_merchant.py <search_term>")
        print("Example: uv run python find_merchant.py נטפליקס")
        sys.exit(1)
    
    search_term = sys.argv[1]
    results = find_merchant(search_term)
    
    # Output as JSON for programmatic use
    print(json.dumps(results, indent=2, default=str, ensure_ascii=False))


if __name__ == "__main__":
    main()
