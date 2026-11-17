## Description:

Detect flaky tests from JUnit XML retries and emit a triage report with top unstable cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and CI maintainers use this skill to analyze JUnit XML retry artifacts, identify flaky candidates and persistent failures, and generate triage output for prioritization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads every JUnit XML file matched by JUNIT_GLOB, so an overly broad glob can expose unrelated local files to analysis.

Mitigation: Set JUNIT_GLOB to CI test result directories only, and avoid broad private folders.

Risk: The skill runs a local bash script with python3.

Mitigation: Install it only in environments where local script execution is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/ci-flake-triage)
- [Publisher profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Text report or JSON summary produced by a local bash script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash and python3; reads JUnit XML files matched by JUNIT_GLOB.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
