## Description: <br>
clash-auto-switch lets an agent check Clash proxy health, list and switch proxy nodes, and automatically move to a preferred healthy node. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adminlove520](https://clawhub.ai/user/adminlove520) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators who run Clash use this skill to let an agent inspect proxy health and switch nodes manually, by region, or automatically when connectivity fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change local proxy routing automatically or on a schedule. <br>
Mitigation: Enable automatic or scheduled switching only when unattended routing changes are acceptable. <br>
Risk: The artifact includes unsafe Clash credential handling in Bash helper scripts. <br>
Mitigation: Prefer the Python/OpenClaw path, remove or rotate embedded Bash secrets before use, and keep CLASH_SECRET in protected local configuration. <br>
Risk: A reachable Clash controller could let the agent alter proxy selection. <br>
Mitigation: Bind the Clash controller to localhost and install the skill only when agent-controlled proxy selection is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adminlove520/clash-auto-switch) <br>
- [Publisher profile](https://clawhub.ai/user/adminlove520) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Agent command responses with Markdown guidance and shell or configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the local Clash controller API when invoked with configured credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
