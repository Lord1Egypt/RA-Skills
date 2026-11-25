## Description:

Read-only Douyin data lookup for finding creators, reviewing public posts and comments, and returning structured JSON for content and audience analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

External creators, marketers, and analysts can use this skill to find Douyin creators, compare public account and post metrics, review comments, and gather trend data for content planning and campaign research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports partial scanner coverage (32 of 54 components fully scanned) and calls out a question about disclosure when sharing links or IDs.

Mitigation: Review the link or ID before querying; requests send the selected keyword or link to guaikei.com, so use only public material appropriate to share with that service.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/guaikei/skills/dy-koc)
- [Guaikei Douyin data service](https://www.guaikei.com)
- [Skill usage and safety instructions](artifact/SKILL.md)
- [Output contract](artifact/references/contract.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [Structured JSON response envelope containing results as arrays or objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public Douyin data; result counts are subject to query and plan limits.]

## Skill Version(s):

1.5.1 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
