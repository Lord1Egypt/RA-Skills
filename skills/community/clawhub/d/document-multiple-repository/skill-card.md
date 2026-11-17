## Description:

Generates consolidated technical documentation for software systems made up of multiple local repositories, including frontend, backend, microservices, infrastructure, documentation, and wikis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannyxyz22](https://clawhub.ai/user/dannyxyz22)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to scan local multi-repository software systems and generate consolidated system, architecture, deployment, repository map, API, code structure, and process documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads repositories and wikis under the ROOT_PATH selected by the user.

Mitigation: Use the narrowest practical ROOT_PATH so the agent only analyzes repositories intended for documentation.

Risk: Generated documentation may consolidate internal architecture, process details, configuration names, and API examples.

Mitigation: Write output to a controlled OUTPUT_PATH and review generated Markdown before sharing it outside the intended audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dannyxyz22/skills/document-multiple-repository)
- [Publisher profile](https://clawhub.ai/user/dannyxyz22)
- [Skill definition](artifact/SKILL.md)
- [Release changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Structured Markdown documentation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated documentation to the user-selected OUTPUT_PATH and does not modify the original repositories.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
