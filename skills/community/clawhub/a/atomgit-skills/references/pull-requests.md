# Pull Requests

Read this file for pull request review, creation, merge checks, comments, assignees, testers, and issue linking.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| List pull requests | `atomgit_get_repository_pulls` |
| Inspect one pull request | `atomgit_get_repository_pull` |
| Create a pull request | `atomgit_create_repository_pull` |
| Update a pull request | `atomgit_update_repository_pull` |
| Read changed files | `atomgit_get_repository_pull_files` |
| Read pull request commits | `atomgit_get_repository_pull_commits` |
| Read pull request comments | `atomgit_get_repository_pull_comments` |
| Add a pull request comment | `atomgit_create_repository_pull_comment` |
| Reply in a discussion thread | `atomgit_reply_pull_request_discussion` |
| Check mergeability | `atomgit_get_repository_pull_merge_status` |
| Read linked issues | `atomgit_get_repository_pull_issues` |
| Link issues | `atomgit_link_repository_pull_issues` |
| Unlink issues | `atomgit_unlink_repository_pull_issues` |
| Merge a pull request | `atomgit_merge_repository_pull` |
| Process review outcome | `atomgit_process_repository_pull_review` |
| Process test outcome | `atomgit_process_repository_pull_test` |
| Assign assignees | `atomgit_assign_repository_pull_assignees` |
| Reset assignees | `atomgit_reset_repository_pull_assignees` |
| Assign testers | `atomgit_assign_repository_pull_testers` |
| Reset testers | `atomgit_reset_repository_pull_testers` |
| List tester options | `atomgit_get_repository_pull_tester_options` |
| Read pull request labels | `atomgit_get_repository_pull_labels` |
| Replace pull request labels | `atomgit_replace_repository_pull_labels` |

## Review Flow

1. Use `atomgit_get_repository_pulls` to find the target PR.
2. Inspect it with `atomgit_get_repository_pull`.
3. Read the diff with `atomgit_get_repository_pull_files` and `atomgit_get_repository_pull_commits`.
4. Leave feedback before calling `atomgit_process_repository_pull_review`.
5. Confirm merge intent before `atomgit_merge_repository_pull`.

## Notes

- Approval-reviewer tools may be exposed under runtime-specific names. Inspect the live tool list before assuming the exact method name.
