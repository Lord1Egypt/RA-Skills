## Description:

Helps agents guide users through managing Volcengine CDN domains with the Volcengine CLI, including domain creation, cache refresh, and content preload workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CDN operators use this skill to prepare and run Volcengine CLI workflows for adding CDN acceleration domains, applying recommended web/download/video configurations, and submitting cache refresh or preload jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate workflows that make live Volcengine CDN configuration changes, including domain creation, cache refresh, and content preload operations.

Mitigation: Review every domain, origin, refresh URL, and preload URL before running commands, and test changes outside production where possible.

Risk: Volcengine credentials may be exposed if AK/SK values are pasted into chat, command history, or shared logs.

Mitigation: Use least-privilege credentials limited to required CDN actions and avoid entering secrets in chat or shell commands that are persisted in history.

Risk: The CLI installation guidance downloads executable tooling before cloud operations are run.

Mitigation: Verify the Volcengine CLI source and checksum independently before installation or upgrade.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-volc-cdn-manage)
- [Volcengine CLI documentation](https://github.com/volcengine/volcengine-cli)
- [CDN AddCdnDomain API documentation](https://www.volcengine.com/docs/6454/97340)
- [CDN SubmitRefreshTask API documentation](https://www.volcengine.com/docs/6454/97345)
- [CDN SubmitPreloadTask API documentation](https://www.volcengine.com/docs/6454/97346)
- [Volcengine CDN console](https://console.volcengine.com/cdn)
- [Parameter reference](references/parameters.md)
- [Usage examples](references/examples.md)
- [FAQ](references/faq.md)
- [CLI installation guide](references/install-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that call live Volcengine CDN APIs when run by the user.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact frontmatter version 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
