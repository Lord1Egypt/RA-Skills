## Description:

Analyzes backlink and referring-domain evidence to produce a human-reviewed link-opportunity plan covering reclamation, competitor intersection, linkable assets, and unlinked mentions without automating outreach or disavow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustgrowth](https://clawhub.ai/user/trustgrowth)

### License/Terms of Use:

MIT-0

## Use Case:

SEO practitioners, site owners, and marketing teams use this skill to turn backlink exports or connected-provider observations into a prioritized, evidence-labeled opportunity plan. It is suited for identifying reclaimable links, competitor link gaps, citable asset opportunities, and unlinked mentions while keeping outreach and irreversible decisions under human control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires running an unbundled local validator script from the active skills root.

Mitigation: Install only when the broader Groundcrew skills root is trusted, and verify the groundcrew-doctor.py script before using its validation result.

Risk: The artifact references provider-selection.md and dataforseo.md safeguards that are not bundled with this release.

Mitigation: Confirm those safeguards are available before using paid providers or direct DataForSEO-backed backlink calls.

Risk: The skill may rely on billable or credential-backed SEO data providers.

Mitigation: Require explicit approval for paid or credential-backed calls, and avoid exposing API keys in prompts or output.

## Reference(s):

- [Connectors and categories](references/connectors.md)
- [Reporting contract](references/reporting.md)
- [ClawHub skill page](https://clawhub.ai/trustgrowth/skills/backlink-opportunities)

## Skill Output:

**Output Type(s):** [markdown, text, guidance]

**Output Format:** [Markdown plan with a prospect table, evidence references, lane labels, limitations, and not-measured notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include draft outreach angles, but not send-ready emails; outreach execution, paid-link decisions, and disavow actions remain human-controlled.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
