---
name: Codex Owner Move E2E
summary: Temporary skill that documents a realistic owner migration validation workflow.
---

# Codex Owner Move E2E

Use this temporary skill to validate that a ClawHub skill can be published under a personal owner, moved to an organization owner with an explicit migration flag, inspected after the move, and removed during cleanup.

## When to use

Run this only for maintainer validation of the skill owner migration flow. It is intentionally scoped to a throwaway slug and should not be installed by users.

## Procedure

1. Publish version 0.0.1 under the authenticated personal publisher.
2. Publish version 0.0.2 with the OpenClaw owner selected and the migration opt-in enabled.
3. Inspect the skill and verify that the latest version is 0.0.2.
4. Delete the temporary skill after validation completes.

## Expected behavior

The publish operation should preserve the same skill record while changing the owner publisher. Existing version history, stats, aliases, and audit history should remain attached to the skill. If the migration flag is missing, the backend should reject the owner change instead of silently transferring ownership.
