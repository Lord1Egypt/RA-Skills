## Description:

Publish markdown articles to Medium, Dev.to, and Hashnode with formatting, SEO optimization, scheduling, cross-posting, and canonical URL guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qoohsuan](https://clawhub.ai/user/qoohsuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and content publishers use this skill to prepare markdown articles, optimize them for SEO, and publish or cross-post them across Medium, Dev.to, and Hashnode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing actions can make draft article content public on external blogging platforms.

Mitigation: Confirm the content is approved for public release before using publish steps or API commands.

Risk: Platform API tokens can grant publishing access beyond the immediate article workflow.

Mitigation: Use least-privilege Dev.to and Hashnode tokens and keep credentials in environment variables rather than article files.

Risk: Testing publish commands with live settings can create unintended public posts.

Mitigation: Use draft or unpublished modes when testing, then explicitly switch to live publishing after review.

## Reference(s):

- [Content Publisher skill page](https://clawhub.ai/qoohsuan/skills/content-publisher)
- [Medium new story](https://medium.com/new-story)
- [Dev.to articles API endpoint](https://dev.to/api/articles)
- [Hashnode GraphQL endpoint](https://gql.hashnode.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with checklists, ordered steps, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform API requests, browser publishing steps, SEO checks, and cross-posting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
