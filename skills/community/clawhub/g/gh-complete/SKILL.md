---
name: gh-view
description: "Complete skill for operating GitHub CLI (gh) on cli-trunk: full command map, subcommands, usage patterns, JSON output, and practical workflows for Issues, PRs, Actions, Repos, Releases, Projects, Secrets, Variables, Codespaces, Extensions, and API."
---

# Skill: Complete GitHub CLI (cli-trunk)

Use `gh` to operate GitHub end-to-end from the command line. This skill is built from the `cli-trunk` source code and is meant for practical, reproducible command execution.

## Goal

- Solve GitHub tasks with precise and repeatable `gh` commands.
- Pick the right command family by domain: PRs, Issues, repositories, Actions, releases, configuration, security, and API.
- Prefer structured output (`--json`, `--jq`) whenever automation is needed.

## Install GitHub CLI on Linux

Use official packages when possible.

### Debian and Ubuntu (official repository)

```bash
(type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \
  && sudo mkdir -p -m 755 /etc/apt/keyrings \
  && out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  && cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
  && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
  && sudo mkdir -p -m 755 /etc/apt/sources.list.d \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
  && sudo apt update \
  && sudo apt install gh -y
```

Upgrade:

```bash
sudo apt update
sudo apt install gh
```

### RPM-based distros (DNF5)

```bash
sudo dnf install dnf5-plugins
sudo dnf config-manager addrepo --from-repofile=https://cli.github.com/packages/rpm/gh-cli.repo
sudo dnf install gh --repo gh-cli
```

Upgrade:

```bash
sudo dnf update gh
```

### RPM-based distros (DNF4)

```bash
sudo dnf install 'dnf-command(config-manager)'
sudo dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
sudo dnf install gh --repo gh-cli
```

### Amazon Linux 2 (yum)

```bash
type -p yum-config-manager >/dev/null || sudo yum install yum-utils
sudo yum-config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
sudo yum install gh
```

### openSUSE and SUSE (zypper)

```bash
sudo zypper addrepo https://cli.github.com/packages/rpm/gh-cli.repo
sudo zypper ref
sudo zypper install gh
```

### Alternative official methods

- Homebrew on Linux:

```bash
brew install gh
```

- Precompiled binaries: https://github.com/cli/cli/releases/latest

### Verify installation

```bash
gh --version
```

## Login and Authentication (Do This First)

Most `gh` commands require authentication. Use one of these methods.

### Interactive login (recommended for local development)

```bash
gh auth login
gh auth status
gh auth setup-git
```

What this does:

- `gh auth login`: signs you in (browser/device flow) and stores credentials.
- `gh auth status`: confirms active account, host, and token scopes.
- `gh auth setup-git`: configures git credential helper integration.

### GitHub Enterprise Server login

```bash
gh auth login --hostname github.example.com
gh auth status --hostname github.example.com
```

### Token-based login (CI/non-interactive)

```bash
export GH_TOKEN=<your_token>
gh auth status
```

Notes:

- `GH_TOKEN` / `GITHUB_TOKEN` are used for `github.com`.
- `GH_ENTERPRISE_TOKEN` / `GITHUB_ENTERPRISE_TOKEN` are used for GHES hosts.

### Common auth lifecycle commands

```bash
gh auth refresh -s repo,read:org,project
gh auth switch
gh auth logout
```

- `gh auth refresh`: updates token scopes.
- `gh auth switch`: switches between authenticated accounts/hosts.
- `gh auth logout`: removes stored credentials for a host.

Notes:

- Official Linux installation documentation in this repo: `cli-trunk/docs/install_linux.md`.
- Recommended official package host: https://cli.github.com/

## Operating Rules

- If you are not inside a local git repository, use `--repo OWNER/REPO` or a full URL.
- For automation, prefer:
  - `--json <fields>` for structured output.
  - `--jq '<filter>'` for JSON filtering.
- For large listings and searches, cap output with `--limit`.
- If no dedicated subcommand exists, use `gh api`.

## Syntax and Patterns

- Required placeholder: `<value>`.
- Optional argument: `[--flag]` or `[<arg>]`.
- Exclusive alternatives: `{a | b}` or `[a | b]` depending on required vs optional.
- Repeatable arguments: `<arg>...`.

## Root Commands (Complete Map)

