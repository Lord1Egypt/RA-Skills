## Description:

Comprehensive research agent for in-depth investigation, including deep research, market research, academic surveys, competitive analysis, technology trends, and topics requiring 100+ source verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericn26-star](https://clawhub.ai/user/ericn26-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research users can use this skill to plan and conduct broad, multi-source investigations and synthesize cited research reports. It is suited to requests that require query decomposition, source collection, fact checking, and structured findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Large autonomous web and PDF research runs can incorporate untrusted, outdated, or low-quality source material.

Mitigation: Treat retrieved content as evidence to be checked, review source quality, and verify important claims against authoritative sources before relying on the report.

Risk: Packaging the skill from a directory containing untrusted symlinks could include unintended files.

Mitigation: Run packaging only from a trusted skill directory and review package contents before distribution.

## Reference(s):

- [DeepResearch Agent Reference Documentation](references/research_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown research reports with inline citations and JSON planning or extraction structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include research plans, source matrices, confidence indicators, contradiction notes, tables, and citation lists.]

## Skill Version(s):

11.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
