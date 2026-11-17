## Description:

Change Safeguard guides agents through impact analysis, checklist-based edits, and post-change verification for workspace file, configuration, and script changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidongkl](https://clawhub.ai/user/weidongkl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make file changes more deliberate by requiring impact analysis, a reviewed edit checklist, execution tracking, and final search-based verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may misread or skip the Chinese-language workflow and miss required confirmations before editing files.

Mitigation: Review the workflow before installation and require agents to present the impact checklist for confirmation before edits.

Risk: Workspace changes can leave stale references if the post-edit search verification is skipped.

Mitigation: Require the final search for old and new strings and record the modification summary before completion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/weidongkl/skills/change-safeguard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with checklist tables and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow; requires confirmation before executing listed edits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
