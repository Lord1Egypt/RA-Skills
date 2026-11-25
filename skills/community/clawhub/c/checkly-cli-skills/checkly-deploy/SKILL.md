---
name: checkly-deploy
description: Deploy Checkly checks to production with npx checkly deploy, including force deployment, preview changes, and CI/CD integration strategies. Use when deploying monitoring checks, updating production configuration, or integrating with deployment pipelines. Triggers on checkly deploy, deploy checks, production deployment, CI/CD deployment.
---

# checkly deploy

Deploy project definitions to Checkly with a reviewed, property-level plan. These commands contact Checkly; `validate` checks configuration but is not a deploy preview.

## Review and apply

Validation can stop planning: a `SlackAppAlertChannel` with destinations requires a connected Checkly Slack app when the account API reports its state. This includes channels deployed before disconnection; connect the app or remove the channel. Remove retired `me-south-1` from checks, monitors, groups, `checks.locations` and `cli.runLocation`. These checks also apply to `validate`, `test` and `pw-test`.

Checks and monitors send their default degraded/max limits explicitly, matching existing backend defaults rather than changing unset deployed limits. Review any baseline or payload-format changes in the plan; ICMP and traceroute validation compares explicit values with effective defaults (see `checkly-monitors`).

```bash
npx checkly validate
npx checkly deploy --preview
# Machine-readable plan (does not deploy)
npx checkly deploy --dry-run > deploy-plan.json
# Apply a reviewed plan using the token returned by the preview
npx checkly deploy --plan-token <plan-token>
```

These are command examples, not captured terminal output. A preview or dry run uploads neither code bundles nor Playwright snapshots. An ordinary deploy parses, validates and bundles locally, requests a plan, asks for confirmation, then uploads and applies that plan. The plan marks `+` creates, `~` updates, `-` deletes and `=` baseline writes, and shows property and script diffs without revealing secrets.

Planning is on by default. Unchanged resources are not written. If the account changes between planning and applying, the CLI refuses the stale plan. An unpinned `--force` run can make a new plan and retry; a run pinned with `--plan-token` stops instead. Preview again and review the new changes before retrying.

The first planned deploy, including the first after `--no-plan`, writes existing resources once to establish a baseline. Identical resources show `=` and count under “to set a baseline”; changed resources show `~`. Payload changes can also produce updates with the note `payload format changed (CLI upgrade)`. Review resets carefully.

A plan with nothing to apply exits 0 without confirmation, including in CI/agent mode without `--force`. It prints `No changes.` and ends with `Project "<name>" is up to date.` It still records deployment state and renews the comparison baseline. Explicit scheduling with scope `all` can run unchanged checks subject to frequency/threshold filters.

## Confirmation and output

In a terminal, the plan and `Apply these changes?` prompt go to stderr. In CI or agent mode, a deploy that needs approval returns exit **3** with `status: "confirmation_required"`, planned changes and a `confirmCommand` pinned to the plan token when available. Present the changes and run that command verbatim after authorization. Exit **2** means invalid flags or arguments; **1** means failure. Do not treat exit 3 as success or retry it blindly with `--force`.

`--force` skips confirmation; it does not disable planning or bypass a supplied plan token. Use it for already authorized automation. Final results go to stdout; progress, warnings, hints, errors and interactive plans/prompts go to stderr. `--dry-run` emits a JSON envelope on stdout: `status: "dry_run"`, `changes`, `confirmCommand`, and (when planned) `preview: { planToken, diff }`. An unplanned fallback has no `preview` object. `--preview` emits a human-readable plan and a command to apply the token later.

## Options

