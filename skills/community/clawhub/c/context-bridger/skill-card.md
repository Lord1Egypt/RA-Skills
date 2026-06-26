## Description: <br>
Maintains and transfers context across sessions, models, and time to avoid repeating information on every new interaction or model switch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loudmouthedmedia](https://clawhub.ai/user/loudmouthedmedia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to preserve working context across new sessions, model switches, and restarts. It creates local registries, discovery data, and handoff notes so future sessions can resume with less manual re-explanation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local context and registry files may contain secrets, credentials, personal data, or untrusted instructions if users add them. <br>
Mitigation: Review handoff and registry content before reuse, and avoid storing secrets, credentials, personal data, or untrusted instructions in those files. <br>
Risk: The setup script creates or overwrites files under ~/.openclaw. <br>
Mitigation: Review setup.sh and the target file paths before running it, especially in an existing OpenClaw environment. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/loudmouthedmedia/context-bridger) <br>
- [Context Bridge Homepage](https://github.com/loudmouthedmedia/context-bridge) <br>
- [Context Bridge Support](https://github.com/loudmouthedmedia/context-bridge/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local JSON or Markdown file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Setup creates or updates local OpenClaw registry, discovery, handoff, and helper script files under ~/.openclaw.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
