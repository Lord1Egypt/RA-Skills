## Description:

Extracts structured clinical trial data from pharmaceutical conference webpages or PDF documents, including drug, manufacturer, indication, phase, trial, conference, efficacy, and safety data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abinww](https://clawhub.ai/user/abinww)

### License/Terms of Use:

MIT

## Use Case:

External users, clinical analysts, and pharmaceutical teams use this skill to turn conference webpages or PDFs into standardized clinical-trial Markdown reports for review and follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can open supplied clinical-data URLs in the host browser, including untrusted or internal/private-network links.

Mitigation: Use trusted public conference or publisher URLs, avoid internal/private-network links, and review browser activity before use.

Risk: PDF handling and report generation can write files or images under the configured output directory.

Mitigation: Use read-only PDF extraction where possible, keep sensitive clinical or business documents out of shared workspaces, and review or clean the output directory after use.

Risk: Clinical outputs may be incomplete or misleading when source tables, images, or scanned PDFs are restricted or poorly extracted.

Mitigation: Verify extracted tables, image references, and expert commentary against the original source before using the report for decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/abinww/skills/clinical-data-extractor)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [markdown, files, guidance]

**Output Format:** [Markdown report with structured tables and optional image references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes report files under the configured output directory, normally ~/.openclaw/workspace, using the 药品名称@适应症.md naming pattern.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
