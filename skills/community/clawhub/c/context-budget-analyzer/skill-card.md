## Description:

Analyzes agent conversations and context trajectories to estimate token usage, identify context and compaction risks, and recommend ways to preserve important information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-zihan](https://clawhub.ai/user/z-zihan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand how agent conversations and context trajectories consume tokens, locate potential context or compaction problems, and create practical preservation and cleanup recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analysis and constraint-loss reports may be misleading when estimates, heuristic classifications, or partially checked references are treated as definitive.

Mitigation: Review the source records and relevant references, and manually confirm important findings before changing context or compaction policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/z-zihan/skills/context-budget-analyzer)
- [Project homepage](https://github.com/z-Zihan/awesome-skills)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with budget tables, findings, and actionable recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token totals may be estimates; trajectory analysis can use recorded usage data.]

## Skill Version(s):

1.8.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
