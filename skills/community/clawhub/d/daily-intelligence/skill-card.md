## Description:

Fully automated daily intelligence briefing system that searches news, generates high-res infographics, creates edge-tts voice narration, uploads to Feishu/Lark docs, and delivers via cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiongwang11](https://clawhub.ai/user/xiongwang11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate and deliver daily AI and technology intelligence briefings with curated modules, high-resolution infographics, Chinese voice narration, Feishu/Lark documents, and scheduled delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring autonomous delivery through external services may send briefings without adequate recipient scoping or consent.

Mitigation: Use a constrained workspace, least-privilege Feishu/Lark and messaging credentials, confirm recipients before sending, and run one-time previews before enabling delivery.

Risk: Scheduled cron jobs may continue running after the intended release or evaluation period.

Mitigation: Create scheduled jobs only with an explicit expiration and maintain a documented removal process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiongwang11/skills/daily-intelligence)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and generated briefing assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include 3600px infographic images, Chinese MP3 narration, Feishu/Lark document links, and cron scheduling configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
