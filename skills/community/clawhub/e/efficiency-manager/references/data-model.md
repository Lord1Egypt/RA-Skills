# Data Model

## Current Shared Storage

- Events: `~/.openclaw/efficiency-manager/data/events.json`
- Config: `~/.openclaw/efficiency-manager/config.json`

All agents should use the same shared store.

## Current Normalized Event Shape

Core fields used today:
- `id`
- `description`
- `category`
- `startTime`
- `endTime`
- `status`
- `notes`
- `tags`
- `createdAt`
- `updatedAt`

## Compatibility Notes

The storage layer already normalizes older records such as:
- `title` -> `description`
- `from` and `to` plus `date` -> `startTime` and `endTime`
- some Chinese category names -> normalized categories

## Current Category Set

Stable categories today:
- `work`
- `study`
- `exercise`
- `social`
- `family`
- `rest`
- `entertainment`
- `chores`
- `other`

If categories change in the future, keep:
- config defaults
- category mappings
- reporter labels
- scheduler defaults

aligned with each other.

## Recommended Future Fields

These fields are useful for turning the skill into a stronger execution coach:
- `importance`
- `urgency`
- `energyBefore`
- `energyAfter`
- `interruptions`
- `outcomeScore`
- `planned`
- `deadline`
- `source`
- `taskId`

Treat them as optional extensions until the code formally supports them everywhere.
