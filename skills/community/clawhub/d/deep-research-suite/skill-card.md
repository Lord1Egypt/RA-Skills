## Description:

Deep Research Suite guides an agent through multi-source search, extraction, synthesis, and structured research report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and developers use this skill to gather public-source information, compare findings, and produce concise research reports for decision support or follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research outputs may persist under memory/research/ and retain sensitive prompts, summaries, or source notes.

Mitigation: Avoid private or sensitive prompts unless local storage is acceptable, and delete generated reports when they are no longer needed.

Risk: Public-source research can include outdated, contradictory, or low-credibility information.

Mitigation: Check source dates, credibility, contradictions, and cited URLs before relying on the report.

## Reference(s):

- [Source skill artifact](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/aptratcn/skills/deep-research-suite)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Markdown research reports with source lists and optional comparison tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be saved under memory/research/ when the workflow is followed.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
