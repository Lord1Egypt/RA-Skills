## Description:

Scan a directory of documents, classify each file by compliance type, resolve version conflicts with the user, and produce a prioritized analysis plan mapping confirmed-current documents to rote skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dangsllc](https://clawhub.ai/user/dangsllc)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance teams, auditors, and developers use this skill to inventory compliance document folders, identify current document versions, and route each relevant file to an appropriate downstream analysis skill before review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect filenames and short snippets from sensitive compliance, business, or health-related documents in the selected directory.

Mitigation: Run it only on the intended document folder and avoid broad scans that include unrelated sensitive files.

Risk: Filename and path classification can misroute ambiguous documents or older versions.

Mitigation: Review the produced manifest and resolve version prompts before using downstream analysis skills.

## Reference(s):

- [Document Finder on ClawHub](https://clawhub.ai/dangsllc/skills/document-finder)
- [Rote Compliance Toolkit](https://github.com/dangssolutions/rote-compliance-toolkit)
- [Rote](https://dangssolutions.com/rote)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown summary table with suggested next steps and a JSON manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritizes confirmed-current documents and records set-aside files after user version resolution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
