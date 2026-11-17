## Description:

Publishes Markdown content to Medium, Dev.to, and Hashnode with formatting, SEO optimization, scheduling, and canonical URL support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qoohsuan](https://clawhub.ai/user/qoohsuan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare, optimize, and publish Markdown articles across Medium, Dev.to, and Hashnode while preserving canonical URLs for cross-posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send content to external services and may publish publicly without a built-in confirmation step.

Mitigation: Require the agent to show the exact title, body, tags, canonical URL, target account, platform, and draft-versus-live setting before any API call or browser publish action.

Risk: Cross-posting can create duplicate, incorrectly attributed, or poorly timed public content if canonical URLs, tags, or posting order are wrong.

Mitigation: Review the proposed cross-posting order, canonical URL, tags, and schedule before approving each platform submission.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qoohsuan/skills/ai-content-publisher)
- [Medium New Story](https://medium.com/new-story)
- [Dev.to Articles API](https://dev.to/api/articles)
- [Hashnode GraphQL API](https://gql.hashnode.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and API payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific publishing steps, credential environment variable names, SEO checks, and API request bodies.]

## Skill Version(s):

1.0.0 (source: clawhub.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
