---
name: atlassian-bitbucket-by-altf1be
description: "Atlassian Bitbucket Cloud skill — full CRUD on repos, PRs, pipelines, issues, snippets, workspaces, branches, deployments, and more via Bitbucket REST API 2.0 with API Token auth."
homepage: https://github.com/ALT-F1-OpenClaw/openclaw-skill-atlassian-bitbucket-by-altf1be
metadata:
  {"openclaw": {"emoji": "🪣", "requires": {"env": ["BITBUCKET_EMAIL", "BITBUCKET_API_TOKEN"]}, "optional": {"env": ["BITBUCKET_WORKSPACE", "BITBUCKET_MAX_RESULTS", "BITBUCKET_USERNAME", "BITBUCKET_APP_PASSWORD"]}, "primaryEnv": "BITBUCKET_EMAIL"}}
---

# Atlassian Bitbucket Cloud by @altf1be

Full CRUD on repos, PRs, pipelines, issues, snippets, workspaces, branches, deployments, and more via Bitbucket REST API 2.0.

## Setup

1. Create an **API Token** at https://id.atlassian.com/manage-profile/security/api-tokens (select the scopes you need).
2. Set environment variables (or create `.env` in `{baseDir}`):

```
# Required
BITBUCKET_EMAIL=you@example.com
BITBUCKET_API_TOKEN=your-api-token

# Optional
BITBUCKET_WORKSPACE=your-default-workspace
BITBUCKET_MAX_RESULTS=50

# Legacy (supported until June 9, 2026)
# BITBUCKET_USERNAME=your-username
# BITBUCKET_APP_PASSWORD=your-app-password
```

3. Install dependencies: `cd {baseDir} && npm install`

## Common Options

Most commands accept these shared flags:

| Flag | Description |
|---|---|
| `-w, --workspace <slug>` | Workspace slug (or set `BITBUCKET_WORKSPACE`) |
| `-r, --repo <slug>` | Repository slug |
| `--pagelen <n>` | Results per page |
| `--page <n>` | Page number |
| `--all` | Fetch all pages |
| `-q, --q <filter>` | Filter query (CQL-style) |
| `--sort <field>` | Sort field |
| `--confirm` | Required for all delete operations |
| `--data <json>` | Raw JSON body for complex payloads |

## Commands

### 1. Repositories (26 commands)

CRUD on repositories, forks, watchers, webhooks, override settings, and permissions.

| Command | Description |
|---|---|
| `repo-list-public` | List all public repositories |
| `repo-list` | List repositories in a workspace |
| `repo-get` | Get repository details |
| `repo-create` | Create a new repository |
| `repo-update` | Update repository settings |
| `repo-delete` | Delete a repository |
| `repo-forks` | List forks of a repository |
| `repo-fork-create` | Fork a repository |
| `repo-watchers` | List repository watchers |
| `hook-list` | List repository webhooks |
| `hook-get` | Get a webhook by UID |
| `hook-create` | Create a repository webhook |
| `hook-update` | Update a webhook |
| `hook-delete` | Delete a webhook |
| `repo-override-settings-get` | Get repository override settings |
| `repo-override-settings-update` | Update repository override settings |
| `repo-group-permission-list` | List group permissions |
| `repo-group-permission-get` | Get a group's permission |
| `repo-group-permission-update` | Update a group's permission |
| `repo-group-permission-delete` | Remove a group's permission |
| `repo-user-permission-list` | List user permissions |
| `repo-user-permission-get` | Get a user's permission |
| `repo-user-permission-update` | Update a user's permission |
| `repo-user-permission-delete` | Remove a user's permission |
| `user-repo-permissions` | List current user's repository permissions |
| `user-ws-repo-permissions` | List current user's repository permissions in a workspace |

```bash
# List repos in a workspace
bitbucket repo-list -w myworkspace

# Get repo details
bitbucket repo-get -w myworkspace -r my-repo

# Create a new private repo
bitbucket repo-create -w myworkspace -r new-repo --is-private true --scm git

# Fork a repo
bitbucket repo-fork-create -w myworkspace -r upstream-repo --data '{"name":"my-fork"}'

# Create a webhook
bitbucket hook-create -w myworkspace -r my-repo --url https://example.com/hook --events repo:push

# Delete a repo (requires --confirm)
bitbucket repo-delete -w myworkspace -r old-repo --confirm
```

