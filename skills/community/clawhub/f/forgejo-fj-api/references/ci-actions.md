# Forgejo CI and Actions

This reference assumes `FORGEJO_URL` and `FORGEJO_TOKEN` are already set.

If required bins, env vars, or `fj` setup are missing, return to `SKILL.md`
prerequisites, readiness checks, or troubleshooting before proceeding.

Use this reference when `fj` is not enough for CI or Forgejo Actions tasks.

## Fast path with `fj`

Use `fj` first for quick checks:

```bash
fj --repo owner/repo actions tasks
fj pr status 55
```

Use this when the user mainly needs recent runs or a simple status
summary.

## REST API coverage

Forgejo API coverage for Actions varies by Forgejo version. Check the target
instance at:

```text
https://<your-forgejo-host>/api/swagger
```

Current Forgejo source exposes these Actions endpoints:

```http
GET /repos/{owner}/{repo}/actions/tasks
GET /repos/{owner}/{repo}/actions/runs
GET /repos/{owner}/{repo}/actions/runs/{run_id}
GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs
POST /repos/{owner}/{repo}/actions/workflows/{workflowfilename}/dispatches
```

`GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs` is present in current
source, but was not found in any checked published tags. Treat it as unreleased
or branch-only unless the target instance Swagger documents it explicitly.

Job-log coverage is also version-sensitive. Checked Forgejo source exposes job-log
paths as web routes rather than stable REST API endpoints, and the URL shape has
changed across versions.

Workflow dispatch requires a `ref`. Current server implementations also support
optional `inputs`, and `return_run_info=true` can switch the response from `204`
to a created-run payload.

## Checking CI for a pull request

1. Get the pull request metadata and head SHA.

```bash
curl -sS \
  -H "Authorization: token $FORGEJO_TOKEN" \
  -H "Accept: application/json" \
  "$FORGEJO_URL/api/v1/repos/$OWNER/$REPO/pulls/55" | jq -r '.head.sha'
```

2. Fetch commit statuses.

```bash
curl -sS \
  -H "Authorization: token $FORGEJO_TOKEN" \
  -H "Accept: application/json" \
  "$FORGEJO_URL/api/v1/repos/$OWNER/$REPO/statuses/$SHA" | jq '.[] | {context, status, target_url}'
```

Related status endpoints also exist under:

```http
GET /repos/{owner}/{repo}/commits/{ref}/statuses
GET /repos/{owner}/{repo}/commits/{ref}/status
```

3. If needed, inspect workflow runs through the Actions endpoints.
4. Only use the run-jobs endpoint when the target instance Swagger documents it.

## Reading job logs

If the target instance exposes job and log endpoints in Swagger, use them.
Otherwise say the instance does not document those endpoints and fall back to the
best available run or status summary rather than inventing details.

## `fj-ex` as a last resort

`fj-ex` is a community extension that fills some gaps such as detailed logs,
artifacts, cancel, rerun, and workflow dispatch by scraping the web UI.

Use it only as an optional fallback, not as a required dependency.

Important constraints:
- It is not part of the core required toolchain
- It may break when the Forgejo web UI changes
- Prefer official API endpoints whenever they exist

## Failure handling

- If `fj actions tasks` works but detailed logs are missing, explain the CLI limitation
- In current `forgejo-cli` source, the listing command is `fj actions tasks`
- If an Actions API endpoint returns `404`, the Forgejo version may not expose it, or the endpoint may only exist on newer unreleased source
- If a status endpoint returns no checks, confirm the repository actually uses Forgejo Actions or commit statuses
- If run details are ambiguous, report uncertainty instead of guessing
