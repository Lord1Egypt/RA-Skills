## Description:

Cross-platform product selection and sourcing analysis for distributors and dropshippers using OpenCLI integrations for Alibaba, AliExpress, and Amazon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lcturing0](https://clawhub.ai/user/lcturing0)

### License/Terms of Use:

MIT-0

## Use Case:

External distributors, dropshippers, and commerce operators use this skill to compare sourcing options against retail-channel signals and produce product-selection recommendations with margin analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Post-selection actions can import products to external store channels or notify listing events without an explicit confirmation boundary in the artifact workflow.

Mitigation: Require explicit confirmation before any post-selection action, including the exact account, product IDs, destination channel, and operation.

Risk: The workflow depends on credentialed Alibaba/OpenCLI commerce tooling and marketplace plugins.

Mitigation: Install only for intended commerce use, verify or pin plugin sources, and check required credentials before running platform actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lcturing0/skills/distributor-product-selection)
- [Project homepage](https://github.com/lcturing0/skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces product research reports and recommended commerce actions based on external marketplace data.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