| Flag | Contract |
|---|---|
| `--preview`, `-p` | Show changes without applying them. |
| `--dry-run` | Print a JSON preview without deploying. |
| `--plan` / `--no-plan` | Planning defaults on. Opting out writes every resource. |
| `--plan-token` | Require the supplied plan token to match; unavailable with `--no-plan`. |
| `--fail-on-drift` / `--no-fail-on-drift` | Refuse overwriting changes made in Checkly since the previous planned deploy. |
| `--prune-unmanaged-relations` | Delete externally added alert subscriptions/private-location assignments; requires planning. |
| `--preserve-resources` | Detach resources removed from code, preserving resources and run history for UI management. |
| `--force`, `-f` | Skip confirmation in authorized automation. |
| `--output`, `-o` | Show changes after deployment; a boolean, not an output-format selector. |
| `--verbose`, `-v` | Include resource names and IDs. |
| `--config`, `-c` | Select the project configuration. |
| `--verify-runtime-dependencies` / `--no-verify-runtime-dependencies` | Runtime dependency validation defaults on. |
| `--cancel-in-progress-deployment` | Intentionally supersede an in-progress deployment instead of waiting. |

Migration warning: `--prune-relations` was renamed to `--prune-unmanaged-relations`. Without pruning, unmanaged subscriptions and assignments are kept and listed in the plan.

If planning is unavailable, ordinary deploys may fall back with a warning. `--plan-token`, relation pruning and drift protection require a plan and fail rather than silently dropping that protection.

## Drift protection and writing web changes into code

```bash
# For an authorized pipeline: protect web edits and preserve removed resources/history
npx checkly deploy --force --fail-on-drift --preserve-resources
# Review drift without applying
npx checkly deploy --preview --fail-on-drift
```

`--fail-on-drift` exits 1 and writes nothing if the deploy would overwrite externally edited or deleted resources. `CHECKLY_FAIL_ON_DRIFT=1` enables it across a pipeline; `--no-fail-on-drift` overrides the environment. It cannot be used with `--no-plan`. `--preview` prints the plan before failing on drift; `--dry-run` ignores this guard and reports changes in JSON. Baseline-only writes have no previous baseline to compare, so produce a warning instead.

When web edits can be represented in code, the interactive prompt offers **Update my code with the changes made in Checkly**. This edits construct files in place, preserves style and emits helpers such as `Frequency`, `RetryStrategyBuilder` and `AssertionBuilder`. It then stops without deploying. Review `git diff` before another deploy. References, secrets and computed values that cannot be safely rewritten are listed for manual migration; a write-back error may leave some files updated, so review them even on failure.

## Properties owned by the deployment

The following properties have explicit omission resets. Dashboard resets apply only to the listed text properties; other omitted Dashboard properties preserve stored values, including web-only edits. Put intended settings into code before applying the plan.

