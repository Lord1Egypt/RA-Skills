## Description:

Helps OpenClaw Feishu group chat operators route bot replies into message threads instead of the main chat stream.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arianxx](https://clawhub.ai/user/arianxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to check and apply local Feishu thread-reply patches when setting up Feishu group chats or after openclaw-lark updates overwrite local changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directly edits installed OpenClaw plugin and Feishu live-card files, which may affect an important or shared OpenClaw instance.

Mitigation: Run the check-only commands first, make an independent backup of target files, and test on a non-critical instance before applying changes.

Risk: Local patches can be overwritten or become incompatible after upstream OpenClaw or openclaw-lark updates.

Mitigation: Re-run status checks after updates and review changed upstream files before reapplying the patches.

Risk: Heartbeat auto-reapply can maintain local patches without manual review.

Mitigation: Use heartbeat automation only where local patch maintenance is acceptable, and require review plus a gateway restart after reapplication.

## Reference(s):

- [How Feishu Group Thread Reply Works](references/how-it-works.md)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and patch scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes check-only commands and local OpenClaw patch guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
