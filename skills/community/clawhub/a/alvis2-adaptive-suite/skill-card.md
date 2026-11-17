## Description:

Adaptive Suite helps Clawdbot provide adaptive coding, business analysis, project management, web and data development, free-resource discovery, and read-only NAS metadata scraping guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill for broad coding, web and data development, business analysis, project planning, low-cost resource discovery, and read-only NAS metadata scanner guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may call the third-party SkillBoss API while assisting with broad tasks.

Mitigation: Use only after defining when external API calls are allowed and avoid sending confidential repository, business, or private file-share data.

Risk: NAS metadata scanning can expose file names, directory structure, and other sensitive metadata.

Mitigation: Limit scans to explicitly approved paths, keep scanning read-only, and add redaction or review before sharing collected metadata.

Risk: The skill has broad assistant behavior across coding, business analysis, project management, web development, and data analysis.

Mitigation: Review generated recommendations, commands, and code before use, especially where outputs affect production systems or business decisions.

## Reference(s):

- [Adaptive Suite on ClawHub](https://clawhub.ai/alvisdunlop/skills/alvis2-adaptive-suite)
- [ClawHub publisher profile: alvisdunlop](https://clawhub.ai/user/alvisdunlop)
- [Moltbot skills documentation](https://docs.molt.bot/tools/skills)
- [SkillBoss API Hub endpoint](https://api.SkillBoss.co/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with code blocks and command or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce guidance involving third-party API use, required local tools, and read-only NAS metadata scanning workflows.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
