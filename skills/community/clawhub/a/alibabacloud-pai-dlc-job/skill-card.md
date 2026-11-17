## Description:

Alibaba Cloud PAI-DLC job management skill for distributed training job CRUD, monitoring logs and events, and GPU sanity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML platform engineers use this skill to manage Alibaba Cloud PAI-DLC distributed training jobs, inspect job state, retrieve logs and events, discover required AIWorkSpace resources, and verify GPU health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact cloud job operations, including stopping jobs, opening web terminals, and generating sharing tokens.

Mitigation: Require explicit user approval before high-impact operations, present current job status before stop actions, and prefer read-only or least-privilege RAM permissions when full job management is not required.

Risk: The skill relies on the user's configured Aliyun profile, which may have broad access to Alibaba Cloud resources.

Mitigation: Configure credentials outside the agent session, avoid pasting secrets into commands, and use short-lived credentials or scoped roles where available.

Risk: PAI-DLC create operations do not expose a client-token, so retries after network failures can create duplicate jobs.

Mitigation: Before reissuing a failed create request, list jobs by display name to detect a previously committed job.

## Reference(s):

- [PAI-DLC API and CLI Reference](references/related-apis.md)
- [PAI-DLC RAM Permission Policies](references/ram-policies.md)
- [PAI-DLC Operation Verification Methods](references/verification-method.md)
- [Job Lifecycle Management](references/job-management.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target Aliyun CLI workflows and should preserve the documented session User-Agent, timeout, confirmation, and least-privilege guidance.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
