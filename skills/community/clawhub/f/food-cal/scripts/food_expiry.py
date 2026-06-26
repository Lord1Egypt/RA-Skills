#!/usr/bin/env python3
"""
Food Expiration Calculator
Calculate if a food product has expired based on product date and shelf life.
"""

import argparse
from datetime import datetime, timedelta
import re


def parse_shelf_life(shelf_life_str: str) -> timedelta:
    """Parse shelf life string like '6 months', '2 years', '18 days'."""
    shelf_life_str = shelf_life_str.lower().strip()
    
    # Pattern to match number and unit
    pattern = r'(\d+)\s*(day|days|month|months|year|years)'
    match = re.search(pattern, shelf_life_str)
    
    if not match:
        raise ValueError(f"Invalid shelf life format: '{shelf_life_str}'. Use format like '6 months', '2 years', '18 days'")
    
    value = int(match.group(1))
    unit = match.group(2)
    
    if 'year' in unit:
        return timedelta(days=value * 365)
    elif 'month' in unit:
        # Approximate month as 30 days
        return timedelta(days=value * 30)
    else:
        return timedelta(days=value)


def calculate_expiry(product_date: str, shelf_life_str: str):
    """Calculate expiration date and status."""
    # Parse product date
    try:
        date_obj = datetime.strptime(product_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: '{product_date}'. Use YYYY-MM-DD")
    
    # Parse shelf life
    shelf_timedelta = parse_shelf_life(shelf_life_str)
    
    # Calculate expiration date
    expiry_date = date_obj + shelf_timedelta
    
    # Calculate days remaining
    today = datetime.now()
    days_remaining = (expiry_date - today).days
    
    # Determine status
    if days_remaining < 0:
        status = "EXPIRED"
        status_detail = f"Expired {abs(days_remaining)} days ago"
    elif days_remaining <= 30:
        status = "EXPIRING SOON"
        status_detail = f"{days_remaining} days remaining"
    else:
        status = "FRESH"
        status_detail = f"{days_remaining} days remaining"
    
    # Output results
    print(f"\n{'='*40}")
    print(f"Food Expiration Calculator")
    print(f"{'='*40}")
    print(f"Product Date:    {date_obj.strftime('%Y-%m-%d')}")
    print(f"Shelf Life:      {shelf_life_str}")
    print(f"Expiration Date: {expiry_date.strftime('%Y-%m-%d')}")
    print(f"{'='*40}")
    print(f"Status: {status}")
    print(f"{status_detail}")
    print(f"{'='*40}\n")
    
    return {
        "product_date": date_obj.strftime('%Y-%m-%d'),
        "shelf_life": shelf_life_str,
        "expiration_date": expiry_date.strftime('%Y-%m-%d'),
        "days_remaining": days_remaining,
        "status": status,
        "status_detail": status_detail
    }


def main():
    parser = argparse.ArgumentParser(description="Food Expiration Calculator")
    parser.add_argument("-d", "--date", required=True, help="Product date (YYYY-MM-DD)")
    parser.add_argument("-s", "--shelf-life", required=True, help="Shelf life (e.g., '6 months', '2 years', '18 days')")
    
    args = parser.parse_args()
    
    try:
        calculate_expiry(args.date, args.shelf_life)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
