## Description:

Validate Babel config files (babel.config.json, .babelrc, .babelrc.json, package.json#babel) for deprecated presets, plugin conflicts, ordering issues, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and build engineers use this skill to validate Babel configuration files, explain current preset and plugin behavior, and get improvement suggestions before CI checks or Babel migration work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The validator reads the Babel config path supplied by the user and may inspect nearby Babel config or package metadata to report conflicts.

Mitigation: Run it only against intended project directories and review generated reports before sharing logs externally.

Risk: Validation and suggestion output can be incorrect or incomplete for project-specific Babel setups.

Mitigation: Review findings before changing build configuration and confirm behavior with the project's normal test or build pipeline.

## Reference(s):

- [Babel Config Validator on ClawHub](https://clawhub.ai/charlie-morrison/skills/babel-config-validator)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration guidance]

**Output Format:** [Human-readable text, JSON findings, or summary status lines.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes distinguish clean results, validation errors, and invalid input.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
