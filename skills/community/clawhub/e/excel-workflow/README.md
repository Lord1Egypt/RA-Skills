# Excel Workflow Skill for OpenClaw

Complete Excel workflow with local processing, Google Drive sync, and formula preservation.

## What This Skill Does

- 📊 **Process Excel files** (.xlsx) with automatic analysis
- 🔄 **Preserve formulas** when updating cells (powered by openpyxl)
- ☁️ **Sync with Google Drive** for automatic backup
- 💾 **Track files** in SQLite database
- 🤖 **AI-ready** with natural language support

## Quick Example

```
User: [uploads sales.xlsx via Telegram]

Bot: ✅ Processed sales.xlsx!
     📊 2 sheets, 15 formulas
     ☁️ Uploaded to Google Drive

User: "What's the total revenue?"

Bot: Total Revenue: 650,000 руб
     - iPhone: 150,000
     - MacBook: 200,000
     - iPad: 300,000

User: "Change iPhone quantity to 20"

Bot: ✅ Updated! C2: 3 → 20
     New revenue: 1,000,000 руб
     Formulas recalculated automatically ✓
```

## Installation

See `SKILL.md` for complete installation instructions.

**Requirements:**
- Python 3.8+ with openpyxl
- rclone (for Google Drive)
- Google Drive account

## Upload to ClawHub

1. Go to https://clawhub.ai/upload
2. Upload `excel-workflow-1.0.0.zip`
3. Fill in details:
   - **Name:** Excel Workflow
   - **Description:** Complete Excel workflow with formula preservation and Google Drive sync
   - **Tags:** excel, spreadsheet, google-drive, formulas, data-analysis

## Features

✅ Formula preservation
✅ Google Drive backup
✅ Multi-file support
✅ Mass formula operations
✅ Natural language queries
✅ SQLite tracking
✅ Formatting preservation
✅ Chart support

## License

MIT License - see LICENSE.txt

## Version

1.0.0 (2026-02-20)
