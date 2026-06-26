## Description: <br>
Detects and coordinates potential conflicts across crontab entries, systemd services, overlapping scripts, log paths, and related mechanism documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alfredming-2026](https://clawhub.ai/user/alfredming-2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect automation mechanisms for duplicate schedules, unhealthy services, overlapping maintenance scripts, inconsistent log locations, and missing coordination documentation. It is intended for periodic checks and post-configuration-change reviews in an OpenClaw-style workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script sends conflict counts, service status, workspace paths, and report locations to a hard-coded Feishu recipient. <br>
Mitigation: Disable Feishu sending or make the recipient configurable before running the script on sensitive systems. <br>
Risk: The skill inspects local crontab, user systemd state, workspace files, logs, and documentation paths. <br>
Mitigation: Run it only in an expected workspace and review the generated report before sharing or acting on its findings. <br>
Risk: The script assumes fixed OpenClaw workspace paths and supporting task utilities. <br>
Mitigation: Confirm or parameterize workspace paths and dependencies before scheduling automated execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alfredming-2026/conflict-coordination) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated conflict reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational summaries and can send notification messages when the bundled script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
