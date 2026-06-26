# Commit Guidelines

## Good commit boundaries

A good commit usually represents one of these:
- one feature slice
- one bug fix
- one refactor with no extra feature work
- one documentation-only update
- one test-only update

## Signs a commit is too broad

- it mixes schema, renderer, and unrelated tooling changes
- it contains both core logic and opportunistic cleanup
- it introduces a feature and a separate follow-up behavior
- it cannot be explained in one sentence

## Recommended response when too broad

Propose a split like:
- commit 1: scaffolding or model change
- commit 2: UI or behavior change
- commit 3: tests or docs if needed

## Message examples

`feat(schema): add runtime node dto definitions`

`feat(renderer): render recursive node tree from children map`

`fix(history): avoid recording viewport-only changes`

`docs(progress): add execution update for queue planning`
