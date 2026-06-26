# Tags

Read this file for repository tag listing, tag creation, and protected-tag workflows.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| List tags | `atomgit_get_repository_tags` |
| Create a tag | `atomgit_create_repository_tag` |
| List protected tags | `atomgit_get_repository_protected_tags` |
| Inspect one protected tag | `atomgit_get_repository_protected_tag` |
| Create a protected tag | `atomgit_create_repository_protected_tag` |
| Update a protected tag | `atomgit_update_repository_protected_tag` |

## Notes

- Protected tags are production controls. Treat them with the same care as branch protection changes.
