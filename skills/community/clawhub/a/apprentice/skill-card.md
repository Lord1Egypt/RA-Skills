## Description:

Apprentice lets an agent observe a user-performed task, synthesize it into a reusable local workflow, and later run or refine that workflow on request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taha2053](https://clawhub.ai/user/taha2053)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use Apprentice to teach agents repeatable local workflows by performing and narrating a task once, then reviewing the synthesized workflow before saving or running it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Observation logs and learned workflow files can persist sensitive instructions, private URLs, credentials, or customer data if a user teaches such material.

Mitigation: Avoid teaching sensitive workflows; inspect and delete raw observation logs or generated files that contain sensitive data.

Risk: Learned workflows may execute local shell scripts with broad local authority.

Mitigation: Preview generated files, inspect run.sh and SKILL.md, restrict workflow names and variables, and run only workflows you have reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taha2053/skills/apprentice)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON workflow records, and shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workflows are local files that users can preview, edit, approve, and run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
