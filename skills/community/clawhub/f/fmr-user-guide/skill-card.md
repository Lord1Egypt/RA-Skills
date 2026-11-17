## Description:

Guides agents through Free Model Router installation, upgrades, migration, agent harness integration, provider key setup, model and channel switching, troubleshooting, data security questions, and runtime capability discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laodao-agent](https://clawhub.ai/user/laodao-agent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate Free Model Router: installing or upgrading it, connecting OpenAI- or Anthropic-compatible agent harnesses, managing provider keys and model routing, troubleshooting local service issues, and answering data-security questions from runtime evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation flow can execute remote installer scripts from freemodel.eu.org.

Mitigation: Review the install path first and prefer downloading, inspecting, and verifying installer scripts before running them locally.

Risk: Provider API keys and the device key are sensitive, and provider keys may be stored locally in plaintext configuration.

Mitigation: Avoid sharing real keys in logs or chats, use the admin UI when appropriate, and treat local file permissions as part of key protection.

Risk: Remote exposure of the local router can carry authentication and transport risks, including plaintext HTTP and limited per-client credential separation.

Mitigation: Keep the router bound locally unless remote access is necessary, warn users before rebinding, and avoid exposing unregistered or unauthenticated endpoints publicly.

Risk: The guide includes local mutation paths for router settings and provider state.

Mitigation: Use runtime probes, version checks, backups, and read-back verification before and after configuration changes.

## Reference(s):

- [Server-resolved source repository](https://github.com/laodao-agent/fmr-user-guide)
- [ClawHub skill page](https://clawhub.ai/laodao-agent/skills/fmr-user-guide)
- [Skill definition](SKILL.md)
- [Installation guide](references/chapters/install.md)
- [Agent harness access guide](references/chapters/access.md)
- [Usage guide](references/chapters/usage.md)
- [Security and data-flow guide](references/chapters/security.md)
- [Troubleshooting guide](references/chapters/troubleshoot.md)
- [Data file map and write permissions](references/data/data-map.md)
- [Provider registration flow](references/data/provider-registration.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, REST API calls, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may guide local service operations and configuration changes; provider API keys and device keys should be treated as sensitive.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
