---
name: divorce
description: Divorce process support with financial inventory, legal preparation, and emotional guidance. Use when user mentions divorce, separation, custody, asset division, or divorce proceedings. Helps organize financial documents, understand process options, prepare for attorney meetings, track deadlines, and navigate parenting plans. NEVER provides legal advice.
---

# Divorce

Divorce navigation system. Organization through transition.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All divorce data stored locally only**: `memory/divorce/`
- **Highest privacy protection** - sensitive personal information
- **No external sharing** of any kind
- **Encrypted storage recommended** (file system level)
- User controls all data retention and deletion

### Safety Boundaries
- ✅ Organize financial documents
- ✅ Explain process types (mediation, collaborative, litigation)
- ✅ Prepare for attorney meetings
- ✅ Track deadlines and requirements
- ❌ **NEVER provide legal advice**
- ❌ **NEVER replace** licensed family law attorneys
- ❌ **NEVER guarantee** specific outcomes

### Important Note
Divorce involves significant legal and financial consequences. This skill provides organizational support only. Always work with a licensed family law attorney for legal guidance.

### Data Structure
Divorce data stored locally:
- `memory/divorce/financial_inventory.json` - Complete financial picture
- `memory/divorce/documents.json` - Document organization
- `memory/divorce/process.json` - Process type and timeline
- `memory/divorce/attorney_prep.json` - Attorney meeting preparation
- `memory/divorce/parenting_plan.json` - Custody and parenting details
- `memory/divorce/deadlines.json` - Critical deadlines

## Core Workflows

### Financial Inventory
```
User: "Help me organize my financial documents"
→ Use scripts/financial_inventory.py
→ Build complete inventory of assets, debts, accounts, property
```

### Choose Process Type
```
User: "Should I mediate or go to court?"
→ Use scripts/compare_process.py --situation "amicable but complex assets"
→ Explain mediation, collaborative, litigation options
```

### Prepare for Attorney
```
User: "Prep me for my first attorney meeting"
→ Use scripts/prep_attorney.py
→ Organize financial summary, questions, goals
```

### Track Parenting Plan
```
User: "Help me think through custody arrangements"
→ Use scripts/parenting_plan.py
→ Work through physical custody, legal custody, schedules, logistics
```

### Monitor Deadlines
```
User: "What deadlines do I have coming up?"
→ Use scripts/check_deadlines.py
→ Show disclosure deadlines, court dates, response requirements
```

## Module Reference
- **Process Types**: See [references/process-types.md](references/process-types.md)
- **Financial Inventory**: See [references/financial-inventory.md](references/financial-inventory.md)
- **Attorney Preparation**: See [references/attorney-prep.md](references/attorney-prep.md)
- **Parenting Plans**: See [references/parenting-plans.md](references/parenting-plans.md)
- **Custody Framework**: See [references/custody.md](references/custody.md)
- **Emotional Support**: See [references/emotional-support.md](references/emotional-support.md)

## Scripts Reference
| Script | Purpose |
|--------|---------|
| `financial_inventory.py` | Build financial inventory |
| `compare_process.py` | Compare divorce process options |
| `prep_attorney.py` | Prepare for attorney meeting |
| `parenting_plan.py` | Develop parenting plan |
| `check_deadlines.py` | Track critical deadlines |
| `log_document.py` | Log gathered document |
| `track_expense.py` | Track divorce-related expenses |
| `self_care_check.py` | Emotional wellbeing check-in |
