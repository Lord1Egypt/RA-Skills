## Description:

Astronclaw Code Review helps agents review JavaScript and TypeScript code for quality, security, and performance issues and generate review reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shixiangyu2](https://clawhub.ai/user/shixiangyu2)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering agents use this skill to scan source code, identify maintainability, security, and performance findings, receive remediation guidance, and produce review reports in common formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accepts file paths and can read local files selected through tool arguments.

Mitigation: Run it in a sandboxed or workspace-scoped runtime and restrict file paths to the intended project; prefer direct code input for untrusted workflows.

Risk: Generated HTML reports may include unescaped content from analyzed code or findings.

Mitigation: Use Markdown or JSON reports for untrusted code, or open HTML only after output escaping is fixed and the report is reviewed in a trusted environment.

Risk: AI-assisted analysis may send code or metadata to an external provider when enabled.

Mitigation: Confirm provider configuration and data handling before enabling external analysis, and disable AI recommendations for sensitive repositories unless approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shixiangyu2/skills/astronclaw-code-review)
- [AstronClaw platform](https://astronclaw.iflytek.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured tool results and review reports in Markdown, HTML, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable review depth, optional security and performance analysis, and optional AI-assisted recommendations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence, skill.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
