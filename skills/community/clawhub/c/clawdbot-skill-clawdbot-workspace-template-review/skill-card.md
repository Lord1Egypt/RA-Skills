## Description:

Compare a Clawdbot workspace against the official templates installed with Clawdbot (npm or source) and list missing sections to pull in, especially after upgrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xadenryan](https://clawhub.ai/user/xadenryan)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to compare local Clawdbot workspace Markdown files against official Clawdbot templates after installation or upgrades. It helps identify missing sections, explain why they matter, and decide whether to add them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent reads local Clawdbot workspace Markdown files and official template files as part of the comparison workflow.

Mitigation: Review the diff output and proposed additions before approving any workspace file changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xadenryan/skills/clawdbot-skill-clawdbot-workspace-template-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with file paths, missing section excerpts, explanations, questions, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports missing sections from official templates and asks before additions are made.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
