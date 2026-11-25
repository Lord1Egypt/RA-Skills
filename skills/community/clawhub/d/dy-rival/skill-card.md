## Description:

A read-only Douyin data source for keyword and user searches, creator posts, video details, comments, and hot lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

Content and marketing teams can use the skill to monitor public Douyin competitor accounts, compare posts and engagement, track hot topics, and review comments. It returns structured data for further analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send supplied public links or IDs to a third-party API.

Mitigation: Review the destination and submit only public links or IDs you intend to query.

Risk: The security scan was partial and notes a possible retry-handling mismatch.

Mitigation: Wait for a request to finish and check its status before retrying; avoid duplicate concurrent requests.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/guaikei/skills/dy-rival)
- [Guaikei API service](https://www.guaikei.com)
- [Output contract](references/contract.md)
- [Command options](references/options.md)
- [Comment demand analysis guide](references/demand-mining.md)

## Skill Output:

**Output Type(s):** [JSON, API data]

**Output Format:** [Structured JSON envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data; result limits depend on the API plan.]

## Skill Version(s):

1.5.1 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
