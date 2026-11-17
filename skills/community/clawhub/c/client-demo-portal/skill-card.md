## Description:

为企业客户快速搭建智慧芽情报门户演示原型，涵盖需求分析、本地搭建、数据对接、演示话术全流程

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External customer-facing solution teams and developers use this skill to plan and assemble a local PatSnap/Zhihuiya intelligence portal demo, connect approved data services, and prepare concise customer walkthrough material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys for Zhihuiya/PatSnap, DeepSeek, and other services could be exposed through local files, URLs, logs, or shared demo material.

Mitigation: Keep keys in protected environment configuration, avoid placing real keys in URLs or logs, and scrub secrets before sharing project files.

Risk: Internal customer documents or confidential analysis questions may be sent to external AI or data services during portal demonstrations.

Mitigation: Use only approved data, redact sensitive content, and confirm external processing approval before connecting customer documents or confidential prompts.

Risk: The portal workflow depends on external APIs and local configuration, so demos can fail if authorization, network access, or health checks are not verified.

Mitigation: Run the documented local health checks, verify authorized API access before customer sessions, and prepare fallback demo data for unstable services.

## Reference(s):

- [Client Demo Portal ClawHub Page](https://clawhub.ai/yuanzhian-patsnap/skills/client-demo-portal)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)
- [鸿远门户开发教训 0527](references/hongyuan_lessons_0527.md)
- [鸿远门户当前状态](references/hongyuan_portal_state.md)
- [调试教训汇总](references/lessons-learned.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local project structure, API integration notes, environment variable setup, debugging checks, and demo talk tracks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
