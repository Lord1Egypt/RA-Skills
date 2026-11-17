## Description:

Monitor bioRxiv/medRxiv preprints and academic discussions to identify emerging research hotspots before they appear in mainstream journals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and research operations teams use this skill to scan preprint feeds and academic discussion signals for early indications of emerging biomedical or quantitative biology topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can save report output to a caller-selected path and may overwrite existing files.

Mitigation: Run it from a limited workspace and constrain output paths before using the save option.

Risk: bioRxiv and medRxiv access attempts use browser-like headers around site protections.

Mitigation: Prefer the arXiv feed path and review whether any bioRxiv or medRxiv access complies with those sites' terms before use.

Risk: The release depends on broad, unpinned Python packages.

Mitigation: Install in an isolated virtual environment and pin or review dependencies before routine use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/emerging-topic-scout)
- [References for Emerging Topic Scout](references/README.md)
- [arXiv Quantitative Biology RSS](https://export.arxiv.org/rss/q-bio)
- [bioRxiv API](https://api.biorxiv.org/)
- [medRxiv API](https://api.medrxiv.org/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, shell commands, configuration]

**Output Format:** [Command-line reports in Markdown, JSON, or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can be printed to stdout or saved to a caller-selected file path.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
