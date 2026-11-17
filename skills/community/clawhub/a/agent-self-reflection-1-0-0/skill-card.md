## Description:

Periodic self-reflection on recent sessions. Analyzes what went well, what went wrong, and writes concise, actionable insights to the appropriate workspace files. Designed to run as a cron job.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrhenghu](https://clawhub.ai/user/mrhenghu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to periodically review recent OpenClaw sessions, extract specific lessons, and route concise insights into workspace memory, tool notes, agent instructions, or skill documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads recent private OpenClaw session history, including direct and group sessions.

Mitigation: Use only when transcript access is acceptable, restrict eligible sessions, keep reads bounded to recent tails, and redact secrets or personal data before retaining insights.

Risk: Transcript-derived summaries can change future agent behavior by writing to memory, agent instructions, tool notes, or skill documentation.

Mitigation: Run with a dry-run or review workflow and require approval before changes to AGENTS.md, TOOLS.md, MEMORY.md, memory files, or any SKILL.md file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrhenghu/skills/agent-self-reflection-1-0-0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown summary with targeted file edits and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads bounded recent session tails and returns a brief 2-4 sentence summary after writing any selected insights.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
