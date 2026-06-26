## Description: <br>
Manage a self-hosted Trello-like WeKan board via `wekancli`, including creating, moving, and archiving cards, lists, and boards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manman1104](https://clawhub.ai/user/manman1104) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate a configured WeKan instance through `wekancli` for board, list, card, checklist, and comment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change board data using the WeKan account or token provided to the agent. <br>
Mitigation: Use a least-privileged or agent-specific WeKan account and confirm create, edit, archive, or delete-related actions before execution. <br>
Risk: Login output and WEKAN_TOKEN grant access to the configured WeKan instance. <br>
Mitigation: Treat tokens and login output as sensitive secrets and avoid exposing them in shared transcripts, logs, or rendered task summaries. <br>
Risk: Some actions, including listing users and delete APIs, may require admin privileges or permanently affect board data. <br>
Mitigation: Avoid admin tokens unless necessary, prefer archiving over deletion, and verify role requirements before running privileged commands. <br>


## Reference(s): <br>
- [WeKan CLI Reference](artifact/references/cli-examples.md) <br>
- [WeKan CLI Skill Installation Notes](artifact/references/user-install.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/manman1104/ces) <br>
- [Wekan CLI package source](https://github.com/madsmith/wekan_cli.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include WeKan identifiers and JSON CLI output; requires WEKAN_URL and WEKAN_TOKEN for authenticated actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
