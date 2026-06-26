## Description: <br>
Deer Flow Manager guides an agent through installing, configuring, updating, uninstalling, and troubleshooting DeerFlow 2.0. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[braveheartzjh](https://clawhub.ai/user/braveheartzjh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage a local DeerFlow 2.0 installation, including model setup, dependency checks, service startup, updates, removal, and common startup troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides real install, update, and uninstall commands that can change or remove a local DeerFlow directory. <br>
Mitigation: Review commands before running them, confirm ~/deer-flow is the intended directory, and back up config.yaml, .env, logs, and custom changes before rebuilding or uninstalling. <br>
Risk: Model setup may involve API keys or other sensitive credentials. <br>
Mitigation: Keep API keys in environment variables or local secret storage, and avoid placing secrets in chat transcripts or source control. <br>


## Reference(s): <br>
- [DeerFlow 2.0 command reference](references/deer-flow-commands.md) <br>
- [DeerFlow upstream repository](https://github.com/bytedance/deer-flow.git) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command tables, file locations, and troubleshooting steps for local DeerFlow management.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
