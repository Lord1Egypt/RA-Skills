## Description:

Put this OpenClaw instance under ArtzAIn governance — every host tool call is checked against your own ArtzAIn Decision API before it runs, failing closed on deny, review, or any engine error.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quantumskipper](https://clawhub.ai/user/quantumskipper)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw administrators and developers use this skill to install and configure ArtzAIn Tool Gate so host tool calls receive an allow, deny, or human-review decision from their ArtzAIn Decision API before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tool names, arguments, and agent IDs are sent to the configured Decision API and recorded in its audit trail; arguments may contain sensitive data.

Mitigation: Keep secrets out of tool arguments and point baseUrl to a deployment you trust.

Risk: A key associated with another ArtzAIn account can send decisions to that account, while configuration errors or API failures block tool calls.

Mitigation: Use a Decision key for the intended account and verify the endpoint and key before enabling the gate.

Risk: The security review reports no findings but notes unresolved references and unverified external links, leaving some evidence incomplete.

Mitigation: Review the package and links before installation, and verify the package signature and attestation as the instructions describe.

## Reference(s):

- [ArtzAIn Tool Gate npm package](https://www.npmjs.com/package/@cognexuslabs/openclaw-artzain)
- [Repository cited by the listing](https://github.com/CogNEXUSlabs/cognexus-tools)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell commands and JSON5 configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes version-pinned installation and setup instructions.]

## Skill Version(s):

0.2.10 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
