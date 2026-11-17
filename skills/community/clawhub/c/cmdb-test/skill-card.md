## Description:

Automates IMyFone CMDB test-environment release requests for selected applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azimao](https://clawhub.ai/user/azimao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release operators use this skill to submit IMyFone CMDB test-environment releases for a named application, using the fixed release2 branch and the 香港-通用-测试 environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to create a real CMDB test-environment release request.

Mitigation: Install and run it only for users authorized to submit IMyFone CMDB test releases.

Risk: A wrong application name, branch, or environment could submit an unintended release request.

Mitigation: Before the final confirmation click, verify the application name, fixed release2 branch, and 香港-通用-测试 environment.

## Reference(s):

- [IMyFone CMDB release page](https://cmdb.imyfone.club/#/cicd/release)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown or plain text status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CMDB account and user confirmation of the application, branch, and test environment before submission.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
