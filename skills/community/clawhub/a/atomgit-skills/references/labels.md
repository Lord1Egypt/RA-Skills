# Labels

Read this file for repository labels and for applying labels to issues or pull requests.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| List repository labels | `atomgit_get_repository_labels` |
| Create a repository label | `atomgit_create_repository_label` |
| Update a repository label | `atomgit_update_repository_label` |
| Replace all repository labels | `atomgit_replace_all_repository_labels` |
| Add labels to an issue | `atomgit_create_repository_issue_label` |
| Replace issue labels | `atomgit_replace_repository_issue_all_labels` |
| Add labels to a pull request | `atomgit_create_repository_pull_label` |
| Read pull request labels | `atomgit_get_repository_pull_labels` |
| Replace pull request labels | `atomgit_replace_repository_pull_labels` |

## Typical Flow

1. Inspect existing repository labels before creating or renaming labels.
2. Use repository label endpoints for taxonomy changes.
3. Use issue or pull-request label endpoints for per-item labeling.
