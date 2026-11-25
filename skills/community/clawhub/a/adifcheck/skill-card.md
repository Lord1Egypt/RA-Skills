## Description:

Check a ham-radio ADIF log's contents — the values LoTW and eQSL actually reject — before upload. Use when asked to validate an .adi or .adx log, find why QSOs were rejected by LoTW or eQSL, or check a log before uploading — for example "check my log before I upload to LoTW", "why did eQSL reject these QSOs", or "validate this ADIF file". Checks modes, submodes and their pairings, band versus frequency, dates and times, satellite fields and state/county codes against the ADIF 3.1.8 specification's own tables, plus the documented LoTW and eQSL acceptance rules. Not for Darwin Core / GBIF occurrence files (that is dwccheck) or iCalendar (.ics) files (that is icslint).

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Ham-radio operators and log maintainers use it to find ADIF content issues and documented LoTW or eQSL acceptance problems before uploading logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command uses an unpinned Git repository, creating a supply-chain risk.

Mitigation: Install from a reviewed fixed commit or verified wheel, using a disposable environment with least privilege.

## Reference(s):

- [ADIF Check on ClawHub](https://clawhub.ai/raktikoo/skills/adifcheck)
- [Publisher profile: raktikoo](https://clawhub.ai/user/raktikoo)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Human-readable validation findings or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports record and field details, severity, rule sources, and an exit code; reads supplied logs without uploading or changing them.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
