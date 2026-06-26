## Description: <br>
Auto Skill Scanner monitors installed OpenClaw skills with static checks for hardcoded credentials, shell injection patterns, environment exposure, and network disclosure risks, then reports findings to configured channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ohmanymoneygomyhome-creator](https://clawhub.ai/user/ohmanymoneygomyhome-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run recurring or on-demand static security scans across installed skills and receive concise findings in their configured messaging channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates recurring automated scans and can deliver summaries broadly across active OpenClaw channels. <br>
Mitigation: Install it only where daily reports are desired, confirm that each active channel is an appropriate recipient, and remove the cron jobs when automated reporting is no longer needed. <br>
Risk: Static pattern matching can produce false positives or miss context-specific issues. <br>
Mitigation: Treat reported findings as review prompts, verify each issue before removing a skill, and use additional review for high-risk environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ohmanymoneygomyhome-creator/auto-skill-scanner) <br>
- [Skill Security Audit reference](references/security-checks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style text report with scan summaries, issue counts, affected skills, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also configure recurring OpenClaw cron jobs that deliver reports to active channels.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
