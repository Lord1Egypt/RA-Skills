# Quickstart

## What to upload

In the ClawHub publish UI, choose the whole folder:

`publish/diagforge-bootstrap`

Do not upload the whole DiagForge repository.

## Suggested publish values

- Slug:
  `diagforge-bootstrap`
- Display name:
  `DiagForge Bootstrap`
- Version:
  `0.1.2`
- Tags:
  `latest`

## Suggested changelog

`Refined bootstrap guidance and clarified local Visio bridge token usage.`

## Token clarification

If the review UI flags `VISIO_BRIDGE_TOKEN` as sensitive, the intended meaning is:

- it is a local token for the user's own DiagForge Visio bridge
- it is not required for cloning or reading the repository
- it is only needed for the bridge-backed smoke test and execution flow
- users should verify the upstream GitHub repository before setting any local token

## Important license note

Skills published on ClawHub are published under MIT-0.
This package is intentionally lightweight so that the full GitHub repository does not need to be republished there.
