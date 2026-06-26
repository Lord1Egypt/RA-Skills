<div align="center">

# 🍜 eat.skill

> *"What's for lunch? What's for dinner? — The two greatest unsolved mysteries of mankind."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)](https://nodejs.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

Staring at your desk for 10 minutes every day trying to decide what to eat for lunch?

Meetings until 6 PM, brain empty, no idea what's for dinner?

Finally made up your mind, only to find a 30-minute queue at the restaurant?

**Install this Skill and let your AI meal buddy remind you on time — decision made in 3 seconds.**

[Install](#-get-started-in-30-seconds) · [Commands](#-commands) · [Reminders](#-scheduled-reminders) · [Contribute](CONTRIBUTING.md)

[中文](README.md)

</div>

---

## ✨ What It Does

Install → say "what should I eat today" → AI picks a food category first, then finds you a restaurant → you say "sure" and go eat.

**No restaurant database required.** Works out of the box — AI comes loaded with food knowledge and picks something for you at random. A restaurant database makes recommendations more precise, but it's entirely optional.

```
You: What should I eat today?

🎲 The dice tumbles through the air... lands!

   🎯 Today's destined flavor — Hot Pot!

   🍲 Suggested order:
     • Base: Half tomato, half spicy (dual pot)
     • Must-have: Tripe, duck intestine, tender beef, tofu
     • Budget: ~$10-15 per person

   📍 Hot pot near you:
     1️⃣ Haidilao (Wangjing) | 💰 $15 | 500m
     2️⃣ Xiaolongkan (Laiguangying) | 💰 $12 | 800m

Hesitate and you'll starve. Commit and you'll feast!
```

## 🚀 Get Started in 30 Seconds

### Option 1: Copy & Paste (any AI tool)

1. Copy the contents of [`SKILL.md`](SKILL.md)
2. Paste into ChatGPT / Claude / any AI chat
3. Say: **What should I eat today?**

> On first use, the AI will chat briefly to learn your taste, location, and budget. After that, recommendations are instant. No restaurant database needed.

### Option 2: Install as an AI Skill

**Claude Code:**

```bash
git clone https://github.com/funAgent/eat-skill.git ~/.claude/skills/eat-skill
cd ~/.claude/skills/eat-skill && npm install
```

**Cursor:**

```bash
git clone https://github.com/funAgent/eat-skill.git .cursor/skills/eat-skill
cd .cursor/skills/eat-skill && npm install
```

**OpenClaw:**

```bash
npx clawhub install eat-skill
```

### Option 3: Just Try It

Run directly in the terminal:

```bash
git clone https://github.com/funAgent/eat-skill.git
cd eat-skill && npm install
node schedule/nudge.mjs
```

## 🎮 Commands

### Core Commands

| Command | What It Does | Or Just Say... |
| --- | --- | --- |
| `/eat` | Show all commands | — |
| `/eat-select` | Help you pick what to eat | "What should I eat today?" |
| `/eat-random` | Roll the dice | "Just pick for me" |
| `/eat-discover` | Search nearby restaurants | "Anything good around here?" |
| `/eat-create` | Create a restaurant Skill | "Make a Skill for this place" |
| `/eat-navigate` | Get directions to a restaurant | "How do I get to Haidilao?" |
| `/eat-pk` | Compare two restaurants | "Which one's better, X or Y?" |
| `/eat-list` | Browse the restaurant database | "What places do we have?" |
| `/eat-nope` | Reject and get a new pick | "Not this one" |
| `/eat-review` | Rate after eating | "Just finished eating" |

### Scene Modes (where it gets fun)

| Command | Scene | Effect |
| --- | --- | --- |
| `/eat-boss` | 🤑 Boss is paying | Go premium — it's on them |
| `/eat-broke` | 😭 End of month | Strict budget, maximum savings |
| `/eat-diet` | 🥗 On a diet | Low-cal options (with gentle nudges not to go too extreme) |
| `/eat-solo` | 🧑 Eating alone | Solo-friendly spots, warm vibes |
| `/eat-date` | 💕 Date night | Great ambiance + avoid-the-awkward tips |
| `/eat-team` | 👥 Team dinner | Variety for picky groups, the "everyone's happy" solver |

## ⏰ Scheduled Reminders

**Auto-enabled on install** — reminds you to eat on time. Recommends a specific restaurant if the database has entries, or suggests a random food category if it doesn't.

### Default Schedule

| Reminder | Time | Frequency | Default |
| --- | --- | --- | --- |
| 🥗 Lunch | 11:50 | Weekdays | ✅ On |
| 🍽️ Dinner | 17:45 | Weekdays | ✅ On |
| 🥐 Weekend brunch | 10:00 | Weekends | ❌ Off |
| 🌙 Late-night snack | 22:00 | Daily | ❌ Off |

### Setting Up Reminders

#### Claude Code (recommended)

```bash
# Lunch reminder
claude schedule "Remind me to eat lunch every weekday at 11:50" \
  --command "node schedule/nudge.mjs --meal lunch"

# Dinner reminder
claude schedule "Remind me to eat dinner every weekday at 17:45" \
  --command "node schedule/nudge.mjs --meal dinner"

# Late-night snack (chaotic mode — wilder recommendations)
claude schedule "Ask me about supper every day at 10 PM" \
  --command "node schedule/nudge.mjs --meal late_night --style chaotic"
```

#### OpenClaw

Auto-registered on install (reads `schedule/eat-schedule.json`).
Adjust timing and toggles in OpenClaw settings.

#### System Crontab (universal)

```bash
crontab -e

# Add these lines (replace with your actual path)
50 11 * * 1-5  cd /path/to/eat-skill && node schedule/nudge.mjs --meal lunch
45 17 * * 1-5  cd /path/to/eat-skill && node schedule/nudge.mjs --meal dinner
```

#### Custom Preferences

Edit `schedule/eat-schedule.json`:

```json
{
  "preferences": {
    "avoidRepeat": true,
    "avoidRepeatDays": 3,
    "maxBudget": 50,
    "excludeCategories": ["fast food"],
    "locationHint": "Wudaokou"
  }
}
```

## 🔍 Nearby Restaurant Discovery (Gaode Maps)

Built-in [Gaode LBS Skill](vendor/amap-lbs-skill/) for nearby restaurant search + route navigation.

### Set Up API Key (free, one-time)

```bash
# 1. Apply: https://console.amap.com/dev/key/app (select "Web Service")
# 2. Set the key
export AMAP_WEBSERVICE_KEY="your_key_here"
```

Free tier: 5,000 requests/day — more than enough for personal use.

### Search + Auto-Generate Skill

```bash
# Search nearby restaurants
AMAP_KEY=$AMAP_WEBSERVICE_KEY node vendor/amap-lbs-skill/scripts/poi-search.js \
  --keywords="food" --city="Beijing"

# Search results → Restaurant Skill (skeleton)
AMAP_KEY=$AMAP_WEBSERVICE_KEY node vendor/amap-lbs-skill/scripts/poi-search.js \
  --keywords="BBQ" --city="Beijing" \
  | node generator/poi-to-skill.mjs --outdir restaurants/

# Route planning
AMAP_KEY=$AMAP_WEBSERVICE_KEY node vendor/amap-lbs-skill/scripts/route-planning.js \
  --type walking --origin "116.338,39.992" --destination "116.345,39.995"
```

## 🏗️ Create Your Own Restaurant Skill

Three ways — pick whatever's easiest:

### Method 1: Tell AI (fastest)

```
/eat-create

Old Wang's BBQ Skewers, downstairs at Wangjing SOHO T1,
5 PM to 2 AM, ~$10/person, lamb skewers $1.20, grilled squid $2.30,
outdoor seating is great in summer
```

### Method 2: Gaode Search + Auto Convert

```bash
AMAP_KEY=$AMAP_WEBSERVICE_KEY node vendor/amap-lbs-skill/scripts/poi-search.js \
  --keywords="Old Wang BBQ" --city="Beijing" \
  | node generator/poi-to-skill.mjs --outdir restaurants/
# Skeleton generated — add your own dish recommendations
```

### Method 3: Fill the Template

```bash
cp templates/restaurant-info.yaml restaurants/laowang-bbq/restaurant-info.yaml
# Edit and fill in
node generator/generate.mjs -i restaurants/laowang-bbq/restaurant-info.yaml \
  -o restaurants/laowang-bbq/SKILL.md
```

## 📋 Restaurant Database

| Restaurant | City | Cuisine | Avg. Price | Status |
| --- | --- | --- | --- | --- |
| [Meizhou Dongpo (Beiyuan Huamao)](restaurants/meizhou-dongpo-beiyuan/) | Beijing, Chaoyang | Sichuan | ¥69 | 🟢 Complete |

> 🙋 What about your go-to spot? [Contribute one →](CONTRIBUTING.md)

## 📁 Project Structure

```
eat-skill/
├── SKILL.md                         # Core Skill (load this and you're good)
├── package.json
├── user-profile.json                # User profile (auto-generated on first use)
│
├── schedule/                        # ⏰ Scheduled reminders
│   ├── nudge.mjs                    # Mealtime nudge script (fun messages + random picks)
│   └── eat-schedule.json            # Reminder config (timing, preferences)
│
├── generator/                       # 🏗️ Restaurant Skill generator
│   ├── generate.mjs                 # Generate SKILL.md from YAML/JSON
│   ├── poi-to-skill.mjs             # Gaode POI → Restaurant SKILL.md converter
│   └── skill-template.md            # Generation template
│
├── vendor/
│   └── amap-lbs-skill/              # 🗺️ Gaode LBS Skill (POI / routes / maps)
│
├── templates/
│   ├── restaurant-info.yaml         # Restaurant info template
│   └── user-profile.example.json    # User profile example
│
├── restaurants/                     # 🍽️ Community restaurant collection (optional)
│   ├── README.md
│   └── meizhou-dongpo-beiyuan/
│
├── CONTRIBUTING.md
└── LICENSE
```

## 🧬 Design Philosophy

| Principle | Description |
| --- | --- |
| **Decisive by default** | Better to pick wrong than let you keep agonizing |
| **On-time nudges** | You don't have to ask — it reminds you at mealtime |
| **Fun first** | Dice rolls, spinning wheels, snarky copy — never the same twice |
| **Composable** | Gaode Skill handles maps, we handle decisions |
| **Community-driven** | More restaurant contributions = better recommendations |
| **Tool-agnostic** | It's just Markdown — works with any AI |

## 🎯 Inspiration

| Project | What It Inspired |
| --- | --- |
| [Jinguyuan Dumpling Skill](https://github.com/JinGuYuan/jinguyuan-dumpling-skill) | Even a single restaurant can have its own AI Skill |
| [colleague.skill](https://github.com/titanwings/colleague-skill) | Pioneer of persona-driven Skills |
| [Gaode LBS Skill](https://github.com/AMap-Web/amap-lbs-skill) | Map capabilities without reinventing the wheel |

## 🤝 Contributing

**The simplest contribution: turn your favorite restaurant into a Skill and open a PR.**

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

[MIT](LICENSE) — Use it freely. Eat well.

## Contact

<div align="center">

[![X (Twitter)](https://img.shields.io/badge/@funAgentApp-000000?style=flat&logo=x&logoColor=white)](https://x.com/funAgentApp)
[![X (Twitter)](https://img.shields.io/badge/@hash--panda-000000?style=flat&logo=x&logoColor=white)](https://x.com/hash-panda)

</div>
