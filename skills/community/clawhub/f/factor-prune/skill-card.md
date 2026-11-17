## Description:

factor-prune helps agents select high-signal, low-redundancy stock factors from stock-factor spreadsheet outputs using greedy forward selection and correlation pruning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mifochen](https://clawhub.ai/user/mifochen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative finance users use this skill to reduce large evaluated stock-factor pools into smaller, lower-redundancy factor lists for downstream QuantAll workflows. The skill is intended for factor selection and diagnostic analysis, not factor synthesis, backtesting, or portfolio construction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Factor formulas and output-path metadata can be sent to a user-supplied QuantAll MCP endpoint over unauthenticated HTTP.

Mitigation: Use the default localhost endpoint or a trusted MCP endpoint, and avoid remote --mcp-url values unless that disclosure is acceptable.

Risk: Execution depends on QuantAll and Python packages, so an uncontrolled environment can change runtime behavior.

Mitigation: Run the skill in a locked QuantAll/Python environment and review package versions before execution.

Risk: QuantAll single-instance execution can fail or remain busy if duplicate instances compete for the local task lock.

Mitigation: Connect to one existing QuantAll instance, use retry/backoff for busy responses, and avoid launching extra instances.

## Reference(s):

- [ClawHub factor-prune Skill Page](https://clawhub.ai/mifochen/skills/factor-prune)
- [factor-prune Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and generated spreadsheet paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces pruned factor-list spreadsheets such as scripts/factor-pure.xlsx or scripts/output/pruned_factors.xlsx; does not produce backtests or multi-factor combinations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
