## Description:

Auto-discover and import Polymarket markets matching configured keywords, categories, and volume criteria, running on a schedule so new matching markets can be imported into Simmer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richducat](https://clawhub.ai/user/richducat)

### License/Terms of Use:

MIT-0

## Use Case:

External Simmer users use this skill to discover Polymarket markets that match their configured search terms, category filters, and liquidity threshold. It previews candidates by default and can import matches into the user's Simmer account when live mode is explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can make changes to a user's Simmer account by importing markets with the configured API key.

Mitigation: Run the default dry run first, enable live mode only after reviewing candidates, and use a scoped API key where available.

Risk: A scheduled live configuration can consume import quota or import more markets than intended.

Mitigation: Keep max_per_run conservative, confirm whether cron scheduling is enabled for live execution, and tune keywords, categories, and minimum volume before scheduled runs.

Risk: The skill depends on simmer-sdk and the SIMMER_API_KEY credential.

Mitigation: Install a pinned or reviewed simmer-sdk version and protect the SIMMER_API_KEY environment variable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richducat/skills/dolph-market-importer)
- [Simmer dashboard](https://simmer.markets/dashboard)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls, files]

**Output Format:** [Console text with optional automaton JSON and local JSON state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry run is the default; live mode imports up to max_per_run and persists imported market IDs for deduplication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
