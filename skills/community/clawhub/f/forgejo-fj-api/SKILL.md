---
name: Forgejo Workflow
description: Forgejo via fj and REST API for repos, issues, PRs, wiki, CI, and reviews.
version: 0.1.1
homepage: https://github.com/nerasse/forgejo-skill
metadata:
  openclaw:
    emoji: "🦊"
    homepage: https://github.com/nerasse/forgejo-skill
    requires:
      bins:
        - fj
        - curl
        - jq
        - git
      env:
        - FORGEJO_URL
        - FORGEJO_TOKEN
    primaryEnv: FORGEJO_TOKEN
    install:
      - id: brew
        kind: brew
        formula: forgejo-cli
        bins:
          - fj
        label: Install Forgejo CLI (brew)
---

Use the `fj` CLI and the Forgejo REST API to interact with Forgejo repositories,
issues, pull requests, wiki pages, CI, and code review workflows.

## Overview

Use this skill when:
- Creating, listing, viewing, editing, or closing issues
- Creating, checking out, merging, or reviewing pull requests
- Managing repositories, forks, releases, labels, and milestones
- Reading or writing wiki pages
- Inspecting Forgejo Actions or CI status
- Performing a structured code review on a Forgejo pull request

Do not use this skill when:
- Working on local-only git operations such as commit, rebase, stash, push, or branch cleanup
- Working with GitHub or GitLab instead of Forgejo
- Performing Forgejo server administration that requires the `forgejo` server CLI

This skill targets one active Forgejo instance at a time.

Prefer `fj` for supported operations, use the REST API for feature gaps, and use
local `git` only for review and diff workflows.

## Prerequisites

Required binaries:
- `fj`
- `curl`
- `jq`
- `git`

Create an application token from:

    $FORGEJO_URL/user/settings/applications

Request only the scopes needed for the task. Common patterns for this skill are:
- `read:repository` or `write:repository` for repositories, pull requests, wiki, and releases
- `read:issue` or `write:issue` for issues, labels, and milestones
- `read:notification` or `write:notification` for notifications
- `read:organization` or `write:organization` for org labels and teams
- `read:user` or `write:user` only if user-level endpoints are needed

`FORGEJO_URL` must be the Forgejo base URL such as
`https://<your-forgejo-host>`, not an `/api/v1` endpoint.

`FORGEJO_URL` is the target Forgejo instance URL, not this skill repository URL.

## Required environment

| Variable | Required | Example | Purpose |
|---|---|---|---|
| `FORGEJO_URL` | Yes | `https://<your-forgejo-host>` | Base URL of the target Forgejo instance for this skill's REST and instance-selection workflow |
| `FORGEJO_TOKEN` | Yes | `forgejo_pat_...` | Application token used by this skill's REST examples and recommended for `fj` setup |

Authenticate `fj` with the same token when the target host is already inferable
from the current repository context:

    fj auth add-key <username>

If the current directory is not a Forgejo repository, or if you need to target a
different instance explicitly, pass the host:

    fj --host <forgejo-host> auth add-key <username>

The examples in this skill use the same token for REST API calls:

    curl -sS \
      -H "Authorization: token $FORGEJO_TOKEN" \
      -H "Content-Type: application/json" \
      -H "Accept: application/json" \
      "$FORGEJO_URL/api/v1/..."

If `FORGEJO_URL` or `FORGEJO_TOKEN` is missing, stop and ask the user to provide
the missing value instead of guessing.

REST-ready requires `FORGEJO_URL` and `FORGEJO_TOKEN`. `fj`-ready also requires
`fj` auth for the target host.

## Readiness check

Before doing Forgejo work, verify the required tools, env, and auth state.

Check binaries:

    command -v fj curl jq git

Check required env vars:

    test -n "$FORGEJO_URL" && test -n "$FORGEJO_TOKEN"

Check `fj` auth for the target host:

    fj auth list

If any readiness check fails, stop and ask for the missing install, env value,
or `fj` auth setup before proceeding.

## Repository resolution

Resolve the target repository in this order:

1. Explicit repository selection when the command supports it, such as `--repo owner/repo`
2. The current repository context as resolved from the available git remotes
3. Ask the user for `owner/repo`

Do not guess the repository from issue or pull request numbers alone.

For many issue and pull-request commands outside a local clone, explicit target
selection is done with embedded forms such as `owner/repo#42` rather than a
separate `--repo` flag.

`forgejo-cli` does not hardcode `origin` here. In practice it can resolve from a
sole remote, the current branch upstream remote, an explicit `--remote`, or a
remote matching `--host`.

Use `FORGEJO_URL` as the source of truth for REST calls. Use `fj --host` when the
current repository context does not already point at the target instance. `fj`
itself does not read `FORGEJO_URL`.

## Tool priority

1. `fj` CLI for all supported Forgejo operations
2. `curl` plus `jq` for Forgejo API gaps
3. `git` for diff, log, merge-base, and blame during code review

Always prefer `fj` over raw API calls when both can do the job.

Unless noted otherwise, the examples below assume the host and repository are
already resolved from repo context, `--host`, `--repo`, or an embedded target.

