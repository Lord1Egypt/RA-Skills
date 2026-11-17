## Description:

Use to fact-check an explainer against its sources before delivery, ensuring every checkable claim traces to a cited source or, for code, the real implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[analyticalmonk](https://clawhub.ai/user/analyticalmonk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and editorial reviewers use this skill to audit explainer drafts or research notes before delivery. It produces a blocking claim-by-claim verification report so unsupported, contradicted, or unsourced factual claims are corrected, supported, softened, or removed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The strict verification gate can slow or block delivery until factual claims are supported, corrected, or removed.

Mitigation: Use the skill when claim verification is required, and review the implicit invocation setting if it should run only on explicit request.

Risk: A fact-check report may still be incomplete if cited sources are not opened and checked against the exact claim text.

Mitigation: Require source passages or exact code locations for each checkable claim and keep the overall verdict at FAIL until all rows are supported.

## Reference(s):

- [Verification Report Format](references/verification-report-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown claim table with PASS/FAIL verdict and recommended fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report blocks delivery until every checkable factual claim is supported.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
