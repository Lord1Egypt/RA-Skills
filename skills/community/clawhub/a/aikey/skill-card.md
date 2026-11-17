## Description:

AI KEY routes users to skills for content creation and review or business analysis, with guided onboarding and follow-up navigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzifei](https://clawhub.ai/user/iamzifei)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and small business operators use AI KEY to choose an appropriate companion skill for planning, drafting, reviewing, and reflecting on content, or for analyzing business performance and decisions. It also guides first-time users and suggests follow-up steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports automatic network version checks beyond the described routing and onboarding tasks.

Mitigation: Review the version-check behavior and decide whether to allow its outbound network access before installing.

Risk: The security summary reports persistent storage of feedback.

Mitigation: Check what feedback is retained and where it is stored, especially before sharing sensitive business or creator information.

Risk: The scan was partial: 12 of 14 components were scanned, and tool-misuse analysis was degraded for two shell scripts.

Mitigation: Review the remaining components and the shell scripts before installation; the suspicious verdict is not evidence of malicious intent.

## Reference(s):

- [Family conventions](references/家族公约.md)
- [Interaction guidelines](references/交互规范.md)
- [Built-in decision rules](references/规则卡.md)
- [Content theory foundation](references/内容理论底座.md)
- [Cognitive framework](references/认知框架.md)
- [AI KEY project and upgrade instructions](https://github.com/iamzifei/aikey#老用户升级zmm-已改名为-ai-key)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Natural-language responses and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route work to companion AI KEY skills or provide a prompt or choice when routing is uncertain.]

## Skill Version(s):

0.3.14 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