| Resource | Defaults when omitted |
|---|---|
| API, browser, multistep checks and `CheckGroupV1` | `retryStrategy`: one immediate retry in another region. |
| Monitors and `PlaywrightCheck` | No CLI retries; Playwright handles its own retries. |
| Checks | Empty `description` and `intent`; `aiAutoRepairEnabled` follows the account setting. |
| Alert channels | `sendRecovery: true`, `sendFailure: true`, `sendDegraded: false`, `sslExpiry: false`, `sslExpiryThreshold: 30`. |
| `PrivateLocation` | No `proxyUrl`. |
| `Dashboard` | Only the text properties are cleared: `logo` and `header` to `''`; `customUrl`, `customDomain`, `favicon`, `link`, `description` to `null`. All other omitted Dashboard properties preserve stored values (web edits included): tags, layout, refresh/pagination, display/privacy booleans and custom CSS. Set intended values explicitly. [Immutable synthesis and bundle sources](https://github.com/checkly/checkly-cli/tree/34833c407768368d6ce64c759a979aec029b732f/packages/cli/src/constructs). |
| `MaintenanceWindow` | `timezone: 'UTC'`, no `repeatEndsAt`; changing timezone while active fails until it ends. |

Removing `group` from a `PlaywrightCheck` also removes the deployed group membership. See `checkly-constructs` for removed-property migration and `shouldFail` restrictions.

## Immediate scheduling is opt-in

Deploying configures ongoing monitoring according to each check's schedule, but does not trigger an immediate run by default.

| Flag | Meaning |
|---|---|
| `--schedule-on-deploy` / `--no-schedule-on-deploy` | Enable immediate post-deploy runs; default off. |
| `--schedule-on-deploy-scope=changed\|all` | Default `changed`: created/updated checks only. `all` includes unchanged checks. |
| `--schedule-on-deploy-threshold=<n\|auto>` | Schedule none if the eligible count exceeds the threshold. Heartbeats do not count. `auto` currently selects 500; server cap 2000. |
| `--schedule-on-deploy-min-frequency=<n\|auto>` | Skip checks running more frequently than this many minutes. `0` includes every frequency; `auto` currently selects 10. |

Threshold and minimum-frequency values must be non-negative whole numbers or `auto`. Explicit scheduling sub-options without `--schedule-on-deploy` are invalid (exit 2). Scope and frequency filters apply before the threshold. The CLI reports counts and reasons for skipped scheduling; server-selected limits can change.

```bash
# Explicitly schedule all eligible checks, including frequent ones, after deployment
npx checkly deploy --schedule-on-deploy --schedule-on-deploy-scope=all --schedule-on-deploy-min-frequency=0
```

## Authorized CI deployment

Set `CHECKLY_API_KEY` and `CHECKLY_ACCOUNT_ID` before starting the CLI. Use a supported Node.js runtime **22.13.0 or later**, install the locked project dependencies, run the intended tests, and apply only after they pass.

`--force` skips confirmation, including approval of deletions in the plan; `--fail-on-drift` protects web edits, not resources removed from code. The examples below use `--preserve-resources` to detach removed resources and keep their history. Review the plan and intentionally authorize the pipeline's creates, updates, resets and detachments. If deletion is intended, review a preview without preservation and pin its `--plan-token` when applying that exact approved plan; do not rely on drift protection as a deletion guard.

```bash
# Run only in already authorized automation; preservation does not make updates harmless.
npm ci
npx checkly test && npx checkly deploy --force --fail-on-drift --preserve-resources
```

### Minimal GitLab CI example

Store `CHECKLY_API_KEY` and `CHECKLY_ACCOUNT_ID` as masked/protected GitLab CI/CD variables, scoped to the intended account/environment; never put their values in YAML. The manual default-branch job is an approval gate for the reviewed changes, not permission for an agent to start it. The Node image is above the CLI's minimum runtime floor. Use a deployment-stage job in the project's existing stage list.

```yaml
deploy-checks:
  stage: deploy
  image: node:24
  resource_group: checkly-production
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: manual
  script:
    - npm ci
    - npx checkly test
    - npx checkly deploy --force --fail-on-drift --preserve-resources
```

The job inherits the two protected variables. Restrict default-branch and deployment approval permissions, and use the same locked code and account when reviewing the plan and running the approved job.

### Test-and-review helper

`scripts/test-and-deploy.sh` intentionally accepts no arguments: it tests the default project, then lets the CLI present/confirm its plan. In CI/agent mode a nonempty unapproved plan returns exit 3; an unchanged plan can return 0. After approval, run the returned `confirmCommand` verbatim **directly**, not through the helper. For a custom configuration or already authorized CI flags, invoke `checkly test` and `checkly deploy` directly with the same `--config` path. The helper rejects arguments before running any checks rather than testing one configuration and forwarding a different deploy target.

An empty test selection fails by default. Do not suppress it in a gate intended to prove tests ran. Jenkins, TeamCity and AWS CodeBuild are detected alongside other CI providers; `CI=false`, `0`, `no` or `off` disables CI detection even on provider hosts. Prefer serialized deployment jobs per project.

## Removing resources and projects

Normal deployment deletes resources removed from code and their run history. Use `--preserve-resources` to detach them instead. Review deletions in the plan before authorizing deployment.

```bash
npx checkly deploy --preview --preserve-resources
npx checkly deploy --preserve-resources
# Decommission a project only when explicitly intended
npx checkly destroy
# Keep its resources as account-level resources
npx checkly destroy --preserve-resources
```

`destroy` also accepts `--force`, `--config` and `--cancel-in-progress-deployment`. It follows asynchronous progress, waits on concurrent operations and treats an already-missing project as deleted. `validate` is not a preview of deletion. A transient lock while verifying a deployment is retried up to three times. Failure to retrieve a heartbeat ping URL after success produces a warning rather than invalidating the deployment.

## Related skills

See `checkly-test`, `checkly-auth`, `checkly-config`, and `checkly-import` for test gates, credentials, defaults and existing-resource adoption.
