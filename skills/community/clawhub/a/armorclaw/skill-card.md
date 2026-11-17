## Description:

ArmorClaw is a local secrets manager for OpenClaw agents that stores API keys, tokens, and credentials in an encrypted vault instead of plain-text .env files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supertechgod](https://clawhub.ai/user/supertechgod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use ArmorClaw to manage local credentials for OpenClaw agents, migrate .env entries into a vault, inject secrets into runtime environments, and audit which skills access stored credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says ArmorClaw's security claims are stronger than the implementation and stored credentials may be exposed in ways users do not expect.

Mitigation: Review carefully before installing and do not treat it as a high-assurance vault unless the reported crypto fallback, password verifier, config-file permissions, and per-skill access model issues are fixed.

Risk: The artifact can use a less battle-tested cryptography fallback when the optional cryptography dependency is unavailable.

Mitigation: Install with the real cryptography dependency and avoid relying on the fallback for sensitive credentials.

Risk: Bot auto-unlock, plaintext export, and storing ARMORCLAW_PASSWORD in configuration can expose the master password or decrypted secrets.

Mitigation: Avoid bot auto-unlock and plaintext export for sensitive vaults, do not store ARMORCLAW_PASSWORD in config, and keep vault and config files tightly permissioned.

Risk: Environment injection and cross-skill secret sharing can make more credentials available to an agent process than intended.

Mitigation: Prefer retrieving only required keys, restrict which skills can access secrets, and review access logs for unexpected reads.

Risk: Static-IP lock mode can lock users out when their external IP changes.

Mitigation: Use IP restriction only with a confirmed static external IP and choose a less brittle lock mode for dynamic home or mobile networks.

## Reference(s):

- [ArmorClaw ClawHub listing](https://clawhub.ai/supertechgod/skills/armorclaw)
- [PHRAIMWORK website](https://phraimwork.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may involve local vault setup, credential import, runtime environment injection, and access-log review.]

## Skill Version(s):

1.0.0 (source: evidence release metadata, SKILL.md metadata, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