### 2. Pull Requests (36 commands)

Full lifecycle management of pull requests: create, review, approve, merge, comment, tasks, and default reviewers.

| Command | Description |
|---|---|
| `pr-list` | List pull requests |
| `pr-create` | Create a pull request |
| `pr-get` | Get a pull request by ID |
| `pr-update` | Update a pull request |
| `pr-activity` | Get PR activity log |
| `pr-approve` | Approve a pull request |
| `pr-unapprove` | Remove approval from a PR |
| `pr-comments` | List PR comments |
| `pr-comment-create` | Add a comment to a PR |
| `pr-comment-get` | Get a specific PR comment |
| `pr-comment-update` | Update a PR comment |
| `pr-comment-delete` | Delete a PR comment |
| `pr-comment-resolve` | Resolve a PR comment thread |
| `pr-comment-reopen` | Reopen a resolved comment thread |
| `pr-commits` | List commits in a PR |
| `pr-decline` | Decline a pull request |
| `pr-diff` | Get the diff of a PR |
| `pr-diffstat` | Get the diffstat of a PR |
| `pr-merge` | Merge a pull request |
| `pr-merge-task-status` | Check merge task status |
| `pr-patch` | Get the patch of a PR |
| `pr-request-changes` | Request changes on a PR |
| `pr-unrequest-changes` | Remove change request from a PR |
| `pr-statuses` | List commit statuses on a PR |
| `pr-tasks` | List tasks on a PR |
| `pr-task-create` | Create a task on a PR |
| `pr-task-get` | Get a specific PR task |
| `pr-task-update` | Update a PR task |
| `pr-task-delete` | Delete a PR task |
| `default-reviewer-list` | List default reviewers |
| `default-reviewer-get` | Get a default reviewer |
| `default-reviewer-add` | Add a default reviewer |
| `default-reviewer-delete` | Remove a default reviewer |
| `effective-default-reviewers` | List effective default reviewers |
| `pr-for-commit` | Find PRs containing a commit |
| `pr-activity-all` | Get activity across all PRs in a repo |

```bash
# List open PRs
bitbucket pr-list -w myworkspace -r my-repo -q 'state="OPEN"'

# Create a PR
bitbucket pr-create -w myworkspace -r my-repo --title "Add feature" \
  --source feature-branch --destination main

# Approve a PR
bitbucket pr-approve -w myworkspace -r my-repo --pr-id 42

# Merge a PR
bitbucket pr-merge -w myworkspace -r my-repo --pr-id 42 --merge-strategy squash

# Add a comment
bitbucket pr-comment-create -w myworkspace -r my-repo --pr-id 42 \
  --body "Looks good to me!"

# Create a task on a PR
bitbucket pr-task-create -w myworkspace -r my-repo --pr-id 42 \
  --data '{"content":{"raw":"Fix the typo on line 10"}}'

# Find PRs for a commit
bitbucket pr-for-commit -w myworkspace -r my-repo --commit abc123
```

### 3. Commits (16 commands)

Read commit details, approve/unapprove commits, manage commit comments, list diffs and patches.

| Command | Description |
|---|---|
| `commit-get` | Get a specific commit |
| `commit-approve` | Approve a commit |
| `commit-unapprove` | Remove commit approval |
| `commit-comments` | List comments on a commit |
| `commit-comment-create` | Add a comment to a commit |
| `commit-comment-get` | Get a specific commit comment |
| `commit-comment-update` | Update a commit comment |
| `commit-comment-delete` | Delete a commit comment |
| `commit-list` | List commits (GET) |
| `commit-list-post` | List commits (POST, with body filters) |
| `commit-list-revision` | List commits from a revision (GET) |
| `commit-list-revision-post` | List commits from a revision (POST) |
| `diff` | Get diff between two refs |
| `diffstat` | Get diffstat between two refs |
| `merge-base` | Get merge base of two refs |
| `patch` | Get patch for a revision |

