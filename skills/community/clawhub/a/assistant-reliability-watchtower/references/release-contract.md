# ARW RC1 release contract

## What ARW is

ARW is a deterministic reliability watchtower for assistant workflows.

It runs probe suites, writes machine-readable artifacts, builds operator digests, emits immediate severe alerts, and fail-closes when reporting evidence is missing or malformed.

## What RC1 means

RC1 means ARW has a clean, installable OpenClaw skill surface for internal use.

An RC1 build should let an operator:
- run smoke probes,
- generate a digest,
- validate scorecard evidence,
- render the delivery preamble,
- and understand the current probe/config surface without reading the whole repository.

## What RC1 is not

RC1 is not:
- a fully generalized public monitoring platform,
- a promise of environment-agnostic deployment everywhere,
- or justification for endless new self-referential evidence gates.

## Anti-goals

- Do not expand beyond ARW-only scope.
- Do not leak private environment-specific adapters into the skill contract.
- Do not treat more timestamp anomaly gates as automatic release progress.

## Success signal

RC1 is complete when the skill package validates, the wrapper paths work, the probe/config/release docs exist, and recurring ARW cycles can recognize completion and alert `<@246113117183016960>` with proof.
