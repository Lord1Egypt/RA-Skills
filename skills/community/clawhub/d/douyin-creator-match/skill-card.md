## Description:

Find and assess Douyin creator candidates using public account, video, post, comment, and trending data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, creator-partnership, and content teams can use the skill to find Douyin accounts and public content relevant to a niche, then compare creator, post, engagement, comment, and trend data to prioritize candidates or inform content research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports medium confidence and partial inspection, and notes expanded customer-prospecting workflows.

Mitigation: Review the prospecting workflows and related guidance before use, and confirm that collection and outreach fit your policies.

Risk: Search terms and content links are sent to the third-party service identified in the skill documentation.

Mitigation: Avoid submitting sensitive queries or links, and make the data transfer clear to users where appropriate.

## Reference(s):

- [Command routing](artifact/references/routing.md)
- [Command options](artifact/references/options.md)
- [Output contract](artifact/references/contract.md)
- [Error handling](artifact/references/errors.md)
- [Demand mining guidance](artifact/references/demand-mining.md)
- [Customer acquisition guidance](artifact/references/customer-acquisition.md)
- [Guaikei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Analysis]

**Output Format:** [Structured JSON data with concise text summaries or tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Douyin data; results may be empty and should be reported as returned. A configured GUAIKEI_API_TOKEN is required for data requests.]

## Skill Version(s):

1.5.0 (source: artifact/SKILL.md frontmatter, artifact/package.json, artifact/references/changelog.md entry dated 2026-11-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
