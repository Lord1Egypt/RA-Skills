## Description:

Build high-performing OpenClaw agents end-to-end, including persona, operating rules, required workspace files, guardrails, autonomy model, heartbeat plan, and skill roster.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced agent builders use this skill to interview for requirements, generate OpenClaw workspace files, add safety guardrails, and iterate on existing agent behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agent workspaces may grant too much autonomy or unclear destructive-action boundaries.

Mitigation: Review autonomy level, ask-before-destructive rules, outbound-message rules, and loop breakers before using generated files.

Risk: Referenced template files are not present in the submitted artifact, which may make generated output less standardized.

Mitigation: Supply or verify the referenced OpenClaw workspace and template materials before relying on generated agent files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/agent-builder1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown workspace files with concise guidance and acceptance-test prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OpenClaw files such as IDENTITY.md, SOUL.md, AGENTS.md, USER.md, HEARTBEAT.md, optional memory files, and targeted diffs for existing agents.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
