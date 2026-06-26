## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blockcloud](https://clawhub.ai/user/blockcloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding-agent users use this skill to record corrections, command failures, feature requests, and durable lessons in markdown files so future sessions can reuse validated learnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs can retain conversation, prompt, or error details and carry them into future agent memory. <br>
Mitigation: Keep logs private, avoid storing secrets or raw prompts, and redact error output before saving it. <br>
Risk: Unreviewed learning entries can promote incorrect or misleading guidance into future agent instruction files. <br>
Mitigation: Review every entry before promotion and scan the skill before deployment. <br>
Risk: Global every-prompt hooks and cross-session sharing can increase privacy exposure. <br>
Mitigation: Avoid global hooks unless needed and use transcript or messaging tools only with explicit approval and sanitized summaries. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to create or update .learnings markdown files and optional hook configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
