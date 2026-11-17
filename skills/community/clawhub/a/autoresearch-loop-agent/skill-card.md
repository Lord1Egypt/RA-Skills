## Description:

Autoresearch guides agents through systematic experiment loops for optimization, ablation studies, and configuration search by iteratively changing one variable, measuring a metric, and keeping or discarding results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[admirobot](https://clawhub.ai/user/admirobot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run structured, metric-driven experiments over code, prompts, configurations, or model settings. It helps an agent set up an experiment protocol, execute iterative trials, record outcomes, and summarize what improved or regressed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can repeatedly run commands and modify code during open-ended experiments.

Mitigation: Run it only in a clean, disposable branch or worktree with explicit experiment, time, and cost limits.

Risk: Its experiment loop may use destructive git resets that erase work.

Mitigation: Confirm the repository has no uncommitted work before running and keep target files and read-only files explicit in autoresearch.config.md.

Risk: Autonomous command execution can expose sensitive repositories or environments to unintended changes.

Mitigation: Avoid running it where secrets are accessible, review autoresearch.config.md before execution, and constrain allowed files and resources.

## Reference(s):

- [Autoresearch Reference](artifact/reference.md)
- [ClawHub skill page](https://clawhub.ai/admirobot/skills/autoresearch-loop-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration files, and tab-separated experiment records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create autoresearch.config.md and results.tsv and may propose or run git commands during an experiment loop.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
