## Description:

Provides file encryption, password hashing, encryption algorithm selection guidance, and basic compliance checks for developers protecting sensitive data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to choose encryption approaches, encrypt or decrypt files with command-line tools, hash passwords, and run basic crypto-related code checks on systems and repositories they control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands proposed by the skill can permanently delete original files after encryption.

Mitigation: Require explicit confirmation before destructive commands, keep backups, and verify decrypted output before removing originals.

Risk: The skill may handle keys, passwords, hashes, tokens, or decrypted sensitive data.

Mitigation: Avoid printing secrets into chat or logs and prefer environment variables or a dedicated secret manager for key material.

Risk: Broad security and network checks can run against unintended paths or domains.

Mitigation: Limit execution to files, repositories, and domains the user controls, and review command scope before running.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, Python, JavaScript, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that modify or delete files; outputs should avoid exposing keys, passwords, hashes, tokens, or decrypted sensitive data.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
