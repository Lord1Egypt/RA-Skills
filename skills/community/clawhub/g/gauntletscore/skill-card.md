## Description:

Trust verification for AI output - verify any document or code before you act on it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wmehobbs](https://clawhub.ai/user/wmehobbs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and organizations use GauntletScore to submit AI-generated documents, code, or ClawHub skill URLs to its cloud API for trust scoring, claim verification, code safety analysis, and certificate verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents, code, and URLs selected for analysis are sent to GauntletScore's cloud API.

Mitigation: Do not submit secrets, private repositories, internal URLs, regulated data, or client material unless approved and vendor privacy and retention terms have been reviewed.

Risk: The skill depends on an external API key and cloud service availability.

Mitigation: Configure GAUNTLET_API_KEY only in approved secret storage and plan for failure handling when the API is unavailable.

Risk: Verification scores and agent debate outputs can still be wrong or incomplete.

Mitigation: Treat results as review support and require human approval before relying on findings for legal, regulatory, security, or production decisions.

## Reference(s):

- [GauntletScore ClawHub Skill](https://clawhub.ai/wmehobbs/skills/gauntletscore)
- [GauntletScore](https://gauntletscore.com)
- [GauntletScore API Documentation](https://gauntletscore.com/docs)
- [GauntletScore Analyze API](https://api.gauntletscore.com/v1/analyze)
- [GauntletScore Certificate Verification API](https://api.gauntletscore.com/v1/verify/{certificate_id})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP request examples and JSON API payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GAUNTLET_API_KEY; submits chosen documents, code, or URLs to GauntletScore's cloud API; analysis is described as read-only.]

## Skill Version(s):

5.1.5 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
