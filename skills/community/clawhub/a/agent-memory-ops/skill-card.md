## Description:

Audit and maintain OpenClaw-style long-term memory. Use for MEMORY.md cleanup, daily-note digestion, duplicate detection, stale-memory review, and promoting durable facts from memory/YYYY-MM-DD.md into curated memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orime](https://clawhub.ai/user/orime)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to audit OpenClaw-style MEMORY.md and memory/*.md files, find duplicate or stale notes, surface follow-ups, and draft durable memory updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown or JSON reports can print selected contents from MEMORY.md and memory/*.md, which may include private or sensitive information.

Mitigation: Treat generated reports as private, review them for secrets or personal information, and avoid placing them in public logs or shared automation.

Risk: Drafted memory candidates may be inappropriate to promote if they are volatile, stale, or sensitive.

Mitigation: Review each candidate before editing curated memory, promote only durable facts, and avoid copying secrets unless the user explicitly asks.

## Reference(s):

- [Agent Memory Ops Playbook](references/playbook.md)
- [ClawHub Skill Page](https://clawhub.ai/orime/skills/agent-memory-ops)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown or JSON reports with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include selected local memory note contents and source line references.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
