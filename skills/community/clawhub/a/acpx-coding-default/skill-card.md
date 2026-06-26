## Description: <br>
Use direct acpx CLI via exec as the default coding execution path for Codex- and Claude-focused agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoyang78](https://clawhub.ai/user/chaoyang78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to route coding, debugging, refactoring, test-running, and repository tasks through the local acpx CLI with Codex or Claude adapters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes coding work through a local acpx command that runs with the user's normal local permissions. <br>
Mitigation: Use it in repositories you trust and review prompts, commands, and resulting changes before sensitive or destructive work. <br>
Risk: acpx sessions may retain context across related tasks. <br>
Mitigation: Reuse named sessions only when continuity is intended and start a fresh session when task context should be isolated. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with shell command templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an explicit working directory and may reuse named acpx sessions when continued context is useful.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
