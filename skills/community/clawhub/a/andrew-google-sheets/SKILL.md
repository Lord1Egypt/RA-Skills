---
name: andrew-google-sheets
description: Google Sheets API ì°ëì¼ë¡ ì¤íë ëìí¸ ì½ê¸°/ì°ê¸°, ìì±, í¬ë§·í ê´ë¦¬. OAuth 2.0 ì¸ì¦ ì¬ì©. ì¬ì©ìì êµ¬ê¸ ìí¸ìì ë°ì´í°ë¥¼ ì¡°ííê³  ìì í  ë ì¬ì©.
---

# Google Sheets

## Overview

Google Sheets API ë¥¼ íµí´ ì¬ì©ìì ì¤íë ëìí¸ë¥¼ ì¡°í, ìì , ìì±í  ì ìë ì¤í¬ìëë¤. OAuth 2.0 ì¸ì¦ì ì¬ì©íì¬ ìì íê² Google Sheets ì ì ê·¼í©ëë¤.

## Setup

### 1. OAuth í´ë¼ì´ì¸í¸ í¤ ì¤ì 

ì´ë¯¸ êµ¬ê¸ ìºë¦°ëì ëì¼í í¤ íì¼ì ì¬ì©í©ëë¤:

```bash
# í¤ íì¼ì´ ì´ë¯¸ ì¤ë¹ëì´ ìë¤ë©´ ìëµ
ls ~/.google-credentials.json
```

### 2. ìì¡´ì± ì¤ì¹

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 3. ì¸ì¦ íì¤í¸

```bash
cd /Users/andrew/.openclaw/workspace/skills/google-sheets
python3 scripts/oauth_setup.py
```

ì²« ì¤íì ë¸ë¼ì°ì ê° ì´ë¦¬ê³  Google ê³ì ì¼ë¡ ë¡ê·¸ì¸ í ê¶íì ë¶ì¬í´ì¼ í©ëë¤.

## Capabilities

### ì¤íë ëìí¸ ì½ê¸°

**ë°ì´í° ì¡°í:**
```
"ì¤íë ë ìí¸ 'ìë¬´ì¼ì§' ì ìµê·¼ 10 ì¤ ë³´ì¬ì¤"
"A1 ë¶í° D10 ê¹ì§ ë°ì´í° ì½ì´ì¤"
```

**í¹ì  ìí¸ ì¡°í:**
```
"'2026 ë 4 ì' ìí¸ì ëª¨ë  ë°ì´í° ë³´ì¬ì¤"
```

### ì¤íë ëìí¸ ì°ê¸°

**ë°ì´í° ì¶ê°:**
```
"ìë¬´ì¼ì§ ìí¸ì ì íëª© ì¶ê°: 'OpenClaw ì¤ì ', ììì¼ '2026-04-21', ìë£ì¼ '2026-04-21', ì§íì¨ '100%'"
```

**ë°ì´í° ìì :**
```
"ìë¬´ì¼ì§ì 6 ë²ì§¸ í ì§íì¨ì '100%' ë¡ ìë°ì´í¸í´ì¤"
```

### ì¤íë ëìí¸ ê´ë¦¬

**ì ì¤íë ëìí¸ ìì±:**
```
"ì ì¤íë ëìí¸ 'íë¡ì í¸ ê´ë¦¬' ë§ë¤ì´ì¤"
```

**ìí¸ ëª©ë¡ íì¸:**
```
"ë´ êµ¬ê¸ ìí¸ ëª©ë¡ ë³´ì¬ì¤"
```

## Usage Examples

### ìì 1: ì¤íë ëìí¸ ëª©ë¡ ì¡°í

```python
from scripts.sheets_ops import list_spreadsheets

# ì¬ì©ìì ëª¨ë  ì¤íë ëìí¸ ëª©ë¡
sheets = list_spreadsheets()
for sheet in sheets:
    print(f"{sheet['name']} - {sheet['spreadsheetId']}")
```

### ìì 2: í¹ì  ë²ì ì½ê¸°

```python
from scripts.sheets_ops import read_range

# í¹ì  ìí¸ì ë²ì ì½ê¸°
data = read_range('SPREADSHEET_ID', 'Sheet1!A1:D10')
for row in data:
    print(row)
```

### ìì 3: ë°ì´í° ì°ê¸°

```python
from scripts.sheets_ops import write_range

# í¹ì  ë²ìì ë°ì´í° ì°ê¸°
write_range(
    spreadsheet_id='SPREADSHEET_ID',
    range_name='Sheet1!A1:D1',
    values=[['ììëª', 'ììì¼', 'ìë£ì¼', 'ì§íì¨']]
)
```

### ìì 4: ë°ì´í° ì¶ê° (Append)

```python
from scripts.sheets_ops import append_rows

# ì í ì¶ê°
append_rows(
    spreadsheet_id='SPREADSHEET_ID',
    range_name='Sheet1!A:D',
    values=[['ì ìì', '2026-04-21', '', '0%']]
)
```

### ìì 5: ì ì¤íë ëìí¸ ìì±

```python
from scripts.sheets_ops import create_spreadsheet

# ì ì¤íë ëìí¸ ìì±
new_sheet = create_spreadsheet('ìë¬´ì¼ì§')
print(f"ìì± ìë£: {new_sheet['spreadsheetId']}")
```

## Files Structure

```
google-sheets/
âââ SKILL.md
âââ scripts/
    âââ oauth_setup.py      # OAuth 2.0 ì¸ì¦ ë° í í° ê´ë¦¬
    âââ sheets_ops.py       # Sheets API ì°ì° í¨ìë¤
```

## Security Notes

- OAuth í í°ì `~/.google-sheets-token.pickle` ì ì ì¥ë©ëë¤
- í´ë¼ì´ì¸í¸ í¤ë `~/.google-credentials.json` ì ì ì¥ë©ëë¤ (ìºë¦°ëì ê³µì )
- ì´ íì¼ë¤ì `.gitignore` ì ì¶ê°ëì´ì¼ í©ëë¤
- ê¶í ë²ì: `https://www.googleapis.com/auth/spreadsheets` (ì¤íë ëìí¸ ì ì²´ ì ê·¼)

## Troubleshooting

**"OAuth í´ë¼ì´ì¸í¸ í¤ íì¼ì´ ììµëë¤" ì¤ë¥:**
- `~/.google-credentials.json` íì¼ì´ ìëì§ íì¸
- êµ¬ê¸ ìºë¦°ë ì¤í¬ ì¤ì  ì ì´ë¯¸ ìì±í í¤ íì¼ìëë¤

**ì¸ì¦ ì¤í¨:**
- í í° íì¼ì ìì íê³  ì¬ì¸ì¦: `rm ~/.google-sheets-token.pickle`

**ê¶í ì¤ë¥:**
- ì¤í í° ìì  í ì¬ì¸ì¦: `rm ~/.google-sheets-token.pickle && python3 scripts/oauth_setup.py`

## Integration with Other Google Skills

Same OAuth credentials (`~/.google-credentials.json`) are shared with `google-calendar` and `google-tasks` skills, so you only need to authenticate once!
