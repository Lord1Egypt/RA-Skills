## Description:

Checks whether a medical-device clinical evaluation equivalence argument includes required report elements and data-access rights, returning decision-support findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT (Python code only; documentation and theory text all rights reserved)

## Use Case:

Medical-device regulatory teams and developers use this skill to screen clinical evaluation reports for missing equivalence elements and evidence of data-access rights before expert review. Its findings do not establish regulatory compliance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation rules and declared web, write, and shell access exceed the offline checker's needs.

Mitigation: Review before installing and restrict invocation and tool access to explicit clinical evaluation equivalence-check tasks.

Risk: Package integrity metadata is stale.

Mitigation: Verify package hashes and integrity metadata with the publisher before use.

Risk: A completeness check may be mistaken for an official regulatory determination.

Mitigation: Treat results as triage and have a qualified reviewer check current official requirements and the underlying evidence.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/cer-equivalence-check)
- [ClawHub publisher profile](https://clawhub.ai/user/zhaoxinghua09-cell)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON decision-support findings from the CLI, with warnings and status codes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flags missing report sections and data-access agreements; human review is required.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release; packaged skill text also mentions 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
