## Description:

Generate passwords, PINs, and memorable passphrases with configurable command-line options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can use this skill to ask an agent for command-line generation of passwords, PINs, and memorable passphrases for testing or low-risk workflows. Generated secrets should not be used for real accounts until the security guidance is addressed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated passwords, PINs, and passphrases may not provide the security level promised by the skill documentation.

Mitigation: Use generated values only for testing or low-risk workflows until the generator uses a cryptographically secure RNG and fixes passphrase entropy.

Risk: The documentation and CLI behavior may lead users to assume stronger defaults or secure-token support than the artifact provides.

Mitigation: Review the command options and generated output before use, and update documentation or implementation before relying on the skill for real secrets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/skills/dinghaibin-password-generator)
- [ClawHub Publisher Profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text generated values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate one or more password, PIN, or passphrase strings; security guidance says not to trust generated secrets for real accounts until randomness and entropy issues are fixed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