```bash
# Get commit details
bitbucket commit-get -w myworkspace -r my-repo --commit abc123def

# List recent commits
bitbucket commit-list -w myworkspace -r my-repo --pagelen 10

# Get diff between two refs
bitbucket diff -w myworkspace -r my-repo --spec "main..feature-branch"

# Approve a commit
bitbucket commit-approve -w myworkspace -r my-repo --commit abc123def

# Comment on a commit
bitbucket commit-comment-create -w myworkspace -r my-repo --commit abc123def \
  --body "This needs a test."
```

### 4. Branches & Tags (9 commands)

List, create, get, and delete branches and tags.

| Command | Description |
|---|---|
| `ref-list` | List all refs (branches + tags) |
| `branch-list` | List branches |
| `branch-create` | Create a branch |
| `branch-get` | Get branch details |
| `branch-delete` | Delete a branch |
| `tag-list` | List tags |
| `tag-create` | Create an annotated tag |
| `tag-get` | Get tag details |
| `tag-delete` | Delete a tag |

```bash
# List branches
bitbucket branch-list -w myworkspace -r my-repo

# Create a branch
bitbucket branch-create -w myworkspace -r my-repo --name feature/new \
  --target main

# Create a tag
bitbucket tag-create -w myworkspace -r my-repo --name v1.0.0 --target main

# Delete a branch (requires --confirm)
bitbucket branch-delete -w myworkspace -r my-repo --name old-branch --confirm
```

### 5. Branch Restrictions (5 commands)

Manage branch permission restrictions (push, merge, delete controls).

| Command | Description |
|---|---|
| `restriction-list` | List branch restrictions |
| `restriction-get` | Get a restriction by ID |
| `restriction-create` | Create a branch restriction |
| `restriction-update` | Update a branch restriction |
| `restriction-delete` | Delete a branch restriction |

```bash
# List restrictions
bitbucket restriction-list -w myworkspace -r my-repo

# Prevent force-push to main
bitbucket restriction-create -w myworkspace -r my-repo \
  --data '{"kind":"force","pattern":"main"}'

# Delete a restriction (requires --confirm)
bitbucket restriction-delete -w myworkspace -r my-repo --id 123 --confirm
```

### 6. Branching Model (7 commands)

Get and configure the branching model (Git Flow style) at the repo and project level.

| Command | Description |
|---|---|
| `branching-model-get` | Get repo branching model |
| `branching-model-settings-get` | Get repo branching model settings |
| `branching-model-settings-update` | Update repo branching model settings |
| `branching-model-effective` | Get effective branching model (inherited + overrides) |
| `project-branching-model-get` | Get project branching model |
| `project-branching-model-settings-get` | Get project branching model settings |
| `project-branching-model-settings-update` | Update project branching model settings |

```bash
# Get effective branching model
bitbucket branching-model-effective -w myworkspace -r my-repo

# Update branching model settings
bitbucket branching-model-settings-update -w myworkspace -r my-repo \
  --data '{"development":{"name":"develop"},"production":{"name":"main"}}'
```

### 7. Pipelines (68 commands)

Full pipeline lifecycle: run, stop, inspect steps/logs, manage variables, schedules, SSH keys, known hosts, caches, runners, OIDC, and workspace/team/user-level pipeline variables.

