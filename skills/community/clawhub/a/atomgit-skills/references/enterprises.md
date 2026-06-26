# Enterprises

Read this file for enterprise members, enterprise issue views, enterprise milestones, enterprise labels, and enterprise-level roles.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| Read enterprise members | `atomgit_get_enterprise_members` |
| Read enterprise members v8 | `atomgit_get_enterprise_members_v8` |
| Inspect one enterprise member | `atomgit_get_enterprise_member` |
| Inspect one enterprise member v8 | `atomgit_get_enterprise_member_v8` |
| Invite an enterprise member | `atomgit_invite_enterprise_member_v8` |
| Update enterprise member permissions | `atomgit_update_enterprise_member_v8` |
| Read enterprise issues | `atomgit_get_enterprise_issues` |
| Read enterprise issues v8 | `atomgit_get_enterprise_issues_v8` |
| Inspect one enterprise issue | `atomgit_get_enterprise_issue` |
| Read enterprise issue comments | `atomgit_get_enterprise_issue_comments` |
| Read enterprise issue labels | `atomgit_get_enterprise_issue_labels` |
| Read enterprise issue statuses | `atomgit_get_enterprise_issue_statuses` |
| Read enterprise issue statuses v5 | `atomgit_get_enterprise_issue_statuses_v5` |
| Read enterprise labels | `atomgit_get_enterprise_labels` |
| Read enterprise pull requests | `atomgit_get_enterprise_pull_requests` |
| Read enterprise milestone list | `atomgit_get_enterprise_milestones_v8` |
| Inspect one enterprise milestone | `atomgit_get_enterprise_milestone_v8` |
| Create an enterprise milestone | `atomgit_create_enterprise_milestone_v8` |
| Update an enterprise milestone | `atomgit_update_enterprise_milestone_v8` |
| Read enterprise projects | `atomgit_get_enterprise_projects_v8` |
| Read enterprise custom roles | `atomgit_get_enterprise_customized_roles_v8` |

## Notes

- Enterprise APIs often require both the enterprise name and extra IDs. Gather both before mutating anything.
- Prefer v8 methods when the runtime exposes both generations for the same domain.
