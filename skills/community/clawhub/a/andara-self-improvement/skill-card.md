## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atiati82](https://clawhub.ai/user/atiati82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to capture command failures, user corrections, missing capabilities, outdated assumptions, and reusable improvements as structured markdown records. The records can later be reviewed and promoted into project or agent memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent self-improvement records can capture sensitive conversation details, command output, secrets, tokens, or environment information. <br>
Mitigation: Keep hooks project-scoped where possible, review hook scripts before enabling them, and do not store secrets, tokens, private transcripts, raw command output, or sensitive environment details in learning files. <br>
Risk: Unreviewed learnings promoted into agent memory can influence future behavior with incorrect or overly broad guidance. <br>
Mitigation: Require manual review before writing to .learnings or promoting entries into AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or Copilot instructions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/atiati82/andara-self-improvement) <br>
- [Publisher Profile](https://clawhub.ai/user/atiati82) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured entry templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent learning, error, and feature-request records when the agent follows the documented workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
