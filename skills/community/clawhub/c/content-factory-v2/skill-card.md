## Description:

Create complete WeChat Official Account viral articles from a user-provided title by researching high-view YouTube videos, confirming topic/outline with user, writing professional content through self-iteration, and outputting both Markdown and HTML formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffli2002](https://clawhub.ai/user/jeffli2002)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketing teams, and agent developers use this skill to research timely source material, confirm an article direction with the user, and produce Chinese WeChat Official Account articles with Markdown and HTML publishing assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling may expose or reuse WeChat, Tavily, Brave, or GLM secrets.

Mitigation: Remove hardcoded secrets, avoid printing credential values, avoid passing secrets on command lines, and rotate any credentials previously used in logged environments.

Risk: Publishing authority is under-scoped for a workflow that can create or submit WeChat drafts.

Mitigation: Require explicit user approval before publishing and review account permissions before enabling automated WeChat operations.

Risk: Proxying publishing requests can weaken transport or destination controls.

Mitigation: Use only HTTPS proxies with an explicit allowlist for expected WeChat API endpoints.

Risk: Promotional calls to action or reference behavior may be added unexpectedly.

Mitigation: Make promotional CTA and reference insertion opt-in and review final article content before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeffli2002/skills/content-factory-v2)
- [API key setup](artifact/API_KEY_SETUP.md)
- [Configuration guide](artifact/CONFIGURATION.md)
- [Update summary](artifact/UPDATE_SUMMARY.md)
- [WeChat publish rules](artifact/references/WECHAT_PUBLISH_RULES.md)
- [WeChat format rules](artifact/references/wechat-format-rules.md)
- [WeChat viral frameworks](artifact/references/wechat_viral_frameworks.md)
- [YouTube research checklist](artifact/references/youtube_research_checklist.md)
- [WeChat Official Account platform](https://mp.weixin.qq.com/)
- [WeChat access token API](https://api.weixin.qq.com/cgi-bin/token)
- [WeChat draft API](https://api.weixin.qq.com/cgi-bin/draft/add)
- [WeChat free publish API](https://api.weixin.qq.com/cgi-bin/freepublish/submit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and HTML article assets with supporting commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-approved outlines, source notes, cover-image workflow guidance, and optional WeChat publishing steps.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
