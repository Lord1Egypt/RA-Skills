---
name: Codex Owner Move Debug
summary: Temporary skill that documents a realistic owner migration validation workflow.
---

# Codex Owner Move Debug

This temporary skill validates the owner migration flow during PR review. It is a realistic documentation body so the normal quality gate can run. The skill is created, moved between publishers, inspected, and deleted.

## Procedure

Publish under the personal owner, then publish a second version under the OpenClaw owner with the migration flag. The expected result is a preserved skill record with updated owner metadata and version history.

## Cleanup

The skill is deleted after validation. It should not be installed or referenced by users.
