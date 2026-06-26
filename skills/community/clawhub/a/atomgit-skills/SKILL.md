---
name: atomgit
description: "Use this skill when the user explicitly mentions AtomGit or atomgit.com, or needs to inspect or change AtomGit repositories, pull requests, issues, branches, releases, tags, permissions, organizations, enterprises, kanban boards, webhooks, or AIHub features through the AtomGit MCP server."
homepage: https://atomgit.com/zkxw2008/AtomGit-Skills
metadata: {"openclaw":{"homepage":"https://atomgit.com/zkxw2008/AtomGit-Skills","requires":{"env":["ATOMGIT_TOKEN"]},"primaryEnv":"ATOMGIT_TOKEN"}}
---

# AtomGit

Use this skill only for AtomGit work. If the user only says "repo", "PR", "issue", "branch", or "tag" without saying AtomGit, do not assume this skill applies; confirm the platform first.

## Start Here

1. Confirm the request is about AtomGit.
2. Inspect the runtime tool list before planning any repository action.
3. If AtomGit tools are not exposed yet, stop the workflow and follow [references/setup-and-safety.md](references/setup-and-safety.md) to connect an AtomGit MCP server manually using the official server docs. Do not install packages or request secrets automatically inside the task.
4. Match the exposed AtomGit MCP tool names exactly.
5. Prefer read operations before write operations.
6. Gather the identifiers you need before mutating anything:
   - `owner` and `repo`
   - `number` for issues and pull requests
   - `branch`, `tag`, `path`, or `sha` when the workflow needs them
7. Confirm destructive or org-wide changes before executing them.

AtomGit MCP must be installed and configured outside this skill before the first AtomGit task. Do not wait until after a business request fails if the tool list already shows the server is missing, and do not ask users to paste tokens into chat.

## Tool Naming

This skill uses canonical AtomGit MCP method names such as `atomgit_get_repository`.

Some runtimes add extra namespace wrappers around MCP tools. Always use the exact tool name exposed by the current runtime instead of assuming a prefix format from an example.

## Common Identifiers

| Identifier | Typical meaning | Notes |
| --- | --- | --- |
| `owner` | Repository owner, username, or organization | Needed for most repository-scoped calls |
| `repo` | Repository name | Needed with `owner` for most repository calls |
| `number` | Issue or pull request number | Replaces older examples that used `issue_number` or `pull_number` |
| `path` | Repository file path | Use with file-content and file-update calls |
| `sha` | Commit or blob SHA | File updates usually need the current file SHA first |
| `page`, `perPage` | Pagination controls | List endpoints often expose both |

## Read References Only As Needed

- Setup, authentication, permissions, and safety:
  [references/setup-and-safety.md](references/setup-and-safety.md)
- Repositories:
  [references/repositories.md](references/repositories.md)
- Pull requests:
  [references/pull-requests.md](references/pull-requests.md)
- Issues:
  [references/issues.md](references/issues.md)
- Branches:
  [references/branches.md](references/branches.md)
- Commits:
  [references/commits.md](references/commits.md)
- Releases:
  [references/releases.md](references/releases.md)
- Tags:
  [references/tags.md](references/tags.md)
- Labels:
  [references/labels.md](references/labels.md)
- Milestones:
  [references/milestones.md](references/milestones.md)
- Users:
  [references/users.md](references/users.md)
- Organizations:
  [references/organizations.md](references/organizations.md)
- Enterprises:
  [references/enterprises.md](references/enterprises.md)
- Kanban:
  [references/kanban.md](references/kanban.md)
- Webhooks:
  [references/webhooks.md](references/webhooks.md)
- Search:
  [references/search.md](references/search.md)
- Members and permissions:
  [references/members.md](references/members.md)
- AIHub:
  [references/aihub.md](references/aihub.md)
