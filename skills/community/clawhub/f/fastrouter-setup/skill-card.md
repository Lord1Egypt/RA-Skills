## Description:

Adds the FastRouter AI provider to OpenClaw, fetches available text and vision models from the FastRouter API, and updates the user's provider configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vamsimnet](https://clawhub.ai/user/vamsimnet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure FastRouter as a model provider, refresh the available FastRouter model list, and make those models selectable in OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill replaces the existing FastRouter provider block while refreshing models.

Mitigation: Review existing custom FastRouter settings before running the skill and preserve any settings that should remain.

Risk: Restarting the OpenClaw gateway can briefly interrupt service.

Mitigation: Approve the gateway restart only when a short interruption is acceptable.

## Reference(s):

- [FastRouter API base URL](https://api.fastrouter.ai)
- [FastRouter models endpoint](https://api.fastrouter.ai/v1/models)
- [ClawHub skill page](https://clawhub.ai/vamsimnet/skills/fastrouter-setup)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands]

**Output Format:** [Markdown with JSON configuration and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OpenClaw provider configuration changes and a short user-facing setup report.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
