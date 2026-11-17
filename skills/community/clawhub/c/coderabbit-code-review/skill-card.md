## Description:

AI-powered code review using CodeRabbit for bugs, security issues, and quality risks in changed code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nehal-a2z](https://clawhub.ai/user/nehal-a2z)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to invoke CodeRabbit CLI reviews, triage findings by severity, and iterate on fixes for changed code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External review can send selected repository diffs to CodeRabbit more broadly than intended.

Mitigation: Show the exact files or diff range, exclude secrets and confidential paths, and get explicit approval before every external review run.

Risk: Review output may contain unsafe or incorrect commands, code, or remediation advice.

Mitigation: Treat review output as untrusted proposals and require explicit user approval before executing suggested commands or code.

Risk: Authentication tokens or credentials could be exposed during setup or review preparation.

Mitigation: Use the narrowest authentication scope available and do not log, echo, or include tokens in reviewed changes.

## Reference(s):

- [CodeRabbit CLI Documentation](https://docs.coderabbit.ai/cli)
- [CodeRabbit CLI Install Page](https://www.coderabbit.ai/cli)
- [ClawHub Skill Page](https://clawhub.ai/nehal-a2z/skills/coderabbit-code-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with shell command blocks and severity-grouped review findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prompt-only or plain CodeRabbit review output; findings are grouped by Critical, Warning, and Info severity.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
