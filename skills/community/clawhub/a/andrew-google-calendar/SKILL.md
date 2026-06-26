---
name: andrew-google-calendar
description: Google Calendar API ì°ëì¼ë¡ ì¼ì  ì¡°í, ìì±, ìì , ìì  ê´ë¦¬. OAuth 2.0 ì¸ì¦ ì¬ì©. ì¬ì©ìì ê°ì¸ ìºë¦°ëìì ì¼ì ì íì¸íê³  ê´ë¦¬í  ë ì¬ì©.
---

# Google Calendar

## Overview

Google Calendar API ë¥¼ íµí´ ì¬ì©ìì ì¼ì ì ì¡°í, ìì±, ìì , ìì í  ì ìë ì¤í¬ìëë¤. OAuth 2.0 ì¸ì¦ì ì¬ì©íì¬ ìì íê² ê°ì¸ ìºë¦°ëì ì ê·¼í©ëë¤.

## Setup

### 1. OAuth í´ë¼ì´ì¸í¸ í¤ ì¤ì 

```bash
# Google Cloud Console ìì OAuth í´ë¼ì´ì¸í¸ í¤ ë¤ì´ë¡ë
# https://console.cloud.google.com/apis/credentials

# í¤ íì¼ì í ëë í ë¦¬ì ë³µì¬
cp ~/Downloads/client_secret_*.json ~/.google-credentials.json
```

### 2. ìì¡´ì± ì¤ì¹

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 3. ì¸ì¦ íì¤í¸

```bash
cd /Users/andrew/.openclaw/workspace/google-calendar
python3 scripts/oauth_setup.py
```

ì²« ì¤íì ë¸ë¼ì°ì ê° ì´ë¦¬ê³  Google ê³ì ì¼ë¡ ë¡ê·¸ì¸í í ê¶íì ë¶ì¬í´ì¼ í©ëë¤.

## Capabilities

### ì¼ì  ì¡°í

**í¥í ì¼ì  íì¸:**
```
"ë¤ì 7 ì¼ ì¼ì ì ë³´ì¬ì¤"
"ë´ì¼ ì¼ì ì ëì¼?"
"ì´ë² ì£¼ íì ëª©ë¡ ìë ¤ì¤"
```

**í¹ì  ê¸°ê° ì¡°í:**
```
"4 ì 15 ì¼ë¶í° 20 ì¼ê¹ì§ ì¼ì ì ë³´ì¬ì¤"
```

### ì¼ì  ìì±

**ì ì¼ì  ì¶ê°:**
```
"ë´ì¼ ì¤í 2 ìì í ë¯¸í ì¼ì  ë§ë¤ì´ì¤, 1 ìê° ëì, Zoom ì¼ë¡"
"ë¤ì ì£¼ ììì¼ 10 ìì dentist ìì½, 30 ë¶"
```

### ì¼ì  ìì 

**ì¼ì  ë³ê²½:**
```
"ë´ì¼ ì¤í 2 ì ë¯¸íì ì¤í 3 ìë¡ ë°ê¿ì¤"
"íì ì ëª©ì 'í ë¯¸í'ìì 'íë¡ì í¸ ê²í  ë¯¸í'ì¼ë¡ ë³ê²½í´ì¤"
```

### ì¼ì  ìì 

**ì¼ì  ì·¨ì:**
```
"ë´ì¼ ì¤í 2 ì ë¯¸í ì·¨ìí´ì¤"
```

## Usage Examples

### ìì 1: í¥í ì¼ì  ì¡°í

```python
from scripts.calendar_ops import list_events, format_event

# ë¤ì 7 ì¼ ì¼ì  ì¡°í
events = list_events(max_results=10)
for event in events:
    print(format_event(event))
```

### ìì 2: ì ì¼ì  ìì±

```python
from scripts.calendar_ops import create_event
from datetime import datetime, timedelta

# ë´ì¼ ì¤í 2 ì íì ìì±
start = datetime.now() + timedelta(days=1, hours=14)
end = start + timedelta(hours=1)

event = create_event(
    summary="í ë¯¸í",
    start_time=start.isoformat(),
    end_time=end.isoformat(),
    description="ì£¼ê° íë¡ì í¸ ê²í ",
    location="Zoom"
)
```

### ìì 3: ìºë¦°ë ëª©ë¡ íì¸

```python
from scripts.oauth_setup import list_calendars

calendars = list_calendars()
for cal in calendars:
    print(f"{cal['summary']} - {cal['accessRole']}")
```

## Files Structure

```
google-calendar/
âââ SKILL.md
âââ scripts/
â   âââ oauth_setup.py      # OAuth 2.0 ì¸ì¦ ë° í í° ê´ë¦¬
â   âââ calendar_ops.py     # Calendar API ì°ì° í¨ìë¤
âââ references/
```

## Security Notes

- OAuth í í°ì `~/.google-calendar-token.pickle` ì ì ì¥ë©ëë¤
- í´ë¼ì´ì¸í¸ í¤ë `~/.google-credentials.json` ì ì ì¥ë©ëë¤
- ì´ íì¼ë¤ì `.gitignore` ì ì¶ê°ëì´ì¼ í©ëë¤
- ê¶í ë²ì: `https://www.googleapis.com/auth/calendar` (ì½ê¸°/ì°ê¸° ì ì²´ ì ê·¼)

## Troubleshooting

**"OAuth í´ë¼ì´ì¸í¸ í¤ íì¼ì´ ììµëë¤" ì¤ë¥:**
- Google Cloud Console ìì OAuth 2.0 í´ë¼ì´ì¸í¸ í¤ë¥¼ ë¤ì ë¤ì´ë¡ë
- `client_secret_XXXXXX.json` íì¼ì `~/.google-credentials.json` ì¼ë¡ ë³µì¬

**ì¸ì¦ ì¤í¨:**
- í í° íì¼ì ìì íê³  ì¬ì¸ì¦: `rm ~/.google-calendar-token.pickle`
- Google Cloud Console ìì API íì±í íì¸

**ê¶í ì¤ë¥:**
- OAuth ëì íë©´ìì íìí ê¶í ì¶ê°
- ì¤í í° ìì  í ì¬ì¸ì¦
