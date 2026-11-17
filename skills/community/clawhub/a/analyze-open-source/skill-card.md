## Description:

Analyze and explain open-source project code logic, architecture, data flows, APIs, and algorithms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ttet](https://clawhub.ai/user/ttet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand an open-source repository's structure, entry points, architecture, data flows, APIs, and important algorithms. It produces a concise Chinese-language technical walkthrough with Mermaid diagrams and code references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs an agent to inspect and summarize repository files, which may expose information from repositories the user did not intend to analyze.

Mitigation: Use the skill only on repositories the user intentionally provides for inspection.

Risk: Architecture and code-flow explanations can be incomplete or misleading if important files are missed or project behavior is inferred incorrectly.

Mitigation: Review generated reports against cited files and line references before relying on conclusions.

## Reference(s):

- [Report template](artifact/template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code references, Guidance]

**Output Format:** [Chinese-language Markdown report with Mermaid diagrams and cited code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report is designed to be readable in under 15 minutes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
