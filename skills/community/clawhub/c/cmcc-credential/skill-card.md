## Description:

Helps an agent load China Mobile Digital Credential app credentials, bind the agent, and request user authorization before sensitive operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riceankim](https://clawhub.ai/user/riceankim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add a CMCC Digital Credential approval step before destructive actions, secret access, or other sensitive agent operations. It supports credential setup, agent binding, authorization-link generation, and polling for approval status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles app secrets and phone numbers.

Mitigation: Use it only in a controlled workspace, restrict access to the memory directory, avoid committing stored credentials, and rotate exposed appKey values.

Risk: The security evidence says the skill should not be treated as a strong approval boundary for high-impact operations.

Mitigation: Require independent human review and platform-native access controls before destructive actions or secret disclosure.

Risk: The helper scripts call an external CMCC credential service and may poll for up to ten minutes.

Mitigation: Confirm endpoint suitability, network permissions, phone-number handling, and timeout behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/riceankim/skills/cmcc-credential)
- [Publisher profile](https://clawhub.ai/user/riceankim)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce credential-status JSON, authorization record IDs, and authorization URLs when its helper scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
