# Repositories

Read this file for repository lookup, repository metadata, files, forks, events, and repository-scoped settings.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| Inspect one repository | `atomgit_get_repository` |
| List current user repositories | `atomgit_get_current_user_repos` |
| List repositories for a user | `atomgit_get_user_repos` |
| List repositories for an organization | `atomgit_get_organization_repositories` |
| Create a personal repository | `atomgit_create_user_repository` |
| Create an organization repository | `atomgit_create_organization_repository` |
| Update repository metadata | `atomgit_update_repository` |
| Fork a repository | `atomgit_fork_repository` |
| Read a path | `atomgit_get_repository_content` |
| Read raw file content | `atomgit_get_repository_raw_file` |
| List files | `atomgit_get_repository_file_list` |
| Inspect a tree | `atomgit_get_repository_tree` |
| Read a blob | `atomgit_get_repository_blob` |
| Create a file | `atomgit_create_repository_file` |
| Update a file | `atomgit_update_repository_file` |
| Upload a file asset | `atomgit_upload_repository_file` |
| Inspect settings | `atomgit_get_repository_settings` |
| Update settings | `atomgit_update_repository_settings` |
| Inspect languages | `atomgit_get_repository_languages` |
| Inspect contributors | `atomgit_get_repository_contributors` |
| Inspect forks | `atomgit_get_repository_forks` |
| Inspect events | `atomgit_get_repository_events` |
| Inspect stargazers | `atomgit_get_repository_stargazers` |
| Inspect subscribers | `atomgit_get_repository_subscribers` |

## Typical Flow

1. If `owner` is unknown, use `atomgit_get_current_user`, `atomgit_get_current_user_repos`, or `atomgit_search_repositories`.
2. Use `atomgit_get_repository` once both `owner` and `repo` are known.
3. For file edits, fetch the current file metadata first so you have the latest `sha`.
