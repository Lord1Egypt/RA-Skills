---
name: gaming-backlog-guide
description: Match the user’s current mood, available time, platform habits, and energy level to the right kind of game experience, then suggest a low-friction way to start. Use when the user feels game paralysis or wants a healthier way to choose what to play next.
---

# Gaming Backlog Guide

Chinese name: 游戏荒推荐指南

## Purpose
Help the user find the right kind of game experience for the current moment instead of doom-scrolling the backlog or starting something that does not fit the available time and energy.
This skill is descriptive only. It does not fetch live release news, store prices, or review scores.

## Use this skill when
- The user wants to play something but cannot choose.
- The user feels low energy, bored, or stuck in backlog guilt.
- The user wants a game direction that fits tonight, the weekend, or a tight schedule.
- The user wants a better leisure match instead of a giant title dump.

## Inputs to collect
- Current mood
- Available play time
- Platform habits
- Budget or backlog pressure
- Recently played genres
- Desired experience or feeling

## Workflow
1. Read mood, energy, time, platform, and budget signals.
2. Infer the kind of experience the user actually needs right now.
3. Recommend 2 to 3 game directions, not a random pile of titles.
4. Separate a play-now option, a weekend option, and one type to avoid for now.
5. End with one easiest-start suggestion.

## Output Format
- Current need profile
- Best-fit directions
- Start here
- Avoid for now
- Tonight’s easiest start

## Quality bar
- The recommendation must match time and energy honestly.
- The output should emphasize experience fit, not title spam.
- Include at least one option the user can start with low friction.
- Stay honest about not having live launch or pricing data.

## Edge cases and limits
- If the user wants brand-new release news, explain that this skill does not provide real-time launch data.
- If budget is tight, prefer backlog, free, or low-cost directions.
- This skill does not replace reviews, sale tracking, or purchasing guidance.

## Compatibility notes
- Works for solo leisure planning, family play, and reward-based downtime.
- Can pair conceptually with gaming-session-scheduler.
- Fully dialogue-based, no store integration required.
