# Scenario Profiles v2.1

Use one profile at setup time, then customize paths/tags.

## Profile A — Solo Builder

- Domains: `company/main`, `operations`, `vendors`
- Typical flow: one project, one agent/user
- Recommended minimum docs:
  - `companies/main/COMPANY.md`
  - `operations/knowledge-mgmt.md`
  - `runbooks/incident-basics.md`

## Profile B — Agency / Multi-Client

- Domains: `companies/<client>/*`, shared `operations/*`, `vendors/*`
- Add privacy routing per client (never cross-post)
- Recommended minimum docs:
  - one `COMPANY.md` per client
  - shared `operations/slack-channels.md`
  - shared `operations/cron-registry.md`

## Profile C — Multi-Agent Ops Team

- Domains: company + project + role/agent routing
- Add explicit handoff + verification checkpoints
- Recommended minimum docs:
  - `operations/agent-ops.md`
  - `operations/testing-protocol.md`
  - `runbooks/agent-unreachable.md`

## Invariant Across All Profiles

1. No execution before source-of-truth read.
2. No "Done" without artifacts.
3. Any workflow change requires write-back in same action.
4. If docs are missing, create minimal doc first.
