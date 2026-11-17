## Description:

Periodic self-reflection on recent sessions. Analyzes what went well, what went wrong, and writes concise, actionable insights to the appropriate workspace files. Designed to run as a cron job.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brennerspear](https://clawhub.ai/user/brennerspear)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to review recent OpenClaw sessions and capture concise, actionable lessons in workspace instruction and memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private OpenClaw session transcripts and persist derived guidance into high-trust agent instruction and memory files.

Mitigation: Use a dry-run or review workflow, restrict eligible sessions, redact sensitive content, and require owner approval before edits to AGENTS.md, TOOLS.md, MEMORY.md, or skill files.

Risk: Unattended cron use can preserve sensitive or misleading reflections without timely review.

Mitigation: Disable raw transcript output in cron logs and review generated insights before allowing persistent updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brennerspear/skills/agent-self-reflection)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown updates and concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append or edit workspace instruction, tool, memory, and skill files with bounded session transcript review.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
