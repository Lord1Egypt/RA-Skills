## Description:

2Ryun Skill helps agents use the 2Ryun REST API to manage documents and notes, search and organize a knowledge base, generate web pages, upload assets, and publish content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iguoguo](https://clawhub.ai/user/iguoguo)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to let an agent work with 2Ryun content workflows, including document import, knowledge-base search, web page generation, asset upload, and publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through write actions that modify, delete, upload, share, extract, or publish user content.

Mitigation: Require explicit user confirmation before any destructive, sharing, upload, extraction, or publishing action.

Risk: Bearer API keys can grant broad access to 2Ryun modules if exposed or over-scoped.

Mitigation: Use a least-privilege API key, preferably read-only for search tasks, and do not paste bearer keys into chat.

Risk: Published pages and uploaded assets may be accessible by URL.

Mitigation: Avoid uploading sensitive files and confirm publication intent before creating public URLs.

## Reference(s):

- [2Ryun API specification](2ryun-api-spec.md)
- [2Ryun platform](https://2ryun.com)
- [Server-resolved source repository](https://github.com/iguoguo/2Ryun-skill)
- [ClawHub skill page](https://clawhub.ai/iguoguo/skills/2ryun-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with REST API request examples and JSON response handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose authenticated API calls that create, update, delete, upload, share, or publish user content.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
