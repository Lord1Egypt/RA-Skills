# OpenClaw Plugin Issue Findings

Generated: deterministic
Status: PASS

## Triage Summary

| Metric                     | Value |
| -------------------------- | ----- |
| Issue findings             | 2     |
| Open issue findings        | 2     |
| Runtime-covered findings   | 0     |
| Runtime-partial findings   | 0     |
| P0                         | 0     |
| P1                         | 0     |
| Open P0                    | 0     |
| Open P1                    | 0     |
| Live issues                | 0     |
| Live P0 issues             | 0     |
| Compat gaps                | 0     |
| Deprecation warnings       | 0     |
| Inspector gaps             | 0     |
| Open inspector gaps        | 0     |
| Runtime coverage artifacts | 0     |
| Upstream metadata          | 2     |
| Contract probes            | 2     |

## Triage Overview

| Class               | Count | P0 | Meaning                                                                                                                                                  |
| ------------------- | ----- | -- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| live-issue          | 0     | 0  | Potential runtime breakage in the target OpenClaw/plugin pair. P0 only when it is not a deprecated compat seam.                                          |
| compat-gap          | 0     | -  | Compatibility behavior is needed but missing from the target OpenClaw compat registry.                                                                   |
| deprecation-warning | 0     | -  | Plugin uses a supported but deprecated compatibility seam; keep it wired while migration exists.                                                         |
| inspector-gap       | 0     | -  | Plugin Inspector needs stronger capture/probe evidence before making contract judgments. Runtime-covered rows are proof-backed and not open report work. |
| upstream-metadata   | 2     | -  | Plugin package or manifest metadata should improve upstream; not a target OpenClaw live break by itself.                                                 |
| fixture-regression  | 0     | -  | Fixture no longer exposes an expected seam; investigate fixture pin or scanner drift.                                                                    |

## P0 Live Issues

_none_

## Other Live Issues

_none_

## Compat Gaps

_none_

## Deprecation Warnings

_none_

## Inspector Proof Gaps

_none_

## Runtime-Covered Inspector Gaps

_none_

## Upstream Metadata Issues

- P2 **openclaw-apple-mail-skill** `upstream-metadata` `plugin-upstream-fix`
  - **package-openclaw-entry-missing**: openclaw-apple-mail-skill: OpenClaw package entrypoint metadata is missing
  - state: open · compat:none
  - evidence:
    - package.json

- P2 **openclaw-apple-mail-skill** `upstream-metadata` `plugin-upstream-fix`
  - **package-plugin-api-compat-missing**: openclaw-apple-mail-skill: plugin API compatibility range is missing
  - state: open · compat:none
  - evidence:
    - package.json

## Issues

- P2 **openclaw-apple-mail-skill** `upstream-metadata` `plugin-upstream-fix`
  - **package-openclaw-entry-missing**: openclaw-apple-mail-skill: OpenClaw package entrypoint metadata is missing
  - state: open · compat:none
  - evidence:
    - package.json

- P2 **openclaw-apple-mail-skill** `upstream-metadata` `plugin-upstream-fix`
  - **package-plugin-api-compat-missing**: openclaw-apple-mail-skill: plugin API compatibility range is missing
  - state: open · compat:none
  - evidence:
    - package.json

## Contract Probe Backlog

- P2 **openclaw-apple-mail-skill** `package-loader`
  - contract: Package metadata declares the OpenClaw plugin API range used by the plugin.
  - id: `package.compat.plugin-api-range:openclaw-apple-mail-skill`
  - evidence:
    - package.json

- P2 **openclaw-apple-mail-skill** `package-loader`
  - contract: OpenClaw package metadata declares entrypoints for cold import and registration capture.
  - id: `package.entrypoint.openclaw-metadata:openclaw-apple-mail-skill`
  - evidence:
    - package.json
