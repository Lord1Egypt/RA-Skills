## Description:

Audit Toolkit Pro helps agents produce audit and compliance guidance for code, contracts, AI logs, financial records, and related evidence, with workflows for batch review, continuous monitoring, multi-standard comparison, trend analysis, custom templates, and report certification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers, compliance officers, legal reviewers, AI ethics reviewers, and audit teams use this skill to structure audits, compare findings against standards, monitor selected targets, and prepare traceable audit outputs. It should be used only for authorized audit targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags broad file and command authority combined with continuous monitoring and external notification features that are not clearly scoped.

Mitigation: Use explicit audit targets, keep watch paths narrow, and review command execution, schedules, notification recipients, and webhook destinations before allowing them to run.

Risk: Audit inputs may include private code, contracts, financial records, AI logs, or regulated data.

Mitigation: Review the skill before installation in sensitive environments and limit inputs to data that is approved for the target agent and audit workflow.

Risk: The artifact describes security assessment workflows that could be misapplied to unauthorized targets.

Mitigation: Run the skill only against systems, files, and records where the user has explicit authorization to audit.

Risk: Monitoring and webhook notification workflows can send audit findings outside the local environment.

Mitigation: Avoid configuring callback or webhook URLs unless the destination is trusted and the data that may be sent is understood.

## Reference(s):

- [Detailed audit-toolkit-pro reference](references/detail.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include audit summaries, structured result descriptions, logs, report paths, and notification guidance depending on the selected workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
