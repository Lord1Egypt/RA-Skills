## Description:

Put this OpenClaw instance under ArtzAIn governance — every host tool call is checked against your own ArtzAIn Decision API before it runs, failing closed on deny, review, or any engine error.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quantumskipper](https://clawhub.ai/user/quantumskipper)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw gateway operators and developers use this skill to connect host tool calls to an ArtzAIn Decision API, apply allow, deny, or review decisions, and configure the gateway integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tool names and arguments are sent to the configured Decision API and recorded in its audit trail.

Mitigation: Keep secrets out of tool arguments and point the gateway only to a trusted ArtzAIn deployment.

Risk: The security review was partial because the release attestation and install-generated package-lock file were unavailable.

Mitigation: Before installing, verify the pinned package version, registry signature, attestation, and package integrity.

Risk: A denied decision, review decision, or API/key error blocks host tool calls.

Mitigation: Check the API endpoint and key, and confirm the review process, before relying on the gateway.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/quantumskipper/skills/artzain)
- [npm package](https://www.npmjs.com/package/@cognexuslabs/openclaw-artzain)
- [ArtzAIn hosted service](https://app.cognexuslabs.ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown instructions with shell commands and a JSON5 configuration example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Version-pinned installation and gateway setup guidance]

## Skill Version(s):

0.2.11 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
