## Description:

Researches major agent harness, runtime, coding-agent, skills, subagent, and plugin releases, producing verified facts, runtime explanations, layered impact analysis, and a source register that separates evidence from judgment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent platform teams, and technical analysts use this skill to assess what a newly released agent runtime or harness does, how it works, and its implications for coding agents, platforms, skills, plugins, subagents, evaluation, and enterprise adoption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may default to Chinese output, which may not suit every user.

Mitigation: Specify the desired output language when invoking the skill and review the result.

Risk: The security analysis is incomplete because one local path-like reference could not be resolved.

Mitigation: Inspect the unresolved reference and review the associated artifact before relying on the scan.

## Reference(s):

- [Fact Table Schema](references/fact-table-schema.md)
- [Impact Layers Analysis](references/impact-layers.md)
- [ClawHub Skill Release](https://clawhub.ai/haiyangchenbj/skills/agent-runtime-impact-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Tables, Source references]

**Output Format:** [Eight-section Markdown research report with a fact table, runtime flow explanation, layered impact analysis, platform comparisons, and source register.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates facts, observations, judgments, and hypotheses; current factual claims require sources.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
