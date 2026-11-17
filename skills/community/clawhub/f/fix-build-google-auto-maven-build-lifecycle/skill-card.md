## Description:

Use when working with Maven build phases, goals, profiles, or customizing the build process for Java projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for Maven lifecycle guidance, including build phases, goals, profiles, resource filtering, test configuration, multi-module builds, CI/CD examples, and build troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example Maven commands such as clean, deploy, and site-deploy can alter build outputs or publish artifacts when run in the wrong project or with active credentials.

Mitigation: Verify the current project, Maven settings, repository targets, credentials, and intended lifecycle phase before running generated commands.

Risk: Build guidance can be applied incorrectly if profiles, skip-test flags, or module selectors do not match the project's release or CI policy.

Mitigation: Review profile activation, test-skip options, and module selection against project policy before using the examples in CI or release workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, XML, properties, YAML, and Groovy code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reference guidance and example Maven commands for agent responses; it does not execute commands automatically.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
