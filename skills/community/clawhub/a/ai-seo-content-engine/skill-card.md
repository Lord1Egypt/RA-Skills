## Description:

Automated SEO content generator that schedules daily SaaS review articles using OpenAI GPT-4o, publishes to a Hugo blog via API, and tracks output in Google Sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mhmalvi](https://clawhub.ai/user/mhmalvi)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

Content teams, affiliate marketers, agencies, and blog operators can use this skill to configure an n8n workflow that drafts SEO-focused SaaS articles, formats them for Hugo, publishes them through a blog admin API, and records publication status in Google Sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow auto-publishes AI-generated review content with admin credentials.

Mitigation: Add a draft or approval step before publication and scope the admin key to the minimum permissions needed.

Risk: The workflow includes unsafe API-key and blog endpoint defaults.

Mitigation: Change the blog endpoint to HTTPS and remove the API-key fallback before installation.

Risk: Generated content may include unsupported first-person testing claims.

Mitigation: Remove first-person testing claims unless real review evidence is available.

## Reference(s):

- [Ai Seo Content Engine on ClawHub](https://clawhub.ai/mhmalvi/skills/ai-seo-content-engine)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with n8n workflow configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup steps, credential placeholders, scheduling guidance, and review recommendations for the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
