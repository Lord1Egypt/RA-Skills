## Description: <br>
Autonomously inspects a live OpenClaw instance across 5 health domains: hardware, config, security, skills, and autonomy, then delivers a quantified traffic-light report with actionable fix guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1215656](https://clawhub.ai/user/1215656) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose local OpenClaw installations, inspect configuration, runtime health, security posture, installed skills, and autonomous readiness, and receive prioritized remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs deep local OpenClaw inspection and may bring configuration, logs, system details, and workspace identity summaries into the agent context. <br>
Mitigation: Use it only in environments where that diagnostic scope is acceptable, avoid echoing raw personal or credential-bearing content, and review generated reports before sharing. <br>
Risk: The security evidence flags recommendations that can encourage forced package installation. <br>
Mitigation: Independently review packages and updates before accepting any command that uses --force or bypasses installation prompts. <br>
Risk: Report delivery can target remote channels such as Slack, DingTalk, Feishu, Discord, or email when configured. <br>
Mitigation: Keep delivery on terminal or local browser unless remote sharing is intentional, verify channel configuration first, and rely on secret redaction as a backstop rather than the primary control. <br>


## Reference(s): <br>
- [ClawHub release: Botlearn Doctor@1.0.2](https://clawhub.ai/1215656/botlearn-doctor-1-0-2) <br>
- [Publisher profile: 1215656](https://clawhub.ai/user/1215656) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Setup and prerequisites](artifact/setup.md) <br>
- [Data collection protocol](artifact/data_collect.md) <br>
- [Security risk analysis reference](artifact/check_security.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown diagnostic report with traffic-light scores, findings, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are generated in English or Chinese based on the user's message language and may include local file paths, scores, and remediation steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 0.2.0 and artifact _meta.json reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
