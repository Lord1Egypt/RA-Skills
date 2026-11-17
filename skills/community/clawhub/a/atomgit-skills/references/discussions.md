# Discussions

Read this file for repository and organization discussion boards: threads, comments, and comment replies.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| List repo discussions | `atomgit_get_repository_discussions` |
| Inspect one repo discussion | `atomgit_get_repository_discussion` |
| List repo discussion comments | `atomgit_get_repository_discussion_comments` |
| List repo comment replies | `atomgit_get_repository_discussion_comment_replies` |
| Create a repo discussion | `atomgit_create_repository_discussion` |
| Update a repo discussion | `atomgit_update_repository_discussion` |
| Delete a repo discussion | `atomgit_delete_repository_discussion` |
| Comment on a repo discussion | `atomgit_create_repository_discussion_comment` |
| Update a repo discussion comment | `atomgit_update_repository_discussion_comment` |
| Delete a repo discussion comment | `atomgit_delete_repository_discussion_comment` |
| Reply to a repo discussion comment | `atomgit_reply_repository_discussion_comment` |
| List org discussions | `atomgit_get_organization_discussions` |
| Inspect one org discussion | `atomgit_get_organization_discussion` |
| List org discussion comments | `atomgit_get_organization_discussion_comments` |
| List org comment replies | `atomgit_get_organization_discussion_comment_replies` |
| Create an org discussion | `atomgit_create_organization_discussion` |
| Update an org discussion | `atomgit_update_organization_discussion` |
| Delete an org discussion | `atomgit_delete_organization_discussion` |
| Comment on an org discussion | `atomgit_create_organization_discussion_comment` |
| Update an org discussion comment | `atomgit_update_organization_discussion_comment` |
| Delete an org discussion comment | `atomgit_delete_organization_discussion_comment` |
| Reply to an org discussion comment | `atomgit_reply_organization_discussion_comment` |

## Typical Flow

1. Confirm the scope first: repository discussions use `owner`/`repo`, organization discussions use the org `path`.
2. List discussions, optionally filtering with `search` (matches title and body) or sorting by `created` / `comment_size`.
3. Read one discussion by its `number`, then its comments, then a comment's replies when deeper context is needed.
4. To create a discussion, gather `title`, `mdContent` (Markdown), and `categoryName` — the category name is required on both repo and org creation.
5. Comment with `create_*_discussion_comment`; reply to an existing comment with `reply_*_discussion_comment` and its comment id.
6. Treat update and delete on discussions or comments as write operations that need explicit confirmation.

## Notes

- Number type is asymmetric: repo discussion `number` accepts a string or a number, but org discussion `number` is string-only — pass `"5"`, not `5`, for organization discussions.
- Update semantics are asymmetric: `atomgit_update_repository_discussion` requires all of `title`, `mdContent`, and `categoryName` (read the current values first and resend them), while `atomgit_update_organization_discussion` accepts a partial update with just the fields to change.
- PR review discussions are a different resource: use `atomgit_reply_pull_request_discussion` and friends from the pull-requests module, not the tools in this file.
