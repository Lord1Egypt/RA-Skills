## Description:

Research US B2B accounts from public business sources, score and deduplicate prospects, and prepare personalized outreach drafts for human review and manual sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US B2B sales and research teams use this agent to define an ideal customer profile, research and prioritize accounts from public or properly licensed sources, and prepare sourced dossiers, prospect sheets, compliance reports, and personalized outreach drafts. A human reviews the research and drafts and sends any outreach manually.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Public business information or personalization details may be outdated or inaccurate.

Mitigation: Record a source URL and research date for each claim, then have a human verify facts and drafts before use.

Risk: Outreach can violate applicable requirements or fail to honor an opt-out.

Mitigation: Use the compliance checker as a lint aid, review messages manually, maintain and check a suppression list, honor opt-outs, and do not automate sending.

Risk: Optional research-provider credentials could be exposed.

Mitigation: Protect provider API keys and use provider data only under its applicable license.

## Reference(s):

- [US B2B research playbook](artifact/references/research-playbook.md)
- [US company data sources](artifact/references/enrichment-sources.md)
- [US compliance guidance](artifact/references/us-compliance.md)
- [Publisher homepage](https://github.com/rapidworker1)

## Skill Output:

**Output Type(s):** [Analysis, CSV, JSON, Markdown, Guidance]

**Output Format:** [Scored prospect sheets, account dossiers, outreach drafts, and compliance reports in CSV, JSON, and Markdown formats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research facts are source-attributed and dated; outreach is drafted for human review and is not sent automatically.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
