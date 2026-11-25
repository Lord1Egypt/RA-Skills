# GitHub Check Re-run setup and compatibility

This is an **opt-in workflow change**, not a reporter option. Obtain approval for
Checkly GitHub App access, the exact repository/job, handler permissions, and the
selected job **plus every dependent job's** side effects before enabling it.

## Prerequisites and caller

- The Checkly GitHub App must have access to the repository and support detached
  Checkly GitHub Check reporting. Metadata is not authorization.
- Re-run requires **Checkly CLI 10.1.0 or newer**. The action prefers the project's
  installed `checkly` dependency: changing `cli-version` alone does not upgrade an
  older project-local CLI, and an exact stable input pin must match that dependency.
  Confirm the resolved version supports job-ID forwarding; version tags/ranges or
  prereleases passing the action's preflight are not proof of feature support.
- Set `github-check-rerun: true` and `github-job-id: ${{ job.check_run_id }}`. This
  numeric ID is not `${{ github.job }}` (the job key). The context property is not
  available on GitHub Enterprise Server; do not manufacture a replacement ID.
- Detached runs with missing job IDs or older stable resolved CLIs fail before
  running checks. `reporting: github-actions` and fallback-to-waiting runs ignore
  the Re-run opt-in; setting the metadata or Markdown reporter is not sufficient.

Add the following step only to an existing reviewed job with checkout, dependency
setup, and approved Checkly credentials. `reporting: github-check` requires the app
integration rather than silently relying on fallback-to-waiting behavior:

```yaml
- uses: checkly/checkly-action@v1
  with:
    command: test
    reporting: github-check
    github-check-rerun: true
    github-job-id: ${{ job.check_run_id }}
  env:
    CHECKLY_API_KEY: ${{ secrets.CHECKLY_API_KEY }}
    CHECKLY_ACCOUNT_ID: ${{ secrets.CHECKLY_ACCOUNT_ID }}
```

## Separate handler on the default branch

A click on the Checkly GitHub Check's Re-run button makes Checkly send a
`repository_dispatch` event of type `checkly-github-check-rerun`. A separate workflow
must exist **on the repository's default branch** and invoke the rerun sub-action;
without it, the metadata does not re-run the job.

```yaml
name: Checkly re-run

on:
  repository_dispatch:
    types: [checkly-github-check-rerun]

permissions: {}

jobs:
  rerun:
    runs-on: ubuntu-latest
    permissions:
      actions: write
    timeout-minutes: 5
    steps:
      - uses: checkly/checkly-action/rerun@v1
```

Keep the `types` filter. Any other workflow with an unfiltered
`on: repository_dispatch` trigger also runs on each click; audit those consumers
before approval. The handler needs only its default `GITHUB_TOKEN` with
`actions: write`; it checks out no repository code and needs no Checkly secrets.
Self-hosted runners need `gh` on `PATH`.

The sub-action validates the event type/version, repository, numeric run/job IDs,
and the job's run/commit before requesting a re-run. Do not replace it with an
unchecked dispatch-to-rerun command. GitHub re-runs the selected job and dependent
jobs as another attempt of the original workflow, using its commit, workflow file,
and original actor privileges; this can repeat deployments or other writes, not
just monitoring checks. A new attempt starts a new Checkly test session.

## Source contract

Authored setup guidance verified against
[`checkly/checkly-action` source](https://github.com/checkly/checkly-action/tree/681b97c6f347b61bf2407c96d94707c3442af9f0),
including its [Re-run documentation](https://github.com/checkly/checkly-action/blob/681b97c6f347b61bf2407c96d94707c3442af9f0/README.md#re-run-a-detached-check),
[caller inputs](https://github.com/checkly/checkly-action/blob/681b97c6f347b61bf2407c96d94707c3442af9f0/action.yml),
and [handler action](https://github.com/checkly/checkly-action/blob/681b97c6f347b61bf2407c96d94707c3442af9f0/rerun/action.yml).
The YAML above is an authored example, not a captured command response or an
installed workflow. Review the upstream action and any moving tag before use.
