---
name: andrew-google-tasks
description: Google Tasks API μ°λμΌλ΅ μμ (Task) κ΄λ¦¬. OAuth 2.0 μΈμ¦ μ¬μ©. μ¬μ©μμ ν  μΌ λª©λ΅μ μ΅°ν, μμ±, μμ , μλ£ μ²λ¦¬ν  λ μ¬μ©.
---

# Google Tasks

## Overview

Google Tasks API λ¥Ό νµν΄ μ¬μ©μμ ν  μΌ (Tasks) μ μ΅°ν, μμ±, μμ , μλ£ μ²λ¦¬ν  μ μλ μ¤ν¬μλλ¤. OAuth 2.0 μΈμ¦μ μ¬μ©νμ¬ μμ νκ² Tasks μ μ κ·Όν©λλ¤.

## Setup

### 1. OAuth ν΄λΌμ΄μΈνΈ ν¤ μ¤μ 

μ΄λ―Έ κµ¬κΈ μΊλ¦°λ, μνΈ μ¤ν¬κ³Ό λμΌν ν¤ νμΌμ μ¬μ©ν©λλ¤:

```bash
# ν¤ νμΌμ΄ μ΄λ―Έ μ¤λΉλμ΄ μλ¤λ©΄ μλµ
ls ~/.google-credentials.json
```

### 2. μμ΅΄μ± μ¤μΉ

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 3. μΈμ¦ νμ¤νΈ

```bash
cd /Users/andrew/.openclaw/workspace/google-tasks
python3 scripts/tasks_ops.py
```

μ²« μ¤νμ λΈλΌμ°μ κ° μ΄λ¦¬κ³  Google κ³μ μΌλ΅ λ΅κ·ΈμΈ ν κ¶νμ λ¶μ¬ν΄μΌ ν©λλ¤.

## Capabilities

### μμ λª©λ΅ μ΅°ν

**μ¬μ©μμ μμ λª©λ΅ νμΈ:**
```
"λ΄ ν  μΌ λª©λ΅ λ³΄μ¬μ¤"
"νμ¬ μ§ν μ¤μΈ μμ λλ μμ΄?"
```

### μ μμ μμ±

**μ ν  μΌ μ¶κ°:**
```
"λ΄μΌ λ―Έν μ¤λΉν  μΌ μ¶κ°ν΄μ¤, λ§κ°μ λ΄μΌ μ¤ν 2 μ"
"νλ΅μ νΈ λ³΄κ³ μλ¥Ό μμ±ν΄μΌ ν΄, λ©λª¨: 5 νμ΄μ§ λ¶λ"
```

### μμ μλ£ μ²λ¦¬

**μμ μλ£:**
```
"λ΄μΌ λ―Έν μ¤λΉ μλ£λ΅ νμν΄μ¤"
```

### μμ μμ 

**μμ λ΄μ© λ³κ²½:**
```
"νλ΅μ νΈ λ³΄κ³ μ λ§κ°μΌμ λ¤μ μ£Ό μμμΌλ΅ λ°κΏμ¤"
```

### μμ μμ 

**μμ μ·¨μ:**
```
"λ¶νμν μμ μμ ν΄μ¤"
```

## Usage Examples

### μμ 1: μμ λª©λ΅ μ΅°ν

```python
from scripts.tasks_ops import list_tasks, format_task

# κΈ°λ³Έ λª©λ΅μ μμ μ΅°ν
tasks = list_tasks('@default')
for task in tasks:
    print(format_task(task))
```

### μμ 2: μ μμ μμ±

```python
from scripts.tasks_ops import create_task

# μ μμ μμ±
task = create_task(
    tasklist_id='@default',
    title='νλ΅μ νΈ λ³΄κ³ μ μμ±',
    notes='5 νμ΄μ§ λ¶λ, κΈμμΌκΉμ§',
    due='2026-04-20T17:00:00+09:00'
)
print(f"μμ μμ± μλ£: {task['title']}")
```

### μμ 3: μμ μλ£ μ²λ¦¬

```python
from scripts.tasks_ops import complete_task

# μμ μλ£
task_id = 'μμ_ID_μ¬κΈ°μ'
complete_task('@default', task_id)
print("μμ μλ£ μ²λ¦¬λ¨!")
```

### μμ 4: μμ λª©λ΅ λª©λ΅ μ΅°ν

```python
from scripts.tasks_ops import list_tasklists

tasklists = list_tasklists()
for tl in tasklists:
    print(f"{tl['title']} - {tl['id']}")
```

## Files Structure

```
google-tasks/
βββ SKILL.md
βββ scripts/
    βββ tasks_ops.py      # Tasks API μ°μ° ν¨μλ¤
```

## Security Notes

- OAuth ν ν°μ `~/.google-tasks-token.pickle` μ μ μ¥λ©λλ¤
- ν΄λΌμ΄μΈνΈ ν¤λ `~/.google-credentials.json` μ μ μ¥λ©λλ¤ (μΊλ¦°λ, μνΈ μ¤ν¬κ³Ό κ³µμ )
- μ΄ νμΌλ¤μ `.gitignore` μ μ¶κ°λμ΄μΌ ν©λλ¤
- κ¶ν λ²μ: `https://www.googleapis.com/auth/tasks` (Tasks μ μ²΄ μ κ·Ό)

## Troubleshooting

**"OAuth ν΄λΌμ΄μΈνΈ ν¤ νμΌμ΄ μμµλλ¤" μ¤λ¥:**
- `~/.google-credentials.json` νμΌμ΄ μλμ§ νμΈ
- κµ¬κΈ μΊλ¦°λ μ¤ν¬ μ¤μ  μ μ΄λ―Έ μμ±ν ν¤ νμΌμλλ¤

**μΈμ¦ μ¤ν¨:**
- ν ν° νμΌμ μμ νκ³  μ¬μΈμ¦: `rm ~/.google-tasks-token.pickle`

**κ¶ν μ¤λ¥:**
- μ¤ν ν° μμ  ν μ¬μΈμ¦: `rm ~/.google-tasks-token.pickle && python3 scripts/tasks_ops.py`

## Integration with Other Google Skills

Same OAuth credentials (`~/.google-credentials.json`) are shared with `google-calendar` and `google-sheets` skills, so you only need to authenticate once!
