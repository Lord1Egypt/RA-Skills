## Description:

Repurpose a single piece of content (tweet, article, description) into 10+ formats: Twitter thread, LinkedIn post, blog intro, email newsletter, Discord announcement, Reddit post, Quora answer, Instagram caption, email subject lines, and meta descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and content teams use this skill to turn one source text item into platform-specific marketing drafts for social, email, blog, community, Q&A, and SEO channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted content, including local file contents passed with @file, may be sent to MiniMax for generation.

Mitigation: Use only content that is appropriate to share with MiniMax; do not pass secrets, credentials, private documents, customer data, regulated content, or .env files unless provider handling has been reviewed and the upload is intended.

Risk: Generated marketing drafts may be inaccurate, misleading, or unsuitable for a target platform or audience.

Mitigation: Review generated outputs before publishing and adapt claims, tone, compliance language, and platform-specific requirements as needed.

## Reference(s):

- [Content Repurposer ClawHub page](https://clawhub.ai/fuzzyb33s/skills/content-multiplier-fuzzyb33s)
- [MiniMax chat completion endpoint](https://api.minimax.chat/v1/text/chatcompletion_pro)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Shell commands, Configuration]

**Output Format:** [Structured JSON with generated text fields and optional per-format output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY; accepts content text or @file input, content type override, tone selection, and output directory.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
