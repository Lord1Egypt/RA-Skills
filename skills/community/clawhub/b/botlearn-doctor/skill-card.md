## Description: <br>
Autonomously inspects a live OpenClaw instance across hardware, configuration, security, skills, and autonomy domains and produces a quantified traffic-light health report with actionable remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calvinxhk](https://clawhub.ai/user/calvinxhk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to diagnose a live OpenClaw installation, collect health signals, and receive prioritized remediation guidance for setup, configuration, security, installed skills, and autonomous operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local OpenClaw configuration, logs, workspace identity files, installed skills, and host details. <br>
Mitigation: Run it only for trusted diagnostics, keep generated reports local by default, and review reports for sensitive information before sharing. <br>
Risk: Reports can be delivered to external services when Slack, Discord, Feishu, Dingtalk, or email delivery is configured. <br>
Mitigation: Enable external delivery only intentionally, verify destination settings, and redact sensitive findings before sending reports outside the local environment. <br>
Risk: The artifact recommends forced installation of related botlearn skills. <br>
Mitigation: Review each suggested installation normally and avoid using force flags that skip risk prompts unless the publisher and target skill are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/calvinxhk/botlearn-doctor) <br>
- [Setup checks](artifact/setup.md) <br>
- [Data collection protocol](artifact/data_collect.md) <br>
- [Security risk checks](artifact/check_security.md) <br>
- [Configuration health checks](artifact/check_config.md) <br>
- [Autonomy checks](artifact/check_autonomy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown health report with scored findings and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports should avoid exposing credential values and should stay local unless the user intentionally configures an external delivery channel.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata; artifact frontmatter declares 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
