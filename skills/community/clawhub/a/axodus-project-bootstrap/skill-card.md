## Description:

Bootstrap new projects with predictable structure and validation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to initialize services, applications, libraries, contracts, or CLI projects with a predictable file structure, local validation commands, and safe configuration defaults.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project scaffolding may create or modify files in an unintended target directory.

Mitigation: Confirm the target path before execution and review the generated file tree before keeping changes.

Risk: Generated dependencies, linting, formatting, or test settings may not match repository policy.

Mitigation: Review dependency and configuration choices, then run the generated install, lint, test, and build commands.

Risk: The artifact trigger metadata is malformed, which may make activation unreliable.

Mitigation: Correct trigger metadata from the placeholder value to explicit activation triggers before publication or installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mzfshark/skills/axodus-project-bootstrap)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Markdown, Code]

**Output Format:** [File tree, generated project files, README guidance, configuration defaults, and validation commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local scaffolding only; does not auto-deploy or modify global tooling unless explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
