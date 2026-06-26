## Description: <br>
Provides an agent execution framework with tool-risk classification, context-budget monitoring, execution modes, lifecycle hooks, and framework status commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xjhveteran199-bit](https://clawhub.ai/user/xjhveteran199-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to structure agent tasks with permission checks, context-budget monitoring, lifecycle hooks, and configurable execution modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approval-required tool calls may continue after only a warning. <br>
Mitigation: Use the skill only for review or in a tightly sandboxed environment until approval handling is changed to fail closed. <br>
Risk: Connecting the framework to real shell, write/delete, browser, messaging, package-install, or network tools could expose high-impact capabilities. <br>
Mitigation: Do not connect those tools unless the approval path is fixed to fail closed and logging or memory behavior is understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xjhveteran199-bit/claude-code-framework) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Default framework configuration](artifact/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured text with code and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe tool risk assessments, context-budget status, execution-mode changes, hook activity, and implementation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
