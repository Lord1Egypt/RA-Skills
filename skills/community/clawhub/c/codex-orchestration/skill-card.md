## Description:

General-purpose orchestration for Codex. Uses update_plan plus background PTY terminals to run parallel codex exec workers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanelindsay](https://clawhub.ai/user/shanelindsay)

### License/Terms of Use:


## Use Case:

Developers and technical agents use this skill to split Codex work into planned worker tasks, run parallel reviews or checks, and synthesize verified results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages no-approval background workers that can run commands, use web search, and make scoped file edits.

Mitigation: Use explicit approval gates for web searches, destructive commands, writes outside intended workspace paths, and long-running or persistent worker processes.

Risk: Parallel workers can create conflicting recommendations or overlapping edits if their scopes are not controlled.

Mitigation: Keep worker tasks read-only by default, use one writer per artifact, and have the orchestrator review synthesized output before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shanelindsay/skills/codex-orchestration)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with inline shell commands and worker prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce background worker commands, plans, synthesized findings, and verification notes.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
