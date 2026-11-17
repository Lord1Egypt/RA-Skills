## Description:

Control LLM API spending per agent. Set daily/weekly/monthly limits with real-time tracking and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set per-agent and global LLM spending limits, log token usage, check budgets before paid calls, and generate local cost reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Budget checks are not an automatic hard spending cap; paid calls can bypass limits unless every caller invokes the check command before making an LLM request.

Mitigation: Wrap every paid call with budget check and treat a nonzero exit code as a block before the request is sent.

Risk: Local budget data can be modified by processes with write access, which can weaken any enforcement decision based on that data.

Mitigation: Protect the configured budget data directory from untrusted writers and run enforcement wrappers in a trusted environment.

Risk: Invalid numeric values can affect configured limits, prices, or usage records.

Mitigation: Validate limits, token counts, and model prices as finite positive values before relying on the tool as an enforcement gate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chloepark85/skills/agent-budget-controller)
- [README](artifact/README.md)
- [Usage Examples](artifact/EXAMPLE.md)
- [Installation Guide](artifact/INSTALL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local JSON and JSONL budget, pricing, and usage files in the configured data directory.]

## Skill Version(s):

1.0.0 (source: release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
