# Report Formats

## FIRST-RUN: Fleet Health Report Card

Use this format when `memory/last-analysis.json` does NOT exist.

```
🩺 Fleet Health Report Card

Overall Grade: {A-F}
Current monthly run rate: ~${monthlyRunRate}
After optimization: ~${optimizedRunRate}

Your fleet has {N} agents:

{agentName} — ~${monthlyCost}/month ({modelName})
{agentName} — ~${monthlyCost}/month ({modelName})
(sorted by cost descending)

🧾 Your Cost Receipts:

• "{what you asked for in your own words}" — ${cost}
  Here's what happened: {plain English breakdown — tool calls, retries, model used}
  You probably didn't realize: {the surprising part — e.g., "each style attempt costs ~$20"}
  → Next time: {ONE concrete action}

• "{what you asked for}" — ${cost}
  Here's what happened: {breakdown}
  You probably didn't realize: {surprise}
  → Next time: {action}

(repeat for all 5 receipts)

🪞 Your Costly Habits:

{habit #1 name in plain English} — ~${weeklyOrMonthlyCost}
  What happened: {2-3 specific examples from their sessions with $ amounts}
  Why it's expensive: {root cause — e.g. "no tool budget so the agent looped 268 times"}
  🔧 I can fix: {config patch if applicable — e.g. "set tool budget to 50 calls"}
  💡 You should: {behavioral change — e.g. "provide specs before saying 'try again'"}

{habit #2 name} — ~${cost}
  What happened: {specific examples with $}
  Why it's expensive: {root cause}
  🔧 I can fix: {config patch or "no config fix — this is a usage habit"}
  💡 You should: {behavioral change}

(repeat for all 3-5 habits)

⚡ Quick Wins (I can fix these for you):

1. {🔴|🟠|🔵} {laymanTitle} — ~${amount}/month
   {laymanDescription}

2. {🔴|🟠|🔵} {laymanTitle} — ~${amount}/month
   {laymanDescription}

💰 Total potential savings: ~${totalSavings}/month (~${annual}/year)

Want me to apply any of these fixes? Just tell me which ones sound good.
```

Severity emojis: critical = 🔴, major = 🟠, minor = 🔵, info = ⚪

---

## DAILY REPORT

Use this format on subsequent runs. Do NOT add extra sections.

```
🩺 ClawDoctor Report

Hey! I checked your agents over the past {timeframe} and found ~${totalSavings}/month in potential savings.

🧾 Your Cost Receipts:

• "{what you asked for}" — ${cost}
  {plain English breakdown}
  You probably didn't realize: {surprise}
  → Next time: {action}

(repeat for top sessions)

🪞 Your Costly Habits:

{habit name} — ~${cost}
  What happened: {specific examples from their sessions with $}
  Why it's expensive: {root cause}
  🔧 I can fix: {config patch if applicable}
  💡 You should: {behavioral change}

⚡ Quick Wins (I can fix these for you):

1. {🔴|🟠|🔵} {laymanTitle} — ~${amount}/month
   {laymanDescription}
   → Just say the word and I'll fix this

💰 Total potential savings: ~${totalSavings}/month

Want me to fix any of these? Just tell me which ones.
```

If no Quick Wins, omit that section. Same for Costly Habits.
If no major+ findings, do NOT send a report. Stay silent.

---
*ClawDoctor by [Faan AI](https://faan.ai)*
