## Description:

Verify claims, numbers, and facts in markdown drafts against local source data before publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and documentation authors use this skill to check markdown drafts for verifiable numeric claims, dates, model references, scores, and percentages before publication. It produces a report that highlights confirmed, unverifiable, and contradicted claims with suggested corrections when contradictions are found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read broad workspace evidence, including memory logs that may contain private or unrelated information.

Mitigation: Review the skill before installation and run it only in workspaces where those local evidence sources are appropriate for the draft being checked.

Risk: The skill automatically queries a localhost status API when available.

Mitigation: Use it when the local service is expected, and treat unavailable API data as a normal condition that shifts verification to local files.

Risk: Fact-check results can be incomplete when source files, score data, logs, or the local API are missing or stale.

Mitigation: Review unverifiable and contradicted claims manually before publishing, and confirm corrections against the underlying source data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nissan/skills/fact-checker)
- [Publisher Profile](https://clawhub.ai/user/nissan)
- [Control Plane status API](http://localhost:8765/status)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown verification report with per-claim statuses and a summary of confirmed, unverifiable, and contradicted claims.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print the report to stdout or write it to a markdown file when an output path is provided.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
