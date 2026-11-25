## Description:

Read-only access to public Douyin data for keyword and user search, creator posts, post details, comments, and trending lists, returned as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

External content teams, marketers, and analysts use this skill to research topics, compare creator activity, track trends, assess public sentiment, and identify audience needs from public Douyin content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and Douyin links are sent to the third-party Guaikei API.

Mitigation: Avoid queries or links that contain sensitive information, and confirm the data being sent before running a request.

Risk: Retry behavior can make a request take a long time, and overlapping retries can duplicate requests.

Mitigation: Wait for the current command to finish before retrying or starting another request.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/guaikei/skills/douyin-search-api)
- [Guaikei API service](https://www.guaikei.com)
- [Output contract](references/contract.md)
- [FAQ and configuration](references/faq.md)
- [Demand mining guidance](references/demand-mining.md)
- [Customer acquisition guidance](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON data with optional concise Markdown analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Douyin content and engagement data; the API response may include an estimated cost.]

## Skill Version(s):

1.5.1 (source: server-resolved release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
