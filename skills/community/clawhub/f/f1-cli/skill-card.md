## Description:

Query Formula 1 data using the f1-cli command-line tool, which wraps the OpenF1 API for race results, lap times, standings, pit stops, telemetry, weather, team radio, overtakes, tire strategy, and other F1 statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barronlroth](https://clawhub.ai/user/barronlroth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and F1 analysts use this skill to have an agent retrieve and interpret Formula 1 session, timing, telemetry, standings, weather, race-control, and strategy data through the f1 CLI and OpenF1.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and using a third-party CLI can introduce supply-chain risk.

Mitigation: Install only from a reviewed or pinned f1-cli release or Homebrew formula revision.

Risk: The skill may make network requests to OpenF1 for public Formula 1 data, including for broad F1-related prompts.

Mitigation: Enable it only in environments where outbound OpenF1 access is acceptable.

Risk: High-frequency telemetry and location queries can fetch large result sets before local limiting is applied.

Mitigation: Prefer server-side filters and narrow session or driver selections for large telemetry-style queries.

## Reference(s):

- [OpenF1 API](https://openf1.org)
- [ClawHub Skill Page](https://clawhub.ai/barronlroth/skills/f1-cli)
- [Publisher Profile](https://clawhub.ai/user/barronlroth)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and references to table, JSON, or CSV CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend f1 CLI commands that query OpenF1; JSON and CSV output modes are available through CLI flags.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
