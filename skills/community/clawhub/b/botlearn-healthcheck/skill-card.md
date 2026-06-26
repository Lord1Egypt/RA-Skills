## Description: <br>
botlearn-healthcheck is a BotLearn autonomous health inspector for OpenClaw instances across hardware, configuration, security, skills, and autonomy domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calvinxhk](https://clawhub.ai/user/calvinxhk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to inspect OpenClaw installations, collect diagnostic evidence, generate scored health reports, and guide repairs after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs broad local inspection of OpenClaw configuration, logs, heartbeat files, identity/profile documents, and secret locations. <br>
Mitigation: Install and run it only in environments where that inspection is acceptable, and review generated reports before sharing them. <br>
Risk: Diagnostic reports are saved persistently and may include sensitive operational context even when credential values are redacted. <br>
Mitigation: Treat saved reports as sensitive operational artifacts and redact paths, identities, and environment details before external distribution. <br>
Risk: The skill may recommend forced package installs or repair commands that change system capabilities. <br>
Mitigation: Approve repair commands one at a time only after checking the exact command, rollback step, and package trust. <br>
Risk: Package and registry checks may contact ClawHub services while local health checks query the OpenClaw gateway. <br>
Mitigation: Run the skill only where those network checks are expected, and review the environment's network policy before scheduled use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/calvinxhk/botlearn-healthcheck) <br>
- [Publisher profile](https://clawhub.ai/user/calvinxhk) <br>
- [README](artifact/README.md) <br>
- [Setup and prerequisites](artifact/setup.md) <br>
- [Data collection protocol](artifact/data_collect.md) <br>
- [OpenClaw platform knowledge](artifact/openclaw_knowledge.md) <br>
- [Fix cases knowledge base](artifact/fix_cases.md) <br>
- [Security domain checks](artifact/check_security.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown reports, HTML reports, diagnostic summaries, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates persistent health reports under the OpenClaw memory health-reports directory and presents repair steps with rollback guidance.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter and README list 0.1.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
