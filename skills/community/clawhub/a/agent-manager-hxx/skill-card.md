## Description: <br>
Manages the OpenClaw Agent lifecycle, including Agent configuration, Matrix account registration, and account binding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cxlhyx](https://clawhub.ai/user/cxlhyx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to add, remove, list, and bind Agents and Matrix accounts in an OpenClaw configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live Matrix credentials and persistent OpenClaw configuration changes with weak safeguards. <br>
Mitigation: Review before installing, use only with a disposable or backed-up OpenClaw configuration, avoid shared terminals and CI logs, prefer HTTPS homeservers, and rotate generated Matrix passwords or tokens after setup. <br>
Risk: The security guidance warns not to rely on CONFIG_PATH until scripts honor it consistently. <br>
Mitigation: Confirm which configuration file will be changed before execution and back up the target OpenClaw configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cxlhyx/agent-manager-hxx) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify OpenClaw configuration files and may emit Matrix user IDs, access tokens, and generated passwords during setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
