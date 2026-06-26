# Patch Discipline
#tags: skills review

## Rule
If the review target is a real artifact and the consultant surfaces a real improvement, patch the artifact before the next round.

## Safety gate
For `skill-rewrite`, `skill-hardening`, and `artifact-improvement`:
- emit `DRY_RUN: ready` before mutation
- patch the artifact
- emit `APPLY: done` after mutation
- emit the updated `PATCH_MANIFEST`

## Allowed patch forms
- direct file edit
- exact rewritten section
- explicit implementation-grade plan if the artifact cannot be edited yet

## What to patch first
1. runtime contract changes
2. safety and stop rules
3. weak-model flow and routing
4. docs split
5. tests and validation
6. packaging or publish details

## What not to do
- do not stop with only a suggestion list when a real fix is accepted
- do not ask the user to decide whether to patch while the review loop is active
- do not hide the accepted change in a later summary

## Version bump rule
- use `patch` for docs, examples, fixtures, and tests that do not change runtime behavior
- use `minor` for routing, runtime contract, recovery, safety, or validation behavior changes that remain backward-compatible
- use `major` for breaking mode changes, schema changes, or incompatible round-output changes

## Patch record
Record the accepted change in the round output block, in the patch manifest, and in the log line.
