# Issues

Read this file for issue triage, issue creation, issue comments, repository issues, and issue-to-PR navigation.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| List repository issues | `atomgit_get_repository_issues` |
| Inspect one issue | `atomgit_get_repository_issue` |
| Create an issue | `atomgit_create_repository_issue` |
| Update or close an issue | `atomgit_update_repository_issue` |
| Read issue comments | `atomgit_get_repository_issue_comments` |
| Add an issue comment | `atomgit_create_repository_issue_comment` |
| Inspect issue reactions | `atomgit_get_repository_issue_reactions` |
| Inspect issue operation logs | `atomgit_get_repository_issue_operate_logs` |
| Inspect issue modify history | `atomgit_get_repository_issue_modify_history` |
| Read issue-linked pull requests | `atomgit_get_repository_issue_pull_requests` |
| List current user issues | `atomgit_get_user_issues` |
| List organization issues | `atomgit_get_organization_issues` |
| List enterprise issues | `atomgit_get_enterprise_issues` |
| List enterprise issues v8 | `atomgit_get_enterprise_issues_v8` |

## Typical Flow

1. Inspect existing labels and milestones before creating a new issue.
2. Use `atomgit_create_repository_issue` with the final title and body.
3. Prefer `atomgit_create_repository_issue_comment` for follow-up context instead of overwriting history.
