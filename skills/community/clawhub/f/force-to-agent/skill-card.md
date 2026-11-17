## Description:

Extract AGENTS.md, SOUL.md, TOOLS.md, and an optional openclaw.json patch from pasted custom-GPT markdown, then create a new workspace-<agent> folder and write the files there instead of overwriting the current workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nga-khan](https://clawhub.ai/user/nga-khan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn pasted custom-GPT or FORCE conversion markdown into a separate OpenClaw workspace containing AGENTS.md, SOUL.md, TOOLS.md, and any optional openclaw.json patch candidate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted agent bootstrap files may shape future agent behavior if the generated workspace is used without review.

Mitigation: Review AGENTS.md, SOUL.md, TOOLS.md, and any openclaw.json snippet before using the generated workspace.

Risk: Incomplete or ambiguous pasted markdown may produce missing file candidates or conflicting agent definitions.

Mitigation: Use the skill's validation and conflict handling to request missing files or clearer source material before saving a workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nga-khan/skills/force-to-agent)

## Skill Output:

**Output Type(s):** [files, markdown, configuration, guidance]

**Output Format:** [Markdown files and optional JSON patch guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a separate workspace folder and reports concise generated paths and results.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
