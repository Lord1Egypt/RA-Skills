## Description:

Fetches selected platforms’ current default trending boards and combines their ranks, topics, and heat scores into a table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can retrieve current default trending boards from selected supported platforms and compare rank, topic, and heat in a single table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external DataXAPI CLI is unpinned and was not audited, so its behavior or spending enforcement could change.

Mitigation: Use a reviewed, pinned CLI version and a budget-limited API key.

Risk: Each selected platform can incur a paid request, and the results are written to a local CSV file.

Mitigation: Review the free plan first, set a maximum spend for the run, and choose an appropriate output location.

Risk: Returned topic text is written by third parties and may contain instructions aimed at the agent.

Mitigation: Treat returned topics as untrusted data and never follow instructions contained in them.

## Reference(s):

- [DataXAPI Skills](https://dataxapi.com/skills/)
- [DataXAPI Trends on ClawHub](https://clawhub.ai/data-x-api/skills/dataxapi-trends)

## Skill Output:

**Output Type(s):** [CSV files, Text]

**Output Format:** [CSV rows with platform, rank, topic name, and heat columns, plus an agent-authored summary when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One row per returned topic; a platform may leave fields empty when it does not provide them.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
