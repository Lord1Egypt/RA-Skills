# Platform Packs

This document describes packs in the `platform` category.

## Packs in this Category

- [GitHub Platform](#platformgithub)
- [GitLab Platform](#platformgitlab)

---

## GitHub Platform

**Pack ID:** `platform.github`

Protects against destructive GitHub CLI operations like deleting repositories, gists, releases, or SSH keys.

### Keywords

Commands containing these keywords are checked against this pack:

- `gh`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `gh-repo-list-view` | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\|release\|issue\|ssh-key\|secret\|variable\|run\|auth\|status\|api)\b)(?:(?:\x22[^\x22]*\x22)\|(?:'[^']*')\|\S+))?)*\s+repo\s+(?:list\|view)\b` |
| `gh-gist-list-view` | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\|release\|issue\|ssh-key\|secret\|variable\|run\|auth\|status\|api)\b)(?:(?:\x22[^\x22]*\x22)\|(?:'[^']*')\|\S+))?)*\s+gist\s+(?:list\|view)\b` |
| `gh-release-list-view` | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\|release\|issue\|ssh-key\|secret\|variable\|run\|auth\|status\|api)\b)(?:(?:\x22[^\x22]*\x22)\|(?:'[^']*')\|\S+))?)*\s+release\s+(?:list\|view)\b` |
| `gh-issue-list-view` | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\|release\|issue\|ssh-key\|secret\|variable\|run\|auth\|status\|api)\b)(?:(?:\x22[^\x22]*\x22)\|(?:'[^']*')\|\S+))?)*\s+issue\s+(?:list\|view)\b` |
| `gh-ssh-key-list` | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\|release\|issue\|ssh-key\|secret\|variable\|run\|auth\|status\|api)\b)(?:(?:\x22[^\x22]*\x22)\|(?:'[^']*')\|\S+))?)*\s+ssh-key\s+list\b` |
| `gh-secret-list` | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\|release\|issue\|ssh-key\|secret\|variable\|run\|auth\|status\|api)\b)(?:(?:\x22[^\x22]*\x22)\|(?:'[^']*')\|\S+))?)*\s+secret\s+list\b` |
| `gh-variable-list` | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\|release\|issue\|ssh-key\|secret\|variable\|run\|auth\|status\|api)\b)(?:(?:\x22[^\x22]*\x22)\|(?:'[^']*')\|\S+))?)*\s+variable\s+list\b` |
| `gh-auth-status` | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\|release\|issue\|ssh-key\|secret\|variable\|run\|auth\|status\|api)\b)(?:(?:\x22[^\x22]*\x22)\|(?:'[^']*')\|\S+))?)*\s+auth\s+status\b` |
| `gh-status` | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\|release\|issue\|ssh-key\|secret\|variable\|run\|auth\|status\|api)\b)(?:(?:\x22[^\x22]*\x22)\|(?:'[^']*')\|\S+))?)*\s+status\b` |
| `gh-api-explicit-get` | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\|release\|issue\|ssh-key\|secret\|variable\|run\|auth\|status\|api)\b)(?:(?:\x22[^\x22]*\x22)\|(?:'[^']*')\|\S+))?)*\s+api\b.*(?:-X\|--method)\s+GET\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `gh-repo-delete` | gh repo delete permanently deletes a GitHub repository. This cannot be undone. | high |
| `gh-repo-archive` | gh repo archive makes a repository read-only. While reversible, it stops all write access. | high |
| `gh-gist-delete` | gh gist delete permanently deletes a Gist. | high |
| `gh-release-delete` | gh release delete permanently deletes a release. | high |
| `gh-issue-delete` | gh issue delete permanently deletes an issue. | high |
| `gh-ssh-key-delete` | gh ssh-key delete removes an SSH key, potentially breaking access. | high |
| `gh-secret-delete` | gh secret delete removes GitHub Actions secrets. | high |
| `gh-variable-delete` | gh variable delete removes GitHub Actions variables. | high |
| `gh-repo-deploy-key-delete` | gh repo deploy-key delete removes a deploy key and can break access. | high |
| `gh-run-cancel` | gh run cancel stops a workflow run and may interrupt deployments. | high |
| `gh-api-delete-actions-secret` | gh api DELETE actions/secrets removes GitHub Actions secrets. | high |
| `gh-api-delete-actions-variable` | gh api DELETE actions/variables removes GitHub Actions variables. | high |
| `gh-api-delete-hook` | gh api DELETE hooks removes repository webhooks. | high |
| `gh-api-delete-deploy-key` | gh api DELETE keys removes deploy keys. | high |
| `gh-api-delete-release` | gh api DELETE releases removes GitHub releases. | high |
| `gh-api-delete-repo` | gh api DELETE calls can be destructive. Please verify the endpoint. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "platform.github:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "platform.github:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## GitLab Platform

**Pack ID:** `platform.gitlab`

Protects against destructive GitLab platform operations like deleting projects, releases, protected branches, and webhooks.

### Keywords

Commands containing these keywords are checked against this pack:

- `glab`
- `gitlab-rails`
- `gitlab-rake`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `glab-repo-list` | `glab(?:\s+--?\S+(?:\s+\S+)?)*\s+repo\s+list\b` |
| `glab-repo-view` | `glab(?:\s+--?\S+(?:\s+\S+)?)*\s+repo\s+view\b` |
| `glab-repo-clone` | `glab(?:\s+--?\S+(?:\s+\S+)?)*\s+repo\s+clone\b` |
| `glab-mr-list` | `glab(?:\s+--?\S+(?:\s+\S+)?)*\s+mr\s+list\b` |
| `glab-mr-view` | `glab(?:\s+--?\S+(?:\s+\S+)?)*\s+mr\s+view\b` |
| `glab-issue-list` | `glab(?:\s+--?\S+(?:\s+\S+)?)*\s+issue\s+list\b` |
| `glab-issue-view` | `glab(?:\s+--?\S+(?:\s+\S+)?)*\s+issue\s+view\b` |
| `glab-variable-list` | `glab(?:\s+--?\S+(?:\s+\S+)?)*\s+variable\s+list\b` |
| `glab-release-list` | `glab(?:\s+--?\S+(?:\s+\S+)?)*\s+release\s+list\b` |
| `glab-release-view` | `glab(?:\s+--?\S+(?:\s+\S+)?)*\s+release\s+view\b` |
| `glab-api-explicit-get` | `glab(?:\s+--?\S+(?:\s+\S+)?)*\s+api\b.*(?:-X\|--method)\s+GET\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `glab-repo-delete` | glab repo delete permanently deletes a GitLab project. | high |
| `glab-repo-archive` | glab repo archive makes a GitLab project read-only. | high |
| `glab-release-delete` | glab release delete removes GitLab releases. | high |
| `glab-variable-delete` | glab variable delete removes GitLab CI/CD variables. | high |
| `glab-api-delete-project` | glab api DELETE /projects/* deletes a GitLab project. | high |
| `glab-api-delete-release` | glab api DELETE releases removes GitLab releases. | high |
| `glab-api-delete-variable` | glab api DELETE variables removes CI/CD variables. | high |
| `glab-api-delete-protected-branch` | glab api DELETE protected_branches removes branch protections. | high |
| `glab-api-delete-hook` | glab api DELETE hooks removes GitLab webhooks. | high |
| `gitlab-rails-runner-destructive` | gitlab-rails runner destructive operations can remove data. | high |
| `gitlab-rake-destructive` | gitlab-rake destructive maintenance tasks can delete or replace data. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "platform.gitlab:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "platform.gitlab:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

