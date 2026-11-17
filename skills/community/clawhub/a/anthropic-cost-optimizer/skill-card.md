## Description:

Audits OpenClaw YAML and JSON configurations for Anthropic API cost drivers, proposes cost-saving changes, shows annotated diffs and savings estimates, and can write confirmed optimizations back to the config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextfrontierbuilds](https://clawhub.ai/user/nextfrontierbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit OpenClaw configurations that use Anthropic models, identify high-impact cost levers, and review proposed YAML or JSON changes before applying them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may cause local OpenClaw configuration files to be inspected in conversations only loosely related to cost tuning.

Mitigation: Use the skill only when the prompt clearly asks for OpenClaw or Anthropic API cost optimization, review the shown diff carefully, and confirm only the changes intended for writing.

## Reference(s):

- [Pricing Reference](references/pricing.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with annotated YAML or JSON diffs and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file edits to OpenClaw configuration after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
