## Description:

Aggregate and manage articles, highlights, notes, and tags from a user's trusted feeds, podcasts, and news sources through FeedNest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucaiaconelli](https://clawhub.ai/user/lucaiaconelli)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to work with FeedNest accounts from an agent: reading and searching articles, managing saved items, highlights, notes, and tags, and generating article audio from trusted sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a FeedNest API key and plugin access to a user's account data.

Mitigation: Install only from the trusted FeedNest plugin publisher, review the package and version before use, and avoid granting unnecessary account permissions.

Risk: Bulk or destructive account actions, such as deleting tags or marking all articles as read, can change user data at scale.

Mitigation: Confirm user intent before bulk or destructive actions and present the affected scope clearly before proceeding.

Risk: RSS article content can be truncated, which may lead to incomplete summaries or analysis.

Mitigation: Check full article content when needed and use the extract-article workflow only for articles that appear truncated.

## Reference(s):

- [FeedNest Skill on ClawHub](https://clawhub.ai/lucaiaconelli/skills/feednest)
- [FeedNest](https://www.feednest.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the FeedNest plugin, a FeedNest Pro account, and an API key.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
