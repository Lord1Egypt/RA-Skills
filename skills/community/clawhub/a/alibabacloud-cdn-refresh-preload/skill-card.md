## Description:

Read-only diagnostics for Alibaba Cloud CDN refresh and preload issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Alibaba Cloud CDN developers and support engineers use this skill to verify refresh and preload task records, inspect cache behavior, and prepare a diagnosis report when an operation appears ineffective.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags possible unintended file access, local file writes, and leakage of local data despite the skill's read-only diagnostic description.

Mitigation: Prefer a corrected release before production use; evaluate it in an isolated environment without unrelated secrets and use narrowly scoped CDN credentials.

Risk: The supplied UID is informational and does not switch the account selected by the Alibaba Cloud CLI credentials.

Mitigation: Verify the CLI caller identity and configure its default credential chain for the intended account before querying CDN tasks.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sdk-team/skills/alibabacloud-cdn-refresh-preload)
- [CDN cache rules](references/cache-rules.md)
- [RAM policies](references/ram-policies.md)
- [Probe result routing](references/probe-result-routing.md)
- [Diagnostic report template](references/report-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown diagnostic report with evidence and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only diagnostic findings; does not submit refresh or preload jobs.]

## Skill Version(s):

0.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
