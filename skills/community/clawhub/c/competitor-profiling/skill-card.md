## Description:

Researches competitor URLs and produces structured competitor profile markdown files using site scraping, SEO data, and market signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coreyhaines31](https://clawhub.ai/user/coreyhaines31)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, product, and sales teams use this skill to generate auditable competitor profiles from supplied competitor URLs, including positioning, pricing, customer proof, SEO strength, and side-by-side comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External scraping and SEO requests may collect sensitive, copyrighted, or unnecessary competitor review content.

Mitigation: Use quick scan for broad lists, confirm before deep profiling or comparing against your own domain, and review or delete raw data that is not needed.

Risk: Raw competitor research is saved locally and may persist beyond the immediate analysis task.

Mitigation: Review the generated raw data folders after use and remove data that should not be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coreyhaines31/skills/competitor-profiling)
- [Profile templates](references/templates.md)
- [MCP tool reference](references/tool-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown profiles and summary files, with raw markdown and JSON evidence saved locally]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes dated raw data folders and synthesized competitor profile files under competitor-profiles/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata.version: 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
