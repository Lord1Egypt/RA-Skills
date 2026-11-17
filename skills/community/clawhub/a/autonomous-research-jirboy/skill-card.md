## Description:

Autonomous Research routes a research topic through a 23-stage autonomous research workflow to produce a paper draft, LaTeX source, citations, charts, and experiment artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to turn a research idea into literature discovery, experiment planning, generated experiment code, result analysis, and draft academic writing for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended execution can run generated research or experiment steps without adequate review.

Mitigation: Keep simulated mode enabled by default, turn approval gates on, and review generated code and experiment plans before execution.

Risk: Shell-based command execution can be unsafe with untrusted research topics or execution settings.

Mitigation: Replace shell command construction with argument-based spawn or execFile before accepting untrusted topics or enabling sandbox or SSH execution.

Risk: Persistent configuration mutation can leave later runs using unexpected models, templates, or execution modes.

Mitigation: Review configuration changes before and after each run, and prefer environment variables for credentials instead of plaintext API keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jirboy/skills/autonomous-research-jirboy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown and LaTeX documents, BibTeX references, generated code, charts, and run artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The normal output set includes a paper draft, LaTeX source, references, charts, and experiment run artifacts.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
