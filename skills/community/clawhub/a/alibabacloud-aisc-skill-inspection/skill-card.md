## Description:

Submits Skill archives to Alibaba Cloud AISC for security scanning, polls task results, and explains findings and scan errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to submit Skill archive URLs for Alibaba Cloud AISC checks, track scan completion, and interpret reported security findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill archive URLs and contents are submitted to Alibaba Cloud AISC for scanning.

Mitigation: Submit private archives only when that data flow is acceptable.

Risk: The scan uses the user's configured Alibaba Cloud credentials.

Mitigation: Use a least-privilege RAM identity limited to the documented AISC actions.

Risk: Unpinned dependencies may reduce reproducibility.

Mitigation: Pin dependency versions when stricter reproducibility is required.

## Reference(s):

- [Published Skill](https://clawhub.ai/sdk-team/skills/alibabacloud-aisc-skill-inspection)
- [RAM Permissions](references/ram-policies.md)
- [Result Interpretation Guide](references/result-interpretation-guide.md)
- [Verification Methods](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Markdown guidance and JSON scan reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include submission counts, task IDs, poll status, and per-file findings when available.]

## Skill Version(s):

0.0.2 (source: ClawHub release metadata and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
