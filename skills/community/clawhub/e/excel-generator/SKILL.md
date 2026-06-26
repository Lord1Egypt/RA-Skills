---
name: excel-generator
description: Generate professional Bloomberg-style Excel workbooks from natural language descriptions. Creates multi-sheet workbooks with dashboards, KPI cards, charts, conditional formatting, and data tables. Use when asked to build Excel files, spreadsheets, dashboards, trackers, or reports.
---

# Excel Generator Skill

Generate professional, Bloomberg-terminal-aesthetic Excel workbooks using Python + openpyxl.

## When to Use
- User asks to build an Excel file, spreadsheet, dashboard, tracker, or report
- User wants to convert data into a formatted Excel workbook
- User needs a business template (inventory, finance, project tracking, HR, etc.)

## How to Use

### Step 1: Understand the Request
Ask (or infer) from the user:
- What type of workbook? (inventory, financial model, dashboard, tracker, etc.)
- What data/sheets are needed?
- Any specific metrics, KPIs, or calculations?

### Step 2: Generate the Workbook
Run the Python generator script:

```bash
cd /Users/synapsefirm/.openclaw/workspace && python3 scripts/excel_generator.py \
  --type "[workbook_type]" \
  --output "excel-projects/[filename].xlsx" \
  --title "[Title]"
```

Or write a custom Python script using openpyxl with the style constants below.

### Step 3: Style Constants (Bloomberg Aesthetic)
Always use these colors for consistency:
```python
NAVY       = "0D1B2A"   # Primary headers
NAVY_MID   = "1B3A5C"   # Sub-headers  
STEEL      = "2D5986"   # Accents
ICE        = "E8F0F8"   # Alternating rows
GOLD       = "C9A84C"   # Section dividers
GREEN_SAFE = "217346"   # OK/positive status
AMBER      = "B8560A"   # Warning status
CRIMSON    = "A50000"   # Danger/negative status
WHITE      = "FFFFFF"
```

### Step 4: Standard Sheet Structure
Every workbook should include:
1. **Dashboard** — KPI cards + summary table (always first sheet)
2. **Data sheets** — specific to the workbook type
3. **Raw Data** (if applicable) — source data tab

### Step 5: Deliver
- Save to `/Users/synapsefirm/.openclaw/workspace/excel-projects/[filename].xlsx`
- For client delivery: create a password-protected version with `Formly2026!` as default password
- Tell the user the file location and what's included

## Workbook Templates Available

### Inventory System
Sheets: Dashboard, Stock (with barcode input), Raw Materials, Projects, Deliveries, Suppliers, Offcuts, Analytics, Barcode Guide
Key features: Auto status formulas (✅ OK / ⚠️ LOW / 🔴 OUT), SUMIF analytics, conditional formatting

### Financial Dashboard  
Sheets: Dashboard, P&L, Cash Flow, Budget vs Actual, KPIs
Key features: Variance calculations, sparklines, YTD comparisons

### Project Tracker
Sheets: Dashboard, Tasks (Kanban), Timeline, Resources, Budget
Key features: RAG status, completion %, budget tracking

### HR/Headcount
Sheets: Dashboard, Roster, Org Chart data, Compensation, Time Off
Key features: Department rollups, cost calculations

### Sales Pipeline
Sheets: Dashboard, Pipeline, Won/Lost, Forecasting, Rep Performance
Key features: Weighted pipeline, close rate tracking

## Example Prompts This Skill Handles
- "Build me an inventory tracking spreadsheet"
- "Create a financial dashboard for my SaaS"
- "Make an Excel tracker for my construction projects"
- "I need a sales pipeline spreadsheet"
- "Generate a HR headcount report template"

## Output Quality Standards
- Minimum 3 sheets per workbook
- Always include a Dashboard as Sheet 1
- Freeze panes on all data sheets
- Alternating row colors (ICE/WHITE)
- Bold navy headers with white text
- All number columns right-aligned with proper formatting ($, %, commas)
- Column widths sized to content
