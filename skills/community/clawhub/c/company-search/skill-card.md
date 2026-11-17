## Description:

Multi-source company research tool that generates structured due-diligence reports covering company background, ownership, legal risk, funding, intellectual property, procurement, hiring, news, competitors, and industry position.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fan31415](https://clawhub.ai/user/fan31415)

### License/Terms of Use:


## Use Case:

External users, developers, and analysts use this skill to research companies from public web sources and produce structured due-diligence reports comparable in scope to Tianyancha or Qichacha. It adapts to available search and fetch tools, with a Python fallback for environments without built-in web access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell-backed local fallback can fetch arbitrary URLs and may reach private networks, internal URLs, or sensitive research targets if installed in a privileged environment.

Mitigation: Review before installation, prefer built-in scoped search and fetch tools, and avoid granting shell access unless the local fallback is necessary.

Risk: The jina and archive fetch strategies may route target URLs and page content through third-party services.

Mitigation: Use direct-only mode for public URLs and do not use jina or archive routing for confidential, internal, or sensitive targets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fan31415/skills/company-search)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown structured report with tables, source links, confidence labels, and optional JSON output from the local search/fetch helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should identify the selected company entity, cite public sources, include retrieval date and confidence, and clearly flag fields that were unavailable or only snippet-verified.]

## Skill Version(s):

2.0.4 (source: evidence.release.version; artifact/package.json lists 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
