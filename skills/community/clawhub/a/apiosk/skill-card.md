## Description:

Apiosk Skill helps agents discover and call pay-per-request APIs through a USDC-funded wallet and Apiosk gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obcraft](https://clawhub.ai/user/obcraft)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to configure a small funded wallet, list available Apiosk APIs, call APIs from shell, Node.js, or Python, and inspect balance and usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a funded crypto wallet and stores private keys in plaintext.

Mitigation: Use a dedicated disposable wallet, keep only small funds in it, do not reuse an existing wallet, and move production use to hardware-wallet or external key-management controls.

Risk: The documented dependency installer uses a curl-to-shell pattern.

Mitigation: Review the installer independently and install Foundry through a verified channel before running wallet or balance scripts.

Risk: Automatic-payment behavior is not fully proven by the shipped clients.

Mitigation: Treat x402 payment claims as unverified until signed authorization and enforceable spending limits are confirmed in the client and gateway.

Risk: Requests are sent through a third-party API gateway.

Mitigation: Avoid sending sensitive data through the gateway and test with low-value requests before broader use.

## Reference(s):

- [Apiosk Skill on ClawHub](https://clawhub.ai/obcraft/skills/apiosk)
- [Apiosk Website](https://apiosk.com)
- [Apiosk Documentation](https://docs.apiosk.com)
- [Apiosk Dashboard](https://dashboard.apiosk.com)
- [Security Policy](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell, JavaScript, and Python examples plus JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands and helper-client guidance for wallet setup, API discovery, paid API calls, balance checks, and usage reports.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
