## Description:

Ranked installable tools for agent jobs - OCR, PDF extraction, NFS-e invoices, bookkeeping, boletos, receipts, web scraping, with reproducible evals on real-world corpora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tlalvarez](https://clawhub.ai/user/tlalvarez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Auxiliar Solve to select installable tools or services for document extraction, OCR, web scraping, bookkeeping, and related automation tasks using ranked recommendations and evaluation evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing an unpinned third-party MCP service.

Mitigation: Pin and verify the npm package and source before installation, and treat returned install commands as recommendations that require separate validation.

Risk: Document workflows may involve sensitive financial or personal information.

Mitigation: Run the MCP with least privilege and avoid sending sensitive document details to third-party services unless privacy, consent, and data-handling requirements are accepted.

## Reference(s):

- [Auxiliar Solve on ClawHub](https://clawhub.ai/tlalvarez/skills/auxiliar-solve)
- [Human-readable rankings](https://auxiliar.ai/solve/)
- [Reproducible eval harness](https://github.com/Tlalvarez/Auxiliar-ai/tree/main/scripts/ocr-walkthrough)
- [Methodology](https://github.com/Tlalvarez/Auxiliar-ai/blob/main/docs/proposals/agent-upgrade-engine.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown-style guidance with command snippets and ranked recommendation data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked candidates, scorecards, install commands, alternatives considered, corpus summaries, caveats, and agent compatibility details.]

## Skill Version(s):

v0.1.0 (source: server release metadata and target metadata; frontmatter 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
