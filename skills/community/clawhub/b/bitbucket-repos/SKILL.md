---
name: bitbucket-repos
description: Browse Bitbucket repositories, manage branches, review pull requests, and work with source code via the Bitbucket Cloud API. Use this skill when users want to inspect repo contents, create branches, manage pull requests, or coordinate code workflows.
---

# Bitbucket

![Bitbucket](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/bitbucket.svg?v=2)

Work with Bitbucket from chat — browse repositories, inspect files, manage branches, review pull requests, and coordinate repository workflows via the Bitbucket Cloud API with OAuth authentication.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=bitbucket-repos) for hosted connection flows and credentials so you do not need to configure Bitbucket API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Bitbucket |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Bitbucket |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Bitbucket Cloud API  │
│   (User Chat)   │     │   (OAuth)    │     │ (Repos/PRs/Branches)│
└─────────────────┘     └──────────────┘     └──────────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Bitbucket  │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ Bitbucket│
   │  File    │           │ Auth     │           │ Cloud │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Bitbucket again."

## Quick Start

```bash
# List repositories in a workspace
clawlink_call_tool --tool "bitbucket_list_repositories_in_workspace" --params '{"workspace": "your-workspace"}'

# List branches in a repository
clawlink_call_tool --tool "bitbucket_list_branches" --params '{"workspace": "your-workspace", "repo_slug": "your-repo"}'

# Get a pull request
clawlink_call_tool --tool "bitbucket_get_pull_request" --params '{"workspace": "your-workspace", "repo_slug": "your-repo", "pull_request_id": 1}'
```

## Authentication

All Bitbucket tool calls are authenticated automatically by ClawLink using the user's connected Bitbucket account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Bitbucket API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=bitbucket and connect Bitbucket.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `bitbucket` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration bitbucket
```

**Response:** Returns the live tool catalog for Bitbucket.

### Reconnect

If Bitbucket tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=bitbucket
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration bitbucket`

## Security& Permissions

- Access is scoped to repositories and resources accessible to the connected Bitbucket account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete repository, delete branch, delete issue) are marked as high-impact and must be confirmed.
- Repository deletion does not affect forks.

## Tool Reference

### Repository Operations

| Tool | Description | Mode |
|------|-------------|------|
| `bitbucket_list_repositories_in_workspace` | List repositories in a workspace | Read |
| `bitbucket_list_repositories` | List public repositories | Read |
| `bitbucket_get_repository` | Get repository metadata | Read |
| `bitbucket_create_repository` | Create a new repository in a workspace | Write |
| `bitbucket_delete_repository` | Permanently delete a repository | Write |
| `bitbucket_browse_repository_path` | Get file content or list directory at a revision | Read |
| `bitbucket_get_file_from_repository` | Get a specific file's content at a commit | Read |
| `bitbucket_list_repository_paths` | List files and directories under a path | Read |

### Branch Operations

| Tool | Description | Mode |
|------|-------------|------|
| `bitbucket_list_branches` | List branches with optional name filtering | Read |
| `bitbucket_get_branch` | Get branch metadata and target commit | Read |
| `bitbucket_create_branch` | Create a new branch from a target commit | Write |
| `bitbucket_get_repositories_branching_model` | Get the repository's branch workflow configuration | Read |
| `bitbucket_get_repositories_effective_branching_model` | Get effective branching model (including inheritance) | Read |

### Commit Operations

| Tool | Description | Mode |
|------|-------------|------|
| `bitbucket_list_commits` | List commits with optional branch/path filters | Read |
| `bitbucket_get_repositories_commit` | Get detailed commit information | Read |
| `bitbucket_get_commit_diff` | Get the unified diff for a commit or range | Read |
| `bitbucket_get_commit_changes` | Get changed files in a commit | Read |
| `bitbucket_get_commit_build_status` | Get build status for a commit | Read |
| `bitbucket_get_commit_diffstat` | Get diffstat (files changed, lines added/removed) | Read |

### Pull Request Operations

| Tool | Description | Mode |
|------|-------------|------|
| `bitbucket_list_pull_requests` | List pull requests by state (OPEN/MERGED/DECLINED) | Read |
| `bitbucket_get_pull_request` | Get a single pull request with full details | Read |
| `bitbucket_get_pull_request_commits` | Get commits included in a PR | Read |
| `bitbucket_get_pull_request_diff` | Get the unified diff for a PR | Read |
| `bitbucket_get_pull_request_diffstat` | Get diffstat for a PR | Read |
| `bitbucket_create_pull_request` | Create a new pull request | Write |
| `bitbucket_update_pull_request` | Update PR title, description, or reviewers | Write |
| `bitbucket_merge_pull_request` | Merge a pull request | Write |
| `bitbucket_approve_pull_request` | Approve a pull request | Write |
| `bitbucket_request_pull_request_changes` | Request changes on a PR | Write |
| `bitbucket_create_pull_request_comment` | Add a top-level or threaded comment to a PR | Write |
| `bitbucket_delete_pull_request_comment` | Delete a PR comment | Write |
| `bitbucket_resolve_pull_request_comment` | Resolve or reopen a PR comment thread | Write |

