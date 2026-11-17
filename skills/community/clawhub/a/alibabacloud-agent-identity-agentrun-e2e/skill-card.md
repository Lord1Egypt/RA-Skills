## Description:

Guides developers through deploying and testing an Alibaba Cloud AgentRun agent with AgentIdentity authentication and tool authorization, then cleaning up trial resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to set up a test identity provider, deploy an AgentRun sample, verify sign-in and tool authorization behavior, and clean up test resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports concerns with token audience validation.

Mitigation: Verify that test tokens are intended for the target service and exercise the workflow with a test identity.

Risk: The security summary reports authorization-control weaknesses.

Mitigation: Use a test account and confirm both permitted and denied tool operations before relying on the configuration.

Risk: The security summary reports cleanup safeguards as an area of concern.

Mitigation: Review the cleanup plan and resource list before running cleanup, especially when reusing an existing Runtime.

Risk: One shared script was only partially analyzed by the scanners.

Mitigation: Review the shared script before running it with cloud credentials or on an account containing important resources.

## Reference(s):

- [Alibaba Cloud Agent Identity development kit](https://github.com/aliyun/agent-identity-dev-kit)
- [AgentRun deployment guide](references/agentrun-deploy.md)
- [Testing checklist](references/testing-checklist.md)
- [RAM policies and permissions](references/ram-policies.md)
- [Cleanup guide](references/cleanup.md)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Code, Testing guidance]

**Output Format:** [Markdown guidance with inline Bash commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive deployment and verification workflow that may create and clean up Alibaba Cloud test resources.]

## Skill Version(s):

0.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
