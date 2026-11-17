## Description:

Provides structured analysis of code, data, text, and decisions with prioritized findings, source labels, counter-evidence checks, and action-oriented Markdown output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, individual technical users, and automation teams use this skill to turn code, datasets, prose, or decision inputs into structured analysis reports. It is suited to code review, option comparison, data report cleanup, and evidence-aware decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and file capabilities.

Mitigation: Enable it only in a sandboxed or otherwise controlled agent environment, and review proposed commands or writes before execution.

Risk: The evidence reports inconsistent local-only, API, network, and write-operation claims.

Mitigation: Confirm network and API behavior is disabled or explicitly controlled before using the skill with sensitive code, data, or documents.

Risk: The skill generates analysis and recommendations that may be incomplete or misleading if the input is weak or ambiguous.

Mitigation: Require source labels, counter-evidence review, and human validation before relying on conclusions for security, business, or production decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-analyze-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown analysis reports with optional text, bash, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Chinese interaction patterns, priority labels, source attribution, counter-evidence review, and action recommendations.]

## Skill Version(s):

1.0.3 (source: evidence.json release.version; target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
