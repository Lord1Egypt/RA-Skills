# Organizations

Read this file for organization discovery, organization members, organization repositories, and organization-scoped roles.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| Inspect an organization | `atomgit_get_organization` |
| Update an organization | `atomgit_update_organization` |
| List organization members | `atomgit_get_organization_members` |
| Inspect one organization member | `atomgit_get_organization_member` |
| Invite an organization member | `atomgit_invite_organization_member` |
| Read organization followers | `atomgit_get_organization_followers` |
| Read organization custom roles | `atomgit_get_organization_customized_roles` |
| Read linked enterprise info | `atomgit_get_organization_enterprise_v8` |
| Read organization repositories | `atomgit_get_organization_repositories` |
| Read organization issues | `atomgit_get_organization_issues` |
| Read organization pull requests | `atomgit_get_organization_pull_requests` |

## Typical Flow

1. Confirm the organization name first.
2. Use read-only member or repository endpoints before mutating organization data.
3. Confirm invites and role-related changes before applying them.
