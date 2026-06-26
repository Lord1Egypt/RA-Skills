# Game Types and Core Loops

Use this file to quickly map user intent to the right game structure.

## Genre-to-Loop Mapping

| Genre | Core Loop | First Vertical Slice |
|-------|-----------|----------------------|
| Endless runner | avoid obstacles -> collect -> increase speed | one lane set, one obstacle family, score and restart |
| Arena shooter | move -> shoot -> survive wave -> upgrade | one arena, one enemy type, one weapon, one upgrade |
| Puzzle | observe -> test move -> validate pattern | one puzzle mechanic with 10 handcrafted levels |
| Platformer | move -> jump -> avoid hazard -> reach exit | one level with one enemy and one checkpoint |
| Idle/incremental | trigger action -> earn -> automate -> scale | one resource, one upgrade tree branch |
| Tactical turn-based | choose action -> resolve turn -> reposition | one map, one enemy squad, one objective |

## Loop Design Checks

- Can players understand the objective within 20 seconds?
- Is failure readable and attributable to player decisions?
- Is retry friction low enough for rapid learning?
- Does one additional mastery skill emerge after three sessions?

## Difficulty Curve Baseline

- Early game teaches one mechanic at a time.
- Mid game combines learned mechanics with controlled variance.
- Late game introduces pressure, not random unfairness.

## Scope Control

Start with one of each:
- one enemy class or challenge primitive
- one progression vector
- one reward feedback style
- one visual identity motif

Expand only after retention signals improve in playtests.
