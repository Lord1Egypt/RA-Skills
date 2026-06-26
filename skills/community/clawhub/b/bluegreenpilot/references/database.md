# Database Policy

Use this reference when deploys involve migrations, seed data, production
snapshots, mock data, or empty homolog data.

## Homolog Data Modes

- `snapshot`: homolog is refreshed from a production snapshot.
- `mock`: homolog uses deterministic fake data.
- `empty`: homolog starts empty.
- `manual`: user manages data setup outside BlueGreenPilot.

## Production Safety

Before production deploy with database changes, require one of:

- confirmed snapshot;
- documented reversible migration;
- manual DBA approval;
- explicit user override.

If the migration is destructive or irreversible, stop and ask for a rollback
strategy. Blue-green traffic rollback does not automatically rollback database
state.

## Snapshot Plan

For snapshot mode, record:

- source database;
- snapshot command or provider;
- timestamp;
- destination environment;
- sanitization requirement;
- restore command;
- owner confirmation.

Never print credentials or database URLs containing secrets.

