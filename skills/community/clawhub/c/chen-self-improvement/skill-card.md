## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture corrections, command failures, missing capabilities, and recurring best practices as durable learning records. The records can later be reviewed, resolved, promoted to project memory, or converted into reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning files and shared memory targets can retain sensitive, personal, customer, or credential material if agents log raw context without review. <br>
Mitigation: Do not store secrets, credentials, private transcripts, personal data, customer data, or raw command output in learning files; review and redact entries before saving or sharing them. <br>
Risk: Hook-based reminders can make the skill active across sessions or projects and can promote broad context-sharing patterns. <br>
Mitigation: Keep hooks project-scoped, avoid global always-on hook configuration unless the scripts have been reviewed, and install the skill only when durable agent memory is intended. <br>
Risk: Promoting entries into AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, MEMORY.md, or Copilot instructions can introduce incorrect or misleading guidance into future sessions. <br>
Mitigation: Require manual review before any learning is promoted to shared memory or cross-session instruction files. <br>


## Reference(s): <br>
- [Chen Self Improvement on ClawHub](https://clawhub.ai/cs995279497-byte/chen-self-improvement) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, hook code, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces durable learning entries and optional hook reminders; users should review entries before promoting them to shared memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
