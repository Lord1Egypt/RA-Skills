## Description: <br>
Agent Maker helps users create OpenClaw agents through guided requirements collection and generated local agent configuration files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squallfire](https://clawhub.ai/user/squallfire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Agent Maker to create, list, and validate local OpenClaw agent configurations for specialized assistant roles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent local agent files in the user's home directory with weak path and overwrite safeguards. <br>
Mitigation: Check whether the target agent already exists, use simple kebab-case names, and review generated files before enabling the agent. <br>
Risk: Custom workspace paths may cause files to be created in an unintended local location. <br>
Mitigation: Avoid custom workspace paths unless the exact path has been reviewed and approved. <br>


## Reference(s): <br>
- [Agent Maker on ClawHub](https://clawhub.ai/squallfire/agent-maker) <br>
- [squallfire publisher profile](https://clawhub.ai/user/squallfire) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance, shell command output, and generated local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent local files under the user's OpenClaw agent and workspace directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
