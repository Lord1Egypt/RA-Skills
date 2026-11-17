## Description:

Analyze and audit content for readability, tone, and sentiment with AI-powered insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams, marketers, copywriters, and publishers use this skill to audit written content for readability, tone, sentiment, SEO performance, audience alignment, and repurposing opportunities before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive unpublished content may be sent through the configured AI or integration services during analysis.

Mitigation: Avoid submitting sensitive drafts unless the user has approved that data flow and the configured services meet the user's privacy requirements.

Risk: API keys can be exposed when bearer tokens are placed directly in shell command arguments.

Mitigation: Use a safer API-key verification method and avoid commands that expose credentials through shell history, process listings, or logs.

Risk: Audit recommendations can be incomplete for factual accuracy, plagiarism, regulated claims, or cultural context.

Mitigation: Require human editorial or subject-matter review before using recommendations for publication, legal, medical, or culturally sensitive content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ncreighton/skills/content-audit-expert)
- [OpenAI API Keys](https://platform.openai.com/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style audit reports with scores, findings, and actionable recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include readability metrics, tone and sentiment classifications, SEO suggestions, audience alignment notes, before/after copy examples, and repurposing ideas.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
