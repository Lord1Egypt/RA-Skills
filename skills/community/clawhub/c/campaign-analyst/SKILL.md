---
name: campaign-analyst
description: Read a paid-ads account like an analyst. Turn 14 days of campaign results into what to scale, what to pause, what to fix and what to test next, with a data floor that refuses a verdict on too little delivery.
license: MIT
---

# Campaign analyst: scale, pause, fix, test next

Most ad reporting answers "what happened". The only useful question is "what do I change on Monday". This is the
method, and the rules that stop it producing confident nonsense.

## The table comes first
Put every campaign (or ad set, or ad) in ONE table, whatever platform it came from, with the same columns:
spend · impressions · clicks · CTR · CPC · conversions · CPA · ROAS · frequency. Two rules make the table honest:

1. **Recompute every ratio from its parts.** Platforms disagree about whether CTR is a fraction or a percentage
   and whether spend is in whole currency or millionths. CPA is spend ÷ conversions, computed by you, every time.
2. **A metric the platform does not publish is UNMEASURED, never 0.** Write it as unmeasured and say so in the
   summary. A zero in a column nobody measured is the single most common way an ad report lies.

Write the platform's own conversion definition next to its rows. "48 conversions" means something different on
each platform, and a cross-platform CPA comparison is only honest when both definitions are on the page.

## The data floor: the rule that separates analysis from noise
Decide the minimums BEFORE you look, state them in the answer, and hold to them. A workable set:

- 1,000 impressions, 50 clicks and a floor of real spend before a row can be judged at all.
- 10 conversions before you compare its CPA to anything.
- A row with **zero** conversions is only a loser once it has spent about two account CPAs; a row with a few
  conversions, once it has spent about two account CPAs for each conversion it produced, plus one.

Everything below the floor goes in an **insufficient data** bucket with what it lacks and what to wait for. It is
never "pause it": killing an under-delivered row is how a winner gets buried before it ever gets a chance.

**The asymmetry that matters:** the evidence needed to STOP spending is not the evidence needed to spend MORE. A
row that has burned five account CPAs for one conversion is a measured loser at any conversion count. The same row
can never be called a winner on that data.

## The other four rules
- **A platform you could not read is named as unreadable.** Its numbers are missing, not zero, and no budget moves
  away from it on the strength of an absence.
- **Learning phase.** A Meta ad set still calibrating is not a verdict, and editing it restarts the learning. Leave
  it alone and say when to look again.
- **Days are the account's own days.** Every platform cuts its window on its own midnights. Never present two
  platforms' windows as hour-aligned.
- **Do not pause what is already paused,** and if the best row in the table is switched off, say plainly that the
  recommendation is to switch it back on.

## What a recommendation must contain
The row, its own numbers as evidence, the reason in one or two sentences, and the concrete next move with the
number in it ("raise the daily budget from 25 to 40 and re-read CPA in 3 days"). A recommendation that cites a
number not in the table is the failure mode to watch for, so check each one back against the row before you send it.

## What a test must contain
One variable (creative, audience, bid, budget, placement, landing page or offer), a hypothesis the numbers already
support, a success metric WITH a number, a budget and a duration. "Test new creative" is not a test.

## Before you send it
Re-read every number in the answer against the table. Every recommendation that moves money (a budget change, a
pause, switching something back on) is a proposal: show it to the person who owns the account and get an explicit
yes before anyone applies it.
