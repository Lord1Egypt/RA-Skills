# Sharing this with a teammate

Install the skill in each teammate's RovoClaw workspace. The skill contains no
credentials, service names, thresholds or personal memory. Those are discovered per
person or supplied by a team signal pack.

## What to send

The folder `skills/brief-engineering/`. Six markdown files:

```
brief-engineering/
├── SKILL.md
└── references/
    ├── signal-catalog.md      which tools exist and which work
    ├── connector-auth.md      Slack, Splunk and SignalFx authentication
    ├── signal-packs.md        team config contract
    ├── personas.md            engineer / EM / PM framing
    ├── team-adoption.md       rollout guidance
    └── install-for-teammates.md
```

Publish an approved build to ClawHub or import the folder into a test RovoClaw
workspace. Do not copy another user's `memory/engineering-brief/` folder.

Do **not** send `memory/engineering-brief/`. That folder holds your confirmed scope and
your findings. Your teammate's brief must discover their own.

## Where it goes

The skill must exist in the RovoClaw workspace's `skills` area. Ask RovoClaw to install
the ClawHub package, or use the workspace import path for a private test build. A local
copy does not change the cloud workspace.

## First run

Your teammate asks for an engineering brief. The skill then:

1. Runs `twg work query --scope me --since 14d` under **their** auth, returning their
   issues, pages and commits — not yours.
2. Takes the repository and project names that appear, and queries Compass with
   `queryString` to find services whose names match.
3. Keeps components where `typeId` is `SERVICE` and the owning team matches theirs.
4. Reads the `platform`, `owner` and `business-unit` custom fields to learn how each
   service is registered.
5. Shows the candidate list and asks for confirmation.
6. Stores the confirmed set at `memory/engineering-brief/scope.json`.

Only step 5 needs the human. Everything else is derived.

## Why the same skill gives a different brief

The skill contains **no service names anywhere**. Everything flows from one file the
brief writes on first run: `memory/engineering-brief/scope.json`.

| Input | Where it comes from |
| --- | --- |
| Services | Compass components owned by their team |
| Service owners | Compass `owner` custom field, stored in scope.json |
| Deploy state | Spinnaker, per confirmed service name |
| Ownership and on-call | Compass, per confirmed component |
| Alerts | Reliability Insights SQL, matched on their service names |
| Work context | `twg --scope me` under their token |
| Alert tags and thresholds | Their team's signal pack, if one exists |
| Persona framing | Their role, recorded in scope.json |

A payments engineer installing this same folder gets payments deploy state and payments
ownership gaps. Nothing from another team appears, because no other team's name is
written into the skill.

**This is worth verifying rather than trusting.** If a teammate's first brief mentions
services they do not own, either `scope.json` was copied from another workspace or
scope confirmation was skipped. Delete the file and ask for a brief again.

A related failure to watch for: a scheduled job whose prompt names services directly.
That silently overrides discovery and pins everyone to one team's view. The schedule
should say "read scope.json", never "brief me on service-a, service-b".

## What they get with no signal pack

Working immediately with delegated TWG access:

- Spinnaker deploy state and prod-versus-staging drift per service
- Compass ownership, on-call coverage, dependencies and platform registration
- Active TPS migrations affecting their services
- SignalFx and Splunk-originated JSM Ops alerts
- Their Atlassian work context and direct notifications

Missing until a pack is registered: service-specific alert matching, workflow cadence
checks and Slack channel evidence. Direct DLQ depth and latency values also need a
registered operational tool. The brief reports these as `not configured` or `not
checked` rather than implying health.

## Adding a signal pack

One JSON file per team, written once by a service owner, at
`memory/engineering-brief/signal-packs/<packId>.json`. Shape and matching rules are in
`signal-packs.md`.

It attaches automatically to any teammate whose confirmed scope matches on exact
service, project, repository or team. Fuzzy matching is deliberately not supported —
that is what stops one team's operational config leaking into another team's brief.

## Scheduling

Each person sets their own, in their own timezone:

```
cron add: weekday 08:30 local, isolated agentTurn,
          message "Run the brief-engineering skill", delivery announce
```

On-call engineers often prefer handoff time instead of morning.

## Verify the install worked

Ask for a brief and check three things:

- The service list is **theirs**, not yours. If IDP services appear for a payments
  engineer, scope confirmation was skipped or another user's `scope.json` was copied.
- The coverage table names every source with a status. A brief with no coverage table
  is not trustworthy.
- Failing connectors say `not checked`, never `healthy`.

## Known limits at install time

Verified on this environment; re-check on theirs, since these are platform-wide rather
than per-user:

- `npx @atlassian/skills add ...` needs public egress to `statlas.prod.atl-paas.net`
  and npm. Where that is blocked, the skill calls the underlying `is` tools directly.
- SignalFx and Splunk-originated alerts are read through JSM Ops source filters.
- Direct Splunk logs and current SignalFx values need approved remote tools registered
  for the RovoClaw principal; the skill cannot grant this access.
- A local Ops Sherpa setup can use Splunk SLAuth and a SignalFx token from Keychain,
  but those laptop credentials are not available to RovoClaw Cloud. The optional
  creator-private Confluence relay carries normalized findings across that boundary
  without copying credentials. See `local-operational-relay.md`.
- Slack is read through delegated Rovo search only for channels explicitly registered
  in the user's signal pack. DMs are excluded.
- No Forge consumption tool exists anywhere in the catalogue.

A teammate installing today gets the work, ownership, deploy, workflow and alert brief.
Direct live metrics show an explicit coverage gap until the workspace has an approved
operational connector.
