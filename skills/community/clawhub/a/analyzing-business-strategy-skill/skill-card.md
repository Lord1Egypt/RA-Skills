## Description: <br>
Captures learnings, errors, feature requests, and corrections so coding agents can improve recurring workflows over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinuscxj](https://clawhub.ai/user/dinuscxj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrections, command failures, feature requests, and reusable patterns in learning logs. The skill also guides promotion of durable lessons into agent memory and instruction files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist session details in learning logs and agent memory files. <br>
Mitigation: Review each entry before writing or promoting it, and redact secrets, personal data, customer details, raw prompts, and full command output. <br>
Risk: Hooks and promoted memory can influence future agent context and behavior. <br>
Mitigation: Keep hooks project-scoped and opt-in, and require human review before enabling hooks or writing to AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, or Copilot instructions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dinuscxj/analyzing-business-strategy-skill) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command snippets and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update durable learning logs and propose promotion into AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, or Copilot instruction files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