### Issue Operations

| Tool | Description | Mode |
|------|-------------|------|
| `bitbucket_list_issues` | List issues with optional state/priority filters | Read |
| `bitbucket_create_issue` | Create a new issue | Write |
| `bitbucket_update_issue` | Update issue attributes | Write |
| `bitbucket_delete_issue` | Permanently delete an issue | Write |
| `bitbucket_create_issue_comment` | Add a comment to an issue | Write |

### User & Workspace

| Tool | Description | Mode |
|------|-------------|------|
| `bitbucket_get_current_user` | Get the authenticated user's profile | Read |
| `bitbucket_list_workspaces` | List workspaces accessible to the user | Read |
| `bitbucket_get_workspace` | Get workspace metadata | Read |
| `bitbucket_list_workspace_members` | List members of a workspace | Read |
| `bitbucket_list_workspace_projects` | List projects in a workspace | Read |

### Pipelines & Deployments

| Tool | Description | Mode |
|------|-------------|------|
| `bitbucket_list_pipelines` | List pipeline runs for a repository | Read |
| `bitbucket_get_repositories_pipelines2` | Get a specific pipeline's details | Read |
| `bitbucket_list_repositories_environments` | List deployment environments | Read |
| `bitbucket_list_deployments` | List deployment history | Read |

### Code Search

| Tool | Description | Mode |
|------|-------------|------|
| `bitbucket_get_workspaces_search_code` | Search code across all repos in a workspace | Read |
| `bitbucket_search_user_repositories_code` | Search code in a specific user's repos | Read |

## Code Examples

### List branches in a repository

```bash
clawlink_call_tool --tool "bitbucket_list_branches" \
  --params '{
    "workspace": "your-workspace",
    "repo_slug": "your-repo",
    "q": "name~\"feature\""
  }'
```

### Create a pull request

```bash
clawlink_call_tool --tool "bitbucket_create_pull_request" \
  --params '{
    "workspace": "your-workspace",
    "repo_slug": "your-repo",
    "title": "Add new feature",
    "source_branch": "feature/new-feature",
    "destination_branch": "main",
    "description": "This PR adds the new feature as described in issue #123"
  }'
```

### Approve a pull request

```bash
clawlink_call_tool --tool "bitbucket_approve_pull_request" \
  --params '{
    "workspace": "your-workspace",
    "repo_slug": "your-repo",
    "pull_request_id": 42
  }'
```

### Get file content from a repository

```bash
clawlink_call_tool --tool "bitbucket_get_file_from_repository" \
  --params '{
    "workspace": "your-workspace",
    "repo_slug": "your-repo",
    "path": "README.md",
    "commit_revision": "main"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Bitbucket is connected.
2. Call `clawlink_list_tools --integration bitbucket` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `bitbucket`.
5. If no Bitbucket tools appear, direct the user to https://claw-link.dev/dashboard?add=bitbucket.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List repos → List branches → Show results          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call         │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update                                 │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Branch names must be unique within a repository and must not include the `refs/heads/` prefix.
- Pull request IDs are numeric. Use `bitbucket_list_pull_requests` to find PR IDs.
- Repository deletion does not affect forks — forks are separate copies.
- Pagination: use the `next` field in responses to iterate through large result sets.
- BBQL (Bitbucket Query Language) supports server-side filtering for branch names.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration bitbucket`. |
| Missing connection | Bitbucket is not connected. Direct the user to https://claw-link.dev/dashboard?add=bitbucket. |
| `BranchNotFound` | Branch does not exist. Check the branch name. |
| `PullRequestNotFound` | Pull request does not exist. Check the PR ID. |
| `RepositoryNotFound` | Repository does not exist or is not accessible. |
| `InvalidArgument` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `bitbucket`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Bitbucket Cloud REST API](https://developer.atlassian.com/cloud/bitbucket/rest/)
- [Bitbucket Repository API](https://developer.atlassian.com/cloud/bitbucket/rest/api-group-repositories/)
- [Bitbucket Pull Request API](https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pullrequests/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=bitbucket-repos
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [GitHub](https://clawhub.ai/hith3sh/github-repos) — For GitHub repository operations
- [GitLab](https://clawhub.ai/hith3sh/gitlab-repos) — For GitLab repository operations
- [Jira](https://clawhub.ai/hith3sh/jira-projects) — For Jira issue tracking

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=bitbucket-repos)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
