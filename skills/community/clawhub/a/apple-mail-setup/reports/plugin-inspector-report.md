# OpenClaw Plugin Compatibility Report

Generated: deterministic
Status: PASS

## Summary

| Metric                     | Value |
| -------------------------- | ----- |
| Fixtures                   | 1     |
| High-priority fixtures     | 1     |
| Hard breakages             | 0     |
| Warnings                   | 2     |
| Compatibility suggestions  | 0     |
| Issue findings             | 2     |
| Open issue findings        | 2     |
| Runtime-covered findings   | 0     |
| Runtime-partial findings   | 0     |
| P0 issues                  | 0     |
| P1 issues                  | 0     |
| Open P0 issues             | 0     |
| Open P1 issues             | 0     |
| Live issues                | 0     |
| Live P0 issues             | 0     |
| Compat gaps                | 0     |
| Deprecation warnings       | 0     |
| Inspector gaps             | 0     |
| Open inspector gaps        | 0     |
| Runtime coverage artifacts | 0     |
| Upstream metadata          | 2     |
| Contract probes            | 2     |
| Decision rows              | 2     |

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

## Hard Breakages

_none_

## Target OpenClaw Compat Records

| Metric                   | Value    |
| ------------------------ | -------- |
| Configured path          | -        |
| Status                   | disabled |
| Compat registry          | -        |
| Compat records           | 0        |
| Compat status counts     | -        |
| Record ids               | -        |
| Hook registry            | -        |
| Hook names               | 0        |
| API builder              | -        |
| API registrars           | 0        |
| Captured registration    | -        |
| Captured registrars      | 0        |
| Package metadata         | -        |
| Plugin SDK exports       | 0        |
| Manifest types           | -        |
| Manifest fields          | 0        |
| Manifest contract fields | 0        |

## Warnings

| Fixture                   | Code                              | Level   | Message                                                       | Evidence     | Compat record |
| ------------------------- | --------------------------------- | ------- | ------------------------------------------------------------- | ------------ | ------------- |
| openclaw-apple-mail-skill | package-plugin-api-compat-missing | warning | package openclaw metadata does not declare compat.pluginApi   | package.json | -             |
| openclaw-apple-mail-skill | package-openclaw-entry-missing    | warning | package openclaw metadata does not declare plugin entrypoints | package.json | -             |

## Suggestions To OpenClaw Compat Layer

_none_

## Issue Findings

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

## Fixture Seam Inventory

| Fixture                   | Priority | Seams           | Hooks | Registrations | Manifest contracts |
| ------------------------- | -------- | --------------- | ----- | ------------- | ------------------ |
| openclaw-apple-mail-skill | high     | plugin-metadata | -     | -             | -                  |

## Decision Matrix

| Fixture                   | Decision            | Seam               | Action                                                                                                               | Evidence     |
| ------------------------- | ------------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------- | ------------ |
| openclaw-apple-mail-skill | plugin-upstream-fix | package-metadata   | Ask the plugin to declare the plugin API range it was built against.                                                 | package.json |
| openclaw-apple-mail-skill | plugin-upstream-fix | package-entrypoint | Ask the plugin to declare openclaw.extensions or runtimeExtensions so cold import can target the correct entrypoint. | package.json |

## Raw Logs

| Fixture                   | Code                        | Level | Message                                                                               | Evidence                                                          | Compat record |
| ------------------------- | --------------------------- | ----- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ------------- |
| openclaw-apple-mail-skill | seam-inventory              | log   | observed 0 hooks, 0 registrations, and 0 manifest contracts                           | -                                                                 | -             |
| openclaw-apple-mail-skill | package-metadata            | log   | selected package metadata for plugin contract checks                                  | package.json, @jehadurre/openclaw-apple-mail-skill, version:1.0.1 | -             |
| openclaw                  | target-openclaw-unavailable | log   | target OpenClaw checkout was not available, so compat record coverage was not checked | not configured                                                    | -             |
