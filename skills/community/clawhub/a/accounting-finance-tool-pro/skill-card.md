## Description:

This skill helps agents support accounting and finance workflows covering valuation modeling, financial analysis, risk assessment, batch processing, and report drafting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External finance analysts, institutional investors, enterprise finance teams, and developers use this skill to guide accounting and finance analysis, build valuation workflows, assess financial risk, and generate structured reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, and command execution authority for finance workflows.

Mitigation: Invoke it only for explicit finance or accounting analysis tasks in a workspace that does not expose unrelated sensitive files.

Risk: The artifact gives inconsistent guidance about storing API keys and references local configuration files.

Mitigation: Use environment variables or a secret manager for credentials and avoid putting live keys in config.yaml.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and structured JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce finance reports, batch-analysis instructions, configuration examples, and risk assessment summaries.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
