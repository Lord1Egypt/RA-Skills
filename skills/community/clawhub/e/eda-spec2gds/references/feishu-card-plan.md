# Feishu Completion Card Plan

## Goal

When an EDA run completes, send a compact Feishu card summarizing:

- Project name
- Run status
- Key PPA metrics
- Preview image link or dashboard link
- Latest run path and artifact locations

## Card Sections

### 1. Header
- Project name
- Status badge: PASS / FAIL / RUNNING

### 2. KPI Block
- Utilization percentage
- Setup WNS (Worst Negative Slack)
- Total power consumption
- DRC/LVS error count

### 3. Links and Actions
- Dashboard detail page URL
- Preview image link
- Final GDS path (displayed as text)

### 4. Warning Block (Optional)
- Maximum slew violations
- Skipped KLayout DRC
- Missing signoff constraints

## Trigger Points

- Run completed successfully
- Run failed
- Run summary manually requested

## Implementation Notes

- Keep the card lightweight; the dashboard remains the deep-dive surface
- Use the dashboard URL as the primary click target
- Future enhancement: attach preview image as a separate image message if card image embedding proves awkward
