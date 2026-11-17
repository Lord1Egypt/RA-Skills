## Description:

Zero-setup token cost analyzer for OpenClaw that runs locally and returns a ranked report with estimated dollar amounts for optimization opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morpheis](https://clawhub.ai/user/morpheis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit OpenClaw token usage, estimate daily and monthly costs, and identify prioritized changes that may reduce spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analyzer reads selected workspace Markdown filenames/sizes and local OpenClaw model configuration to estimate token costs.

Mitigation: Run it only against the intended workspace path and review the report before acting on recommendations.

Risk: JSON output may be consumed by automation and can include workspace-derived filenames.

Mitigation: Avoid untrusted filenames when using JSON output in downstream scripts.

Risk: Cost recommendations are estimates based on detected configuration, bundled pricing, and fixed usage assumptions.

Mitigation: Validate recommendations against current provider pricing and real usage before making billing or configuration decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/morpheis/skills/costclaw)
- [Project Homepage](https://github.com/Morpheis/costclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain-text or JSON cost report with ranked recommendations and command/configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against a selected workspace path; JSON output is available for automation.]

## Skill Version(s):

0.3.1 (source: ClawHub release metadata; artifact frontmatter reports 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
