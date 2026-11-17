## Description:

Review and finalize configuration topics through a structured item-by-item confirmation flow that inventories in-scope settings, records decisions, and requires a final explicit pre-apply confirmation before any real configuration change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silronin](https://clawhub.ai/user/silronin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and operators use this skill to run a structured review of configuration choices before changing real systems. It is intended for multi-item configuration reviews that need source-backed inventory, item-by-item decisions, tracking in Markdown, and a mandatory final apply confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can produce recommendations that affect real configuration behavior if later applied.

Mitigation: Keep the review scope narrow, verify the source-backed inventory and final summary, and require a fresh explicit confirmation before any real configuration change.

Risk: The skill may write a local Markdown tracking file while documenting the review.

Mitigation: Review the tracking file for sensitive configuration details and keep it within the intended workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/silronin/skills/config-review-flow)
- [Publisher profile](https://clawhub.ai/user/silronin)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown review inventory, per-item decisions, summaries, and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local configuring/ Markdown tracking file during the review workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
