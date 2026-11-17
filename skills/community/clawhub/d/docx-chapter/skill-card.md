## Description:

Docx Chapter Clean helps agents turn chapter outlines into researched Markdown and DOCX drafts with source, footnote, and screenshot verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccmxigua](https://clawhub.ai/user/ccmxigua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and writers use this skill to create research-backed chapter drafts, convert them to DOCX, and verify citations, footnotes, source support, and screenshot evidence before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can open arbitrary citation URLs in a browser.

Mitigation: Review footnote URLs before screenshot verification, avoid private or authenticated pages, and use a network-restricted environment when appropriate.

Risk: Research text or page text may be sent to model tooling.

Mitigation: Do not process confidential, private, or regulated content unless the execution environment and model tooling are approved for that data.

Risk: LLM-selected highlights are candidate evidence and may not prove that a source supports a claim.

Mitigation: Keep human review in the verification loop and compare highlighted evidence against the exact claim before delivery.

Risk: DOCX mutation and footnote post-processing can affect links, footnote references, or document formatting.

Mitigation: Run the bundled DOCX verification checks and manually review generated files before sharing them.

## Reference(s):

- [Docx Chapter Clean on ClawHub](https://clawhub.ai/ccmxigua/skills/docx-chapter)
- [Unified Search Suite dependency](https://clawhub.ai/ccmxigua/unified-search-suite)
- [Claim verification schema](references/claim_verification_schema.json)
- [Mandatory search templates](references/search_templates.md)
- [Claude Code issue 50597](https://github.com/anthropics/claude-code/issues/50597)
- [Citation Check Skill](https://github.com/serenakeyitan/citation-check-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown, DOCX files, JSON verification reports, screenshots, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pandoc and may use external search, model calls, browser automation, and DOCX post-processing.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
