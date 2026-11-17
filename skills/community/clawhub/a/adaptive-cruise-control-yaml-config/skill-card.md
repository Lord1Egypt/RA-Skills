## Description:

Use this skill when reading or writing YAML configuration files, loading vehicle parameters, or handling config file parsing with proper error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to read and write YAML configuration files, load vehicle parameters, and handle missing or malformed configuration safely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent may read or write an unexpected YAML file if the configured file path is wrong.

Mitigation: Review the specific YAML file paths and defaults the agent will use before deployment.

Risk: Unsafe YAML parsing can execute unwanted constructs in some YAML libraries.

Mitigation: Use safe YAML loading as directed by the skill and avoid unsafe loader APIs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/adaptive-cruise-control-yaml-config)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Python code examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
