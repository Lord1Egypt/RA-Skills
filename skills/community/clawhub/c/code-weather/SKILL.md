---
name: code-weather
version: 1.0.0
description: >
  A daily weather report for your codebase. Clear skies when tests pass and
  coverage is high. Thunderstorms when bugs are clustering. Fog when nobody
  can understand the new module. Hurricane warning when that dependency with
  9 critical CVEs hasn't been updated. Check the forecast before you code.
author: J. DeVere Cooley
category: fun-tools
tags:
  - visualization
  - health
  - dashboard
  - daily
metadata:
  openclaw:
    emoji: "🌤️"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - fun
      - daily-driver
---

# Code Weather

> "You wouldn't go outside without checking the weather. Why would you start coding without checking the forecast?"

## What It Does

Every morning, before you write a line of code, Code Weather gives you the **atmospheric conditions** of your codebase. Not metrics. Not dashboards. A weather report — because your brain already knows what "thunderstorms" means, but it has to think about what "cyclomatic complexity trending upward in the auth module" means.

## The Weather Report

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ⛅ CODE WEATHER REPORT — Monday, March 3, 2026            ║
║    Repository: acme-platform                                 ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║    CURRENT CONDITIONS:  Partly Cloudy ⛅                     ║
║    Temperature:  72°F (comfortable)                          ║
║    Wind:         Light breeze from the east (minor churn)    ║
║    Visibility:   Good (code is readable)                     ║
║    Pressure:     Falling (complexity increasing)             ║
║                                                              ║
║    ┌──────────────────────────────────────────────┐          ║
║    │              ⛅                               │          ║
║    │           .-~~~-.                             │          ║
║    │    .- ~ ~-(       )- ~-.                     │          ║
║    │   /                     \                    │          ║
║    │  ~    acme-platform      ~                   │          ║
║    │ (      Partly Cloudy      )                  │          ║
║    │  ~         72°F          ~                   │          ║
║    │   \                     /                    │          ║
║    │    ~ - . _________. - ~                      │          ║
║    └──────────────────────────────────────────────┘          ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  5-DAY FORECAST:                                             ║
║                                                              ║
║  Mon     Tue     Wed     Thu     Fri                         ║
║  ⛅      🌤️      🌤️      ⛈️      🌧️                         ║
║  72°     75°     76°     58°     62°                         ║
║  Cloudy  Clear   Clear   Storm!  Rain                        ║
║                                                              ║
║  ⚠️ Thursday: Sprint deadline. Expect turbulence.            ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  REGIONAL WEATHER (by module):                               ║
║                                                              ║
║  src/auth/      ☀️ Sunny     All tests pass. Clean code.     ║
║  src/checkout/  ⛅ Cloudy    2 flaky tests. Watch for rain.  ║
║  src/payments/  🌧️ Rainy     4 open bugs. Coverage dropping. ║
║  src/api/       ⛈️ Stormy    Deprecated dep. 2 CVEs.         ║
║  src/utils/     🌫️ Foggy     No docs. 3 confusing functions. ║
║  src/ui/        ☀️ Sunny     Recent refactor. Feeling fresh. ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  WEATHER ALERTS:                                             ║
║                                                              ║
║  🌪️ TORNADO WATCH: src/api/legacy-adapter.ts                ║
║     Last meaningful update: 14 months ago.                   ║
║     3 consumers. 0 tests. Bus factor: 0 (author left).      ║
║     If this breaks, nobody knows how to fix it.              ║
║                                                              ║
║  ⛈️ SEVERE THUNDERSTORM: src/payments/                       ║
║     Bug density spiking. 4 bugs in 2 weeks (was 1/month).   ║
║     Coverage dropped 8% since last sprint.                   ║
║     Forecast: More bugs incoming if not addressed.           ║
║                                                              ║
║  🌫️ FOG ADVISORY: src/utils/data-transformer.ts              ║
║     Cyclomatic complexity: 47. No documentation.             ║
║     3 developers asked "what does this do?" this month.      ║
║     Visibility: near zero.                                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Weather Conditions Mapping

### Temperature (Overall Health)

| Temp | Condition | What It Means |
|---|---|---|
| 80°+ | 🔥 Hot | Everything's great. High coverage, clean code, happy team |
| 70-79° | ☀️ Warm | Healthy. Minor issues but nothing urgent |
| 60-69° | ⛅ Cool | Some concerns accumulating. Needs attention soon |
| 50-59° | 🌧️ Cold | Significant issues. Bugs clustering, coverage falling |
| 40-49° | ⛈️ Frigid | Serious problems. Multiple alerts active |
| < 40° | 🥶 Frozen | Crisis. Production issues, major technical debt |

