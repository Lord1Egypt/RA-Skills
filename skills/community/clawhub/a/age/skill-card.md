## Description:

Age is an age file encryption reference covering key generation, X25519 encryption, SSH key support, passphrase mode, pipe patterns, SOPS integration, YubiKey plugins, and security considerations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and security-conscious operators use this skill as an age file encryption reference for key generation, encryption and decryption workflows, secret-sharing recipes, plugin choices, and security limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example commands may include sensitive paths, private keys, .env files, recipient lists, and cloud bucket destinations.

Mitigation: Review and adapt each path, recipient, key, local file, and bucket destination before running or asking an agent to run the examples.

Risk: Encryption guidance can be misapplied if recipients, identity files, or passphrase choices are wrong.

Mitigation: Verify recipient keys and identity files, use strong passphrases where passphrase mode is chosen, and test decryption before relying on encrypted backups or shared secrets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ckchzh/skills/age)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown-style command reference with shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command-specific sections cover intro, key generation, encryption, decryption, recipes, plugins, and security.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
