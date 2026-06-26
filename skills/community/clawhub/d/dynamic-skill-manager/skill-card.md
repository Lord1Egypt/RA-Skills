## Description: <br>
Track and manage OpenClaw skills usage, find idle skills, and safely uninstall unused ones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[welkeyever](https://clawhub.ai/user/welkeyever) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to inspect installed OpenClaw skills, track skill usage, identify idle skills, and uninstall unused non-system skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete installed skills during uninstall operations. <br>
Mitigation: Inspect the target skill name before uninstalling and back up any skill you may need to restore. <br>
Risk: The skill stores usage context in a local usage log. <br>
Mitigation: Do not pass secrets or sensitive task details as tracking context, and periodically review or delete ~/.openclaw/workspace/.skill-manager/. <br>


## Reference(s): <br>
- [Dynamic Skill Manager on ClawHub](https://clawhub.ai/welkeyever/dynamic-skill-manager) <br>
- [OpenClaw project homepage](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text CLI output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify a local skill registry, usage log, archive metadata, and installed skill directories under ~/.openclaw/workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
