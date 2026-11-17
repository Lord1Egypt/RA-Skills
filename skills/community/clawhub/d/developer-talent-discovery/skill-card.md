## Description:

Find developers through Crawlora public GitHub user datasets and verify relevant repository and contribution evidence for role-specific shortlists or open-source collaborator discovery, without outreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, hiring teams, and open-source project leads use the skill to find developers and build role-specific shortlists grounded in public GitHub repositories and contribution evidence. The skill does not contact candidates or make hiring decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public profile or contact data may be mistaken for consent to recruiting outreach or a reliable hiring decision.

Mitigation: Use public contact fields only as evidence leads, do not initiate outreach without an explicit request, and review fit through a conversation or work assessment.

Risk: Stored activity, availability, and location indicators may be stale or incomplete.

Mitigation: Keep searches bounded, preserve crawl and retrieval times, and label profile-derived claims and unknowns rather than treating them as verified facts.

Risk: Using the Crawlora service requires an API key and processes public GitHub profile data.

Mitigation: Install only if comfortable using Crawlora and handling its API key; keep queries limited to the requested scope.

## Reference(s):

- [Crawlora endpoint reference](reference/endpoints.md)
- [Developer Talent Discovery release](https://clawhub.ai/crawlora-org/skills/developer-talent-discovery)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown shortlist with profile and repository links, dated work evidence, and unresolved fit questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public GitHub evidence only; distinguishes observed work from unverified fit and preserves source and retrieval dates.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
