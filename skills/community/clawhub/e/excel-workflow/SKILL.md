---
name: excel-workflow
description: |
  Complete Excel workflow with local file processing, Google Drive sync, and formula preservation.
  Process Excel files (.xlsx), track changes in SQLite, sync with Google Drive, and preserve formulas during updates.
  Use this skill when users want to upload Excel files, query data, update cells while preserving formulas, or sync with Google Drive.
compatibility: Requires Python 3.8+, openpyxl, rclone, and Google Drive OAuth setup
metadata:
  author: alexey
  version: "1.0.0"
  openclaw:
    emoji: 🔄
    requires:
      bins:
        - rclone
        - python3
      env:
        - OPENCLAW_EXCEL_PATH
---

# Excel Workflow

Complete workflow for Excel file management with local processing, Google Drive backup, formula preservation, and SQLite tracking.

## Features

- ✅ **Formula Preservation** — Update cells without losing formulas (powered by openpyxl)
- ✅ **Google Drive Sync** — Automatic backup to Google Drive using rclone
- ✅ **SQLite Tracking** — Track all files, formulas, and metadata in local database
- ✅ **Multi-file Support** — Work with multiple Excel files simultaneously
- ✅ **Data Analysis** — Query data, read formulas, and analyze structure
- ✅ **Mass Operations** — Create formulas for entire columns at once

## Quick Start

### 1. Upload Excel File

Simply drop an `.xlsx` file into the chat. The workflow automatically:
1. Analyzes file structure (sheets, formulas)
2. Uploads to Google Drive (`gdrive:Excel/`)
3. Saves metadata to SQLite tracker

```bash
# Manual processing
~/.openclaw/tools/openclaw-excel/excel-workflow process /path/to/file.xlsx
```

### 2. Query Data

```bash
# Ask questions about your data
~/.openclaw/tools/openclaw-excel/excel-workflow query "what is total revenue?" --file sales.xlsx
```

### 3. Update Cells (Formulas Preserved!)

```bash
# Update values - formulas stay intact
~/.openclaw/tools/openclaw-excel/excel-workflow update '{"C2": 100}' --file sales.xlsx

# Update formulas
~/.openclaw/tools/openclaw-excel/excel-workflow update '{"D2": "=B2*C2*1.5"}' --file sales.xlsx
```

## Installation

### Prerequisites

1. **Python 3.8+** with openpyxl
2. **rclone** for Google Drive integration
3. **Google Drive** account

### Step 1: Install Dependencies

```bash
# Install rclone (macOS)
brew install rclone

# Python packages (installed in venv automatically)
pip install openpyxl
```

### Step 2: Setup Google Drive

```bash
# Configure rclone with Google Drive
rclone config
```

Follow prompts:
- Name: `gdrive`
- Storage: `drive` (Google Drive)
- Scope: `1` (Full access)
- Auto config: `y` (opens browser for OAuth)

Verify:
```bash
rclone lsd gdrive:
```

### Step 3: Create Excel Folder

```bash
rclone mkdir gdrive:Excel/
```

### Step 4: Install Skill Files

The skill consists of 3 components:

1. **Excel CLI** (`~/.openclaw/tools/openclaw-excel/excel`)
   - Commands: `info`, `read`, `update`, `show-formulas`, `get-cell`

2. **Tracker CLI** (`~/.openclaw/tools/openclaw-excel/excel-tracker`)
   - SQLite database at `~/.openclaw/excel_tracker.db`
   - Commands: `add`, `get-latest`, `search`, `list`, `stats`

3. **Workflow Orchestrator** (`~/.openclaw/tools/openclaw-excel/excel-workflow`)
   - Commands: `process`, `query`, `update`, `list`, `stats`

