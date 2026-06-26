# Kanban

Read this file for organization kanban boards, kanban content, and kanban item state updates.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| List organization kanbans | `atomgit_get_organization_kanbans` |
| Inspect one kanban | `atomgit_get_organization_kanban` |
| Read kanban content | `atomgit_get_organization_kanban_content` |
| Read kanban item list | `atomgit_get_org_kanban_item_list` |
| Add an item | `atomgit_add_org_kanban_item` |
| Update kanban state | `atomgit_update_org_kanban_state` |
| Update linked issue or pull data | `atomgit_update_org_kanban_repo_item` |

## Typical Flow

1. Confirm the organization and kanban identifier.
2. Read the current kanban content before moving items.
3. Treat kanban state changes as organization-scoped operations even when the item points to a repository issue or pull request.