| Command | Description |
|---|---|
| `pipeline-list` | List pipelines |
| `pipeline-get` | Get pipeline details |
| `pipeline-create` | Trigger a new pipeline |
| `pipeline-stop` | Stop a running pipeline |
| `pipeline-steps` | List steps in a pipeline |
| `pipeline-step-get` | Get a pipeline step |
| `pipeline-step-log` | Get step log output |
| `pipeline-step-log-container` | Get step container log |
| `pipeline-test-reports` | Get test reports for a step |
| `pipeline-test-cases` | Get test cases for a step |
| `pipeline-test-case-reasons` | Get test case failure reasons |
| `pipeline-config-get` | Get pipeline configuration |
| `pipeline-config-update` | Update pipeline configuration |
| `pipeline-build-number-update` | Update the next build number |
| `pipeline-var-list` | List repo pipeline variables |
| `pipeline-var-get` | Get a pipeline variable |
| `pipeline-var-create` | Create a pipeline variable |
| `pipeline-var-update` | Update a pipeline variable |
| `pipeline-var-delete` | Delete a pipeline variable |
| `pipeline-schedule-list` | List pipeline schedules |
| `pipeline-schedule-get` | Get a schedule |
| `pipeline-schedule-create` | Create a pipeline schedule |
| `pipeline-schedule-update` | Update a pipeline schedule |
| `pipeline-schedule-delete` | Delete a pipeline schedule |
| `pipeline-schedule-executions` | List schedule executions |
| `pipeline-ssh-keypair-get` | Get SSH key pair |
| `pipeline-ssh-keypair-update` | Update SSH key pair |
| `pipeline-ssh-keypair-delete` | Delete SSH key pair |
| `pipeline-known-host-list` | List known hosts |
| `pipeline-known-host-get` | Get a known host |
| `pipeline-known-host-create` | Add a known host |
| `pipeline-known-host-update` | Update a known host |
| `pipeline-known-host-delete` | Delete a known host |
| `pipeline-cache-list` | List pipeline caches |
| `pipeline-cache-delete` | Delete all caches |
| `pipeline-cache-delete-by-name` | Delete a cache by name |
| `pipeline-cache-content-uri` | Get cache content URI |
| `pipeline-runner-list` | List repo pipeline runners |
| `pipeline-runner-get` | Get a pipeline runner |
| `pipeline-runner-create` | Create a pipeline runner |
| `pipeline-runner-update` | Update a pipeline runner |
| `pipeline-runner-delete` | Delete a pipeline runner |
| `env-var-list` | List deployment environment variables |
| `env-var-create` | Create a deployment env variable |
| `env-var-update` | Update a deployment env variable |
| `env-var-delete` | Delete a deployment env variable |
| `team-pipeline-var-list` | List team pipeline variables |
| `team-pipeline-var-get` | Get a team pipeline variable |
| `team-pipeline-var-create` | Create a team pipeline variable |
| `team-pipeline-var-update` | Update a team pipeline variable |
| `team-pipeline-var-delete` | Delete a team pipeline variable |
| `user-pipeline-var-list` | List user pipeline variables |
| `user-pipeline-var-get` | Get a user pipeline variable |
| `user-pipeline-var-create` | Create a user pipeline variable |
| `user-pipeline-var-update` | Update a user pipeline variable |
| `user-pipeline-var-delete` | Delete a user pipeline variable |
| `ws-oidc-config` | Get workspace OIDC configuration |
| `ws-oidc-keys` | Get workspace OIDC keys |
| `ws-runner-list` | List workspace runners |
| `ws-runner-get` | Get a workspace runner |
| `ws-runner-create` | Create a workspace runner |
| `ws-runner-update` | Update a workspace runner |
| `ws-runner-delete` | Delete a workspace runner |
| `ws-pipeline-var-list` | List workspace pipeline variables |
| `ws-pipeline-var-get` | Get a workspace pipeline variable |
| `ws-pipeline-var-create` | Create a workspace pipeline variable |
| `ws-pipeline-var-update` | Update a workspace pipeline variable |
| `ws-pipeline-var-delete` | Delete a workspace pipeline variable |

```bash
# Trigger a pipeline on main
bitbucket pipeline-create -w myworkspace -r my-repo \
  --data '{"target":{"ref_type":"branch","type":"pipeline_ref_target","ref_name":"main"}}'

# List recent pipelines
bitbucket pipeline-list -w myworkspace -r my-repo --pagelen 5

# Get step logs
bitbucket pipeline-step-log -w myworkspace -r my-repo \
  --pipeline-uuid {uuid} --step-uuid {uuid}

# Stop a running pipeline
bitbucket pipeline-stop -w myworkspace -r my-repo --pipeline-uuid {uuid}

# Create a repo pipeline variable (secured)
bitbucket pipeline-var-create -w myworkspace -r my-repo \
  --key API_KEY --value secret123 --secured true

# Create a workspace-level variable
bitbucket ws-pipeline-var-create -w myworkspace \
  --key DEPLOY_TOKEN --value tok_abc --secured true

# Schedule a pipeline
bitbucket pipeline-schedule-create -w myworkspace -r my-repo \
  --data '{"cron_pattern":"0 0 * * *","target":{"ref_type":"branch","ref_name":"main"}}'
```

### 8. Deployments (16 commands)

Manage deploy keys and deployment environments.

