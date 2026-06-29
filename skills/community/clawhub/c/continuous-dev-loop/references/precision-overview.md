# Precision Overview

The precision layer is optional.

Its job is to improve observability and supervisor control without changing core protocol truth.

## Precision Capabilities

Precision MAY define:

- project defaults through `profile.json`
- runtime tuning through `tuning.json`
- advisory scoring
- advisory review cadence
- metrics and trend tracking
- optional hook execution

## Hard Rules

- Precision MUST NOT replace the footer contract.
- Precision MUST NOT replace core stop rules.
- Precision MUST NOT invent a new continuation status model.
- Precision MUST NOT stop or pause a loop by itself.
- Precision MUST degrade safely when missing or unsupported.
- Precision MUST be profile-scoped when logic is language- or stack-specific.
- Precision output MUST be advisory unless a runtime explicitly documents enforcement through repo-local runtime policy.

## Precision Advice Fields

A runtime MAY emit only these advisory precision fields unless it documents additional fields explicitly:

- `ROUND_SCORE`
- `PRECISION_ADVICE`
- `PRECISION_FLAGS`
- `REVIEW_DUE`

These fields are optional. They are not core protocol.

## Advisory Enumerations

- `PRECISION_ADVICE`: `none|warn|pause_review`
- `ROUND_SCORE`: integer `0-100` or `none`
- `REVIEW_DUE`: `true|false`
- `PRECISION_FLAGS`: zero or more short machine-readable flags

## Safe Routing Rule

Precision output is advisory only.

If a runtime chooses to act on advisory output, that behavior MUST be documented outside this skill as explicit repo-local runtime policy.

Any runtime decision to pause or stop based on precision output MUST still map back to core protocol truth and core footer fields.
