## Description:

Monitor and summarize competitor clinical trial status changes from ClinicalTrials.gov.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and pharma competitive intelligence teams use this skill to search ClinicalTrials.gov, retrieve trial details, and summarize current trial status, recruitment, and recent updates for selected sponsors, conditions, statuses, or NCT IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies can change behavior across installs.

Mitigation: Pin and review Python dependencies before deploying the skill in a controlled or production environment.

Risk: The artifact provides current ClinicalTrials.gov lookup and summary behavior, but not durable snapshot comparison for complete status-change monitoring.

Mitigation: Use it for current trial lookups unless snapshot storage and comparison are added and validated.

## Reference(s):

- [ClinicalTrials.gov API v2](https://clinicaltrials.gov/api/v2)
- [ClinicalTrials.gov Data API documentation](https://clinicaltrials.gov/data-api/api)
- [API documentation](references/api-docs.md)
- [Usage examples](references/examples.md)
- [Clinical trial status codes](references/status-codes.md)
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/clinicaltrials-gov-parser)
- [Publisher profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; tool output may be JSON or terminal tables/text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ClinicalTrials.gov API v2 over HTTPS and may produce current lookup summaries rather than persisted change history.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