See [Installation Guide](https://github.com/your-repo/excel-workflow) for detailed setup.

## Commands

### Process Command

Analyze file, upload to Drive, and save to tracker:

```bash
excel-workflow process /path/to/file.xlsx [--telegram-id ID]
```

**Output:**
```json
{
  "status": "success",
  "filename": "sales.xlsx",
  "file_id": 1,
  "drive_url": "gdrive:Excel/sales.xlsx",
  "analysis": {
    "sheets": 2,
    "formulas": 15,
    "sheet_names": ["Sales", "Summary"]
  },
  "message": "✅ File processed successfully!"
}
```

### Query Command

Read data and answer questions:

```bash
excel-workflow query "show me the data" [--file filename.xlsx]
```

**Output:**
```json
{
  "filename": "sales.xlsx",
  "file_id": 1,
  "sheets": ["Sales", "Summary"],
  "data": [
    [
      {"address": "A1", "value": "Product", "type": "str"},
      {"address": "B1", "value": "Price", "type": "int"}
    ]
  ],
  "formulas": [
    {"cell": "D2", "formula": "=B2*C2"}
  ],
  "question": "show me the data",
  "context": {
    "sheet_count": 2,
    "formula_count": 15,
    "uploaded_at": "2026-02-20 10:30:00"
  }
}
```

### Update Command

Update cells (values or formulas):

```bash
# Update values
excel-workflow update '{"C2": 100, "C3": 200}' [--file filename.xlsx]

# Update formulas
excel-workflow update '{"D2": "=B2*C2*1.5"}' --file sales.xlsx

# Mass update - create formulas for entire column
excel-workflow update '{"D2": "=B2*0.5", "D3": "=B3*0.5", ...}' --file data.xlsx
```

**Output:**
```json
{
  "status": "success",
  "filename": "sales.xlsx",
  "updated": 2,
  "changes": [
    {"cell": "C2", "old_value": 50, "new_value": 100},
    {"cell": "C3", "old_value": 75, "new_value": 200}
  ],
  "message": "✅ Updated and re-uploaded to Google Drive"
}
```

### List Command

Show tracked files:

```bash
excel-workflow list [--limit 10]
```

**Output:**
```json
[
  {
    "id": 2,
    "original_filename": "sales_2026.xlsx",
    "sheet_count": 2,
    "formula_count": 15,
    "uploaded_at": "2026-02-20 14:20:00"
  },
  {
    "id": 1,
    "original_filename": "budget.xlsx",
    "sheet_count": 3,
    "formula_count": 42,
    "uploaded_at": "2026-02-19 09:15:30"
  }
]
```

### Stats Command

Show statistics:

```bash
excel-workflow stats
```

**Output:**
```json
{
  "total_files": 5,
  "files_on_drive": 5,
  "total_sheets": 12,
  "total_formulas": 87
}
```

## Usage Patterns for AI Agents

### Pattern 1: User Uploads Excel File

**User action:** Uploads `sales.xlsx` via Telegram

**Agent workflow:**
1. File saved to temporary location by Telegram handler
2. Detect `.xlsx` extension
3. Run: `excel-workflow process /path/to/sales.xlsx --telegram-id <id>`
4. Parse JSON result and respond:

```
Agent: "✅ I've received and processed sales.xlsx!

📊 Analysis:
- 2 sheets: Sales, Summary
- 15 formulas detected
- ☁️ Uploaded to Google Drive

What would you like to know about this file?"
```

### Pattern 2: User Asks Question

**User:** "What's the total revenue in my sales file?"

**Agent workflow:**
1. Run: `excel-workflow query "what is total revenue?" --file sales.xlsx`
2. Receive data with all rows and formulas
3. Analyze the data to find revenue-related columns and totals
4. Respond with answer:

```
Agent: "Looking at your sales.xlsx file:

Total Revenue: 650,000 руб

Breakdown:
- iPhone: 150,000 (3 × 50,000)
- MacBook: 200,000 (2 × 100,000)
- iPad: 300,000 (5 × 60,000)

The file has a SUM formula in cell D5 that calculates this automatically."
```

### Pattern 3: User Requests Update

**User:** "Change iPhone quantity to 20"

**Agent workflow:**
1. Query to understand structure: `excel-workflow query "find iPhone row"`
2. Identify that iPhone is in row 2, quantity in column C
3. Run: `excel-workflow update '{"C2": 20}' --file sales.xlsx`
4. Confirm update:

```
Agent: "✅ Updated sales.xlsx:

Changed C2 (iPhone quantity): 3 → 20

New revenue for iPhone: 1,000,000 руб (was 150,000)
Total revenue updated automatically thanks to formulas!

File has been re-uploaded to Google Drive."
```

### Pattern 4: Mass Formula Creation

**User:** "Create a column that multiplies price by 0.5 for all products"

**Agent workflow:**
1. Read file to determine row count
2. Generate update JSON with formulas for each row
3. Run: `excel-workflow update '{"D2": "=B2*0.5", "D3": "=B3*0.5", ...}' --file prices.xlsx`
4. Confirm:

```
Agent: "✅ Created formulas for 50 rows!

Column D now contains =B*0.5 formula for all products.
File updated on Google Drive."
```

## Technical Details

### Components

1. **Excel CLI** — openpyxl-based tool for reading/writing Excel files
   - Preserves formulas using `data_only=False`
   - Commands: `read`, `update`, `info`, `show-formulas`, `get-cell`

2. **Tracker** — SQLite database for file metadata
   - Location: `~/.openclaw/excel_tracker.db`
   - Tracks: filename, sheets, formulas, paths, timestamps

3. **Workflow Orchestrator** — Integrates Excel CLI, rclone, and tracker
   - Orchestrates: analyze → upload → track → update cycle
   - Progress messages to stderr, JSON results to stdout

### File Locations

- **Tracker database:** `~/.openclaw/excel_tracker.db`
- **Google Drive folder:** `gdrive:Excel/`
- **Local files:** User-specified paths (Telegram downloads to `~/.openclaw/media/`)

### Formula Preservation

**How it works:**
- openpyxl loads workbooks with `data_only=False`
- Formulas stored as text strings (e.g., `"=B2*C2"`)
- When updating cell with formula string, openpyxl preserves it
- Excel recalculates formulas when file is opened

**Example:**
```python
# This preserves formulas
ws['D2'] = '=B2*C2'  # Formula remains
ws['B2'] = 100       # Data changes, formula in D2 recalculates
```

### What's Preserved vs Not Preserved

**✅ Preserved:**
- Formulas (=SUM, =IF, =B2*C2, etc.)
- Data (numbers, text, dates)
- Structure (sheets, tables)
- Formatting (colors, fonts, borders, bold)
- Charts (diagrams update automatically)

**⚠️ May Not Work:**
- Conditional formatting (complex rules)
- Macros (.xlsm files not supported)
- Pivot tables (may break)
- Slicers and advanced filters

## Error Handling

**Common errors:**

1. **File not found**
   ```json
   {"error": "File not found: /path/to/file.xlsx"}
   ```

2. **Google Drive not configured**
   ```json
   {"error": "rclone remote 'gdrive' not configured"}
   ```
   Solution: Run `rclone config`

3. **Formula syntax error**
   ```json
   {"error": "Invalid formula: =B2*"}
   ```
   Solution: Check formula syntax

4. **Database locked**
   ```json
   {"error": "Database is locked"}
   ```
   Solution: Wait and retry

## Examples

### Example 1: Financial Data Analysis

```bash
# Upload stock data
excel-workflow process ~/Desktop/ARKK.xlsx

# Query
excel-workflow query "show last 10 rows" --file ARKK.xlsx

# Add calculated column (50% of price)
# First, find row count, then generate formulas
excel-workflow update '{"C2": "=B2*0.5", "C3": "=B3*0.5", ...}' --file ARKK.xlsx
```

### Example 2: Price List Update

```bash
# Process price list
excel-workflow process prices.xlsx

# Update prices
excel-workflow update '{"B10": 99.99, "B11": 149.99}' --file prices.xlsx

# Add tax column
excel-workflow update '{"D2": "=B2*1.2"}' --file prices.xlsx
```

### Example 3: Multiple Files

```bash
# Upload multiple files
excel-workflow process january.xlsx
excel-workflow process february.xlsx

# List all files
excel-workflow list

# Query specific file
excel-workflow query "total sales" --file january.xlsx

# Stats
excel-workflow stats
```

## Troubleshooting

### Issue: "rclone not found"

```bash
# Install rclone
brew install rclone  # macOS
sudo apt install rclone  # Linux
```

### Issue: "openpyxl not installed"

```bash
# Install in virtual environment
cd ~/.openclaw/tools/openclaw-excel
python3 -m venv venv
./venv/bin/pip install openpyxl
```

### Issue: "Google Drive permission denied"

```bash
# Reconfigure rclone
rclone config
# Delete old gdrive remote and create new one
```

### Issue: "Formulas become values"

**This should NOT happen!** If it does:
1. Check that `excel` CLI uses `data_only=False` when loading workbook
2. Ensure formula strings start with `=`
3. Verify openpyxl version: `pip show openpyxl` (should be 3.1.0+)

## Best Practices

### For Users

1. **Name files descriptively**
   - Good: `sales_2026_Q1.xlsx`
   - Bad: `Book1.xlsx`

2. **Ask specific questions**
   - Good: "What's the total revenue in January?"
   - Bad: "Tell me about the file"

3. **Keep file structure consistent**
   - Makes it easier for AI to understand

### For Developers

1. **Always check file existence** before processing
2. **Use sessions** for multiple operations on same file
3. **Handle errors gracefully** with try/except
4. **Show progress** in stderr, results in stdout
5. **Validate formulas** before updating cells

## API Reference

See [Excel CLI Documentation](./excel_cli.md) and [Tracker Documentation](./tracker.md) for detailed API reference.

## Resources

- [openpyxl Documentation](https://openpyxl.readthedocs.io/)
- [rclone Documentation](https://rclone.org/docs/)
- [Microsoft Excel File Format](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-xlsx/)
- [Google Drive with rclone](https://rclone.org/drive/)

## Support

- GitHub Issues: [your-repo/excel-workflow/issues]
- Documentation: [your-repo/excel-workflow/docs]
- Community: [OpenClaw Community]

## License

MIT License - see LICENSE.txt

## Changelog

### Version 1.0.0 (2026-02-20)

- Initial release
- Formula preservation with openpyxl
- Google Drive sync via rclone
- SQLite tracking
- Multi-file support
- Mass formula operations
- AI agent integration patterns
