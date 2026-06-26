# Canonical Policy

This document is the source of truth for the dependency guardrail.

## Purpose

Reduce software supply-chain risk before dependency changes land in manifests, lockfiles, or generated install commands.

## Scope

Apply this policy whenever an agent proposes or performs any of the following:

- add a new dependency
- upgrade an existing dependency to a materially different version
- introduce a transient install command such as `npx`, `pnpm dlx`, or `uvx`
- replace one package with another
- justify retaining a risky dependency during review

## Required Behavior

1. Do not add or upgrade a dependency without a Socket review first.
2. Prefer existing project capabilities or standard-library implementations over new packages.
3. Review manifest and lockfile changes together.
4. Treat install scripts, obfuscation, privileged capabilities, typosquatting indicators, and unusual maintainer patterns as escalation triggers.
5. If the dependency cannot be reviewed because tooling is unavailable, require human review before proceeding.

## Preferred Tooling Order

1. MCP `depscore`
2. Socket CLI package inspection
3. Human review when neither is available

## Required Pre-Change Summary

Before applying the dependency change, the agent must state:

- why the package is needed
- whether an existing alternative exists
- what the score or report showed
- whether the package adds transitive risk
- whether install scripts or risky capabilities are present

## Risk Signals To Watch

Treat the following as significant risk indicators even if the package is popular:

- critical or high alerts
- low supply-chain, vulnerability, maintenance, quality, or license scores
- install scripts such as `preinstall`, `install`, or `postinstall`
- capabilities such as shell, filesystem, network, environment-variable, eval, or unsafe access
- large unexpected transitive dependency trees
- suspicious naming or publisher patterns

## Expected Outcome

Every dependency review should end with one of these outcomes:

- `allow`
- `allow_with_warning`
- `block_pending_human_review`
- `block`

Use `decision-matrix.md` to assign the outcome.
