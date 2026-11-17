---
name: checkly-deploy
description: Deploy Checkly checks to production with npx checkly deploy, including force deployment, preview changes, and CI/CD integration strategies. Use when deploying monitoring checks, updating production configuration, or integrating with deployment pipelines. Triggers on checkly deploy, deploy checks, production deployment, CI/CD deployment.
---

# checkly deploy

Deploy checks to Checkly cloud with `npx checkly deploy`.

## Quick start

```bash
# Deploy with confirmation prompt
npx checkly deploy

# Force deploy (skip prompt)
npx checkly deploy --force

# Keep removed code resources in Checkly instead of deleting run history
npx checkly deploy --preserve-resources

# Preview changes without deploying
npx checkly validate
npx checkly deploy --preview

# Destroy the deployed project resources when intentionally decommissioning
npx checkly destroy --force
```

## How deployment works

`npx checkly deploy`:
1. ✅ Parses your project
2. ✅ Validates all checks
3. ✅ Bundles code and dependencies
4. ✅ Shows preview of changes
5. ⚠️  Asks for confirmation
6. ✅ Creates/updates resources in Checkly cloud
7. ✅ Schedules checks to run continuously

## Command reference

```bash
npx checkly deploy [options]
```

### Options

| Flag | Description |
|------|-------------|
| `--force, -f` | Skip confirmation prompt |
| `--preserve-resources` | Detach resources removed from code, keeping them and their run history in Checkly for UI management instead of deleting them |
| `--verbose, -v` | Show created/updated resource names and IDs during deploy output |
| `--cancel-in-progress-deployment` | If a deployment for this project is already in progress, cancel it instead of waiting for it to finish |
| `--config=<path>` | Path to checkly.config.ts |
| `--verify-runtime-dependencies` | Validate npm package compatibility |

### Destroy options

```bash
npx checkly destroy [options]
```

| Flag | Description |
|------|-------------|
| `--force, -f` | Skip confirmation prompt |
| `--config=<path>` | Path to checkly.config.ts/js |
| `--preserve-resources` | Remove the project link but keep project resources as normal account-level resources |
| `--cancel-in-progress-deployment` | If a deploy or destroy operation is already in progress, cancel it instead of waiting before retrying |

## Deployment workflows

### Interactive deployment

```bash
npx checkly deploy

# Output:
# Parsing your project... done
# 
# Changes to be deployed:
#   + 2 checks to create
#   ~ 1 check to update
#   - 0 checks to delete
#
# Do you want to deploy? (y/N)
```

Type `y` to confirm, `n` to cancel.

### Force deployment (CI/CD)

```bash
npx checkly deploy --force

# No confirmation prompt
# Useful for automated pipelines
```

`--force` skips confirmation prompts, including the destructive-delete guard. In CI, use it only when the pipeline already reviewed the deployment diff or intentionally accepts destructive changes.

### Agent-mode confirmation

In agent mode, running `npx checkly deploy` without `--force` returns exit code 2 and a JSON `confirmation_required` envelope before project parsing. Present its `changes` to the user and run the returned `confirmCommand` verbatim only after explicit approval.

The confirmation envelope warns that deletion is possible but cannot list the exact resources yet. Preview first whenever resources may have been removed from code:

```bash
npx checkly deploy --preview --verbose
```

Review and present any deletions before requesting approval. The interactive itemized delete guard is skipped by `--force`, including the `--force` in an approved `confirmCommand`, so it is not a substitute for previewing. The generated command omits parser defaults and may include deliberate resolved-target flags; do not edit it or append `--force` yourself.

### Preserve removed resources

When a resource is removed from code, a normal deploy deletes it from Checkly and loses run history. With `--preserve-resources`, the resource is detached from the project instead: it remains in the Checkly account, keeps its run history, and becomes UI-managed.

```bash
# Prefer this when removing checks/groups/dashboards from code but preserving history
npx checkly deploy --preserve-resources

# CI-safe deploy that detaches removed resources instead of deleting them
npx checkly deploy --force --preserve-resources
```

Without `--preserve-resources`, interactive non-forced deploys now do an extra dry-run when deletions are possible and require explicit confirmation before permanently deleting removed resources. Forced deploys skip that second prompt.

### Verbose deployment output

```bash
npx checkly deploy --verbose

# Shows created/updated resources with human-readable names and IDs
# Useful when auditing exactly which Checkly resources changed
```

`--verbose` is most helpful when you need to match deploy output back to specific Checkly resources during debugging or rollout review.

### Concurrent deployments

Deploy runs asynchronously with live progress. If another deployment for the same project is already running, the CLI normally waits for that deployment to finish. Use `--cancel-in-progress-deployment` only when you intentionally want the new deployment to replace the in-flight one:

```bash
npx checkly deploy --force --cancel-in-progress-deployment
```

In CI, prefer serializing deploy jobs per environment. Add `--cancel-in-progress-deployment` only for workflows where a newer commit should supersede an older still-running deploy.

### Destroying/decommissioning a project

`npx checkly destroy` is destructive. Use it only when intentionally removing a Checkly CLI project from the account, and prefer a reviewed PR or explicit operator confirmation before running it.

```bash
# Preview project state first
npx checkly validate

# Destroy project-managed resources, skipping the prompt only in approved automation
npx checkly destroy --force

# Detach the project but keep checks/groups/dashboards as account-level resources
npx checkly destroy --force --preserve-resources
```

