## Description:

Search Douyin videos and public creator profiles, retrieve post details, comments and live trends, and help agents produce structured social media intelligence summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content, marketing, and research teams can use the skill to find public Douyin videos and creators, inspect posts and comments, and monitor trending topics. Agents can use the structured results to prepare trend, sentiment, demand, and content analysis summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flagged account discovery and identity-linked lead generation; scan coverage was partial and its benign verdict has medium confidence.

Mitigation: Use those capabilities only when they fit the request, and review the results in light of the stated limits of the security scan.

Risk: Search terms and supplied Douyin links or IDs are sent to the third-party GUAIKEI API.

Mitigation: Before querying, consider whether sharing the supplied terms or identifiers with GUAIKEI is appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-news-brief)
- [GUAIKEI service and token access](https://www.guaikei.com)
- [Output contract](references/contract.md)
- [Options and parameters](references/options.md)
- [Errors and retry guidance](references/errors.md)
- [FAQ and environment setup](references/faq.md)
- [Demand mining guidance](references/demand-mining.md)
- [Customer acquisition guidance](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown, Guidance]

**Output Format:** [Structured JSON results; agent-written summaries and analysis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include public video, creator, comment, and trend data; report detail depends on the query and available results.]

## Skill Version(s):

1.5.0 (source: server-resolved release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
