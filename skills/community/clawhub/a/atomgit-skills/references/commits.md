# Commits

Read this file for commit history, commit inspection, commit diffs, commit comments, and commit comparisons.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| List commits | `atomgit_get_repository_commits` |
| Inspect one commit | `atomgit_get_repository_commit` |
| Compare two commits | `atomgit_compare_repository_commits` |
| Read commit diff | `atomgit_get_repository_commit_diff` |
| Read commit patch | `atomgit_get_repository_commit_patch` |
| Read commit comments | `atomgit_get_repository_commit_comments` |
| Read one commit comment | `atomgit_get_repository_commit_comment` |
| Create a commit comment | `atomgit_create_repository_commit_comment` |
| Update a commit comment | `atomgit_update_repository_commit_comment` |
| Read commit-ref comments | `atomgit_get_repository_commit_ref_comments` |
| Read commit statistics | `atomgit_get_repository_commit_statistics` |

## Typical Flow

1. Use `atomgit_get_repository_commits` or `atomgit_get_repository_commit` to locate the target SHA.
2. Use diff or patch endpoints when the user needs exact change content.
3. Use `atomgit_compare_repository_commits` for range-based review instead of fetching both commits separately.