Destroy uses the async backend endpoint: large-project deletion streams progress instead of timing out at the initial HTTP request, waits/retries when another deploy/delete is already in progress, and treats an already-missing project as successfully deleted. Use `--cancel-in-progress-deployment` only when the new destroy should supersede the current in-flight operation.

### Preview changes

```bash
# Validate without deploying
npx checkly validate

# Shows what would be deployed
# Catches errors before deployment
```

## CI/CD integration

### GitHub Actions

```yaml
name: Deploy Checks

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version: '22.13.0'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Test checks
        env:
          CHECKLY_API_KEY: ${{ secrets.CHECKLY_API_KEY }}
          CHECKLY_ACCOUNT_ID: ${{ secrets.CHECKLY_ACCOUNT_ID }}
        run: npx checkly test
      
      - name: Deploy checks
        env:
          CHECKLY_API_KEY: ${{ secrets.CHECKLY_API_KEY }}
          CHECKLY_ACCOUNT_ID: ${{ secrets.CHECKLY_ACCOUNT_ID }}
        run: npx checkly deploy --force --preserve-resources
```

### GitLab CI

```yaml
deploy-checks:
  stage: deploy
  only:
    - main
  script:
    - npm ci
    - npx checkly test
    - npx checkly deploy --force
  variables:
    CHECKLY_API_KEY: $CHECKLY_API_KEY
    CHECKLY_ACCOUNT_ID: $CHECKLY_ACCOUNT_ID
```

### Deploy on application deployment

```bash
#!/bin/bash
# deploy-app-and-monitoring.sh

# Deploy application
./deploy-app.sh

# Deploy updated monitoring checks
npx checkly deploy --force

echo "✅ Application and monitoring deployed"
```

## Deployment strategies

### Test before deploy

```bash
# Validate locally first
npx checkly test

# Deploy only if tests pass
if [ $? -eq 0 ]; then
  npx checkly deploy --force
fi
```

### Staged deployment

```bash
# 1. Deploy to staging project
CHECKLY_ACCOUNT_ID=$STAGING_ACCOUNT npx checkly deploy --force

# 2. Run smoke tests
npm run smoke-tests

# 3. Deploy to production
CHECKLY_ACCOUNT_ID=$PROD_ACCOUNT npx checkly deploy --force
```

### Feature branch testing

```yaml
# GitHub Actions - test on PRs, deploy on main
on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - run: npm ci
      - run: npx checkly test  # Test on all branches
        env:
          CHECKLY_API_KEY: ${{ secrets.CHECKLY_API_KEY }}
          CHECKLY_ACCOUNT_ID: ${{ secrets.CHECKLY_ACCOUNT_ID }}
  
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'  # Deploy only on main
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - run: npm ci
      - run: npx checkly deploy --force
        env:
          CHECKLY_API_KEY: ${{ secrets.CHECKLY_API_KEY }}
          CHECKLY_ACCOUNT_ID: ${{ secrets.CHECKLY_ACCOUNT_ID }}
```

## What gets deployed

### Created resources

- ✅ New checks (API, Browser, Multi-Step, Monitors)
- ✅ Check groups
- ✅ Alert channel subscriptions
- ✅ Private location assignments
- ✅ Retry strategies
- ✅ Environment variables

### Updated resources

- ✅ Check configuration changes
- ✅ Schedule changes (frequency, locations)
- ✅ Code changes (for checks with scripts)
- ✅ Alert channel assignments

### NOT deployed

- ❌ Alert channel definitions (configure in UI)
- ❌ Private location infrastructure (configure in UI)
- ❌ Account-level settings
- ❌ Team/user management

## Deployment preview

Before deployment, Checkly shows a summary:

```
Changes to be deployed:

+ Create checks:
  • homepage-check (Browser)
  • api-status-check (API)

~ Update checks:
  • login-flow-check (Browser)
    - frequency: 10 → 5 minutes
    - locations: +eu-west-1

- Delete checks:
  (none)

Detached (kept in account, now UI-managed):
  • legacy-status-page (StatusPage)

+ Create groups:
  • critical-checks

~ Update groups:
  (none)
```

## Troubleshooting

### "No changes to deploy"

**Cause**: All checks already deployed and up-to-date

**Solution**: This is normal. Only deploy when you have changes.

### "Cannot deploy: validation errors"

**Solution**:
```bash
# Check validation errors
npx checkly validate

# Fix errors in your code
# Re-run validate until no errors

# Deploy
npx checkly deploy
```

### "Quota exceeded" errors

**Cause**: Account plan limits reached (checks, locations, etc.)

**Solution**:
- Upgrade your Checkly plan
- Delete unused checks in UI
- Contact Checkly support

### Deploy or destroy hangs, conflicts, or times out

The CLI follows async deploy/destroy progress and can wait for an in-flight operation. If it appears stuck, first confirm whether another deploy/delete is already running for the same project. Use `--cancel-in-progress-deployment` only when you intentionally want the current command to replace that in-flight operation.

**Solution:**
```bash
# Check network connectivity
curl https://api.checklyhq.com/health

# Verify authentication
npx checkly whoami

# Try again with verbose output
npx checkly deploy --verbose --force
```

## Related Skills

- See `checkly-test` to test before deploying
- See `checkly-import` to import existing checks
- See `checkly-checks` for check creation
- See `checkly-auth` for CI/CD authentication