| Command | Description |
|---|---|
| `deploy-key-list` | List deploy keys |
| `deploy-key-get` | Get a deploy key |
| `deploy-key-create` | Add a deploy key |
| `deploy-key-update` | Update a deploy key |
| `deploy-key-delete` | Delete a deploy key |
| `deployment-list` | List deployments |
| `deployment-get` | Get a deployment |
| `environment-list` | List deployment environments |
| `environment-get` | Get an environment |
| `environment-create` | Create a deployment environment |
| `environment-update` | Update a deployment environment |
| `environment-delete` | Delete a deployment environment |
| `project-deploy-key-list` | List project deploy keys |
| `project-deploy-key-get` | Get a project deploy key |
| `project-deploy-key-create` | Add a project deploy key |
| `project-deploy-key-delete` | Delete a project deploy key |

```bash
# List deployment environments
bitbucket environment-list -w myworkspace -r my-repo

# Create a staging environment
bitbucket environment-create -w myworkspace -r my-repo \
  --data '{"name":"Staging","environment_type":{"name":"Staging"}}'

# Add a deploy key
bitbucket deploy-key-create -w myworkspace -r my-repo \
  --key "ssh-rsa AAAA..." --label "CI deploy key"

# Delete an environment (requires --confirm)
bitbucket environment-delete -w myworkspace -r my-repo \
  --environment-uuid {uuid} --confirm
```

### 9. Commit Statuses (4 commands)

Create and manage build statuses on commits.

| Command | Description |
|---|---|
| `status-list` | List commit statuses |
| `status-create` | Create a commit status |
| `status-get` | Get a commit status |
| `status-update` | Update a commit status |

```bash
# Report a build status
bitbucket status-create -w myworkspace -r my-repo --commit abc123 \
  --state SUCCESSFUL --key build-42 --url https://ci.example.com/42

# List statuses on a commit
bitbucket status-list -w myworkspace -r my-repo --commit abc123
```

### 10. Issue Tracker (33 commands)

Full issue management: CRUD, comments, attachments, changes, voting, watching, import/export, components, milestones, and versions.

| Command | Description |
|---|---|
| `issue-list` | List issues |
| `issue-get` | Get an issue |
| `issue-create` | Create an issue |
| `issue-update` | Update an issue |
| `issue-delete` | Delete an issue |
| `issue-comment-list` | List issue comments |
| `issue-comment-get` | Get an issue comment |
| `issue-comment-create` | Add a comment to an issue |
| `issue-comment-update` | Update an issue comment |
| `issue-comment-delete` | Delete an issue comment |
| `issue-attachment-list` | List issue attachments |
| `issue-attachment-get` | Get an issue attachment |
| `issue-attachment-upload` | Upload an attachment |
| `issue-attachment-delete` | Delete an attachment |
| `issue-change-list` | List issue changes |
| `issue-change-get` | Get an issue change |
| `issue-change-create` | Create an issue change |
| `issue-vote-check` | Check if you voted on an issue |
| `issue-vote` | Vote on an issue |
| `issue-unvote` | Remove your vote |
| `issue-watch-check` | Check if you are watching an issue |
| `issue-watch` | Watch an issue |
| `issue-unwatch` | Stop watching an issue |
| `issue-export` | Start an issue export |
| `issue-export-status` | Check export status |
| `issue-import` | Start an issue import |
| `issue-import-status` | Check import status |
| `component-list` | List components |
| `component-get` | Get a component |
| `milestone-list` | List milestones |
| `milestone-get` | Get a milestone |
| `version-list` | List versions |
| `version-get` | Get a version |

```bash
# List open bugs
bitbucket issue-list -w myworkspace -r my-repo -q 'kind="bug" AND state="open"'

# Create an issue
bitbucket issue-create -w myworkspace -r my-repo \
  --title "Login broken" --kind bug --priority critical

# Comment on an issue
bitbucket issue-comment-create -w myworkspace -r my-repo --issue-id 7 \
  --body "Reproduced on Chrome 120."

# Upload an attachment
bitbucket issue-attachment-upload -w myworkspace -r my-repo --issue-id 7 \
  --file ./screenshot.png

# Export all issues
bitbucket issue-export -w myworkspace -r my-repo

# List milestones
bitbucket milestone-list -w myworkspace -r my-repo
```

### 11. Snippets (25 commands)

