## Description: <br>
Operate and troubleshoot the AIHealingMe CLI through the npm package (`aihealingmecli`) for auth, user, audio, plan, chat, emotion, subscription, payload-shaping, command-diagnostic, and API failure-handling workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bebetterest](https://clawhub.ai/user/bebetterest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run and troubleshoot AIHealingMe CLI commands, shape JSON payloads, diagnose command and API errors, and verify account, healing, chat, emotion, subscription, and raw API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through account, billing, raw API, and sensitive emotional-health workflows. <br>
Mitigation: Use test accounts where possible, verify `whoami`, region, and API base before mutation, and require explicit human approval before account, billing, delete, notification, raw API, chat, emotion, memory, or behavior actions. <br>
Risk: Bearer tokens or passwords may be exposed when passed directly on command lines. <br>
Mitigation: Avoid passing real passwords or bearer tokens on the command line; prefer scoped test credentials and confirm token state with safe inspection commands. <br>
Risk: The skill depends on the external `aihealingmecli` npm package and live AIHealingMe service behavior. <br>
Mitigation: Install only if the package is trusted, run smoke checks before operational use, and confirm API target, locale, region, and network behavior before executing state-changing commands. <br>


## Reference(s): <br>
- [Command Map](references/command-map.md) <br>
- [Error Playbook](references/error-playbook.md) <br>
- [AIHealingMe](https://aihealing.me/) <br>
- [ClawHub Skill Page](https://clawhub.ai/bebetterest/aiheal-cli-operator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CLI command sequences, payload-file recommendations, troubleshooting steps, and validation guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