- `gh pr` (pull requests)
- `gh issue` (issues)
- `gh repo` (repositories)
- `gh release` (releases)
- `gh run` (workflow runs)
- `gh workflow` (workflows)
- `gh auth` (authentication)
- `gh config` (configuration)
- `gh project` (GitHub Projects)
- `gh secret` (secrets)
- `gh variable` (Actions variables)
- `gh search` (global search)
- `gh gist` (gists)
- `gh extension` / `gh ext` (extensions)
- `gh codespace` / `gh cs` (Codespaces)
- `gh org` (organizations)
- `gh ruleset` / `gh rs` (rulesets)
- `gh cache` (Actions cache)
- `gh label` (labels)
- `gh ssh-key` (SSH keys)
- `gh gpg-key` (GPG keys)
- `gh attestation` / `gh at` (artifact attestations)
- `gh agent-task` / `gh agent` (preview)
- `gh api` (REST/GraphQL API)
- `gh browse` (open in browser)
- `gh status` (cross-repo status)
- `gh copilot` (preview)
- `gh completion` (shell completion)
- `gh licenses` (third-party licenses)
- `gh preview` (experimental commands)
- `gh actions` (hidden; guidance text)
- `gh accessibility` / `gh a11y` (hidden; accessibility)
- `gh credits` (hidden)
- `gh version` (hidden)

## Subcommands by Domain

### Pull Requests: `gh pr`

- `list`, `create`, `status`
- `view`, `diff`, `checkout`, `checks`, `review`, `merge`, `update-branch`, `ready`, `comment`, `close`, `reopen`, `revert`, `edit`, `lock`, `unlock`

Examples:
```bash
gh pr list --repo OWNER/REPO --limit 20
gh pr view 123 --repo OWNER/REPO --json number,title,state,author
gh pr checks 123 --repo OWNER/REPO
```

### Issues: `gh issue`

- `list`, `create`, `status`
- `view`, `comment`, `close`, `reopen`, `edit`, `develop`, `lock`, `unlock`, `pin`, `unpin`, `transfer`, `delete`

Examples:
```bash
gh issue list --repo OWNER/REPO --limit 50
gh issue view 456 --repo OWNER/REPO --json number,title,state,labels
gh issue create --repo OWNER/REPO --title "Bug" --body "Details"
```

### Repositories: `gh repo`

- `list`, `create`
- `view`, `clone`, `fork`, `set-default`, `sync`, `edit`, `deploy-key`, `license`, `gitignore`, `rename`, `archive`, `unarchive`, `delete`, `credits`, `garden`, `autolink`

Examples:
```bash
gh repo view OWNER/REPO --web
gh repo list OWNER --limit 100
gh repo sync OWNER/REPO
```

### Releases: `gh release`

- `list`, `create`
- `view`, `edit`, `upload`, `download`, `delete`, `delete-asset`, `verify`, `verify-asset`

Examples:
```bash
gh release list --repo OWNER/REPO
gh release view v1.2.3 --repo OWNER/REPO
gh release download v1.2.3 --repo OWNER/REPO
```

### GitHub Actions: `gh run`, `gh workflow`, `gh cache`

- `gh run`: `list`, `view`, `rerun`, `download`, `watch`, `cancel`, `delete`
- `gh workflow`: `list`, `enable`, `disable`, `view`, `run`
- `gh cache`: `list`, `delete`

Examples:
```bash
gh run list --repo OWNER/REPO --limit 10
gh run view <run-id> --repo OWNER/REPO --log-failed
gh workflow run ci.yml --repo OWNER/REPO
```

### Authentication and Config: `gh auth`, `gh config`

- `gh auth`: `login`, `logout`, `status`, `refresh`, `git-credential`, `setup-git`, `token`, `switch`
- `gh config`: `get`, `set`, `list`, `clear-cache`

Examples:
```bash
gh auth status
gh auth refresh -s repo,read:org
gh config set git_protocol ssh
```

### Projects: `gh project`

- Project-level: `list`, `create`, `copy`, `close`, `delete`, `edit`, `link`, `view`, `mark-template`, `unlink`
- Items: `item-list`, `item-create`, `item-add`, `item-edit`, `item-archive`, `item-delete`
- Fields: `field-list`, `field-create`, `field-delete`

Examples:
```bash
gh project list --owner ORG
gh project view 1 --owner ORG --web
gh project item-list 1 --owner ORG
```

### Secrets and Variables: `gh secret`, `gh variable`

- `gh secret`: `list`, `set`, `delete`
- `gh variable`: `get`, `set`, `list`, `delete`

Examples:
```bash
gh secret list --repo OWNER/REPO
gh secret set MY_SECRET --repo OWNER/REPO --body "value"
gh variable set MY_VAR --repo OWNER/REPO --body "value"
```

### Global Search: `gh search`

- `code`, `commits`, `issues`, `prs`, `repos`

Examples:
```bash
gh search prs "is:open review:required org:ORG"
gh search code "function NewCmd" --repo OWNER/REPO
```

PowerShell note: for queries containing negative qualifiers (`-qualifier`), use stop-parsing with `--%`.

### Gists, Labels, and Keys

