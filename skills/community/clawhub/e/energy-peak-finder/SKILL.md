---
name: energy-peak-finder
description: Turn several days of observation into a simple energy pattern review with likely peak windows, low windows, disruptors, task matching, and a one-week experiment. Use when the user wants to schedule deep work, admin, recovery, and social tasks around real energy patterns instead of guesswork.
---

# Energy Peak Finder

## Overview

Use this skill to spot when the user's energy actually supports focus, creativity, stamina, and recovery. It helps the user observe repeated peaks and troughs, separate sustainable energy from urgency or caffeine spikes, and match task types to the most realistic time windows.

This skill is descriptive only. It does not use wearables, calendars, biometrics, or analytics backends.

## Trigger

Use this skill when the user wants to:
- find their best window for deep work
- understand daily energy slumps
- distinguish true energy from urgency or caffeine buzz
- match task type to time of day
- run a one-week experiment before locking in a schedule

### Example prompts
- "Help me figure out when my energy peaks"
- "I keep doing hard work at the wrong time of day"
- "Map my focus windows from these notes"
- "Turn my energy observations into a weekly experiment"

## Workflow

1. Review several days of energy, alertness, mood, hunger, and interruptions.
2. Divide the day into simple time blocks.
3. Identify repeated peaks, troughs, and false peaks.
4. Note confounders like sleep, meals, workouts, caffeine, and interruptions.
5. Match task types to each energy band.
6. Suggest a one-week experiment to validate the pattern.

## Inputs

The user can provide any mix of:
- notes about mornings, afternoons, and evenings
- focus, creativity, stamina, or crash periods
- sleep quality, meals, caffeine, or workout context
- interruptions from work or family
- task types that feel easier or harder at different times
- notes from several days or one rough week

## Outputs

Return a markdown energy review with:
- observation summary
- task matching by energy band
- hypotheses about what boosts or drains energy
- one seven-day experiment

## Safety

- Use repeated observations when possible, not one unusually good or bad day.
- Separate energy from mood, panic, or deadline urgency.
- Keep recommendations flexible when family, health, or work obligations limit ideal scheduling.
- Do not turn the pattern into a fixed identity label too quickly.

## Acceptance Criteria

- Return markdown text.
- Identify a best window, lowest window, and common disruptors.
- Match peak, medium, and low-energy tasks to usable time bands.
- End with a one-week experiment.
