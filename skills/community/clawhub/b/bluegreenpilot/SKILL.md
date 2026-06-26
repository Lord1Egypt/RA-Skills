---
name: bluegreenpilot
description: "Guide safe blue-green deployments with persistent repo config, environment state, health checks, explicit switch confirmation, and rollback discipline."
version: 2026.6.4
homepage: https://github.com/ThiagoCAltoe/bluegreenpilot
metadata: {"openclaw":{}}
---

# BlueGreenPilot

Use this skill when the user wants to configure, plan, verify, deploy, promote,
switch traffic, or roll back a blue-green deployment flow.

BlueGreenPilot is a deployment safety protocol. It must help the user operate
their real environment without relying on chat memory or guessing.

## Hard Rules

- Never switch production traffic without explicit final confirmation.
- Never deploy to the active production slot unless the user explicitly says
  they are not using blue-green for that environment.
- Never store secrets in `.bluegreenpilot/config.yaml`.
- Never assume the active slot. Read state, query the environment, or ask.
- Never assume a project is greenfield. If `.bluegreenpilot` is missing and the
  user mentions production, first ask whether production already exists.
- Never treat an environment as a blue-green slot. `dev`, `homolog`, `staging`,
  and `prod` are environments; `blue` and `green` are slots inside one
  environment.
- Never say `homolog` is `green` or `prod` is `blue` unless config explicitly
  models that nonstandard topology and the user confirms the risk.
- If a project has `homolog` and `prod`, treat it as a candidate for mapping,
  not as proof that blue-green is already implemented.
- Stop if the state backend is unknown or unreadable.
- Stop if brownfield adoption says the inactive production slot is not
  provisioned.
- Stop if rollback is unknown for production.
- Stop if database changes are involved and snapshot/migration policy is unknown.
- Prefer read-only discovery before any write/deploy action.
- Treat `homolog` as production-like for safety checks and data policy, but not
  as a production traffic slot unless config explicitly says so.
- Always produce a plan before running deployment commands.
- Record what changed after every switch or rollback.

## Environment vs Slot Model

Keep environments and slots separate.

- Environments are deployment stages such as `dev`, `homolog`, `staging`, and
  `prod`.
- Slots are parallel runtime targets inside one environment, such as `blue` and
  `green`.

Correct model:

```txt
homolog
  single-slot, or homolog-blue/homolog-green if explicitly configured

prod
  blue: active production slot
  green: inactive production candidate slot
```

Incorrect model:

```txt
homolog = green
prod = blue
```

If the user says an app has homolog and prod, say it is a good candidate for
BlueGreenPilot mapping. Do not claim blue-green exists yet. First discover
whether production can run two equivalent slots and switch traffic between them.

## Files

Use these files in the target application repository:

```txt
.bluegreenpilot/config.yaml
.bluegreenpilot/state.dev.yaml
.bluegreenpilot/state.homolog.yaml
.bluegreenpilot/state.prod.yaml
.bluegreenpilot/history/
```

`config.yaml` is versioned and contains topology/workflow only. Environment
state may be versioned for simple projects, but production state is usually
stored in CI artifacts, the server, object storage, or another trusted backend.
Secrets belong in `.env`, CI secrets, server env vars, Vault, Doppler, 1Password,
or equivalent secret storage.

The `state.backend` config field tells the agent where state persists across
developer machines, homolog, CI, and production. If the backend is not readable,
stop and ask how to retrieve state before planning a deploy.

## Standard Workflow

1. Identify the requested operation: init, status, plan, deploy, verify, switch,
   promote, rollback, or audit.
2. Read `.bluegreenpilot/config.yaml`. If missing, run init workflow.
3. Determine target environment: dev, homolog, prod, or custom.
4. Read state for that environment. If missing or stale, ask how to retrieve or
   initialize it.
5. Confirm active and inactive slots for blue-green environments.
6. Check deploy mode: no-docker, docker, mixed, CI, script, manual.
7. Check database policy: snapshot, mock, empty, manual, or none.
8. Generate a concise plan with commands, checks, switch method, rollback path,
   and unknowns.
