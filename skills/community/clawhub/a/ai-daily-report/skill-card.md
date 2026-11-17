## Description:

Automatically generates and sends a daily AI report from recent AI news and popular open-source AI projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fireflywwj](https://clawhub.ai/user/fireflywwj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate a daily AI briefing with news summaries and selected open-source AI projects, then receive it as a rendered report image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically send generated report images to a Feishu chat.

Mitigation: Configure FEISHU_CHAT_ID only for the intended destination and review that destination before enabling scheduled runs.

Risk: The skill processes internet-sourced news and project content before upload.

Mitigation: Review generated reports before distribution and fix SVG escaping before relying on unattended execution.

Risk: The GitHub project fetch can use GITHUB_TOKEN.

Mitigation: Provide a least-privilege token and avoid sharing broader credentials with the skill runtime.

Risk: Project descriptions may be sent through googletrans when that optional dependency is available.

Mitigation: Disable or document googletrans use if external translation is not acceptable for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fireflywwj/skills/ai-daily-report)
- [SVG report template](references/report_template.svg)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown reports, SVG/PNG report files, JSON data files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can send the rendered PNG to Feishu when FEISHU_CHAT_ID and required tooling are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
