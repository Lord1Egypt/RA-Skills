## Description:

Search, compare, and book accommodation across platforms with real pricing, user preferences, and end-to-end execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Travelers and travel-planning agents use this skill to compare accommodations across booking platforms, calculate true total costs, shortlist options, and proceed with booking when explicitly asked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can proceed toward real booking execution, which may create travel commitments or charges without adequate confirmation.

Mitigation: Require an explicit final booking confirmation screen before any booking is completed.

Risk: Persistent booking memory can contain sensitive travel details, payment-related information, identity documents, precise future itinerary details, or credentials.

Mitigation: Make stored travel data opt-in, owner-only, reviewable, and deletable; do not store payment details, identity documents, precise future itinerary details, or credentials.

## Reference(s):

- [ClawHub Booking skill page](https://clawhub.ai/ivangdavila/skills/booking)
- [Search & Compare](artifact/search.md)
- [Platforms & Data Sources](artifact/platforms.md)
- [Pricing & Total Cost](artifact/pricing.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown recommendations with comparison tables and concise booking guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curated shortlists, total-cost breakdowns, cancellation policy notes, location context, review-pattern summaries, and final booking confirmation prompts.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
