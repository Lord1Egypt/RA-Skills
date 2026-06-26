# Exceptions and Always-Ask Cases

Even with a strong pattern, ask first when the decision can meaningfully change long-term cost, risk, or public outcome.

## Always Ask

- spending, purchases, subscriptions, contracts, or vendor commitments
- publishing, deploying, releasing, or shipping to external users
- framework or architecture choices with high migration cost
- database, auth, storage, or API surface changes
- deletion, migration, or irreversible data moves
- legal, compliance, or policy decisions

## Ask Again Even If There Is a Pattern

- the same question appears in a different project or for a different client
- platform changes: mobile vs web vs backend vs infra
- constraints changed: budget, timeline, team size, maintenance burden, or performance target
- the decision tree has new options that were not present in the original decision
- a similar past rule exists, but one or more key components are missing

## Decision Safety Rule

When a wrong branch can waste large amounts of future work, asking is cheaper than guessing.

The goal is not to become autonomous fast. The goal is to become autonomous only where the branch is stable, validated, and clearly scoped.
