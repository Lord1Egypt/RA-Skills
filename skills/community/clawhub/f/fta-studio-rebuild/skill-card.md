## Description:

Provides a source snapshot and engineering guidance for rebuilding, extending, and validating FTA Studio, a fault tree analysis editor and analysis tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guiqulaihaiqing](https://clawhub.ai/user/guiqulaihaiqing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reliability engineers use this skill to restore or extend FTA Studio, troubleshoot its editor and analysis features, and validate changes using the included source, examples, and scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports potentially destructive installation and process stopping behavior.

Mitigation: Avoid installation until file replacement and process termination risks are addressed; review the changes and affected processes before proceeding.

Risk: Reported issues could affect safety-analysis results, and the security scan had incomplete coverage with partial analysis and degraded static checks.

Mitigation: Independently review analysis-result issues before relying on outputs, and treat behavior not covered by the scan as unassessed.

## Reference(s):

- [FTA Studio Rebuild on ClawHub](https://clawhub.ai/guiqulaihaiqing/skills/fta-studio-rebuild)
- [Architecture](references/architecture.md)
- [Frontend](references/frontend.md)
- [medini Parity](references/medini-parity.md)
- [Windows Packaging](references/windows-packaging.md)
- [Pitfalls](references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with source files, examples, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a restorable source snapshot, Windows launchers, examples, and validation scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
