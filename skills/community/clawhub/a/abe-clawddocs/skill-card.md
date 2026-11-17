## Description:

Clawdbot documentation expert with decision tree navigation, search scripts, doc fetching, version tracking, and config snippets for all Clawdbot features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to find, interpret, and apply Clawdbot documentation for setup, provider configuration, troubleshooting, automation, platform deployment, and common configuration snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Questions and configuration details may be sent to the external SkillBoss service.

Mitigation: Use the skill only when SkillBoss API use is acceptable, and avoid sharing API tokens, private logs, production secrets, or proprietary infrastructure details unless privacy and retention terms have been reviewed.

Risk: The package references helper scripts and snippets that may be absent unless supplied elsewhere.

Mitigation: Confirm required scripts and snippet files exist in the installed skill before relying on search, cache, indexing, or ready-made configuration workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/abe-clawddocs)
- [Clawdbot documentation](https://docs.clawd.bot/)
- [Clawdbot Discord provider documentation](https://docs.clawd.bot/providers/discord)
- [SkillBoss API Hub endpoint](https://api.skillboss.com/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require SKILLBOSS_API_KEY; full-text index workflows may require qmd.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
