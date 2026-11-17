## Description:

FluidGraph provides deterministic steady-state fluid network solving and reliability analysis for TOML-defined pump, pipe, valve, and load scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lichaoprogress](https://clawhub.ai/user/lichaoprogress)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use FluidGraph to validate fluid-network definitions, analyze valve and load scenarios, compare reliability outcomes, and render readable reports without relying on LLM-generated calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File-path inputs may read arbitrary local files despite the documented whitelist.

Mitigation: Run the skill in a sandboxed workspace, prefer inline TOML or known project files, and block untrusted prompts from choosing arbitrary local paths until whitelist, extension, and size checks are enforced consistently.

Risk: Unsupported topologies and unreachable loads can return null values that may be mistaken for calculated zero values.

Mitigation: Report unsupported topologies and null values exactly as returned, and do not estimate pressure, flow, velocity, or pressure-drop values that are absent from AnalysisResult.

## Reference(s):

- [FluidGraph Skill Contract](artifact/SKILL.md)
- [FluidGraph Release README](artifact/README.md)
- [ClawHub Skill Page](https://clawhub.ai/lichaoprogress/skills/fluidgraph)
- [ClawHub Publisher Profile](https://clawhub.ai/user/lichaoprogress)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Structured JSON SkillResult objects, AnalysisResult JSON, and Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic calculations use SI units in JSON; null means no valid value, not zero.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
