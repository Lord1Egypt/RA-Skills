## Description:

Transforms business questions into structured data-analysis reports through a seven-layer workflow covering persona understanding, data scoping, method selection, Python-based computation, quality checks, and Feishu-style report output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts, product teams, operations teams, and decision makers use this skill to turn data-backed business questions into scoped analyses, validated findings, and actionable report recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may run Python and install analysis packages in the user's environment.

Mitigation: Approve package names and versions before installation, and run the skill in an isolated virtual environment or sandbox.

Risk: Business datasets may include sensitive raw data.

Mitigation: Provide only the minimum scoped data needed for the analysis, anonymize sensitive fields when possible, and control access to generated outputs.

Risk: Analytical conclusions can be misleading when data quality, sample size, or method assumptions are weak.

Mitigation: Use the skill's required data-quality checks, cross-validation, and confidence annotations before acting on recommendations.

## Reference(s):

- [Full-Link Data Analysis Skill Page](https://clawhub.ai/openlark/skills/full-link-data-analysis)
- [Analysis Methods Library](artifact/references/methods.md)
- [Data-Aware Routing Rules](artifact/references/routing.md)
- [Quality Assurance Mechanism](artifact/references/quality.md)
- [Feishu Document Format Report Template](artifact/references/feishu-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Feishu-style Markdown analytical reports with findings, method notes, confidence annotations, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Python analysis code and package-installation commands during execution; final reports should omit raw execution traces.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
