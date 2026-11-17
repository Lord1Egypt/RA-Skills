## Description:

Funnel Analyzer creates conversion funnels, diagnoses drop-off points, compares industry benchmarks, suggests optimizations, and generates reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, growth teams, and developers use this skill to analyze funnel step counts, identify conversion drop-offs, compare common industry benchmarks, and produce optimization reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted funnel data may trigger command execution through unsafe arithmetic parsing.

Mitigation: Use only trusted funnel data until parsing is fixed to accept canonical integers only, and review the shell arithmetic before installation.

Risk: The release includes an unrelated utility script that stores local data persistently.

Mitigation: Remove the generic utility script or clearly document its local storage behavior before deployment.

Risk: Security evidence marks this release as suspicious.

Mitigation: Review and scan the skill before deployment, following the server-provided security guidance.

## Reference(s):

- [Funnel Analyzer on ClawHub](https://clawhub.ai/ckchzh/skills/funnel-analyzer)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces funnel visualizations, diagnostic tables, benchmark summaries, optimization suggestions, comparisons, and report text from user-provided funnel step counts.]

## Skill Version(s):

2.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
