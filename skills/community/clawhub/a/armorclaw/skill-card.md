## Description: <br>
AES-256 encrypted secrets manager for OpenClaw agents that stores API keys, tokens, and credentials in a local vault instead of plain-text .env files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SuperTechGod](https://clawhub.ai/user/SuperTechGod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use ArmorClaw to store, retrieve, import, and audit secrets used by OpenClaw agents. It is intended for securing API keys, migrating from .env files, sharing secrets across skills, and reviewing credential access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flags ArmorClaw as requiring review because its credential-handling claims may not match several high-impact behaviors. <br>
Mitigation: Review the credential-handling tradeoffs before installation and use the secure dependency path for production-like use. <br>
Risk: Bot auto-unlock and ARMORCLAW_PASSWORD can expose the master password or make unattended access easier than expected. <br>
Mitigation: Avoid bot auto-unlock and ARMORCLAW_PASSWORD storage unless the environment is tightly controlled and the access model is explicitly accepted. <br>
Risk: Bulk environment injection, broad .env scanning, and export back to .env can expose secrets to processes or plaintext files that should not receive them. <br>
Mitigation: Inject only the secrets needed by trusted processes, limit .env scanning to explicit paths, and treat exported .env files as temporary plaintext that must be protected and removed. <br>


## Reference(s): <br>
- [ArmorClaw on ClawHub](https://clawhub.ai/SuperTechGod/armorclaw) <br>
- [PHRAIMWORK](https://phraimwork.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with CLI commands, Python snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local vault operations, environment-injection patterns, and audit/reporting workflows for agent secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md metadata, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
