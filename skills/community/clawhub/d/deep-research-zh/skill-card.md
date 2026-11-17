## Description:

A Chinese-language deep research skill that guides agents through clarified scope, approved research plans, multi-source research cycles, and Chinese Markdown/PDF report delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mydearzsy](https://clawhub.ai/user/mydearzsy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and researchers use this skill to run controlled, multi-source Chinese deep research workflows for literature reviews, competitive intelligence, industry research, policy research, and trend reports with explicit citations and limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact workflow mandates saving reports, converting PDFs, and sending output through Feishu or the current chat without user permission.

Mitigation: Require explicit user confirmation before saving files, converting reports, or sending any report through messaging channels.

Risk: The artifact workflow references prior memory access without clear consent or scoping.

Mitigation: Ask for consent before memory access, scope memory queries to the active research task, and disclose any memory-derived context used in the report.

Risk: The README does not fully align with the security guidance around web access, messaging delivery, and PDF dependencies.

Mitigation: Update public documentation to disclose web research behavior, Feishu/current-chat delivery behavior, and PDF conversion dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mydearzsy/skills/deep-research-zh)
- [README.md](artifact/README.md)
- [Deep Research Quick Reference](artifact/quickref.md)
- [Deep Research Example Workflow](artifact/example.md)
- [Markdown to PDF helper script](artifact/scripts/md2pdf.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown research plans and reports with citations, optional PDF files, and concise status messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save reports to disk, convert Markdown to PDF, and send files through Feishu or the current chat according to the artifact workflow.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
