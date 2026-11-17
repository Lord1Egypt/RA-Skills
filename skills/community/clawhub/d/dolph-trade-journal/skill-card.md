## Description:

Auto-log trades with context, track outcomes, generate calibration reports to improve trading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richducat](https://clawhub.ai/user/richducat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to sync prediction-market trades, review recent history, update outcomes, export records, and generate daily, weekly, or monthly trading reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling is under-scoped for a trading API key.

Mitigation: Use a narrowly scoped read-only Simmer API key and avoid setting SIMMER_API_URL unless it points to a trusted HTTPS Simmer endpoint.

Risk: The artifact ships populated trade history that may be stale or sensitive.

Mitigation: Review, remove, or reset bundled data/trades.json before using the journal.

Risk: Dependency and API-origin controls need publisher review.

Mitigation: Remove the unused unpinned dependency and validate the API origin before sending credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richducat/skills/dolph-trade-journal)
- [Simmer API](https://api.simmer.markets)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [CLI text reports, JSON trade records, and optional CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY for API sync; stores local trade history under data/trades.json.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog; artifact frontmatter says 1.1.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
