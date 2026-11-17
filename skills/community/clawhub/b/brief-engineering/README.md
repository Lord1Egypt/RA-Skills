# brief-engineering

Version **1.0.7**.

A technical daily brief for engineers. It answers one question each morning: what do I
need to do today, and in what order.

Not a notification dump. It pulls your sprint work, review queue and calendar alongside
service health, then writes the day as five ordered buckets: Start here, Your sprint,
Waiting on you, Your services, Plan for the day. Every item carries an owner, an evidence
link and a next step. The dashboard opens with a short story of the day and a
three-step action plan; source detail stays available without crowding the first screen.

## What you need

- A RovoClaw workspace.
- Delegated TWG access for Atlassian work and JSM Ops.
- Slack connected in Rovo when Slack evidence is wanted.
- Optional approved remote tools registered with RovoClaw for direct Splunk logs or
  SignalFx metric values.

No build step. No dependencies. No credentials in the skill.

## Install

Ask RovoClaw to install `@vmishra-atlassian/brief-engineering` from ClawHub into its
workspace. For an unpublished test build, import the `brief-engineering` folder into
the test workspace instead. Only files imported into the RovoClaw workspace affect the
cloud agent.

Then ask: `Run my engineering brief.`

After updating, rebuild and replace the published dashboard. Its runtime must display
the installed skill version and current connector-preflight timestamp; coverage rows
from a prior dashboard must not be carried forward.

## First run

The skill discovers your scope rather than being configured. It runs
`twg work query --scope me`, matches the repositories and projects that surface against
Compass components, filters to services your team owns, and asks you to confirm once.
The confirmed set is written to `memory/engineering-brief/scope.json`.

That is why the same folder gives a different brief to each person. There are no service
names anywhere in the skill.

**If a teammate's first brief shows services they do not own**, either scope confirmation
was skipped or a `scope.json` was copied across. Delete it and run again.

## What is in the box

| File | Purpose |
| --- | --- |
| `SKILL.md` | The playbook: scope discovery, collection, ranking, output shape |
| `references/signal-catalog.md` | Every connector, with verified working or blocked status |
| `references/connector-auth.md` | Slack, Splunk and SignalFx authentication and recovery |
| `references/signal-packs.md` | Team config contract for thresholds and critical workflows |
| `references/personas.md` | Engineer, EM and PM framing over the same evidence |
| `references/team-adoption.md` | Rollout order and failure modes |
| `references/install-for-teammates.md` | Per-person setup detail |

## Do not copy this

`memory/engineering-brief/` holds confirmed scope and findings. It is per-person. Send
the skill folder only.

## Optional: team signal pack

Without one you still get deploys, ownership, on-call gaps, alerts, incidents,
migrations and your own work context.

A signal pack adds team-specific context: service aliases, alert tags, SLO thresholds,
critical workflow names and cadence, and Slack channel allowlists. One JSON file,
registered once by a service owner, attaches automatically to anyone whose confirmed
scope matches. See `references/signal-packs.md`.

## Scheduling

Each person sets their own, in their own timezone. Weekday morning works well. On-call
engineers often prefer handoff time.

## Known gaps

Verified 2 September 2026:

- **Slack** works through delegated Rovo search. The skill discards results outside the
  team's explicit channel allowlist and excludes DMs.
- **SignalFx alerts** work through JSM Ops with `source = SignalFx`.
- **Splunk-originated alerts** work through JSM Ops with `source = Splunk`.
- **Direct Splunk logs and current SignalFx values** need approved remote tools
  registered for the RovoClaw principal. They are `not registered` without that grant;
  a discovered route that rejects a complete schema-valid request is reported as
  `failed` and requires its integration owner to repair the registered runtime.
- Where remote tools are not available, the optional creator-private operational relay
  lets a local collector publish only normalized findings to Confluence for RovoClaw to
  read. Tokens and raw responses remain local.
- **Forge app consumption** has no registered route in the checked catalogue.

The brief distinguishes `not registered`, `failed`, and `runtime unavailable` rather
than collapsing all connector problems into "not checked".
