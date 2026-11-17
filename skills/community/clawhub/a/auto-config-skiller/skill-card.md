## Description:

Provides one-click environment initialization, core skill installation, and configuration for OpenClaw users to streamline setup and dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhongchen](https://clawhub.ai/user/wuhongchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to diagnose a fresh OpenClaw environment, install core skills and dependencies, configure Feishu and LLM settings, and optionally add an agent persona.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may run mutable remote installers and install broad, unpinned components.

Mitigation: Review each external source first and run the setup only in a disposable or low-privilege environment.

Risk: The generated .env file may contain API keys or service credentials.

Mitigation: Protect the generated file, avoid using sensitive production credentials during evaluation, and rotate keys if exposure is suspected.

Risk: Downloaded persona text may be reused as a system prompt without review.

Mitigation: Manually review and pin any persona content before using it as agent instructions.

## Reference(s):

- [Usage Guide](docs/USAGE_GUIDE.md)
- [ClawHub Skill Page](https://clawhub.ai/wuhongchen/skills/auto-config-skiller)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and generated local configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update local OpenClaw skill directories, .env configuration, and persona.md during setup.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
