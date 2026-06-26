---
name: astro-life-insights
description: Personalized daily astrological insights focused on relationships, work, personal growth, and luck. Positive framing only. Uses your natal chart + astronomy-engine transits.
version: 1.1.1
---

# Astro Life Insights ✨

**Personalized daily astrology for YOUR life, with a positive twist.**

## What This Does

Calculates current planetary transits against YOUR natal chart and provides insights for:

- 💕 **Relationships** - Love, connection, partnerships
- 💼 **Work** - Career, achievement, projects
- 🌱 **Personal Growth** - Learning, spirituality, transformation
- 🍀 **Luck** - Opportunities, abundance, manifestation

**Everything is framed positively.** Challenging transits become growth opportunities. Saturn squares = building foundations. Mars oppositions = channeling passion.

---

## Setup (One-Time, Required)

> ⚠️ **This skill ships with no personal data.** You must run setup before anything works. Your birth data stays on your machine only.

### 1. Install Dependencies

```bash
cd path/to/astro-life-insights
npm install
```

### 2. Configure Your Birth Chart

```bash
node configure.js
```

You'll be prompted for:
- Birth date (YYYY-MM-DD)
- Birth time (HH:MM in 24-hour format)
- Birth location (city, country)

This saves to `~/.config/astro-life-insights/natal-chart.json`

### 2. Test It

```bash
node daily.js
```

Should output your personalized insights for today!

---

## Usage

### Get Today's Insights (Human-Readable)

```bash
node daily.js
```

**Output:**
```
✨ Your Astrological Weather - March 13, 2026

💕 RELATIONSHIPS
Uranus square natal Mars (building)
→ Freedom and intimacy find balance.
→ Action: Break free from limiting patterns.

💼 WORK
Sun square natal Uranus (EXACT TODAY)
→ Building identity through productive challenge.
→ Action: Honor both your needs and commitments.

🌱 PERSONAL GROWTH
Neptune sextile natal Moon (building)
→ Intuition guides evolutionary path.
→ Action: Tune into subtle guidance.

🍀 LUCK
Venus square natal Neptune (building)
→ Fortune through clarifying values.
→ Action: Invest in what you truly value.

✨ OVERALL: 15 active transits today. Rich day for inner work.
```

### Get Insights for Specific Date

```bash
node daily.js 2026-03-15
```

### Check Upcoming Transits

```bash
node upcoming.js
```

Shows major transits coming in the next 30 days.

### Get JSON Output (for dashboards and automation)

```bash
node daily-json.js
```

Returns structured JSON — perfect for integrating into dashboards, agents, or any app.

---

## JSON Output Schema (`daily-json.js`)

```json
{
  "date": "2026-03-13",
  "totalTransits": 15,
  "relationships": [
    {
      "transit": "Uranus square",
      "planet": "uranus",
      "natal": "mars",
      "insight": "Freedom and intimacy find balance.",
      "action": "Break free from limiting patterns.",
      "emoji": "💕",
      "exact": false
    }
  ],
  "work": [ ... ],
  "growth": [ ... ],
  "luck": [ ... ]
}
```

### Field Reference

| Field | Type | Description |
|---|---|---|
| `date` | string | ISO date for this reading |
| `totalTransits` | number | Total active transits across all categories |
| `planet` | string | Transiting planet (lowercase: `sun`, `moon`, `mars`, etc.) |
| `natal` | string | Natal planet being aspected (lowercase) |
| `transit` | string | Aspect type string e.g. `"Uranus square"` |
| `insight` | string | Positive interpretation of the transit |
| `action` | string | What to do about it today |
| `exact` | boolean | Whether the transit is exact today (peak influence) |

---

## Aspect Reference

Understanding aspects helps you interpret the data. Each aspect represents a geometric relationship between planets:

| Symbol | Name | Angle | Vibe | Meaning |
|---|---|---|---|---|
| ☌ | Conjunction | 0° | Fusion | Two forces merge — intense, focused, amplified energy |
| ☍ | Opposition | 180° | Tension | Opposing forces — awareness through contrast |
| □ | Square | 90° | Challenge | Friction that demands growth — a productive challenge |
| △ | Trine | 120° | Harmony | Natural flow and ease — gifts arriving without effort |
| ⚹ | Sextile | 60° | Opportunity | An open door — rewards conscious action |
| ⚻ | Quincunx | 150° | Adjustment | Subtle misalignment requiring creative adaptation |

