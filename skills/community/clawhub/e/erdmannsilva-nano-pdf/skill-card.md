## Description:

Edit PDFs with natural-language instructions using the nano-pdf CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erdmannsilva](https://clawhub.ai/user/erdmannsilva)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use this skill to apply targeted edits to a chosen PDF page with natural-language instructions through the nano-pdf CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The nano-pdf package is fetched from PyPI at install time without a fixed reviewed version.

Mitigation: Use the skill in a constrained workspace, avoid exposing sensitive files or credentials, and review the installed package version according to local policy.

Risk: PDF edits may target the wrong page when page numbering differs by nano-pdf version or configuration.

Mitigation: Check the edited PDF output and retry with the alternate page numbering convention if the edit is off by one.

Risk: Generated PDF edits can be incorrect or unsuitable for sharing without inspection.

Mitigation: Sanity-check the output PDF before sending or publishing it.

## Reference(s):

- [nano-pdf PyPI project](https://pypi.org/project/nano-pdf/)
- [ClawHub skill page](https://clawhub.ai/erdmannsilva/skills/erdmannsilva-nano-pdf)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown with inline bash commands and edited PDF file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the nano-pdf CLI; users should verify page numbering and review generated PDFs before sharing.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
