## Description: <br>
Lightweight, memory-safe Auto Dream workflow for OpenClaw that consolidates recent notes into existing memory files without replacing the user's current memory structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrgyan](https://clawhub.ai/user/mrgyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to consolidate durable information from recent memory notes into existing long-term and project memory files while preserving the current memory structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may write incorrect, low-value, or sensitive information into long-term memory files if candidate notes are not reviewed carefully. <br>
Mitigation: Run it deliberately, review the memory-file diff before accepting or committing changes, and avoid storing secrets in memory files. <br>
Risk: Optional commit behavior may persist unintended memory changes. <br>
Mitigation: Commit only after confirming the generated memory updates and dream-log entry are accurate. <br>


## Reference(s): <br>
- [Auto Dream Light on ClawHub](https://clawhub.ai/mrgyan/auto-dream-light) <br>
- [Adapted Auto Dream Plan](references/adapted-plan.md) <br>
- [Manual Run Guide](references/manual-run.md) <br>
- [Semi-Automatic Mode](references/semi-auto.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with optional file edits and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update MEMORY.md, memory/projects/**, memory/system/auto-dream-log.md, and daily memory notes when durable information is found.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
