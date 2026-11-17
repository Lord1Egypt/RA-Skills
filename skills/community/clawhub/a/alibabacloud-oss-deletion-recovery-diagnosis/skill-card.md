## Description:

Diagnoses accidental OSS deletions and leftover storage using read-only bucket metadata, then explains recoverability and manual next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OSS administrators use this skill to assess whether deleted objects can be recovered, explain why buckets remain nonempty or storage charges persist, and identify manual next steps without changing resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing or ambiguous bucket details may expose account bucket names through inventory lookup.

Mitigation: Supply an explicit bucket name, use least-privilege read-only RAM permissions, and avoid invoking the skill from vague prompts.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-deletion-recovery-diagnosis)
- [Recovery decision tree](references/recovery-decision-tree.md)
- [Deletion residue checklist](references/deletion-residue-checklist.md)
- [Read-only RAM policy](references/ram-policies.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown diagnosis with findings and manual next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports degraded queries and avoids making changes to OSS resources.]

## Skill Version(s):

0.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
