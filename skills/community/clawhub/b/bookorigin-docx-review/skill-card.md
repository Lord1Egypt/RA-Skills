## Description:

Runs a local Chinese-language DOCX ZIP and structure preflight, then builds an advisory review package bound to the source hash and reviewer decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and editorial reviewers use this skill to preflight authorized DOCX教材 files locally, identify limited structural review candidates, and package human decisions for later review. Its output is advisory and does not approve, sign, modify, or validate delivery readiness for the document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs access to the DOCX and review JSON files supplied by the user.

Mitigation: Use it only with files the caller is authorized to process, and keep outputs in the same controlled local review workflow.

Risk: DOCX structure preflight can miss malware, rendering issues, factual problems, copyright concerns, teaching quality issues, or print-readiness problems.

Mitigation: Treat the findings as advisory and pair them with normal security scanning, editorial review, rights review, and document acceptance checks.

Risk: Review-package integrity checks show case consistency but do not establish identity, signature, approval, or a tamper-proof chain of custody.

Mitigation: Use separate signing, identity, approval, and record-management controls when those assurances are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongsheng123132/skills/bookorigin-docx-review)
- [Action contract](artifact/action-contract.json)

## Skill Output:

**Output Type(s):** [JSON, guidance]

**Output Format:** [Single-line JSON objects from CLI actions, with advisory findings and review-package manifests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only processing; outputs omit absolute paths, source text, DOCX bytes, and secrets according to the action contract.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
