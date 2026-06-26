---
name: game-inventory-manager
description: Sort clutter, obligations, files, objects, or attention drains through a game inventory lens. Classify what should stay equipped, stay in quick access, move to storage, be sold or delegated, be discarded or archived, or be combined into higher-value batches. Use when the user feels overloaded by too many items, tasks, or commitments and needs a practical first cleanup move.
---

# Game Inventory Manager

Chinese name: 游戏背包整理.

## Overview

Use this skill to reduce complexity instead of creating a prettier pile. It helps the user classify what deserves active attention, what should be stored, and what is only occupying scarce space or energy.

## When to use

Use this skill when the user wants to:
- declutter physical or digital items
- triage too many tasks or obligations
- reduce low-value attention drains
- decide what to keep, park, combine, delegate, or remove
- find one 10 to 20 minute cleanup action

### Example prompts
- "Sort this messy to-do list like a game inventory"
- "Help me decide what stays in active use and what should leave"
- "I feel overloaded by files, errands, and random obligations"

## Inputs

Useful inputs include:
- list of items, tasks, files, or commitments
- what feels heavy, urgent, or emotionally sticky
- value, frequency of use, and replacement cost
- time or energy constraints

## Workflow

1. Review the current inventory.
2. Sort items into equipped, quick access, storage, sell or delegate, discard or archive, and craft or combine.
3. Explain the sorting logic.
4. Pick the highest-value slot to clear first.
5. End with one short cleanup action.

## Output

Return markdown with:
- backpack status overview
- sorted inventory by category
- first slot to clear
- craft suggestions
- one cleanup move under 20 minutes

## Limits

- This skill does not delete files, move objects, or spend money automatically.
- It should not force emotionally loaded items into an immediate discard decision.
- Mixed physical and digital clutter may need separate passes.

## Acceptance Criteria

- The output reduces complexity.
- The classification logic is visible.
- At least one realistic cleanup action fits inside 10 to 20 minutes.
