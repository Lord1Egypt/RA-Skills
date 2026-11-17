# Authentication and profiles

Read this reference for authentication, actor selection, saved profiles, organization or project context, and environment conflicts.

## MCP profile selector behavior

`profile_ref` is an opaque connection-scoped selector, not a credential. Do not
persist it as global state, expose it as a secret, or silently switch actors.
If a call returns `profile_required`, discover profiles and ask when needed. If
it returns `invalid_profile`, discard the selector and rediscover. If it
returns `no_profiles_authorized`, explain that the user must authorize an
Atoll agent profile. If it returns `profile_selector_not_supported`, do not
retry as another actor; use a connection that supports per-call selection or
ask the user to resolve the connection limitation.

Resolve the organization and project from live accessible data. Exact project
names, slugs, and IDs are valid only when the current connection exposes them.
Do not infer a project from a similarly named workspace or carry project
context across conversations without rechecking it.

## How Atoll Works

Atoll connects strategy to execution through a reasoning chain:

```
Goals (directional objectives with deadlines)
  → KPIs (live metrics — manual, webhook, or API-fed)
    → Initiatives (bets expected to move specific KPIs)
      → Milestones + Issues (execution work)
```

This means an agent can reason: "We're off pace on paying_customers → the Content Pipeline initiative should drive signups but has stalled issues → unblocking those is the highest-leverage action right now."

Agents are organization members using the same API and authorization model as humans. Effective organization role and project scope still govern each action; agent identity does not bypass those checks.

## Authentication

All requests require: `Authorization: Bearer sk_atoll_<key>`

API keys are generated in **Agents** (for agents) or **Settings > Integrations > Create API Key** (for integrations). Each key is scoped to one org. Store both values as env vars:

```bash
export ATOLL_API_KEY="sk_atoll_..."
export ATOLL_ORG_ID="..."          # UUID of the org the key belongs to
```

For OpenClaw / ClawHub, prefer skill-scoped config in `~/.openclaw/openclaw.json` instead of global shell exports:

```json5
{
  skills: {
    entries: {
      "atoll": {
        enabled: true,
        apiKey: "sk_atoll_...",
        env: {
          ATOLL_ORG_ID: "..."
        }
      }
    }
  }
}
```

`apiKey` maps to `ATOLL_API_KEY` because the ClawHub `atoll` skill (1.0.7 and later) declares it as the OpenClaw primary env; optional defaults such as `ATOLL_PROJECT`, `ATOLL_TEAM`, and `ATOLL_BASE_URL` belong under `env`. Older installs (`atoll` 1.0.6 or legacy `atoll-api` 1.0.22 and earlier) declare no primary env, so OpenClaw ignores `apiKey` and blocks `ATOLL_API_KEY` under `env`; run `openclaw skills update atoll` (or `atoll-api`). `openclaw skills info atoll` lists `Primary env: ATOLL_API_KEY` for an updated skill; verify the credentials with the sanity check below.

**Sanity check** — exercises the org-scoped issues endpoint, not just `/api/auth/me`:

```bash
: "${ATOLL_API_KEY:?missing}" "${ATOLL_ORG_ID:?missing}" && \
  curl -sS -o /dev/null -w "HTTP:%{http_code}\n" \
    "https://atollhq.com/api/orgs/$ATOLL_ORG_ID/issues?limit=1" \
    -H "Authorization: Bearer $ATOLL_API_KEY"
# Expect: HTTP:200
```

If `$ATOLL_ORG_ID` is empty, the URL collapses to `/api/orgs//issues` which 308-redirects to a non-existent route and returns `Unauthorized` — a misleading symptom that looks like an auth failure. `GET /api/auth/me` alone cannot catch this since it doesn't depend on `$ATOLL_ORG_ID`. Always guard both vars.

For agent diagnostics, `/api/auth/me` reports the organization role in `auth.role` and live per-project `view`/`edit`/`admin` grants in `auth.projectAccess[]`. Project-scoped agents intentionally remain org guests. Organization-role and project-access changes are read live and do not require key rotation; `scopes: []` is normal for a standard agent key.

Human project administrators can read the bounded workforce projection at `GET /api/orgs/{id}/agents/workforce?projectId=...` only for projects where their effective access is `admin`. Organization owners/admins may request the full inventory or a project filter; individual owners retain their own-agent read path. The response is read-only, separates `can_view` from existing management capabilities, and omits credentials, auth IDs, emails, hidden projects, private content, and lifecycle fields. Unauthorized project filters are concealed as `404`; use `limit` 1-100 and `offset` for pagination.

## Saved CLI profiles and environment selection

For machines or agents that need multiple credentials, use auth profiles:

```bash
atoll auth login --profile agent-a --key sk_atoll_... --org-id org-uuid
atoll auth login --profile agent-b --key sk_atoll_... --org-id org-uuid --project project-id --team team-id
atoll auth profiles
atoll auth use agent-a

# Run one command as a specific profile
atoll --profile agent-b issue list
```

Profiles can store default org ID, project, team, and base URL values. For named profiles, always persist `--org-id` or pass `--org-id` per command. Resource commands fail when the selected profile has no org ID so agents do not accidentally operate with the wrong scope.

Env vars remain supported for CI, containers, and one-off runtime usage, but persistent developer/agent machines should prefer profiles. When a profile is selected, ambient `ATOLL_*` env vars do not silently override profile context; conflicting env values fail before network calls. Pass `--profile`, use repo-local `.atoll/context.json`, or opt into env mode with `--env-mode` / `ATOLL_ENV_MODE=1`.

Repo-local `baseUrl` values cannot reuse a saved profile key unless that same base URL is stored in the profile. Set `ATOLL_TRUST_REPO_BASE_URL=1` only for a single process after verifying both the repository and destination host.

### Agent lifecycle boundary

Agent rows add `lifecycle_state` and `lifecycle_version`; lease rows add immutable `agent_lifecycle_version`. Only enabled agents can authenticate, receive new assignments, mint keys, change access/policy, or use runner authority. Disable preserves history and capacity; revoke retains identity but releases capacity and is terminal. Enable requires fresh credentials/consent and never resumes work automatically. Human-only management uses `POST /api/orgs/{id}/agents/{agentId}/lifecycle` with action, expected_version, and idempotency_key. CLI/MCP callers cannot use it. Authorized workforce `capabilities` report the available transitions and management controls; historical visibility does not grant effective access. See API endpoints for replay and conflict behavior.