Create and manage code snippets, their revisions, files, diffs, comments, commits, and watchers.

| Command | Description |
|---|---|
| `snippet-list` | List your snippets |
| `snippet-create` | Create a snippet |
| `snippet-ws-list` | List workspace snippets |
| `snippet-ws-create` | Create a workspace snippet |
| `snippet-get` | Get a snippet |
| `snippet-update` | Update a snippet |
| `snippet-delete` | Delete a snippet |
| `snippet-revision-get` | Get a snippet revision |
| `snippet-revision-update` | Update a snippet revision |
| `snippet-revision-delete` | Delete a snippet revision |
| `snippet-file` | Get a file from a snippet |
| `snippet-file-revision` | Get a file at a specific revision |
| `snippet-diff` | Get diff between snippet revisions |
| `snippet-patch` | Get patch for a snippet revision |
| `snippet-comment-list` | List snippet comments |
| `snippet-comment-get` | Get a snippet comment |
| `snippet-comment-create` | Add a comment to a snippet |
| `snippet-comment-update` | Update a snippet comment |
| `snippet-comment-delete` | Delete a snippet comment |
| `snippet-commit-list` | List snippet commits |
| `snippet-commit-get` | Get a snippet commit |
| `snippet-watch-check` | Check if watching a snippet |
| `snippet-watch` | Watch a snippet |
| `snippet-unwatch` | Unwatch a snippet |
| `snippet-watchers` | List snippet watchers |

```bash
# List your snippets
bitbucket snippet-list

# Create a snippet
bitbucket snippet-create --title "Bash helper" --is-private true \
  --file ./helper.sh

# List workspace snippets
bitbucket snippet-ws-list -w myworkspace

# Get a specific file from a snippet
bitbucket snippet-file -w myworkspace --snippet-id abc123 --filename helper.sh

# Delete a snippet (requires --confirm)
bitbucket snippet-delete -w myworkspace --snippet-id abc123 --confirm
```

### 12. Workspaces (17 commands)

List workspaces, manage hooks, members, permissions, and list user PRs.

| Command | Description |
|---|---|
| `workspace-list` | List workspaces you belong to |
| `workspace-list-for-user` | List workspaces for a user |
| `workspace-permissions-for-user` | Get workspace permissions for a user |
| `workspace-user-permission` | Get a specific user's workspace permission |
| `workspace-get` | Get workspace details |
| `workspace-hook-list` | List workspace webhooks |
| `workspace-hook-get` | Get a workspace webhook |
| `workspace-hook-create` | Create a workspace webhook |
| `workspace-hook-update` | Update a workspace webhook |
| `workspace-hook-delete` | Delete a workspace webhook |
| `workspace-member-list` | List workspace members |
| `workspace-member-get` | Get a workspace member |
| `workspace-permission-list` | List workspace permissions |
| `workspace-repo-permissions` | List repo-level permissions in workspace |
| `workspace-repo-permission-get` | Get repo-level permission |
| `workspace-project-list` | List projects in a workspace |
| `workspace-user-prs` | List PRs authored by the current user in a workspace |

```bash
# List workspaces
bitbucket workspace-list

# Get workspace details
bitbucket workspace-get -w myworkspace

# List workspace members
bitbucket workspace-member-list -w myworkspace

# List my open PRs across the workspace
bitbucket workspace-user-prs -w myworkspace -q 'state="OPEN"'

# Create a workspace webhook
bitbucket workspace-hook-create -w myworkspace \
  --url https://example.com/hook --events repo:push,pullrequest:created
```

### 13. Projects (16 commands)

CRUD on projects, default reviewers, and group/user permissions at the project level.

| Command | Description |
|---|---|
| `project-create` | Create a project |
| `project-get` | Get a project |
| `project-update` | Update a project |
| `project-delete` | Delete a project |
| `project-default-reviewer-list` | List project default reviewers |
| `project-default-reviewer-get` | Get a project default reviewer |
| `project-default-reviewer-add` | Add a project default reviewer |
| `project-default-reviewer-delete` | Remove a project default reviewer |
| `project-group-permission-list` | List project group permissions |
| `project-group-permission-get` | Get a group's project permission |
| `project-group-permission-update` | Update a group's project permission |
| `project-group-permission-delete` | Remove a group's project permission |
| `project-user-permission-list` | List project user permissions |
| `project-user-permission-get` | Get a user's project permission |
| `project-user-permission-update` | Update a user's project permission |
| `project-user-permission-delete` | Remove a user's project permission |

