## Description:

Collects public Douyin posts, comments, engagement metrics, and trending topics, then supports content performance reviews and evidence-based next-step strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content teams, social media analysts, marketers, and customer support teams use the skill to review public Douyin content, track trends and competitors, understand audience feedback, and identify content opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, links, and IDs supplied to the skill are sent to the GUAIKEI third-party API.

Mitigation: Review the provider's terms and data handling, and submit only the identifiers needed for the requested analysis.

Risk: Account discovery and identifiable lead generation can expose personal information or enable unwanted contact.

Mitigation: Use results only for authorized internal analysis, minimize retained identifiers, and do not use them for unsolicited outreach or resale.

Risk: The security scan was benign with medium confidence, but several files were only partially analyzed.

Mitigation: Review the skill and its dependencies before deployment, and reassess if the skill or its permissions change.

## Reference(s):

- [Skill overview and command guide](artifact/readme.md)
- [Output contract](artifact/references/contract.md)
- [Command options](artifact/references/options.md)
- [Comment analysis and demand mining](artifact/references/demand-mining.md)
- [Public lead handling guidance](artifact/references/customer-acquisition.md)
- [Error handling](artifact/references/errors.md)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-performance-review)
- [GUAIKEI service and access](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data with concise analysis and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include content, author, engagement, comment, and trend fields; the agent should report relevant fields rather than paste full result payloads.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
