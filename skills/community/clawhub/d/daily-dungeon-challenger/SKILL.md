---
name: daily-dungeon-challenger
description: Reframe a day into a main dungeon and side quests with clear win conditions, time budgets, fallback modes, and reward prompts. Use for daily planning, morning starts, midday replans, or low-energy recovery.
---

# Daily Dungeon Challenger

Chinese name: 每日副本挑战

## Purpose
Turn an ordinary day into a game-like dungeon run so the user can see what matters, what can wait, and how to keep moving when energy drops.
This skill is descriptive only. It does not create calendar events or call external systems.

## Use this skill when
- The user has too many tasks and needs a clear main challenge for today.
- The user wants a morning launch plan, midday replan, or evening rescue version.
- The user is procrastinating because the day feels shapeless.
- The user wants a realistic plan that still feels motivating.

## Inputs to collect
- Available time today
- Current energy level or focus capacity
- Must-do items
- Nice-to-progress items
- Urgent interruptions or fixed constraints
- Preferred reward or rest style

## Workflow
1. Collect the user's available time, energy bar, required tasks, and optional progress tasks.
2. Map the day into one main dungeon, one to three side quests, a supply phase, and a failure floor.
3. For each dungeon element, define the title, win condition, time budget, reward drop, and retreat rule.
4. If surprise tasks arrive or energy collapses, rewrite the run as a simplified dungeon mode.
5. End with a minimum viable win line so the user still knows how to salvage the day.

## Output Format
- Today's dungeon overview with one main dungeon and one to three side quests.
- Clear completion rules, recommended order, and time budget for each item.
- A fallback mode with minimum success criteria and damage control steps.
- At least one reward, recovery, or reflection prompt after completion.

## Quality bar
- The main dungeon must be concrete enough that success is obvious.
- Total task load must match real energy and available time.
- Always include what to do if the user cannot finish the ideal version.
- Avoid fantasy scheduling and overload.

## Edge cases and limits
- If the user is already overloaded, output a retreat build instead of adding more challenge.
- If urgent items interrupt the plan, allow the dungeon order to change immediately.
- Do not present this as a replacement for formal project management software.

## Compatibility notes
- Works for morning planning, midday replanning, and evening rescue mode.
- Can connect conceptually with boss-battle-calendar or quest-chain-decomposer for larger arcs.
- Text only, no calendar sync required.
