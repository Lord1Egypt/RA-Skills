## Description:

Validate OpenClaw gateway configuration changes before applying them to production.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loopintoai](https://clawhub.ai/user/loopintoai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to validate OpenClaw gateway provider, model, API key, and related configuration changes before production rollout. It checks config syntax, provider connectivity, and model availability, then reports whether the change should be applied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider API keys may be transmitted to configurable provider endpoints during validation.

Mitigation: Use only trusted gateway configs and trusted provider endpoints, and avoid validating untrusted baseUrl changes with real API keys.

Risk: Applying a validated file can replace production gateway configuration and trigger a gateway restart.

Mitigation: Review the exact config file, confirm the backup location, and run the apply step only when prepared for production impact.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status messages with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform provider API connectivity checks and advise whether changes should be applied.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
