## Description:

Guides agents through SEO audits that diagnose crawlability, indexation, technical SEO, on-page optimization, content quality, authority signals, and prioritized fixes for organic search performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and site operators use this skill to audit SEO health, investigate ranking or traffic drops, and produce prioritized technical, on-page, and content recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read a local product marketing context file if one exists.

Mitigation: Do not place confidential strategy or private business details in that context file unless the agent is allowed to use them during SEO work.

Risk: The skill may use external SEO tools on URLs or page content provided by the user.

Mitigation: Use public URLs or approved test pages when possible, and avoid sharing sensitive unpublished content with external tools.

Risk: SEO recommendations can affect public traffic and indexing when implemented without review.

Mitigation: Review recommended fixes, especially robots.txt, canonical, redirect, noindex, sitemap, and migration changes, before applying them to production.

## Reference(s):

- [AI Writing Detection](references/ai-writing-detection.md)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [ClawHub skill page](https://clawhub.ai/mariokarras/skills/abm-seo-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown audit report with findings, evidence, fixes, priorities, and action plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference external SEO tools and requires user-provided site context, URLs, or analytics details for stronger findings.]

## Skill Version(s):

1.0.0 (source: server release metadata; skill metadata and changelog mention 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