```bash
# Create a project
bitbucket project-create -w myworkspace --key PROJ --name "My Project"

# List project default reviewers
bitbucket project-default-reviewer-list -w myworkspace --project-key PROJ

# Add a default reviewer to a project
bitbucket project-default-reviewer-add -w myworkspace --project-key PROJ \
  --user-uuid {uuid}

# Delete a project (requires --confirm)
bitbucket project-delete -w myworkspace --project-key PROJ --confirm
```

### 14. Users (4 commands)

Get current user info, list emails, and look up other users.

| Command | Description |
|---|---|
| `user-get-current` | Get the authenticated user |
| `user-emails` | List your email addresses |
| `user-email-get` | Get a specific email address |
| `user-get` | Get a user by UUID or username |

```bash
# Get current user info
bitbucket user-get-current

# List your emails
bitbucket user-emails

# Look up another user
bitbucket user-get --user-uuid {uuid}
```

### 15. SSH Keys (5 commands)

Manage SSH keys on your Bitbucket account.

| Command | Description |
|---|---|
| `ssh-key-list` | List SSH keys |
| `ssh-key-get` | Get an SSH key |
| `ssh-key-create` | Add an SSH key |
| `ssh-key-update` | Update an SSH key label |
| `ssh-key-delete` | Delete an SSH key |

```bash
# List SSH keys
bitbucket ssh-key-list

# Add an SSH key
bitbucket ssh-key-create --key "ssh-ed25519 AAAA..." --label "work laptop"

# Delete an SSH key (requires --confirm)
bitbucket ssh-key-delete --key-id 123 --confirm
```

### 16. GPG Keys (4 commands)

Manage GPG keys for commit signature verification.

| Command | Description |
|---|---|
| `gpg-key-list` | List GPG keys |
| `gpg-key-get` | Get a GPG key |
| `gpg-key-create` | Add a GPG key |
| `gpg-key-delete` | Delete a GPG key |

```bash
# List GPG keys
bitbucket gpg-key-list

# Add a GPG key
bitbucket gpg-key-create --key "-----BEGIN PGP PUBLIC KEY BLOCK-----..."

# Delete a GPG key (requires --confirm)
bitbucket gpg-key-delete --key-id abc123 --confirm
```

### 17. Source / File Browsing (4 commands)

Browse repository source files and commit new files.

| Command | Description |
|---|---|
| `src-history` | Get file history |
| `src-root` | List files at the repo root (or a path) |
| `src-create` | Create/update a file via commit |
| `src-get` | Get file contents |

```bash
# List files at root
bitbucket src-root -w myworkspace -r my-repo

# Get file contents
bitbucket src-get -w myworkspace -r my-repo --path src/index.js

# Get file history
bitbucket src-history -w myworkspace -r my-repo --path README.md

# Create/update a file
bitbucket src-create -w myworkspace -r my-repo \
  --path config.yml --message "Add config" --file ./config.yml
```

### 18. Downloads (4 commands)

Manage repository download artifacts.

| Command | Description |
|---|---|
| `download-list` | List downloads |
| `download-get` | Get a download |
| `download-upload` | Upload a download artifact |
| `download-delete` | Delete a download |

```bash
# List downloads
bitbucket download-list -w myworkspace -r my-repo

# Upload an artifact
bitbucket download-upload -w myworkspace -r my-repo --file ./release-v1.0.zip

# Delete a download (requires --confirm)
bitbucket download-delete -w myworkspace -r my-repo --filename release-v1.0.zip --confirm
```

### 19. Webhooks (2 commands)

Discover available webhook event types.

| Command | Description |
|---|---|
| `webhook-events` | List all webhook event subjects |
| `webhook-event-types` | List event types for a subject |

```bash
# List webhook event subjects
bitbucket webhook-events

# List event types for a subject
bitbucket webhook-event-types --subject repository
```

### 20. Search (3 commands)

Search code, accounts, and teams.

