## Description:

本地监控屏幕活动，评估专注度，记录视觉历史，支持工作内容分析与专注状态查询，需用户许可启动。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hr2ay](https://clawhub.ai/user/hr2ay)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking users and agents use this skill to start or query a local FocusAI monitor that records screen activity, scores focus, recalls same-day activity history, and controls model/provider settings after user consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed for periodic screen monitoring, activity history storage, and screenshot analysis by configured visual model providers.

Mitigation: Install and use it only with explicit user consent, and limit invocations to clear FocusAI monitoring or history requests.

Risk: The install path may run unpinned external code through start.bat.

Mitigation: Review or pin the upstream code before running start.bat.

Risk: Broad natural-language triggers can expose sensitive same-day screen history.

Mitigation: Check that FocusAI data exists for the current day and answer history questions only when the user explicitly asks for that recall.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hr2ay/skills/focus-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration, Analysis]

**Output Format:** [Markdown guidance with inline code, local HTTP API calls, and concise activity summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language interaction guidance; requires explicit user consent before monitoring and same-day FocusAI data before history analysis.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
