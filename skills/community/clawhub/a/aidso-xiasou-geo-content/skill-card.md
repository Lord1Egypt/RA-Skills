## Description:

AIDSO虾搜生成式引擎优化内容生产 Skill，支持 API Key 绑定、检查，并根据品牌、AI问题和目标优化AI平台生成内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangyuanmile-coder](https://clawhub.ai/user/tangyuanmile-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to bind or check an AIDSO GEO API key and generate brand-focused content intended for citation or improved visibility on supported AI platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API-key binding flow handles the AIDSO credential in an unsafe and under-disclosed way.

Mitigation: Review the skill before installing, use a dedicated low-privilege AIDSO API key, and rotate any key already used with this binding flow.

Risk: The skill can store AIDSO_GEO_API_KEY in a local .env file in the skill directory.

Mitigation: Avoid sharing the skill directory or committing the .env file, and prefer environment-level secret management when available.

Risk: Confirmed content generation sends brand and AI-question data to the AIDSO API and consumes 6 credits.

Mitigation: Confirm the brand, question, target AI platform, and credit spend before running generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangyuanmile-coder/skills/aidso-xiasou-geo-content)
- [AIDSO API key settings](https://geo.aidso.com/setting?type=apiKey)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON command output with generated article text or Markdown when content generation succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AIDSO_GEO_API_KEY credential and explicit confirmation before spending 6 credits on content generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
