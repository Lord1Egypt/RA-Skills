# Permission Manifest

## Network

Allowed outbound hosts:

- `api.github.com`
- `registry.npmjs.org`
- `docs.openclaw.ai`
- `clawhub.ai`

## Filesystem

Allowed writes:

- `data/YYYY-MM-DD/openclaw-ecosystem-snapshot.json`

No other filesystem writes are required.

## Secrets

No secrets are required for the default run.

Optional future GitHub token:

- only for higher REST API rate limits,
- read-only public metadata scope,
- never stored in output,
- never required for the default run.

## External Mutation

This skill does not:

- create GitHub issues or pull requests,
- create accounts,
- send emails,
- charge payments,
- alter remote data.
