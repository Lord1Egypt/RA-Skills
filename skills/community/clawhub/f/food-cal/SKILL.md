---
name: food-cal
description: Food expiration calculator. Use when user wants to check if a food product has expired based on production/purchase date and shelf life. Calculates expiration date and tells user if food is still good, expired, or close to expiration.
category: daily life tool
contact: googcheng@qq.com
---

# Food Expiration Calculator

This skill calculates whether a food product has expired based on the product date and shelf life.

## Usage

User provides:
- **Product date**: The production date, manufacture date, or purchase date (format: YYYY-MM-DD)
- **Shelf life**: How long the product lasts (e.g., "6 months", "2 years", "18 months")

## Output

The calculator returns:
- Expiration date
- Days remaining until expiration (or days since expiration)
- Status: "Fresh" (more than 30 days left), "Expiring Soon" (less than 30 days), or "Expired"

## Script

Use the Python script `scripts/food_expiry.py` to calculate:

```bash
python scripts/food_expiry.py --date 2025-06-01 --shelf-life "6 months"
```

Arguments:
- `--date` or `-d`: Product date (YYYY-MM-DD)
- `--shelf-life` or `-s`: Shelf life (e.g., "6 months", "2 years", "18 days")

The script outputs the expiration date, days remaining, and status.
