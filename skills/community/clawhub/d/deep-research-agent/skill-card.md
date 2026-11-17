## Description:

Deep Research Agent guides agents through quick research, deep dives, comparisons, landscape mapping, and adoption evaluations with source-aware structured outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jahonn](https://clawhub.ai/user/jahonn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users use this skill to turn broad research questions into structured summaries, sourced reports, comparison matrices, landscape maps, and adoption recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research outputs can reflect stale, biased, incomplete, or low-credibility web sources.

Mitigation: Use the skill's source hierarchy, recency checks, bias checks, citations, and gaps-and-caveats sections before relying on conclusions.

Risk: Deep-dive workflows may write workspace report files and could overwrite an existing report if an agent proceeds without confirmation.

Mitigation: Ask the agent to confirm before writing or overwriting files such as RESEARCH.md.

Risk: Installing through an npm CLI path adds installer trust and version-pinning risk.

Mitigation: Install through ClawHub when possible; otherwise pin and verify the installer before use.

## Reference(s):

- [Research Agent Methodology Reference](references/methodology.md)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills](https://agentskills.io)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research reports, comparison matrices, landscape maps, decision frameworks, and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deep-dive mode may produce a workspace report file such as RESEARCH.md; shorter modes return structured results in the conversation.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
