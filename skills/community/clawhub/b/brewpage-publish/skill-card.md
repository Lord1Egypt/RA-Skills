## Description:

Draft, publish, and update BrewPage pages and sites from supplied content, including forms that save visitor responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kochetkov-ma](https://clawhub.ai/user/kochetkov-ma)

### License/Terms of Use:

MIT

## Use Case:

Developers and site owners use this skill to prepare BrewPage drafts, publish pages or static sites, and update a specific publication. It can also create forms that save visitor responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published pages may be open to anyone with the link, and public pages may be discoverable.

Mitigation: Review the content and access settings before publishing; remove sensitive information or use password protection when appropriate.

Risk: Workspace history or recovery receipts may contain owner keys that can manage anonymous publications.

Mitigation: Keep those files private and out of shared logs, prompts, and uploaded content.

Risk: The skill uses shell, network, and local file-writing capabilities to prepare and publish content.

Mitigation: Review the requested action and runtime permissions, and use a local draft when no remote publication is intended.

## Reference(s):

- [BrewPage](https://brewpage.app)
- [BrewPage REST API](https://brewpage.app/api/)
- [BrewPage Page data guide](https://brewpage.app/llms-page-data.txt)
- [BrewPage templates](https://brewpage.app/templates)
- [BrewPage custom domains guide](https://brewpage.app/llms-full.txt#custom-domains)
- [OpenClaw skill documentation](https://docs.openclaw.ai/tools/skills)
- [ClawHub release](https://clawhub.ai/kochetkov-ma/skills/brewpage-publish)
- [Publisher profile](https://clawhub.ai/user/kochetkov-ma)

## Skill Output:

**Output Type(s):** [HTML, Markdown, JSON, Files, Guidance, Links]

**Output Format:** [Draft page or site content and a concise publication result, including a reader link when a publish succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include forms that save visitor responses and published content with selected access settings.]

## Skill Version(s):

1.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
