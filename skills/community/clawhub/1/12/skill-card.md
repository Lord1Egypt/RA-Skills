## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[china-mobile2008](https://clawhub.ai/user/china-mobile2008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture corrections, failed operations, knowledge gaps, and recurring workflow improvements so future sessions can reuse them as project memory or skill updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Learning logs can persist sensitive project context, private transcript details, or user corrections into future agent prompts. <br>
Mitigation: Keep logs project-local where possible, redact secrets and private transcript details, and require explicit review before promoting entries into AGENTS.md, SOUL.md, TOOLS.md, MEMORY.md, CLAUDE.md, or Copilot instructions. <br>
Risk: Broad hooks, cross-session transcript reading, session messaging, and sub-agent spawning can expand context sharing beyond the user's intent. <br>
Mitigation: Do not enable global hooks by default, and use transcript access, session messaging, and sub-agent spawning only with clear user intent. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [ClawHub Skill Page](https://clawhub.ai/china-mobile2008/12) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration examples, and learning-log file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-local learning entries and optional hook configuration guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
