## Description:

Fetches AI news from 36Kr or Huxiu, rewrites it into a WeChat Official Account article, and publishes it to the WeChat draft box.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anydebug](https://clawhub.ai/user/anydebug)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and developers use this skill to collect daily AI industry news, select one publishable topic, draft a 1,000-2,000 word WeChat article, and create a WeChat Official Account draft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect a WeChat Official Account by creating a draft.

Mitigation: Require manual confirmation before any WeChat draft is created and review the final article before publication.

Risk: The skill reads WeChat credentials and may load them from shared workspace files.

Mitigation: Provide credentials through a dedicated secret mechanism and use a low-privilege or isolated account.

Risk: The publishing script can install a global npm package if the publishing CLI is missing.

Mitigation: Preinstall and pin @wenyan-md/cli before running the skill instead of allowing automatic global installation.

Risk: The workflow scrapes external news sites and rewrites news content.

Mitigation: Run in an isolated workspace and review source attribution, factual accuracy, and rights-sensitive content before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anydebug/skills/ai-news-publisher)
- [36Kr AI news channel](https://www.36kr.com/information/AI/)
- [Huxiu AI channel](https://www.huxiu.com/channel/106.html)
- [Writing guide](references/writing-guide.md)
- [Scrapling fetching guide](references/scrapling-fetching.md)
- [Scrapling parsing guide](references/scrapling-parsing.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown article with frontmatter, shell commands, and publication status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local topic history and may create a WeChat Official Account draft when credentials are configured.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
