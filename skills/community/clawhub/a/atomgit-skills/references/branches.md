# Branches

Read this file for branch lookup, branch creation, and branch protection rules.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| List branches | `atomgit_get_repository_branches` |
| Inspect one branch | `atomgit_get_repository_branch` |
| Create a branch | `atomgit_create_repository_branch` |
| List branch protection rules | `atomgit_get_branch_protection_rules` |
| Create a protection rule | `atomgit_create_branch_protection_rule` |
| Update a protection rule | `atomgit_update_branch_protection_rule` |

## Typical Flow

1. Inspect the current branch or protection rules first.
2. Create the branch from a known ref or commit SHA.
3. Confirm review-count and status-check changes before modifying shared-branch protection.
