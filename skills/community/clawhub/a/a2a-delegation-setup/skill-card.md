## Description: <br>
Guided setup and troubleshooting for installing, enabling, configuring, verifying, and updating @aramisfa/openclaw-a2a-outbound in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aramisfacchinetti](https://clawhub.ai/user/aramisfacchinetti) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to install, configure, validate, update, and troubleshoot @aramisfa/openclaw-a2a-outbound on an OpenClaw Gateway host before handing off routine delegation to the runtime delegation skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or updating the third-party OpenClaw plugin changes gateway capabilities. <br>
Mitigation: Confirm trust in the plugin publisher and package before running install or update commands. <br>
Risk: Gateway configuration edits, target URLs, and restarts can affect active delegation behavior. <br>
Mitigation: Review target aliases, base URLs, URL override policy, and restart timing before applying changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aramisfacchinetti/a2a-delegation-setup) <br>
- [openclaw-a2a-outbound homepage](https://github.com/aramisfacchinetti/openclaw-a2a-plugins/tree/master/packages/openclaw-a2a-outbound#readme) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command blocks and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before installs, updates, restarts, or configuration edits.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
