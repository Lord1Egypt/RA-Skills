## Description:

AuthLock provides TOTP-bound secret protection for passwords, certificates, keys, and other sensitive data through a local command-line vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnluicn](https://clawhub.ai/user/johnluicn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use AuthLock to seal, locate, list, decrypt, and optionally route secrets for short-lived operational use while requesting a current TOTP code for each decryption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles high-value secrets and the security evidence flags misleading protection boundaries.

Mitigation: Require manual review before use, keep vault paths tightly scoped, and do not treat stored configuration as strong protection if the vault directory is exposed.

Risk: The artifact supports decrypted output to files and execution through an --exec path.

Mitigation: Avoid --exec, write decrypted material only to explicit low-risk paths, and prefer short-lived in-memory use without echoing plaintext.

Risk: Decryption depends on TOTP and optional PIN handling.

Mitigation: Request a fresh TOTP code for each decryption, avoid caching codes, and review time synchronization and PIN requirements before operational use.

## Reference(s):

- [AuthLock ClawHub skill page](https://clawhub.ai/johnluicn/skills/authlock)
- [johnluicn ClawHub publisher profile](https://clawhub.ai/user/johnluicn)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command-line examples and local CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write encrypted vault files, decrypted output files, or temporary execution files when invoked through the bundled CLI.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