### Planet Glyphs & Meanings

| Glyph | Planet | Governs |
|---|---|---|
| ☀️ | Sun | Identity, vitality, purpose |
| 🌙 | Moon | Emotions, instincts, inner world |
| ☿ | Mercury | Mind, communication, learning |
| ♀ | Venus | Love, beauty, values, pleasure |
| ♂ | Mars | Drive, action, desire, courage |
| ♃ | Jupiter | Expansion, luck, wisdom, growth |
| ♄ | Saturn | Structure, discipline, mastery |
| ⛢ | Uranus | Revolution, freedom, sudden change |
| ♆ | Neptune | Dreams, intuition, spirituality |
| ♇ | Pluto | Transformation, power, rebirth |

---

## Dashboard Integration

`daily-json.js` is designed for dashboard use. Here's how to integrate it:

### Server-Side (Node.js)

```js
// In your server.js API endpoint
const { execSync } = require('child_process');
const astroPath = path.join(process.env.HOME, '.openclaw', 'workspace', 'skills', 'astro-life-insights', 'daily-json.js');

const output = execSync(`/opt/homebrew/bin/node daily-json.js`, {
  encoding: 'utf8',
  timeout: 10000,
  cwd: path.dirname(astroPath),
  env: { ...process.env, PATH: '/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin', HOME: process.env.HOME }
});
const data = JSON.parse(output.trim());
```

> ⚠️ **Important**: Always use the full node path (`/opt/homebrew/bin/node`) and set `PATH` explicitly in `env`. launchd/daemon environments often don't inherit shell PATH.

### Educational Visualization

When building a UI, display transits with:
- **Planet chip**: glyph + planet name (hoverable with meaning)
- **Aspect symbol**: colored by vibe (square=purple, trine=indigo, etc.)
- **Natal chip**: what in your natal chart is being activated
- **"EXACT TODAY" badge**: pulsing highlight when `exact: true`
- **Aspect description**: what the aspect type means geometrically
- **Insight**: the positive interpretation
- **Action**: concrete thing to do today
- **Planet meanings**: educational footer so users learn over time

This turns a transit like `"Uranus square natal Mars"` into something anyone can understand and learn from, not just astrologers.

---

## How It Works

1. **Calculate Transits** - Uses astronomy-engine to find current planetary positions
2. **Compare to Natal Chart** - Identifies aspects (conjunctions, trines, squares, etc.)
3. **Map to Life Areas** - Venus/Mars/7th house = relationships, Sun/Saturn/10th = work, etc.
4. **Positive Interpretation** - Frames every transit as opportunity
5. **Actionable Advice** - Tells you what to DO about it

---

## Files

- `configure.js` — One-time setup for your natal chart
- `daily.js` — Human-readable daily insights
- `daily-json.js` — Machine-readable JSON output for dashboards/automation
- `upcoming.js` — See future transits
- `calculate.js` — astronomy-engine wrapper
- `interpret.js` — Transit → insight mapping
- `data/interpretations.json` — Database of positive meanings
- `data/life-areas.json` — Life area → planet/house mapping

---

## Why This is Different

**Other astrology tools:**
- Generic sun sign horoscopes (not personalized)
- Focus on negative/challenging aspects
- No actionable advice
- Not tailored to YOUR life

**This tool:**
- Uses YOUR exact natal chart
- Everything framed positively
- Focused on relationships, work, growth, luck
- Tells you what to DO, not just what to expect
- JSON output ready for dashboard integration

---

## Privacy & Your Data

Your natal chart is stored **locally on your machine** at:
```
~/.config/astro-life-insights/natal-chart.json
```

This file is **outside the skill folder** and is never packaged or published. This skill ships with zero personal data — every user must run `configure.js` to enter their own birth details before anything works.

Nothing is sent to external services. All calculations happen locally using the `astronomy-engine` npm package.

---

## Requirements

- Node.js 16+
- `astronomy-engine` npm package (run `npm install` in the skill directory)

---

## Changelog

### v1.1.0
- Documented `daily-json.js` JSON output format and full field schema
- Added Aspect Reference table (symbols, angles, meanings)
- Added Planet Glyphs reference
- Added Dashboard Integration guide with server-side code and educational visualization patterns
- Added note on PATH requirement for daemon/launchd environments

### v1.0.0
- Initial release

---

**Built with intention 🌀**
