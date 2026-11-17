## Description:

Control Ecovacs FAMIBOT pet robots via the Open Platform Access Key and POST /robot/skill/pet/cmd for device discovery, state queries, everyday settings, display and sound actions, single motions, and the showcase_custom dance preset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ecovacs-ai](https://clawhub.ai/user/ecovacs-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and integrators use this skill to let an agent operate supported Ecovacs FAMIBOT pet robots by reading device state, adjusting routine settings, playing built-in sounds, running motions, and sending the documented showcase dance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an Ecovacs Open Platform Access Key that can authorize pet-robot control.

Mitigation: Prefer ECOVACS_AK environment injection, avoid persistent set-ak storage when possible, and protect or delete ~/.ecovacs_session.json if local storage is used.

Risk: The skill can trigger physical movement, repeated sounds, device reset, scheduling, and camera or microphone state changes.

Mitigation: Require clear user intent before sensitive actions, start with read-only get commands for verification, and review commands before execution.

Risk: A custom ECOVACS_PORTAL_URL could route requests to an untrusted gateway.

Mitigation: Use only official HTTPS Ecovacs gateways unless the alternate endpoint is explicitly trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ecovacs-ai/skills/ecovacs-skills-pet-control)
- [Ecovacs Mainland China Open Platform](https://open.ecovacs.cn/)
- [Ecovacs Non-China Open Platform](https://open.ecovacs.com/)
- [API Reference](references/api.md)
- [Pet Schema Notes](references/schema.md)
- [Phoenix Single Action](references/phoenix-single-action.md)
- [Phoenix Action Control](references/phoenix-action-control.md)
- [Action Sequence](references/action-sequence.md)
- [Dance Routines](references/dance-routines.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline bash, JSON, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing instructions for Ecovacs Open Platform requests and local helper-script usage.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
