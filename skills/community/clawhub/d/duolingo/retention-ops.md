# Multi-Topic Retention Operations

Retention must work for one or many active topics.

## Daily Planner

At session start:
1. choose topic from rotation policy
2. serve one fast win
3. serve one review item
4. queue next due action

## Rotation Policies

| Policy | Use when | Example |
|--------|----------|---------|
| Alternating days | two balanced priorities | Mon english, Tue cooking |
| Weighted split | one primary topic | 70 percent english, 30 percent cooking |
| Daily stack | short sessions available | english loop then cooking loop |

## Review Queue Rules

- Reviews are scheduled from misses and low-confidence passes.
- Each topic keeps its own queue in `topics/<slug>/queue.md`.
- Daily planner should include at least one review before new content.

## Comeback Triggers

- Day 1 miss: lightweight reminder and one easy loop.
- Day 3 miss: restart with guided recap.
- Day 7 miss: rebuild momentum with a mini-checkpoint.

## Weekly Reset

Weekly operations:
- archive completed queue items
- rebalance topic rotation
- review checkpoint outcomes
- adjust next-week loop targets