- `gh gist`: `clone`, `create`, `list`, `view`, `edit`, `delete`, `rename`
- `gh label`: `list`, `create`, `clone`, `edit`, `delete`
- `gh ssh-key`: `add`, `delete`, `list`
- `gh gpg-key`: `add`, `delete`, `list`

### Codespaces: `gh codespace` (`gh cs`)

- `code`, `create`, `edit`, `delete`, `jupyter`, `list`, `view`, `logs`, `ports`, `ssh`, `cp`, `stop`, `select`, `rebuild`

Examples:
```bash
gh cs list
gh cs ssh -c <codespace>
gh cs ports -c <codespace>
```

### Extensions: `gh extension` (`gh ext`)

- `search`, `list`, `install`, `upgrade`, `remove`, `browse`, `exec`, `create`

Examples:
```bash
gh ext search
gh ext install owner/gh-myext
gh ext exec myext -- --help
```

### Rulesets, Org, Attestation, Agent Task

- `gh ruleset`: `list`, `view`, `check`
- `gh org`: `list`
- `gh attestation`: `download`, `inspect`, `verify`, `trustedroot`
- `gh agent-task` (preview): `list`, `create`, `view`

Examples:
```bash
gh ruleset list --repo OWNER/REPO
gh at verify -R OWNER/REPO ./artifact.zip
gh agent-task list
```

### Useful Standalone Commands

- `gh browse` (issues, PRs, paths, commits, settings, releases, wiki, actions)
- `gh api` (authenticated REST/GraphQL)
- `gh status` (issues, PRs, mentions, activity)
- `gh copilot` (preview)
- `gh completion -s {bash|zsh|fish|powershell}`
- `gh licenses`

## Complete Command Explanations (All Root Commands)

This section explains each root command in plain language and points to its key subcommands.

### Collaboration and Code Review

- `gh pr`: manage pull requests from creation to merge.
  - Main subcommands: `list`, `view`, `create`, `status`, `checks`, `review`, `merge`, `checkout`, `diff`, `update-branch`, `ready`, `comment`, `edit`, `close`, `reopen`, `revert`, `lock`, `unlock`.
- `gh issue`: manage issue lifecycle and discussion.
  - Main subcommands: `list`, `view`, `create`, `status`, `comment`, `edit`, `develop`, `close`, `reopen`, `transfer`, `delete`, `pin`, `unpin`, `lock`, `unlock`.
- `gh label`: create and maintain repository labels.
  - Main subcommands: `list`, `create`, `clone`, `edit`, `delete`.

### Repositories and Releases

- `gh repo`: administer repositories.
  - Main subcommands: `list`, `view`, `create`, `clone`, `fork`, `sync`, `set-default`, `edit`, `rename`, `archive`, `unarchive`, `delete`, `autolink`, `deploy-key`, `license`, `gitignore`, `credits`, `garden`.
- `gh release`: create, publish, inspect, and verify releases.
  - Main subcommands: `list`, `view`, `create`, `edit`, `upload`, `download`, `delete`, `delete-asset`, `verify`, `verify-asset`.
- `gh gist`: work with GitHub Gists.
  - Main subcommands: `list`, `view`, `create`, `edit`, `rename`, `clone`, `delete`.

### Actions, CI, and Workflow Automation

- `gh run`: inspect and control workflow runs.
  - Main subcommands: `list`, `view`, `watch`, `rerun`, `download`, `cancel`, `delete`.
- `gh workflow`: inspect and trigger workflow files.
  - Main subcommands: `list`, `view`, `run`, `enable`, `disable`.
- `gh cache`: manage GitHub Actions cache entries.
  - Main subcommands: `list`, `delete`.

### Projects, Organization, and Governance

- `gh project`: manage GitHub Projects (project, item, and field operations).
  - Main subcommands: `list`, `view`, `create`, `edit`, `delete`, `copy`, `close`, `link`, `unlink`, `mark-template`, plus `item-*` and `field-*` families.
- `gh org`: organization-level operations.
  - Main subcommands: `list`.
- `gh ruleset`: inspect and evaluate repository rulesets.
  - Main subcommands: `list`, `view`, `check`.

### Security, Secrets, and Identity

- `gh auth`: account and token authentication lifecycle.
  - Main subcommands: `login`, `status`, `refresh`, `setup-git`, `token`, `switch`, `logout`, `git-credential`.
- `gh secret`: manage secrets at repository/org/environment/user scope.
  - Main subcommands: `list`, `set`, `delete`.
- `gh variable`: manage Actions/Dependabot variables.
  - Main subcommands: `list`, `get`, `set`, `delete`.
- `gh ssh-key`: manage SSH keys on your GitHub account.
  - Main subcommands: `list`, `add`, `delete`.
- `gh gpg-key`: manage GPG keys on your GitHub account.
  - Main subcommands: `list`, `add`, `delete`.
