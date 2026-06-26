## Description: <br>
D&D 3.5 standard rules RPG character system for AI lobster assistants that generates character sheets from SOUL.md and MEMORY.md, tracks XP and leveling, computes combat stats, emits RPG flavor text, sends daily reports, and includes arena and dashboard features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ramboxie](https://clawhub.ai/user/ramboxie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add an RPG-style progression layer to an OpenClaw assistant, including character initialization, XP synchronization, level and stat reporting, prestige, arena interactions, dashboard viewing, and scheduled status reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads assistant identity and memory files and maintains ongoing saved RPG state. <br>
Mitigation: Install it only in the intended OpenClaw workspace and review generated state before relying on it. <br>
Risk: The dashboard can be exposed on the local network. <br>
Mitigation: Bind the dashboard to localhost, add access controls, or avoid running it on shared networks. <br>
Risk: Telegram reporting and cron setup can create outbound notifications or persistent automation. <br>
Mitigation: Leave Telegram configuration unset and do not run setup-cron.mjs unless those behaviors are intended. <br>
Risk: The documented report.mjs --preview behavior is not honored by the current implementation. <br>
Mitigation: Test reporting without Telegram credentials or in an isolated workspace before enabling live notifications. <br>


## Reference(s): <br>
- [Claw RPG skill page](https://clawhub.ai/ramboxie/claw-rpg) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Class Features & Feats](references/abilities.md) <br>
- [Class System](references/classes.md) <br>
- [Prestige System](references/prestige.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated JSON state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can update persistent character state, emit RPG flavor text, send optional Telegram notifications, and serve a local web dashboard.] <br>

## Skill Version(s): <br>
3.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
