## Description: <br>
Manages AI agent project memory by creating and maintaining project-level .openclaw files for mission, snapshot, and decision context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanchunlee](https://clawhub.ai/user/hanchunlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use APPM to preserve project goals, current status, next actions, and decision history across session resets and parallel project switches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill maintains persistent local memory from conversation-derived project context. <br>
Mitigation: Review what is written to .openclaw files and the APPM registry, and avoid using the skill with sensitive projects or conversations unless local persistence is acceptable. <br>
Risk: Automatic updates may write project state without a clearly documented review step. <br>
Mitigation: Configure agent workflows to ask before updating SNAPSHOT.md or data/appm_registry.json, and periodically inspect those files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanchunlee/appm) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and local project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local .openclaw project memory files and may read or write a local APPM registry.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
