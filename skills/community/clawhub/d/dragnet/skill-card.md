## Description:

Generate a Dragnet marketplace profile by scanning an OpenClaw workspace for professional builder signals, producing a structured profile, and signing it for upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unrelatedworks](https://clawhub.ai/user/unrelatedworks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to generate or update a Dragnet marketplace profile that summarizes professional capability signals from their workspace and prepares a signed JSON file for upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads broad private workspace data, including memory, identity, configuration, installed skills, and conversation exports.

Mitigation: Use it only in workspaces intended for profile summarization, inspect every generated field before signing, and exclude raw personal data, secrets, and private conversation content.

Risk: The included signing mechanism is not strong proof of identity or authenticity.

Mitigation: Treat the signature as a Dragnet upload artifact, not as independent identity verification, and verify publisher claims through trusted channels before relying on them.

Risk: The authoritative security verdict is suspicious.

Mitigation: Review the skill carefully before installation and execution, especially its workspace scanning behavior and generated profile contents.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/unrelatedworks/skills/dragnet)
- [Dragnet Marketplace](https://dragnet.unrelated.works)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON profile output and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a dragnet-profile.json file after interactive review and signing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
