# Search

Read this file for AtomGit-wide repository, issue, and user search workflows.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| Search repositories | `atomgit_search_repositories` |
| Search issues | `atomgit_search_issues` |
| Search users | `atomgit_search_users` |

## Typical Flow

1. Use search when the request does not already contain a trusted `owner` and `repo`.
2. Narrow the result set before moving into repository-scoped endpoints.
