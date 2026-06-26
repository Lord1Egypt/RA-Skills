# bilimclass — BilimClass School Schedule Skill for OpenClaw

Access [BilimClass](https://bilimclass.kz) (Kazakhstan school platform) schedule, homework, and diary through the unofficial API. Built for Kazakhstan students who want their AI assistant to check schedule and homework.

## Features

- 📅 **Schedule** — lessons with teachers, times, and homework for any date
- 📋 **Week view** — get the full week at once
- 📝 **Diary** — detailed homework details per subject
- 🔌 **Auto-config** — reads token from `~/.openclaw/.env.json`
- 🌍 **CLI + Agent** — works via CLI and as an OpenClaw skill (auto-triggers)

## Install

### Quick (OpenClaw users)

Run in your OpenClaw terminal:

```bash
# Option 1: from ClawHub (skip to "Setup" below), run in your OpenClaw terminal:
openclaw skills install bilimclass

# Option 2: manually clone into your skills folder:
openclaw skills install bilimclass

# Option 3: from source
git clone https://github.com/YOUR_USERNAME/bilimclass-openclaw.git ~/.openclaw/workspace/skills/bilimclass
```

### Requirements

- Python 3.x with `requests`

```bash
pip install requests
```

## Setup

1. **Get your JWT token:**
   - Log into [bilimclass.kz](https://bilimclass.kz)
   - Open browser console (F12 → Console)
   - Run: `localStorage.token`
   - Copy the whole output

2. **Add to `~/.openclaw/.env.json`:**
   ```json
   {
     "bilimclass": {
       "token": "eyJ0eXAiOiJKV1QiLCJ...",
       "expires": "2027-04-05T16:15:39",
       "schoolId": "YOUR_SCHOOL_ID",
       "eduYear": "2025",
       "userId": "YOUR_USER_ID",
       "studentSchoolUuid": "YOUR_UNIQUE_UUID",
       "studentGroups": [
         {"uuid": "...", "name": "Группа 1"},
         {"uuid": "...", "name": "Группа 2"}
       ]
     }
   }
   ```

   > **How to find your IDs:** After logging in, open DevTools → Network tab → click any request to `api.bilimclass.kz` → check the Query String parameters for `schoolId`, or look at the JWT payload (decode at [jwt.io](https://jwt.io)) for `sub` (userId).

3. **Test it:**
   ```bash
   python3 ~/.openclaw/workspace/skills/bilimclass/scripts/bilimclass.py tomorrow
   ```

## Usage

### CLI Commands

```bash
bilimclass.py today
bilimclass.py tomorrow
bilimclass.py schedule 06.04.2025
bilimclass.py week 06.04.2025     # week starting Monday
bilimclass.py diary 2025-04-06   # detailed homework
bilimclass.py schedule 06.04.2025 --raw  # raw JSON
bilimclass.py help
```

### As an OpenClaw Skill

Once installed, the skill auto-triggers on natural language:

- "какое расписание на завтра?"
- "какая домашка по математике?"
- "что уроки на понедельник?"
- "расписание на неделю"
- "домашка" / "оценки" / "дневник"

### Sample Output

```
📅 06 АПРЕЛЯ
  🕐 08:00 - 08:40 | Математика
     👨‍🏫 А. Б. Иванова
  🕐 08:45 - 09:25 | Английский язык
     👨‍🏫 В. П. Петрова
     📝 ex. 6 p. 90, card
  🕐 09:40 - 10:20 | Физика
     👨‍🏫 Г. С. Сидоров
     📝 §48, задачи 1-5
```

## How It Works

The skill talks to BilimClass's internal API:

```
OpenClaw Agent → bilimclass.py → api.bilimclass.kz (Bearer JWT) → JSON → Formatted output
```

The JWT token lasts ~1 year, so you only need to refresh it annually.

## Security

- **No secrets in code** — token is read from `~/.openclaw/.env.json` at runtime
- **Add `.env.json` to your `.gitignore`**
- The skill is **100% local** — no data is sent anywhere except to BilimClass API
- This is an **unofficial** client — BilimClass does not provide a public API

## Limitations

- Unofficial API — endpoints may change
- JWT tokens expire (~1 year lifespan)
- Only works for your own account (no multi-user support yet)

## License

MIT — use it, modify it, share it.

---

Built for Kazakhstan students. Made with ❤️ by [Bolt69](https://github.com/bolt69) ⚡
