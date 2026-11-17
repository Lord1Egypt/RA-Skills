## Description:

OpenClaw pet companion skill. Manage adopted pets, run interactions, and produce pet image prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yazelin](https://clawhub.ai/user/yazelin)

### License/Terms of Use:


## Use Case:

External users and agents use clawpet to adopt and manage virtual pets, check pet status, run care interactions, and prepare photorealistic pet image prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch and run unpinned code from the referenced GitHub repository.

Mitigation: Install only after reviewing the referenced source, and prefer a pinned, reviewed release or commit.

Risk: Generated pet images may be sent through Telegram.

Mitigation: Require user confirmation before sending media, and verify the recipient channel and file path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yazelin/skills/clawpet)
- [clawpet GitHub package](https://github.com/yazelin/clawpet.git)
- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and plain-text image prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to generate pet image prompts and send generated images through Telegram after confirmation.]

## Skill Version(s):

0.1.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
