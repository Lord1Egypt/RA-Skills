## Description: <br>
Records agent learnings, errors, user corrections, feature requests, and better practices so future sessions can review and promote durable knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AndyLue](https://clawhub.ai/user/AndyLue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent operators use this skill to maintain a persistent learning loop across agent sessions. It guides agents to log corrections, command failures, feature requests, knowledge gaps, and reusable practices into project memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning files can capture conversation details, command output, or errors that include sensitive information. <br>
Mitigation: Keep .learnings private or gitignored by default, and do not store secrets, credentials, customer data, raw prompts, or sensitive command parameters in these files. <br>
Risk: Hook-based reminders and error detection may run during agent workflows and surface tool output into persistent logging decisions. <br>
Mitigation: Enable hooks only intentionally, review hook configuration before use, and keep hook output limited to reminders rather than automatic commits or promotions. <br>
Risk: Promoting logged entries into shared memory files or new skills can spread incorrect, stale, or sensitive content. <br>
Mitigation: Require human review before committing logs or promoting content into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or new skills. <br>


## Reference(s): <br>
- [Agent Setup Guide](references/agent-setup.md) <br>
- [OpenClaw Integration Guide](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Skill Extraction Guide](references/skill-extraction.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [ClawHub Skill Page](https://clawhub.ai/AndyLue/ai-self-evolution) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and structured file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .learnings Markdown files and promote selected entries to CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or new skill files when the agent follows the workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
