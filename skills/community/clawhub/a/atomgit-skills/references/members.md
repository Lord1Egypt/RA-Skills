# Members And Permissions

Read this file for repository collaborators, repository roles, permission checks, and repository access mode changes.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| List repository collaborators | `atomgit_get_repository_collaborators` |
| Add a repository collaborator | `atomgit_add_repository_collaborator` |
| Check collaborator membership | `atomgit_check_repository_collaborator` |
| Read self collaborator permission | `atomgit_get_self_collaborator_permission` |
| Read repository custom roles | `atomgit_get_repository_customized_roles` |
| Update repository member role | `atomgit_update_repository_member_role` |
| Read repository permission mode | `atomgit_get_repository_transition` |
| Update repository permission mode | `atomgit_update_repository_transition` |

## Typical Flow

1. Inspect current collaborators and roles before granting new access.
2. Confirm whether the request is about repository membership, organization membership, or enterprise membership; those use different APIs.
3. Treat permission-mode changes as high-impact operations and confirm them explicitly.
