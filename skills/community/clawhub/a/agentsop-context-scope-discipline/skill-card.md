## Description:

Helps coding agents keep editable file context small by separating read-only exploration from files that will actually be edited, monitoring a roughly 25k-token working-file budget, and dropping files after edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentsope](https://clawhub.ai/user/agentsope)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users apply this skill during multi-file edits to decide which files belong in the editable working set, which should stay read-only, and when to drop or split work to avoid context dilution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advisory and may cause an agent to omit relevant context if it classifies the editable working set too narrowly.

Mitigation: Use repo-map, search, or read-only references to verify candidate files before editing, and add files when they will actually be changed.

Risk: The guide is primarily Chinese-language and uses Aider-oriented command examples generalized across coding-agent harnesses.

Mitigation: Map /add, /read, /drop, and /tokens to the target agent's equivalent controls before applying the workflow.

Risk: The 25k-token budget is an empirical warning signal rather than a hard limit for every model or task.

Mitigation: Treat wrong-file edits, truncation, and missed targets as triggers to drop files, shrink read-only context, or split the task earlier.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentsope/skills/agentsop-context-scope-discipline)
- [R1 source evidence](references/R1-source-evidence.md)
- [Aider edit errors troubleshooting](https://aider.chat/docs/troubleshooting/edit-errors.html)
- [Aider token limits troubleshooting](https://aider.chat/docs/troubleshooting/token-limits.html)
- [Aider repo map documentation](https://aider.chat/docs/repomap.html)
- [Aider SWE-Bench Lite repo-map analysis](https://aider.chat/2024/05/22/swe-bench-lite.html)
- [Aider edit formats documentation](https://aider.chat/docs/more/edit-formats.html)
- [Aider commands documentation](https://aider.chat/docs/usage/commands.html)
- [Aider conventions documentation](https://aider.chat/docs/usage/conventions.html)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown prose with inline command examples and decision tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory workflow output; the skill itself does not execute commands or access data.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
