## Description:

China Localization provides Chinese-language interface strings, localized search, weather summaries, and China service integration helpers for OpenClaw users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add Chinese-first localization, Chinese search behavior, weather summaries, and configuration guidance for China-oriented service integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests powerful third-party credentials for integrations that are mostly unimplemented.

Mitigation: Configure only credentials needed for implemented features, and avoid adding Feishu, WeChat, DingTalk, Amap, or Alipay secrets until each integration is implemented and scoped.

Risk: Baidu search and Feishu-style outputs may be placeholder or mock data rather than live service results.

Mitigation: Treat these outputs as illustrative and verify results against the source service before using them for operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincentlau2046-sudo/skills/china-localization)
- [Feishu Open Platform](https://open.feishu.cn/app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, Chinese-language text, TypeScript objects, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first output; credentials are configured through environment variables; several third-party integrations return placeholder or mock results.]

## Skill Version(s):

2.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
