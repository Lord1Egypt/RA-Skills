## Description:

Diagnoses Alibaba Cloud OSS endpoint, region, internal-network, and custom-domain access issues using read-only checks and evidence-based guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to diagnose OSS endpoint and region mismatches, internal-network access failures, and custom-domain problems without changing cloud resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The diagnosis inspects caller identity, bucket metadata, and custom-domain DNS and CNAME details.

Mitigation: Use least-privilege credentials limited to sts:GetCallerIdentity, oss:GetBucketInfo, oss:ListBuckets, and oss:ListCname; avoid sharing sensitive report details unnecessarily.

Risk: A failed API check may leave the endpoint or CNAME state unverified.

Mitigation: Report degraded status and the specific limitations instead of treating missing data as a successful check.

Risk: Suggested Alibaba Cloud CLI installation or upgrade may alter the local environment.

Mitigation: Review any suggested CLI installation or upgrade before allowing it.

## Reference(s):

- [Endpoint rules](references/endpoint-rules.md)
- [Diagnosis tree](references/diagnosis-tree.md)
- [Read-only RAM permissions](references/ram-policies.md)
- [Dial-test guidance](references/dial-test-guidance.md)
- [ClawHub skill listing](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-endpoint-internal-diagnosis)

## Skill Output:

**Output Type(s):** [Markdown, Configuration guidance]

**Output Format:** [Markdown diagnosis with status, findings, and next actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports degraded checks and explicitly identifies auto-filled inputs; changes are suggested only, not applied.]

## Skill Version(s):

0.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