### Sky Conditions (Code Quality)

| Condition | Icon | Meaning |
|---|---|---|
| **Clear** | ☀️ | Tests passing, linter clean, no open bugs |
| **Partly Cloudy** | ⛅ | Minor warnings, flaky tests, small TODO count |
| **Cloudy** | ☁️ | Multiple warnings, growing TODO list, stale branches |
| **Rainy** | 🌧️ | Failing tests, open bugs, declining coverage |
| **Stormy** | ⛈️ | Critical bugs, security vulnerabilities, CI broken |
| **Foggy** | 🌫️ | Poor documentation, confusing naming, low readability |
| **Snowy** | ❄️ | Frozen development, no commits in weeks, stalled PRs |

### Wind (Change Velocity)

| Speed | Meaning |
|---|---|
| **Calm** | Stable. Few changes happening. |
| **Light breeze** | Normal development pace. Healthy churn. |
| **Moderate wind** | Active development. Lots of changes flowing. |
| **Strong wind** | Rapid changes. Sprint deadline approaching. |
| **Gale** | Chaotic. Too many changes, too fast. Review quality dropping. |
| **Hurricane** | Emergency. Production firefighting. All hands on deck. |

### Pressure (Complexity Trend)

| Pressure | Meaning |
|---|---|
| **Rising** | Complexity decreasing. Refactoring happening. Getting healthier. |
| **Stable** | Complexity steady. Normal development. |
| **Falling** | Complexity increasing. Features adding weight. Watch for storms. |
| **Plummeting** | Complexity spiking. Deadline pressure. Technical debt accumulating fast. |

### Visibility (Readability)

| Visibility | Meaning |
|---|---|
| **Clear (10+ miles)** | Well-documented, well-named, obvious structure |
| **Good (5-10 miles)** | Mostly readable, some areas need docs |
| **Fair (1-5 miles)** | Several confusing areas, naming inconsistencies |
| **Poor (< 1 mile)** | Significant areas where only the author understands the code |
| **Zero** | "What does this function do?" "Nobody knows." |

## The Forecast Algorithm

```
CURRENT CONDITIONS:
├── Temperature = weighted average of:
│   ├── Test pass rate (25%)
│   ├── Code coverage (20%)
│   ├── Open bug count (20%)
│   ├── Dependency health (15%)
│   └── Recent commit quality (20%)
│
├── Sky = worst-performing quality metric
├── Wind = commit velocity (commits/day, PR throughput)
├── Pressure = complexity delta (this week vs. last week)
└── Visibility = documentation coverage + naming quality score

FORECAST:
├── Based on trends over last 7/14/30 days
├── Known events (sprint deadlines, releases) = expected storms
├── Seasonal patterns (Friday deploys = higher wind)
└── Historical patterns (this module storms every Q4)
```

## Special Weather Events

```
🌪️ TORNADO: A critical system with zero tests and zero documentation.
             Could destroy everything if it breaks. No warning.

🌊 TSUNAMI: A breaking change in a dependency that affects 50%+ of codebase.
             Long-period wave — you won't feel it until it hits.

🌋 VOLCANO: A major rewrite erupting. Lava (new code) flowing in all
             directions. Existing terrain being reshaped.

🏜️ DROUGHT: No commits in 2+ weeks. Development has stopped.
             The codebase is drying out.

🌈 RAINBOW: A major refactor just landed. Coverage went up. Bugs went down.
             The storm is over and everything is cleaner.

❄️ ICE AGE:  The project has been frozen. No development, no maintenance,
             no hope. Consider archiving.
```

## When to Invoke

- **Every morning.** Check the weather before you code. 30-second habit.
- Before sprint planning (know the atmospheric conditions before committing to work)
- During standup (share the weather with the team instead of boring metrics)
- Before a production deploy (is the forecast clear or stormy?)
- Weekly for trend analysis (is the climate getting warmer or colder?)

## Why It Matters

Developers look at dashboards and think "numbers." They look at weather and think "should I bring an umbrella?" Code Weather translates abstract metrics into intuitive conditions your brain processes instantly.

You don't need to understand cyclomatic complexity trends to know that "thunderstorms in the payments module" means stay alert.

Zero external dependencies. Zero API calls. Pure codebase climate science.
