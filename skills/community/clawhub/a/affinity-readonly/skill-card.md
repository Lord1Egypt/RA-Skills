## Description:

Read-only Affinity CRM access for analysis and memo preparation that fetches companies, people, notes, opportunities, interactions, or relationship data via API for summarized analysis without writes or API-key exposure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howdymarc](https://clawhub.ai/user/howdymarc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to retrieve Affinity CRM records for analysis-only workflows, including company, person, note, opportunity, interaction, and relationship summaries. It is intended for read-only memo preparation and evidence gathering without modifying CRM data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Affinity API key can be sent to an unintended host if AFFINITY_API_BASE is changed.

Mitigation: Use a read-only, least-privileged Affinity token; avoid setting AFFINITY_API_BASE except in controlled testing; prefer a trusted fixed API host or explicit allowlist; rotate the token if the base URL may have been manipulated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howdymarc/skills/affinity-readonly)
- [Affinity API base URL](https://api.affinity.co)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with optional JSON API responses and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Affinity API access; requires AFFINITY_API_KEY in the local environment.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence, released 2026-03-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
