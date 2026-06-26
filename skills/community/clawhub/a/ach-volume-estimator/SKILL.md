---
name: ach-volume-estimator
description: Estimate Dwolla's end-of-month ACH transaction volume from daily KPI emails. Use when processing ACH KPI emails, when Dave asks about monthly volume projections, or when the daily ACH cron needs a monthly estimate. Extracts transactions and business days from email data, calculates per-BD rate, and projects monthly total using US Federal Reserve bank holiday calendar.
---

# ACH Monthly Volume Estimator

## Workflow

1. **Fetch the ACH KPI email:**
   ```bash
   gog gmail messages search "subject:ACH KPIs" --account glaser.dave@gmail.com --max 1 --json
   ```

2. **Download the PDF attachment** (contains all charts and data):
   ```bash
   # Get message details with attachment IDs
   gog gmail get <MESSAGE_ID> --account glaser.dave@gmail.com --json
   # Find the attachment named "ACH KPIs.pdf" (mimeType: application/pdf)
   # Download it:
   gog gmail attachment <MESSAGE_ID> <ATTACHMENT_ID> --account glaser.dave@gmail.com --out ~/clawd/work/ach-kpis-latest.pdf
   ```

3. **Extract data from the PDF.** The PDF contains Tableau dashboard exports with:
   - ACH Transactions chart: MoM bar chart with monthly totals, per-BD averages, 5/20/60-day comparisons
   - Client Growth charts (10K and 5K thresholds)
   - Top 60 Clients tables (60-day and 20-day comparisons)
   
   Key numbers to extract:
   - Current month transaction total (partial, from MoM bar chart)
   - Business days elapsed (derive from date range in "Prev. 20 Days" row or count from month start to report date)
   - YTD avg transactions per business day
   - SPLY monthly total for comparison

4. **Run the estimator:**
   ```bash
   python3 ~/clawd/skills/ach-volume-estimator/scripts/estimate.py \
     --transactions <MTD_TOTAL> --bds-elapsed <BDS_SO_FAR> [--month YYYY-MM]
   ```
   Or if you already have per-BD rate:
   ```bash
   python3 ~/clawd/skills/ach-volume-estimator/scripts/estimate.py \
     --per-bd <RATE> [--month YYYY-MM]
   ```
   Add `--json` for structured output.

5. **Compare to benchmarks:**
   - Jan 2026 actual: 6.12M (20 BDs, 305K/BD)
   - Dec 2025 actual: 6.41M (22 BDs, 291K/BD)
   - SPLY from the PDF MoM chart

6. **Generate the visual dashboard:**
   ```bash
   ~/clawd/scripts/ach-dashboard-gen
   ```
   This reads `~/clawd/work/ach-reports/latest-ach-data.json` (or falls back to the latest markdown report) and writes `~/clawd/work/ach-reports/dashboard.html`.
   View at: http://192.168.1.60:3013/html/work/ach-reports/dashboard.html
   TV mode: http://192.168.1.60:3013/html/work/ach-reports/dashboard.html?tv=1

7. **Deliver:** Include estimate in the ACH KPI summary sent to Dave. Include the dashboard URL.

## Output Format

One-liner: `2026-02 estimate: 5.81M txns | (19 BDs, 12 elapsed, 7 remaining) | 306,000/BD | (3,672,000 so far)`

## Business Day Calendar

Script uses US Federal Reserve bank holiday calendar (2025-2027 hardcoded). Excludes weekends and all Fed holidays (New Year's, MLK, Presidents' Day, Memorial Day, Juneteenth, Independence Day, Labor Day, Columbus Day, Veterans Day, Thanksgiving, Christmas).

## Integration

Wire into the existing "Daily ACH KPIs summary to Dave" cron (9:30 AM ET weekdays). After extracting email data, run the estimator and append the monthly projection to Dave's summary.
