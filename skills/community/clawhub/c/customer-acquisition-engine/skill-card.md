## Description:

Searches public Douyin videos, creators, comments, and trending lists to support content research, audience analysis, and lead discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Marketing, content, and sales teams use this skill to research public Douyin content, analyze comments and audience needs, track competitors and trends, and identify potential leads. It returns data for internal analysis and does not contact users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Douyin links are sent to GuaiKei when the service is called.

Mitigation: Tell the user before sending inputs and get confirmation; submit only the keyword or public link needed for the requested analysis.

Risk: The security summary flags detail retrieval as outside the declared capability summary and says inspection of some components was incomplete.

Mitigation: Limit detail lookups to posts the user asks about, and review the incompletely inspected components before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/engheng-art/skills/customer-acquisition-engine)
- [GuaiKei service and support](https://www.guaikei.com)
- [Public customer acquisition guide](references/customer-acquisition.md)
- [Comment demand analysis guide](references/demand-mining.md)
- [JSON output contract](references/contract.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown tables, Shell commands]

**Output Format:** [Structured JSON from CLI commands, with concise Markdown summaries or tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include public content and engagement fields; some commands save JSON results in the skill's logs directory.]

## Skill Version(s):

1.5.0 (source: artifact/SKILL.md frontmatter, artifact/package.json, evidence.json release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
