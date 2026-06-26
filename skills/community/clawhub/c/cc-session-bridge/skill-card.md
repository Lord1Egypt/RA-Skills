## Description: <br>
Cc Session Bridge helps agents install and run a script that converts Claude Code session streams into OpenClaw session records for AIMA collection and display. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steflerjiang](https://clawhub.ai/user/steflerjiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw/AIMA operators use this skill to install and run a Claude Code session bridge so CC work can be associated with AIMA tasks and reviewed in OpenClaw. It is intended for environments where session capture is explicitly desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge can persist full Claude Code session contents, tool results, and related metadata in OpenClaw session logs. <br>
Mitigation: Use it only when session capture is intended, run from a least-privilege working directory, avoid sensitive repositories or customer data, and review generated ~/.openclaw session logs. <br>
Risk: Captured sessions may retain sensitive data longer than expected if local retention and redaction controls are not configured. <br>
Mitigation: Add redaction and retention controls before using the skill for sensitive workloads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steflerjiang/cc-session-bridge) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation and usage guidance for a local Python bridge script and YAML configuration.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
