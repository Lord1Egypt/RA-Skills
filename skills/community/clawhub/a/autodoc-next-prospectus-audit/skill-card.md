## Description:

Audit one local prospectus PDF, DOC, or DOCX through PDRouter and download the annotated document with AutoDoc NEXT2.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paodingai](https://clawhub.ai/user/paodingai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and document reviewers use the skill to submit one local prospectus for an annotated audit, check its status, and explicitly download the completed result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports an unpinned command that installs external skills, and part of the referenced script was only partially inspected.

Mitigation: Consider postponing installation until the CLI and external repository are pinned to reviewed versions and the script is fully inspected; the scan is incomplete, so the absence of other reported issues does not establish that the skill is safe.

## Reference(s):

- [AutoDoc NEXT2.0 on ClawHub](https://clawhub.ai/paodingai/skills/autodoc-next-prospectus-audit)
- [PDRouter service](https://platform.paodingai.com/)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [Annotated PDF or DOCX document, with audit status and download metadata]

**Output Parameters:** [1D (one prospectus per invocation)]

**Other Properties Related to Output:** [PDF input produces an annotated PDF; DOC or DOCX input produces an annotated DOCX. Result download is an explicit step after audit completion.]

## Skill Version(s):

1.5.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
