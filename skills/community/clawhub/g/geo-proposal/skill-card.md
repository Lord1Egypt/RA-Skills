## Description:

Auto-generate a professional, client-ready GEO service proposal from audit data, including executive summary, findings, service packages, pricing, timeline, and terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External consultants, agencies, and sales teams use this skill to turn GEO audit data into client-ready service proposals with package recommendations, pricing, timelines, and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated proposals may include inaccurate audit summaries, ROI projections, pricing recommendations, or client-facing claims.

Mitigation: Review the generated proposal against the underlying audit data before sending it to a client.

Risk: The skill can save proposal files and update matching local prospect records.

Mitigation: Review generated files and any prospect status changes under ~/.geo-prospects before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/geo-proposal)

## Skill Output:

**Output Type(s):** [Text, Markdown, PDF, Files, Guidance]

**Output Format:** [Markdown proposal file, optional PDF follow-up, and confirmation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves proposals under ~/.geo-prospects/proposals and may update matching prospect records under ~/.geo-prospects/prospects.json.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
