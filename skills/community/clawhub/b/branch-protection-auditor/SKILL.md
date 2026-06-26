---
name: branch-protection-auditor
description: Audit GitHub/GitLab branch protection rules across repositories. Check required reviews, status checks, force push restrictions, admin bypass, and CODEOWNERS enforcement — then flag gaps and generate recommended rulesets.
---

# Branch Protection Auditor

Audit branch protection rules across your GitHub or GitLab repos. Find repos with no protection on main, missing required reviews, disabled status checks, admin bypass enabled, and missing CODEOWNERS — then generate recommended rulesets to fix the gaps.

Use when: "audit branch protection", "are our repos protected", "who can push to main", "review requirements", "security audit repos", "branch rules", "CODEOWNERS check", or before compliance audits.

## Commands

### 1. `audit` — Scan All Repos

#### Step 1: List Repositories

```bash
# GitHub — list org repos
gh api "orgs/$ORG/repos?per_page=100&type=all" --paginate | \
  python3 -c "
import json, sys
repos = json.load(sys.stdin)
for r in repos:
    if not r['archived']:
        print(f'{r[\"full_name\"]}\t{r[\"default_branch\"]}\t{r[\"private\"]}')
"

# Or list user repos
gh repo list --json nameWithOwner,defaultBranchRef --limit 100
```

#### Step 2: Check Protection Rules

```bash
# For each repo, check branch protection
gh api "repos/$REPO/branches/$DEFAULT_BRANCH/protection" 2>/dev/null | python3 -c "
import json, sys
try:
    p = json.load(sys.stdin)
    checks = {
        'required_reviews': p.get('required_pull_request_reviews') is not None,
        'min_reviewers': p.get('required_pull_request_reviews', {}).get('required_approving_review_count', 0),
        'dismiss_stale': p.get('required_pull_request_reviews', {}).get('dismiss_stale_reviews', False),
        'require_code_owner': p.get('required_pull_request_reviews', {}).get('require_code_owner_reviews', False),
        'status_checks': p.get('required_status_checks') is not None,
        'strict_checks': p.get('required_status_checks', {}).get('strict', False),
        'enforce_admins': p.get('enforce_admins', {}).get('enabled', False),
        'force_push': not p.get('allow_force_pushes', {}).get('enabled', True),
        'deletions': not p.get('allow_deletions', {}).get('enabled', True),
        'linear_history': p.get('required_linear_history', {}).get('enabled', False),
        'signed_commits': p.get('required_signatures', {}).get('enabled', False),
    }
    for k, v in checks.items():
        status = '✅' if v else '❌'
        print(f'  {status} {k}: {v}')
except:
    print('  ❌ NO PROTECTION RULES')
"
```

#### Step 3: Check CODEOWNERS

```bash
# Check if CODEOWNERS exists
for path in ".github/CODEOWNERS" "CODEOWNERS" "docs/CODEOWNERS"; do
  if gh api "repos/$REPO/contents/$path" --silent 2>/dev/null; then
    echo "✅ CODEOWNERS found at $path"
    break
  fi
done || echo "❌ No CODEOWNERS file"
```

#### Step 4: Generate Report

```markdown
# Branch Protection Audit — [Org Name]

## Summary
- Repos scanned: 45
- Protected: 32 (71%)
- Unprotected: 13 (29%) 🔴
- Fully compliant: 18 (40%)

## Unprotected Repos (Critical)
| Repo | Default Branch | Public? | Last Commit | Risk |
|------|---------------|---------|-------------|------|
| api-service | main | No | 2 days ago | 🔴 Active, unprotected |
| legacy-app | master | No | 1 year ago | 🟡 Inactive |
| docs-site | main | Yes | 1 week ago | 🔴 Public, unprotected |

## Protection Gaps (Protected but incomplete)
| Repo | Reviews | Status Checks | Admin Enforce | Force Push Block | CODEOWNERS |
|------|---------|--------------|---------------|-----------------|------------|
| web-app | ✅ 2 | ✅ | ❌ | ✅ | ❌ |
| mobile-api | ✅ 1 | ❌ | ❌ | ✅ | ✅ |
| data-pipeline | ✅ 1 | ✅ | ✅ | ❌ | ❌ |

## Recommendations
1. Enable protection on 13 unprotected repos (script provided)
2. Require min 2 reviewers on all repos (currently 8 repos have 1)
3. Enable admin enforcement on 24 repos (admins can bypass)
4. Add CODEOWNERS to 27 repos
5. Block force push on 5 repos that allow it
```

### 2. `fix` — Apply Recommended Protection Rules

Generate a script to apply branch protection:

```bash
# Apply protection to a repo
gh api -X PUT "repos/$REPO/branches/main/protection" \
  -f required_pull_request_reviews='{"required_approving_review_count":2,"dismiss_stale_reviews":true,"require_code_owner_reviews":true}' \
  -f required_status_checks='{"strict":true,"contexts":["ci/test","ci/lint"]}' \
  -f enforce_admins=true \
  -f restrictions=null \
  -F allow_force_pushes=false \
  -F allow_deletions=false
```

### 3. `compliance` — Map to Security Frameworks

Generate compliance evidence for:
- SOC 2: CC6.1 (access controls), CC8.1 (change management)
- ISO 27001: A.12.1.2 (change management)
- NIST: CM-3 (configuration change control)
- PCI-DSS: 6.4 (change control procedures)