- `gh attestation`: download, inspect, and verify artifact attestations.
  - Main subcommands: `download`, `inspect`, `verify`, `trustedroot`.

### Discovery and Navigation

- `gh search`: search code, commits, issues, PRs, and repositories on GitHub.
  - Main subcommands: `code`, `commits`, `issues`, `prs`, `repos`.
- `gh browse`: open repo pages, files, issues, PRs, commits, and settings in your browser.
  - Useful flags: `--branch`, `--commit`, `--settings`, `--wiki`, `--projects`, `--actions`, `--blame`, `--no-browser`.
- `gh status`: aggregated dashboard of assigned issues, PRs, review requests, mentions, and activity.
  - Useful flags: `--org`, `--exclude`.

### Extensions, Aliases, and Developer Experience

- `gh extension` (`gh ext`): discover/install/manage CLI extensions.
  - Main subcommands: `search`, `list`, `install`, `upgrade`, `remove`, `browse`, `exec`, `create`.
- `gh alias`: create and manage command shortcuts.
  - Main subcommands: `set`, `list`, `delete`, `import`.
- `gh completion`: generate shell completion scripts.
  - Main usage: `gh completion -s bash|zsh|fish|powershell`.
- `gh config`: read and update CLI behavior.
  - Main subcommands: `get`, `set`, `list`, `clear-cache`.

### API and Advanced Power Tools

- `gh api`: send authenticated REST/GraphQL requests when built-in subcommands are not enough.
  - Important options: `--method`, `--field`, `--raw-field`, `--input`, `--paginate`, `--slurp`, `--jq`, `--template`, `--header`, `--hostname`, `--preview`.
- `gh codespace` (`gh cs`): manage Codespaces.
  - Main subcommands: `list`, `create`, `view`, `edit`, `logs`, `ports`, `ssh`, `stop`, `delete`, `rebuild`, `code`, `cp`, `jupyter`, `select`.
- `gh agent-task` (`gh agent`) (preview): create/list/view Copilot agent tasks.
  - Main subcommands: `create`, `list`, `view`.
- `gh copilot` (preview): run GitHub Copilot CLI via `gh`.

### Informational and Hidden Commands

- `gh licenses`: view third-party license info for the current `gh` build.
- `gh preview`: run unstable preview commands (currently includes preview tools such as `prompter`).
- `gh actions` (hidden): informational help text about Actions command groups.
- `gh accessibility` / `gh a11y` (hidden): accessibility guidance and related configuration pointers.
- `gh credits` (hidden): credits animation/static credits.
- `gh version` (hidden): print current `gh` version/build info.

## Advanced API Usage

Use `gh api` when no dedicated subcommand exists or when you need custom payload/query control.

REST examples:
```bash
gh api repos/{owner}/{repo}/pulls/123
gh api repos/{owner}/{repo}/issues -X GET -f state=open -f per_page=100
```

GraphQL examples:
```bash
gh api graphql -f query='query { viewer { login } }'
gh api graphql --paginate -f query='query($endCursor: String) { viewer { repositories(first: 100, after: $endCursor) { nodes { nameWithOwner } pageInfo { hasNextPage endCursor } } } }'
```

## Quick Recipes by Intent

- Show PRs with failing checks:
```bash
gh pr list --repo OWNER/REPO --json number,title,statusCheckRollup --jq '.[] | select(any(.statusCheckRollup[]?; .conclusion=="FAILURE")) | {number,title}'
```

- Get open issues in a compact format:
```bash
gh issue list --repo OWNER/REPO --json number,title,author --jq '.[] | "#\(.number) \(.title) (@\(.author.login))"'
```

- Fast Actions diagnosis:
```bash
gh run list --repo OWNER/REPO --limit 5
gh run view <run-id> --repo OWNER/REPO --log-failed
```

## Command Selection Heuristic

- If the task is about PRs or Issues, start with `gh pr` or `gh issue`.
- If it is CI/CD related, use `gh run`, `gh workflow`, and `gh cache`.
- If it is repository administration, use `gh repo`.
- If it is governance/security, use `gh ruleset`, `gh secret`, `gh variable`, and `gh attestation`.
- If no clear coverage exists, use `gh api`.

## Diagnostics and Common Errors

- Authentication issues: run `gh auth status`, then `gh auth login` or `gh auth refresh -s <scopes>`.
- Unresolved repository context: run inside a valid git repo or pass `--repo OWNER/REPO`.
- Ambiguous PR/Issue selectors: use full URL or explicit number.
- In scripts, avoid human-oriented output; use `--json` + `--jq`.

## Completeness Criterion

This skill covers the full command catalog visible in `pkg/cmd/root/root.go` and subcommands registered in `pkg/cmd/*` modules within `cli-trunk`.
