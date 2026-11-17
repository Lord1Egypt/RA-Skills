## Description:

Generate academic papers from metadata using the EasyPaper Python SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinkgranite](https://clawhub.ai/user/pinkgranite)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to generate structured LaTeX academic papers from metadata and to follow EasyPaper SDK workflows for setup, generation, venue formatting, and final PDF selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable or unverified package and toolchain installation sources can introduce supply-chain risk.

Mitigation: Pin and verify the EasyPaper package and use trusted package managers or HTTPS sources for supporting tools.

Risk: The HTTP Typesetter fallback may expose draft paper metadata or document content off-host.

Mitigation: Prefer local PDF compilation or configure an explicitly trusted HTTPS Typesetter endpoint before processing confidential or unpublished drafts.

Risk: Generated academic content may contain incorrect claims, citations, or formatting.

Mitigation: Review generated papers, references, and final PDFs before submission or publication.

## Reference(s):

- [EasyPaper ClawHub Skill Page](https://clawhub.ai/pinkgranite/skills/easypaper)
- [EasyPaper Repository](https://github.com/PinkGranite/EasyPaper)
- [EasyPaper Plugin Reference](https://github.com/PinkGranite/EasyPaper/tree/master/plugins/easypaper)
- [Example Metadata](https://github.com/PinkGranite/EasyPaper/blob/master/examples/meta.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of LaTeX source and PDF outputs through the EasyPaper SDK and local toolchain.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