| Command | Description |
|---|---|
| `search-code` | Search for code in a workspace |
| `search-account` | Search for accounts |
| `search-team` | Search for teams |

```bash
# Search code
bitbucket search-code -w myworkspace --search-query "import express"

# Search for an account
bitbucket search-account --search-query "john"
```

### 21. Reports (9 commands)

Manage commit reports and annotations (code quality, security, etc.).

| Command | Description |
|---|---|
| `report-list` | List reports on a commit |
| `report-get` | Get a report |
| `report-create` | Create a report |
| `report-delete` | Delete a report |
| `report-annotation-list` | List report annotations |
| `report-annotation-get` | Get a report annotation |
| `report-annotation-create` | Create an annotation |
| `report-annotation-bulk-create` | Bulk create annotations |
| `report-annotation-delete` | Delete an annotation |

```bash
# Create a code quality report
bitbucket report-create -w myworkspace -r my-repo --commit abc123 \
  --report-id lint-report --title "ESLint" --report-type BUG \
  --data '{"result":"PASSED"}'

# Add annotations to a report
bitbucket report-annotation-bulk-create -w myworkspace -r my-repo \
  --commit abc123 --report-id lint-report \
  --data '[{"path":"src/app.js","line":42,"message":"Unused variable","severity":"MEDIUM"}]'

# List reports on a commit
bitbucket report-list -w myworkspace -r my-repo --commit abc123
```

### 22. Properties (12 commands)

Get, set, and delete application properties on commits, repos, PRs, and users.

| Command | Description |
|---|---|
| `commit-property-get` | Get a commit property |
| `commit-property-update` | Set a commit property |
| `commit-property-delete` | Delete a commit property |
| `repo-property-get` | Get a repo property |
| `repo-property-update` | Set a repo property |
| `repo-property-delete` | Delete a repo property |
| `pr-property-get` | Get a PR property |
| `pr-property-update` | Set a PR property |
| `pr-property-delete` | Delete a PR property |
| `user-property-get` | Get a user property |
| `user-property-update` | Set a user property |
| `user-property-delete` | Delete a user property |

```bash
# Set a repo property
bitbucket repo-property-update -w myworkspace -r my-repo \
  --app-key myapp --property-name env --data '{"tier":"production"}'

# Get a repo property
bitbucket repo-property-get -w myworkspace -r my-repo \
  --app-key myapp --property-name env

# Delete a PR property (requires --confirm)
bitbucket pr-property-delete -w myworkspace -r my-repo --pr-id 42 \
  --app-key myapp --property-name review-status --confirm
```

### 23. Addon (10 commands)

Manage Bitbucket Connect addon lifecycle, linkers, and linker values.

| Command | Description |
|---|---|
| `addon-delete` | Uninstall the addon |
| `addon-update` | Update the addon descriptor |
| `addon-linkers` | List addon linkers |
| `addon-linker-get` | Get an addon linker |
| `addon-linker-values-delete` | Delete all linker values |
| `addon-linker-values` | List linker values |
| `addon-linker-value-create` | Create a linker value |
| `addon-linker-value-update` | Update a linker value |
| `addon-linker-value-delete` | Delete a linker value |
| `addon-linker-value-get` | Get a linker value |

```bash
# List addon linkers
bitbucket addon-linkers

# Create a linker value
bitbucket addon-linker-value-create --linker-key my-linker \
  --data '{"key":"issue-42","href":"https://tracker.example.com/42"}'

# Delete a linker value (requires --confirm)
bitbucket addon-linker-value-delete --linker-key my-linker --value-id 42 --confirm
```

## Security

- Auth method: Basic auth with App Passwords (BITBUCKET_USERNAME + BITBUCKET_APP_PASSWORD)
- No secrets or tokens printed to stdout
- All delete operations require explicit `--confirm` flag
- Path traversal prevention for file uploads (`safePath()`)
- Built-in rate limiting with exponential backoff retry (3 attempts)
- File size validation before upload
- Lazy config validation (only checked when a command runs)

## Dependencies

- `commander` — CLI framework
- `dotenv` — environment variable loading
- Node.js built-in `fetch` (requires Node >= 18)

## Author

Abdelkrim BOUJRAF — [ALT-F1 SRL](https://www.alt-f1.be), Brussels
X: [@altf1be](https://x.com/altf1be)
