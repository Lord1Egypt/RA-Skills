## Description:

Extracts a specified feature's implementation path from project code and produces technical development documentation covering business logic, data flow, exception handling, and Mermaid diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[addxing](https://clawhub.ai/user/addxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to trace a named feature from entry point through implementation and produce documentation that another developer can use to understand or reimplement the behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects relevant source code and may expose implementation details in generated documentation.

Mitigation: Use it only in codebases where that level of source inspection and documentation output is acceptable.

Risk: Generated implementation traces or diagrams may be incomplete or misleading if the entry point or code path is wrong.

Mitigation: Review the selected entry point, cited code paths, and Mermaid diagrams before relying on the documentation.

## Reference(s):

- [Source Repository](https://github.com/addxing/function-extraction)
- [ClawHub Skill Page](https://clawhub.ai/addxing/skills/function-extraction)
- [Documentation Template](template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown technical documentation with Mermaid diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes implementation-chain analysis, code locations, flowcharts, sequence diagrams, and dependency graphs when applicable.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
