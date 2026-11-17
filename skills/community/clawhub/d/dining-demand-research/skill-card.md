## Description:

Research public Resy and OpenTable restaurant profiles and time-specific availability to build dated dining shortlists and comparisons without booking or ordering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Diners and dining researchers use this skill to compare restaurant profiles, prices, and observed reservation availability for a specified location, local time, and party size. It also distinguishes ticketed dining events from ordinary reservations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dining search details, including location, time, party size, and restaurant identifiers, are sent to Crawlora using an API key.

Mitigation: Use the skill only if sharing those search details and using a Crawlora API key is acceptable.

Risk: Displayed availability is a temporary snapshot and may change before a diner books.

Mitigation: Show retrieval times and avoid presenting observed slots as held or confirmed reservations.

## Reference(s):

- [Dining demand research on ClawHub](https://clawhub.ai/crawlora-org/skills/dining-demand-research)
- [Crawlora dining endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown comparison and dated shortlist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes provider and venue identifiers, local dining time and party size, observed availability, source links, and retrieval timestamps; does not make reservations.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