9. Ask before executing state-changing actions.
10. After execution, record result, commit/release id, active slot, checks, and
    rollback metadata.

## Init Workflow

Ask only for missing facts:

- App name.
- Whether production already exists today.
- Branch model: single branch, dev/homolog/prod, or custom.
- Environments: dev, homolog, prod, custom.
- For each environment: deploy mode, blue-green or single-slot, URLs.
- Docker usage: none, all environments, homolog only, prod only, or mixed.
- Switch method: manual, script, nginx, Cloudflare, load balancer, CI, other.
- Rollback method.
- Healthcheck path and smoke commands.
- Database type and whether deploys include migrations.
- Homolog data mode: production snapshot, mock data, empty database, manual.
- Where state should be stored.

Create `.bluegreenpilot/config.yaml` and example state files. Do not ask for
secrets. If a command needs a secret, reference an env var name instead.

## Existing Production / Brownfield Adoption

If the app is already live, do not start by proposing a blue-green switch.
Adopt current production first:

1. Ask for the current production URL, deploy mode, current release/source, and
   whether the current live service should be labeled `blue` or `green`.
2. Treat the current live service as the stable active slot.
3. Mark the opposite production slot as `not-provisioned` until the user creates
   an equivalent secondary production slot. A homolog/staging environment does
   not count as the inactive production slot unless the user deliberately
   defines that topology and accepts the risk.
4. Record `adoption.mode: brownfield` and `inactive_slot_status:
   not-provisioned`.
5. Block deploy/switch plans until the inactive slot is provisioned and verified.

If the CLI is available, use:

```bash
bluegreenpilot --project /path/to/app adopt-prod \
  --app <name> \
  --public-url <current-prod-url> \
  --deploy-mode <docker|script|manual|ci|mixed|no-docker> \
  --active-slot <blue|green> \
  --source <current-release-or-commit> \
  --state-backend <repo|server-file|ci-artifact|object-storage|manual>
```

## Deploy Plan Shape

Always show:

```txt
Target: <environment>
Current active slot: <slot or unknown>
Deploy target: <inactive slot>
Source: <branch/tag/commit>
Database policy: <snapshot/mock/empty/manual/none>
Pre-flight checks:
  - ...
Deploy steps:
  - ...
Verification:
  - ...
Switch:
  - method
  - requires final confirmation: yes/no
Rollback:
  - ...
Unknowns / blockers:
  - ...
```

## Production Switch Gate

Before switching production, ask a direct confirmation that includes:

- target environment;
- current active slot;
- proposed new active slot;
- release/commit;
- healthcheck result;
- rollback command or procedure.

Do not proceed from vague approval. The user must clearly approve the switch.

## Rollback Workflow

For rollback:

1. Read current state.
2. Identify last known stable slot/release.
3. Check whether rollback affects database state.
4. Generate rollback plan.
5. Ask for confirmation.
6. Switch back or run rollback command.
7. Verify public URL.
8. Record rollback reason and result.

## Variant References

Read only the relevant reference:

- Docker and mixed Docker deployments: `references/docker.md`
- No-Docker/manual/script deployments: `references/no-docker.md`
- Database snapshot/mock/empty policy: `references/database.md`
- Config/state model and examples: `references/configuration.md`

## Helper Script

If available, use:

```bash
bluegreenpilot init
bluegreenpilot --project /path/to/app validate --env prod
bluegreenpilot --project /path/to/app status prod
bluegreenpilot --project /path/to/app plan prod --source <branch-or-commit>
```

If only the skill bundle is installed, use the bundled helper:

```bash
python {baseDir}/scripts/bluegreenpilot.py init
python {baseDir}/scripts/bluegreenpilot.py adopt-prod --app <name> --public-url <current-prod-url>
python {baseDir}/scripts/bluegreenpilot.py status --env prod
python {baseDir}/scripts/bluegreenpilot.py plan --env prod
```

The helper is conservative. It creates templates and reports missing facts; it
does not switch traffic or run destructive deployment commands.
