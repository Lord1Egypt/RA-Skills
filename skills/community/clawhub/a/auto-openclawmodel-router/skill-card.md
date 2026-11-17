## Description:

Auto Model Router - Automatically select the best model based on task complexity for OpenClaw agents

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmchenggh](https://clawhub.ai/user/hmchenggh)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to classify work into model-routing categories, choose an appropriate model plan, and generate routing guidance for setup, fallback behavior, and sub-agent handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic model and provider switching may route prompts or files to providers the user did not intend to use.

Mitigation: Choose an allowed provider and region plan explicitly, and review provider data-sharing expectations before enabling routing.

Risk: Sub-agent dispatch can branch work or preserve task state without enough user control.

Mitigation: Disable sub-agent creation where possible, or require confirmation before a sub-agent is created for a sudden task.

Risk: Saved configuration and OpenClaw reload behavior can change future task routing broadly.

Mitigation: Review the saved configuration before reloading OpenClaw, keep a backup, and prefer a pinned installer version.

## Reference(s):

- [Project homepage](https://github.com/HMCHENGGH/auto-model-router)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline command examples and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces model-routing choices, setup commands, configuration examples, and fallback guidance for OpenClaw tasks.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
