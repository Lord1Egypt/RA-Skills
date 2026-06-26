# Milestones

Read this file for repository milestone planning and milestone assignment workflows.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| List milestones | `atomgit_get_repository_milestones` |
| Inspect one milestone | `atomgit_get_repository_milestone` |
| Create a milestone | `atomgit_create_repository_milestone` |
| Update a milestone | `atomgit_update_repository_milestone` |

## Typical Flow

1. List milestones before assigning one to an issue.
2. Use milestone creation or update endpoints only after the title and due date are confirmed.
3. Enterprise milestones live in the enterprise reference, not this file.
