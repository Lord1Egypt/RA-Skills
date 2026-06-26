---
name: check-deployment-status
description: Check deployment status of PRs and commits using continuous-deployment MCP and UCS deployer MCP. Use when user asks "is this deployed", "check deployment", "deployment status", "is PR merged and deployed", "check UP status", "introduced to production", or provides a GitHub PR URL and wants deployment info.
---

# Check Deployment Status

Check whether a PR/commit is deployed to staging and production using the continuous-deployment MCP tools.

## Usage

```bash
/check-deployment-status <PR-URL>           # Check deployment of a GitHub PR
/check-deployment-status <commit-hash>      # Check deployment of a specific commit
/check-deployment-status <service-name>     # List recent commits and their deployment status
```

## Key Concepts

### PR Head Commit != Merge Commit

When a PR is merged via SubmitQueue, the merge commit on main is DIFFERENT from the PR's head commit. The continuous-deployment system tracks the merge commit, not the PR head.

**Workflow:**
1. Get PR metadata → extract head SHA
2. Use `findServiceCommits` with search text to find the actual merge commit on main
3. Use `getCommitDeploymentStatus` with the merge commit hash

### UP Deployment Stages

| Stage | Meaning |
|-------|---------|
| Build created | Binary built from commit |
| Deployed to staging | Running on staging instances |
| Soaked | Staging soak period passed |
| Waited for deployment window | Outside deploy freeze windows |
| **Introduced to production** | **Fully deployed to production** — code is live |

**"Introduced to production" = fully deployed.** Not partial, not in-progress. The commit is running on all production instances.

### Deployment Status Values

| Status | Meaning |
|--------|---------|
| `DEPLOYMENT_STATUS_DEPLOYED` | Commit is running in this environment |
| `DEPLOYMENT_STATUS_DEPLOYING` | Deployment in progress |
| (empty) | Not deployed to this environment |

## Step-by-Step Workflow

### Step 1: Get PR Metadata

Use `mcp__code-mcp__get_github_pull_request_metadata`:
```
org: uber-code
repo: go-code
number: <PR number>
```

Extract: title, head SHA, merged status, base branch.

### Step 2: Find Merge Commit

The PR head SHA won't be found in deployment system. Search for the merge commit:

Use `mcp__continuous-deployment__continuousdeployment_findservicecommits`:
```
service_name: <service-name>
filter: { search_text: "<keyword from PR title>", commited_after: "2026-02-25T00:00:00Z" }
offset: 0
limit: 5
```

The result includes the merge commit hash, serial number, and code review metadata linking back to the PR.

### Step 3: Check Deployment Status

Use `mcp__continuous-deployment__continuousdeployment_getcommitdeploymentstatus`:
```
hash: <merge-commit-hash>
repository: gitolite@code.uber.internal:go-code
options: { scope: "SCOPE_ALL_SERVICES" }
```

Returns deployment status per service per environment (staging, production, bits-test-sandbox).

## MCP Tools Reference

### continuous-deployment MCP

| Tool | Purpose |
|------|---------|
| `findServiceCommits` | Search commits by service name, author, text, date range |
| `getCommitDeploymentStatus` | Get deployment status of a commit across all environments |
| `listServiceCommits` | List recent commits for a service (with serial-based pagination) |
| `getCommitsInDeployment` | List commits in a specific deployment task |
| `listCommitSegments` | Get deployment segments for a service |
| `getConfigForService` | Get continuous deployment config for a service |

### code-mcp

| Tool | Purpose |
|------|---------|
| `get_github_pull_request_metadata` | PR status, author, labels, SubmitQueue status |
| `get_github_pull_request_diff` | PR diff content |
| `get_github_pull_request_comments` | PR comments |

### UCS deployer MCP

| Tool | Purpose |
|------|---------|
| `ucsdeployer_status` | Rollout status for a specific deployment object |
| `deploystatemanager_read` | Read deploy state |

### Service-Name Only Mode

If only a service name is provided (no PR/commit):

Use `mcp__continuous-deployment__continuousdeployment_listservicecommits`:
```
service_name: <service-name>
offset: 0
limit: 5
```

Then check deployment status for each returned commit using Step 3.

## Common Patterns

### Stacked PRs

For stacked PRs, each PR may affect different services. Check deployment per-service:
- PRs changing `marketing-recommendations/` → check `marketing-recommendations` service
- PRs changing `ads-insights/` → check `ads-insights` service

### Repository URI

For go-code monorepo, always use: `gitolite@code.uber.internal:go-code`