## Repository operations

    fj repo view owner/repo
    fj repo create my-repo --private --description "..."
    fj repo clone owner/repo
    fj repo fork owner/repo
    fj repo delete owner/repo
    fj repo readme owner/repo
    fj repo browse owner/repo
    fj repo migrate <URL> name --service forgejo --include wiki,releases,issues --token

When using `--include` values such as `wiki`, `releases`, or `issues`, specify a
non-`git` migration service such as `forgejo`. The `--token` flag is interactive
and should not be documented as `--token <value>`.

There is no generic `fj repo list` command in `forgejo-cli`. To list repositories,
use user or organization commands such as:

    fj user repos
    fj user repos username
    fj org repo list my-org

When not inside the target repository, prefer explicit repository selection when
the command supports it:

    fj <command> --repo owner/repo

For issue and pull-request commands that do not support `--repo`, use an embedded
target such as `owner/repo#42`.

## Issues

    fj issue search
    fj issue create "Bug: ..." --body "..."
    fj issue view 42
    fj issue edit 42 title "New title"
    fj issue comment 42 "My comment"
    fj issue close 42

If the repository uses issue templates, issue creation may require `--template`
or `--no-template`.

## Pull requests

    fj pr search
    fj pr create "feat: ..." --body "..."
    fj pr create --agit "..."
    fj pr view 55
    fj pr checkout 55
    fj pr status 55
    fj pr merge 55 --method rebase --delete
    fj pr close 55
    fj pr comment 55 "LGTM"
    fj pr edit 55 labels --add bug --rm wip

Some PR commands can infer the PR number from the current branch, but `fj pr checkout`
still requires an explicit PR number.

`fj pr create --agit` is a specialized local-git workflow that pushes
`HEAD:refs/for/<base>` and may prompt to write git config.

Before checking out a pull request locally, inspect the current worktree:

    git status --porcelain

If the worktree is dirty, warn the user before running `fj pr checkout`.

`fj pr checkout` will fail if there are uncommitted changes.

## Releases

    fj release list
    fj release create 0.1.0 --tag 0.1.0

## Organizations and teams

    fj org list
    fj org view my-org
    fj org label list my-org
    fj org label add my-org "bug" "#d73a4a"
    fj org team list my-org
    fj org team member add my-org devs username

## Wiki

Read wiki pages with `fj`:

    fj wiki --repo owner/repo view "Page Name"

List wiki pages with `fj`:

    fj wiki --repo owner/repo contents

Use the REST API for wiki writes, updates, and deletes. See
`references/api-cheatsheet.md`.

## Labels and milestones

Use `fj` for organization labels. Repository labels are available under
`fj repo labels` on current `forgejo-cli` source builds, but not in packaged
`v0.4.0` and `v0.4.1` releases.

Use the REST API for milestones, and as the fallback whenever the local `fj`
build does not expose the needed label operation. See
`references/api-cheatsheet.md`.

## CI and Forgejo Actions

Use `fj` for the quick status path:

    fj --repo owner/repo actions tasks
    fj pr status 55

Use the REST API when detailed run information is needed. See
`references/ci-actions.md`.

## Code review

When asked to review a pull request, follow `references/code-review.md`.

Short version:
1. Inspect worktree state before checkout.
2. Check out the pull request with `fj pr checkout <number>`.
3. Determine the actual base branch from the pull request metadata.
4. Compute the merge base against that base branch.
5. Review the diff using the criteria in `references/code-review.md`.
6. Post a comment with findings.
7. Approve only if the user explicitly asks for approval.
8. Merge only if the user explicitly asks for merge.

Keep approval and merge as separate actions.

## Pagination

Many Forgejo API endpoints support `?page=<n>&limit=<n>`.

When fetching large result sets, keep paging until the response shape or
available pagination metadata indicates there are no more results.

## Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| `FORGEJO_URL` is not set | Required instance URL missing | Export `FORGEJO_URL` before running `fj` or REST workflows |
| `FORGEJO_TOKEN` is not set | Required application token missing | Create a token in Forgejo and export `FORGEJO_TOKEN` |
| `fj: command not found` | `forgejo-cli` is not installed | Install `fj` with the supported metadata installer or another package source |
| `curl: command not found` or `jq: command not found` | REST fallback tools are missing | Install the missing system tools before using REST workflows |
| `git: command not found` | Local review and diff workflows are unavailable | Install `git` before using review flows |
| `fj auth add-key` fails | `fj` needs both a username and a resolvable target host | Run `fj auth add-key <username>` in a configured repo or `fj --host <host> auth add-key <username>` |
| `fj` is not authenticated for the target host | REST may work, but CLI commands will fail | Run `fj auth list` to inspect configured hosts, then add the key for the target host |
| `repo not found` | Wrong owner or repo, wrong instance, or missing access | Verify `owner/repo`, the target instance, and token permissions |
| `cannot infer repository` | No local git remote and no explicit repo selection | Ask the user for `owner/repo`, and include `--host` or a host-qualified target when needed |
| `HTTP 401` or `HTTP 403` | Invalid token or insufficient scope | Verify token validity, scopes, and repo permissions |
| `HTTP 404` from the API | Wrong path or endpoint unsupported on this Forgejo version | Recheck the URL and confirm support in `$FORGEJO_URL/api/swagger` |
| `fj` lacks the requested operation | CLI gap compared to Forgejo API | Fall back to `curl` and `jq` using the REST API |
