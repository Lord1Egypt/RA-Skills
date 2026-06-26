## Description: <br>
Automated SEO content generator that schedules daily SaaS review articles using OpenAI GPT-4o, publishes to a Hugo blog via API, and tracks output in Google Sheets. Supports 18 SaaS categories and 4 content types. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[mhmalvi](https://clawhub.ai/user/mhmalvi) <br>

### License/Terms of Use: <br>
CC BY-NC-SA 4.0 <br>


## Use Case: <br>
External developers, content operators, affiliate marketers, and agencies use this skill to configure an n8n workflow that generates scheduled SaaS review, comparison, best-of, and guide articles, publishes them to a Hugo blog, and records publication status in Google Sheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can publish AI-generated posts directly to a live blog on a recurring schedule. <br>
Mitigation: Add a manual approval or draft-only step before activation, and review factual claims, pricing, recommendations, and affiliate disclosures before publication. <br>
Risk: The blog publishing step uses an API-key header and the evidence notes a plain HTTP admin API placeholder. <br>
Mitigation: Use HTTPS for the blog admin API and store a dedicated low-privilege API key in environment or credential storage. <br>
Risk: The article prompt asks for first-person testing claims that may be unsupported. <br>
Mitigation: Remove unsupported first-person claims or require real review notes before generated articles are published. <br>
Risk: The workflow depends on OpenAI, Google Sheets, SMTP, and blog API credentials. <br>
Mitigation: Use dedicated low-privilege credentials for each service and rotate any credential that may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mhmalvi/ai-seo-content-engine) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [n8n content generation workflow](artifact/workflows/content-gen-workflow.json) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON workflow configuration and inline environment-variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance for an n8n workflow that uses OpenAI, Google Sheets, SMTP, and a Hugo blog admin API.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
