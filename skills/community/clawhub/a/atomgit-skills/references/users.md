# Users

Read this file for current-user profile data, user lookup, emails, SSH keys, subscriptions, namespaces, and user-scoped repository views.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| Inspect current user | `atomgit_get_current_user` |
| Update current user profile | `atomgit_update_current_user` |
| Inspect another user | `atomgit_get_user` |
| Read current user emails | `atomgit_get_current_user_emails` |
| Read current user keys | `atomgit_get_current_user_keys` |
| Read one user key | `atomgit_get_user_key` |
| Add a user key | `atomgit_add_user_key` |
| Read current user namespace | `atomgit_get_current_user_namespace` |
| Read current user namespaces | `atomgit_get_current_user_namespaces` |
| Read current user organizations | `atomgit_get_current_user_organizations` |
| Read current user pull requests | `atomgit_get_current_user_pull_requests` |
| Read current user starred repositories | `atomgit_get_current_user_starred_repos` |
| Read current user subscriptions | `atomgit_get_current_user_subscriptions` |
| Read user events | `atomgit_get_user_events` |
| Read user organizations | `atomgit_get_user_organizations` |
| Read user repositories | `atomgit_get_user_repos` |
| Read user starred repositories | `atomgit_get_user_starred_repos` |
| Read user subscriptions | `atomgit_get_user_subscriptions` |

## Notes

- Use current-user endpoints when the request is about "me" or "my".
- Use user-specific endpoints when the request names another AtomGit account.
