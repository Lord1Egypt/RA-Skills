## Description:

Supports deep research and citation checking by finding scholarly sources, checking reference metadata against registries, and producing cited reports and bibliography exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[docsor1212](https://clawhub.ai/user/docsor1212)

### License/Terms of Use:

MIT

## Use Case:

Researchers, students, and analysts can use Cite Holmes to plan literature searches, check references, and prepare reports or bibliography exports. Review incomplete or consequential citation checks before relying on them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports serious weaknesses that could undermine citation verification; the scan was partial.

Mitigation: Review the reported weaknesses before installation and independently verify citations and claims you rely on.

Risk: ClawScan reports a network request restriction bypass, and partial scan coverage leaves behavior uncertain.

Mitigation: Use a pinned, reviewed release and check that its network behavior fits your policy before enabling it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/docsor1212/skills/cite-holmes)
- [Citation verification details](references/verification-details.md)
- [Security and behavior declaration](references/security.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, BibTeX, RIS]

**Output Format:** [Markdown research and verification reports, JSON workpapers, and bibliography exports in CSV, BibTeX, RIS, or GB/T 7714 formats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include citation-verification verdicts and may flag incomplete checks for human review.]

## Skill Version(s):

6.9.0 (source: skill frontmatter; server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
