## Description:

A Chinese-language data analysis skill that helps agents apply decision-first analysis, statistical rigor checks, A/B test interpretation, method selection, and common analysis pitfall detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, product managers, operations staff, and data analysts use this skill to structure dataset analysis, evaluate experiments, identify statistical pitfalls, and produce concise decision-oriented reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read user-provided datasets, which may include sensitive or confidential data.

Mitigation: Keep sensitive files out of the agent workspace unless they are necessary for the analysis, and review outputs before sharing them.

Risk: The skill may suggest shell commands or package installations while helping with data analysis workflows.

Mitigation: Review proposed commands before execution and run them only in an appropriate sandbox or controlled environment.

Risk: External data source credentials may be needed for some workflows.

Mitigation: Provide credentials through environment variables only when required and avoid placing keys in prompts, scripts, notebooks, or configuration files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/data-analysis-toolkit)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include statistical summaries, confidence intervals, decision recommendations, limitations, and next-step guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
