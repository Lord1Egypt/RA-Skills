## Description:

Transform blog posts, articles, and long-form content into multiple formats, including videos, podcasts, social media posts, and summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams, marketers, and creators use this skill to repurpose owned long-form content into platform-specific drafts for social posts, email sequences, video scripts, podcast scripts, summaries, and related distribution assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle credentials for OpenAI, Anthropic, Google Drive, WordPress, Slack, or related integrations.

Mitigation: Use only scoped credentials intended for this workflow and store them in a managed environment or vault.

Risk: The skill describes publishing, CRM sync, Slack webhook use, and social distribution workflows that could expose content externally.

Mitigation: Require manual review and approval before generated content is posted, synced, or sent to third-party services.

Risk: Source content may include confidential, regulated, copyrighted, or attribution-sensitive material.

Mitigation: Repurpose only content the user owns or is approved to use, and avoid confidential or regulated material unless organizational policy allows it.

Risk: Generated marketing content can include factual errors, unsupported claims, or misleading statistics.

Mitigation: Fact-check generated claims against the source material before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/ai-powered-content-repurposing)
- [Skill homepage](https://github.com/ncreighton/empire-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with prompt examples, configuration snippets, and generated content drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce platform-specific drafts for social media, email, video, podcast, summaries, calendars, SEO metadata, and publishing workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
