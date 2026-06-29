---
name: memory-curator
description: Update cspr preference memory from accumulated feedback and recent newspaper outcomes.
---

# memory-curator

Use this skill after the user has provided feedback or after several runs.

Workflow:

1. Read `~/.cspr/state/feedback.jsonl`.
2. Read recent newspaper outputs when useful.
3. Read current `~/.cspr/memory/profile.yaml`.
4. Update topics, source preferences, and disliked patterns.
5. Write a complete updated profile to a run folder.
6. Apply it with:

    prefmem update --in RUN/profile.yaml

Feedback actions include `save`, `more`, `less`, and `hide-source`. Keep updates conservative and avoid overfitting from one reaction.

